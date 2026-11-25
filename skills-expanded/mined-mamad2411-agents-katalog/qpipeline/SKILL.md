---
name: qpipeline
description: "This skill should be used when the user asks to \"run the full pipeline\", \"qpipeline\", \"end-to-end review\", \"thorough review\", \"qpipeline auto\", an autonomous build, or wants a composable multi-phase workflow. Presets: review (quick), thorough (full QRALPH-equivalent), content, code. `auto` = autonomous end-to-end SDLC Workflow. Custom phase composition supported."
version: 0.3.0
---

# /qpipeline -- Composable Multi-Phase Pipeline Orchestrator

## Purpose

Orchestrate end-to-end workflows by composing review primitives into phased pipelines. **This SKILL.md's protocol IS the orchestrator** -- follow the steps below in order, executing each phase per its Phase Type description, gating on human approval where required. This is NOT skill-to-skill composition: phases that need deterministic, code-enforced state (review/review-loop convergence) invoke the same ultracode Workflow that powers `/qreview` and `/qloop`; phases that are single deterministic tool calls (test-gate) or a single fresh-context agent (verify) are just that.

> **Hard rule: NEVER hand-write a review/pipeline workflow script.** The ONLY
> sanctioned paths for this skill are `scriptPath=review-loop.workflow.js`
> (the `review` / `review-loop` phase types) and `scriptPath=pipeline-auto.workflow.js`
> (`/qpipeline auto`, below). If a phase's script file is missing, STOP and
> report — do not improvise a workflow or hand-roll a review loop in prose. A
> hand-rolled script has no `model:` tiering, so every agent it spawns
> silently inherits the invoking session's model (including expensive
> long-context variants) — this is the single largest source of runaway spend
> observed across past runs.

Ship with four presets. Accept custom phase lists. Gate on human approval where required. Never skip a phase.

The presets above are the **gated, human-in-the-loop** pipeline. `/qpipeline auto` is a **separate, autonomous** mode — see below.

## Version check (best-effort, non-blocking)

Before the first phase, run `python3 <tools>/version-check.py check` once. It is
rate-limited (~once/day) and fails silent-and-open. If it prints an upgrade notice,
relay that single line to the user, then continue — never block, retry, or wait on it.

## Autonomous mode: `/qpipeline auto`

When the user asks for `/qpipeline auto` (or "build this autonomously end-to-end"), run the **`pipeline-auto` ultracode Workflow**. The gated presets above exist to pause at human gates; `auto` is the opposite (no stopping). This mode drives a full SDLC from a one-line goal to a verified stop:

`requirements → design → separate-context TDD (per-slice worktrees, by wave) → serialized integration → unit/integration verify → stop-at-verify`

Every emitted artifact converges through the **same** engine that powers `/qloop` (run in-process per artifact), and every "need a human" moment routes through **`/qdecide` first** — a `decline` hard-stops, a `draft` on reversible-internal work proceeds-and-stages, and anything irreversible/external/spend is human-gated (qdecide can never authorize it). The whole run stays on a feature branch.

### Run it

Resolve the workflow script path (`js/` beside `tools/`):
- plugin: `<plugin>/js/pipeline-auto.workflow.js`
- fork: `~/.claude/ai-review-tools/js/pipeline-auto.workflow.js`

Invoke the **Workflow** tool with that `scriptPath` and:

```json
{
  "goal": "<the one-line goal to build>",
  "requirements": "requirements/current.md",
  "design": "DESIGN.md",
  "toolsDir": "<plugin>/tools  (or ~/.claude/ai-review-tools in the fork)",
  "threshold": 0,
  "maxRounds": 4,
  "maxParallel": 5
}
```

Optional args: `deployTarget` (declared, never inferred — see §6 of the design and the `auto prod` section below), `prodAutonomous: true` (opt-in prod deploy — set by `auto prod`), `smokeContract` (path to the cumulative smoke suite, default `smoke/prod.suite.json`), `stopAfter` (`requirements`|`design`|`tdd`|`integration`, for staged/bounded runs), `planOnly: true` (a zero-spend parser/plan check), `complexity` (`{files, toolTypes, contextFraction}` — CLI-time signal that tiers reviewer models; see below), `budgetReserve` (fraction of the run's budget to keep in reserve, default `0.05` — the pipeline stops gracefully via the runtime's shared `budget` signal before the hard spend throw, leaving room for the tail; inactive when the run has no budget target), and `team` (pre-resolved; otherwise phase 0 resolves it via `team-selector.py`). The Workflow streams per-phase progress via `log()` (watch with `/workflows`) and returns a `report` (with `report.warnings` for any degradation) and each artifact's convergence outcome. On a hard-stop / human-gate it returns `{status:"halted", at, decision, report}` — surface the decision and stop.

