---
name: relentless-orchestrate
description: Master orchestrator for the relentless pipeline. Chains implement → validate → remediate → re-validate in a loop until all gates pass and live execution is clean. Owns the circuit breaker and escalation decisions. Follows RelentlessAgent principles — fresh context per phase, first-person progress summaries, zero context drift.
user-invocable: true
---

# Relentless Orchestrator

Drive the full implementation-to-validation pipeline. This skill is a **thin coordination loop** — it never does heavy work directly. Every phase runs in a fresh-context subagent. The orchestrator reads summaries, writes progress, and decides what to dispatch next.

**Announce at start:** "Starting relentless orchestration pipeline."

## Core Principles (from RelentlessAgent)

These six principles govern every design decision in this skill:

1. **Fresh context per phase.** Each phase (gates, implement, validate, remediate) runs in its own subagent with a clean context window. The orchestrator passes: original task + chronological progress summary. No phase inherits accumulated context from a prior phase.

2. **First-person progress summaries.** After each phase completes, the orchestrator writes `_orchestration_state.md` — a chronological narrative of what happened, what passed, what failed, and what's next. This file IS the orchestrator's memory. Not a structured report — a progress journal.

3. **Crash recovery = read state + continue.** If the orchestrator crashes, runs out of context, or is re-invoked, it reads `_orchestration_state.md` and picks up from the last completed phase. Same pattern every time — no special codepaths, no `--from=` flags.

4. **The state file is the only thing that survives.** Between phases, no in-memory state. No accumulated tool results. The orchestrator reads the state file, reads the latest artifact (`_gates.json`, `_validation_report.json`, test output), makes a decision, dispatches the next subagent, and writes the result back to the state file. Everything else is discarded.

5. **No vector memory, no RAG, no compression.** Just a loop: read state → dispatch subagent → read result → write state → decide next step.

6. **Zero context drift — architecturally impossible.** Each subagent gets a fresh window. The orchestrator stays thin (just reads summaries, never raw data). If the orchestrator's own context gets heavy, the state file contains everything needed to resume in a new session.

## Pipeline (this skill owns the full loop)

