---
name: sdk-design
description: Design and build client SDKs for APIs. Outputs idiomatic client libraries with auth handling, retry logic, pagination, error types, and developer experience best practices across Python, TypeScript, and Go.
argument-hint: [API type, target languages, authentication method, distribution channel]
allowed-tools: Read, Write, Bash
---

# SDK Design

A great SDK makes your API feel native to the language it's written in. It hides auth, retries, pagination, and serialization — so developers write business logic, not plumbing.

## Process

1. **Design the interface first** — how would the ideal SDK look from the caller's perspective?
2. **Generate from OpenAPI/proto** — use code generation where possible, customize where it matters.
3. **Handle auth transparently** — credential storage, token refresh, header injection.
4. **Wrap errors** — typed exceptions, not raw HTTP status codes.
5. **Implement retry logic** — exponential backoff with jitter for transient failures.
6. **Abstract pagination** — iterators that hide cursor management.
7. **Add request/response logging** — configurable, scrubs secrets.
8. **Publish and version** — semantic versioning, changelog, migration guides.
9. **Write examples** — real use cases, not just API surface coverage.

## Output Format

### Python SDK

```python
# acme_sdk/__init__.py
from .client import AcmeClient
from .models import Order, OrderItem, User
from .exceptions import (
    AcmeError, AuthenticationError, RateLimitError,
    NotFoundError, ValidationError, ServerError
)

__version__ = "1.4.0"
__all__ = [
    "AcmeClient",
    "Order", "OrderItem", "User",
    "AcmeError", "AuthenticationError", "RateLimitError",
    "NotFoundError", "ValidationError", "ServerError",
]
```

