---
name: input-validation
description: Design comprehensive input validation and sanitization to prevent injection attacks, XSS, path traversal, and data corruption. Outputs validation schemas, sanitization functions, and security-focused middleware.
argument-hint: [application type, input surfaces, languages/frameworks, threat model]
allowed-tools: Read, Write, Bash
---

# Input Validation & Sanitization

Every piece of untrusted input is an attack surface. Validate early, fail loudly, sanitize before use. The goal is to accept only what you explicitly allow — not to block what you explicitly forbid.

## Process

1. **Inventory all input surfaces** — HTTP params, headers, body, cookies, file uploads, env vars, IPC.
2. **Define schema for each input** — type, format, length, allowed values.
3. **Choose validation strategy** — allowlist (preferred) over denylist.
4. **Validate at the boundary** — as early as possible before any processing.
5. **Sanitize for context** — HTML context differs from SQL context differs from shell context.
6. **Return structured errors** — tell the user what's wrong without exposing internals.
7. **Log validation failures** — they're often attack signals.
8. **Test with adversarial inputs** — fuzzing, OWASP test vectors.

## Output Format

### Validation Schema (Pydantic / Python)

```python
# schemas/order.py
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Annotated, Optional
import re
from decimal import Decimal
from datetime import datetime

# Custom annotated types
Email = Annotated[str, Field(pattern=r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', max_length=254)]
UUID = Annotated[str, Field(pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')]
SafeString = Annotated[str, Field(min_length=1, max_length=500, pattern=r'^[a-zA-Z0-9 \-_.,!?\'\"]+$')]

class OrderItemSchema(BaseModel):
    product_id: UUID
    quantity: Annotated[int, Field(gt=0, le=100)]
    
    # Custom validator for business rules
    @field_validator('product_id')
    @classmethod
    def validate_product_exists(cls, v):
        # Note: do DB checks at service layer, not schema layer
        if v.startswith('0' * 8):  # Sentinel/test IDs blocked in prod
            raise ValueError("Invalid product ID")
        return v

class CreateOrderSchema(BaseModel):
    model_config = {"str_strip_whitespace": True}
    
    user_id: UUID
    items: Annotated[list[OrderItemSchema], Field(min_length=1, max_length=50)]
    shipping_address: "AddressSchema"
    notes: Optional[Annotated[str, Field(max_length=500)]] = None
    
    @field_validator('notes')
    @classmethod
    def sanitize_notes(cls, v):
        if v is None:
            return v
        # Strip HTML tags from free-text field
        import bleach
        return bleach.clean(v, tags=[], strip=True)
    
    @model_validator(mode='after')
    def validate_total_quantity(self):
        total = sum(item.quantity for item in self.items)
        if total > 500:
            raise ValueError("Total order quantity cannot exceed 500")
        return self

class AddressSchema(BaseModel):
    model_config = {"str_strip_whitespace": True}
    
    street: Annotated[str, Field(min_length=5, max_length=200)]
    city: Annotated[str, Field(min_length=2, max_length=100, pattern=r'^[a-zA-Z\s\-\.]+$')]
    country: Annotated[str, Field(pattern=r'^[A-Z]{2}$')]  # ISO 3166-1 alpha-2
    postal_code: str = Field(max_length=20)
    
    @field_validator('postal_code')
    @classmethod
    def validate_postal_code(cls, v, info):
        country = info.data.get('country', '')
        patterns = {
            'US': r'^\d{5}(-\d{4})?$',
            'GB': r'^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$',
            'DE': r'^\d{5}$',
        }
        pattern = patterns.get(country)
        if pattern and not re.match(pattern, v):
            raise ValueError(f"Invalid postal code format for {country}")
        return v
```

### SQL Injection Prevention

