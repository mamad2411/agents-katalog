# Outbound-Integration Rules — Python Examples

**Framework basis:** Python 3.11+, `httpx` (sync or async), `tenacity` for retry,
`pybreaker` for circuit-breaking, Pydantic v2 for response models. The rules
themselves are framework-agnostic — these examples only show one concrete stack.
**Translation hints:** `requests` → pass `timeout=(connect, read)` and use
`urllib3.Retry` on an adapter; `aiohttp` → `ClientTimeout`. **Version-sensitive:**
`httpx.Timeout` takes separate connect/read; Pydantic v2 uses `model_validate`.

## Rule 1 — Every outbound call is time-bounded
Violation:
```python
r = httpx.get(url)                          # default timeout is None → can hang forever
```
Correct:
```python
timeout = httpx.Timeout(connect=2.0, read=5.0, write=5.0, pool=2.0)
client = httpx.Client(timeout=timeout)      # explicit bounds
```

## Rule 2 — Retry only what is safe, with capped jittered backoff
Violation:
```python
while True:                                 # unbounded
    try: return client.get(url); 
    except Exception: time.sleep(1)         # fixed delay
```
Correct:
```python
@retry(stop=stop_after_attempt(3),
       wait=wait_random_exponential(multiplier=0.2, max=5),
       retry=retry_if_exception_type((httpx.TransportError,)))   # transient + idempotent
def fetch_rate(): ...
```

## Rule 3 — Break the circuit on a failing dependency
Violation:
```python
def fetch(): return client.get("/rate")     # every call hits a dead dependency
```
Correct:
```python
breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=30)
@breaker
def fetch(): return client.get("/rate")     # fails fast once open
```

## Rule 4 — Check the status before trusting the body
Violation:
```python
data = client.get("/rate").json()           # 500 body parsed as success
```
Correct:
```python
resp = client.get("/rate")
resp.raise_for_status()                      # raises on 4xx/5xx
data = resp.json()
```

## Rule 5 — Validate and map the response at the boundary
Violation:
```python
data = client.get("/rate").json()
domain.rate = data["rate"]                   # raw external schema leaks inward
```
Correct:
```python
class RateDto(BaseModel):
    rate: Decimal
    currency: str
dto = RateDto.model_validate(client.get("/rate").json())   # fails loudly if renamed/missing
```

## Rule 6 — Convert remote failures into typed local errors
Violation:
```python
def fetch(): return client.get("/rate").json()   # raw httpx.ConnectError escapes
```
Correct:
```python
def fetch():
    try:
        r = client.get("/rate"); r.raise_for_status(); return RateDto.model_validate(r.json())
    except httpx.HTTPError as e:
        raise RatesUnavailable() from e          # typed local error
```

## Rule 7 — Make writes idempotent where the protocol allows
Violation:
```python
client.post("/charges", json=charge)         # retried POST → double charge
```
Correct:
```python
client.post("/charges", json=charge,
            headers={"Idempotency-Key": str(charge_id)})   # retry-safe
```

## Rule 8 — Isolate the client behind an interface
Violation:
```python
class InvoiceService:
    def bill(self):
        httpx.post(url, json=...)            # HTTP inside business logic
```
Correct:
```python
class RatesPort(Protocol):
    def fetch_rate(self) -> RateDto: ...     # seam; fake in tests
class InvoiceService:
    def __init__(self, rates: RatesPort): self._rates = rates
```

## Rule 9 — Propagate context outward; never leak secrets
Violation:
```python
logger.info("calling rates key=%s body=%s", api_key, resp.text)   # secret + full body
```
Correct:
```python
client.get("/rate", headers={
    "X-Correlation-Id": correlation_id_var.get(),   # propagate trace
    "Authorization": f"Bearer {token}",             # not logged
})
```

## Rule 10 — Bound concurrency and payload size
Violation:
```python
def fetch(): return httpx.get(url)           # new client + connection per call
```
Correct:
```python
# one shared client with a bounded pool, reused across calls
client = httpx.Client(limits=httpx.Limits(max_connections=20, max_keepalive_connections=10))
```
