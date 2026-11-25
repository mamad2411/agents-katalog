---
name: lane-backend
description: Backend build lane of a delivery run — sibling-mirror premise, prior-art and new-dependency gates, signal→binding-constraint tables, generate rules, lens dispatch by touch and domain, spec conformance. Read by @architect, @implementer and /add-feature; not run on its own.
kind: skill
pack: delivery
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# lane-backend — the backend build procedure of a delivery run

The stack-specific half of `/add-feature`, cut from the backend pack's former `add-feature` body —
the orchestrator (`/add-feature`, delivery pack) owns the run, the tiers, the acceptance contract,
the human gates and the verdict; this skill owns how THIS stack builds a change. Read by
`@architect` (constraints and design slices), `@implementer` (one task at a time) and the
orchestrator (which lenses to dispatch, what to validate). Tier words below are run tiers
(`.claude/templates/governance/tiers.json`): T1 ≈ the former trivial, T2 ≈ standard, T3 ≈ heavy.

| Section | Run phase | Reader |
|---|---|---|
| Premise · Prior-art gate | P2 | @product-analyst, orchestrator |
| Phase 2 — signal reads, binding constraints, design slices | P4 | @architect |
| Phase 3 Retrieve · Phase 4 Generate · Sibling-shape halt · New-dependency gate · All-tier floors · Standards gate | P6 | @implementer |
| Phase 5 Update | P6b | doc-writer / orchestrator |
| Phase 6 Validate (lens tables, spec conformance, observability, release) | P7–P12 | orchestrator |
| Phase 7 Improve | P15 | orchestrator |

## The Premise (read this first, internalize, do not deviate)

**Existing siblings are the truth.** When 50 endpoints in this codebase follow pattern X — same controller shape, same DI primitive, same error envelope, same validation library, same file path under `<module>/<kind>/...` — that pattern IS the project's intentional truth. The 51st endpoint does not get to invent pattern Y. Future maintainers can't predict where things live, fixes can't be applied uniformly, and the codebase fragments by one more weight every time someone improvises.

**The agent's job is exactly this:**
1. Find ≥2 sibling endpoints / services / modules in the same pack (same module if it exists; nearest neighbor module if not).
2. Read their shape — file paths, naming, layer boundaries, error envelopes, validation, DI primitives, logging, test layout.
3. Mirror that shape for the new feature. Innovating without precedent is the failure mode.

**Siblings govern shape, not guarantees.** The engineering baseline outranks every sibling (§ Standards gate): a sibling with no unique constraint, no timeout or no denial test is a defect to fix in this change, not a shape to copy.

**The agent does NOT:**
- Ask the user about cosmetic style (camelCase vs snake_case, file naming, import order). **Mirror the sibling silently.**
- Ask the user which error type / DI primitive / validation library to use. **Mirror the sibling silently.**
- Draft an ADR to legitimize a one-off shape. **Mirror the sibling, no ADR.**
- Reach for a pattern from training data when the codebase already has one. **Sibling wins.**

**The agent ONLY asks the user when:**
- **No siblings exist** — this is genuinely the first feature in a new module / new layer / new primitive class. Ask once, get the shape blessed, then mirror it forever after.
- **Requirements conflict with existing patterns** — the new feature's shape genuinely cannot be expressed in the project's existing primitives (e.g., first async job in a sync-only codebase).
- **Cross-module dependency requires architecture decision** — a new coupling between modules that didn't talk before; this is an ADR, not a code question.

That's it. Three escalation triggers. Everything else is silent sibling-mirror with the gates below.

## Prior-art gate (every tier, before design)

Sibling search finds a pattern to *copy*. This gate asks a different question first: **does the capability already exist** under another name? Building a second copy of something the codebase already has is the single most expensive waste mode in a mature project, and sibling-mirror does not catch it.

