---
description: Modular monolith layout, bridge policy, god- and micro-package bans
globs:
  - internal/**
  - cmd/**
alwaysApply: false
---

# Modular Monolith and God-Package Policy

## Purpose

`cmd/control` is a **modular monolith**: one deployable process, many **compile-time domain packages**. Bridges wire domains to the composition root. **God packages and god services are forbidden** — split or extract before adding surface. **Micro-packages and premature splits are also forbidden** — keep or merge until a domain boundary is real.

Cross-ref: `structure.mdc`, `boundaries.mdc`, `cold-path.mdc`, `naming.mdc`.

## Modular monolith (what this is)

| Fact | Rule |
| :--- | :--- |
| Runtime | Single `cmd/control` process (admin, payment webhooks, workers in-process) |
| Packages | `internal/campaign/`, `brand/`, `flow/`, … are **modules**, not microservices |
| Data | Shared Postgres; outbox applies Redis side effects — no cross-service RPC for admin |
| Tracker | Separate binary; must not import `controlplane` admin (`boundaries.mdc`) |

**Not in scope:** service mesh, per-domain repos, gRPC between admin domains, shared "platform" god package that owns all business rules.

## `doc.go` (mandatory)

Every production Go package **must** include `doc.go` at its directory root.

| Scope | Path |
| :--- | :--- |
| Domain / service | `internal/<name>/doc.go` |
| Composition root | `internal/controlplane/doc.go` |
| Shared util | `pkg/<name>/doc.go` |
| Binary entry | `cmd/<binary>/doc.go` (`package main`) |
| Focused subpackage | `internal/controlplane/authz/doc.go`, `ingestion/traceprobe/doc.go`, … |

**Excluded:** generated subtrees (`db/`, `pb/`, sqlc output) inside a domain — no `doc.go` there.

**Content:** mandatory detailed package doc in `doc.go` — role, invariants, allowed/forbidden, verification commands (`comments.mdc`). Edit `doc.go` in the same PR when adding a package; no Python/shell codegen.

New package without `doc.go` in the same PR is a **merge blocker**. Legacy tree: add or refresh when touching the package.

## Bridges (`*_bridge.go`, `*_admin_adapter.go`)

Bridges exist **only inside the modular monolith composition root** (`internal/controlplane/` and domain `NewReader(deps)` wiring). They are **dependency-inversion glue**, not a layer.

| Allowed in a bridge | Forbidden in a bridge |
| :--- | :--- |
| `var _ domain.Host = (*Service)(nil)` compile check | Business rules, validation, SQL, report math |
| Pass `pool`, `cfg`, outbox enqueue to domain `Store` / `Runtime` | New HTTP routes or handler bodies |
| Map controlplane DTO <-> domain DTO at the boundary | Growing `Effects` / `Host` without splitting the port |
| Factory: `NewManagementOpsReader(svc)` from deps struct | Pass-through shim that only re-exports domain funcs (delete in same migration) |
| Read config knobs (`AutoscaleEnabled`, thresholds) | "Temporary" logic left for more than one PR |

**Naming:** `*_bridge.go` = `Service` implements a domain port. `*_admin_adapter.go` = thin registration or error mapping. `*_wire.go` / `adminapi_wire.go` = route table only. Do not call RTB type glue in `ingestion/` a "bridge" in new docs — use `*_glue.go` or keep existing names only.

**Lifecycle:** When a domain moves out of `controlplane`, shrink the matching bridge in the **same** change set. A bridge file that only grows for three PRs without domain growth is a god-service smell — stop and split.

## Migration cruft ban (no prefix/suffix hacks)

**Reference:** `lead-intent-processor` wires domains via **direct imports** (`internal/app/deps.go` → `internal/crm/admin`, `internal/ingest`, …). No type-alias files, no filename-prefix inventories.

These patterns were transitional during `controlplane` drain. **Forbidden in new code**; delete when touching a call site.

| Banned pattern | Example | Do instead |
| :--- | :--- | :--- |
| `*_aliases.go` | `controlplane/fraudadmin_aliases.go`, `internal/nodeadmin_aliases.go` | Import `fraudadmin.FooDTO` at call site; fix tests to use domain package |
| Pass-through funcs in alias files | `func ScoreNode(...) { return nodeadmin.ScoreNode(...) }` | Call `nodeadmin.ScoreNode` directly |
| New `service_<domain>_*.go` in controlplane | `service_fraud_api.go` | `internal/fraudadmin/handlers.go` + bridge only |
| Filename repeats package dir | `fraudadmin_handlers.go` in `internal/fraudadmin/` | `handlers.go` (`naming.mdc`) |
| `domains.go` `Prefixes: []string{...}` for new domains | Classify files by `node_`, `service_rtb` token | `composition_drain_inventory.go` row: package path + bridge file |
| Redundant subdir | `internal/broker/server/` | `internal/broker/` |
| `pkg/*/server/` duplicating `internal/*` | Dead `pkg/broker/server` | Delete; `pkg/` = wire protocol only |

**Allowed (not a hack):**

| Pattern | When |
| :--- | :--- |
| `*_bridge.go` in `controlplane/` | Implements domain `Host` / `Effects`; <= 200 lines |
| `*admin` package name | Real domain boundary (`fraudadmin`, `billingadmin`) — not a filename prefix |
| `composition_drain_inventory.go` | Explicit source file → target package map |

**Sunset:** delete all `*_aliases.go` and prefix-based `domains.go` rows as call sites migrate (`composition_drain_inventory.go`).

## God package ban (hard ceilings)

Violations block merge unless an explicit waiver names the split PR that follows within one release.

| Surface | Ceiling | Action when exceeded |
| :--- | :--- | :--- |
| Package file count | **40 production `.go` files** (exclude `db/`, `*_test.go`, `pb/`) | Split by subdomain package (`reportjob` vs `reports`) |
| Package LOC | **~8000** non-generated LOC | Split; do not add a 900-line file |
| Single production file | **~500 lines** | Split by role (`handlers`, `store`, `worker`) — `code-style.mdc` |
| `controlplane.Service` fields | **No unrelated domain fields**; prefer domain `Store` / `Runtime` on `Service` with lazy init | Extract field group to domain package |
| Domain port (`Host`, `Effects`, `DeliveryHost`, …) | **<= 12 methods** per interface | Split port (`WizardHost`, `ImportExportHost`, …) |
| Bridge file | **<= 200 lines** per `*_bridge.go` | Second bridge file by concern (`campaign_delivery_bridge.go`, not one 600-line file) |
| `internal/controlplane` growth | **Must shrink net LOC** over a domain extraction milestone | New features land in domain package first |

**Legacy ports** already above 12 methods (`campaign.Effects`, …): do **not** add methods — split or use an existing narrower port (`WizardHost`, `ImportExportHost`, …) in the same PR.

**God package definition:** one package that owns unrelated domains, or keeps absorbing handlers/SQL while sibling packages stay stubs. **`internal/controlplane` must trend smaller** — it is composition root, not the product core.

## Micro-package ban (no numeric floor — semantic floor)

There is **no** minimum file/LOC count. A package is **too small / invalid** when it has no real domain boundary, not when it is merely compact.

**Valid compact package** (keep as-is): owns a bounded admin surface end-to-end — e.g. `marginguard/`, `platformadmin/` (`doc.go`, `http_handlers.go`, `store.go`, `types.go`, narrow `host.go`). Small file count is fine.

### Minimum viable new `internal/<domain>/`

Create a **new** domain package only when extracting from `controlplane` or splitting a god package **and** the same change set includes:

| Required (same PR / milestone) | Detail |
| :--- | :--- |
| Bounded surface | Own `/api/v1/...` routes **or** worker tick entry called from `cmd/control` |
| Persistence or rules | `store.go` / `*_tx.go` **or** pure validators used by handlers (not dead types) |
| `doc.go` | Package module doc at root — **mandatory**, may be long (`comments.mdc`) |
| Wire | Registration in `adminapi_wire.go` or worker bootstrap — not orphan import |

**At least two** of: handlers (or worker), store/tx, behavioral validators/types. A lone `host.go` + `types.go` stub is **rejected**.

### Forbidden micro-patterns

| Pattern | Why banned | Do instead |
| :--- | :--- | :--- |
| `internal/common`, `internal/util`, `internal/helpers` with domain logic | Hidden god kernel | `pkg/coldpath` (stdlib-only consumers) or owning domain package |
| Package = one DTO, one helper, one sqlc wrapper | Ceremony without boundary | Keep in parent domain file |
| `pkg/*` used by a single `internal/*` package | Fake shared layer | Move into that internal package |
| Split parent only to fix import cycle with 1–2 funcs | Accidental architecture | Narrow port or move func to correct owner |
| Premature hot-path split (`ingest/`, `filter/` under `ingestion/`) without explicit task | `structure.mdc` future target | Stay in `ingestion/` until milestone |
| New package with no routes/store in tree | Placeholder package | Finish extraction in same PR or do not create |
| Pass-through package that only re-exports another | Duplicate boundary | Direct import from owning domain package |

### When **not** to create a package (keep in parent)

- Fewer than **3** production `.go` files **and** no dedicated OpenAPI path prefix **and** no worker loop — keep in existing domain or `controlplane` until extraction is complete.
- Logic used only inside one existing package — add a file there (`editor_handlers.go`), not `internal/campaigneditor/`.
- Parent is **below** god ceilings and team is not running a named extraction milestone.

### Premature split vs required split

| Situation | Action |
| :--- | :--- |
| `controlplane` or domain package **above** god ceilings (`structure.mdc`) | Split by subdomain (`reports` / `reportjob`) |
| Named milestone / operator task: "extract X from controlplane" | New package in **atomic** PR |
| "Might need this later" | **Forbidden** — no empty package |
| Compact but complete domain (`brand/`, `marginguard/`) | **Keep** — not micro |

Violations block merge unless the PR completes the minimum viable table in the same change set.

## How to avoid god packages (required order)

1. **New admin behavior** -> `internal/<domain>/` (`handlers.go`, `store.go`, `*_tx.go`). Register from `adminapi_wire.go`.
2. **Postgres + outbox** -> domain `store` method; bridge only calls `store` and maps errors.
3. **Cross-domain orchestration** (publish gate + flow validate) -> domain `Runtime` with injected narrow port, not 20 new `Service` methods.
4. **Shared helper** -> `pkg/coldpath` or domain package function; never `controlplane/util.go` for one domain.
5. **Type at call site** -> import domain package (`fraudadmin.FooDTO`); never add `*_aliases.go`
6. **Hot path** -> stays in `ingestion/`; never "bridge" admin into tracker.

## Agent checklist (before adding code)

| Question | If "no" -> |
| :--- | :--- |
| Does this belong to one domain package? | Create or extend that package |
| Is new package minimum viable (2+ of handlers/worker, store, rules + wire + `doc.go`)? | Do not create; finish in parent or complete extraction |
| Would this be a util/common package? | Forbidden — use domain or `pkg/coldpath` |
| Can `Host`/`Effects` stay <= 12 methods? | Split the port first |
| Is `controlplane` only wiring + outbox? | Move logic down |
| Is this a second composition root? | Forbidden |
| Will package/file ceilings breach? | Split in same PR |
| Is split only because parent is "large" but under ceilings? | Premature — keep in parent |

## Related rules

`structure.mdc`, `boundaries.mdc`, `cold-path.mdc`, `naming.mdc`, `code-style.mdc`, `anti-slop.mdc`.
