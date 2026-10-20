---
description: SLA, sources-only repo, rule index, commits
alwaysApply: true
---

# Core Policy

## Purpose

Canonical SLA ceilings, repository hygiene, commit conventions, and the rule index for `ad-event-processor`. Human architecture docs live in `docs/ARCHITECTURE.md` and `docs/DEVELOPMENT.md`. Do not duplicate task backlogs in rules or docs.

Engineering rules live in `.cursor/rules/*.mdc`. Do not copy agent rules into `docs/`.

## SLA and budgets

| Surface | Metric / knob | Ceiling |
| :--- | :--- | :--- |
| Tracker ingest | `ad_http_request_duration_seconds` p95 | < 50 ms |
| Tracker ingest | `ad_http_request_duration_seconds` p99 | < 80 ms (hard ceiling 100 ms) |
| Filter deadline | `FILTER_TIMEOUT_MS` (production) | <= 100 ms |
| Filter deadline | `FILTER_TIMEOUT_MS` (dev default) | 5000 ms |
| Redis unified-filter Lua | p99 per shard | < 10 ms |
| Geo filter | p99 (sampled) | < 10 us |
| RTB auction | `RunAuction` p99 | < 15 us |
| RTB catalog scan | p99 candidates scanned | < 500 |
| Fraud boost snapshot | incremental per `FilterEngine.Check` | < 500 us |
| Fraud boost bench | `BenchmarkFilterFraudBoost` | ~90 ns, 0 allocs/op |
| Static slot shard | `GetShard` (StaticSlot) | ~5.6 ns, 0 allocs/op |
| Load-test abort | control-cohort p99 > 80 ms for 30 s | abort run |
| Load-test abort | budget invariant violation | abort run |
| Postgres budget | `current_spend <= budget_limit` | `AssertBudgetInvariant` (+/-1 micro-unit) |

Load-test abort triggers: control-cohort handler p99 above 80 ms for 30 seconds, or any budget invariant violation in Postgres.

## Sources-only repository

A fresh clone is not runnable out of the box. Required bootstrap:

1. `make gen` / `make proto` for sqlc and protobuf outputs.
2. Provide env and secrets (see `.env.example`, `config/env/`).
3. Build BPF artifacts (`make gen bpf-dev`).
4. Fetch GeoIP data per `docs/DEVELOPMENT.md`.
5. Start compose (`bash scripts/dev/stack/stack.sh`).

**Never commit:** generated code, `bin/*`, `.cache/`, `var/`, secrets, or runtime JWT files. Canonical ignore: root `.gitignore`. Local dev license path: `var/license.jwt` (not repo-root `license.jwt`).

**Root clutter ban:** no `*.txt` or `*.log` in repo root (except README, LICENSE). Gate and test transcripts go in `var/ci/` (`CI_ARTIFACT_DIR`); load-test and fault drill output in other `var/` subtrees. Compiled binaries go in `bin/`, not root.

**Agent verification on operator machines:** shared dev hosts are not CI. Agents must not loop `go build`, `go test`, or full-repo typecheck without an explicit operator ask. Default checks: `read_lints`, `grep`, `gofmt -e`, scoped `go list -e`. Full table: `anti-slop.mdc` (**Agent local environment**, **Compile and test ritual ban**).

## Commit policy

| Rule | Detail |
| :--- | :--- |
| Title style | Imperative plain English; lead with Add, Remove, Fix, Wire, Drop, Guard, Reject |
| Title surface | Name concrete surface: route, handler, table, env var, binary |
| Avoid prefixes | `refactor:`, `docs:`, `chore:`, vague umbrellas (`perf`, `cleanup`, `misc`, `WIP`) |
| Avoid tokens | Milestone tokens (`M-...`, `GAP-...`) |
| Body | Optional: why and what to verify; no file manifest |
| Scope | One logical change set per commit |
| Docs-only | No docs-only commits unless code ships in the same commit |

## Rule index

Always applied on every agent turn (no glob filter):