1. Search by **behavior, not name** — handler/route names, service methods, domain verbs, table/column names that would already cover the ask. A "send invoice email" feature may already live inside a `NotificationService.dispatch(...)` path.
2. **Near-duplicate found → HALT.** Surface the existing implementation (path + what it does) and ask the user: extend it, replace it, or ship a deliberate parallel (rare — requires a one-line rationale recorded in the PR).
3. Nothing matches → continue (the orchestrator records the result in `requirements.md § Impact`).

This is the cheapest check in the command and prevents the costliest rework. It runs at every tier.

## Sibling-shape halt (mechanical gate, all tiers)

**Before declaring success / before merge, the auditor compares the new file(s) against ≥2 sibling files in the same module.** This is the same `regressed` mechanism from `parity-auditor.md` (V2-structure conformance) — borrowed, adapted for greenfield adds.

Halt if the new file:
- **Imports utilities sibling files don't import** (sign of pattern drift — fetched from training data instead of mirrored).
- **Uses an error type / DI primitive / validation library siblings don't use** (e.g., raw `try/catch` when siblings use a `Result` envelope; raw `axios` when siblings use a typed client; `zod` when siblings use `class-validator`).
- **Sits at a path that doesn't match the existing module shape** (e.g., `src/foo/handlers/` when siblings live at `src/<module>/controllers/`).
- **Names exports / classes / files differently from siblings** (PascalCase vs camelCase drift, suffix drift like `*Service` vs `*Manager`).

Halt verdict for each new file uses the shared vocabulary in [`templates/snippets/sibling-shape-halt.md`](../../../../snippets/sibling-shape-halt.md): `aligned` (matches ≥2 siblings) | `drifted` (one or more axes diverge) | `no-siblings` (escalate to user — first feature in module, get shape blessed).

Any `drifted` → HALT before merge. Either re-shape to match siblings (default closure) or — if the deviation is intentional and load-bearing — write an ADR justifying it and promote the run (`risk-tier.py --write`). Drift without ADR is forbidden.

## New-dependency gate (all tiers)

The sibling-shape halt flags an unfamiliar import as *drift* — fetched from training data instead of mirrored. This gate covers the other case: a dependency the feature **genuinely needs** that no sibling already uses (first HTTP client, first PDF lib, first crypto package).

Adding it is not automatically wrong, but it is never silent. Before the package lands:

- **Confirm it's actually new** — not already in the lockfile under a sibling's import. Reuse the existing one if so.
- **Run a dependency review** (dispatch `security-auditor` on the dep): maintenance health (last release, open-CVE count), license compatibility, transitive bloat / install size, and whether a stdlib or already-present primitive does the job. Not installed → record the four facts with the command that produced each (`npm view <pkg> time.modified license`, `npm audit` / `osv-scanner`, the lockfile delta) — facts, not a verdict — and report `UNREVIEWED(dependency) — security-auditor not installed (security pack)`; the run is INCOMPLETE.
- **Record the decision** — one line in the PR (T1 / T2) or an ADR (T3, or any dep touching auth / crypto / payment / data-handling).

HALT on an unreviewed new dependency. A new package on a write-path / security surface with no ADR is forbidden.

## All-tier floors (risk-bearing diffs)

The **minimal** observability sign-off and the diff-scoped security pre-flight are a floor at every tier — triggered by the diff, not the tier label (the same way `n-plus-one-scan` is triggered by a new list endpoint).

**Trigger:** the diff adds an **endpoint**, an **external call**, or a **write path** (DB mutation, queue publish, state change). When none of these are present, the floor is a no-op.

When triggered, run regardless of tier:

- **Minimal observability sign-off** — the new endpoint emits a request counter + latency histogram; the external call emits success/failure + latency; sensitive data is redacted in logs. (The full Phase 6 sign-off — alert rules, correlation-id propagation, trace spans on hot paths — runs at T2/T3 in P11.)
- **Diff-scoped security pre-flight** — `/security-audit` scoped to the diff. Block on any BLOCKER. Not installed → `UNREVIEWED(security) — /security-audit not installed (security pack)` and the run is INCOMPLETE; the builder never grades its own diff. (The full security lens fan-out runs at P8; this floor is the diff-scoped minimum.)

