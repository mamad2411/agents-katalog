---
name: auth-architecture
description: Design authentication and authorization architecture covering JWT, OAuth2, RBAC, session management, and MFA. Outputs auth flow diagrams, token strategy, permission models, and implementation patterns.
argument-hint: [application type, user types, compliance requirements, existing identity provider]
allowed-tools: Read, Write, Bash
---

# Auth Architecture

Authentication (who are you?) and authorization (what can you do?) are the most security-critical parts of any system. Getting them wrong is catastrophic; getting them right requires deliberate design before any code is written.

## Process

1. **Identify identity sources** — internal users, external OAuth, service accounts, API consumers.
2. **Choose token strategy** — JWT vs. opaque tokens vs. session cookies; trade-offs matter.
3. **Design the permission model** — RBAC, ABAC, or resource-level permissions.
4. **Map all auth flows** — login, refresh, logout, MFA, password reset, service-to-service.
5. **Plan token lifecycle** — expiry, refresh windows, revocation strategy.
6. **Define trust boundaries** — what verifies tokens, which services are trusted callers.
7. **Document attack scenarios** — replay, CSRF, token theft, privilege escalation.

## Output Format

### Auth Strategy Decision Matrix

| Scenario | Recommended Approach | Why |
|----------|---------------------|-----|
| Web app, same domain | HttpOnly session cookie | CSRF-safe, can be revoked instantly |
| SPA + API, different domains | Short-lived JWT (15min) + refresh token | Stateless, revocable via refresh |
| Mobile app | Long-lived refresh + short access token | Secure storage, offline capability |
| Service-to-service | mTLS or signed JWT with short expiry | No user context, machine identity |
| Public API (third-party) | API key + optional OAuth | Simplicity for developers |
| Admin panel | Session cookie + MFA | Higher security, explicit logout |

### JWT Token Strategy

```python
# auth/tokens.py
import jwt
import secrets
import hashlib
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from typing import Optional

@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    access_expires_at: datetime
    refresh_expires_at: datetime

class TokenService:
    ACCESS_TOKEN_TTL = timedelta(minutes=15)   # Short-lived
    REFRESH_TOKEN_TTL = timedelta(days=30)     # Rotated on each use

    def __init__(self, private_key: str, public_key: str, algorithm: str = "RS256"):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm   # RS256 (asymmetric) — not HS256

    def create_token_pair(
        self,
        user_id: str,
        roles: list[str],
        permissions: list[str],
        device_id: str = None,
    ) -> TokenPair:
        now = datetime.now(timezone.utc)
        
        # Access token — short lived, contains claims
        access_payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + self.ACCESS_TOKEN_TTL,
            "type": "access",
            "roles": roles,
            "permissions": permissions,
            "jti": secrets.token_urlsafe(16),  # Unique ID for tracking
        }
        if device_id:
            access_payload["did"] = device_id

        access_token = jwt.encode(access_payload, self.private_key, algorithm=self.algorithm)

        # Refresh token — opaque, stored server-side
        refresh_token_raw = secrets.token_urlsafe(64)
        refresh_token_hash = hashlib.sha256(refresh_token_raw.encode()).hexdigest()

        # Store hashed refresh token in DB
        refresh_expires = now + self.REFRESH_TOKEN_TTL
        self._store_refresh_token(
            token_hash=refresh_token_hash,
            user_id=user_id,
            device_id=device_id,
            expires_at=refresh_expires,
        )

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token_raw,   # Return raw; store hash
            access_expires_at=now + self.ACCESS_TOKEN_TTL,
            refresh_expires_at=refresh_expires,
        )

    def verify_access_token(self, token: str) -> dict:
        """Verify and decode access token. Raises on invalid/expired."""
        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=[self.algorithm],
                options={"require": ["exp", "iat", "sub", "type"]}
            )
            if payload.get("type") != "access":
                raise jwt.InvalidTokenError("Not an access token")
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Access token expired")
        except jwt.InvalidTokenError as e:
            raise TokenInvalidError(f"Invalid token: {e}")

    def rotate_refresh_token(self, refresh_token: str) -> TokenPair:
        """
        Rotate refresh token on use — detect token reuse.
        If a token is used twice, it was stolen; invalidate all tokens for device.
        """
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        stored = self._get_refresh_token(token_hash)

        if not stored:
            # Token not found — possible replay attack
            # Check if this token was recently rotated (indicates theft)
            if self._was_recently_rotated(token_hash):
                self._revoke_all_tokens_for_user(stored["user_id"])
                raise TokenReuseError("Refresh token reuse detected — all sessions invalidated")
            raise TokenInvalidError("Refresh token not found")

        if stored["expires_at"] < datetime.now(timezone.utc):
            raise TokenExpiredError("Refresh token expired")

        # Invalidate used token, issue new pair
        self._revoke_refresh_token(token_hash)
        user = self._get_user(stored["user_id"])

        return self.create_token_pair(
            user_id=user.id,
            roles=user.roles,
            permissions=user.permissions,
            device_id=stored.get("device_id"),
        )

    def revoke_all_sessions(self, user_id: str):
        """Force logout from all devices."""
        self._revoke_all_tokens_for_user(user_id)
```