**Complexity posture (deliberate, not defaulted).** A `/qpipeline auto` run is definitionally a multi-file, multi-tool full SDLC, so team resolution passes explicit `--files`/`--tool-types` to `team-selector.py` (from your `complexity` arg, else a full-SDLC floor of files≥2/tool-types≥2) — model escalation engages by design rather than being left to a per-run agent's discretion. The same `complexity` is forwarded into every convergence loop so reviewers are tiered via `resolveReviewerModel`, not trusted verbatim from the team's declared model.

**Return `status` values:** `verified` (no deployTarget — stopped at verify), `staged` (deployTarget given, staging deployed + smoked green, stopped before prod), `promoted` (`auto prod` — prod deployed + smoked green), `rolled-back` (prod smoke failed, auto-rollback restored prod), `hard-page` (prod smoke failed and a human must be paged — stateful target or rollback failed to restore), `halted` (a gate refused; see `decision`).

**This mutates the working tree** (it authors requirements/design and, in the TDD phase, builds code in git worktrees). Run it in the target project on a branch you're willing to have modified.

### `/qpipeline auto prod`

`/qpipeline auto prod` is the explicit opt-in that, after the verified stop, runs the **production tail**: `DEPLOY-PLAN (qloop'd) → staging deploy → staging smoke → guardrail gate → qdecide(irreversible) → prod publish → prod smoke → PROMOTE | auto-rollback → re-smoke → escalate/hard-page`. Invoke the Workflow with `prodAutonomous: true` plus a declared `deployTarget`. Plain `/qpipeline auto` (no `prodAutonomous`) never publishes to prod: with a `deployTarget` it staging-deploys + smokes then stops (`status: staged`); with no `deployTarget` it stops at verify (`status: verified`).

**`deployTarget` is DECLARED, never inferred** (auto-detect may only *suggest* commands):

```json
{
  "kind": "cloudflare-worker | vercel | npm | ...",
  "stagingCmd": "wrangler deploy --env staging",
  "prodCmd": "wrangler deploy --env production",
  "stagingUrl": "https://staging.example.dev",
  "prodUrl": "https://example.dev",
  "rollbackCmd": "wrangler rollback --env production",
  "stateful": false
}
```

