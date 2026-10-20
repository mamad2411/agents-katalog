---
description: Naming, forbidden legacy tokens - always applied on every edit
alwaysApply: true
---

# Naming

## Purpose

Always applied on every agent turn and every file edit. Forbid cryptic identifiers and legacy product tokens. Enforce semantic clarity aligned with `lead-intent-processor`. Go receivers: `quality.mdc`. Comments: `comments.mdc`. Package layout: `structure.mdc`. Root clutter: `core.mdc`.

## Forbidden trash naming

Do not use cryptic suffixes, meaningless numbers, or lazy abbreviations.

| Pattern | Why banned | Better alternative |
| :--- | :--- | :--- |
| `m1`, `m2`, `m8` | Cryptic milestone/versioning | `load_test_milestone_8`, `v2_reconciler` |
| `n1`, `n2` | Meaningless numeric tags | `ledger_fix_2026`, `consistency_patch` |
| `v1_old`, `new_logic` | Temporal naming (rots immediately) | `legacy_v1_compat`, `batch_processor_v2` |
| `f1`, `f2` | Lazy filter/field abbreviations | `license_filter`, `geo_filter` |
| `ch`, `pg`, `rd`, `rdb`, `rdbs` | Driver/client abbreviations | `clickhouseConn`, `postgresConn`, `redisClient`, `redisShards` |
| `res`, `res2` | Generic result variables | `auction_result`, `auth_response` |
| `GAP_prefix_001` style codes, `WI-123` | Bureaucratic ticket/milestone IDs | Semantic slug: `wire_silent_reject_hot_path` |
| `M-8`, `M8` milestone tokens in titles | Milestone tokens in commits and headings | Concrete surface name: `silent_reject_hot_path` |

## Forbidden bureaucratic naming

Do not use ticket prefixes, gap codes, or milestone IDs in file names, backlog headings, commit titles, operator docs, or Grafana panel text.

| Banned | Use instead |
| :--- | :--- |
| Ticket-style gap codes (`GAP` + team + number) | Describe the work: `antifraud_doc_code_parity` |
| `P0 item #4`, `Action item 7` | Semantic slug in PR description only |
| `WI-4521`, `JIRA-123` | Link to tracker URL in PR description only; not in repo prose |

Backlog files in `deploy/vendor/` are removed; cross-reference by semantic slug in PR descriptions only.

CI: `bash scripts/ci/naming/legacy_naming.sh` rejects `GAP-<TEAM>-<digits>` in `README.md`, `docs/`, `deploy/vendor/`, `.cursor/rules/`.

Exception: `fault_proof proof=open` in fault tests is telemetry, not a backlog ID (`fault-tests.mdc`).

## Legacy token ban

Strictly forbidden in new code, documentation, and variable names. Remove existing occurrences when touched.

| Forbidden | Use instead |
| :--- | :--- |
| `BidShard` | `ad-event-processor` (or internal short `aed` below) |
| `espx`, `espx_`, `ESPX_` | `ad-event` / `ad_event`, or product short `aed` / `aed_` |
| `legacy`, `old` (without context) | Specific context, e.g. `legacy_v1_api` |

## Product vs stack surfaces

| Surface | Canonical name |
| :--- | :--- |
| Go module, imports, public docs titles | `ad-event-processor` |
| Docker compose volumes | `ad_event_processor_*` (historical prefix) |
| Admin UI product strings | `ad-event-processor` |
| Control plane API | `/api/v1/*` on `:8188` |
| Env / license knobs (existing contract) | `AD_EVENT_PROCESSOR_*` |

### Internal short form: `aed`

Inside the repo (shell helpers, script log tags, local identifiers, operator notes), **`aed`** is the allowed abbreviation for **ad-event-processor** (same role as `lip` for lead-intent-processor).

| Form | Use |
| :--- | :--- |
| `aed` | prose short name, log tags (`aed: …`) |
| `aed_` / `AED_` | shell function / local prefix when a product token is required (`aed_compose`, not `ad_event_processor_compose`) |
| `ad-event-processor` | module path, UI brand, README titles, external-facing copy |

Do not invent parallel product tokens (`aep`, `adep`, `ad_event_proc`). Prefer `aed` over spelling out `ad_event_processor_*` for **internal shell helpers**.

**Keep full `ad_event_processor_*` (wire / historical contracts — do not shorten):**

| Kind | Examples |
| :--- | :--- |
| Env keys | `AD_EVENT_PROCESSOR_*` |
| Prometheus / metrics | `ad_event_processor_edge_*` |
| Go build tags | `ad_event_processor_bpf_trace` |
| Ingress schema | `ad_event_processor_native` |
| DB user / DB name / compose volumes | `ad_event_processor_user`, `ad_event_processor_*` volumes |

**Shell helpers (use `aed_`):** `aed_go_bin` / `aed_go_run` / `aed_go_build`, `aed_compose`, `aed_read_env`, `aed_compose_dev_overlay`, stack helpers in `scripts/dev/stack/stack.sh`.

## Forbidden marketing prose

