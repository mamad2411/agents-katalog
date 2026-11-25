---
name: qa-e2e-generator
description: >-
  Turn one work-item id into executable end-to-end (UI/API) test automation.
  Invoke when a QA engineer hands you a ticket id and wants a full E2E suite
  generated, run, reviewed, and pushed for review. Triggers: "generate e2e
  tests for PROJ-123", "qa-e2e-generator PROJ-123", "write end-to-end tests
  for this ticket", "automate e2e for <ticket>", "build a Playwright suite
  from this story". Standalone orchestrator — NOT auto-invoked by
  sdlc-engine. Requires a prior QA foundation (qa-strategy.md) and a
  configured ticket adapter (project.md). Top-of-pyramid only: no unit tests.
  Not for: manual/functional case writing (qa-case-generator), unit tests, or auto-invocation by sdlc-engine.
version: 0.1.0
license: Apache-2.0
allowed-tools: Read, Write, Bash, Glob, Grep, Agent, AskUserQuestion, TaskCreate, TaskUpdate, Skill
---

# qa-e2e-generator

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"qa-e2e-generator"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.

For a managed run, follow [`references/runtime-authority.md`](../../references/runtime-authority.md):
record phase decisions and execution evidence through runtime operations and use
`legacy.export` for compatibility ledgers. Direct JSONL appends never advance a run.


Orchestrator skill. One ticket id in, executable E2E automation out. You run an
11-phase pipeline that alternates inline shell steps with seven isolated
subagent dispatches, each returning a **structured verdict** and writing its
artifact to disk. Every completed phase is appended to a run ledger, so the flow
is resumable.

> Scope is the top of the test pyramid only — UI-level and API-level E2E.
> Unit-test generation is out of scope. Do not auto-invoke from the main SDLC
> orchestrator; a human (or a QA workflow) starts this explicitly.

> **Methodology owner.** How automated scripts are structured and scoped is defined by the `test-scripts`
> blueprint in `agentic-qe`
> (`skills/qe-blueprints/references/catalog/build/test-scripts.md`). This skill
> executes; the blueprint is the authority on method. If the two ever disagree,
> the blueprint wins and this file is what gets corrected — one source of truth,
> so two agents cannot follow two different sets of practices.

## Invocation

```
qa-e2e-generator PROJ-123
```

Exactly one argument: the ticket id. Missing it, halt with:

```
Usage: qa-e2e-generator <TICKET-ID>
```

## Inputs

| Input | Source | Notes |
|---|---|---|
| Ticket id | CLI arg (e.g. `PROJ-123`) | Required. Drives run slug + branch name. |
| Ticket adapter | `.agentic/guides/project.md` → `## Work Item Adapter` | Must be `configured`. Never a hardcoded backend. |
| QA strategy | `.agentic/guides/testing/qa-strategy.md` | Produced by the QA-foundation skill. |
| Git conventions | `.agentic/guides/standards/git-workflow.md` | Branch/commit rules for workspace setup. |
| Test env URL + auth | Asked at the env-config gate | Written with **actual** values, never placeholders. |

## Output

Run root:

```
docs/superpowers/qa-tasks/<date>-<slug>/e2e/
```

where `<date>` = `date +%Y-%m-%d` and `<slug>` = lowercased ticket id. Treat
`$RUN_DIR = docs/superpowers/qa-tasks/<date>-<slug>`; all artifacts land under
`$RUN_DIR/e2e/`.

| Artifact | Written by | Purpose |
|---|---|---|
| `$RUN_DIR/e2e/events.jsonl` | every phase | Run ledger; resume source of truth. |
| `$RUN_DIR/e2e/ac-check.json` | Phase 2 | Normalized AC + confidence. |
| `$RUN_DIR/e2e/context-manifest.json` | Phase 3 | Feature area + repo topology. |
| `$RUN_DIR/e2e/complexity-assessment.json` | Phase 4 | Sizing / routing signal. |
| `$RUN_DIR/e2e/test-plan.md` | Phase 5 | Scenario-level suite plan. |
| `$RUN_DIR/e2e/env-config.json` | Phase 6 | Real target env + auth wiring. |
| `$RUN_DIR/e2e/execution-results.json` | Phase 8 | First-run pass/fail evidence. |
| test spec files | Phase 7 | The generated E2E suite (in the target repo). |