```
┌──────────────────────────────────────────────────────────────┐
│  relentless-orchestrate (THIS SKILL — thin loop)             │
│  ── read state → dispatch → write state ──                   │
│                                                              │
│  Phase 0: Pre-flight ── /relentless-preflight                │
│    └→ validate deps, profiles, ports, PRD structure          │
│    └→ write _relentless_config.json (shared config)          │
│    └→ FAIL → stop pipeline, report issues                    │
│                                                              │
│  Phase 1: Gates ──── via relentless engine                    │
│    └→ /relentless-gates (if _gates.json missing)             │
│    └→ -n / -t from config.pipeline.gates                     │
│    └→ write _orchestration_state.md                          │
│                                                              │
│  Phase 2: Implement ── via relentless engine                  │
│    └→ /relentless-implement (Implementer Agent)              │
│    └→ -n / -t from config.pipeline.implement                 │
│    └→ verify: TDD gates exit 0                               │
│    └→ write _orchestration_state.md                          │
│                                                              │
│  Phase 3: Validate ── via relentless engine                   │
│    └→ /relentless-validate (Validator Agent)                 │
│      └→ /relentless-devloop (browser testing delegate)       │
│    └→ -n / -t from config.pipeline.validate                  │
│    └→ read: _validation_report.json                          │
│    └→ write _orchestration_state.md                          │
│                                                              │
│  Phase 4: Remediate (looped)                             ┐   │
│    └→ /relentless-remediate (Remediator Agent)            │   │
│    └→ Re-validate: -n / -t from config.pipeline.revalidate│   │
│    └→ Regression: TDD gates check                        │   │
│    └→ write _orchestration_state.md                      │   │
│    └→ max loops from config.pipeline.remediate_max_loops ─┘   │
│                                                              │
│  Phase 5: Final Report                                       │
│    └→ aggregate from _orchestration_state.md                  │
│    └→ escalate non-fixable errors to user                    │
│    └→ mark complete or partial                               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Agent Roles

| Agent | Skill | Engine | Responsibility |
|-------|-------|--------|---------------|
| **PRD Writer** | `/relentless-prd` | `relentless` (config: pipeline.prd) | Codebase research + PRD generation |
| **Gate Generator** | `/relentless-gates` | `relentless` (config: pipeline.gates) | Generates failing TDD gate tests from PRD |
| **Implementer** | `/relentless-implement` | `relentless` (config: pipeline.implement) | Writes code, passes TDD gates |
| **Validator** | `/relentless-validate` | `relentless` (config: pipeline.validate) | Runs live execution, captures errors |
| **Dev Loop** | `/relentless-devloop` | N/A (delegated by validator) | Browser testing — navigate, click, screenshot, report |
| **Pre-flight** | `/relentless-preflight` | N/A (quick checks) | Validates env, writes `_relentless_config.json` |
| **Remediator** | `/relentless-remediate` | N/A (bounded, targeted) | Patches code from structured error report |
| **Orchestrator** | `/relentless-orchestrate` (this) | N/A (thin loop) | Dispatch, read summaries, write state |

All heavyweight phases (gates, implement, validate) run through the `relentless` engine, getting: per-session loop detection (`ToolLoopDetector`), cross-session stuck detection (`StateTracker`), cost tracking, `asyncio` timeouts, and `max_tool_calls` caps. Session counts (`-n`) and timeouts (`-t`) for each phase come from `_relentless_config.json` → `pipeline.<phase>.sessions` / `pipeline.<phase>.timeout_min`. The remediator is a targeted fix agent (bounded scope) defined in `/relentless-remediate`, so it runs as a bare subagent. Pre-flight runs once before the pipeline and writes `_relentless_config.json` — the shared config contract for all phases.

**Key principle:** No agent judges its own output. The implementer doesn't validate. The validator doesn't fix. The remediator doesn't validate its own fixes. Each handoff creates an independent checkpoint.

## The State File: `_orchestration_state.md`

This is the orchestrator's memory — a first-person chronological progress journal. Updated after every phase. Format:

```markdown
# Orchestration: prd_<slug>.md

## Current Phase: <phase name>
## Status: <in_progress | completed | failed | escalated>
## Loop Count: 0/<remediate_max_loops>

## Progress

