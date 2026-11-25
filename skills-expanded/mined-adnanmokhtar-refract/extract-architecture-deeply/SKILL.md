---
name: extract-architecture-deeply
description: Round-two deep architecture extraction — analyzes top-level package/module import graph, traces representative request lifecycles end-to-end, identifies bounded-context boundaries, locates cross-cutting concerns. Output is a structured architecture map with file:line citations. Used by /setup-project Phase 2.8 in REFINE mode to upgrade round-one architecture detection from "this is layered MVC" to a concrete layer diagram + 3-5 traced lifecycles.
kind: skill
pack: learning
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: extract-architecture-deeply

## Purpose

Round-one Phase 2 detects the architectural shape from folder structure + framework conventions ("controllers/", "services/", "repositories/" → "this is layered MVC"). That gets you the floor (knowing which packs to apply).

Round-two needs the actual graph. A first-pass `ai/architecture.md` says "controllers depend on services depend on repositories." Round-two says "the request lifecycle for `POST /api/invoices` is: `app/controllers/invoices.py:Invoice.create:42` → `app/services/billing.py:BillingService.create_invoice:128` → `app/repositories/invoice.py:InvoiceRepository.persist:67` → `INSERT into invoices...` (transaction wraps lines 130-145, fans out to `LedgerService.append_entries:215` after persist). The `auth` middleware injects user at `app/middleware/auth.py:34` ahead of the controller; tracing is via `tracing.py:23` decorator." That second version is anchorable.

## Premise

- Real source is the truth. Read every handler in the traced lifecycle — entry, every middleware in the chain, every called function down to the I/O boundary — before writing the YAML.
- Every step, layer name, boundary, and cross-cutting concern cites `<path:line>` resolvable at the current commit.
- The import graph is computed from real `import`/`require` statements, not from folder naming conventions.
- Empty extraction is honest — a `not detected` row for a missing concern + the WEAK gate are valid outputs.
- Fabrication — inventing a layer from a folder name, a middleware that's defined-but-never-registered, or a lifecycle from framework defaults — is the failure mode the WEAK gate flags.

## Mechanical halt

- Hand-wave grep on architecture output — `etc.`, `...`, `the usual layers`, `roughly layered`, `appears MVC-ish`, a step listed without `<file:line>` — REFUSE to advance.
- Rewrite the offending block with concrete citations OR downgrade the section to `[REFINE-WEAK: architecture]`.
- If a cross-cutting concern is genuinely absent (no rate-limiter, no tracing), record `<NOT-DETECTED: <reason>>` (e.g. `<NOT-DETECTED: no middleware registered for rate-limiting>`).
- Never synthesize a "framework default" the codebase doesn't actually wire up — the rate-limit-or-tracing gap is the finding.

## When to use

- `/setup-project --refine` Phase 2.8 — once per project (not per domain).
- Manually when refreshing `ai/architecture.md` for a project that has substantial code but a generic round-one architecture file.

## Inputs

- `entry_surfaces` (optional) — list of surfaces to trace (default: auto-discover from `manage.py` / `main.ts` / `cmd/server/main.go` / `index.ts` / Procfile).
- `output_section` — section path inside `.claude/_refine-extract.md` (default: `## Architecture`).

## Procedure

### Step 1 — Build a top-level package/module graph

Detect the language + module-resolution rule:

- Python: every `__init__.py` directory is a package. Read each top-level package's `__init__.py` for re-exports.
- Node / TypeScript: top-level `src/<package>/` directories OR Nx / Turborepo / pnpm workspaces (`packages/*`).
- Go: top-level directories that aren't `vendor/` / `_examples/`. Each has its own `package <name>` declaration.
- Java: top-level Maven/Gradle modules; package roots inside `src/main/java/`.
- Rust: workspace members; or top-level `mod` declarations in `lib.rs`.
- Ruby: `app/` subdirectories in Rails; or gem `lib/<gem>/` roots.

For each top-level package P:

- List the packages it imports from (NOT external libs — only this codebase's own packages).
- Count import occurrences (a single line `import X` is one edge; `from X import (a, b, c)` is still one edge — fan-in/fan-out is per-edge, not per-symbol).

Output: an adjacency list. Compute fan-in (who imports me) and fan-out (who do I import).

### Step 2 — Identify layers from the graph

A layer is a *level* in the partial order. Detect by:

- Cycle detection: any cycle is a layer-violation candidate (or a sign that the project doesn't enforce layers).
- Levels: nodes with fan-in 0 are leaves (sinks) — typically infrastructure/data layer. Nodes with fan-out 0 are roots (entry points) — typically the API or CLI layer.
- Heuristic naming match: package names like `controllers`, `routers`, `endpoints`, `views`, `handlers` are presentation layer. `services`, `usecases`, `application` are application layer. `repositories`, `gateways`, `adapters` are infrastructure layer. `models`, `entities`, `domain`, `core` are domain layer.

Synthesize a layer diagram (text/ASCII):

```
┌────────────────────────────────────────────────────────┐
│ Presentation:  app/controllers/, app/middleware/       │
│                ↓                                        │
│ Application:   app/services/, app/usecases/            │
│                ↓                                        │
│ Domain:        app/models/, app/domain/                │
│                ↓                                        │
│ Infrastructure: app/repositories/, app/external/       │
└────────────────────────────────────────────────────────┘
```

If the codebase doesn't fit a clean layered shape (e.g. modular monolith / hexagonal / CQRS / actor-based), use the actual shape. **Never force a layered diagram onto a non-layered codebase.** Record what you find:

```
Hexagonal: ports = app/ports/, adapters = app/adapters/, domain = app/core/
Boundary discipline: domain NEVER imports adapters (verified by import graph)
```

### Step 3 — Identify bounded-context boundaries

A boundary is a *deliberate* lack of edge. Compute:

- For each pair of top-level packages (A, B), check if there's an import edge A→B AND B→A.
- If A and B BOTH have substantial fan-out elsewhere but no edge between them, it's a likely boundary.
- Cross-reference with the business-domain extraction (Phase 2.7). If `billing` and `healthcare` are detected as separate domains AND their packages don't import each other, that's a confirmed boundary.

Boundaries are mediated by something — find the mediator:

- Anti-corruption layer (translator class).
- Façade (a class in package A that's the only entry point used by B).
- Event bus / queue (A publishes; B consumes; no direct call).

Record: each boundary as `<A> ⇄ <B> via <mediator>`.

### Step 4 — Trace representative request lifecycles

Pick at LEAST 3 representative entry points per surface:

- HTTP: 1 GET (read-heavy), 1 POST (write-heavy), 1 DELETE (cascade-revealing).
- GraphQL: 1 query + 1 mutation.
- Queue consumer: 1 most-frequent message.
- Scheduled job: 1 longest-running.
- CLI: 1 critical command.

Pick by heuristics: high test coverage, mentioned in monitoring/Sentry config, high git churn, or appears in user-flow docs. If unclear, pick the first 3 that match a CRUD pattern.

For each picked entry:

1. Find the route/handler registration (e.g. `urls.py`, `app.use('/api/...')`, `@app.route`, `@Controller`).
2. Find the handler function.
3. Walk the call graph: for each function call inside the handler body, follow the import + read the called function. Stop at:
   - External lib calls (record but don't recurse).
   - DB ORM calls (record as `[DB-WRITE Invoice]` / `[DB-READ Invoice]`).
   - HTTP/queue calls (record as `[EXTERNAL <vendor>]` / `[QUEUE-PUBLISH <topic>]`).
   - The end of the handler.
4. Note middleware in the chain (auth, logging, rate-limit, tracing, error-handling).

Record per lifecycle:

```yaml
- name: POST /api/invoices
  entry: app/controllers/invoices.py:create:42
  middleware:
    - auth at app/middleware/auth.py:34
    - tracing at app/middleware/tracing.py:23
  steps:
    - app/services/billing.py:BillingService.create_invoice:128
    - app/repositories/invoice.py:InvoiceRepository.persist:67
    - "[DB-WRITE Invoice via INSERT]"
    - app/services/ledger.py:LedgerService.append_entries:215
    - "[DB-WRITE LedgerEntry x N via INSERT]"
    - app/events/outbox.py:OutboxRepository.append:45 (event: invoice.created)
  transaction_boundary: app/services/billing.py:128-145 (manual `with transaction.atomic()`)
  side_effects:
    - DB writes: Invoice (1), LedgerEntry (N), OutboxEvent (1)
    - External calls: none in transaction; outbox-relay polls separately
  error_paths:
    - ValidationError → 422 via app/exceptions/handlers.py:18
    - IntegrityError (FK violation) → 409 via app/exceptions/handlers.py:34
```

### Step 5 — Locate cross-cutting concerns

For each concern, find where it lives + how it's invoked:

- **Authentication** — middleware? decorator? In-handler check?
- **Authorization** — RBAC / ABAC? Where is the permission check?
- **Logging** — structured (JSON)? plain? Which library? Standard fields?
- **Tracing** — OpenTelemetry? framework-native? Which exporter?
- **Rate limiting** — middleware? per-user? per-IP? per-endpoint?
- **Error handling** — global handler? per-controller try/catch? framework default?
- **Caching** — decorator? service-layer? Where is the invalidation?
- **Feature flags** — library? per-request? per-tenant?

Each one: 1 line + `file:line`.

### Step 6 — Output

Write to `.claude/_refine-extract.md` under `## Architecture`:

```yaml
extraction_date: <YYYY-MM-DD>
shape: <layered|hexagonal|modular-monolith|microservices|cqrs|actor|mixed>
strong_signals: ["import-graph", "lifecycles", "boundaries", "cross-cutting"]

import_graph_summary:
  top_level_packages: <N>
  total_edges: <N>
  cycle_violations: <N>   # 0 means clean layered enforcement
  notable: |
    <2-3 sentences calling out anything unusual — heavy fan-in modules,
     packages that violate the layer ordering, etc.>

layer_diagram: |
  <ASCII diagram from Step 2>

bounded_contexts:
  - name: <context>
    packages: [<list>]
    boundary_discipline: <enforced|partial|none>
    mediator: <facade|event|anti-corruption-layer|none>

representative_lifecycles:
  - <YAML block per Step 4>

cross_cutting:
  authentication: { mechanism: <...>, location: <file:line> }
  authorization: { mechanism: <...>, location: <file:line> }
  logging: { library: <...>, shape: <...>, location: <file:line> }
  tracing: { library: <...>, exporter: <...>, location: <file:line> }
  rate_limiting: { mechanism: <...>, location: <file:line>, or "not detected" }
  error_handling: { strategy: <...>, location: <file:line> }
  caching: { strategy: <...>, invalidation: <...>, location: <file:line>, or "not detected" }
  feature_flags: { library: <...>, location: <file:line>, or "not detected" }
```

## Quality gate

- **STRONG**: import graph extracted, ≥ 3 lifecycles traced end-to-end, ≥ 1 boundary identified, ≥ 4 cross-cutting concerns located — **and each of those counts is evidenced the way the worked example above evidences them**: every lifecycle step carries `<file:function:line>`, every boundary names the two modules it separates plus the import that crosses it, every cross-cutting concern is `located` at a `<file:line>` in the chain rather than merely `detected` in the dependency list.
- A concern recorded as `not detected` counts toward the ≥ 4 **only when the greps that looked for it are named**. "Not detected" with no search behind it is silence, and silence should not clear a gate.
- **WEAK**: any of the above missed → flag `[REFINE-WEAK: architecture]`. Phase 4.7-DEEP will NOT rewrite `ai/architecture.md` from a WEAK extraction.
- The gate used to be four bare counts while the worked example above carried all the rigour — so a run could hit `3 lifecycles / 1 boundary / 4 concerns` with a layer diagram inferred from folder names and pass. The citation requirements are the example's standard, moved into the gate where it binds.

## Anti-patterns

- **Forcing a layered diagram** onto a non-layered codebase.
- **Skipping import-graph cycles** as inconvenient — cycles are real architectural information; report them.
- **Synthesizing lifecycles** from framework defaults instead of tracing actual handlers.
- **Citing middleware that's defined but never registered** — only middleware in the actual chain counts.
- **Generalizing across surfaces** — if HTTP and queue handlers behave differently (e.g. queue handlers skip tenant middleware), record both. Don't average.

## Verify (postconditions)

Contract: [`templates/snippets/postcondition-check.md`](../../../../snippets/postcondition-check.md). **Preconditions are not verification** — this skill guards its entry and must also check its exit. Every entry under `## Failure modes` that this skill's own write could cause becomes a check here, observed rather than assumed, reported when it passes as well as when it fails, and `NOT RUN` with a reason where no signal is available. A failure mode the skill documented and never checked is a risk it accepted on the caller's behalf without saying so.
