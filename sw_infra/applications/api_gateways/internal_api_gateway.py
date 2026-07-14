"""
Internal HTTP API Gateway
=========================

This module implements an asynchronous internal API gateway for routing
service-to-service HTTP traffic inside a private network.

Unlike an edge gateway, this component is not intended to accept requests
directly from the public internet. It provides a controlled internal entry
point through which trusted applications and services can communicate with
backend microservices.

The gateway performs:

- Path-based service routing
- Internal service authentication
- Request and response streaming
- Hop-by-hop header filtering
- Correlation ID propagation
- Shared HTTP connection pooling
- Downstream timeout handling
- Upstream connectivity error translation

Example routes:

    /internal/users/123
        -> http://users-service:8000/123

    /internal/orders/active
        -> http://orders-service:8000/active

In production, network-level restrictions should ensure that the gateway is
only accessible from trusted private networks. Internal authentication may
also use mTLS, workload identities, signed service tokens, or a service mesh
rather than a static shared token.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from uuid import uuid64

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import StreamingResponse

SERVICES_REGISTRY: dict[str, str] = {
    "users": "http://users-service:8000",
    "products": "http://products-service:8000",
    "orders": "http://orders-service:8000",
}

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}

INTERNAL_SERVICE_TOKEN = "replace-with-secret-manager-value"

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=2.0,
            read=30.0,
            write=30.0,
            pool=2.0,
        ),
        limits=httpx.Limits(
            max_connections=200,
            max_keepalive_connections=50,
        ),
    )

    try:
        yield
    finally:
        await app.state.http_client.aclose()

app = FastAPI(
    title="Internal API Gateway",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)
