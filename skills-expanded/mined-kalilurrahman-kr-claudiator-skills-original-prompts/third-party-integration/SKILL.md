---
name: third-party-integration
description: Integrate third-party services via OAuth flows, webhook handling, and API clients. Outputs OAuth implementation, webhook verification, idempotent event handling, and graceful degradation patterns.
argument-hint: [third-party service, integration type, auth method, data flow direction]
allowed-tools: Read, Write, Bash
---

# Third-Party Integration

Integrating with external services is one of the highest-risk activities in software engineering. External APIs change, go down, send duplicate events, and have rate limits. Design integrations to be resilient, verifiable, and replaceable.

## Process

1. **Map the integration** — what data flows in/out, what auth is needed, what events trigger what.
2. **Implement OAuth (if required)** — authorization code flow with PKCE for user-delegated access.
3. **Secure webhook endpoints** — signature verification before processing any payload.
4. **Idempotent event handlers** — webhook redelivery is guaranteed; your handler must be safe to call twice.
5. **Graceful degradation** — what happens when the third party is down?
6. **Test with real sandbox** — don't just mock; validate against the real API.
7. **Monitor integration health** — rate limit approaching, error rate, webhook lag.

## Output Format

### OAuth 2.0 Authorization Code Flow

```python
# oauth/client.py
import secrets
import hashlib
import base64
from urllib.parse import urlencode, urlparse, parse_qs
import httpx
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

@dataclass
class OAuthToken:
    access_token: str
    refresh_token: str | None
    expires_at: datetime
    scope: str
    token_type: str = "Bearer"
    
    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at - timedelta(minutes=5)

class OAuthClient:
    """
    OAuth 2.0 Authorization Code flow with PKCE.
    Supports: Stripe, GitHub, Google, Slack, Salesforce, etc.
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        authorization_url: str,
        token_url: str,
        redirect_uri: str,
        scopes: list[str],
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_url = authorization_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self._http = httpx.Client(timeout=30.0)
    
    def get_authorization_url(self, user_id: str) -> tuple[str, str]:
        """
        Generate authorization URL and state token.
        Store state in session before redirecting.
        
        Returns:
            (authorization_url, state) — redirect user to URL, store state
        """
        # PKCE: code verifier + challenge
        code_verifier = secrets.token_urlsafe(96)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).rstrip(b"=").decode()
        
        # State: prevents CSRF
        state = secrets.token_urlsafe(32)
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "response_type": "code",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        
        # Store state → code_verifier mapping (in Redis/session)
        self._store_pkce_state(state, code_verifier, user_id)
        
        url = f"{self.authorization_url}?{urlencode(params)}"
        return url, state
    
    def exchange_code(self, code: str, state: str) -> OAuthToken:
        """Exchange authorization code for tokens. Call from redirect handler."""
        
        # Verify state and retrieve code_verifier
        pkce_data = self._get_pkce_state(state)
        if not pkce_data:
            raise ValueError("Invalid or expired OAuth state")
        
        response = self._http.post(
            self.token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code_verifier": pkce_data["code_verifier"],
            },
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        
        data = response.json()
        return self._parse_token_response(data)
    
    def refresh_token(self, refresh_token: str) -> OAuthToken:
        """Refresh expired access token."""
        response = self._http.post(
            self.token_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return self._parse_token_response(response.json())
    
    def get_valid_token(self, stored_token: OAuthToken) -> OAuthToken:
        """Return valid token, refreshing if expired."""
        if not stored_token.is_expired:
            return stored_token
        
        if not stored_token.refresh_token:
            raise TokenExpiredError("Access token expired and no refresh token available")
        
        new_token = self.refresh_token(stored_token.refresh_token)
        self._store_token(new_token)
        return new_token
    
    def _parse_token_response(self, data: dict) -> OAuthToken:
        expires_in = data.get("expires_in", 3600)
        return OAuthToken(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=expires_in),
            scope=data.get("scope", ""),
        )


# FastAPI OAuth routes
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/oauth")

github_oauth = OAuthClient(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    authorization_url="https://github.com/login/oauth/authorize",
    token_url="https://github.com/login/oauth/access_token",
    redirect_uri=f"{settings.BASE_URL}/oauth/github/callback",
    scopes=["read:user", "user:email", "repo"],
)

@router.get("/github")
async def github_login(request: Request, user_id: str):
    url, state = github_oauth.get_authorization_url(user_id)
    request.session["oauth_state"] = state
    return RedirectResponse(url)

@router.get("/github/callback")
async def github_callback(request: Request, code: str, state: str):
    if request.session.get("oauth_state") != state:
        raise HTTPException(400, "Invalid OAuth state")
    
    try:
        token = github_oauth.exchange_code(code, state)
        user_id = request.session.get("user_id")
        await token_store.save(user_id, "github", token)
        return RedirectResponse("/dashboard?connected=github")
    except Exception as e:
        raise HTTPException(400, f"OAuth failed: {str(e)}")
```