### RBAC Permission Model

```python
# auth/permissions.py
from enum import Enum
from functools import wraps
from fastapi import Depends, HTTPException, status

# Define permissions as fine-grained strings
class Permission(str, Enum):
    # Orders
    ORDERS_READ = "orders:read"
    ORDERS_CREATE = "orders:create"
    ORDERS_UPDATE = "orders:update"
    ORDERS_DELETE = "orders:delete"
    ORDERS_CANCEL = "orders:cancel"
    # Users
    USERS_READ = "users:read"
    USERS_CREATE = "users:create"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"
    # Admin
    ADMIN_FULL = "admin:*"

# Role → Permission mappings
ROLE_PERMISSIONS: dict[str, set[str]] = {
    "customer": {
        Permission.ORDERS_READ,
        Permission.ORDERS_CREATE,
        Permission.ORDERS_CANCEL,
    },
    "support": {
        Permission.ORDERS_READ,
        Permission.ORDERS_UPDATE,
        Permission.USERS_READ,
    },
    "ops": {
        Permission.ORDERS_READ,
        Permission.ORDERS_UPDATE,
        Permission.ORDERS_DELETE,
        Permission.USERS_READ,
        Permission.USERS_UPDATE,
    },
    "admin": {
        Permission.ADMIN_FULL,
    },
}

def get_effective_permissions(roles: list[str]) -> set[str]:
    """Resolve effective permissions from roles — union of all role permissions."""
    perms = set()
    for role in roles:
        perms.update(ROLE_PERMISSIONS.get(role, set()))
    
    # Admin wildcard grants all permissions
    if Permission.ADMIN_FULL in perms:
        return {p.value for p in Permission}
    
    return perms

# FastAPI dependency
def require_permission(*permissions: Permission):
    """Decorator/dependency that checks the caller has all required permissions."""
    def dependency(current_user: dict = Depends(get_current_user)):
        user_permissions = set(current_user.get("permissions", []))
        
        missing = [p for p in permissions if p not in user_permissions]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {missing}"
            )
        return current_user
    return dependency

# Resource-level authorization (ownership check)
def require_resource_owner_or_permission(resource_owner_id: str, *fallback_permissions: Permission):
    """Allow resource owner OR users with elevated permissions."""
    def dependency(current_user: dict = Depends(get_current_user)):
        is_owner = current_user["sub"] == resource_owner_id
        user_permissions = set(current_user.get("permissions", []))
        has_permission = any(p in user_permissions for p in fallback_permissions)
        
        if not (is_owner or has_permission):
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return dependency


# Usage in routes
@router.get("/orders/{order_id}")
async def get_order(
    order_id: str,
    current_user: dict = Depends(require_permission(Permission.ORDERS_READ)),
):
    order = await order_service.get(order_id)
    # Customers can only see their own orders
    if "admin" not in current_user["roles"] and order.user_id != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Not your order")
    return order

@router.delete("/orders/{order_id}")
async def delete_order(
    order_id: str,
    _: dict = Depends(require_permission(Permission.ORDERS_DELETE)),
):
    await order_service.delete(order_id)
```

### OAuth2 Integration

