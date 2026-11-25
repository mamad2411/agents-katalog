---
name: golang-api-surface
description: >
  Design and review Go HTTP/gRPC API surfaces: resource models, error shapes,
  pagination, idempotency, least exposure, and compatibility. Use for owned APIs.
---

# Golang API Surface

## Research grounding

Runbook for **shaping the external API surface** of Go services—what is exposed,
how it is modeled, and how to keep it minimal and stable. Skill id:
`golang-api-surface`.

## Scope And Authorization

- **In scope:** APIs you own; authorized design reviews.
- **Out of scope:** scraping or abusing third-party private APIs.
- Prefer design docs + contract tests before large releases.
- Redact production URLs/secrets in examples.
- Pair with `golang-api-versioning`, `api-documentation-writing`, `code-quality-standards`.

## When To Use

- Greenfield Go service public/partner API design.
- Reducing over-broad endpoints or debug surfaces in production.
- Standardizing errors, pagination, and filter query params.
- Focus tokens: **golang, api, surface**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Versioning strategy | `golang-api-versioning` |
| Gateway authentication | `golang-api-gateway-auth` |
| AuthZ matrix | `golang-access-control` |
| OpenAPI writing only | `api-documentation-writing` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Resources | Nouns, consistent IDs, avoid RPC-over-HTTP unless intentional |
| Methods | Safe GET; idempotent PUT/DELETE; POST creates/actions |
| Errors | Stable `code`, HTTP status, no stack traces to clients |
| Pagination | Cursor preferred over deep offset |
| Filtering | Allowlist fields; cap page size |
| Exposure | No `/debug/pprof` public; admin under separate auth/listener |
| gRPC | Package versioning; field numbers stable; no debug service public |
| Pitfalls | Returning entire DB models; chatty N+1 endpoints |

## Workflow

### 1. Confirm scope and success criteria

1. Consumers (mobile, partner, internal), SLA, authorization.
2. Success: documented surface; contract tests; unused endpoints removed or gated.
3. Security: default deny on new routes without review.

### 2. Inventory current surface

```bash
# Find registered routes (project-specific)
rg -n "HandleFunc|Methods\(|http\.Handle|Register.*Server" --glob '*.go'
# gRPC services
rg -n "Register\w+Server" --glob '*.go'
```

1. List public vs internal listeners.
2. Flag debug, metrics, and admin endpoints exposure.
3. Compare with OpenAPI/proto published contracts.

### 3. Baseline

1. Traffic per route (top N).
2. Error rate and payload size p99.
3. Consumer SDKs depending on fields.

### 4. Design / reshape

```go
type ErrorBody struct {
	Code    string `json:"code"`
	Message string `json:"message"`
	// Details optional, non-sensitive
}

type ListParams struct {
	PageSize int
	Cursor   string
}

const MaxPageSize = 100

func clampPage(n int) int {
	if n <= 0 {
		return 20
	}
	if n > MaxPageSize {
		return MaxPageSize
	}
	return n
}
```

1. Expose DTOs, not internal storage models (hide password hashes, PII by default).
2. Prefer coarse resources over micro-endpoints that force chatty clients.
3. Action endpoints (`POST /invoices/{id}/void`) when not CRUD.
4. Idempotency-Key on creating POSTs where double-submit hurts.
5. Disable or bind `pprof`/admin to localhost or mesh-only.

### 5. Verify with evidence

```bash
go test ./api/... -count=1
go test ./... -count=1
# contract tests / openapi validate
```

1. Unknown fields policy documented (ignore vs reject).
2. AuthZ coverage on every route (`golang-access-control`).
3. Public port scan of staging: no unexpected listeners.

### 6. Observe and harden

1. Metrics per route template (not raw path IDs).
2. Alert on 404 spikes (scanning) and 5xx.
3. Deprecate unused fields/routes with timeline.

### 7. Hand off

1. Publish OpenAPI/proto; changelog process.
2. SDK generation notes if any.
3. Link versioning skill for breaking changes.

## Surface minimization checklist

| Question | If no |
| --- | --- |
| Does a consumer need it? | Do not expose |
| Is admin required publicly? | Separate listener |
| Can field be enumerated for abuse? | Gate + rate limit |
| Is error message an oracle? | Genericize |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Model | Explicit DTO | `json` on ORM entity |
| Pagination | Cursor + max | Unlimited list |
| Debug | Mesh-only pprof | `/debug/*` on :443 |
| Errors | Stable codes | panic stack to client |
| Topic fidelity | API surface design | Generic go test only |

## Output Checklist

- [ ] Consumer goals and surface inventory done
- [ ] DTOs and error shape standardized
- [ ] Pagination/filter caps enforced
- [ ] Debug/admin exposure reduced
- [ ] Contract tests green
- [ ] Metrics on route templates
- [ ] Docs published
- [ ] `code-quality-standards` applied

## Rules

- Least exposure; stable contracts.
- Focus on `golang-api-surface`.
- Authorized API testing only.
- Never document live secrets in examples.
