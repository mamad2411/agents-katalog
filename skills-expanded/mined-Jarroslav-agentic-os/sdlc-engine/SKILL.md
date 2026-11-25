---
name: sdlc-engine
description: Heavy orchestrator that runs the full 13-stage (Phase 0-12) governed SDLC flow for a single unit of work. Invoke this skill only as the execution engine dispatched by sdlc-guided (mode=hitl) or sdlc-auto (mode=autonomous) — never in direct response to a bare user request, and never with a mode other than hitl or autonomous. Trigger phrases that mean "call sdlc-engine" arrive pre-translated through those two entry skills: "start sdlc", "implement this with sdlc", "run autonomously", "factory mode", "ship this without asking", a resumed run handed back from sdlc-runs. Owns run bootstrap, branch safety, complexity routing, spec/plan approval, TDD implementation with evidence capture, deferred bounded code review, QA gates, feature verification, and handoff. mode is the only branching input between the two calling styles: phase sequence, artifact shapes, file paths, and gate ids are identical either way — only the gate-arbiter behavior at each judgment gate differs. Not for: direct user invocation (sdlc-guided and sdlc-auto are the only entry points) or lightweight flows (sdlc-brief, sdlc-direct).
discoverable: false

---

# sdlc-engine

## Availability and contract authority

The bundled runtime supports contract validation, policy resolution, durable lifecycle
persistence, bounded dispatch, decisions, evidence, reconciliation, and regenerable exports.
Managed lifecycle operations must be available before running this workflow. An unavailable
operation blocks the requested managed action with an explicit limitation.
Do not emulate initialization, dispatch, gate resolution, resume, or transitions by writing
JSON/JSONL files, and do not report a managed run as started or completed.

`runtime/agentic_runtime/registry.json` is the sole source for identifiers, transitions, and
defaults; the plugin-local runtime is the identical bundled source. Consult generated
`references/runtime-contracts.md` for its readable projection.

