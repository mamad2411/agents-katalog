---
name: hunter-recon
description: >-
  Build the Surface Map: the enumerated, deduplicated inventory of every
  addressable, probe-able unit of the quarry (HTTP routes, web screens and their
  controls, CLI commands, background jobs, data contracts, auth/role/flag states,
  external integrations). The Surface Map is the denominator for every coverage
  claim and the work queue for the hunt. Load and run this before any probing,
  before assigning oracles, before stating any coverage fraction or verdict, and
  whenever asked to map, enumerate, inventory, or scope a target, or when a
  coverage denominator is missing or stale. Produces surface_map.json plus a
  human-reviewable surface_map.md. Assumes hunter-doctrine is loaded.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
argument-hint: <target-path-or-url> [--black-box] [--budget N] [--resume <run-dir>]
---

# Hunter Recon — building the Surface Map

Recon answers the question every later stage depends on: **what is there to
probe?** Its output, the Surface Map, is the denominator. Without it, "clean"
has no meaning and "coverage" is a number over an unknown total — which the
doctrine forbids (`hunter-doctrine`, coverage honesty).

Recon does not probe for deviations. It enumerates surfaces and assesses risk.
Probing is a later stage that consumes this map. A surface recon has never
listed is not cold and not dark — it is **invisible**, which is worse than dark
because it is not even counted. The whole job of recon is to shrink the
invisible set to zero and label everything else `dark` until a probe touches it.

## Inputs

- `target`: a filesystem path to source, a base URL, or both.
- `mode`: `source` (source available), `black-box` (URL only), or `hybrid`.
- `budget`: max SurfaceUnits to fully expand and rank (default 5000). Governs the
  combinatorial-explosion mitigation below.
- `resume`: a prior run directory. Recon is incremental against it (see
  "Incremental re-recon").

## Output artifacts

Written to `<run-dir>/recon/`:

- `surface_map.json` — the machine contract. Array of SurfaceUnit objects plus a
  `recon_meta` header. This is the denominator every downstream stage reads.
- `surface_map.md` — human-reviewable rendering (see "Markdown rendering").
- `recon_quality.json` — the completeness cross-validation result (see
  "Completeness check").

`surface_map.json` is a **stable contract**. Do not reorder or renumber on
re-recon; ids are content-derived (below) so they survive.

## The SurfaceUnit schema

Every enumerated surface is one SurfaceUnit. Emit exactly this shape:

```json
{
  "id": "sfc/http/7a3f9c2e",
  "class": "http_route",
  "locator": {
    "method": "POST",
    "path": "/api/v1/cart/{cartId}/items",
    "handler": "src/routes/cart.ts:addItem",
    "url": null
  },
  "discovered_by": ["route_table_introspection", "openapi"],
  "requires_state": {
    "auth": "customer",
    "role": null,
    "flags": {"new_checkout": true},
    "tenant": null
  },
  "risk_score": 74,
  "risk_factors": ["mutation", "auth_boundary", "user_input", "money"],
  "assigned_oracles": ["http_contract", "authz_probe", "injection"],
  "coverage_state": "dark",
  "last_probed": null,
  "parent": null,
  "sampling": {"sampled": false, "cohort": null, "represents": 1},
  "content_hash": "7a3f9c2e"
}
```

Field rules:

- `id` — `sfc/<class-prefix>/<content_hash>`. **Content-derived and stable**
  (see "Stable ids"). Never a sequential counter.
- `class` — one of the surface classes in the table below. Closed set.
- `locator` — everything needed to address the surface. Populate the fields
  relevant to the class; leave others `null`. Never invent a locator you did not
  observe (anti-fabrication law).
- `discovered_by` — every enumeration method that independently found this unit.
  Two or more entries is the per-unit signal that the completeness check passed
  for this unit.
- `requires_state` — the auth/role/flag/tenant state the surface needs. This is
  what makes surfaces multiply; see "The state matrix".
- `risk_score` — 0–100 from the risk model below. Drives probe order and
  sampling.
