---
name: python-api-client
description: "When to activate: httpx, API clients, retry logic, auth headers, rate limiting client-side, OpenAPI client generation"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python API Client Patterns

## httpx Async Client
```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class APIClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=httpx.Timeout(timeout, connect=5.0),
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        )
    
    async def __aenter__(self) -> "APIClient":
        return self
    
    async def __aexit__(self, *_) -> None:
        await self._client.aclose()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.TransportError)),
    )
    async def get(self, path: str, **params) -> dict:
        response = await self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()
    
    async def post(self, path: str, body: dict) -> dict:
        response = await self._client.post(path, json=body)
        response.raise_for_status()
        return response.json()

# Usage
async with APIClient("https://api.example.com", settings.api_key) as client:
    user = await client.get("/v1/users/123")
```

## Rate-Limiting Client
```python
import asyncio
import time

class RateLimitedClient:
    def __init__(self, client: APIClient, calls_per_second: float = 10.0) -> None:
        self._client = client
        self._min_interval = 1.0 / calls_per_second
        self._last_call: float = 0.0
        self._lock = asyncio.Lock()
    
    async def get(self, path: str, **params) -> dict:
        async with self._lock:
            elapsed = time.monotonic() - self._last_call
            if elapsed < self._min_interval:
                await asyncio.sleep(self._min_interval - elapsed)
            self._last_call = time.monotonic()
        return await self._client.get(path, **params)
```

## Pagination Helper
```python
async def paginate(client: APIClient, path: str, page_size: int = 100) -> list[dict]:
    items = []
    page = 1
    while True:
        response = await client.get(path, page=page, per_page=page_size)
        items.extend(response["data"])
        if len(response["data"]) < page_size or not response.get("has_more"):
            break
        page += 1
    return items
```
