# Observability Rules — Python Examples

**Framework basis:** Python 3.11+, `structlog` (or stdlib `logging` with a JSON
formatter), `contextvars` for correlation, `prometheus_client` for metrics. The
rules themselves are framework-agnostic — these examples only show one concrete
stack. **Translation hints:** stdlib logging → pass fields via `extra={...}` and a
JSON formatter; OpenTelemetry → `trace.get_current_span().set_attribute(...)`.
**Version-sensitive:** `contextvars` is 3.7+; `structlog` context binding via
`bind_contextvars`.

## Rule 1 — Log structured, not concatenated
Violation:
```python
logger.info(f"processed order {oid} for user {user}")   # unqueryable prose
```
Correct:
```python
logger.info("order processed", order_id=oid, user_id=user)   # filterable fields
```

## Rule 2 — One correlation id per request, threaded everywhere
Violation:
```python
logger.info("import started")               # not joinable to the request
```
Correct:
```python
correlation_id = request.headers.get("X-Correlation-Id") or str(uuid4())
bind_contextvars(correlation_id=correlation_id)   # set in middleware, on every line after
logger.info("import started")
```

## Rule 3 — Never log sensitive data
Violation:
```python
logger.info("auth", user=email, password=password, token=token)
```
Correct:
```python
logger.info("authentication succeeded", user_id=user_id)   # no secrets
```

## Rule 4 — Use the right level, and mean it
Violation:
```python
logger.error("user opened dashboard")       # routine event at ERROR → alert noise
logger.debug("payment gateway rejected charge")   # real failure hidden at DEBUG
```
Correct:
```python
logger.info("dashboard opened")
logger.error("payment rejected", reason=reason)   # failure needing attention
```

## Rule 5 — Log an exception once, with cause and context
Violation:
```python
except IOError as e:
    logger.error("import failed", exc_info=e)
    raise                                    # re-logged again by outer layers
```
Correct:
```python
except IOError as e:
    logger.error("import failed", file=name, exc_info=e)   # once, with context
    raise ImportFailed(name) from e          # exception-warden maps the response
```

## Rule 6 — Instrument key operations deliberately
Violation:
```python
def import_csv(...):                         # no signal it ran or how it went
    ...
```
Correct:
```python
IMPORT_ROWS = Counter("import_rows", "rows imported", ["outcome"])
IMPORT_TIME = Histogram("import_duration_seconds", "import duration")
with IMPORT_TIME.time():
    result = do_import(...)
IMPORT_ROWS.labels(outcome=result.outcome).inc(result.count)
```

## Rule 7 — Metric and label cardinality is bounded
Violation:
```python
REQ = Counter("http_requests", "requests", ["path"])
REQ.labels(path=request.url.path).inc()      # raw ids in path → cardinality blowup
```
Correct:
```python
REQ = Counter("http_requests", "requests", ["route", "status"])
REQ.labels(route="/accounts/{id}", status="200").inc()   # templated, bounded
```

## Rule 8 — Instrumentation is side-effect-free and cheap
Violation:
```python
logger.debug("state = %s", expensive_to_json(huge))   # built even when DEBUG off
```
Correct:
```python
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("state = %s", expensive_to_json(huge))
```

## Rule 9 — Log at the boundary, not in a loop
Violation:
```python
for row in rows:
    save(row)
    logger.info("saved row", row_id=row.id)   # N log lines
```
Correct:
```python
for row in rows:
    save(row)
logger.info("batch saved", count=len(rows))   # one summary
```

## Rule 10 — No print() for application logging
Violation:
```python
print(f"import done {count}")                 # bypasses structure/level/routing
```
Correct:
```python
logger = structlog.get_logger(__name__)
logger.info("import done", count=count)
```
