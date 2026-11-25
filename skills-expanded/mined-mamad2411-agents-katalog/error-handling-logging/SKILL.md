---
name: error-handling-logging
description: |
  Structured error handling and logging patterns. Apply for any error handler, exception class,
  middleware, or logging configuration. Covers custom exception hierarchy, global handlers,
  structured JSON logging, request tracing, and Sentry integration.
---

# Error Handling & Logging

## Custom Exception Hierarchy
```python
class AppError(Exception):
    """Base exception for all application errors"""
    def __init__(self, code: str, message: str, status_code: int = 500, details: dict = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class ValidationError(AppError):
    def __init__(self, message: str, details: dict = None):
        super().__init__("VALIDATION_ERROR", message, 400, details)

class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: str = None):
        msg = f"{resource} not found"
        if resource_id:
            msg += f": {resource_id}"
        super().__init__("RESOURCE_NOT_FOUND", msg, 404)

class ForbiddenError(AppError):
    def __init__(self, action: str = None):
        msg = f"Access denied" + (f": {action}" if action else "")
        super().__init__("FORBIDDEN", msg, 403)

class ConflictError(AppError):
    def __init__(self, resource: str):
        super().__init__("RESOURCE_CONFLICT", f"{resource} already exists", 409)
```

## Global Exception Handler
```python
# FastAPI
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.warning("app_error",
        code=exc.code, message=exc.message,
        path=request.url.path, request_id=request.state.request_id
    )
    return JSONResponse(status_code=exc.status_code, content={
        "success": False,
        "data": None,
        "error": {
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
            "request_id": request.state.request_id,
        }
    })

@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", exc_info=exc, path=request.url.path)
    return JSONResponse(status_code=500, content={
        "success": False,
        "data": None,
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "request_id": getattr(request.state, "request_id", None),
        }
    })
```

## Structured Logging Setup
```python
# core/logging.py
import structlog
import logging

def setup_logging(log_level: str = "INFO"):
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(level=getattr(logging, log_level))

logger = structlog.get_logger()

# Usage — always include context
logger.info("payment.processed",
    payment_id=payment.id,
    user_id=user.id,
    amount=payment.amount,
    provider="payme",
    duration_ms=elapsed_ms,
    request_id=request_id,
)
```