Resolve policy before any workflow mutation with `${CLAUDE_PLUGIN_ROOT}/runtime/run.py`.
The caller supplies `hitl` or `autonomous` as an explicit override; for example:

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"sdlc-engine","overrides":{"mode":"hitl"}}
```

Policy resolution does not create a run or authorize unavailable lifecycle operations.

## Purpose

You are the single orchestrator behind every governed SDLC run in this plugin. `sdlc-guided` and
`sdlc-auto` are thin wrappers: each normalizes its caller's intent into a `task_input` and a
`mode`, then dispatches you. From that point forward you own the run end to end — bootstrapping the
run directory, routing through complexity, driving spec/plan approval, supervising TDD
implementation, running the deferred bounded code review, executing QA gates and feature
verification, and handing off. `sdlc-runs` retains resume and repair authority over runs you
produce; you must leave behind evidence it can act on, but you do not implement resume/repair
yourself beyond honoring the run state you are handed.

> Ground every phase in what the run's own artifacts and the host repo's guides actually say. Never
> invent a fact — about the codebase, the ticket, test output, or review findings — that isn't
> backed by an artifact, a tool result, or a dispatched subagent's return. When information is
> missing, say so and route to a gate or a clarifying question; do not fill the gap from assumption.

## When to invoke — and when not to

- Invoke when `sdlc-guided` or `sdlc-auto` dispatch you with a `mode` and a `task_input`. That
  is the only legitimate entry point.
- Invoke when `sdlc-runs` hands back a `run_id` for a run that was interrupted mid-phase and the
  user or the calling skill wants it driven to completion.
- Do not invoke yourself in response to a raw user message — route through `sdlc-guided` (hitl) or
  `sdlc-auto` (autonomous) first, so `mode` is always explicit before you start.
- Do not re-implement logic owned by the `superpowers` skills you dispatch into (brainstorming,
  writing-plans, test-driven-development, subagent-driven-development) — call them, don't inline
  their behavior.

## Where this pipeline stops and the project's own begins

Some repositories already run their own delivery pipelines. When `.agentic/agentic-sdlc/config.json` defines
`project_orchestration`, load it before Phase 0 and treat those pipelines as the
only thing permitted to select or invoke the project's fleet roles.

This pipeline keeps intake, analysis, planning, QA, documentation, status and
delivery handoff. For implementation it invokes exactly **one** selected project
pipeline and retains only that pipeline's summary and serialized gate results —
not its internal reasoning, not its worker output. Use the configured neutral
state file rather than opening a second one, and never spawn project workers
directly. Two orchestrators writing the same run is the failure this boundary
exists to prevent.

## Inputs

| Field | Source | Notes |
|---|---|---|
| `mode` | caller | `hitl` or `autonomous` — the only branching input |
| `task_input` | caller | raw text, external work-item reference, spec path, or greenfield idea |
| `run_id` (resume only) | `sdlc-runs` | when resuming, the caller supplies an existing run_id instead of you minting one |

## Intended lifecycle and storage (requires lifecycle operations)

Before any run-artifact write, establish branch/worktree ownership and inspect the working tree
and upstream. Do not reset, commit, or discard unrelated changes. Autonomous dirty-tree work
requires explicit project policy or must stop. Each mutating worker uses an isolated worktree
and owns a specific file set; serialize dependent work. SQLite is not a checkout sandbox.

The runtime database `.agentic/state/runtime.sqlite3` is the authority for lifecycle state.
Run artifacts at `.agentic/runs/<run-id>/` are regenerable exports, including metadata, events,
decisions, review reports, and evidence. Human-authored specs, plans, and work-item documents
remain under `docs/superpowers/`. Never replace those documents with database-only content.
Legacy `meta.json`, `events.jsonl`, and `decisions.jsonl` files are compatibility views generated
with `legacy.export`; editing them never changes runtime state.
Never adopt sibling-run artifacts without explicit provenance and supported reconciliation.

Run states are `pending`, `running`, `waiting_for_user`, `interrupted`,
`reconciliation_required`, `completed`, `failed`, and `cancelled`. The registry defines legal
transitions. Resume and reconciliation must use runtime operations and durable database state,
not an export's phase counter, JSONL replay, or manual metadata edits. Missing runtime operations
block; export validation alone does not implement them. A failure to persist an authoritative
decision blocks progression; export regeneration failures do not erase a committed decision.

All phase steps below require supported lifecycle operations. Optional external-adapter failure
may degrade only when authoritative local runtime persistence is available; it never licenses
a JSON fallback for missing runtime operations. Only the coordinator resolves gates and dispatches.
Review and resolver workers are advisory. Registry worker defaults are story 3, bug 2,
hotfix/spike/epic 1; epic children run sequentially.

### Resume and assignment recovery

When dispatched with an existing `run_id`, first call `run.status` and confirm the run is
`running` under the current coordinator lease. Inspect `.agentic/runs/<run-id>/run.json` only
after regenerating it with `run.export`; it projects assignments, messages, events, evidence,
and dispatch reservations. Continue existing assignment IDs with their recorded owners. Do not
replace an unavailable owner or infer a completed assignment from prose or a changed checkpoint.
User-owned fixture and checkpoint files are immutable inputs; preserve them byte for byte and
keep progress in managed runtime state.

For each actual worker dispatch, reserve it with `task.dispatch`, refresh the run revision, then
start its worker lease with `dispatch.start` before launching the worker. This binds the recorded
worker and applies the concurrency, active-run, and dispatch-deadline limits. Refresh the revision
again after start and finish the dispatch with `task.result`; if it times out, reconcile it with
`dispatch.recover` before considering another attempt. A worker's completion report alone does not
complete its assignment. Transition the corresponding assignment through `assignment.transition`
with its current assignment revision, run revision, lease epoch, coordinator ID, and recorded
worker ID. Validate the owned-path diff and acceptance evidence before transitioning to
`completed`. If work cannot be tied to its existing assignment, its owner is unavailable, or
runtime state cannot be updated, stop that branch of work and escalate. Never rewrite exported JSON
or create a replacement assignment to make the run appear complete.

Before handoff or a completion claim, refresh authoritative state and the run export. Any
assignment still pending, running, waiting, or escalation-required prevents a claim that all
delegated work completed. The runtime implements `run.complete`, but the shipped host adapter
does not yet provide an integrated path to produce its trusted host-signed gate and evidence
claims. Leave the run active and report that host integration limitation until that path is
certified.

If `sdlc-runs` passes a response to a gate that was waiting for the user, do not treat the resume
request itself as approval. Verify the gate ID and current artifact hash, submit the supplied
response through `gate-arbiter`, and persist that exact decision with `decision.record` under the
current coordinator lease before advancing. If the decision is missing, stale, or does not match
the artifact, stop and ask the user again.

## Phase map

| # | Phase | Skippable | Gate(s) |
|---|---|---|---|
| 0 | Doctor + memory load | no | — |
| 1 | Requirements | no | `requirements.ambiguous`, `classification.confirm` |
| 2 | Feature branch | no | (branch_guard decision, not a judgment gate) |
| 3 | Complexity scoring | no | — |
| 4 | Spec (conditional on routing = brainstorming) | yes | `spec.clarification`, `spec.approved` |
| 5 | Plan | no | `plan.approved` |
| 6 | QA Checklist | per `phase_set` | `qa-checklist.approved` |
| 7 | Implementation | no | — |
| 8 | QA Test Review | per `phase_set` | `qa-tests.approved` |
| 9 | Final code review (bounded retries) | never once Phase 7 is reached | `code-review.check`, `code-review.final` |
| 10 | QA gates + feature verification | never once Phase 7 is reached | `qa.drift`, `feature.verification` |
| 11 | QA Health Update | per `phase_set` | — |
| 12 | Handoff | no | — |

`phase_set` is computed from the work-type classification and the Phase 3 routing decision (see
`${CLAUDE_PLUGIN_ROOT}/references/phase-routing.md` for the full derivation table). Phases outside
`phase_set` are recorded as skipped through runtime operations and projected into metadata and stay skipped for the
life of the run — you never reconsider a skip decision later. Phase 4 is the clearest case: it runs
when Phase 3 resolves `routing = brainstorming`, or unconditionally for a spike; the `writing-plans` fast path skips straight
from Phase 3 to Phase 5. Phases 9 and 10 are the hard floor — once Phase 7 begins, both always run,
regardless of `phase_set`.

## Operating steps

### Phase 0 — Doctor + memory load

1. Resolve run identity through supported runtime operations only after establishing branch/worktree ownership and checking the working tree. Unavailable operations block. Do not create a managed run directory with the current bundle.
2. Read `.agentic/agentic-sdlc/doctor.json` and `.agentic/agentic-sdlc/config.json`. If doctor state
   looks stale, this is a signal to suggest `sdlc-preflight`, not a reason to block — proceed on the
   config you have.
3. Dispatch `role-memory` exactly once to load the sdlc role's `memory_brief` from
   `.agents/memory/sdlc/MEMORY.md` and the relevant `.agents/memory/sdlc/daily/<date>.md` entries.
   Do not re-read `memory_brief` mid-run under any circumstance — Phase 0 is its only load point.
   `config.memory.auto_write_on` governs whether later phases are allowed to write new memory, not
   whether you may re-read it.
4. When lifecycle persistence exists, initialize authoritative state through runtime operations;
   metadata and events are regenerable exports, not directly written authoritative state.
5. Record Phase 0 start/completion through those operations only after required checks pass.

### Phase 1 — Requirements

1. Dispatch `story-intake` with `task_input`, `mode`, and the memory brief for context. It
   normalizes free-form text, an external work-item reference, a spec path, or a greenfield idea
   into a single `requirements.md` under `docs/superpowers/specs/`.
2. If `story-intake` cannot resolve ambiguity within the requirements it was given, route
   `requirements.ambiguous` through `gate-arbiter`. Respect
   `config.mode_defaults.<mode>.max_clarifying_questions_per_phase` (default 3) as a budget on
   clarifying questions — exhausting the budget does not auto-approve anything downstream, it only
   stops you from asking a fourth question before escalating.
3. Determine the work-type classification (`story | bug | hotfix | spike | epic`) from the
   normalized requirements and route it through the `classification.confirm` gate. If the
   classification is `epic`, dispatch `story-proxy` to decompose it into child stories before
   continuing — do not carry an undecomposed epic into branch/complexity phases.
4. Call the lifecycle adapter with intent `prepare_for_development` (fields: `schema`, `intent`,
   `mode`, `run_id`, `phase`, `local_work_item_path`, `run_work_item_path`, `artifacts`, `policy`).
   Emit `work_item.created` and `work_item.assigned` as the adapter confirms. Adapter absence or
   failure never blocks the run — degrade to local-only history plus a `work_item.adapter_warning`
   event and keep going.

### Phase 2 — Feature branch

1. Read `.agentic/guides/standards/git-workflow.md` for branch naming convention.
2. Inspect the working tree and upstream state, and populate `branch_guard`: `current_branch`,
   `base_branch`, `target_branch`, `working_tree` (`clean|dirty`), `upstream`
   (`none|ahead|behind|diverged|in-sync`), `target_branch_exists`, `base_refreshed`, `decision`.
3. **HITL dirty-tree handling** — offer exactly these options through `gate-arbiter`: `stash`,
   `commit first`, `hard reset` (only with explicit confirmation naming the branch by name),
   `proceed with the existing dirty state` (only with a recorded warning event), `abort`. Set
   `branch_guard.decision` to the matching value (`stash`, `commit-first`, `hard-reset`,
   `proceed-dirty`, `abort`).
4. **Autonomous dirty-tree handling** — halt on any dirty tree (`branch_guard.decision = "halted"`)
   unless project policy explicitly permits auto-stash. Never hard-reset, never commit the user's
   changes, never proceed dirty without policy backing, in autonomous mode.
5. Confirm the owned feature branch/worktree established before run-artifact writes. Give every mutating worker an isolated worktree; SQLite does not sandbox checkout changes.

### Phase 3 — Complexity scoring

Apply the heuristic fast paths before ever dispatching an agent:

| Condition | Score | Routing |
|---|---|---|
| Single-file scope, no risk keyword, goal under 25 words | 8 | `writing-plans` |
| Any risk keyword present, OR `affected_file_estimate >= 7`, OR a multi-system-integration goal | 24 | `brainstorming` |
| Anything else | — | dispatch `effort-sizing` → `sizing-analyst` agent |

- Score bands: 6–14 → `writing-plans`; 15–36 → `brainstorming`. A score `>= 25` additionally forces
  the `premium` model tier at every subsequent dispatch in this run (see Model tier resolution).
- A `sizing-analyst` result of `"split-required"` halts the run — do not attempt to force a score.
- Write `complexity.json` (validate against `complexity.schema.json`), finalize `phase_set` per
  `${CLAUDE_PLUGIN_ROOT}/references/phase-routing.md`, and record both through supported runtime operations; metadata is an export.

### Phase 4 — Spec (conditional)

Runs when Phase 3 routing resolved to `brainstorming`, or unconditionally for a spike.

1. Dispatch `superpowers:brainstorming` to shape `design.md`, grounded in `requirements.md` and any
   `codebase-scout` findings gathered so far.
2. If open questions remain, route `spec.clarification` through `gate-arbiter`, bounded by the
   same `max_clarifying_questions_per_phase` budget as Phase 1.
3. Route `spec.approved` through `gate-arbiter`. A revision request increments loop
   `spec.revision` (cap 3, halt on exceed) — every managed retry counts, including user-requested reruns. Direct document edits alone are not an attempt.
4. `max_clarifying_questions_per_phase` never auto-approves `spec.approved` — exhausting the
   question budget forces an explicit gate call, not a default yes.

### Phase 5 — Plan

1. Dispatch `superpowers:writing-plans` — from `design.md` when Phase 4 ran, or directly from
   `requirements.md` on the fast path — to produce `plan.md`. Every implementation task line must
   carry an explicit `Test-first: yes` or `Test-first: no` annotation; this drives Phase 7 evidence
   validation.
2. Route `plan.approved` through `gate-arbiter`. A revision request increments loop
   `plan.revision` (cap 3, halt on exceed), including user-requested retries.

### Phase 6 — QA Checklist

1. Dispatch `qa-scoping --checklist`, grounded in `requirements.md` and
   `.agentic/guides/testing/qa-strategy.md`, to produce `qa-checklist.md`. It returns
   `checklist_path`.
2. Route `qa-checklist.approved` through `gate-arbiter` when Phase 6 is in `phase_set`.

### Phase 7 — Implementation

1. Dispatch `superpowers:subagent-driven-development` over `plan.md`'s task list, with
   `superpowers:test-driven-development` governing each task's red-green discipline.
2. For every task marked `Test-first: yes`, capture `evidence/<task-id>.json` with: `schema`,
   `task_id`, `test_first` (`true`), `failing_test_command`, `failure_excerpt` (must match
   `/FAIL|Error|Assert|expected|exit code/i`), `implementation_summary`, `passing_command`,
   `passing_excerpt` (must match `/PASS|ok|passed/i`), `files_touched`, `diff_lines_added`,
   `diff_lines_removed`. Validate each file against `evidence.schema.json` right after writing it,
   and again right before it is summarized into any gate call.
3. A failed evidence check retries under loop `evidence.retry:<task-id>` (cap 2, escalate on
   exceed) — one counter per task, not a run-wide counter.
4. Resolve the model tier for each dispatch per Model tier resolution below, using
   `${CLAUDE_PLUGIN_ROOT}/references/model-routing.md`.

### Phase 8 — QA Test Review

1. Dispatch `qa-scoping --review-tests` to review the tests written in Phase 7 for quality and
   completeness, producing `qa-test-review.md`.
2. A failed review retries under loop `qa-test-review.retry` (cap 1, escalate on exceed).

### Phase 9 — Final code review (bounded retries)

1. Build `review-bundle.json`: `schema`, `diff_base`, `changed_files`, `diffstat`
   (`files`, `added`, `removed`), `risk_flags`, `evidence_summaries`, `artifact_refs`. Validate
   against `review-bundle.schema.json`.
2. Dispatch `code-review-orchestrator`, passing `qa-checklist.md` as a bounded `ArtifactRef` (never
   the full checklist body). The orchestrator applies its own methodology from
   `code-review-orchestrator/references/review-lenses.md` — you do not duplicate review-lens logic
   here.
3. Initial review uses `code-review.final`. Reports are advisory; the coordinator resolves the gate.
4. Findings trigger fix-up attempts under `code-review.fixup`, whose registry cap counts retries
   after the initial attempt. Each `code-review.check` reviews original findings and the fix-up diff.
   Widen review only when new high-risk flags appear or the user explicitly requests it.
5. Accept a successful final permitted retry. A failed exhausted budget halts before another attempt.

- Deterministic artifact shape/schema failures (a malformed `review-bundle.json`, a missing field)
  are fixed with direct, deterministic instructions — never dispatch a model reviewer to fix a
  schema violation.

### Phase 10 — QA gates + feature verification

1. Dispatch `gate-runner`. It returns `{passed, blocked_gate, drift_detected, gate_plan}` after
   running lint → build → unit/affected tests → optional configured UI tests in sequence.
2. If `drift_detected`, route `qa.drift` through `gate-arbiter` before proceeding.
3. **On failure (autonomous mode)** — triage into `test_issue`, `flaky`, `environment_issue`, or
   `application_issue`:
   - `test_issue` / `flaky` / `environment_issue` → dispatch `test-heal`. Its loop decision is one
     of `needs_rerun`, `converged`, `capped`.
   - `application_issue` (or anything `test-heal` hands back unresolved) → dispatch a fix-up
     implementation task.
   - Both paths count against loop `gate-runner.retry` (cap 2, escalate on exceed).
4. Dispatch `acceptance-check` per the matrix below:

| `required` | `verified` | `blocking` | Outcome |
|---|---|---|---|
| `false` | — | — | skip the gate; emit deterministic `qa.ready` |
| `true` | `true` | `false` | emit `feature.verified`, then `qa.ready` |
| `true` | — | `true` | route `feature.verification` gate — HITL: user decides; autonomous: `lead-proxy` verdict drives fix-up loop `acceptance-check.retry` (cap 2, escalate on exceed) |

`acceptance-check` returns `{required, verified, tool, results, blocking}` and writes
`verification-evidence.json` plus per-feature `evidence/verification/<feature-id>.json`, both
validated against `verification-evidence.schema.json`.

Call the lifecycle adapter with intent `record_delivery_audit` once Phase 10 reaches a passing
state, carrying the review and QA artifact refs for the audit trail. As with every adapter call, a
missing or failing adapter degrades to a local-only record plus `work_item.adapter_warning` — it
never blocks the gate.

### Phase 11 — QA Health Update

Dispatch `qa-scoping --update` to refresh `.agentic/guides/testing/qa-health.md` once Phase 10
passes, when Phase 11 is in `phase_set`.

### Phase 12 — Handoff

1. Call the lifecycle adapter with intent `complete_or_handoff`. Emit `qa.passed` and
   `work_item.transitioned`.
2. Reconcile the two work-item mirrors — the canonical Markdown store at
   `docs/superpowers/work-items/work-item-events.jsonl` and the run-local mirror at
   `<run_dir>/work-item.md` — by priority order: `the runtime database is authoritative for lifecycle state when they disagree. Emit `work_item.reconciled` once resolved.
