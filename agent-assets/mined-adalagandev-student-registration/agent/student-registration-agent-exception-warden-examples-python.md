# Exception Warden — Python Examples

**Framework basis:** All examples use **FastAPI 0.11x** (Starlette 0.4x
middleware, Pydantic v2 models) on **Python 3.12+**, with psycopg3-style
connection pools. Version-sensitive details:
- Python ≥ 3.9: exception chaining via `raise ... from e` (Rule 8) and
  parenthesized multi-item `with` (Rule 9) work as shown.
- Pydantic v2: validation error collection differs from v1
  (`e.errors()` shape changed) — Rule 10's mapping assumes v2.

The rules themselves are framework-agnostic — when the repo uses Flask,
Django/DRF, or another stack, translate the idiom (e.g., FastAPI's
`@app.exception_handler` ↔ Flask's `@app.errorhandler` ↔ DRF's
`custom_exception_handler`); the rule still applies unchanged.

## Rule 1 — Boundary handling only

```python
# VIOLATION — route handler builds its own error response
@app.get("/orders/{id}")
def get_order(id: str):
    try:
        return repo.find(id)
    except NotFound:
        return JSONResponse(status_code=404, content={"error": "not found"})

# CORRECT — raise typed exception; ONE global handler formats all responses
@app.get("/orders/{id}")
def get_order(id: str):
    return repo.find(id)  # raises OrderNotFoundError

@app.exception_handler(AppError)
def handle_app_error(request: Request, exc: AppError):
    return error_response(exc, request.state.request_id)
```

## Rule 2 — Zero internal leakage

```json
// VIOLATION — leaks driver, SQL host, and internals
{ "error": "psycopg2.OperationalError: connection to db-primary.internal:5432 failed" }

// CORRECT — generic body; full detail in server logs under the same request_id
{ "code": "INTERNAL_ERROR", "message": "An unexpected error occurred.",
  "details": [], "request_id": "req_8f3a1c" }
```

## Rule 3 — Expected vs unexpected

```python
# Expected: typed exception → 409, message safe to show the client
raise DuplicateEmailError("An account with this email already exists.")

# Unexpected: a KeyError bubbling up → global handler logs the stack trace,
# fires an alert, and the client sees only the generic INTERNAL_ERROR body.
```

## Rule 4 — One error schema

```json
{
  "code": "ORDER_NOT_FOUND",
  "message": "No order exists with the given ID.",
  "details": [],
  "request_id": "req_8f3a1c"
}
```

Violation: one endpoint returning `{"error": "..."}` while another returns
`{"code": ..., "message": ...}` — consolidate to one shape.

## Rule 5 — Codes for machines, messages for humans

```python
# VIOLATION — test parses human-readable message; breaks when copy changes
assert "already exists" in resp.json()["message"]

# CORRECT — assert on the stable code
assert resp.json()["code"] == "DUPLICATE_EMAIL"
```

## Rule 6 — Deliberate status mapping

```python
STATUS_MAP: dict[type[AppError], int] = {
    ValidationError:          400,
    UnauthenticatedError:     401,
    ForbiddenError:           403,
    NotFoundError:            404,
    ConflictError:            409,
    RateLimitError:           429,
    UpstreamUnavailableError: 502,
    UpstreamTimeoutError:     504,
    # anything unmapped → 500 + alert
}
```

Violation: `return {"success": False, "error": "..."}` with HTTP 200.

## Rule 7 — Request ID everywhere

```
Client sees:  { "code": "INTERNAL_ERROR", ..., "request_id": "req_8f3a1c" }
Server log:   ERROR req_8f3a1c POST /orders — OrderRepoError: ...
              Traceback (most recent call last): ...
```

```python
# Middleware: generate/propagate the ID before anything else
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request.state.request_id = request.headers.get("x-request-id", f"req_{uuid4().hex[:6]}")
    return await call_next(request)
```

## Rule 8 — Catch only what you handle

```python
# VIOLATION — swallows everything, discards original trace
try:
    charge(order)
except Exception as e:
    logger.error(e)
    raise PaymentError("failed")

# CORRECT — typed catch, chained cause
try:
    charge(order)
except GatewayTimeout as e:
    raise UpstreamUnavailableError("payment gateway timeout") from e
```

Also forbidden: bare `except:` (catches SystemExit/KeyboardInterrupt) and
`except Exception: pass` (log-and-ignore) outside the global handler.

## Rule 9 — Fail fast, clean up always

```python
# VIOLATION — exception between writes leaves half-committed state; conn leaks
conn = pool.acquire()
conn.execute(insert_order)
conn.execute(insert_payment)   # raises → order saved, payment not
pool.release(conn)

# CORRECT — validate first; context managers + transaction guarantee cleanup
validate(order)  # raises ValidationError before any write
with pool.acquire() as conn, conn.transaction():
    conn.execute(insert_order)
    conn.execute(insert_payment)
```

## Rule 10 — Exhaustive validation errors

```json
{
  "code": "VALIDATION_FAILED",
  "message": "Request validation failed.",
  "details": [
    { "field": "email",    "code": "INVALID_FORMAT", "message": "Must be a valid email address." },
    { "field": "quantity", "code": "OUT_OF_RANGE",   "message": "Must be between 1 and 100." }
  ],
  "request_id": "req_8f3a1c"
}
```

```python
# Collect ALL failures, then raise once
errors = []
if not EMAIL_RE.match(body.email):
    errors.append(FieldError("email", "INVALID_FORMAT", "Must be a valid email address."))
if not 1 <= body.quantity <= 100:
    errors.append(FieldError("quantity", "OUT_OF_RANGE", "Must be between 1 and 100."))
if errors:
    raise ValidationError(errors)
```