- **`rollbackCmd` is mandatory for prod** — the guardrail gate REFUSES prod without a present, dry-validated rollback.
- **`stateful: true`** downgrades a failed-smoke recovery from auto-rollback to **hard-page-only** (code rollback can't undo DB/KV/R2 mutations).

**The guardrail gate** (`prod-tail.py deploy_gate`, surfaced in the scorecard) must be fully green before prod: every artifact 0 P0/P1, unit + integration green, staging smoke 100%, rollback present + dry-validated, prod smoke assertions reviewed up front, this feature added its new smoke checks, `prodAutonomous` set, and **qdecide ≠ decline** (a `decline` hard-blocks; qdecide can never *authorize* an irreversible deploy — H-010).

**The curated, cumulative prod smoke suite** (`smoke/prod.suite.json`, `smokeContract` arg) is ONE maintained, versioned artifact — a growing regression net, not per-run-ephemeral. **Every feature MUST append its checks** (the gate fails a feature that ships no smoke check for its new behavior). Post-deploy the FULL suite runs against prod via parallel Haiku fan-out (batched by `plan_smoke_batches`, target 200+ checks, sub-linear wall-clock). Any check fails → auto-rollback (stateless) or hard-page (stateful) → re-smoke to prove restored.

> **Validation status:** phases 0–2 (requirements → design → slice validation) are behaviorally verified end-to-end; the full inlined Workflow (incl. the phase 7–8 prod tail) parses/links in the sandbox and the prod-tail safety cores are unit-tested. Phases 3–8 (per-slice TDD worktrees, serialized integration, verify, deploy tail) are structurally complete and parser-verified but await a full end-to-end behavioral run before production reliance. **Always dry-run `auto prod` against a throwaway staging target first.**

### Scorecard (mandatory final step)

When the Workflow ends, run the deterministic scorecard against the run and present it verbatim (same as `/qloop` step 5):

```
python3 <tools>/scorecard.py --workflow <session>/workflows/<runId>.json
```

## Presets

### `review` (default)

Quick review cycle. Use when the artifact exists and needs a quality pass.

Phases: `test-gate` -> `review-loop` -> `verify`

### `thorough`

Full QRALPH-equivalent pipeline. Use for greenfield features or anything Travis wants buttoned up end-to-end.

Phases: `ideate` -> `plan` -> `execute` -> `review-loop` -> `test-gate` -> `verify` -> `demo`

### `content`

Content and documentation review. Use for articles, proposals, strategy docs.

Phases: `review-loop` -> `verify`

### `code`

Code with test emphasis. Use for implementation work where test coverage matters.

Phases: `review-loop` -> `test-gate` -> `verify`

## Phase Types

Execute each phase type as described. Do not improvise phase behavior.

### `ideate`

Brainstorm and refine the concept. Read the artifact (if provided) and requirements. Produce `IDEATION.md` with concept options, tradeoffs, and a recommendation. **Gate:** present options to the user; user confirms the concept before proceeding.

### `plan`

Create an implementation plan. Produce `PLAN.md` with numbered tasks, dependencies, and SP estimates. Each task must be independently executable. **Gate:** present the plan to the user; user confirms before proceeding.

### `execute`

Execute plan tasks. For each task in PLAN.md, perform the implementation. Record results per task. This phase MUST be followed by a review phase -- verify this before starting the pipeline (see Compositional Integrity).

### `review`

Single-round multi-agent review — mechanically identical to `/qreview` steps 2-3 (`skills/qreview/SKILL.md`):

1. Resolve the team: `python3 <tools>/team-selector.py "<short artifact description>" --artifact <artifact_path> --json --files <N> --tool-types <N> --context-window 200000`.
2. Invoke the **Workflow** tool with `scriptPath` = `js/review-loop.workflow.js` (plugin) or `~/.claude/ai-review-tools/js/review-loop.workflow.js` (fork) and `{ artifact, requirements, team, rounds: 1, threshold: 0 }`.

Record the returned `final_findings` / `final_counts` as the phase result. Never hand-write the review loop — see the hard rule above.

### `review-loop`

Iterative review-fix cycle — mechanically identical to `/qloop` (`skills/qloop/SKILL.md`). This is the core phase:

1. Resolve the team (same `team-selector.py` call as `review`, above).
2. Invoke the **Workflow** tool with `scriptPath` = `js/review-loop.workflow.js` and `{ artifact, requirements, team, threshold: 0, maxRounds: 5 }` (omit `rounds` so it runs until-converged).

The Workflow owns round tracking, the fix-ALL gate, the min-2-rounds floor, stuck detection, and max-rounds escalation in code — do not reimplement any of this in prose, and do not hand-roll a review/fix loop yourself. Record the returned `outcome` (`converged` or `escalated`, plus `history`) as the phase result; an `escalated` outcome is a gate — present it to the user per Step 3 below.

### `test-gate`

Run deterministic tests via `tools/test-runner.py`. Discover co-located tests for the artifact and execute them. **Hard gate:** all tests must pass. If any test fails, the pipeline blocks. Fix failures and re-run. Do not advance past this phase with failing tests.

### `verify`

Fresh-context acceptance verification. Spawn the `verifier` agent (`agents/verifier.md`) with NO knowledge of the review history. The verifier receives only the artifact, requirements, and a clean review prompt. The verifier produces an independent pass/fail assessment. If the verifier fails the artifact, return to the review-loop or escalate.

### `demo`

Present the completed work to the user. Show what changed, what was reviewed, what findings were addressed, and the final convergence status. **Gate:** user approves or provides feedback. Maximum 2 revision cycles -- if the user rejects twice, escalate rather than looping indefinitely.

### `deploy`

Pre-deployment checks. Validate that the artifact is in a deployable state: tests pass, no P0/P1 findings remain, all gates cleared. **Gate:** user confirms deployment.

### `smoke`

Live validation of the deployed artifact. Run the artifact in its production context and verify it produces correct output. Record evidence of success or failure. If smoke fails, roll back and return to the fix phase.

### `learn`

Extract learnings from the completed pipeline. Record what worked, what surprised, what the review caught that manual inspection would have missed. Store learnings for future pipeline runs.

## Pipeline Protocol

Follow these steps in order. Do not skip steps. Do not combine steps.

### Step 1: Resolve the Phase List

Pick a preset (or accept a custom phase list) and validate it before doing any work (see Compositional Integrity, below). Present the resolved phase list to the user so the run is auditable from the start.

### Step 2: Execute Phases

Walk the phase list in order. For each phase, execute exactly what its **Phase Type** entry above describes — no more, no less:

- `test-gate` -- run `tools/test-runner.py` on the artifact.
- `review` -- resolve the team, then invoke the Workflow (`scriptPath=js/review-loop.workflow.js`, `rounds: 1`).
- `review-loop` -- resolve the team, then invoke the Workflow (`scriptPath=js/review-loop.workflow.js`, no `rounds`, until-converged).
- `execute` -- perform the plan's implementation tasks directly.
- `verify` -- spawn the `verifier` agent (`agents/verifier.md`).
- `ideate` / `plan` / `demo` / `deploy` / `smoke` / `learn` -- per their Phase Type entries; these are gates, not driver-tracked state.

Record each phase's result (findings, convergence outcome, test results, or gate decision) before moving to the next phase — carry it forward in context, since there is no separate persisted pipeline state. Do not advance to the next phase until the current one has a recorded result.

**Model tiering (Sonnet 5 by default).** Agent-spawning phases follow the same policy as `/qreview` and `/qloop`: default to **Sonnet 5**, escalate to **Opus** for high-stakes lenses (`security-reviewer`, `architecture-reviewer`) or complex work (change spans more than one file, needs more than two distinct tool-execution types, or exceeds ~20% of context).
- `review` / `review-loop` — pass the complexity flags (`--files`, `--tool-types`) into `team-selector.py`, and let the Workflow spawn each reviewer with its resolved `model` (already tiered in the `team` array) — never re-tier or override by hand.
- `verify` — a fresh-context verifier is a reviewer: default Sonnet 5, escalate to Opus by the same rule.
- `execute` — implementation typically touches multiple files, so it usually runs on **Opus**; a single-file, low-tool task stays on Sonnet 5.

### Step 3: Handle Gates

Gate phases (`ideate`, `plan`, `demo`, `deploy`) and an `escalated` `review-loop` outcome all work the same way:
1. Present the gate message / findings to the user and stop.
2. Wait for the user's approval or feedback.
3. On approval, advance to the next phase. On feedback, handle per phase type (`demo` allows 2 revision cycles, others escalate rather than looping indefinitely).

There is no auto-approve and no timeout — a gate blocks until the user responds.

### Step 4: Pipeline Completion

Once every phase has a recorded result, present the completion summary to the user.

Then ALWAYS emit the deterministic scorecard as the final output (pure, reproducible, no LLM), same as `/qloop` step 5:

```
python3 <tools>/scorecard.py --workflow <session>/workflows/<runId>.json
```

Run it against the `review`/`review-loop` phase's Workflow run (the richest in findings). It reports **Process**, **Issues Found** (by severity), **Token Cost** (per-model USD), and **Model Execution Time** (per-agent wall-clock rolled per model + the workflow wall-clock total). Pass `--pricing PATH` to override USD rates.

## Compositional Integrity

Validate the phase list as part of Step 1, before any phase executes:

- Any pipeline containing `execute` MUST also contain `review-loop`. Code changes without review are not permitted. All four built-in presets already satisfy this by construction; a custom phase list that omits `review-loop` after `execute` must be rejected — tell the user what's missing rather than proceeding.
- There is no `--skip` option. Phase skipping is not supported at any level; if a phase is in the list, it executes.

## Tools Reference

All tools live in the `tools/` directory relative to the plugin root:

- **`js/review-loop.workflow.js`** -- the ultracode Workflow (the loop engine) used by the `review` and `review-loop` phase types. Generated from `js/adjudication.mjs` + `js/prompts.mjs`; do not hand-edit.
- **`tools/team-selector.py`** -- deterministic domain classification + team selection + model tiering. Used before `review` / `review-loop` phases.
- **`tools/test-runner.py`** -- test discovery and execution. Used by the `test-gate` phase.
- **`tools/finding-parser.py`** -- finding validation, deduplication, convergence, formatting (the Python oracle backing the Workflow's JS port). Pure functions.
- **`tools/scorecard.py`** -- deterministic end-of-run scorecard.

## Key Rules

### No Skip Flag

There is no mechanism to skip a phase. If a phase is in the pipeline, it executes.

### Compositional Integrity is Verified Before Execution Begins

Invalid phase compositions (an `execute` with no `review-loop`) must be caught and reported before any work starts, not discovered partway through.

### Gates Block Until Confirmed

Gate phases stop and wait for the user. There is no timeout. There is no auto-approve.

### No Cross-Session Checkpoint / Resume

Unlike the prior Python-driver implementation, this protocol does not persist state to disk between turns. A pipeline run lives in the current conversation's context; there is no `/qpipeline status`, `/qpipeline resume <project-id>`, or `/qpipeline reset`. If a run needs to span multiple sessions, checkpoint manually (write the phase results and resolved team/artifact paths to a file) before ending the session, and re-establish that context when resuming.
