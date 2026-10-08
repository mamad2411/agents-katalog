---
name: api-integrations
description: API connector patterns for OAuth lifecycle, webhooks, rate limiting, and agent-native tool calling.
origin: AI Dev Kit
---

# API Integrations

Agent-native integration patterns for external APIs, OAuth, webhooks, and rate limiting.

## When to Use

- Connecting to third-party APIs (Stripe, Slack, GitHub, Twilio, etc.)
- Implementing OAuth 2.0 / OIDC authentication flows
- Building webhook receivers and event handlers
- Adding rate limiting and retry logic to external calls
- Creating agent-callable tool wrappers for APIs

## OAuth 2.0 Lifecycle

### Authorization Code Flow (with PKCE)

```python
# FastAPI OAuth2 with PKCE
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="provider",
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    server_metadata_url="https://provider.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@app.route("/login")
async def login(request):
    redirect_uri = request.url_for("auth")
    return await oauth.provider.authorize_redirect(request, redirect_uri)

@app.route("/auth")
async def auth(request):
    token = await oauth.provider.authorize_access_token(request)
    user = await oauth.provider.parse_id_token(request, token)
    # Store token, redirect with session
```

### Token Refresh Pattern

```python
async def get_valid_token(client):
    token = load_stored_token()
    if token.expires_at < now() + timedelta(minutes=5):
        token = await client.refresh_token(token.refresh_token)
        save_token(token)
    return token.access_token
```

### OAuth Token Storage

- Never store tokens in cookies or localStorage
- Use httpOnly, secure, sameSite=strict cookies for web
- For services: encrypt tokens at rest with KMS
- Rotate refresh tokens on each use

## Webhook Patterns

### Receiver with Signature Verification

```python
from fastapi import APIRouter, Request, HTTPException
import hmac, hashlib

router = APIRouter()

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not verify_signature(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET):
        raise HTTPException(401, "Invalid signature")

    event = json.loads(payload)
    await handle_event(event)
    return {"received": True}

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### Webhook Reliability

- Respond 200 within 5 seconds
- Process asynchronously (BackgroundTasks, Celery, SQS)
- Log all events with idempotency key
- Retry on failure with exponential backoff
- Dead letter queue for unrecoverable events

## Rate Limiting

### Token Bucket Pattern

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.buckets: dict[str, list[float]] = defaultdict(list)

    async def check(self, key: str) -> bool:
        now = time.time()
        window = [t for t in self.buckets[key] if now - t < self.period]
        self.buckets[key] = window
        if len(window) >= self.max_calls:
            return False
        self.buckets[key].append(now)
        return True

limiter = RateLimiter(max_calls=100, period=60.0)

@app.get("/api/external")
async def call_external(request: Request):
    ip = request.client.host
    if not await limiter.check(ip):
        raise HTTPException(429, "Rate limit exceeded")
    return await external_api.fetch()
```

### API Provider Rate Limits

- Track provider limits in config: `{ provider: { calls_per_minute, daily_limit } }`
- Enforce client-side before sending request
- Return 429 with `Retry-After` header
- Implement request queue for burst traffic

## Retry with Backoff

```python
import asyncio
from functools import wraps

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    jitter: bool = True,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as exc:
                    last_exc = exc
                    if attempt == max_retries:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    if jitter:
                        delay *= (0.5 + random.random())
                    await asyncio.sleep(delay)
            raise last_exc
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
async def call_api():
    return await httpx.get("https://api.provider.com/v1/data")
```

## Agent-Callable Tool Wrapper

```python
# Wrap API as a tool for agent calling
from pydantic import BaseModel, Field

class CreateInvoiceInput(BaseModel):
    customer_id: str
    amount: int
    currency: str = "usd"
    description: str = Field(..., max_length=500)

class CreateInvoiceResult(BaseModel):
    invoice_id: str
    status: str
    url: str

async def create_invoice(
    input: CreateInvoiceInput,
) -> CreateInvoiceResult:
    """Create an invoice in Stripe and return the payment URL."""
    # Implementation calls Stripe API
    # Agent can call this tool with structured input
    ...
```

## Pagination

```python
async def fetch_all_pages(
    client: httpx.AsyncClient,
    url: str,
    params: dict,
    max_pages: int = 50,
) -> list[dict]:
    """Fetch all pages with cursor-based pagination."""
    results = []
    page = 0
    while page < max_pages:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data["items"])
        cursor = data.get("next_cursor")
        if not cursor:
            break
        params["cursor"] = cursor
        page += 1
    return results
```

## Timeout and Circuit Breaker

```python
import httpx

client = httpx.AsyncClient(
    timeout=httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=10.0)
)

# Circuit breaker pattern
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 60.0):
        self.failures = 0
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = "closed"
        self.last_failure: float | None = None

    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure > self.reset_timeout:
                self.state = "half-open"
            else:
                raise CircuitOpenError("circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
            return result
        except Exception:
            self.failures += 1
            self.last_failure = time.time()
            if self.failures >= self.threshold:
                self.state = "open"
            raise
```

## Verification

- Test OAuth flow with mock token endpoint
- Verify webhook signature validation rejects bad signatures
- Confirm rate limiter returns 429 after threshold
- Check retry logic with failing mock server
- Validate circuit breaker opens and resets correctly
