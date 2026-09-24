# FastAPI Error Handling

FastAPI error handling using the **global handler pattern** - routes raise exceptions, handlers format responses.

## Core Pattern

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

# 1. Routes just raise - no try/except
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await user_service.get(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user

# 2. Global handlers format responses
@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}}
    )
```

## HTTPException

### Basic Usage

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

### With Custom Headers

```python
raise HTTPException(
    status_code=401,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"}
)
```

### FastAPI vs Starlette HTTPException

```python
from fastapi import HTTPException  # Accepts any JSON-able detail
from starlette.exceptions import HTTPException as StarletteHTTPException  # Only strings

# FastAPI's HTTPException allows dict detail
raise HTTPException(
    status_code=400,
    detail={"code": "invalid_input", "field": "email"}
)

# When registering handler, use Starlette's to catch both
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "http_error", "message": str(exc.detail)}}
    )
```

## Global Exception Handlers

### Domain Exceptions

```python
from enum import StrEnum

class ErrorCode(StrEnum):
    USER_NOT_FOUND = "user_not_found"
    PERMISSION_DENIED = "permission_denied"

class DomainError(Exception):
    def __init__(self, code: ErrorCode, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        }
    )
```

### RequestValidationError

Override default validation error format:

```python
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Option 1: Simple message (hide details)
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "message": "Invalid request"}}
    )

    # Option 2: Formatted errors
    errors = []
    for error in exc.errors():
        loc = ".".join(str(x) for x in error["loc"][1:])  # Skip "body"
        errors.append({"field": loc, "message": error["msg"]})
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "errors": errors}}
    )
```

### Generic Exception Handler

Catch-all for unexpected errors:

```python
import logging

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log full error for debugging
    logger.exception("Unhandled exception", extra={
        "path": request.url.path,
        "method": request.method,
    })
    
    # Return safe message to client (hide internal details)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "internal_error", "message": "Internal server error"}}
    )
```

## Middleware vs Exception Handlers

| Use Case | Middleware | Exception Handler |
|----------|------------|-------------------|
| Add request_id to all responses | ✅ | |
| Log all requests/responses | ✅ | |
| Format specific exceptions | | ✅ |
| Catch exceptions from middleware | | ✅ |
| Timing/metrics | ✅ | |

### Adding Request Context via Middleware

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestContextMiddleware)

# Use in exception handler
@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": request_id,
            }
        }
    )
```

## Dependency Injection Errors

Exceptions in dependencies propagate to handlers:

```python
from fastapi import Depends

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = await verify_token(token)
    if not user:
        raise AuthenticationError()  # Propagates to exception handler
    return user

@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user  # Only reached if get_current_user succeeds
```

## Reusing Default Handlers

Extend default behavior instead of replacing:

```python
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Add logging
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    # Then use default handler
    return await http_exception_handler(request, exc)
```

## Security: Preventing Information Leakage

### Don't Expose Stack Traces

```python
# BAD - Exposes internals
@app.exception_handler(Exception)
async def bad_handler(request: Request, exc: Exception):
    import traceback
    return JSONResponse(
        status_code=500,
        content={"error": traceback.format_exc()}  # Never do this!
    )

# GOOD - Safe generic message
@app.exception_handler(Exception)
async def good_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error")  # Log internally
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "internal_error", "message": "Internal server error"}}
    )
```

### Sanitize Validation Errors

```python
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    # Don't include exc.body - may contain sensitive data
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "message": "Invalid request"}}
    )
```

## Error Response Schema

Consistent error format:

```python
from pydantic import BaseModel
from typing import Any

class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str | None = None
    errors: list[dict[str, Any]] | None = None  # For validation errors

class ErrorResponse(BaseModel):
    error: ErrorDetail

# Document in OpenAPI
@app.get("/users/{user_id}", responses={
    404: {"model": ErrorResponse, "description": "User not found"},
    500: {"model": ErrorResponse, "description": "Internal server error"},
})
async def get_user(user_id: int):
    ...
```
