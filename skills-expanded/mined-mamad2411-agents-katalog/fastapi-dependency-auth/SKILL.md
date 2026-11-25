---
name: fastapi-dependency-auth
description: >
  FastAPI Depends-based authentication and authorization for owned APIs: OAuth2
  / Bearer schemes, current_user dependencies, role/scopes checks, router-level
  guards, and test overrides. Use when Depends(get_current_user),
  OAuth2PasswordBearer, Security scopes, or fixing missing auth on routes.
---

# FastAPI Dependency Auth

## Scope And Authorization

- **In scope:** FastAPI apps you own.
- **Out of scope:** Credential stuffing third-party APIs.
- Auth dependencies must fail closed (401/403), never optional by accident on sensitive routes.
- Redact tokens in logs and test fixtures.
- Pair with `fastapi-security-patterns` and `api-auth-and-jwt-abuse` for token threats.

## When To Use

- Implementing `get_current_user` / `require_role` via `Depends`.
- Applying auth to `APIRouter` once instead of per-handler.
- OAuth2 password flow or Bearer JWT validation.
- Scopes/roles for fine-grained access.
- Overriding auth in pytest with `dependency_overrides`.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Async I/O correctness | `fastapi-async-best-practices` |
| CORS/headers/TrustedHost | `fastapi-security-patterns` |
| IDOR object checks depth | `idor-broken-object-authorization` |
| JWT crypto attacks catalog | `api-auth-and-jwt-abuse` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Scheme | `HTTPBearer` / `OAuth2PasswordBearer` |
| User dep | Resolve identity once; cache per request |
| Authz | Separate `require_roles(...)` deps |
| Router | `dependencies=[Depends(get_current_user)]` |
| Errors | 401 unauthenticated; 403 forbidden |
| Tests | `app.dependency_overrides` |

## Workflow

### 1. Confirm scope and success criteria

1. Public vs protected routes matrix.
2. Success: unauthenticated protected routes 401; wrong role 403; tests cover both.

### 2. Inventory routes and deps

```bash
rg -n "APIRouter|Depends\\(|OAuth2|get_current_user|Security\\(" app -g'*.py'
```

1. List routes missing dependencies.
2. Note dual paths that parse JWT manually inconsistently.

### 3. Implement core dependencies

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer = HTTPBearer(auto_error=True)

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
) -> User:
    user = await verify_token(creds.credentials)  # raise on invalid/expired
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

def require_roles(*roles: str):
    async def _inner(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return _inner
```

```python
router = APIRouter(prefix="/v1", dependencies=[Depends(get_current_user)])

@router.get("/admin/stats")
async def stats(user: User = Depends(require_roles("admin"))):
    return {"ok": True}
```

1. Use `auto_error=True` unless you intentionally support optional auth.
2. For optional: separate `get_current_user_optional`—never reuse loosely on admin routes.
3. Object-level authz: check resource.owner_id == user.id inside handler/service.

### 4. Password/OAuth2 forms (if used)

1. Prefer modern flows; if `OAuth2PasswordBearer` tokenUrl used, protect token endpoint with rate limits.
2. Store password hashes with strong KDF; never log passwords.
3. Short-lived access tokens; rotate secrets via env.

### 5. Testing

```python
def test_protected(client):
    assert client.get("/v1/me").status_code == 401

def test_ok(client, app):
    app.dependency_overrides[get_current_user] = lambda: User(id="u1", role="user")
    try:
        assert client.get("/v1/me").status_code == 200
    finally:
        app.dependency_overrides.clear()
```

### 6. Verify with evidence

```bash
pytest -q
curl -s -o /dev/null -w "%{http_code}\n" "$BASE/v1/me"
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $TOKEN" "$BASE/v1/me"
```

### 7. Hand off

1. Document public route allowlist.
2. Centralize token verification—no copy-paste JWT decode.
3. Cross-link security patterns for transport/CORS.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Protection | Router-level Depends | Forgot Depends on new route |
| Roles | 403 when authenticated but denied | 401 for everything |
| Optional auth | Explicit optional dep | `auto_error=False` everywhere |
| Tests | Overrides + 401 cases | Only happy path |
| Authz | Ownership checks | Trust body `user_id` |

## Output Checklist

- [ ] Protected/public matrix complete
- [ ] get_current_user fail-closed
- [ ] Role/scope deps for admin
- [ ] Router dependencies applied
- [ ] Object-level authz considered
- [ ] Pytest 401/403 cases
- [ ] Residual risk noted

## Rules

- Fail closed on auth failures.
- Authn ≠ authz.
- Don’t log bearer tokens.
- Async token I/O follows async best practices.
- Broader FastAPI hardening → `fastapi-security-patterns`.
