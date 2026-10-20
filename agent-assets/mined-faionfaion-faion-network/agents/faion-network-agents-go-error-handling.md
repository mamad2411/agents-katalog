# Go Error Handling (typed AppError + middleware)

## Summary

**One-sentence:** Produces a Go error-handling pipeline (typed AppError, fmt.Errorf %w wrapping, repository boundary mapping, middleware translation, golangci-lint errorlint/wrapcheck) that yields consistent HTTP responses across the service.

**One-paragraph:** Define `AppError{Code, Message, HTTPStatus, Err}` implementing `Error()` and `Unwrap()` so `errors.Is/As` work through wrapping. Always wrap with `fmt.Errorf("context: %w", err)`, never `%v`. Map driver errors (pgx.ErrNoRows, sql.ErrNoRows) to AppError at the repository layer — never let driver errors reach handlers. Handlers return error; an HTTP middleware logs and translates AppError to JSON via `errors.As`. Panic recovery middleware runs BEFORE the error mapper. `golangci-lint` runs with errorlint, wrapcheck, errcheck, nilnil enabled.

**Ефективно для:** new Go services, refactors merging ad-hoc error shapes into one typed envelope, repos where driver errors leak to handlers or status codes get demoted on rewrap, services adopting structured logging tied to AppError fields.

## Applies If (ALL must hold)

- Service returns errors across layers (handler → service → repository).
- Team accepts one typed AppError and one translation middleware.
- golangci-lint can be added to CI with custom linters enabled.
- Errors must map to HTTP status codes deterministically.

## Skip If (ANY kills it)

- Pure library code that never reaches an HTTP boundary (use errors.Is/As only).
- Pre-1.13 Go codebase that cannot use `%w` wrapping (upgrade first).
- Generated code where errors are owned by a different layer (protoc-gen-* envelopes).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Layer list (handler/service/repository) | Markdown | `[[go-backend]]` layout |
| Driver list (pgx, sqlx, http clients) | Markdown | infra ADR |
| HTTP framework | string (gin/echo/net-http) | tech stack ADR |
| Logger | string (slog/zap/zerolog) | observability ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-backend]]` | Provides apperror/ package location and middleware wiring. |
| `[[go-http-handlers]]` | Handlers return error and use the translation middleware. |
| `[[error-handling]]` | Cross-language RFC 7807 envelope this maps onto. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: AppError shape, %w wrapping, repo boundary mapping, Handler+Wrap, panic-then-map order, lint config, constructors not mutable vars | ~800 |
| `content/02-output-contract.xml` | essential | Required apperror package shape + middleware order + lint config | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: %v wrapping, type assertion at HTTP boundary, driver errors leaking, mutable package vars, status demotion on rewrap | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: scaffold pkg/apperror → wrap rules → repo mapping → middleware → lint gate | ~800 |
| `content/06-decision-tree.xml` | essential | Root question on Go service + HTTP layer | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold pkg/apperror | sonnet | Template-driven. |
| Boundary mapping for new driver | sonnet | Lookup table generation. |
| errors.Is/As migration from type assertions | opus | AST-level reasoning over wrap chains. |
| Lint config | haiku | Boilerplate YAML. |

## Templates

| File | Purpose |
|------|---------|
| `templates/apperror.go` | Drop-in pkg/apperror package: AppError type, constructors, Wrap helper. |
| `templates/error-middleware.go` | HTTP middleware translating AppError to JSON via errors.As. |
| `templates/prompt-error-scaffold.txt` | Prompt for sub-agent generating the apperror package + middleware. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-error-handling.py` | Verifies %w usage, no type assertions at HTTP boundaries, apperror.go shape. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[go-backend]]` — middleware order
- `[[go-http-handlers]]` — handler signatures
- `[[error-handling]]` — RFC 7807 cross-mapping

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: Go service with HTTP layer, %w available (Go 1.13+), team can install one translation middleware. Any "no" -> skip.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/apperror.go`