Technical docs (`README.md`, `docs/`, `deploy/vendor/ANTIFRAUD.md`, `docs/ARCHITECTURE.md`, Grafana descriptions) must not read like sales copy. Doc lie catalog: `anti-slop.mdc` Documentation lie modes.

| Banned in tech docs | Use instead |
| :--- | :--- |
| `enterprise-grade`, `premium`, `world-class` | Name the surface: `edge-xdp`, `FilterEngine` |
| `ultra-low latency`, `ultra-fast`, `lightning-fast` | SLA from `core.mdc` or bench name + scope |
| `guarantee`, `guaranteed`, `never` (unqualified) | Concrete behavior or `fail-closed` / batch-only ML |
| `eliminated` (Redis/script ops) | File + function that runs the op, or "cached on miss" |
| `hundreds of thousands of RPS` (unqualified) | Load-test config or measured metric |
| `Why buyers choose`, competitor tables | Remove; SKU limits in `sku.yaml` only |
| `unlimited` as hype | License field `max_active_campaigns: 0` = no cap in JWT schema |
| `intelligent`, `AI-powered` (unqualified) | `cmd/fraud-scorer`, `cmd/ivt-detector`, SKU flag |
| `complete data privacy`, `spy-tool` | Omit; not verifiable in code |
| `crush`, `eliminates fees` pitch | Omit |

`deploy/vendor/SALES.md`: SKU table and license workflow only; no competitor anchors or positioning essays.

User-visible admin UI (`web/src`): no `(skeleton)`, demo KPIs, or "coming soon" without `StubBanner` (`ui.mdc`, `anti-slop.mdc`). Fixture/seed display strings: trash tokens, round KPIs, duplicate row labels — full ban tables in `ui.mdc` (**Fixture and seed data**); canonical names in `cmd/admin/seed_catalog.go`.

## Semantic clarity

Match naming quality and structure of `lead-intent-processor`.

### Structs and fields

- **No god structs:** `Service` or equivalent with 50+ fields or unrelated domains — split by role (`Store`, `Runtime`, `Worker`) per domain package (`modular-monolith.mdc`).
- **No god ports:** `Host`, `Effects`, `DeliveryHost` and similar **<= 12 methods**; split before adding (`modular-monolith.mdc`).
- **Explicit roles:** `PostgresGate` is too vague. Use `PostgresWriteGate` or `PostgresCampaignStore`.
- **Field names:** `settlePoolField` is trash. Use `SettlementPool`.

### Handler and interface names

Banned as interface or field names on HTTP handlers: `API`, `Backend`, `Provider`, `Service` (when the name only means "implementation"). Name the **route or domain role** (`MiniAppRoutes`, `CampaignReader`). File matches type: `mini_app_routes.go`, not `backend.go`.

### File and path naming

- Production Go: snake_case `<role>_<rest>.go` — `track_core.go`, `runtime_patch.go`, `handlers.go` (package `fraudadmin`).
- **Inside `internal/<domain>/`:** do not repeat the package directory name as a filename prefix. The path already scopes the domain.
  - BAD: `internal/campaign/campaign_dto.go`, `internal/flow/flow_validate.go`, `internal/fraudadmin/fraudadmin_handlers.go`
  - GOOD: `internal/campaign/dto.go`, `internal/flow/validate.go`, `internal/fraudadmin/handlers.go`
- Cross-package or composition-root files keep the domain token when the package name differs: `internal/controlplane/campaign_runtime_bridge.go`.
- **Banned (new):** `controlplane/*_aliases.go`, new `service_<domain>_*.go` in controlplane, `domains.go` prefix tokens — `modular-monolith.mdc` (**Migration cruft ban**).
- Split near 500 lines or when transport mixes with core logic.
- Tests beside code: `*_test.go`, `*_bench_test.go`, `*_fault_test.go`.
- **Shared vocabulary subpackages** (split by role, not filename prefix):
  - `internal/licensing/verify/`, `entitlements/`, `trial/` — JWT/HWID, limits/features, trial SKU
  - `internal/domain/budget/`, `shard/` — settlement/invariants; slot map and Redis hash-tag keys
  - Hot path imports `domain`, `domain/budget`, `domain/shard` directly; avoid `domain/db` on ingest/filter
  - One-release `aliases.go` at `licensing/` and `domain/` roots only (`modular-monolith.mdc`)

```go
// BAD path
internal/campaign/campaign_editor_handlers.go
internal/controlplane/fraudadmin_aliases.go
internal/controlplane/service_fraud_api.go

// GOOD path
internal/campaign/editor_handlers.go
internal/fraudadmin/handlers.go
internal/controlplane/fraudadmin_bridge.go
```

## Examples

```go
// BAD
f := openFilter()
v1 := f.Check(req)

// GOOD
geoFilter := openGeoFilter()
verdict := geoFilter.Check(request)

// BAD
type Service struct {
    ch driver.Conn
    m8 *Worker
}

// GOOD
type ClickHouseStore struct {
    conn           driver.Conn
    loadTestWorker *LoadTestWorker
}
```

## Related rules

`anti-slop.mdc`, `code-style.mdc`, `comments.mdc`, `core.mdc`, `quality.mdc`, `structure.mdc`.
