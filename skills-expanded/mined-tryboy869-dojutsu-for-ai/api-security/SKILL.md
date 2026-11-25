---
name: api-security
description: "Apply when building any API endpoint, authentication system, or web service. Covers OWASP Top 10, rate limiting, input validation, JWT patterns, and secrets management."
---

# API SECURITY — Non-Negotiable Standards

## Input Validation (Pydantic / Zod)
```python
class JobSubmit(BaseModel):
    job_type: str = Field(..., pattern=r"^[a-z_]{3,50}$")
    payload: dict = Field(default_factory=dict)
    
    @validator("payload")
    def limit_payload_size(cls, v):
        if len(json.dumps(v)) > 10_000:
            raise ValueError("Payload exceeds 10KB limit")
        return v
```

## Rate Limiting
```python
# Every public endpoint needs rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/jobs")
@limiter.limit("100/minute")
async def submit_job(request: Request, ...):
    ...
```

## Authentication
```python
# JWT validation — always verify signature AND expiry
# Never trust payload without verification
def verify_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    # raises jwt.ExpiredSignatureError, jwt.InvalidTokenError
```

## Secrets Management
```python
# NEVER hardcode — always from environment
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str  # must be set or app fails to start
    redis_url: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
```

## CORS, Headers
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # NOT "*" in production
    allow_methods=["GET", "POST"],
)
# Add security headers
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
```

## Forbidden
❌ `allow_origins=["*"]` in production
❌ Secrets in code or git
❌ No rate limiting on public endpoints
❌ Logging request bodies (may contain PII/secrets)
❌ SQL string concatenation (use ORM or parameterized queries)
