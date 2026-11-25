---
name: error-handling
description: "Apply when designing error handling, exception hierarchies, or failure recovery in any application. Covers: domain exceptions, global handlers, retry patterns, graceful degradation, circuit breaker. Trigger for: error handling, exception, try/catch, failure, recovery, resilience."
---

# ERROR HANDLING — Production Resilience Patterns

## Domain Exception Hierarchy
```python
# Base exceptions (never catch Exception directly)
class AppError(Exception):
    """Base for all application errors."""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} {id} not found", "NOT_FOUND")

class ValidationError(AppError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"{field}: {reason}", "VALIDATION_ERROR")

class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message, "CONFLICT")

# Business logic raises domain errors, not HTTP exceptions
async def get_job(job_id: str) -> Job:
    job = await db.find(job_id)
    if not job:
        raise NotFoundError("Job", job_id)  # ✅ domain error
    return job
```

## Global Error Handler (FastAPI)
```python
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    status_map = {
        "NOT_FOUND": 404,
        "VALIDATION_ERROR": 422,
        "CONFLICT": 409,
    }
    return JSONResponse(
        status_code=status_map.get(exc.code, 500),
        content={"error": {"code": exc.code, "message": exc.message,
                           "request_id": get_request_id()}}
    )

@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    log.exception("unhandled_error", error=str(exc))
    return JSONResponse(status_code=500, content={"error": {"code": "INTERNAL_ERROR",
        "message": "An unexpected error occurred"}})
```

## Circuit Breaker (for external dependencies)
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_time=60):
        self.failures = 0
        self.threshold = failure_threshold
        self.recovery_time = recovery_time
        self.last_failure: datetime | None = None
        self.state = "closed"  # closed, open, half-open

    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if (datetime.utcnow() - self.last_failure).seconds > self.recovery_time:
                self.state = "half-open"
            else:
                raise ServiceUnavailableError("Circuit open — dependency down")
        try:
            result = await func(*args, **kwargs)
            self.failures = 0; self.state = "closed"
            return result
        except Exception:
            self.failures += 1
            self.last_failure = datetime.utcnow()
            if self.failures >= self.threshold:
                self.state = "open"
                log.error("circuit.opened", failures=self.failures)
            raise
```

## Forbidden
❌ `except Exception: pass` (silent failures)
❌ Catching and re-raising without context
❌ HTTP exceptions in business logic layer
❌ No logging in error handlers
❌ Exposing stack traces to API clients
❌ No fallback for external service failures