### Webhook Handling

```python
# webhooks/handler.py
import hmac
import hashlib
import json
import time
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from functools import wraps

router = APIRouter(prefix="/webhooks")

def verify_stripe_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify Stripe webhook signature (HMAC-SHA256)."""
    # Stripe format: t=timestamp,v1=signature
    parts = {k: v for k, v in (item.split("=", 1) for item in signature.split(","))}
    timestamp = parts.get("t", "")
    sig = parts.get("v1", "")
    
    # Reject timestamps older than 5 minutes (replay protection)
    if abs(time.time() - int(timestamp)) > 300:
        return False
    
    expected = hmac.new(
        secret.encode(),
        f"{timestamp}.{payload.decode()}".encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, sig)


def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub webhook signature (SHA-256)."""
    expected = "sha256=" + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/stripe")
async def stripe_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.body()
    signature = request.headers.get("Stripe-Signature", "")
    
    if not verify_stripe_signature(payload, signature, settings.STRIPE_WEBHOOK_SECRET):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    event = json.loads(payload)
    
    # Return 200 immediately — process in background
    # Stripe retries for up to 3 days if it doesn't receive 2xx within 30s
    background_tasks.add_task(process_stripe_event, event)
    return {"received": True}


async def process_stripe_event(event: dict):
    """Idempotent event processor — safe to call multiple times."""
    event_id = event["id"]
    event_type = event["type"]
    
    # Idempotency: check if already processed
    if await idempotency_store.exists(f"stripe:{event_id}"):
        logger.info(f"Skipping already-processed Stripe event {event_id}")
        return
    
    try:
        handlers = {
            "payment_intent.succeeded": handle_payment_succeeded,
            "payment_intent.payment_failed": handle_payment_failed,
            "customer.subscription.deleted": handle_subscription_cancelled,
            "invoice.payment_failed": handle_invoice_failed,
        }
        
        handler = handlers.get(event_type)
        if handler:
            await handler(event["data"]["object"])
        else:
            logger.info(f"Unhandled Stripe event type: {event_type}")
        
        # Mark as processed
        await idempotency_store.set(f"stripe:{event_id}", "1", ex=86400 * 30)
    
    except Exception as e:
        logger.error(f"Failed to process Stripe event {event_id}: {e}")
        # Don't re-raise — returning 200 to Stripe prevents retry storm
        # But do alert
        await alert(f"Stripe webhook processing failed: {event_id}", severity="high")


async def handle_payment_succeeded(payment_intent: dict):
    order_id = payment_intent.get("metadata", {}).get("order_id")
    if not order_id:
        logger.warning(f"PaymentIntent {payment_intent['id']} has no order_id metadata")
        return
    
    await order_service.mark_paid(
        order_id=order_id,
        payment_id=payment_intent["id"],
        amount_cents=payment_intent["amount_received"],
    )
```