HALT on a failure here at any tier. A write path is a T2 trigger anyway (`tiers.json`); the floor is what keeps a mis-tiered one honest.

## Standards gate (all tiers)

Run [`templates/snippets/standards-gate.md`](../../../../snippets/standards-gate.md) with the `backend-api` baseline, plus `data` whenever the feature touches an entity, migration, query or repository. Select the fired rows before Generate and carry them into the plan; close each with evidence before the Output block. The floor above and the Phase 6 reviewers' verdicts are evidence for the rows they cover — cite them, don't re-judge. Any `UNMET` or `SKIPPED` row → `INCOMPLETE`.

## Signals (Phase 1 step 3 — resolved before design)

3. Identify signals from ask/spec AND `CLAUDE.md`:
   - Multi-tenant? AI? Webhook? Payment? Real-time? Event-sourced? File-upload? Search? Notifications? Background job? Cross-service? Compliance?
   - **These signals are Phase 2's input, not Phase 3's.** They resolve to binding constraints *before* the architects are dispatched — see § Phase 2 Step 1. A signal read after the design is confirmed is a rework ticket, not a constraint.
4. Define scope boundaries: what's IN, what's explicitly OUT.

## Phase 2 — Organize: signal reads and binding constraints (run P4 — read by @architect)

**Constraints are read BEFORE the design, not after it.** These signal-driven reads once sat downstream of a confirmed design — so the architects proposed a schema and an API surface before anything told them what the domain forbids. A `schema-architect` that learns "no PAN column" *after* it proposed one was handed a rework ticket, not a constraint. `@architect` runs Step 1 → Step 2 before it writes `design.md`, and carries every Step-2 constraint into `design.md § Constraints`.

### Step 1 — Resolve every signal to its reads

Read the row for each signal Phase 1 resolved. Don't read everything — read what matters for THIS feature.

| Signal | Read these patterns |
|---|---|
| Multi-tenant | `multi-tenancy.md`, `tenant-isolation.md` |
| AI / LLM | `prompt-builder.md`, `ai-cost-tracking.md` |
| Webhook | `webhook-flow.md` (inbound signature-verify + replay + enqueue-then-ack; outbound signing + retry/DLQ) |
| Payment | `idempotency.md` (distributed-systems pattern) — plus the **rule** `templates/domains/payment/rules/payment-idempotency.md`, which is a rule, not a pattern, and loads from the payment domain overlay rather than `ai/patterns/` |
| Real-time | `ssr-safety.md`, websocket patterns |
| Event-sourced | `event-sourcing.md`, `cqrs.md` |
| Cross-service call | `saga.md`, `outbox.md`, `circuit-breaker.md`, `idempotency.md`, `api-versioning.md` |
| Heavy reads | `caching-strategy.md`, `indexing-strategy.md` |
| High scale | `sharding-partitioning.md` |
| Frontend | `rendering-strategy.md`, `i18n.md`, `forms.md` |
| User-facing UI | `design-systems.md`, `theming.md`, `rtl.md`, `motion.md` |
| New DB tables | `migrations.md`, `indexing-strategy.md` |
| Deployment change | `zero-downtime-deploys.md`, `cicd-pipeline.md` |
| Observability needs | `structured-logging.md`, `metrics.md`, `tracing.md` |
| Security surface | `zero-trust.md`, `auth-flow.md` |
| Testing strategy | `test-strategy.md`, `test-doubles.md` |

### Step 2 — Convert the design-shaping signals into binding constraints

Five signals do not merely add a pattern to the reading list — they decide the schema and the API surface, and getting them late means rebuilding both. For these, **state the constraint as a decision the design must already encode.** The run makes these calls at P4; it does not hand them to the user and it does not defer them to a P8–P11 reviewer.