```python
# acme_sdk/client.py
import httpx
import time
import random
import logging
from typing import Iterator, Optional, TypeVar, Generic
from dataclasses import dataclass

from .exceptions import (
    AcmeError, AuthenticationError, RateLimitError,
    NotFoundError, ValidationError, ServerError
)
from .models import Order, User
from .auth import TokenAuth, ApiKeyAuth

logger = logging.getLogger("acme_sdk")

T = TypeVar("T")

@dataclass
class Page(Generic[T]):
    items: list[T]
    next_cursor: Optional[str]
    has_more: bool
    total: Optional[int] = None


class AcmeClient:
    """
    Acme API client.
    
    Usage:
        # API key auth
        client = AcmeClient(api_key="your-key")
        
        # OAuth (auto-refreshes tokens)
        client = AcmeClient(
            client_id="...",
            client_secret="...",
            token_url="https://auth.acme.com/token"
        )
        
        # Custom base URL (e.g., staging)
        client = AcmeClient(api_key="...", base_url="https://staging.api.acme.com")
    """
    
    DEFAULT_BASE_URL = "https://api.acme.com/v1"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
    
    def __init__(
        self,
        api_key: str = None,
        client_id: str = None,
        client_secret: str = None,
        token_url: str = None,
        base_url: str = None,
        timeout: float = None,
        max_retries: int = None,
        http_client: httpx.Client = None,
    ):
        if api_key:
            self._auth = ApiKeyAuth(api_key)
        elif client_id and client_secret:
            self._auth = TokenAuth(client_id, client_secret, token_url)
        else:
            raise ValueError("Provide either api_key or client_id + client_secret")
        
        self._base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout or self.DEFAULT_TIMEOUT
        self._max_retries = max_retries if max_retries is not None else self.DEFAULT_MAX_RETRIES
        
        self._http = http_client or httpx.Client(
            timeout=self._timeout,
            headers={"User-Agent": f"acme-python-sdk/1.4.0"},
            follow_redirects=True,
        )
        
        # Sub-clients (namespaced API access)
        self.orders = OrdersClient(self)
        self.users = UsersClient(self)
        self.products = ProductsClient(self)
    
    def _request(
        self,
        method: str,
        path: str,
        params: dict = None,
        json: dict = None,
        **kwargs
    ) -> dict:
        url = f"{self._base_url}/{path.lstrip('/')}"
        headers = self._auth.get_headers()
        
        last_exception = None
        
        for attempt in range(self._max_retries + 1):
            try:
                response = self._http.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    headers=headers,
                    **kwargs
                )
                
                # Log request (scrub auth headers)
                logger.debug(
                    f"{method} {url} → {response.status_code}",
                    extra={"params": params, "status": response.status_code}
                )
                
                # Handle errors
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 1))
                    if attempt < self._max_retries:
                        time.sleep(retry_after)
                        continue
                    raise RateLimitError(
                        f"Rate limit exceeded. Retry after {retry_after}s",
                        retry_after=retry_after,
                        response=response
                    )
                
                if response.status_code in self.DEFAULT_RETRY_STATUS_CODES and attempt < self._max_retries:
                    delay = min(2 ** attempt * 0.5, 30) * (0.5 + random.random())
                    logger.warning(f"HTTP {response.status_code}, retrying in {delay:.1f}s (attempt {attempt + 1})")
                    time.sleep(delay)
                    continue
                
                self._raise_for_status(response)
                
                if response.status_code == 204:  # No content
                    return {}
                
                return response.json()
            
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exception = e
                if attempt < self._max_retries:
                    delay = min(2 ** attempt * 0.5, 30) * (0.5 + random.random())
                    logger.warning(f"Connection error: {e}, retrying in {delay:.1f}s")
                    time.sleep(delay)
                    continue
                raise AcmeError(f"Connection failed after {self._max_retries} retries: {e}") from e
        
        if last_exception:
            raise AcmeError("Max retries exceeded") from last_exception
    
    def _raise_for_status(self, response: httpx.Response):
        if response.status_code < 400:
            return
        
        try:
            error_data = response.json()
        except Exception:
            error_data = {"message": response.text}
        
        message = error_data.get("message", "Unknown error")
        error_code = error_data.get("code", "UNKNOWN")
        
        exceptions = {
            401: AuthenticationError,
            403: AuthenticationError,
            404: NotFoundError,
            422: ValidationError,
        }
        
        exc_class = exceptions.get(response.status_code, ServerError if response.status_code >= 500 else AcmeError)
        
        raise exc_class(
            message,
            status_code=response.status_code,
            error_code=error_code,
            response=response
        )
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self._http.close()
    
    def close(self):
        self._http.close()


class OrdersClient:
    def __init__(self, client: AcmeClient):
        self._client = client
    
    def create(
        self,
        user_id: str,
        items: list[dict],
        idempotency_key: str = None
    ) -> Order:
        """
        Create a new order.
        
        Args:
            user_id: The user placing the order
            items: List of {product_id, quantity} dicts
            idempotency_key: Optional key to prevent duplicate orders
        
        Returns:
            Order: The created order
        
        Raises:
            ValidationError: If items are invalid
            NotFoundError: If user doesn't exist
        
        Example:
            order = client.orders.create(
                user_id="usr_abc123",
                items=[{"product_id": "prd_xyz", "quantity": 2}]
            )
        """
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        
        data = self._client._request(
            "POST", "/orders",
            json={"user_id": user_id, "items": items},
            headers=headers
        )
        return Order(**data)
    
    def get(self, order_id: str) -> Order:
        """Get an order by ID."""
        data = self._client._request("GET", f"/orders/{order_id}")
        return Order(**data)
    
    def list(
        self,
        user_id: str = None,
        status: str = None,
        page_size: int = 20,
    ) -> Iterator[Order]:
        """
        Iterate over orders. Handles pagination automatically.
        
        Example:
            for order in client.orders.list(user_id="usr_abc", status="delivered"):
                print(order.id, order.total)
        """
        cursor = None
        
        while True:
            params = {"page_size": page_size}
            if user_id:
                params["user_id"] = user_id
            if status:
                params["status"] = status
            if cursor:
                params["cursor"] = cursor
            
            data = self._client._request("GET", "/orders", params=params)
            
            items = [Order(**item) for item in data.get("items", [])]
            for item in items:
                yield item
            
            cursor = data.get("next_cursor")
            if not cursor:
                break
    
    def list_page(
        self,
        cursor: str = None,
        page_size: int = 20,
        **filters
    ) -> Page[Order]:
        """Get a single page (for manual pagination control)."""
        params = {"page_size": page_size, **filters}
        if cursor:
            params["cursor"] = cursor
        
        data = self._client._request("GET", "/orders", params=params)
        
        return Page(
            items=[Order(**item) for item in data.get("items", [])],
            next_cursor=data.get("next_cursor"),
            has_more=bool(data.get("next_cursor")),
            total=data.get("total"),
        )
    
    def cancel(self, order_id: str, reason: str = None) -> Order:
        """Cancel an order."""
        data = self._client._request(
            "POST", f"/orders/{order_id}/cancel",
            json={"reason": reason} if reason else {}
        )
        return Order(**data)
```

```python
# acme_sdk/exceptions.py
from typing import Optional
import httpx

class AcmeError(Exception):
    """Base exception for all Acme SDK errors."""
    def __init__(
        self,
        message: str,
        status_code: int = None,
        error_code: str = None,
        response: httpx.Response = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.response = response
    
    def __repr__(self):
        return f"{self.__class__.__name__}(message={self.message!r}, status_code={self.status_code})"

class AuthenticationError(AcmeError):
    """Invalid credentials or insufficient permissions."""

class RateLimitError(AcmeError):
    """API rate limit exceeded."""
    def __init__(self, message: str, retry_after: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after

class NotFoundError(AcmeError):
    """Resource not found."""

class ValidationError(AcmeError):
    """Request data is invalid."""
    @property
    def validation_errors(self) -> list:
        if self.response:
            return self.response.json().get("errors", [])
        return []

class ServerError(AcmeError):
    """Acme API server error (5xx)."""
```

### TypeScript SDK

