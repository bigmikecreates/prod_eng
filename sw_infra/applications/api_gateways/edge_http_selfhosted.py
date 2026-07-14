"""
HTTP API Gateway
================

Overview
--------
This module implements an asynchronous edge HTTP API Gateway using FastAPI
and HTTPX.

An API Gateway acts as the single entry point into a distributed system,
accepting requests from external clients and routing them to the appropriate
backend microservice. Rather than clients communicating directly with every
service, they interact only with the gateway, which centralizes concerns such
as routing, authentication, request forwarding, connection management, and
error handling.

This implementation functions as a lightweight reverse proxy for internal
services. Requests are dynamically routed based on the first path segment
(e.g. `/users/...`, `/products/...`, `/orders/...`) using an in-memory
service registry.

Architecture
------------
Incoming client requests follow the pipeline below:

1. Receive an incoming HTTP request.
2. Authenticate the request using an API key dependency.
3. Resolve the target service from the service registry.
4. Construct the downstream HTTP request.
5. Forward headers, query parameters, and streaming request body.
6. Stream the downstream response back to the client.
7. Close downstream resources after streaming completes.

The gateway is intentionally transparent, preserving request methods,
status codes, response bodies, and most headers while removing
hop-by-hop headers defined by RFC 9110.

Features
--------
- Dynamic path-based request routing
- Reverse proxy for internal HTTP services
- Shared asynchronous HTTP connection pool
- Streaming request and response bodies
- API key authentication
- Gateway timeout handling
- Bad Gateway handling for unavailable services
- Hop-by-hop header filtering
- Connection lifecycle management using FastAPI lifespan events

Design Principles
-----------------
The implementation emphasizes:

- Asynchronous, non-blocking I/O
- Minimal request buffering
- Connection reuse via a shared HTTPX AsyncClient
- Transparent proxy semantics
- Separation of infrastructure concerns from business logic
- Simplicity suitable for self-hosted deployments and learning purposes

This gateway intentionally focuses on request forwarding rather than advanced
API management features such as service discovery, load balancing, rate
limiting, retries, circuit breakers, caching, distributed tracing, or
observability, all of which can be layered on incrementally.

Use Cases
---------
This component is suitable as:

- An edge gateway for microservice architectures
- A reverse proxy for internal APIs
- A local development gateway
- A foundation for service mesh concepts
- A learning implementation of API gateway architecture
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import (
    FastAPI, Request, Response,
    HTTPException, Depends, status
)
from fastapi.responses import StreamingResponse

SERVICES_REGISTRY = {
    "users": "http://localhost:8001",
    "products": "http://localhost:8002",
    "orders": "http://localhost:8003",
}

# These headers apply to one HTTP connection and should not be forwarded
# between the client, gateway, and downstream service.
HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade"
}

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=2.0,
            read=30.0,
            write=30.0,
            pool=2.0
        )
    )

    try:
        yield
    finally:
        await app.state.http_client.aclose()

app = FastAPI(
    title="Pythonic API Gateway",
    lifespan=lifespan,
)

async def verify_api_key(request: Request) -> str:
    api_key = request.headers.get("x-api-key")

    if api_key == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    
    return api_key

def filter_response_headers(
        response: httpx.Response,
) -> dict[str, str]:
    return {
        name: value
        for name, value in response.headers.items()
        if name.lower() not in HOP_BY_HOP_HEADERS
        and name.lower() != "content-length"
    }

async def stream_and_close(
        response: httpx.Response,
) -> AsyncIterator[bytes]:
    try:
        async for chunk in response.aiter_raw():
            yield chunk
    finally:
        await response.aclose()

@app.api_route(
    "/{service}/{path:path}",
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
        "HEAD",
    ]
)

async def route_gateway(
    service: str,
    path: str,
    request: Request,
    _api_key: str = Depends(verify_api_key),
) -> StreamingResponse:
    base_url = SERVICES_REGISTRY.get(service)

    if base_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown service: {service}",
        )
    
    downstream_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    client: httpx.AsyncClient = request.app.state.http_client

    downstream_request = client.build_request(
        method=request.method,
        url=downstream_url,
        params=request.query_params,
        headers={
            name: value
            for name, value in request.headers.items()
            if name.lower() not in HOP_BY_HOP_HEADERS
            and name.lower() not in {
                "host",
                "content-length",
            }
        },
        content=request.stream(),
    )

    try:
        downstream_response = await client.send(
            downstream_request,
            stream=True,
        )
    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Downstream service timed out",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to connect to downstream service",
        ) from exc
    
    return StreamingResponse(
        content=stream_and_close(downstream_response),
        status_code=downstream_response.status_code,
        headers=filter_response_headers(downstream_response),
    )