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
    "products": "http:localhost:8002",
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
) -> AsyncInterator[bytes]:
    try:
        async for chunk in response.aiter_raw():
            yield chunk
    finally:
        await response.close()

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