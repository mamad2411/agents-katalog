---
name: gate-arbiter
discoverable: false
description: Invoke this skill whenever an SDLC pipeline phase reaches a judgment gate and needs a resolved, logged verdict — spec approval, plan approval, QA drift, code review (final or check round), requirements ambiguity, spec clarification, or feature verification. Trigger phrases include "resolve this gate", "route this decision", "get a verdict for <gate_id>", "who approves this", "check the escalation rule", or "record this decision". It is the single entry point for every recognized gate id in both hitl and autonomous modes. Not for: the `qa.ready` signal — that stays deterministic inside the calling pipeline and never enters this router's table — gate ids outside its recognized set, or making the underlying judgment itself (it resolves and logs verdicts through the configured mode).
---

# gate-arbiter

Coordinator-owned router for every judgment gate in the SDLC pipeline. Given a gate id and a mode
(`hitl` or `autonomous`), it decides *how* the gate gets settled — human question, deterministic
check, fast-path approval, or dispatched stand-in reviewer — always returns one fixed verdict
shape, and requires a supported authoritative commit before progression.

> The coordinator decides and commits through supported runtime operations; workers advise. It never edits a spec, plan, diff, or evidence file, and it never
> runs review-lens subagents itself — those live one level down, inside `code-review-orchestrator`.

## Availability and authority

`runtime/agentic_runtime/registry.json` is the sole source of gate/loop identifiers and policy
defaults. `references/runtime-contracts.md` is generated from it. The bundled runtime provides
versioned lifecycle, decision, evidence, export, and reconciliation operations. This skill must
commit gate decisions through the runtime operation (`decision.record`) when a runtime run exists;
an unavailable operation blocks. Never simulate resolution by appending JSON/JSONL or claim a
managed gate was committed.

The authority is `.agentic/state/runtime.sqlite3`. `.agentic/runs/<run-id>/` holds
regenerable exports, not the decision ledger of record. Use `legacy.export` only to refresh
compatibility ledgers for older readers. Preserve human specs/plans under
`docs/superpowers/`. Establish branch/worktree ownership before any run-artifact writes.

## Operating modes

| Mode | Behavior |
|---|---|
| `hitl` | Every recognized gate goes to `AskUserQuestion`. No fast-path, deterministic shortcut, or stand-in substitutes for the human's answer. The two code-review gates are the one carve-out: run the inline `code-review-orchestrator` skill first to produce a report, then ask the human — the report informs the question, it never resolves the gate on its own. |
| `autonomous` | Resolution tries cheapest-first: deterministic check → mandatory escalation check → eligible fast-path → advisory stand-in subagent. Code-review gates are pinned to the inline skill and never fall through to fast-path or stand-in dispatch. |

An unrecognized gate id is a structural error in either mode, not a judgment call: reject
immediately, decision `abort`, confidence `low`, escalation forced.

## Gate catalog

`gate_id` is a frozen, shared-contract enum. Reuse these ids verbatim — never invent new ones,
never abbreviate them.

| Gate ID | Resolver | Kind |
|---|---|---|
| `requirements.ambiguous` | `story-proxy` | subagent |
| `spec.clarification` | `story-proxy` | subagent |
| `spec.approved` | `lead-proxy` | subagent |
| `plan.approved` | `lead-proxy` | subagent |
| `code-review.final` | `code-review-orchestrator` | skill (inline) |
| `code-review.check` | `code-review-orchestrator` | skill (inline) |
| `qa.drift` | `lead-proxy` | subagent |
| `feature.verification` | `lead-proxy` | subagent |

Three additional ids are recognized (valid in both modes and checked against the registry)
but carry no resolver row: `classification.confirm`, `qa-checklist.approved`, `qa-tests.approved`.
In autonomous mode they have no stand-in to dispatch to — they resolve through eligible deterministic/fast-path steps after mandatory escalation checks, or escalate to the user.

A related but separate id, `qa.ready`, is never routed through this skill at all — see Non-goals.

## Resolution order

1. Reject unknown IDs or malformed required inputs as structural blockers. Validate required
   evidence shape deterministically; missing evidence cannot be approved by a resolver.
2. Evaluate mandatory escalation against effective policy and all known risk flags, including
   `security`, `breaking-change`, `migration`, and `spend`. This check precedes **every**
   approval path, including deterministic approvals and fast-path hints.
3. For review gates, invoke `code-review-orchestrator` inline for an advisory report. The
   coordinator retains gate authority; review workers cannot approve or transition the run.
4. In `hitl`, obtain the user's judgment. A report or fast-path hint cannot substitute for it.
   Mandatory escalation in autonomous mode also goes to the user before approval.
