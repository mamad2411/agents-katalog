---
name: fastapi-security-patterns
description: >
  Secure FastAPI apps: Depends-based auth wiring, CORS/TrustedHost, HTTPS
  termination assumptions, security headers, Pydantic validation boundaries,
  JWT/OAuth2 schemes, and safe middleware order. Use when FastAPI CORS,
  TrustedHostMiddleware, OAuth2PasswordBearer, or hardening Starlette/FastAPI.
---

# FastAPI Security Patterns

## Scope And Authorization

- **In scope:** FastAPI/Starlette services you own.
- **Out of scope:** Unauthorized testing of third-party APIs.
- Prefer TLS at the edge; configure app for proxy headers carefully.
- Redact secrets from OpenAPI examples and exception handlers.
- Pair with `fastapi-dependency-auth`, `fastapi-async-best-practices`, `code-quality-standards`.

## When To Use

- Baseline hardening for a new or existing FastAPI service.
- Reviewing CORS, hosts, docs exposure, and middleware stack.
- Ensuring request bodies validated via Pydantic models (not raw dict trust).
- Closing unauthenticated docs/admin in production.
- Aligning error handlers to avoid stack traces.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Deep Depends auth design | `fastapi-dependency-auth` |
| Async blocking I/O | `fastapi-async-best-practices` |
| Express middleware | `express-middleware-security` |
| JWT attack catalog | `api-auth-and-jwt-abuse` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Validation | Pydantic models on all inputs |
| CORS | Explicit origins; no `*` with credentials |
| Hosts | TrustedHostMiddleware allowlist |
| Docs | Disable or protect `/docs` in prod |
| Headers | Security headers middleware / edge |
| Auth | Depends everywhere sensitive |
| Errors | Generic 500 messages |

## Workflow

### 1. Confirm scope and success criteria

1. Public exposure, auth model, edge TLS.
2. Success: headers/CORS/host checks pass; openapi limited; auth tests green.

### 2. Inventory app surface

```bash
rg -n "FastAPI\\(|CORSMiddleware|TrustedHost|include_router|docs_url" app -g'*.py'
```

1. Note middleware order (last added = outer in Starlette).
2. List routers without auth dependencies.

### 3. Apply secure skeleton

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    docs_url=None if settings.ENV == "production" else "/docs",
    redoc_url=None if settings.ENV == "production" else "/redoc",
    openapi_url=None if settings.ENV == "production" else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # explicit list
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

# Security headers can be edge (nginx) or custom middleware
```

1. Body size limits at proxy; app still validates shapes.
2. Use response models to avoid leaking internal ORM fields.
3. Dependency auth on routers—see dependency-auth skill.

### 4. Pydantic boundaries

```python
class CreateItem(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    # no is_admin field

@router.post("/items", response_model=ItemOut)
async def create(item: CreateItem, user=Depends(get_current_user)):
    return await service.create(user.id, item)
```

1. Never accept arbitrary `dict` for privileged updates.
2. Separate read/write models.

### 5. Secrets and config

1. JWT signing keys from env/secret manager (`env-config-12factor`).
2. Different keys per env; reject `alg=none` style misuse in verify.
3. Rate-limit auth routes at edge or middleware.

### 6. Verify with evidence

```bash
pytest -q
curl -sI "$BASE/health" | rg -i 'strict-transport|x-content-type|content-security' || true
curl -s -o /dev/null -w "%{http_code}\n" -H "Origin: https://evil.example" -H "Access-Control-Request-Method: GET" -X OPTIONS "$BASE/v1/items"
curl -s -o /dev/null -w "%{http_code}\n" "$BASE/docs"
```

1. Disallowed host → 400 from TrustedHost when enabled correctly.
2. Unauthenticated protected route → 401.
3. Oversize/invalid body → 422 with safe detail.

### 7. Hand off

1. Production checklist for docs/CORS/hosts.
2. Edge vs app header ownership.
3. Link async and auth skills.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| CORS | Allowlist | `allow_origins=["*"]` + credentials |
| Docs | Off in prod | Public Swagger with try-it + prod data |
| Models | Strict Pydantic | `body: dict` |
| Errors | Stable codes | Traceback in JSON |
| Auth | Router Depends | Security only “documented” |

## Output Checklist

- [ ] CORS/hosts/docs hardened for env
- [ ] Middleware order reviewed
- [ ] Pydantic on inputs; response models on outputs
- [ ] Auth dependencies on sensitive routers
- [ ] Secrets via env/secret store
- [ ] Test/curl evidence
- [ ] Residual risk noted

## Rules

- Owned apps only.
- Validate all untrusted input with Pydantic.
- Disable or protect docs in production.
- Fail closed on auth; generic 500s.
- Deep auth deps → `fastapi-dependency-auth`.