## Reference tree

Prompt templates and helper scripts resolve against `${CLAUDE_PLUGIN_ROOT}`.

```
${CLAUDE_PLUGIN_ROOT}/skills/qa-e2e-generator/
├── SKILL.md
├── references/
│   └── subagents/            # one prompt template per isolated subagent
│       ├── ac-check.md       # Phase 2 — also the ac-check.json schema doc
│       ├── context.md        # Phase 3 — context-manifest.json schema doc
│       ├── plan.md           # Phase 5 — test-plan.md contract
│       ├── generate.md       # Phase 7–8 — generation + execution validation
│       ├── validate.md       # Phase 9–10 — code review + user review gate
│       └── mr.md             # Phase 11 — MR handoff
└── scripts/
    ├── qa-append-event.sh    # append a completed-phase record to the ledger
    ├── qa-assemble-meta.sh   # roll run artifacts into run metadata
    └── qa-e2e-smoke-test.sh  # quick smoke run of the toolchain + generated skeleton

${CLAUDE_PLUGIN_ROOT}/references/qa-authoring/   # shared authoring set
    (reached from subagent prompts as ../../references/qa-authoring/)
```

- `references/subagents/<name>.md` — read the file, then dispatch the Agent
  tool with it as the subagent's brief. Phase 4 is the exception: it dispatches
  the **named agent type** `sizing-analyst`, so there is no file to read.
- `../../references/qa-authoring/` — shared, cross-subagent authoring guidance
  (AC-quality rubric, scenario design heuristics, selector/naming conventions,
  spec structure). Subagents cite it so generated tests read as one house style;
  keep skill-specific orchestration out of it.
- `scripts/` — inline helpers. Paths are fixed; call them by absolute
  `${CLAUDE_PLUGIN_ROOT}/skills/qa-e2e-generator/scripts/<script>`.

## Pipeline

| # | Mode | Blast | Dispatch | Agent inputs | Writes | Event |
|---|---|---|---|---|---|---|
| 0 | inline | R0 | — | — | resume state | `preflight` |
| 1 | inline | R0 | — | — | `adapter` var | `environment-validation` |
| 2 | agent | R1 | `subagents/ac-check.md` | `ticket_id`, `adapter`, `run_dir` | `ac-check.json` | `ac-quality-check` |
| 3 | agent | R1 | `subagents/context.md` | `ac_check_path`, `adapter`, `run_dir` | `context-manifest.json` | `context-gathering` |
| 4 | agent type | R1 | `sizing-analyst` | `task_description`, `feature_area`, `run_dir` | `complexity-assessment.json` | `complexity-assessment` |
| 5 | agent | R1 | `subagents/plan.md` | `manifest_path`, `complexity_path`, `run_dir` | `test-plan.md` | `test-suite-planning` |
| 6 | inline | R2 | — | — | `env-config.json`, branch, worktree | `workspace-setup` |
| 7 | agent | R2 | `subagents/generate.md` | `plan_path`, `manifest_path`, `run_dir` | test spec files | `test-generation` |
| 8 | (same agent) | R1 | `subagents/generate.md` | `plan_path`, `manifest_path`, `run_dir` | `execution-results.json` | `test-execution-validation` |
| 9 | agent | R1 | `subagents/validate.md` | `results_path`, `plan_path`, `manifest_path`, `run_dir` | review notes | `code-review` |
| 10 | (same agent) | gate | `subagents/validate.md` | `results_path`, `plan_path`, `manifest_path`, `run_dir` | — | `user-review-gate` |
| 11 | agent | R3 (gated) | `subagents/mr.md` | `manifest_path`, `plan_path`, `results_path`, `run_dir` | merge request | `handoff` |