- `assigned_oracles` — oracle ids to run against this surface, chosen by class +
  risk_factors. Recon assigns; it does not run them.
- `coverage_state` — one of `dark | cold | sign | find`. Recon initialises
  **every** unit to `dark`. Only a probing stage may advance it. Never emit
  `cold` from recon.
- `last_probed` — ISO-8601 or `null`. `null` until probed.
- `parent` — the `id` of the containing surface (a control's screen, a
  subcommand's parent command); `null` for top-level.
- `sampling` — if this unit stands in for a cohort under the explosion
  mitigation, `sampled=true`, `cohort` names the group, `represents` is the
  cohort size. Coverage math multiplies by `represents` only when explicitly
  chosen to (see "Combinatorial explosion").

## Surface classes and enumeration strategies

Enumerate each class by the methods listed, **in priority order**. Priority is
by yield-per-cost and reliability: authoritative machine-readable sources first,
crawling last. Run at least two methods per class you touch — the completeness
check depends on it.

### `http_route` — HTTP/API endpoints
1. **Framework route-table introspection** (authoritative). Ask the framework
   for its registered routes rather than reading source: Express
   `app._router.stack`, Flask `app.url_map`, FastAPI `app.routes`, Django
   `get_resolver().url_patterns`, Rails `bin/rails routes`, Spring
   `RequestMappingHandlerMapping`. This yields method, path template, and
   handler with no guessing.
2. **OpenAPI / Swagger / GraphQL SDL.** If a spec is served or committed, parse
   it. Each operation is a SurfaceUnit; GraphQL fields/mutations are units.
3. **Decorator / annotation scan.** `@app.route`, `@GetMapping`, `@Controller`,
   Nest `@Get()`. Regex is acceptable here because it cross-validates method 1.
4. **Sitemap / robots.txt** (black-box friendly).
5. **Crawl** — follow links and forms from known entry points under each auth
   state. Lowest priority: crawling misses unlinked and mutation endpoints.

### `web_page` — pages/screens/views
1. **Router config** — React Router route tree, Vue Router, Angular routes,
   Next/Nuxt/SvelteKit **file-based routing conventions** (a file at
   `app/orders/[id]/page.tsx` is the screen `/orders/:id`).
2. **Server-side view registry** — Django views, Rails controllers+views.
3. **Crawl with auth states** — crawl once per auth state in the matrix;
   authenticated crawls reveal screens anonymous crawls cannot.
4. **Sitemap.**

### `ui_control` — interactive controls per screen
For each `web_page`, build a DOM inventory. These are child SurfaceUnits with
`parent` set to the screen. Enumerate:
- buttons, links, submit/reset controls
- inputs and their types, selects, textareas, checkboxes, radios, file uploads
- forms (each form is a unit; its action+method is a probe target)
- menus, dropdowns, tabs, accordions
- dialogs / modals and the trigger that opens them
- drag/gesture targets, sortable lists, canvas hit-regions
Methods: (1) static JSX/template scan for control elements; (2) live DOM
snapshot after render (authoritative — reveals dynamically injected controls);
(3) accessibility-tree walk (roles: `button`, `textbox`, `menuitem`) which
catches controls the other two miss.

### `cli_command` — command-line surface
1. **`--help` tree walk** — parse top-level help, recurse into every subcommand
   (`tool x --help`, `tool x y --help`) until no new subcommands appear. Each
   command and each flag is captured; each command is a SurfaceUnit, flags live
   in its `locator`.
2. **Arg-parser introspection** — enumerate the parser directly (argparse
   `_subparsers`, Click `commands`, Cobra command tree, clap) — authoritative,
   no help-text parsing.
3. **Man pages** and shell-completion scripts (they encode the full command
   grammar).

### `background_job` — jobs, queues, crons, workers, event handlers
Enumerate: cron schedules (`crontab`, k8s `CronJob`, framework schedulers),
queue consumers (Celery tasks, Sidekiq workers, BullMQ processors, SQS/Kafka
handlers), webhook receivers, and message/event subscribers. Methods: scheduler
config files; task-registration decorators (`@celery.task`, `@shared_task`);
queue-binding declarations. Locator carries the trigger (schedule or
topic/queue name) and the handler.

### `data_contract` — schemas, migrations, types
Enumerate: DB schema (tables, columns, constraints, indexes), migrations (each
migration is a unit — it is a behaviour change), ORM models, JSON Schema / Avro
/ Protobuf definitions, and exported type definitions. These are probe targets
for `data_contract` oracles (constraint enforcement, migration reversibility)
and inputs to `hunter-intent`.

### `integration` — external integrations
Enumerate outbound dependencies: third-party API clients, payment/email/SMS
providers, object storage, auth providers (OAuth/SAML), feature-flag services.
Methods: SDK/client imports, base-URL constants, env-var references for
endpoints and keys. Locator names the provider and the call site. Never probe a
live third party without explicit authorisation (`hunter-doctrine`, escalation).

### `state` — the auth/role/feature-flag matrix
Not probed directly, but every other surface's `requires_state` draws from it.
Enumerate the axes (below) so the multiplication is explicit and auditable.

## The state matrix — why surfaces multiply

A surface behaves differently under different state. `GET /admin/users` is one
locator but three distinct surfaces: anonymous (should 401/redirect), customer
(should 403), admin (should 200). Each is a separate SurfaceUnit with the same
locator and different `requires_state`, because each has a different expectation
and a different oracle (the anonymous and customer variants are authz probes).

Enumerate the state axes first:

- **auth**: `anonymous`, plus each authenticated principal type you have or were
  given credentials for.
- **role**: every role/permission tier (`customer`, `admin`, `support`, …).
- **flags**: every feature flag that gates a surface, with its on/off values.
- **tenant / plan**: multi-tenancy or plan tiers that change behaviour.

The naive product of axes is the explosion problem. Mitigate as below — do not
enumerate the full Cartesian product blindly.

## Combinatorial explosion — sampling and risk ranking

If `|surfaces| × |states|` exceeds `budget`, do not silently truncate (that
manufactures invisible surfaces). Instead:

1. **Rank every candidate unit by `risk_score`.** Fully expand the top of the
   ranking until budget is reached.
2. **Cohort the tail.** Group the un-expanded remainder into cohorts by
   (class, risk band, shared handler/route-prefix). Emit **one representative
   SurfaceUnit per cohort** with `sampling.sampled=true`, `cohort` naming the
   group, and `represents` = cohort size. Choose the representative as the
   highest-risk member of the cohort.
3. **Never merge a sampled cohort into cold.** A cohort represented by one
   probed unit is reported as `sampled` coverage, not full coverage: the
   verdict is at best `PASS (LIMITED COVERAGE)` with the cohorts listed. The
   coverage fraction states probed-units / total-units where a cohort counts as
   `represents` units in the denominator and 1 in the numerator unless every
   member was probed.

State the budget, the cutoff risk_score, and the cohort list in `recon_meta`, so
the sampling decision is auditable rather than hidden.

## The risk model

`risk_score` is 0–100. Compute it as the sum of factor weights, capped at 100.
Record the contributing factors in `risk_factors` so the score is explainable
(the doctrine requires attribution).

| Factor | Weight | Applies when |
|---|---|---|
| `mutation` | 20 | Surface writes state (POST/PUT/PATCH/DELETE, mutation, migration, job that writes) |
| `auth_boundary` | 18 | Surface enforces or crosses an authz boundary |
| `money` | 18 | Payments, billing, credits, pricing, refunds |
| `pii` | 14 | Handles personal or sensitive data |
| `user_input` | 12 | Accepts free-form or file input (injection/upload surface) |
| `external_io` | 10 | Calls a third party or writes to storage/queue |
| `destructive` | 12 | Deletes, cancels, or is irreversible |
| `recently_changed` | 10 | Touched by a commit in the change window (see re-recon) |
| `complexity` | up to 8 | Handler cyclomatic complexity / branch count, scaled |
| `unauthenticated_reach` | 8 | Reachable with no credential |
| `historical_finds` | 10 | This surface or its neighbourhood produced Finds before |

Weights are the default model; record the model version in `recon_meta`
(`risk_model: v1`) so scores are comparable across runs. Ranking, not the
absolute number, drives probe order.

## Stable ids

Downstream stages, resumed runs, and diffs across commits all key on `id`. Ids
must survive re-recon and must not collide.

- `content_hash` = first 8 hex chars of a hash over the **stable identity
  tuple** for the class, never over volatile fields:
  - `http_route`: `method + normalised_path_template + requires_state`
    (path *template*, so `/users/{id}` is stable regardless of the id value).
  - `web_page`: `route_pattern + requires_state`.
  - `ui_control`: `parent_id + control_role + accessible_name + ordinal`.
  - `cli_command`: `full_command_path` (e.g. `tool db migrate`).
  - `background_job`: `handler_symbol + trigger`.
  - `data_contract`: `object_kind + qualified_name`.
  - `integration`: `provider + call_site_symbol`.
- Never hash line numbers, timestamps, generated ids, or free-text — they churn
  and would break stability on trivial edits.
- On collision (same tuple, genuinely different surface), append the
  disambiguating field to the tuple and record it in `locator`; do not truncate
  to fewer hash chars.

## Black-box mode (URL only, no source)

When only a base URL is available, route-table and file-routing methods are
gone. Use, in priority order:

1. **Served OpenAPI/GraphQL** — probe conventional locations
   (`/openapi.json`, `/swagger.json`, `/v3/api-docs`, `/graphql` introspection,
   `/.well-known/`). A served spec is authoritative and turns black-box into a
   near-source-level map.
2. **`sitemap.xml`, `robots.txt`.**
3. **Authenticated crawl per auth state** — the primary method. Crawl links and
   forms; every form action+method is an `http_route` unit; every rendered
   screen is a `web_page`; live DOM inventory gives `ui_control` units.
4. **Response-shape inference** — observed 404 vs 401 vs 405 distinguishes
   "route absent" from "route exists, wrong method/auth", which reveals surfaces
   crawling did not link to. Record the observation as `discovered_by:
   response_probe`; it is weaker evidence, so mark such units
   `risk_factors: ["inferred_existence"]`.

In black-box mode, invisible surfaces are unavoidably larger. Say so: set
`recon_meta.mode = black-box` and `recon_meta.enumeration_confidence` lower, and
expect the completeness check to report higher disagreement. Never present a
black-box map as if it were exhaustive.

## Completeness check — cross-validate two methods per class

An enumeration you cannot corroborate is a Sign about the map, not a fact. For
every class you enumerated, run **at least two independent methods** and compare
their unit sets. Emit `recon_quality.json`:

```json
{
  "per_class": [
    {
      "class": "http_route",
      "methods": ["route_table_introspection", "openapi"],
      "counts": {"route_table_introspection": 142, "openapi": 128},
      "agreement": 121,
      "only_in_route_table_introspection": 21,
      "only_in_openapi": 7,
      "disagreement_ratio": 0.20,
      "quality": "review"
    }
  ],
  "classes_single_method": ["background_job"],
  "invisible_risk": "medium",
  "overall": "review"
}
```

Interpret disagreement as a **recon-quality signal**, not noise:

- Units only in the route table but not the spec → spec is stale, or endpoints
  are undocumented. Both are worth a `conformance` Sign (feed to
  `hunter-intent`).
- Units only in the spec but not the route table → documented-but-unimplemented,
  or the introspection missed a router. Investigate before trusting the map.
- `disagreement_ratio` > 0.15 on any class → `quality: review`; > 0.40 →
  `quality: unreliable`, and the map must not be used as a full-coverage
  denominator until reconciled.
- Any class enumerated by only one method → list it in `classes_single_method`
  and raise `invisible_risk`. One method is a Sign, not corroboration.

Never discard the smaller set to make the numbers agree. Reconcile by
investigating each discrepancy, or carry it forward as a known map gap.

## Incremental re-recon on a changed codebase

Recon is re-run as the quarry changes. Do not rebuild from scratch and do not
renumber.

1. Load the prior `surface_map.json`.
2. Compute the **change window**: the set of files changed since the prior run's
   commit (via VCS diff). If no VCS, fall back to mtime.
3. Re-enumerate; recompute `content_hash` per unit.
4. Diff by `id`:
   - **unchanged** ids → carry forward `coverage_state` and `last_probed`. A
     surface that was `cold` and did not change **stays cold**.
   - **new** ids → `coverage_state: dark`, `+recently_changed` risk factor.
   - **id present before, gone now** → mark `coverage_state: dark` and
     `locator.removed: true`; keep it one run so its disappearance is auditable,
     then drop.
   - **same id, changed handler content** (handler hash differs) → **reset to
     `dark`** even though the id is stable. Prior cold evidence is stale; a
     changed handler is unprobed until re-probed. Add `recently_changed`.
5. Record `recon_meta.rerecon_from` and the change-window size.

The rule that makes this honest: **a changed surface loses its cold status.**
Carrying a stale cold across a code change is reporting dark as clean.

## Markdown rendering

`surface_map.md` is for a human reviewing scope before the hunt spends budget.
Order and content:

```
# Surface Map — <target>  ·  <hunt-id>  ·  <ISO-8601>
mode: source  ·  risk_model: v1  ·  budget: 5000/5000 used

## Totals
surfaces: 318  ·  dark: 318  ·  cold: 0  ·  sign: 0  ·  find: 0
sampled cohorts: 4 (representing 1,142 units)
recon quality: review (http_route disagreement 0.20)

## By class            surfaces   states   risk (max/median)
http_route                  142        3    92 / 61
web_page                     54        3    70 / 40
ui_control                   88        -    55 / 22
cli_command                  19        1    48 / 20
background_job                7        -    66 / 40
data_contract                 5        -    50 / 30
integration                   3        -    72 / 55

## Highest-risk surfaces (probe order)
92  sfc/http/7a3f9c2e  POST /api/v1/cart/{cartId}/items  [customer]  mutation,money,user_input
88  sfc/http/1d0b...   DELETE /api/v1/accounts/{id}      [admin]     mutation,destructive,pii
...

## Sampled cohorts (not fully covered)
cohort http:list-endpoints  ·  represents 214  ·  representative sfc/http/9c1a...

## Recon-quality flags
http_route: 21 routes not in OpenAPI (spec stale?) — feed to hunter-intent
background_job: single-method enumeration — invisible_risk raised
```

Every surface renders `dark` here because recon has not probed anything. That is
correct output: the map is the to-do list, not a result.

## Handoff

- To **the probing stages**: `surface_map.json` is the work queue, ordered by
  `risk_score`, with `assigned_oracles` per unit. A probe advances a unit's
  `coverage_state` and stamps `last_probed`; it never edits `id`, `locator`, or
  `risk_score`.
- To **`hunter-intent`**: the map plus `recon_quality.json`. Intent binds
  NormativeClaims to `SurfaceUnit.id`s and treats spec/route disagreements as
  candidate conformance deviations.
- To **reporting** (`brand-system` §12.2): the map is the coverage denominator.
  The report's coverage map is a direct rendering of `coverage_state` across all
  units. Any verdict cites `probed / total` from this file.

## Self-check before emitting the map

- [ ] Every unit initialised `coverage_state: dark`; no `cold` emitted by recon
- [ ] Every id is content-derived and stable, not sequential
- [ ] At least two enumeration methods per class attempted;
      `classes_single_method` populated where not
- [ ] `recon_quality.json` written with per-class disagreement
- [ ] State matrix expanded into `requires_state`; authz variants are distinct units
- [ ] Explosion handled by risk-ranked sampling with cohorts, not truncation
- [ ] No locator, endpoint, or control fabricated — every unit traces to a method
- [ ] `recon_meta` records mode, budget, risk_model, and rerecon_from