```typescript
// src/client.ts
import type { Order, User, Page, CreateOrderParams } from './types';
import { AcmeError, AuthError, NotFoundError, RateLimitError, ValidationError } from './errors';

interface ClientOptions {
  apiKey?: string;
  clientId?: string;
  clientSecret?: string;
  baseUrl?: string;
  timeout?: number;
  maxRetries?: number;
}

export class AcmeClient {
  private readonly baseUrl: string;
  private readonly timeout: number;
  private readonly maxRetries: number;
  private token: string | null = null;
  private tokenExpiry: Date | null = null;
  
  readonly orders: OrdersClient;
  readonly users: UsersClient;

  constructor(private readonly options: ClientOptions) {
    this.baseUrl = options.baseUrl ?? 'https://api.acme.com/v1';
    this.timeout = options.timeout ?? 30_000;
    this.maxRetries = options.maxRetries ?? 3;
    this.orders = new OrdersClient(this);
    this.users = new UsersClient(this);
  }

  async request<T>(
    method: string,
    path: string,
    options: { params?: Record<string, string>; body?: unknown; headers?: Record<string, string> } = {}
  ): Promise<T> {
    const url = new URL(path.replace(/^\//, ''), this.baseUrl + '/');
    if (options.params) {
      for (const [key, value] of Object.entries(options.params)) {
        url.searchParams.set(key, value);
      }
    }

    const authHeaders = await this.getAuthHeaders();
    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);

      try {
        const response = await fetch(url.toString(), {
          method,
          headers: {
            'Content-Type': 'application/json',
            'User-Agent': 'acme-ts-sdk/1.4.0',
            ...authHeaders,
            ...options.headers,
          },
          body: options.body ? JSON.stringify(options.body) : undefined,
          signal: controller.signal,
        });
        clearTimeout(timeoutId);

        if (response.status === 429) {
          const retryAfter = parseInt(response.headers.get('Retry-After') ?? '1', 10);
          if (attempt < this.maxRetries) {
            await delay(retryAfter * 1000);
            continue;
          }
          throw new RateLimitError('Rate limit exceeded', retryAfter);
        }

        if ([500, 502, 503, 504].includes(response.status) && attempt < this.maxRetries) {
          const backoff = Math.min(Math.pow(2, attempt) * 500, 30_000);
          await delay(backoff * (0.5 + Math.random()));
          continue;
        }

        await this.throwForStatus(response);

        if (response.status === 204) return {} as T;
        return response.json() as Promise<T>;

      } catch (err) {
        clearTimeout(timeoutId);
        if (err instanceof AcmeError) throw err;
        lastError = err as Error;
        if (attempt < this.maxRetries) {
          await delay(Math.pow(2, attempt) * 500);
        }
      }
    }

    throw new AcmeError(`Request failed after ${this.maxRetries} retries: ${lastError?.message}`);
  }

  private async throwForStatus(response: Response): Promise<void> {
    if (response.ok) return;
    
    const body = await response.json().catch(() => ({ message: 'Unknown error' }));
    const message = body.message ?? 'Unknown error';

    switch (response.status) {
      case 401: case 403: throw new AuthError(message);
      case 404: throw new NotFoundError(message);
      case 422: throw new ValidationError(message, body.errors);
      default:
        if (response.status >= 500) throw new AcmeError(message, response.status);
        throw new AcmeError(message, response.status);
    }
  }

  private async getAuthHeaders(): Promise<Record<string, string>> {
    if (this.options.apiKey) {
      return { 'X-API-Key': this.options.apiKey };
    }
    // OAuth token refresh logic...
    return { 'Authorization': `Bearer ${await this.refreshToken()}` };
  }
}

class OrdersClient {
  constructor(private readonly client: AcmeClient) {}

  async create(params: CreateOrderParams): Promise<Order> {
    return this.client.request<Order>('POST', '/orders', { body: params });
  }

  async get(orderId: string): Promise<Order> {
    return this.client.request<Order>('GET', `/orders/${orderId}`);
  }

  async *list(filters: { userId?: string; status?: string } = {}): AsyncIterable<Order> {
    let cursor: string | undefined;
    do {
      const page = await this.client.request<Page<Order>>('GET', '/orders', {
        params: { ...filters, ...(cursor ? { cursor } : {}) },
      });
      for (const item of page.items) yield item;
      cursor = page.nextCursor ?? undefined;
    } while (cursor);
  }
}

function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

### Publishing

```bash
# Python — PyPI
pip install build twine
python -m build
twine upload dist/*

# pyproject.toml
[project]
name = "acme-sdk"
version = "1.4.0"
requires-python = ">=3.9"
dependencies = ["httpx>=0.25.0"]

# TypeScript — npm
npm publish --access public
```

## Rules

- **Design the interface before the implementation** — write usage examples first.
- **One SDK per language** — don't share code across languages; idiomatic matters more than DRY.
- **Typed return values** — return domain objects, not raw dicts.
- **Handle token refresh transparently** — callers should never deal with expired tokens.
- **Wrap pagination with iterators** — never make callers manage cursors manually.
- **Exponential backoff with jitter** — always jitter to prevent thundering herd.
- **Typed exceptions** — `NotFoundError` beats `HTTPError(status_code=404)`.
- **Log but don't expose secrets** — scrub auth headers from debug logs.
- **Semantic versioning** — breaking changes require a major version bump.
- **Write a changelog** — every release documents what changed and why.
