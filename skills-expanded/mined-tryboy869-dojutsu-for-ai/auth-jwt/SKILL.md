---
name: auth-jwt
description: "Apply when implementing authentication and authorization with JWT, OAuth2, or session tokens. Covers: JWT structure, refresh tokens, OAuth2 flows, RBAC, secure cookie patterns. Trigger for: authentication, JWT, OAuth, login, session, token, auth."
---

# AUTH JWT — Production Patterns

## JWT Structure & Validation
```python
from datetime import datetime, timedelta, timezone
import jwt
from pydantic import BaseModel

SECRET_KEY = os.environ["JWT_SECRET"]  # min 32 random bytes
ALGORITHM  = "HS256"

class TokenPayload(BaseModel):
    sub: str       # user ID
    exp: datetime
    iat: datetime
    role: str

def create_access_token(user_id: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=15),  # SHORT expiry
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> TokenPayload:
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**data)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

## Refresh Token Pattern
```python
# Access token: 15 min (stateless)
# Refresh token: 7 days (stored in DB, revocable)

async def refresh(refresh_token: str) -> dict:
    # 1. Verify refresh token exists in DB
    stored = await db.get_refresh_token(refresh_token)
    if not stored or stored.revoked or stored.expires_at < now():
        raise HTTPException(401, "Invalid refresh token")
    
    # 2. Rotate: revoke old, issue new pair
    await db.revoke_refresh_token(refresh_token)
    new_access = create_access_token(stored.user_id, stored.role)
    new_refresh = await db.create_refresh_token(stored.user_id)
    return {"access_token": new_access, "refresh_token": new_refresh}
```

## Secure Cookie (prefer over localStorage)
```python
@app.post("/auth/login")
async def login(response: Response, credentials: LoginSchema):
    tokens = await authenticate(credentials)
    # HttpOnly prevents XSS, Secure requires HTTPS, SameSite prevents CSRF
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 3600,
    )
    return {"access_token": tokens.access_token}  # in response body
```

## RBAC — Role-based access
```python
from enum import Enum
from functools import wraps

class Role(str, Enum):
    USER  = "user"
    ADMIN = "admin"

def require_role(*roles: Role):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_current_user), **kwargs):
            if current_user.role not in roles:
                raise HTTPException(403, "Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

@app.delete("/users/{id}")
@require_role(Role.ADMIN)
async def delete_user(id: str, current_user: User = Depends(get_current_user)): ...
```

## Forbidden
❌ Long-lived access tokens (> 1 hour)
❌ Storing tokens in localStorage (XSS risk)
❌ JWT secret < 32 bytes
❌ No token revocation mechanism
❌ Putting sensitive data in JWT payload (it's base64, not encrypted)
❌ `algorithm=None` or `algorithms=[]`