**Payment.** First decide *which payment shape*, because the two shapes have opposite constraints and the wrong axis is the common failure:

- **Card-on-file / save-a-payment-method (no money moves).** Idempotency is not the axis here — PCI scope is.
  - **Never persist a PAN, CVV, or track data.** Any of the three moves the whole server from PCI SAQ-A to SAQ-D; `templates/domains/payment/lenses/payment-review.md:17` makes PAN-on-our-servers a BLOCKER with no exceptions, and its worked example prices the mistake as "full PCI audit, $50k+/year, quarterly scans, dedicated network segment" (`:131`). The card is tokenized by the provider's hosted field in the client; the server never sees it.
  - **Persist exactly the token envelope:** `{provider_customer_id, provider_pm_id, brand, last4, exp_month, exp_year}`. Anything beyond that set needs a written reason; a `card_number` / `cvv` / `expiry_raw` column is a HALT, not a review comment.
  - **If the card will ever be charged off-session, store the mandate / consent reference the provider returns at setup time.** Retrofitting it means re-collecting consent from every already-saved card, because the original setup that would have captured it is gone.
  - **Scope the provider customer object per tenant-user, not per user.** One platform-level customer holding cards across tenants is a cross-tenant leak with a payment provider on the other end of it.
  - **The detach event is inbound, not optional.** Cards expire, issuers revoke, customers remove them upstream; the provider emits a detach/removal event and the design carries a handler for it, or the local vault silently diverges from the provider's truth and a "saved card" 500s at charge time.
  - **Decide the default-card rule now.** "Exactly one default per customer" is an invariant, and two concurrent set-default calls satisfy it only under a partial unique index (`UNIQUE (customer_id) WHERE is_default`) or a single-statement swap — never under read-then-write.
- **Charge / capture / refund (money moves).** Idempotency key required, generated by us and persisted *before* the provider call so a retry after a timeout resolves to the same charge instead of a second one. Money is minor-units + currency, never a float.

**Multi-tenant.** The tenant is resolved once at the edge and read downstream; it is never accepted from body, params, query, or a bare request header (`ai/patterns/multi-tenancy.md`). The design states which layer applies the filter — the repository base class by construction, or Postgres RLS — and every new cache key is tenant-prefixed by construction, not by convention.

**Webhook (inbound).** The design decides the ack boundary before the handler exists: verify signature on the **raw** body, dedup on the provider's event id, enqueue, then ack. Any design that does real work before the ack has chosen a provider-timeout retry storm.

**Cross-service call.** Every new outbound call carries timeout + retry policy + circuit breaker + fallback as part of the design, not as Phase-6 findings. A retry without an idempotency key on the receiving side is a duplicate-write design, so decide which side owns the key here.

**Event-sourced / new DB tables.** The design names the aggregate root and its invariants before it names columns — which operations the domain admits is a design decision, and a table shaped for CRUD when the domain is append-only is wrong in a way no later review catches. (`/add-module` runs the same decision at module grain — see its § Aggregate-shape decision.)

For every other signal, the read IS the constraint — carry the pattern file forward and move on.

### Step 3 — Deep design slices (optional, with the constraints attached)

`@architect` owns `design.md`. When a slice needs a stack specialist and its pack is installed, it may dispatch these in parallel (read-only proposals it folds into `design.md`):

- `api-architect` — module shape, API surface, DTOs, service boundaries, DI wiring.
- `schema-architect` (if DB changes) — tables, columns, indexes, FKs, migration approach.
- `telemetry-architect` — logs + metrics + traces + alerts + SLOs for this feature.
- `system-architect` (if cross-service / distributed) — boundaries, consistency model, failure modes.
- `ui-architect` (if frontend) — page/component shape, state, services, i18n keys.
- `design-system-architect` (if new UI patterns) — tokens + primitives needed.