```python
# auth/oauth.py — Social login (Google, GitHub)
from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth

router = APIRouter()
oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@router.get('/auth/google')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth/google/callback')
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get('userinfo')
    
    if not userinfo or not userinfo.get('email_verified'):
        raise HTTPException(400, "Google login failed or email not verified")
    
    # Find or create user
    user = await user_service.find_or_create_oauth_user(
        provider="google",
        provider_id=userinfo["sub"],
        email=userinfo["email"],
        name=userinfo.get("name"),
    )
    
    # Issue our own tokens
    tokens = token_service.create_token_pair(
        user_id=user.id,
        roles=user.roles,
        permissions=get_effective_permissions(user.roles),
    )
    
    response = RedirectResponse(url="/dashboard")
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,        # Not accessible via JS
        secure=True,          # HTTPS only
        samesite="lax",       # CSRF protection
        max_age=30 * 24 * 3600,
    )
    return response
```

### MFA Implementation

```python
# auth/mfa.py
import pyotp
import qrcode
import io
import base64

class MFAService:
    def setup_totp(self, user_id: str, email: str) -> dict:
        """Generate TOTP secret and provisioning URI."""
        secret = pyotp.random_base32()
        
        # Store encrypted secret (don't store plaintext)
        encrypted = encrypt(secret, key=settings.MFA_ENCRYPTION_KEY)
        db.store_mfa_secret(user_id, encrypted)
        
        # Generate QR code
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(email, issuer_name="MyApp")
        
        qr = qrcode.make(uri)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "secret": secret,   # Show once for manual entry
            "qr_code": f"data:image/png;base64,{qr_b64}",
            "uri": uri,
        }
    
    def verify_totp(self, user_id: str, code: str) -> bool:
        """Verify TOTP code — accept 1 window before/after for clock skew."""
        encrypted_secret = db.get_mfa_secret(user_id)
        secret = decrypt(encrypted_secret, key=settings.MFA_ENCRYPTION_KEY)
        
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)
    
    def generate_backup_codes(self, user_id: str) -> list[str]:
        """Generate one-time backup codes for account recovery."""
        codes = [secrets.token_hex(5) for _ in range(10)]
        hashed = [hashlib.sha256(c.encode()).hexdigest() for c in codes]
        db.store_backup_codes(user_id, hashed)
        return codes  # Return plaintext once; store hashes
```

### Auth Flow Diagram

```
Login Flow:
  Client → POST /auth/login {email, password}
    → Verify credentials
    → [if MFA enabled] → Return {mfa_required: true, temp_token}
      → Client → POST /auth/mfa {code, temp_token}
    → Issue access_token (15min) + refresh_token (30d, httponly cookie)
    → Return {access_token, expires_at}

Authenticated Request:
  Client → GET /api/orders
    Authorization: Bearer <access_token>
  → Gateway verifies JWT signature + expiry
  → Extract claims (user_id, roles, permissions)
  → Forward to service with X-User-ID header

Token Refresh:
  Client → POST /auth/refresh
    Cookie: refresh_token=<opaque>
  → Verify refresh token in DB
  → Rotate: invalidate old, issue new pair
  → Return new {access_token}

Logout:
  Client → POST /auth/logout
    Cookie: refresh_token=<opaque>
  → Revoke refresh token in DB
  → Clear cookie
  
Force Logout All Devices:
  Client → POST /auth/logout-all
    Authorization: Bearer <access_token>
  → Revoke ALL refresh tokens for user
```

## Rules

- **Use RS256 (asymmetric) not HS256** — services can verify tokens without knowing the signing secret.
- **Short access token TTL** — 15 minutes maximum; longer TTLs can't be revoked.
- **Rotate refresh tokens on every use** — detect stolen tokens by watching for reuse.
- **HttpOnly + Secure cookies for refresh tokens** — never store refresh tokens in localStorage.
- **Permissions in token, roles for management** — embed fine-grained permissions in JWT, not just role names.
- **Resource-level auth checks in code** — JWT proves identity; code must still check ownership.
- **Never return 403 with details** — "not found" is safer than "forbidden" for resources users shouldn't know exist.
- **Revocation on security events** — force logout all sessions on password change, account compromise.
- **MFA backup codes** — always provide account recovery; store hashes, not plaintext.
- **Audit all auth events** — logins, failures, logouts, token revocations, permission denials.