### Phase 1: Gates (completed)
I found _gates.json already present with 15 ACs (12 machine, 3 manual).
Gate files confirmed on disk. Ran baseline: 0/12 pass (expected — implementation hasn't started).

### Phase 2: Implement (completed)
Launched relentless with 5-session limit. After 3 sessions, 11/12 gates passed.
Re-ran implementation — session 4 fixed the remaining gate (AC-7 had wrong field name).
All 12 machine gates now pass. Full test suite: 320 frontend + 26 backend, no regressions.

### Phase 3: Validate (completed)
Validator tested 5 API endpoints, 3 frontend routes. Found 2 errors:
- E-1: TypeError in DemandPlanTable.tsx (runtime, auto-fixable)
- E-2: SP permission denied on lakemeter_catalog (permission, escalate)
Report written to _validation_report.json.

### Phase 4: Remediate — Loop 1 (completed)
Dispatched remediator for E-1. Fix applied: null check on monthly_data.
Re-ran validator: E-1 resolved, E-2 still present (expected — permission error).
TDD gates: 12/12 still pass (no regression).
Stuck detection: E-2 is not auto-fixable. No more auto-fixable errors. Exiting loop.

### Phase 5: Final Report
[will be written when phase completes]

## Artifacts
- _gates.json: present, 15 ACs
- _validation_report.json: present, 1 error remaining (E-2, permission)
- _relentless_state.md: present (implementer's self-assessment)

## Escalated
- E-2: SP lakemeter-sp needs USE_CATALOG on lakemeter_catalog

## Next Action
Write final report. Mark complete with 1 escalation.
```

**Rules for the state file:**
- Write in first person ("I found...", "I dispatched...", "I decided to...")
- Include concrete numbers (gate counts, error counts, loop counts)
- Reference artifact file names (not their contents — keep the state file lean)
- Always update `Current Phase`, `Status`, `Loop Count`, and `Next Action`
- On crash recovery, the orchestrator reads this file to know exactly where to resume

## Process

### Step 0: Read state, read config, resolve environment

Every invocation starts the same way — read the state file and config:

```bash
cat _orchestration_state.md 2>/dev/null || echo "NO_STATE"
cat _relentless_config.json 2>/dev/null || echo "NO_CONFIG"
```

**If state exists:** Parse `Current Phase`, `Status`, and `Databricks Profile`. Resume from the next incomplete phase. Do NOT re-run completed phases. Write: "Resuming orchestration from Phase N."

**If no state — Phase 0: Pre-flight.** Before starting the pipeline, run or verify pre-flight:

#### Phase 0: Pre-flight

Check if `_relentless_config.json` already exists (pre-flight already ran):

```bash
cat _relentless_config.json 2>/dev/null
```

**If config exists:** Read it. Extract `databricks.profile`, `project_root`, `stack`, and port numbers. Skip to Phase 1.

**If config missing:** Run pre-flight to generate it. Use the Agent tool:

```
Run /relentless-preflight for the project at <project_root>.
PRD file: <prd_file>.
Validate the environment and write _relentless_config.json.
```

**If pre-flight reports FAIL checks:** Stop. Report the failures to the user. Do NOT proceed to Phase 1 until pre-flight passes. The user must fix the environment and re-invoke the orchestrator.

**If pre-flight passes:** Read `_relentless_config.json` for the resolved environment.

#### Environment from config

All downstream phases need these values from `_relentless_config.json`:

| Value | Config path | Used by |
|-------|-------------|---------|
| Databricks profile | `databricks.profile` | validator, remediator, implementer |
| Project root | `project_root` | all phases |
| Backend port | `backend.port` | validator |
| Frontend port | `frontend.port` | validator |
| App name | `databricks.app_name` | validator |
| Test command | `backend.test_command` | orchestrator (gate checks) |
| Stack | `stack` | validator (surface inference) |
| Gate sessions/timeout | `pipeline.gates.sessions` / `.timeout_min` | orchestrator (Step 1) |
| Implement sessions/timeout | `pipeline.implement.sessions` / `.timeout_min` | orchestrator (Step 2) |
| Validate sessions/timeout | `pipeline.validate.sessions` / `.timeout_min` | orchestrator (Step 3) |
| Revalidate sessions/timeout | `pipeline.revalidate.sessions` / `.timeout_min` | orchestrator (Step 4b) |
| Remediate max loops | `pipeline.remediate_max_loops` | orchestrator (Step 4) |
| Implement max retries | `pipeline.implement_max_retries` | orchestrator (Step 2) |
| Stuck threshold | `pipeline.stuck_threshold` | relentless engine |
| Tool repeat limit | `pipeline.tool_repeat_limit` | relentless engine |
| Max tool calls | `pipeline.max_tool_calls` | relentless engine |

**This config MUST be passed to every subagent prompt** — the implementer, validator, and remediator all read it, but the orchestrator should also include key values (especially Databricks profile) directly in the subagent task description for clarity.

Store the resolved profile in `_orchestration_state.md` under a `## Environment` section:

```markdown
## Environment
- Databricks Profile: `fe-westus` (from _relentless_config.json)
- Project Root: `/absolute/path/to/project`
- Stack: fullstack
- Config: _relentless_config.json present
```

Create `_orchestration_state.md` with the PRD target, environment, and Phase 1.

This is the unified crash recovery pattern. No `--from=` flags. No special codepaths. Just: read state, find where we left off, continue.

### Step 1: Ensure gates (relentless-protected)

1. **Check for `_gates.json`** — if present, verify gate files exist on disk
2. If missing, dispatch gates through the relentless engine (loop detection, cost tracking, timeout).

Read session count and timeout from `_relentless_config.json` → `pipeline.gates` (defaults: sessions=2, timeout_min=15):

```bash
# Read config values (or use defaults)
GATES_N=$(jq -r '.pipeline.gates.sessions // 2' _relentless_config.json 2>/dev/null || echo 2)
GATES_T=$(jq -r '.pipeline.gates.timeout_min // 15' _relentless_config.json 2>/dev/null || echo 15)

env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT relentless -d /absolute/path/to/project -n $GATES_N -t $GATES_T -p bypassPermissions -v \
  "Run /relentless-gates on prd_<slug>.md. Generate failing TDD gate tests for all machine-verifiable acceptance criteria. Write _gates.json manifest." \
  > /absolute/path/to/project/relentless_gates.log 2>&1
```

Run in background. Wait for completion, then check exit code and `_gates.json`.

3. Run baseline gate check:

```bash
cd backend && uv run pytest tests/gates/ --no-header -q --timeout=30 2>&1 | tail -5
```

4. **Write state:** Record gate count, which already pass (if any), baseline status
5. If all gates already pass: write "Gates already pass. Skipping to validation." and proceed to Step 3.

### Step 2: Run Implementer (subagent)

Dispatch `/relentless-implement prd_<slug>.md` — this launches the relentless CLI in a background process (fresh context per sub-session, the RelentlessAgent pattern).

Wait for completion. Then run the gate tests yourself (do NOT trust the implementer's self-report):

```bash
cd backend && uv run pytest tests/gates/ -v --no-header --timeout=30 2>&1
```

**Write state** with gate results. Include:
- How many gates passed/failed
- Which ACs failed and their error messages (1-line each)
- Whether a re-run is needed

**Decision** (read `pipeline.implement_max_retries` from config, default 2):
- All gates pass → proceed to Step 3
- <= 3 failures → re-run implement (up to `implement_max_retries` total sessions)
- \> 3 failures after max retries → escalate to user: "PRD may need revision"

### Step 3: Run Validator (relentless-protected)

Dispatch validation through the relentless engine (loop detection, cost tracking, timeout). The validator can be token-heavy — Chrome DevTools screenshots, network requests, Databricks CLI log tailing.

Build the task description with:
- The PRD's `validation_surfaces` and `log_commands`
- Progress summary from `_orchestration_state.md` (so it knows what was implemented)
- **The Databricks profile** from the `## Environment` section of the state file

Read session count and timeout from `_relentless_config.json` → `pipeline.validate` (defaults: sessions=2, timeout_min=20):

```bash
VAL_N=$(jq -r '.pipeline.validate.sessions // 2' _relentless_config.json 2>/dev/null || echo 2)
VAL_T=$(jq -r '.pipeline.validate.timeout_min // 20' _relentless_config.json 2>/dev/null || echo 20)

env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT relentless -d /absolute/path/to/project -n $VAL_N -t $VAL_T -p bypassPermissions -v \
  "Run /relentless-validate on prd_<slug>.md. Use Databricks profile <RESOLVED_PROFILE> for ALL Databricks CLI commands. Write _validation_report.json. Progress so far: <1-2 sentence summary from _orchestration_state.md>" \
  > /absolute/path/to/project/relentless_validate.log 2>&1
```

Run in background. Wait for completion, then read the report:

```bash
cat _validation_report.json 2>/dev/null | jq '.summary'
```

**Write state** with validation results. Include:
- Surfaces tested and their status
- Error count by category
- List each error (1-line: ID, category, auto_fixable)

**Decision:**
```
if total_errors == 0:
    → Step 5: Final Report (PASS)
elif auto_fixable > 0:
    → Step 4: Remediation Loop
elif needs_escalation > 0 and auto_fixable == 0:
    → Step 5: Final Report (PARTIAL — escalate only)
```

### Step 4: Remediation Loop

```
loop_count = 0
max_loops = config.pipeline.remediate_max_loops  # default: 3
prev_error_count = total_errors

while has_auto_fixable_errors and loop_count < max_loops:
    4a. Dispatch remediator subagent (fresh context)
    4b. Dispatch validator subagent (fresh context, re-check)
    4c. Run TDD gates (regression check)
    4d. Write state with loop results
    4e. Check stuck detection

    loop_count++
```

#### 4a. Spawn Remediator subagent

Use the Agent tool to dispatch `/relentless-remediate`. The remediator reads `_validation_report.json` and `_relentless_config.json` directly — you only need to tell it which errors to focus on:

```
Run /relentless-remediate.

Auto-fixable errors to fix from _validation_report.json:
{paste error IDs and 1-line summaries, e.g.:}
- E-1: TypeError in DemandPlanTable.tsx (runtime) — add null check for monthly_data
- E-3: Missing import in EstimateCard.tsx (runtime) — add formatCurrency import

Databricks profile: <PROFILE from _relentless_config.json>
Project root: <PROJECT_ROOT from _relentless_config.json>

Fix ONLY these errors. Do not refactor or run tests.
```

The remediator skill enforces its own constraints (minimal diff, source_file boundaries, no self-validation). See `relentless-remediate/SKILL.md` for full rules.

#### 4b. Re-run Validator (relentless-protected)

Dispatch a fresh validation through relentless (same pattern as Step 3, but with remediation context).

Read from `_relentless_config.json` → `pipeline.revalidate` (defaults: sessions=1, timeout_min=15):

```bash
REVAL_N=$(jq -r '.pipeline.revalidate.sessions // 1' _relentless_config.json 2>/dev/null || echo 1)
REVAL_T=$(jq -r '.pipeline.revalidate.timeout_min // 15' _relentless_config.json 2>/dev/null || echo 15)

env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT relentless -d /absolute/path/to/project -n $REVAL_N -t $REVAL_T -p bypassPermissions -v \
  "Run /relentless-validate on prd_<slug>.md. This is re-validation after remediation loop <N>. Use Databricks profile <RESOLVED_PROFILE>. Write _validation_report.json." \
  > /absolute/path/to/project/relentless_revalidate_<N>.log 2>&1
```

It writes a new `_validation_report.json`.

#### 4c. Regression Check

After remediation, run TDD gates to confirm nothing broke:

```bash
cd backend && uv run pytest tests/gates/ -v --no-header -q --timeout=30 2>&1
```

If TDD gates regressed:
- The remediation introduced a bug
- Escalate: "Remediation for E-X broke TDD gate AC-Y."
- Do NOT revert automatically — let the user decide

#### 4d. Write state

Update `_orchestration_state.md` with:
- Loop number
- Errors before vs after
- Which were fixed, which remain
- TDD gate regression status

#### 4e. Stuck detection

```
current_error_count = new_report.summary.auto_fixable

if current_error_count >= prev_error_count:
    # No improvement — stop immediately
    ESCALATE remaining errors
    break

prev_error_count = current_error_count
```

**Stuck detection beats loop counting.** If loop 2 has the same errors as loop 1, don't burn 3 more loops. The remediator is failing — escalate now.

### Step 5: Final Report

Read `_orchestration_state.md` and aggregate all phase results into a single report. This is the ONLY step that produces long output — all prior steps are lean state updates.

```
## Orchestration Results: prd_<slug>.md

### Pipeline Summary
| Phase | Agent | Status | Detail |
|-------|-------|--------|--------|
| Gates | relentless-gates | DONE | 11 machine gates + 4 manual |
| Implement | relentless-implement | PASS | 11/11 gates green (2 sessions) |
| Validate | relentless-validate | DONE | 2 errors found |
| Remediate | remediator subagent | PARTIAL | 1 fixed, 1 escalated |
| Re-validate | relentless-validate | DONE | 1 error remaining (permission) |
| Regression | TDD + full suite | PASS | No regressions |

### TDD Gate Results (source of truth)
| AC   | Gate Test | Result |
|------|-----------|--------|
| AC-1 | test_ac1_ramp_override | PASS |
| AC-2 | test_ac2_null_defaults | PASS |
| ...  | ... | ... |
| AC-12 | (manual) | SKIP |

Gates: 11/11 passed, 4 skipped (manual)

### Live Execution Results
- Backend API: 5/5 endpoints healthy
- Frontend: 0 console errors after remediation
- Database: migrations verified

### Remediation History
| Loop | Error | Action | Result |
|------|-------|--------|--------|
| 1 | E-1: TypeError in DemandPlanTable | Remediator added null check | FIXED |
| 1 | E-2: SP permission denied | Skipped (not auto-fixable) | ESCALATED |

Loops used: 1/<remediate_max_loops>

### Escalated Issues (require human action)
1. **E-2: Permission denied** — SP `lakemeter-sp` needs `USE CATALOG` on `lakemeter_catalog`

### Manual ACs (require human verification)
- [ ] AC-12: Load demand plan tab, check console for errors
- [ ] AC-13: Select Growth tier, observe hero card change
- [ ] AC-14: Compare hero card total vs demand stream row sum

### Files Modified
<from git diff --stat>

### Completion Status
- [x] TDD gates: all machine gates green
- [x] Full test suite: no regressions
- [x] Live execution: validated (1 remediation applied)
- [ ] 1 permission error escalated to user
- [ ] 3 manual ACs require human verification
```

### Step 6: Update artifacts

1. Update `_gates.json` — set each gate's `status` to: `passed`, `failed`, `skipped`, or `error`
2. Write final `_orchestration_state.md` with `Status: completed` (or `Status: partial`)

## Escalation Rules

The orchestrator escalates to the human when:

| Condition | Action |
|-----------|--------|
| Permission/auth error detected | Escalate immediately — no remediation attempt |
| Infrastructure error detected | Escalate immediately |
| Circuit breaker hit (`remediate_max_loops`) | Stop, report all attempts, escalate remaining |
| TDD gates regressed after remediation | Report regression, escalate |
| Same error count across consecutive loops | Stop looping (stuck), escalate that error |
| Implement fails after `implement_max_retries` | Escalate — PRD may need revision |
| Validator can't start app | Escalate — environment issue |

The PRD's `escalate_on` array provides additional project-specific escalation triggers.

## Design Principles

### The orchestrator is a for loop, not a brain

Read state. Dispatch subagent. Read result. Write state. Decide next step. That's it. The orchestrator does NOT read source code, run tests, analyze errors, or make complex judgments. It reads summaries and makes binary decisions: proceed, loop, or escalate.

### No agent judges its own output

The implementer doesn't validate its code. The validator doesn't fix errors. The remediator doesn't verify its patches. Each handoff creates an independent quality checkpoint. This prevents self-reinforcing errors where an agent "fixes" a bug by changing the test that caught it.

### Fresh context per phase = zero context drift

Every subagent starts with a clean context window containing only: the original task, the progress summary, and the specific phase instructions. No accumulated tool results, no stale code snippets, no prior phase artifacts in memory. Context drift is architecturally impossible.

### The state file is the single source of truth

`_orchestration_state.md` is the orchestrator's memory. It survives crashes, context compaction, and session boundaries. If you can read the state file, you can resume the pipeline from any point. No vector database, no RAG, no embeddings — just a file on disk.

### Crash recovery is the normal codepath

There is no "resume mode" vs "fresh mode". Every invocation reads the state file. If it exists, resume. If it doesn't, start fresh. Same pattern, no branching. This is the RelentlessAgent insight: the recovery path IS the happy path.

### Stuck detection beats loop counting

The circuit breaker (`remediate_max_loops`, default 3) is a safety net. The real signal is: did the error count decrease? If not, the remediator is failing — stop immediately. Don't burn compute on a problem that needs human judgment.

### Escalation is not failure

Escalating a permission error to the human is correct behavior. The orchestrator's job is to autonomously fix what it can and clearly surface what it can't. A report that says "10 errors fixed, 2 need your attention" is a successful orchestration.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Implement never reaches all gates | Check if gates are testing the right thing; some may need revision |
| Validator finds 0 errors but app is broken | Validation surfaces may be incomplete; add more endpoints/routes to PRD |
| Remediator breaks TDD gates | Regression check catches this; escalate |
| Circuit breaker fires on first loop | Errors may all be non-auto-fixable; check triage categories |
| Orchestrator runs out of context | Read `_orchestration_state.md` — it has everything needed to resume |
| `_validation_report.json` missing | Re-run validator — orchestrator will dispatch from current phase |
| State file corrupted | Delete it and re-invoke — orchestrator will re-assess from artifacts on disk |