**Dispatch contract (architects don't re-derive, and are not left to guess).** This is the same payload discipline Phase 4 already applies to its leaves — an architect given only "design this feature" is exactly the leaf that re-derives. PASS DOWN to every architect:

- the **Phase-1 requirements** (or the Spec-ID + the acceptance criteria in its scope),
- the **resolved signals** from Phase 1 Step 3,
- the **pattern files** Step 1 selected for those signals,
- the **binding constraints** from Step 2, verbatim, marked as constraints rather than suggestions — `schema-architect` is told "no PAN column, provider token only" *before* it proposes a schema,
- the **sibling** whose shape the design must mirror (path), so the API surface is not invented.

**Mechanical gate on the returned design:** every Step-2 constraint appears in the design either satisfied or explicitly waived with a reason. A design that is silent on a live constraint is not confirmable — send it back. A design that *contradicts* one is a HALT, not a review comment.

If a named architect is not installed in this project, produce that design axis inline against its pack's checklist — never silently skip the axis.

Cross-reference outputs for contradictions. Resolve before proceeding.

## Phase 3 — Retrieve (run P6 — read before each task)

ALWAYS (the universal pre-flight): see [`templates/snippets/phase-3-always-reads.md`](../../../../snippets/phase-3-always-reads.md).

Plus:
- `.claude/rules/` — every file (auto-loaded, but re-scan for this task).
- `ai/architecture.md` — existing layers, data flow, trust boundaries.
- `ai/modules.md` — existing modules (mirror their shape).
- `ai/patterns/api-contract.md` — response shape + DTO evolution.
- `ai/patterns/error-handling.md` — typed errors + HTTP mapping.

SIGNAL-BASED: **already done — Phase 2 Step 1, before the design.** Do not re-read those pattern files here and do not re-resolve the signals; carry Phase 2's constraint set forward unchanged. If a signal was missed and only surfaces now, that is a design-invalidating find: return to Phase 2 Step 2 rather than patching it into the implementation.

EXISTING CODE:
- 1-2 sibling modules in the same layer — confirm the pattern is project-wide.
- The exact module(s) being extended (if any).

## Phase 4 — Generate (run P6 — @implementer, one plan.md task at a time)

### Scaffold

- New module? → `module-scaffold` skill.
- New endpoints on existing module? → `/add-endpoint` pattern per endpoint.
- DB changes? → `/add-migration`, then `schema-diff` skill to verify; if populated table touched, run `migration-rehearsal` skill.
- Frontend? → `/add-page` / `/add-component` / `/add-crud-page` per ui-architect's design.

**Dispatch contract (leaves don't re-derive).** When a task calls `/add-module` or `/add-endpoint` internally, PASS down — never make the leaf re-derive what this orchestration already resolved:
- the **run_id** and the **Spec-ID / spec path** when there is one (so the leaf reads the same contract, not a fresh interpretation),
- the **requirements** (`ai/runs/<run_id>/requirements.md` — the AC-IDs relevant to that leaf),
- the relevant **`design.md` slice** (the module-shape / API-surface / DTO / DI decisions for that leaf, not the whole design),
- the **resolved signals** (multi-tenant / AI / webhook / payment / cross-service) so the leaf applies the right domain requirements without re-detecting them.
A leaf that re-derives requirements or re-detects signals is a contract breach — the run already did that work once.

### Implement

Mirror sibling modules EXACTLY. Never invent a layout / name / export style.

Domain-specific implementation requirements:

**Multi-tenant**: every query filters by `tenant_id`. Every cache key tenant-prefixed. Events carry tenant in metadata (not payload).

**AI / LLM**: prompt builder uses documented 4-layer structure. `max_tokens` always set. Tokens + cost logged per call.

**Webhook**: raw body + HMAC verified BEFORE processing. Idempotency key stored. Return 200 within budget.

**Payment**: implement the Step-2 constraint set (`design.md § Constraints`) for the shape this feature actually is — card-on-file (provider token envelope only, no PAN column, mandate reference stored, provider customer scoped per tenant-user, detach handler wired, default-card race closed by a partial unique index) or money-moving (idempotency key generated and persisted before the provider call, minor-units money). Re-deciding the shape here means Phase 2 designed the wrong one.

**Cross-service**: timeout + retry policy + circuit breaker + fallback per call.

### Tests

The acceptance tests already exist and are locked (the orchestrator's P5, `lock-acceptance.sh`) — Generate makes them green;
it never edits them. Beyond them, the implementer writes internal unit tests outside the lock covering:
- Edge cases the locked criteria do not reach → unit tests.
- Edge cases → boundary tests.
- Multi-tenant? → cross-tenant leak test.
- AI? → prompt-eval fixture added.
- Webhook? → signature verification test + idempotency test.
- Cross-service? → `contract-test` if applicable.

**Build-time traceability.** `python3 .claude/scripts/trace-matrix.py <run_id> --phase=build` maps every REQ → AC → task → test and fails on any orphan — an unmapped AC-ID is an untested acceptance criterion and may not ship. Its matrix is the **AC-ID → test → file** map the Spec-conformance gate cites.

Verify:
- Unit tests exist for every use-case.
- Integration tests exist for every repo change.
- E2E test for the user flow.
- All tests pass locally.

Run skills:
- `endpoint-test-method` against dev server for each new endpoint.
- `coverage-gap` — are changed lines tested?
- `n-plus-one-scan` on new list endpoints (database pack, when installed).

## Phase 5 — Update (run P6b — doc-writer, or the orchestrator when the documentation pack is absent)

Update via `doc-writer`:
- `ai/modules.md` — new row if a module was added.
- `ai/status.md` — prepend Recent Changes entry (what / why / follow-ups).
- `ai/patterns/<new>.md` — if a new reusable pattern emerged.
- `ai/decisions/NNNN-*.md` — ADR if an architectural decision was made.
- `ai/dynamic/changelog.md` — one-line summary.
- When built from a spec: add a `Spec: <Spec-ID>` backreference to the `ai/status.md` Recent Changes entry and the `ai/dynamic/changelog.md` line (and include it in the PR description) so "which spec built this?" is answerable. **This backref is an every-tier invariant:** a T1 run skips the rest of this section but still emits `Spec: <Spec-ID>` in its output block and the PR.
- For UI changes: regenerate i18n keys in `locales/`.

## Phase 6 — Validate (run P7–P11 — which lenses, which checks)

### Review (one parallel fan-out of read-only lenses — P8–P11)

**Always dispatch**:
- `code-reviewer`
- `test-reviewer`
- `doc-drift-scan` skill — does the change need doc updates beyond status.md?

**Dispatch based on TOUCH** (what files changed):
| Touched | Agent |
|---|---|
| Backend code | `api-reviewer` |
| DB entities / migrations | `schema-reviewer` (+ `migration-review` command for migrations) |
| Frontend components | `ui-reviewer`, `design-system-guardian`, `accessibility-auditor`, `i18n-auditor` |
| Auth / crypto / secrets | `security-auditor`, `auth-reviewer` |
| Hot paths / queries | `performance-optimizer`, `query-optimizer` |
| Events / queues / cross-service | `resilience-reviewer` |
| Telemetry / logs / metrics | `observability-reviewer` |

**Dispatch based on DOMAIN SIGNALS** (what the project is):
| Signal | Agent |
|---|---|
| Multi-tenant | `tenant-isolation-reviewer` |
| AI | `security-auditor` + lens `ai-review` |
| Payment | `code-reviewer` + lens `payment-review` |

**Missing-agent contract (applies to every dispatch table in this skill):** if a named agent is not installed in this project, that axis is **not reviewed** — do not grade it yourself; the builder judging its own change is not a review. Record `UNREVIEWED(<axis>) — <agent> not installed (<pack> pack)` in the consolidation note and end the run **INCOMPLETE**, naming the install that closes it (`/setup-project --include=<pack>`). Never silently skip the axis, and never claim a reviewer that did not run.

Consolidate findings from the persisted `ai/runs/<run_id>/reviews/*.json`, never from the reviewers' prose. **Mechanical halt**: the verifier refutes every IMPORTANT candidate (refute mode); HALT while a confirmed IMPORTANT finding stands. Record `reviewers_dispatched=N` and `reviewers_clean=N` — proceed only when they are equal. After a fix, re-run that specific lens; do not paper over, do not aggregate-and-ignore.

### Spec-conformance gate (spec path only)

**Spec depth in → enforced out.** When the run was built from a spec, iterate the spec's depth sections and emit a per-section **verdict**. This is the gate that makes the ingested spec binding rather than decorative — a spec is only worth its depth if every section it declared is checked against the shipped code. **HALT on any unmet section.**

| Spec section | Conformance check (per item) | Verdict |
|---|---|---|
| Acceptance criteria | every AC-ID maps to a named new test in a named file (`trace-matrix.py --phase=build`) | `met` / **HALT** |
| NFR / SLO | each one is implemented AND the note states **how it is measured** (which metric / load test / budget) | `met` / **HALT** |
| Authorization rules | each rule has a test asserting **denial** for the unauthorized role(s), not just allow-path coverage | `met` / **HALT** |
| PII / declared sensitive fields | each declared PII field has a **redaction check** (log-redaction test or assertion it never serializes) | `met` / **HALT** |
| Observability requirements | each required signal (log / metric / trace / alert) is **matched to an actually-emitted signal** in the diff | `met` / **HALT** |
| Rollout / migration | the Release pre-flight note is **populated FROM the spec's rollout section**, not re-derived (flag / migration ordering / rollback / staging come from the spec) | `met` / **HALT** |
| Success metric | the success metric is **instrumented** (an emitted signal proves it) OR **explicitly deferred** with a one-line reason in the PR | `met` / `deferred` / **HALT** |

Emit this table — plus the `trace-matrix.py` map — in the run's output. Any row that is neither `met` nor (for Success metric) explicitly `deferred` → HALT; do not paper over a missing section, and do not silently downgrade the spec's depth.

### Observability sign-off

Verify:
- Every new endpoint emits request counter + latency histogram.
- Every external call emits success/failure + latency.
- New errors have alert rules (or explicit "no alert needed" note).
- Correlation id propagates through.
- Trace spans on hot paths.
- Sensitive data redacted in logs.

If gaps: dispatch `/add-telemetry` before ship *(observability pack, when co-installed)*. **A redirect must land somewhere** — when that pack is absent, emit the missing signals inline against the project's existing telemetry primitives (`references/<framework>.md`) before ship and record it in the report; never route a gap into a command the project does not have.

### Domain-specific verifications (signal-driven)

Run based on signals:
- AI → `/prompt-eval` + `/token-audit`
- Webhook → `/simulate-webhook` with a new fixture
- Multi-tenant → `/tenant-leak-audit` focused on changed files
- Public API surface → `api-snapshot` diff (breaking change detection)
- Cross-service → `chaos-test` planned for staging (ticket, not inline)
- Frontend → `visual-check` + `a11y-scan` for affected routes

### Security pre-flight

Dispatch `/security-audit` scoped to the diff. Block on any BLOCKER.

### Release pre-flight (T3 → `ai/runs/<run_id>/release.md`; T2 → one PR note)

At T3 this is `release.md` in the run (≤80 lines); at T2 one short note in the PR description — not a new ceremony. **When built from a spec, populate this FROM the spec's Rollout/migration section — do not re-derive it.** Each field below is copied from the spec and confirmed against the diff; a field the spec specified but the code contradicts is a Spec-conformance-gate HALT (and a `Deviation:` annotation):

- **Flag decision**: behind a feature flag, or flagless with rationale (e.g., additive endpoint, no existing-path risk).
- **Migration ordering**: if schema changed, expand → migrate → contract sequence stated; deploy is safe with old + new code running simultaneously.
- **Rollback path**: one sentence — flag off / revert commit / down-migration. "Cannot roll back" requires an ADR.
- **Staging verification**: what gets checked on staging before production (the `chaos-test` ticket for cross-service features lands here).

If any check fails: HALT, report the failure, do not paper over.

## Phase 7 — Improve (run P15 — feed the learning loop)

- Run `/learn-from-task` to capture: decisions, patterns followed/introduced, corrections, follow-ups.
- If a new shape emerged in 3+ places across this feature: queue to `ai/dynamic/learned-patterns.md`.
- If a user correction during architecture review reset the design direction: append to `ai/dynamic/feedback-learned.md`.
- If a decision warrants formal ADR: queue to `ai/dynamic/decisions-pending.md`.
- If review surfaced drift between code + convention: append to `ai/dynamic/drift-log.md`.
- **Spec-drift learning (spec path).** If implementation diverged from the spec contract — a section was wrong or incomplete, or an Open question got resolved during the build — close the loop in TWO places (do not invent a new file):
  - **Annotate the source spec** in place: a `Deviation: <section> — <what the code does instead + why>` note where a section proved wrong/incomplete, or a `Resolved: <open question> — <answer chosen during build>` note where an Open question was answered.
  - **Queue the delta to `ai/dynamic/feedback-learned.md`** so the divergence feeds the learning layer.
  - **Surface it in the PR** (a "Spec deviations / resolutions" line) so the reviewer sees the spec is no longer the literal blueprint.

## Hard rules (lane)

- The standards gate runs at every tier. Tier shrinks ceremony, never the baseline.
- No feature ships without tests for every acceptance criterion. On the spec path this is mechanical: every AC-ID maps to a named test in a named file (Phase 4 traceability rebuild) or it HALTs.
- No feature ships without telemetry. The minimal observability sign-off is an all-tier floor on any diff that adds an endpoint / external call / write path — at every tier.
- No feature ships with any security BLOCKER open. The diff-scoped security pre-flight is an all-tier floor on the same risk-bearing diffs.
- Spec depth in → enforced out: when built from a spec, every depth section passes the Phase 6 Spec-conformance gate or it HALTs; unresolved spec Open questions HALT before Generate.
- The `Spec: <Spec-ID>` backreference is emitted at every tier when built from a spec, even when Phase 5 is skipped.
- Domain signals drive automatic reviewer dispatch — don't forget them.
- Every consulted pattern logged in the report for traceability.

## Related

### Sibling commands — where the boundary falls
- `/add-module` · `/add-endpoint` — the leaves a task may call. The run owns the spec, the cross-module sequencing and the capability decision; they own the file grain. Anything they re-derive, the run already resolved (§ Dispatch contract).
- `/analyze-module` — run it first on any module this feature will extend that nobody has touched in a month; it is the read-only pre-flight that says whether extending is safe.
- `/fix-bug` — a feature that "doesn't work" is a defect in shipped code, not an increment. Feature work that starts as a bug report is misrouted.

### Patterns
- `ai/patterns/api-contract.md` — the contract every endpoint in the feature converges on.
- `ai/patterns/error-handling.md` — one error shape across the whole feature, not one per module.
- Signal-gated per module touched: `multi-tenancy.md`, `transaction-boundary.md` (a write spanning two aggregates), `webhook-flow.md`, `async-job-offload.md`.

Patterns are read per touched module, not up-front as a set. A pattern read on a module this feature never opens produced no finding.

### Rules
- `.claude/rules/backend-principles.md`
- `.claude/rules/concurrency-discipline.md`
