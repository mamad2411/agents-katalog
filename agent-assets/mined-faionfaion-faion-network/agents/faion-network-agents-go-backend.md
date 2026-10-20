# Go Backend (cmd/ + internal/, Gin/Echo)

## Summary

**One-sentence:** Produces a Go HTTP backend scaffold with cmd/ + internal/ layout, consumer-side interfaces, context-first I/O signatures, typed AppError mapped to HTTP via one middleware, and a context-aware worker pool.

**One-paragraph:** Production-grade Go backend with the standard `cmd/api/main.go` entry point and `internal/{handler,service,repository,model,middleware,config}` domain code. Interfaces are defined at the consumer side (service defines `UserRepository`, repository implements it). `context.Context` is the first arg of every exported I/O function; `gin.Context` is never captured inside a goroutine. Handlers use `ShouldBindJSON` (returns error) and call `c.Error(err)` so a single ErrorHandler middleware maps AppError to HTTP. Worker pools select on both jobs channel and `ctx.Done()` to drain cleanly under cancellation.

**Ефективно для:** new Go HTTP services, refactors that mix interface ownership or leak gin.Context across goroutines, agent-generated scaffolds where main.go bloats with business logic, services adopting structured error handling.

## Applies If (ALL must hold)

- Building or refactoring a Go HTTP service (Gin, Echo, or net/http).
- Module supports the standard `cmd/` + `internal/` layout (Go 1.18+).
- Team accepts a single ErrorHandler middleware that owns HTTP error mapping.
- All I/O functions can take `context.Context` as the first argument.

## Skip If (ANY kills it)

- Library or CLI tool — no HTTP layer; layout rules don't apply.
- Heavily-customised framework forcing a different layout (go-kit, goa).
- Codebase already uses the pkg/internal-monorepo pattern with shared interfaces.
- gRPC-only service — see go-grpc methodology instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Go module name | string (`github.com/acme/svc`) | `go.mod` |
| Framework choice | string (gin / echo / net-http) | tech stack ADR |
| Database driver | string (pgx, gorm, sqlx) | infra ADR |
| Worker concurrency target | int (default `runtime.NumCPU()`) | perf budget |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-error-handling]]` | AppError type the middleware maps from. |
| `[[go-http-handlers]]` | thin-handler pattern this layout enforces. |
| `[[go-concurrency]]` | worker-pool patterns referenced in the scaffold. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules: layout, consumer interfaces, *Request DTOs, thin main, context first, ErrorHandler, Pool patterns | ~800 |
| `content/02-output-contract.xml` | essential | Required dir tree + invariants: cmd/api/main.go, internal/*, no external internal/ imports | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: interface in impl, gin.Context in goroutine, c.JSON for errors, bloated main, blocking Pool.Submit | ~700 |
| `content/04-procedure.xml` | medium | 6-step scaffold procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Root question on Go HTTP service + standard layout support | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate cmd/api/main.go wiring | sonnet | Template-driven; no novel reasoning. |
| Author AppError + middleware | sonnet | Pattern from templates/. |
| Worker pool scaffold | opus | Concurrency invariants benefit from careful reasoning. |
| Layout audit on existing repo | sonnet | check-layout.sh + diff reporting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/app-error.go` | AppError struct, sentinel errors, constructors. |
| `templates/check-layout.sh` | CI script verifying internal/ dirs exist and internal/ is not imported externally. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-backend.py` | Validates a Go repo against the layout invariants (cmd/, internal/, no external internal/ imports). | Pre-commit gate; CI before `go build`. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[go-error-handling]]` — error types this layout uses
- `[[go-http-handlers]]` — handler thinness rules
- `[[go-concurrency]]` — pool / channel invariants

## Decision tree

The decision tree at `content/06-decision-tree.xml` checks: HTTP service yes/no, standard layout permitted yes/no, context-first allowed yes/no. All three yes -> run-the-checklist; any no -> defer.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/app-error.go`

```go
// internal/apperror/apperror.go — typed application errors with HTTP mapping
package apperror

import (
	"fmt"
	"net/http"
)

// AppError carries a machine-readable code, human message, HTTP status, and optional cause.
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

// Unwrap enables errors.Is / errors.As traversal.
func (e *AppError) Unwrap() error { return e.Err }

// Sentinel errors — use errors.Is to check.
var (
	ErrNotFound = &AppError{
		Code: "NOT_FOUND", Message: "Resource not found", HTTPStatus: http.StatusNotFound,
	}
	ErrUnauthorized = &AppError{
		Code: "UNAUTHORIZED", Message: "Authentication required", HTTPStatus: http.StatusUnauthorized,
	}
	ErrBadRequest = &AppError{
		Code: "BAD_REQUEST", Message: "Invalid request", HTTPStatus: http.StatusBadRequest,
	}
)

// NewNotFound creates a dynamic not-found error with resource name.
func NewNotFound(resource string) *AppError {
	return &AppError{
		Code:       "NOT_FOUND",
		Message:    fmt.Sprintf("%s not found", resource),
		HTTPStatus: http.StatusNotFound,
	}
}

// Wrap wraps a cause error with an internal error message.
func Wrap(err error, message string) *AppError {
	return &AppError{
		Code:       "INTERNAL_ERROR",
		Message:    message,
		HTTPStatus: http.StatusInternalServerError,
		Err:        err,
	}
}
```

### `templates/check-layout.sh`

```bash
set -euo pipefail

required=("cmd" "internal/handler" "internal/service" "internal/repository" "internal/model")
for d in "${required[@]}"; do
  [[ -d "$d" ]] || { echo "MISSING required dir: $d"; exit 1; }
done

# Verify internal/ is not imported from outside this module.
mod=$(go list -m)
if grep -RIn "\"$mod/internal/" --include="*.go" -- . | grep -v "^./$mod" >/dev/null 2>&1; then
  echo "FAIL — internal/ package imported from outside module"
  exit 1
fi

go vet ./...
echo "layout ok"
```
