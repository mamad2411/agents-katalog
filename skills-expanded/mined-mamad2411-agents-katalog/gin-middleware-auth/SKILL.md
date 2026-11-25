---
name: gin-middleware-auth
description: >
  Authentication and authorization middleware for Go Gin frameworks: bearer/JWT
  validation, session cookies, API keys, role checks, error responses, and test
  patterns. Use when hardening owned Gin services — not for bypassing third-party
  auth. Pair with `code-quality-standards` and JWT skills for token crypto details.
---

# Gin Middleware Auth

## Scope And Authorization

- **In scope:** Applications you own or are authorized to modify/test.
- **Out of scope:** Building auth bypasses against third-party Gin apps; forging tokens
  for systems without permission.
- Prefer short-lived tokens, validated issuers, and explicit route group protection.
- Never log raw bearer tokens or session IDs.
- Pair with `api-auth-and-jwt-abuse` for threat modeling and `go-style-conventions`.

## When To Use

- Adding `Authorization: Bearer` middleware to Gin route groups.
- Enforcing roles/permissions after authentication.
- Centralizing 401/403 JSON error shapes.
- Testing middleware with `httptest` and injected context claims.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| JWT crypto/claims deep dive | `api-auth-and-jwt-abuse` / JWT skills |
| OAuth/OIDC provider integration | OAuth skills |
| ABAC policy engine design | `golang-abac-design` |
| Generic Go style | `go-style-conventions` |
| TLS termination | infra skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Piece | Role |
| --- | --- |
| Middleware | `gin.HandlerFunc` wrapping `c.Next()` |
| Route groups | `r.Group("/api", AuthRequired())` |
| Context keys | Store `user_id` / claims on `c.Set` |
| 401 vs 403 | Unauthenticated vs authenticated but forbidden |
| Skip paths | Health/login exempt carefully |
| Order | Request ID → max body → auth → authorize → handler |

## Workflow

### 1. Define auth requirements

1. Record which routes are public vs authenticated vs role-gated.
2. Choose mechanism: JWT bearer, session cookie, mTLS+header, API key (service-to-service).
3. Success: unauthenticated requests 401; wrong role 403; valid passes with claims in context.

### 2. JWT bearer middleware (sketch)

```go
package middleware

import (
    "net/http"
    "strings"

    "github.com/gin-gonic/gin"
)

const ContextUserKey = "user"

type Claims struct {
    Sub   string
    Roles []string
}

type TokenValidator interface {
    Validate(token string) (Claims, error)
}

func AuthRequired(v TokenValidator) gin.HandlerFunc {
    return func(c *gin.Context) {
        h := c.GetHeader("Authorization")
        if h == "" || !strings.HasPrefix(h, "Bearer ") {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing_token"})
            return
        }
        raw := strings.TrimSpace(strings.TrimPrefix(h, "Bearer "))
        claims, err := v.Validate(raw)
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid_token"})
            return
        }
        c.Set(ContextUserKey, claims)
        c.Next()
    }
}

func RequireRole(role string) gin.HandlerFunc {
    return func(c *gin.Context) {
        v, ok := c.Get(ContextUserKey)
        if !ok {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing_principal"})
            return
        }
        claims := v.(Claims)
        for _, r := range claims.Roles {
            if r == role {
                c.Next()
                return
            }
        }
        c.AbortWithStatusJSON(http.StatusForbidden, gin.H{"error": "forbidden"})
    }
}
```

Validator must check: signature, `exp`/`nbf`, `iss`, `aud`, algorithm allowlist (no `none`).

### 3. Wire routes

```go
r := gin.New()
r.Use(gin.Recovery())
r.GET("/healthz", health)

api := r.Group("/api/v1")
api.Use(middleware.AuthRequired(validator))
{
    api.GET("/me", getMe)
    admin := api.Group("/admin", middleware.RequireRole("admin"))
    admin.GET("/stats", getStats)
}
```

### 4. API key middleware (service)

```go
func APIKey(header string, expected func() string) gin.HandlerFunc {
    return func(c *gin.Context) {
        if subtle.ConstantTimeCompare([]byte(c.GetHeader(header)), []byte(expected())) != 1 {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid_api_key"})
            return
        }
        c.Next()
    }
}
```

Use constant-time compare; load keys from Secret Manager / env; rotate with dual keys.

### 5. Cookie sessions (if used)

- `HttpOnly`, `Secure`, `SameSite=Lax|Strict`.
- Server-side session store or encrypted cookie with rotation.
- CSRF protection for browser cookie auth on state-changing routes.

### 6. Tests

```go
func TestAuthRequired_MissingToken(t *testing.T) {
    gin.SetMode(gin.TestMode)
    r := gin.New()
    r.Use(middleware.AuthRequired(fakeValidator{}))
    r.GET("/x", func(c *gin.Context) { c.Status(200) })

    w := httptest.NewRecorder()
    req := httptest.NewRequest(http.MethodGet, "/x", nil)
    r.ServeHTTP(w, req)
    if w.Code != http.StatusUnauthorized {
        t.Fatalf("got %d", w.Code)
    }
}
```

Matrix: missing, expired, wrong aud, valid, valid-but-wrong-role.

### 7. Hardening checklist

- [ ] Algorithm allowlist in JWT parse
- [ ] Clock skew bounded
- [ ] HTTPS only in prod
- [ ] No auth on debug pprof without protection
- [ ] Consistent error JSON without user enumeration where required
- [ ] Context keys typed; avoid stringly collisions
- [ ] Middleware order documented

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Failures | Abort + JSON 401/403 | `c.Next()` after error |
| Secrets | Validator uses JWKS | Hardcoded HMAC in repo |
| Roles | Explicit middleware | Handler copy-paste checks only half routes |
| Compare | Constant-time API keys | `==` on secrets |
| Logs | Request id + user id | Authorization header dump |

## Output Checklist

- [ ] Route auth matrix documented
- [ ] Middleware validates tokens correctly (tests)
- [ ] Role gates return 403
- [ ] Public routes remain public intentionally
- [ ] Tokens not logged
- [ ] Key/JWT config from secure store
- [ ] CSRF considered for cookies
- [ ] `code-quality-standards` applied

## Rules

- Owned apps only; no auth-bypass guidance for third parties.
- Prefer standard JWT validation libraries over hand-rolled crypto.
- 401 unauthenticated, 403 unauthorized — do not conflate casually.
- Keep middleware small; business authZ may need policy engines (`golang-abac-design`).
- Never commit signing keys.