```python
# NEVER do this:
def bad_query(user_id: str):
    return db.execute(f"SELECT * FROM users WHERE id = '{user_id}'")

# Always use parameterized queries:
def safe_query(user_id: str):
    return db.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# With SQLAlchemy ORM (safe by default):
from sqlalchemy import select, text
from models import User

def get_user(user_id: str, session):
    # ORM — safe
    return session.get(User, user_id)

# For dynamic ORDER BY (can't parameterize column names):
ALLOWED_SORT_COLUMNS = frozenset({"created_at", "name", "price", "status"})
ALLOWED_SORT_DIRS = frozenset({"asc", "desc"})

def safe_list_query(sort_by: str, sort_dir: str, session):
    if sort_by not in ALLOWED_SORT_COLUMNS:
        raise ValueError(f"Invalid sort column: {sort_by}")
    if sort_dir not in ALLOWED_SORT_DIRS:
        raise ValueError(f"Invalid sort direction: {sort_dir}")
    
    # Safe: column name comes from allowlist, not user input
    stmt = text(f"SELECT * FROM products ORDER BY {sort_by} {sort_dir}")
    return session.execute(stmt)
```

### XSS Prevention

```python
import bleach
from markupsafe import Markup, escape

# Context 1: Displaying user content in HTML
def render_user_content(user_input: str) -> str:
    """Allow safe HTML subset, strip everything else."""
    ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a', 'blockquote']
    ALLOWED_ATTRS = {'a': ['href', 'title', 'rel']}
    ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']
    
    return bleach.clean(
        user_input,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )

# Context 2: Inserting into HTML attribute
def safe_attr_value(user_input: str) -> str:
    """For use in HTML attributes — escape all special chars."""
    return str(escape(user_input))

# Context 3: Inserting into JavaScript (avoid if possible)
import json
def safe_js_value(user_input) -> str:
    """JSON-encode for safe injection into JS."""
    return json.dumps(user_input)

# Context 4: URL parameters
from urllib.parse import quote
def safe_url_param(user_input: str) -> str:
    return quote(user_input, safe='')
```

### Path Traversal Prevention

```python
import os
from pathlib import Path

UPLOAD_DIR = Path("/var/uploads").resolve()

def safe_file_path(filename: str) -> Path:
    """Prevent path traversal (../../etc/passwd)."""
    # Strip directory components
    safe_name = Path(filename).name  # Takes only the filename, no dirs
    
    # Validate filename characters
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', safe_name):
        raise ValueError(f"Invalid filename: {filename}")
    
    # Resolve to absolute path and verify it's under upload dir
    full_path = (UPLOAD_DIR / safe_name).resolve()
    
    try:
        full_path.relative_to(UPLOAD_DIR)
    except ValueError:
        raise SecurityError(f"Path traversal attempt detected: {filename}")
    
    return full_path

def safe_read_file(filename: str) -> bytes:
    path = safe_file_path(filename)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    return path.read_bytes()
```

### File Upload Validation

```python
import magic
from fastapi import UploadFile, HTTPException

ALLOWED_MIME_TYPES = frozenset({
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
})
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_upload(file: UploadFile) -> bytes:
    # Size check (stream — don't read all at once for huge files)
    content = b""
    size = 0
    chunk_size = 64 * 1024  # 64KB chunks
    
    while chunk := await file.read(chunk_size):
        content += chunk
        size += len(chunk)
        if size > MAX_FILE_SIZE:
            raise HTTPException(400, f"File exceeds {MAX_FILE_SIZE // 1024 // 1024}MB limit")
    
    # MIME type check via magic bytes (not Content-Type header — that's user-controlled)
    detected_mime = magic.from_buffer(content[:2048], mime=True)
    if detected_mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, f"File type not allowed: {detected_mime}")
    
    # Extension check (defense in depth)
    ext = Path(file.filename or "").suffix.lower()
    ext_to_mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", 
                   ".png": "image/png", ".webp": "image/webp", ".pdf": "application/pdf"}
    
    if ext not in ext_to_mime or ext_to_mime[ext] != detected_mime:
        raise HTTPException(400, "File extension doesn't match content")
    
    return content
```