5. In autonomous mode without mandatory escalation, accept a supported deterministic result
   or eligible, evidence-grounded fast path. Presence of `context.fast_path` alone is insufficient.
   Otherwise request the mapped resolver's advice; if none applies, ask the user.
6. Validate advice, reevaluate escalation using newly reported risks and confidence, and then
   have the coordinator commit the decision through the supported runtime operation. Low
   confidence and exhausted malformed-output retries require escalation. Persistence failure
   blocks progression; an advisory verdict is not a committed gate decision.

## `feature.verification` deterministic sub-rules (autonomous only, in order)

Read `<run_dir>/acceptance-check-plan.json` and `<run_dir>/evidence/verification/*.json`
(each evidence file carries `result` — `PASS|FAIL|INCONCLUSIVE|BLOCKED` — and `screenshot_path`).
Evaluate in this order, stopping at the first match:

1. Verification tool is `"unconfigured"` **and** any evidence result is `BLOCKED` → `request-changes`.
   This is a hard escalation even though the mode is autonomous.
2. Any evidence `result` is `FAIL` → `request-changes` with concrete follow-ups.
3. Any evidence `result` is `INCONCLUSIVE` → `request-changes`, asking for expanded coverage.
4. Any evidence entry is missing its `screenshot_path` artifact → `request-changes`.
5. All `PASS`, all screenshots present, zero console/network errors, no risk flags → deterministic
   `approve`. Only after mandatory escalation checks; no stand-in dispatch is needed.
6. All `PASS` but risk flags are present → do not stop; apply mandatory escalation and otherwise seek advisory confirmation.

## Escalation rule

Evaluate mandatory escalation before any approval path, including deterministic and fast-path results. Force any stand-in- or orchestrator-produced advice back to a human question (`AskUserQuestion`)
when any of the following hold:

- `confidence` is `low`.
- The verdict's `risk_flags` intersect the caller-supplied `escalate_on` list.
- The stand-in returned unparseable output twice in a row (second parse failure).

The full escalation predicate — including how risk-flag intersection is computed and how the
"low confidence" threshold is read off a stand-in's structured return — is authored once in
`references/decision-heuristics.md`; do not re-derive it ad hoc, follow that reference.

## Human override and audit trail

