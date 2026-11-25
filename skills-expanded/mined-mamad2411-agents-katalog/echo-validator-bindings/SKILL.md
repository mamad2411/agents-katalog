---
name: echo-validator-bindings
description: >
  LabStack Echo binder and validator safety for owned Go services: Bind/BindJSON,
  path/query/form binding, go-playground validator tags, custom validators, and
  rejecting unknown fields. Use when Echo c.Bind, Validate, binding tags, or
  mass-assignment risks in Go APIs. Not for general XSS/SQLi beyond input gates.
---

# Echo Validator Bindings

## Scope And Authorization

- **In scope:** Go services using LabStack Echo that you own or are authorized to harden.
- **Out of scope:** Attacking third-party Echo apps without permission.
- Validation is a control layer—still use parameterized SQL, authz checks, and output encoding.
- Redact request dumps that contain passwords, tokens, or PII in tickets.
- Pair with `code-quality-standards` and Go style skills when editing handlers.

## When To Use

- Reviewing or implementing `c.Bind`, `c.BindJSON`, query/path binding on Echo routes.
- Adding `validate:"required,email,..."` tags and registering a `Validator` on Echo.
- Preventing mass assignment (binding into structs with privileged fields).
- Custom validators (UUID, enum, password policy) and consistent 400 error bodies.
- Hardening against oversized bodies and unexpected content types.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| SQL injection defense depth | `sqli-sql-injection` |
| XSS in templates | `xss-cross-site-scripting` |
| JWT/auth middleware | `api-auth-and-jwt-abuse` / FastAPI-like auth skills for patterns |
| Express middleware security | `express-middleware-security` |
| Implementation quality baseline | `code-quality-standards` |
| Generic Go style | `go-style-conventions` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Bind targets | Separate request DTOs from domain/DB models |
| Tags | `json` + `validate` on DTO fields only |
| Unknown fields | Disallow or explicitly ignore; never bind into entity with `IsAdmin` |
| Errors | Map validator errors to stable 400 JSON; no stack traces |
| Limits | `BodyLimit` middleware; max multipart memory |
| Custom | Register on `binding.Validator` once at startup |

## Workflow

### 1. Confirm scope and success criteria

1. List public routes that accept JSON/form/query input.
2. Success: invalid payloads return 400; privileged fields not client-settable; tests cover negative cases.

### 2. Inventory Echo setup

1. Find `e := echo.New()` and middleware (`BodyLimit`, logger, recover).
2. Locate all `c.Bind` / `c.BindJSON` / manual `json.Decoder` usage.
3. Check whether `e.Validator` is set.

### 3. Introduce request DTOs and validator

```go
package api

import (
  "net/http"

  "github.com/go-playground/validator/v10"
  "github.com/labstack/echo/v4"
)

type CustomValidator struct {
  v *validator.Validate
}

func (cv *CustomValidator) Validate(i interface{}) error {
  return cv.v.Struct(i)
}

func NewEcho() *echo.Echo {
  e := echo.New()
  e.Validator = &CustomValidator{v: validator.New()}
  e.Use(middleware.BodyLimit("1M"))
  return e
}

type CreateUserRequest struct {
  Email string `json:"email" validate:"required,email"`
  Name  string `json:"name" validate:"required,min=1,max=100"`
  // NOTE: no Role/IsAdmin here — set server-side only
}

func CreateUser(c echo.Context) error {
  var req CreateUserRequest
  if err := c.Bind(&req); err != nil {
    return echo.NewHTTPError(http.StatusBadRequest, "invalid json")
  }
  if err := c.Validate(&req); err != nil {
    return echo.NewHTTPError(http.StatusBadRequest, err.Error())
  }
  // map req → domain; set Role defaults in service layer
  return c.NoContent(http.StatusCreated)
}
```

### 4. Harden binding edge cases

1. **Path/query:** use dedicated structs with `param`/`query` tags; validate IDs as `uuid` or `numeric`.
2. **Mass assignment:** never bind JSON into GORM/ent models that include `role`, `balance`, `verified`.
3. **Unknown JSON fields:** for sensitive APIs, decode with `json.Decoder.DisallowUnknownFields()` into the DTO before validate.
4. **Content-Type:** reject unexpected types for JSON-only endpoints.
5. **Files:** validate extension/MIME server-side; size limits separate from JSON BodyLimit.

```go
func BindStrictJSON(c echo.Context, dst interface{}) error {
  dec := json.NewDecoder(c.Request().Body)
  dec.DisallowUnknownFields()
  if err := dec.Decode(dst); err != nil {
    return err
  }
  return c.Validate(dst)
}
```

### 5. Custom validators and i18n-safe errors

1. Register tags for business rules (`oneof=active inactive`, `startswith=...` sparingly).
2. Translate `validator.ValidationErrors` into field → code maps for clients.
3. Do not reflect raw internal errors to clients.

### 6. Verify with evidence

```bash
go test ./...

# Negative cases with curl (authorized env)
curl -sS -D- -o /dev/null -X POST "$BASE/users" \
  -H 'Content-Type: application/json' \
  -d '{"email":"not-an-email","name":""}'

curl -sS -D- -X POST "$BASE/users" \
  -H 'Content-Type: application/json' \
  -d '{"email":"a@b.co","name":"n","is_admin":true}'
# Expect: is_admin ignored or 400 if DisallowUnknownFields
```

1. Table-driven tests for each DTO: missing fields, overflow strings, wrong types.
2. Confirm handlers never trust client `id` for ownership without authz (pair with IDOR skill if needed).

### 7. Hand off

1. Document DTO conventions in the service README.
2. Lint rule or code review checklist: “no Bind into DB model.”
3. Apply `code-quality-standards` / `go-style-conventions`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Structs | `CreateUserRequest` DTO | Bind into `User` ORM model |
| Validation | `validate` tags + `c.Validate` | Only check non-nil after Bind |
| Privileged fields | Server-assigned role | Client sets `is_admin` |
| Errors | Stable field errors | Panic stack in JSON |
| Limits | BodyLimit + max string tags | Unlimited body and names |

## Output Checklist

- [ ] Echo Validator registered
- [ ] BodyLimit (and multipart limits if any) configured
- [ ] All mutating routes use DTOs + validate
- [ ] No privileged fields on request structs
- [ ] Unknown-field policy decided and tested
- [ ] Negative unit/integration tests present
- [ ] Error JSON shape documented
- [ ] Residual risks (authz after bind) noted

## Rules

- Owned services only for active testing.
- Validation ≠ authorization; always check actor vs resource.
- Keep secrets out of validation error examples.
- Focus on Echo bind/validate; deeper injection classes route to specific skills.