### Validation Middleware (FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging

logger = logging.getLogger("security")

app = FastAPI()

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    # Log validation failures — may indicate attack
    client_ip = request.client.host
    logger.warning(
        "Validation failure",
        extra={
            "ip": client_ip,
            "path": str(request.url.path),
            "errors": exc.errors(),
        }
    )
    
    # Return structured error — don't expose internals
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Invalid request data",
            "details": [
                {
                    "field": ".".join(str(loc) for loc in err["loc"]),
                    "message": err["msg"],
                    "type": err["type"]
                }
                for err in exc.errors()
            ]
        }
    )

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    # Block obviously malicious patterns before hitting route handlers
    path = request.url.path
    
    # Path traversal in URL
    if ".." in path or "%2e%2e" in path.lower():
        logger.warning(f"Path traversal attempt: {path} from {request.client.host}")
        return JSONResponse(status_code=400, content={"error": "Invalid path"})
    
    # Null bytes
    if "\x00" in path or "%00" in path:
        logger.warning(f"Null byte injection attempt from {request.client.host}")
        return JSONResponse(status_code=400, content={"error": "Invalid request"})
    
    response = await call_next(request)
    return response
```

### Request Size Limits

```python
# FastAPI / Starlette
from starlette.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.example.com", "*.example.com"]
)

# Limit body size in nginx:
# client_max_body_size 10m;

# In application layer:
@app.middleware("http")
async def limit_body_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10 * 1024 * 1024:
        return JSONResponse(status_code=413, content={"error": "Request too large"})
    return await call_next(request)
```

### Testing Adversarial Inputs

```python
import pytest
from httpx import AsyncClient

SQL_INJECTION_PAYLOADS = [
    "' OR '1'='1",
    "1; DROP TABLE users--",
    "' UNION SELECT * FROM users--",
    "1' AND SLEEP(5)--",
]

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    "';alert(1)//",
]

PATH_TRAVERSAL_PAYLOADS = [
    "../../etc/passwd",
    "..%2F..%2Fetc%2Fpasswd",
    "%2e%2e%2fetc%2fpasswd",
    "....//....//etc/passwd",
]

@pytest.mark.asyncio
@pytest.mark.parametrize("payload", SQL_INJECTION_PAYLOADS)
async def test_sql_injection_blocked(client: AsyncClient, payload: str):
    response = await client.get(f"/users?search={payload}")
    # Should return 422 or sanitized result, never 500 (which would indicate DB error)
    assert response.status_code in (400, 422)
    assert "error" in response.json()

@pytest.mark.asyncio
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
async def test_xss_sanitized(client: AsyncClient, payload: str):
    response = await client.post("/posts", json={"content": payload})
    if response.status_code == 201:
        # If accepted, verify the script tag is stripped
        assert "<script>" not in response.json()["content"]

@pytest.mark.asyncio
@pytest.mark.parametrize("payload", PATH_TRAVERSAL_PAYLOADS)
async def test_path_traversal_blocked(client: AsyncClient, payload: str):
    response = await client.get(f"/files/{payload}")
    assert response.status_code in (400, 403, 404)
```

## Rules

- **Allowlist, not denylist** — define what's valid, reject everything else.
- **Validate at the boundary** — don't trust data that came through layers you don't control.
- **Never trust `Content-Type`** — always verify file magic bytes for uploads.
- **Parameterized queries always** — string interpolation into SQL is never acceptable.
- **Context-aware output encoding** — HTML escaping ≠ URL encoding ≠ JS encoding.
- **Reject, don't sanitize for security-critical fields** — an invalid email should be rejected, not "fixed".
- **Log validation failures with context** — they're often probing attacks.
- **Size limits on all inputs** — strings, arrays, file uploads, JSON depth.
- **Never expose validation internals** in error messages — no stack traces, no schema hints to attackers.
- **Test with OWASP vectors** — SQL injection, XSS, path traversal, XXE, SSRF.