3. Hand off to `mr-submit` for commit, push, and MR/PR creation. If the caller wants hands-off
   monitoring after that, chain into `mr-watch` — it is a separate skill you dispatch, not logic you
   inline here.
4. Beyond this point, resume/repair authority belongs to `sdlc-runs`. Leave durable runtime state and regenerable exports that supported resume operations can inspect.

## Judgment gates and gate-arbiter

Every judgment gate call goes through `gate-arbiter`, passing bounded `ArtifactRefs` (never
inlined full documents): `kind` (`"spec"|"plan"|"diff"|"qa-report"|"evidence"`), `path`, `summary`,
`signature`, `sections` — capped at 2 KB per artifact and 6 KB per gate call in total.

- **hitl**: every judgment gate prompts the user directly. Never use an autonomous fast-path,
  a deterministic default, or a subagent stand-in verdict to approve a gate in this mode.
- **autonomous**: deterministic checks, then mandatory escalation checks, precede eligible fast-path approvals; only fall back to a
  stand-in subagent verdict (e.g. `lead-proxy` for `feature.verification`, `story-proxy` for epic
  decomposition) when no deterministic path resolves the gate.

Gate ids in this run, verbatim: `requirements.ambiguous`, `spec.clarification`, `spec.approved`,
`plan.approved`, `code-review.final`, `code-review.check`, `qa.drift`, `feature.verification`,
`classification.confirm`, `qa-checklist.approved`, `qa-tests.approved`.

