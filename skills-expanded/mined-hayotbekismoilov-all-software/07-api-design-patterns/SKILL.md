---
name: api-design-patterns
description: |
  RESTful API design patterns: versioning, pagination, filtering, sorting, webhooks, idempotency.
  Apply when designing or building any API endpoint. Covers request/response contracts,
  error codes, pagination cursor vs offset, webhook signatures, and API documentation standards.
---

# API Design Patterns

## Versioning Strategy
```
/api/v1/users          — stable production
/api/v2/users          — new version (breaking changes)
/api/v1/users          — v1 maintained for 6 months after v2 launch, then deprecated
```
Never break existing endpoints — always add a new version.

## Pagination

### Cursor-Based (Preferred for large datasets)
```json
// Request: GET /api/v1/orders?cursor=eyJpZCI6MTAwfQ&limit=20
// Response:
{
  "data": [...],
  "meta": {
    "next_cursor": "eyJpZCI6MTIwfQ",
    "prev_cursor": "eyJpZCI6MTAxfQ",
    "has_next": true,
    "has_prev": false,
    "limit": 20
  }
}
```

### Offset-Based (Simple use cases only)
```json
// Request: GET /api/v1/products?page=3&per_page=20
{
  "data": [...],
  "meta": { "page": 3, "per_page": 20, "total": 847, "total_pages": 43 }
}
```

## Filtering & Sorting
```
GET /api/v1/products?
  category=electronics
  &price_min=100
  &price_max=500
  &status=active
  &sort=price_asc        # or price_desc, created_at_desc
  &search=wireless
  &page=1
  &per_page=20
```

## Idempotency Keys
```python
# For payment and order endpoints — prevent duplicate processing
@app.post("/api/v1/payments")
async def create_payment(
    request: PaymentRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key")
):
    # Check if already processed
    cached = await redis.get(f"idempotency:{idempotency_key}")
    if cached:
        return json.loads(cached)
    
    result = await process_payment(request)
    # Cache result for 24 hours
    await redis.setex(f"idempotency:{idempotency_key}", 86400, json.dumps(result))
    return result
```

## Webhook Design
```python
# Sign all webhooks with HMAC-SHA256
import hmac, hashlib

def sign_webhook(payload: dict, secret: str) -> str:
    body = json.dumps(payload, sort_keys=True)
    return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()

# Receiver must verify signature
def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)  # Constant-time comparison
```

## Standard Error Codes
```python
ERROR_CODES = {
    # Auth
    "AUTH_MISSING_TOKEN": (401, "Authentication token is required"),
    "AUTH_INVALID_TOKEN": (401, "Token is invalid or expired"),
    "AUTH_INSUFFICIENT_PERMISSION": (403, "You don't have permission for this action"),
    
    # Validation
    "VALIDATION_ERROR": (400, "Request validation failed"),
    "RESOURCE_NOT_FOUND": (404, "Requested resource does not exist"),
    "RESOURCE_CONFLICT": (409, "Resource already exists"),
    
    # Rate limiting
    "RATE_LIMIT_EXCEEDED": (429, "Too many requests — retry after {retry_after}s"),
    
    # Business logic
    "INSUFFICIENT_STOCK": (422, "Not enough stock available"),
    "PAYMENT_FAILED": (422, "Payment processing failed"),
    "ORDER_NOT_CANCELLABLE": (422, "Order cannot be cancelled in current status"),
}
```
