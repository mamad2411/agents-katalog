---
name: golang-api-versioning
description: >
  Version Go HTTP and gRPC APIs: URL/header/proto strategies, deprecation,
  compatibility tests, and sunset. Use for owned public or partner APIs.
---

# Golang API Versioning

## Research grounding

Runbook for **API versioning** in Go services so clients can evolve without
hard breaks. Covers REST and gRPC/protobuf. Skill id: `golang-api-versioning`.

## Scope And Authorization

- **In scope:** APIs you own; coordinated consumer communication.
- **Out of scope:** forcing breaking changes on external parties without notice when contracts forbid it.
- Prefer compatibility tests in CI.
- Pair with `golang-api-surface`, `api-documentation-writing`, `code-quality-standards`.

## When To Use

- Introducing v2 of a Go HTTP API or new proto package version.
- Deprecating fields/endpoints with sunset dates.
- Choosing URL vs header vs content-type versioning.
- Focus tokens: **golang, api, versioning**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Initial surface design | `golang-api-surface` |
| Gateway auth | `golang-api-gateway-auth` |
| Proto schema recovery | `protobuf-grpc-reverse-engineering` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Strategy | Pros | Cons |
| --- | --- | --- |
| URL `/v1` | Very visible | Path clutter; multi-mount |
| Header `Accept-Version` | Clean paths | Harder to cache/debug |
| Content-Type profile | Precise | Client complexity |
| gRPC package `api.v1` | Idiomatic | Dual servers during migrate |
| Additive proto fields | Compatible | Must not reuse field numbers |

**Compatibility rules (REST):** additive JSON fields OK; remove/rename = major.
**Proto:** never change field meaning; reserve deleted numbers.

## Workflow

### 1. Confirm scope and success criteria

1. API consumers, SLA for deprecation, authorization.
2. Success: vN and vN+1 coexist; contract tests both green; sunset plan published.
3. Define what “breaking” means for this product.

### 2. Inventory

1. Current versions in traffic; oldest client.
2. Undocumented clients (mobile app builds).
3. Shared DTOs that couple versions accidentally.

### 3. Baseline

1. Capture OpenAPI/proto for current version (hash).
2. List planned breaking changes.

### 4. Implement versioning in Go

```go
// URL versioning with chi/mux style
r.Route("/v1", func(r chi.Router) {
	r.Mount("/", v1.NewHandler(svc))
})
r.Route("/v2", func(r chi.Router) {
	r.Mount("/", v2.NewHandler(svc))
})

// Shared domain service; adapters map DTOs per version
```

```protobuf
// proto
package myapi.v1;
service Users { rpc GetUser(GetUserRequest) returns (User); }
```

1. Prefer separate packages `internal/api/v1` and `v2` over giant switch soup.
2. Share domain layer; translate at edges.
3. Deprecation headers: `Deprecation: true`, `Sunset: <date>`, `Link` to docs.
4. Feature flags for risky additive behavior if needed.
5. gRPC: run both service versions; dual-register carefully.

### 5. Verify with evidence

```bash
go test ./internal/api/v1/... ./internal/api/v2/... -count=1
go test ./... -count=1
# buf breaking / openapi diff in CI
buf breaking --against '.git#branch=main'
```

1. Old client fixtures still pass against v1.
2. New fields appear in v2 only; v1 ignores unknown inbound fields if policy says so.
3. Load both versions under canary.

### 6. Observe and harden

1. Metrics: request count by version; alert when v1 traffic near sunset still high.
2. Communication plan to consumers at T-90/T-30/T-7.
3. After sunset, return clear 410/Unimplemented with upgrade link.

### 7. Hand off

1. Changelog and migration guide.
2. SDK release matrix.
3. Remove v1 code only after traffic ~0 and legal hold ok.

## Deprecation timeline example

| Milestone | Action |
| --- | --- |
| T0 | Announce v2; v1 frozen (bugfix only) |
| T+30 | SDKs default to v2 |
| T+90 | Sunset header enforced messaging |
| T+180 | Disable v1 |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Break | New major version | Silent field type change |
| Proto | Reserve deleted fields | Reuse field number |
| Code | Version packages | One handler `if version==` everywhere |
| Sunset | Metrics-gated | Hard cut no notice |
| Topic fidelity | Versioning tactics | Generic go test only |

## Output Checklist

- [ ] Version strategy chosen and documented
- [ ] Dual-running plan for old/new
- [ ] Contract/breaking CI checks
- [ ] Deprecation headers and dates
- [ ] Consumer communication sent
- [ ] Traffic metrics by version
- [ ] `code-quality-standards` applied

## Rules

- Additive when possible; break only with major + notice.
- Focus on `golang-api-versioning`.
- Never reuse proto field numbers.
- Authorized API changes only.