The coordinator commits every gate decision through supported runtime operations after mandatory
escalation checks. Resolver/reviewer reports are advisory. Authoritative persistence failure blocks;
export write failure may be repaired after a successful commit.

## Retry accounting

Read loop IDs, `max_retries`, and `on_cap` from the registry; `references/gate-catalog.md`
explains their use. A cap counts retries **after the initial attempt**. Evaluate success before
exhaustion: exhausted budgets prevent another attempt but never invalidate success. All
managed retries count, including user-requested reruns. Resume does not reset counters. Extra
attempts require an explicit recorded budget increase before dispatch.

`spec.revision`, `plan.revision`, `evidence.retry:<task-id>`, `qa-test-review.retry`,
`code-review.fixup`, `gate-runner.retry`, `acceptance-check.retry`, and
`arbiter.malformed.retry` are stable IDs. Evidence retries are per task. On failed exhaustion,
the coordinator records the prescribed interruption or escalation through supported runtime
operations. It does not increment export JSON or invent additional attempts.

## Model tier resolution

Resolve a tier (`economy | standard | premium`) at every agent dispatch — never name a concrete
model. `premium` triggers when either a risk flag in `meta.json.escalate_on` is set, or
`complexity.json.score >= 25`. `config.model_tiers.<tier>` defaults to `"inherit"` unless the host
project overrides it. Consult `${CLAUDE_PLUGIN_ROOT}/references/model-routing.md` for the full
resolution order, and `${CLAUDE_PLUGIN_ROOT}/references/tokenomics.md` when weighing a fast-path
skip against a full agent dispatch.