> Phases 7–8 are **one** generate dispatch that emits two events; 9–10 are one
> validate dispatch that emits two events. Phase 11's `handoff` event does not
> fire on subagent return — it fires in finalization, after
> `qa-assemble-meta.sh` has rolled up run metadata.

### Subagent dispatch contract

For each file-backed subagent phase:

1. Read the prompt template from `references/subagents/<name>.md`.
2. Dispatch the Agent tool, passing the exact input keys from the table (no
   more, no fewer). Subagents are **isolated** — they receive only the
   paths/values handed to them, never your whole context.
3. The subagent grounds strictly in its inputs, writes its structured artifact
   into `$RUN_DIR/e2e/`, and returns a structured verdict (never prose).
4. Append the event:
   `${CLAUDE_PLUGIN_ROOT}/skills/qa-e2e-generator/scripts/qa-append-event.sh "$RUN_DIR/e2e" <phase-number> <name> complete`
   For a managed SQLite run, the helper requires the coordinator run ID, lease
   epoch, and expected revision environment and records `event.record`; missing
   context fails closed. Refresh compatibility views with `legacy.export`.

Phase 4 skips step 1 and dispatches the `sizing-analyst` agent type
directly. Model-tier guidance: mechanical passes (AC check, MR compose) run
fine on **economy**; sizing and validation warrant **standard**; generation of
a non-trivial suite warrants **premium**.

### Inter-phase data handoff (3 → 4)

Phase 4 does not re-derive its inputs. Pull them from prior artifacts:

- `task_description` ← `.description` of `ac-check.json`
- `feature_area` ← `.feature_area` of `context-manifest.json`

## Phase detail

### Phase 0 — preflight (inline, R0)

Parse the argument; halt with the usage line if absent. Check for an existing
`$RUN_DIR/e2e/events.jsonl`. If found, this is a resume — read completed phases
from `.phase` / `.name` records and offer the user:

- **continue** — skip every phase whose number ≤ the last recorded phase, and
  re-read prior JSON outputs from disk instead of regenerating them.
- **regenerate** — delete the run dir and start clean.

### Phase 1 — environment validation (inline, R0)

Verify the gate files and repopulate the `adapter` variable. **This phase always
re-runs**, even on resume, because later dispatches need `adapter`; on resume it
does its work but **suppresses its own event** (do not append
`environment-validation` again).

Gate checks — halt on any failure:

| Condition | Halt message |
|---|---|
| `qa-strategy.md` missing | `ERROR: qa-strategy.md not found — run qa-baseline` |
| `project.md` missing | `ERROR: project.md not found — run /repo-guides` |
| No `## Work Item Adapter` section, or `**Status**:` ≠ `configured` | `ERROR: no ticket adapter configured in project.md's ## Work Item Adapter section — run /repo-guides` |

Read the adapter from `.agentic/guides/project.md` `## Work Item Adapter`
(fields `**Adapter**:`, `**Status**:`; required value `configured`).

### Phase 2 — AC quality check (agent, R1)

Dispatch `ac-check`. It resolves the ticket through the adapter and writes
`ac-check.json` with fields `ticket_id`, `title`, `description`, `ac[]`,
`ac_confidence`, `ac_source`. **Halt if `ac_confidence` < 50%** — the ticket is
too ambiguous to automate against; send it back for AC clarification.

### Phase 3 — context gathering (agent, R1)

Dispatch `context`. It reads `ac_check_path` and produces
`context-manifest.json` (`feature_area`, `test_repo.separate`, `test_repo.root`,
…). It must **never scan the whole codebase without user approval** — grounded,
targeted exploration only.

### Phase 4 — complexity assessment (agent type, R1)

Dispatch the `sizing-analyst` type with the handed-off `task_description`
and `feature_area`. Writes `complexity-assessment.json`.

### Phase 5 — test-suite planning (agent, R1)

Dispatch `plan`. Consumes `manifest_path` + `complexity_path`, emits
`test-plan.md` — the scenario inventory the generator implements.

### Phase 6 — workspace setup (inline, R2, resume-guarded)

Skip cleanly if the resume check already recorded `workspace-setup`.