### Rate Limit Aware API Client

```python
# integrations/base_client.py
import time
import asyncio
from collections import deque
from threading import Lock

class RateLimitedClient:
    """API client with automatic rate limit handling."""
    
    def __init__(self, base_url: str, token: str, requests_per_second: float = 10):
        self._base_url = base_url
        self._token = token
        self._rps = requests_per_second
        self._request_times = deque()
        self._lock = Lock()
        self._http = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0,
        )
    
    async def _throttle(self):
        """Client-side rate limiting to avoid hitting API limits."""
        with self._lock:
            now = time.monotonic()
            window = 1.0
            
            # Remove old timestamps
            while self._request_times and now - self._request_times[0] > window:
                self._request_times.popleft()
            
            if len(self._request_times) >= self._rps:
                sleep_time = window - (now - self._request_times[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            
            self._request_times.append(time.monotonic())
    
    async def get(self, path: str, **kwargs) -> dict:
        await self._throttle()
        
        response = await self._http.get(path, **kwargs)
        
        # Handle rate limit response
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            logger.warning(f"Rate limited by API, waiting {retry_after}s")
            await asyncio.sleep(retry_after)
            return await self.get(path, **kwargs)  # Retry once
        
        # Log remaining quota
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")
        if remaining and int(remaining) < 100:
            logger.warning(f"API rate limit low: {remaining} remaining, resets {reset}")
        
        response.raise_for_status()
        return response.json()
```

### Integration Health Monitoring

```python
# monitoring/integration_health.py
from prometheus_client import Counter, Histogram, Gauge

# Metrics
webhook_received = Counter("webhooks_received_total", "Webhooks received", ["provider", "event_type"])
webhook_processed = Counter("webhooks_processed_total", "Webhooks processed", ["provider", "event_type", "status"])
api_call_duration = Histogram("third_party_api_duration_seconds", "Third-party API call duration", ["provider", "endpoint"])
api_errors = Counter("third_party_api_errors_total", "Third-party API errors", ["provider", "status_code"])
token_refresh_count = Counter("oauth_token_refreshes_total", "OAuth token refreshes", ["provider"])

# Health check endpoint
@app.get("/health/integrations")
async def integration_health():
    results = {}
    
    # Check Stripe connectivity
    try:
        await stripe_client.get("/v1/balance")
        results["stripe"] = {"status": "ok"}
    except Exception as e:
        results["stripe"] = {"status": "degraded", "error": str(e)}
    
    # Check GitHub API
    try:
        resp = await github_client.get("/rate_limit")
        remaining = resp["rate"]["remaining"]
        results["github"] = {
            "status": "ok" if remaining > 100 else "warning",
            "rate_limit_remaining": remaining,
        }
    except Exception as e:
        results["github"] = {"status": "error", "error": str(e)}
    
    overall = "ok"
    if any(r["status"] == "error" for r in results.values()):
        overall = "degraded"
    
    return {"status": overall, "integrations": results}
```

## Rules

- **Verify webhook signatures before processing** — never trust payload content alone.
- **Reject timestamps older than 5 minutes** — prevents replay attacks.
- **Return 200 immediately, process asynchronously** — slow webhook handlers cause provider retries.
- **Idempotent event handlers always** — webhook redelivery is guaranteed by all providers.
- **Log event IDs, not payloads** — event payloads may contain PII; log the ID for debugging.
- **Client-side rate limiting** — stay under API limits proactively rather than handling 429s reactively.
- **Token storage with encryption** — OAuth tokens in DB must be encrypted at rest.
- **Graceful degradation when third-party is down** — queue actions, cache responses, serve stale data.
- **Use provider sandbox/test environments** — never test webhook logic against production webhooks.
- **Rotate webhook secrets regularly** — treat webhook secrets like API keys; rotate on team changes.