## Lifecycle adapter calls

Three intents only, verbatim: `prepare_for_development`, `record_delivery_audit`,
`complete_or_handoff`. Every call carries the standard input fields: `schema`, `intent`, `mode`,
`run_id`, `phase`, `local_work_item_path`, `run_work_item_path`, `artifacts`, `policy`. Adapters are
resolved per `${CLAUDE_PLUGIN_ROOT}/references/work-item-adapters.md` — no ticket or MR backend is
hardcoded here. Adapter absence or failure degrades to local-only history plus a
`work_item.adapter_warning` event; it never blocks or halts the run.

## Resume and idempotency

Resume/reconciliation require supported runtime operations and database state. Never replay JSONL
or edit metadata to simulate them. Preserve human documents and verified evidence; use operation
idempotency rather than blindly overwriting artifacts. Unavailable operations block with the current bundle.

## Run-state artifacts and schema validation

| Artifact | Schema |
|---|---|
| `meta.json` (incl. `loops`, `branch_guard`) | `meta.schema.json` |
| `events.jsonl` (per line) | `event-line.schema.json` |
| `decisions.jsonl` (per line) | `decision-line.schema.json` |
| `evidence/<task-id>.json` | `evidence.schema.json` |
| `review-bundle.json` | `review-bundle.schema.json` |
| `complexity.json` | `complexity.schema.json` |
| `verification-evidence.json`, `evidence/verification/<feature-id>.json` | `verification-evidence.schema.json` |