A human's answer always wins and is tagged as the authoritative decision — even one delivered
after an automated verdict was already produced (e.g., the code-review report informed a human
answer, or an escalation surfaced a stand-in's low-confidence call). The superseded automated
verdict is preserved for audit under a resolver-specific field, never the reverse:

- `prior_subagent_verdict` — for gates resolved by a dispatched stand-in (`story-proxy`, `lead-proxy`).
- `prior_orchestrator_verdict` — for the two code-review gates, resolved by the inline
  `code-review-orchestrator` skill.

## Code-review gates (special case)

`code-review.final` and `code-review.check` never reach fast-path or stand-in dispatch, in either
mode, because the resolver itself needs to fan out further sub-work (parallel review-lens
subagents) that a single dispatched stand-in cannot do. Resolve them by invoking the
`code-review-orchestrator` skill inline via the **Skill tool** — never the Agent tool — passing:

- `gate_id`
- `original_task`
- `artifacts` — review bundle, diff/`diff_base`, spec/story, project guides, evidence summaries,
  optional QA report
- `memory_brief`
- `run_dir`
- on `code-review.check` only: `prior_verdict` — the full prior verdict object, or an ArtifactRef
  to `<run_dir>/code-review-final.json`. The orchestrator safe-fails without it.

`code-review.final` evaluates the whole change. `code-review.check` is a narrow re-verification of
previously identified findings plus their fix — it should not restart a full review unless the fix
itself introduces new high-risk concerns.

If the orchestrator produces no usable verdict, return a blocking low-confidence request-changes recommendation; the coordinator records the blocked outcome only through supported runtime operations.

## Inputs

| Field | Notes |
|---|---|
| `gate_id` | one of the enum values above |
| `question` | human-readable prompt, used verbatim by `AskUserQuestion` and carried into the event ledger |
| `options?` | optional choice list; when present, `decision` may be `<option-text>` instead of `approve/request-changes/abort` |
| `context.task` | grounding context for the gate |
| `context.artifacts` | ArtifactRefs — paths/summaries, never inlined bodies |
| `context.phase` | pipeline phase, carried into `events.jsonl` |
| `context.risk_flags` | flags checked against `escalate_on` |
| `context.memory_brief` | read from the per-role memory store |
| `context.fast_path?.reason` | advisory hint only; requires evidence and mandatory escalation checks |
| `mode` | `hitl` \| `autonomous` |
| `run_dir` | run-scoped directory all persisted files below are relative to; conventionally a run's directory under `.agentic/` |
| `escalate_on` | caller-supplied risk-flag list for the escalation rule |

## Outputs — verdict object

| Field | Notes |
|---|---|
| `decision` | `approve` \| `request-changes` \| `abort` \| `<option-text>` |
| `rationale` | grounded in `context` and any resolver output — never invented |
| `follow_ups` | concrete next actions, if any |
| `confidence` | `high` \| `medium` \| `low` |
| `risk_flags` | flags surfaced by the resolver |
| `source` | `hitl` \| `deterministic` \| `fast-path` \| `subagent` |

Code-review verdicts carry additional fields: `business_review`, `standards_review`, `findings`,
and on check rounds `finding_status`. Internally these are tagged `verdict.source: "skill"` when
produced autonomously by the orchestrator, or `"hitl"` when the orchestrator's report was
human-reviewed.

## Retry and persistence contract

`arbiter.malformed.retry` has its `max_retries` and `on_cap` in the registry. Counts mean
retries after the initial attempt. Check success before exhaustion: a valid final retry is
usable. All reruns share the budget, including user-requested ones; extra attempts require an
explicit recorded budget increase. Resume does not reset the budget.

Once implemented, coordinator-owned runtime transactions persist the decision and matching
state/event atomically. Metadata, `decisions.jsonl`, `events.jsonl`, `code-review-final.json`,
and `code-review-check.json` are regenerable exports. Never use best-effort export writes as a
substitute for authoritative persistence. An export failure after commit may be repaired; a
failed or unavailable authoritative commit prevents progression.

## Evidence schema (validated upstream, before this skill sees it)

```json
{
  "schema": 1, "task_id": "<id>", "test_first": <boolean>,
  "failing_test_command": "<string>", "failure_excerpt": "<string, ~500 chars>",
  "implementation_summary": "<string>", "passing_command": "<string>",
  "passing_excerpt": "<string, ~500 chars>", "files_touched": ["<path>", "..."],
  "diff_lines_added": <integer>, "diff_lines_removed": <integer>
}
```
Required subset — missing any forces `request-changes`: `schema`, `task_id`, `test_first`,
`failing_test_command`, `failure_excerpt`, `passing_command`, `passing_excerpt`, `files_touched`.

## Dispatch and interaction mechanics

- **Stand-in dispatch** (non-code-review gates): use the **Agent tool**. Pass `description`
  (include the `gate_id`) and `prompt` (the full inputs block; artifacts as ArtifactRefs — paths
  or summaries, never inlined bodies). Parse the returned stdout as JSON; retry once on parse
  failure; escalate on a second failure.
- **Code-review gates**: use the **Skill tool** to invoke `code-review-orchestrator` inline — see
  Code-review gates above. This step spends a model call, same as a stand-in dispatch, but never
  runs as a dispatched subagent.
- **Human interaction**: `AskUserQuestion`, passed `question`, `options`, and a compact bundle
  drawn from `context`.

## Blast radius

R1 — coordinator-owned runtime decision mutations only when implemented; JSON/JSONL are regenerable exports. It never writes
repo files (R2) and never triggers external side effects (R3); it only reads upstream artifacts
(evidence files, verification plan) and resolver output before recording a decision.

## Non-goals

- Does not run review-lens subagents, write code, or generate specs/plans — it only routes to
  resolvers and records outcomes.
- Does not modify any input artifact (spec, diff, evidence, verification plan) — decision-only.
- Does not decide the `qa.ready` signal. That stays out of this routing table entirely — the
  calling pipeline decides it deterministically once verification work is done or skipped, and
  nothing reaches hand-off without recorded verification proof for user-visible changes.
- Does not allow any autonomous shortcut — fast-path, deterministic, or stand-in — to substitute
  for a human answer on a recognized gate when `mode` is `hitl`.
- Does not let the two code-review gates reach fast-path or stand-in dispatch, in either mode.

## Cross-skill dependencies

- **`sdlc-engine`** — assembles gate inputs (review bundle, ArtifactRefs, `memory_brief`), owns runtime coordination, decides `qa.ready` deterministically, and blocks on failed authoritative persistence. Export warnings do not invalidate committed state.
- **`code-review-orchestrator`** — the skill invoked inline at the review step; runs bounded parallel
  review-lens subagents itself, reports standards/security findings and advisory verdicts. The coordinator owns final resolution.
- **Stand-in resolvers** — `story-proxy` (requirements/clarification gates), `lead-proxy`
  (spec/plan/drift/verification gates).
- **Memory** — reads `memory_brief` from the per-role memory store under `.agents/memory/sdlc/`.

## References tree

- `references/decision-heuristics.md` — the authoritative escalation predicate: how confidence
  levels are read from a resolver's structured return, how `risk_flags` intersection against
  `escalate_on` is computed, and how the two-strikes malformed-output rule is counted across a
  retry. Consult it before hand-rolling escalation logic anywhere else in the pipeline.