```go
// Package apperror defines a structured error type for HTTP services.
// Use constructors (NewNotFound, NewValidation, etc.); never modify package-level vars.
package apperror

import (
	"errors"
	"fmt"
	"net/http"
)

// AppError carries an API-stable code, human message, HTTP status, and optional wrapped error.
type AppError struct {
	Code       string `json:"code"`
	Message    string `json:"message"`
	HTTPStatus int    `json:"-"`
	Err        error  `json:"-"`
}

func (e *AppError) Error() string {
	if e.Err != nil {
		return fmt.Sprintf("%s: %v", e.Message, e.Err)
	}
	return e.Message
}

func (e *AppError) Unwrap() error { return e.Err }

func NewNotFound(resource string) *AppError {
	return &AppError{
		Code:       "NOT_FOUND",
		Message:    fmt.Sprintf("%s not found", resource),
		HTTPStatus: http.StatusNotFound,
	}
}

func NewUnauthorized(msg string) *AppError {
	return &AppError{Code: "UNAUTHORIZED", Message: msg, HTTPStatus: http.StatusUnauthorized}
}

func NewValidation(msg string) *AppError {
	return &AppError{Code: "VALIDATION_ERROR", Message: msg, HTTPStatus: http.StatusBadRequest}
}

// Wrap preserves Code and HTTPStatus from an inner *AppError when present.
func Wrap(err error, msg string) *AppError {
	var inner *AppError
	if errors.As(err, &inner) {
		return &AppError{
			Code:       inner.Code,
			Message:    msg,
			HTTPStatus: inner.HTTPStatus,
			Err:        err,
		}
	}
	return &AppError{
		Code:       "INTERNAL_ERROR",
		Message:    msg,
		HTTPStatus: http.StatusInternalServerError,
		Err:        err,
	}
}
```

### `templates/error-middleware.go`

```go
// Package httpx provides HTTP handler wrappers including error translation middleware.
// Handler is a func(ResponseWriter, *Request) error variant of http.HandlerFunc.
// Wrap converts it to a standard HandlerFunc and translates *AppError to JSON responses.
package httpx

import (
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"

	"yourmod/pkg/apperror"
)

type errBody struct {
	Code    string `json:"code"`
	Message string `json:"message"`
	TraceID string `json:"trace_id,omitempty"`
}

// Handler is like http.HandlerFunc but returns an error.
type Handler func(http.ResponseWriter, *http.Request) error

// Wrap converts a Handler to http.HandlerFunc with error translation.
func Wrap(h Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		err := h(w, r)
		if err == nil {
			return
		}
		var appErr *apperror.AppError
		if !errors.As(err, &appErr) {
			appErr = apperror.Wrap(err, "internal error")
		}
		if appErr.HTTPStatus >= 500 {
			slog.ErrorContext(r.Context(), "http error",
				"code", appErr.Code, "status", appErr.HTTPStatus, "err", err)
		} else {
			slog.InfoContext(r.Context(), "http client error",
				"code", appErr.Code, "status", appErr.HTTPStatus)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(appErr.HTTPStatus)
		if encErr := json.NewEncoder(w).Encode(errBody{
			Code:    appErr.Code,
			Message: appErr.Message,
			TraceID: TraceIDFromCtx(r.Context()),
		}); encErr != nil {
			slog.ErrorContext(r.Context(), "failed to encode error response", "err", encErr)
		}
	}
}

// TraceIDFromCtx extracts the trace ID from context — implement per project.
func TraceIDFromCtx(r interface{ Value(any) any }) string {
	if id, ok := r.Value("trace_id").(string); ok {
		return id
	}
	return ""
}
```

### `templates/prompt-error-scaffold.txt`

```text
Create pkg/apperror with AppError type per
free/dev/software-developer/go-error-handling/templates/apperror.go.

Requirements:
  1. Constructor functions only — no exported mutable package vars.
  2. Wrap must preserve inner *AppError's HTTPStatus and Code when wrapping a typed error.
  3. Add WrapWithStatus(err, msg, status int) for explicit override.

Add pkg/httpx/error_middleware.go per
free/dev/software-developer/go-error-handling/templates/error-middleware.go:
  - Recovery middleware that catches panics and converts to 500 AppError.
  - Wrap adapter translating Handler errors to JSON responses.
  - 4xx → slog.Info, 5xx → slog.Error.

Add table-driven tests in pkg/apperror/apperror_test.go covering:
  - errors.As across wrapping chains.
  - Wrap preserves inner HTTPStatus (NewNotFound wrapped should still be 404).
  - Error() string format.

Run: go test ./pkg/apperror/... -race -v
Run: golangci-lint run --enable errorlint,wrapcheck,errcheck ./...
```