Validate every structured artifact twice: immediately after writing it, and again immediately before
handing its `ArtifactRef` to a gate. Run validation as:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate-run-artifact.py <schema> <artifact>
```

`events.jsonl` lines carry `schema`, `ts`, `event`, `run_id`, `phase`, `actor`, `summary`,
`artifacts`, `data`. Semantic/lifecycle event names used across this run, verbatim: `phase.started`,
`phase.completed`, `phase.failed`, `phase.interrupted`, `artifact.written`, `decision.recorded`,
`loop.capped`, `work_item.created`, `work_item.assigned`, `work_item.transitioned`,
`work_item.linked_artifact`, `work_item.adapter_receipt`, `work_item.adapter_warning`,
`work_item.reconciled`, `status.repaired`, `spec.approved`, `plan.approved`, `qa.ready`,
`feature.verified`, `qa.passed`.

## How this skill uses its references/ tree

- `${CLAUDE_PLUGIN_ROOT}/references/gate-catalog.md` — explanatory loop accounting; registry values are authoritative;
  consult it whenever incrementing or checking a loop counter.
- `${CLAUDE_PLUGIN_ROOT}/references/tokenomics.md` — token-cost guidance for fast-path-vs-dispatch
  decisions at Phase 3 and every subsequent agent dispatch.
- `${CLAUDE_PLUGIN_ROOT}/references/schemas/` — `meta.schema.json`, `event-line.schema.json`,
  `decision-line.schema.json`, `evidence.schema.json`, `review-bundle.schema.json`,
  `complexity.schema.json`, `verification-evidence.schema.json`; the inputs to
  `scripts/validate-run-artifact.py`.
- `${CLAUDE_PLUGIN_ROOT}/references/work-item-adapters.md` — the three-intent adapter contract and
  per-provider mapping, consulted at every `prepare_for_development` / `record_delivery_audit` /
  `complete_or_handoff` call.
- `${CLAUDE_PLUGIN_ROOT}/references/phase-routing.md` — the classification → `phase_set` derivation
  table, consulted at Phase 1's `classification.confirm` and finalized at Phase 3.
- `${CLAUDE_PLUGIN_ROOT}/references/model-routing.md` — tier resolution order for every dispatch.
- `${CLAUDE_PLUGIN_ROOT}/references/lifecycle-artifacts.md` — canonical shapes and paths for every
  run-state artifact listed above, consulted whenever writing or reconciling a work-item mirror.

## Intended outputs (after lifecycle implementation)

- Populated run directory `.agentic/runs/<run-id>/` with every artifact listed above.
- Updated human work-item documents and regenerable ledger exports; database owns lifecycle state.
- Updated `.agentic/guides/testing/qa-health.md` (Phase 11, when in `phase_set`).
- A feature branch in the current checkout, carrying the implementation, ready for `mr-submit`.
- Intended durable database state for supported resume/repair operations; trusted run completion remains unsupported by the current bundle.

## Non-goals

- Does not re-implement logic already owned by the `superpowers` skills it dispatches into.
- Does not dispatch a model reviewer to fix artifact shape/schema failures — those get deterministic
  fix instructions only.
- Does not dispatch mutating workers without isolated worktrees.
- Does not treat export failure as a lost committed decision; authoritative commit failure blocks.
- Does not re-read `memory_brief` mid-run — loaded once, at Phase 0.
- Does not inline full spec/plan/diff bodies into gate prompts — `ArtifactRefs` plus capped
  summaries only.
- Does not adopt, copy, or symlink artifacts from a sibling run directory, ever.
- Does not let `max_clarifying_questions_per_phase` auto-approve `spec.approved`, `plan.approved`,
  a review gate, a drift gate, or a blocking verification gate.
- Does not run a second full Round-2 code review unless a new high-risk flag appears or the user
  explicitly asks for one.
- Does not block or halt a run solely because a lifecycle adapter is missing or failing.

## Cross-references

Calls into: `gate-arbiter`, `story-intake`, `effort-sizing` (→ `sizing-analyst`
agent), `superpowers:brainstorming`, `superpowers:writing-plans`, `qa-scoping`
(`--checklist` / `--review-tests` / `--update`), `superpowers:subagent-driven-development`,
`superpowers:test-driven-development`, `gate-runner`, `test-heal`, `acceptance-check`, `lead-proxy`
(autonomous verdict role for blocking verification), `story-proxy` (epic decomposition),
`code-review-orchestrator` (consumes `qa-checklist.md` as an `ArtifactRef`; applies its own
`references/review-lenses.md` methodology), `mr-submit` (post-handoff), `mr-watch` (optional
post-handoff monitoring chain), `role-memory` (Phase 0 load), `codebase-scout` (codebase grounding
for requirements and complexity scoring). Invoked by: `sdlc-guided` (hitl), `sdlc-auto`
(autonomous), and resumed via `sdlc-runs`.
