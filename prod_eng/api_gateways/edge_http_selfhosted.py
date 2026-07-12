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