| File | Scope |
| :--- | :--- |
| `core.mdc` | SLA, repo policy, commit style, rule index |
| `naming.mdc` | Identifiers, legacy tokens, marketing ban |
| `comments.mdc` | Required/forbidden comments, ASCII format, critical-code headers |
| `quality.mdc` | Go receivers, verification honesty |
| `anti-slop.mdc` | CI honesty, doc lie modes, slop gates, agent-resistant verification, agent checklist |

| Rule file | Topic |
| :--- | :--- |
| `architecture.mdc` | Hot/cold invariants, I/O round-trip limits, fail-closed |
| `structure.mdc` | Current flat layout, cmd map, package split policy |
| `development.mdc` | Codegen, compose, benchmarks, fault runbooks |
| `ci.mdc` | Merge gates, BPF thresholds, test tiers |
| `code-style.mdc` | Layout, types, sqlc, proto, PR gates |
| `hot-path.mdc` | `/track`, parsers, gnet, filters, 0 allocs |
| `parser.mdc` | Ingress wire policy, chaos verification |
| `traffic.mdc` | `/click`, `/track`, macros, CAPI |
| `cold-path.mdc` | Admin, payment, ledger, notify |
| `data-layer.mdc` | Redis, Lua, PG, CH, sharding |
| `boundaries.mdc` | Import matrix, layer coupling, agent scope, test dishonesty catalog |
| `control-plane.mdc` | Outbox, workers, admin API, server-authoritative RBAC |
| `modular-monolith.mdc` | Modular monolith, bridges, god- and micro-package policy, migration cruft ban |
| `frontend-modular.mdc` | Admin SPA layers, Tailwind + shadcn/ui package map |
| `frontend-patterns.mdc` | Frontend patterns (паттерны фронтенда): composition, effects, races, errors, async/cancel |
| `frontend-primitives.mdc` | UI primitive stack (kit, chrome, Button/Input, shell roles, variant vs action) |
| `frontend-slop.mdc` | Admin mock tiers, agent execution protocol, visual layout drift **VL-***, RBAC, styling, errors, Playwright honesty |
| `rtb.mdc` | OpenRTB auction, shadow to live |
| `edge.mdc` | Nginx Lua, XDP sync operators, fingerprint pipeline |
| `xdp-bpf.mdc` | XDP/eBPF C hot path: maps, token bucket, verifier, test tiers |
| `compliance.mdc` | Defensive perimeter |
| `licensing.mdc` | JWT, trial registry, USDT tiers |
| `regions.mdc` | Enterprise multi-region |
| `ui.mdc` | Admin layout, macro/micro layout, cold path, AI honesty |
| `frontend-slop.mdc` | Admin mock tiers, agent protocol, **Shared style contracts**, visual layout VL-* |
| `agent-self-initiative.mdc` | LLM self-initiative ban: SD-* catalog, layout invariant, revert protocol (@ cite) |
| `react.mdc` | React Hot (charts/telemetry) vs Cold (CRUD), heap leaks, canvas |
| `frontend-hot-path.mdc` | Suboptimal ops taxonomy, scale regimes S/L/F, Big-O vs locality |
| `tradeoffs.mdc` | Rejected alternatives, evidence matrix |
| `fault-tests.mdc` | Chaos/outbox/parser proofs |
| `testing.mdc` | Test taxonomy, holdouts |
| `load-test-bpf.mdc` | Load test + BPF probes |
| `xdp-bpf.mdc` | XDP/eBPF C per-packet contracts and verification |

## Precedence

When rules conflict, apply in this order:

1. `core.mdc` - SLA and repo policy.
2. `anti-slop.mdc` - CI honesty and agent verification.
3. `testing.mdc` - holdout tests and invariant proofs.
4. `hot-path.mdc` - ingest path constraints.
5. `cold-path.mdc` - admin, payment, ledger paths.
6. `structure.mdc` - current flat controlplane layout is canonical.

## Related rules

`architecture.mdc`, `anti-slop.mdc`, `comments.mdc`, `development.mdc`, `naming.mdc`, `quality.mdc`.