**Env-config gate (before any test file is written):** ask the user for the test
environment URL and the auth method. Write `env-config.json` from their real
answers:

```json
{ "base_url": ..., "auth_method": ..., "auth_env": ... }
```

> Never write example/placeholder values. `auth_env` holds the **name** of the
> env var carrying the secret — the secret itself is never written to disk.

**Target repo:** read `test_repo.separate` / `test_repo.root` from the manifest.
`separate = true` → the external test repo at `test_repo.root`; otherwise the
current repo. Bind `GIT_REPO` accordingly and scope **every** git command with
`git -C "$GIT_REPO"`.

> When `test_repo.separate = true`, never run branch operations in the main repo.

**Branch:** read `git-workflow.md` for naming; derive the branch, falling back to
`qa/{ticket_id_lower}-e2e-tests`. Resolve it:

| State | Action |
|---|---|
| On base branch | `fetch` + fast-forward-only merge, verify clean, create the new branch |
| Branch exists, clean, on right base | Reuse via `checkout` |
| Dirty / stale / diverged | AskUserQuestion → continue / recreate / reconcile / abort |

Base-branch fallback chain: configured base → repo default → `main`.

**Dirty working tree** → AskUserQuestion with five options: stash / commit first
/ hard reset (only after explicit confirmation that **names the branch and
acknowledges data loss**) / proceed dirty (with warning) / abort (write
nothing).

> Never auto-stash, hard-reset, or proceed dirty without explicit user
> confirmation. Isolate parallel writes with a git worktree so concurrent spec
> generation cannot corrupt the tree.

### Phases 7–8 — generation + execution validation (one agent, R2 then R1)

Dispatch `generate` once. It implements `test-plan.md` into spec files against
the configured env, then runs them. It may lean on the optional `playwright-cli`
skill for a Playwright toolchain, and on `qa-e2e-smoke-test.sh` to confirm the
runner and spec skeleton execute before committing to the full run. Emit
`test-generation` after files land, then `test-execution-validation` after the
run writes `execution-results.json`.

### Phases 9–10 — code review + user review gate (one agent, R1 then gate)

Dispatch `validate` once against `results_path` + `plan_path` + `manifest_path`.
Emit `code-review` after the automated review, then present the results at the
`user-review-gate` and emit that event once the human decision is recorded.

### Phase 11 — MR handoff (agent, R3, gated)

The external side-effect. Only after finalization:

1. Roll up metadata:
   `${CLAUDE_PLUGIN_ROOT}/skills/qa-e2e-generator/scripts/qa-assemble-meta.sh "$RUN_DIR/e2e"`
   This compatibility assembler remains for unmanaged fixtures; managed runs
   must use the runtime lifecycle operation and `legacy.export` to regenerate
   metadata.
2. Dispatch `mr`, which composes and opens the merge request through the
   adapter (handing off to the `mr-submit` skill — no source-control platform
   hardcoded).
3. Append the `handoff` event.

> R3 stays behind a gate: no MR is opened until the user-review gate has passed
> and metadata is assembled. The MR is the only step that touches anything
> outside the run dir / target repo.

## Blast radius

| Tag | Meaning | Phases |
|---|---|---|
| R0 | read-only | 0, 1 |
| R1 | run-artifact writes under `$RUN_DIR/e2e/` | 2–5, 8, 9 |
| R2 | repo file writes (branch, env-config, specs) | 6, 7 |
| R3 | external side-effect, gate-guarded | 11 |

## Decision rules (summary)

- AC confidence < 50% → halt.
- Any missing gate file / unconfigured adapter → halt with the exact message.
- Never scan the whole codebase without user approval.
- Never take a destructive git action (hard reset, stash, dirty proceed) without
  explicit user confirmation.
- Never run branch ops in the main repo when the test repo is separate.
- Env config uses real values, never placeholders.

## Non-goals

- No unit-test generation.
- No auto-invocation from `sdlc-engine`.
- No destructive git actions without explicit confirmation.
- No whole-codebase scanning without approval.
- No placeholder values in `env-config.json`.
