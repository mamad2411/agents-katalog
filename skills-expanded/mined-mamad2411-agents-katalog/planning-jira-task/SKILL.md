---
name: "planning-jira-task"
description: 'Plan HOW to execute a single task from a Jira task plan. Runs a pipeline of specialist subagents: pre-execution setup (branch, Jira transition, execution brief), codebase analysis and execution planning, behaviour-driven test specification, and refactoring evaluation. Produces all planning artifacts needed before implementation begins. Use when the user says "plan task 3", "prepare task 2 for execution", "how should we implement task 1", or when the orchestrating-jira-workflow skill invokes Phase 5 of the pipeline. Requires that the task plan exists at docs/<TICKET_KEY>-tasks.md. Plans ONLY the specified task — produces planning artifacts but does NOT implement anything. After this skill completes, the clarifying-assumptions skill should be invoked to critique the plan before execution begins.'
---

# Planning Jira Task

## Purpose

Plan exactly HOW to execute ONE task from the task plan. This skill runs a
pipeline of specialist subagents that analyse the task, inspect the codebase,
and produce detailed planning artifacts: an execution brief, an execution
plan with recommended skills and approach, a behaviour-driven test
specification, and a refactoring evaluation.

These artifacts are then critiqued by the `clarifying-assumptions` skill
(Phase 6) before any implementation begins. This separation ensures that
approach decisions — framework choices, library selections, architectural
patterns — are challenged and confirmed before code is written.

This skill produces planning artifacts ONLY. It does NOT implement anything.
Implementation is handled by the `executing-jira-task` skill (Phase 7).

## Platform Compatibility

This skill works across multiple AI coding tools. Each platform uses a
different syntax for dispatching subagents:

| Platform        | Dispatch syntax                                                     |
| --------------- | ------------------------------------------------------------------- |
| Claude Code CLI | `agent <subagent-name> "<prompt>"` — native subagent via Agent tool |
| Cursor IDE      | Place `.md` files in `.cursor/agents/` or `@`-mention the subagent  |
| OpenCode CLI    | Subagents invoked via Task tool or `@`-mention in messages          |

All three platforms support the Agent Skills open standard (SKILL.md format).
The subagent files are self-contained markdown — each platform discovers and
dispatches them using its own native mechanism.

If your platform does not support native subagent dispatch, read the subagent
file and execute its instructions directly, keeping the subagent's output
contract intact so downstream steps can consume it.

## Inputs

| Input         | Source              | Required | Example    |
| ------------- | ------------------- | -------- | ---------- |
| `TICKET_KEY`  | User / `$ARGUMENTS` | Yes      | `JNS-6065` |
| `TASK_NUMBER` | User / `$ARGUMENTS` | Yes      | `3`        |

Both the ticket snapshot (`docs/<TICKET_KEY>.md`) and the task plan
(`docs/<TICKET_KEY>-tasks.md`) must exist. If either is missing, tell the user
which prerequisite skill to run.

### Input contract (produced by upstream skills)

The task plan file `docs/<TICKET_KEY>-tasks.md` must contain these sections,
built up across the preceding phases:

| Required section / element                  | Produced by                | Used in step        | Why                                              |
| ------------------------------------------- | -------------------------- | ------------------- | ------------------------------------------------ |
| `## Task <N>:` with all 8 subsections       | planning-jira-tasks        | Step 1 (load)       | Source content for the execution brief           |
| `## Dependency Graph`                       | planning-jira-tasks        | Step 1 (pre-flight) | Validates dependencies are satisfied             |
| `## Decisions Log`                          | clarifying-assumptions     | Step 1 (brief)      | Resolved decisions folded into execution context |
| Per-task `Questions to answer` resolved     | clarifying-assumptions     | Step 1 (pre-flight) | Pre-flight checks all questions are answered     |
| `## Jira Subtasks` table with keys          | creating-jira-subtasks     | Step 1 (Jira)       | Maps task number to Jira subtask key for status  |
| `Jira Subtask: <KEY>` in each task section  | creating-jira-subtasks     | Step 1 (Jira)       | Identifies which Jira issue to transition        |
| `**Status:**` on previously completed tasks | executing-jira-task (self) | Step 1 (pre-flight) | Checks whether dependencies are marked complete  |

**Pre-flight gate:** If the `## Jira Subtasks` table is missing, subtasks were
not created in Jira. Warn the user and ask whether to proceed without Jira
integration or run the creating-jira-subtasks skill first. This is a warning,
not a hard block — execution can proceed without Jira tracking.

## Subagent Registry

| Subagent              | Path                                 | Purpose                                                                                         |
| --------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------------- |
| `execution-prepper`   | `./subagents/execution-prepper.md`   | Pre-execution: validates task, sets up branch, transitions Jira to In Progress, assembles brief |
| `execution-planner`   | `./subagents/execution-planner.md`   | Analyses the task, inspects the codebase, and produces an execution plan with skills            |
| `test-strategist`     | `./subagents/test-strategist.md`     | Defines behaviour-driven tests based on business requirements, not implementation               |
| `refactoring-advisor` | `./subagents/refactoring-advisor.md` | Evaluates whether existing code needs refactoring before or during task execution               |

Before delegating, read the subagent file to understand its contract (expected
input format, output format, and rules). The path is relative to this skill's
directory.

### Skill Dependencies

All subagents depend on external skills that **must** be installed before
execution. These are validated by the orchestrator's `preflight-checker`
before execution begins AND by each subagent at runtime (defense-in-depth).

**If any skill is missing**, the subagent will STOP immediately and report
the missing skill to the orchestrator. The orchestrator will then prompt the
user to install the skill and re-dispatch the subagent from the beginning.
There is no fallback behavior — all skills are required.

| Subagent              | Depends on                 | Level    | Install command                                           |
| --------------------- | -------------------------- | -------- | --------------------------------------------------------- |
| `execution-planner`   | `/find-skills`             | Required | `skills install vercel-labs/skills/find-skills`           |
| `execution-planner`   | `/writing-plans`           | Required | `skills install obra/superpowers/writing-plans`           |
| `test-strategist`     | `/writing-plans`           | Required | `skills install obra/superpowers/writing-plans`           |
| `test-strategist`     | `/test-driven-development` | Required | `skills install obra/superpowers/test-driven-development` |
| `test-strategist`     | `/vitest`                  | Required | `skills install antfu/skills/vitest`                      |
| `refactoring-advisor` | `/writing-plans`           | Required | `skills install obra/superpowers/writing-plans`           |

## Output

Planning artifacts written to disk (persisted, never deleted, never committed
to git):

| Artifact                                  | Produced by           | Consumed by                                                   |
| ----------------------------------------- | --------------------- | ------------------------------------------------------------- |
| `docs/<KEY>-task-<N>-brief.md`            | `execution-prepper`   | All downstream subagents, critique-analyzer                   |
| `docs/<KEY>-task-<N>-execution-plan.md`   | `execution-planner`   | test-strategist, refactoring-advisor, task-executor, critique |
| `docs/<KEY>-task-<N>-test-spec.md`        | `test-strategist`     | refactoring-advisor, task-executor, critique                  |
| `docs/<KEY>-task-<N>-refactoring-plan.md` | `refactoring-advisor` | task-executor, critique                                       |

**Artifact preservation rule:** These files are NEVER deleted. They persist
for the lifetime of the workflow. They are NEVER committed to git — they are
orchestration artifacts, not implementation output.

**On re-plan cycles:** If Phase 6 critique triggers a re-plan, these files
are overwritten with updated versions. The subagents receive both the prior
artifact (already on disk) and the new decisions from the critique. They
produce an updated artifact that reflects the new decisions while preserving
any work that was not affected by the change.

### Output contract (consumed by downstream skills)

| Artifact                | Consumed by                    | Why                                                 |
| ----------------------- | ------------------------------ | --------------------------------------------------- |
| Execution brief         | executing-jira-task            | Self-contained context for implementation           |
| Execution plan          | executing-jira-task            | Approach, skills, file-level strategy               |
| Test specification      | executing-jira-task            | Behavioural tests the executor must implement       |
| Refactoring plan        | executing-jira-task            | Pre-implementation refactoring to apply             |
| All four artifacts      | clarifying-assumptions (Ph. 6) | Critique-analyzer reviews for bias and alternatives |
| Per-task decisions file | self (on re-plan)              | Subagents know what changed on re-dispatch          |

---

## Execution Steps

### 1. Dispatch: Execution Prepper

Read `./subagents/execution-prepper.md` and dispatch the execution-prepper
subagent with:

- `TICKET_KEY`
- `TASK_NUMBER`
- `BRANCH_OVERRIDE` (if the orchestrator or user specified a branch name)

The execution-prepper handles four setup steps in one dispatch:

1. **Validates the task** — checks that the task exists, dependencies are
   marked complete, and all questions are resolved.
2. **Ensures the working branch** — checks current branch, creates or switches
   to the feature branch, stashes uncommitted changes if needed.
3. **Transitions the Jira subtask to "In Progress"** — if the subtask key
   and Jira MCP are available. Skips silently if not.
4. **Assembles the execution brief** — reads the task plan and Decisions Log,
   builds a self-contained brief, writes it to
   `docs/<TICKET_KEY>-task-<N>-brief.md`.

Collect its output as the `PREP_SUMMARY`.

**If pre-flight FAIL:** The subagent reports what needs resolution (unsatisfied
dependencies or unresolved questions). Relay this to the user and stop — do
not proceed to the planning pipeline.

**If an existing ticket branch was found:** The subagent notes this. Ask the
user whether to reuse the existing branch or create a new task-level branch.
If the user chooses to reuse, re-dispatch with the branch name as
`BRANCH_OVERRIDE`.

**If changes were stashed:** Inform the user that uncommitted changes were
stashed and will need to be popped later.

After the prep summary confirms PASS, proceed to step 2 using the brief file
path from the summary.

### 2. Dispatch: Execution Planner

Read `./subagents/execution-planner.md` and dispatch the execution-planner
subagent with the execution brief path.

The execution-planner will:

- Read the `## Problem Framing` section and Phase 3 decisions from
  `docs/<TICKET_KEY>-tasks.md` to understand the end user and their need.
- Analyse the task and the relevant parts of the codebase.
- Use the `/find-skills` skill to identify the best available skills for the
  task.
- Produce a structured execution plan with recommended skills, approach,
  file-level strategy, and a **User Impact Assessment** connecting every major
  implementation decision to its consequence for the end user.
- **Write the plan to `docs/<TICKET_KEY>-task-<N>-execution-plan.md`.**

The User Impact Assessment feeds into Phase 6 critique, where the developer
evaluates whether each user-facing trade-off is acceptable given the Problem
Framing context established in Phase 3.

Collect its output as the `EXECUTION_PLAN_SUMMARY`.

**On re-plan:** If this is a re-dispatch after Phase 6 critique, pass the
path to the per-task decisions file (`docs/<KEY>-task-<N>-decisions.md`) as
additional context. The planner reads the prior decisions and adjusts its
plan accordingly without starting from scratch.

### 3. Dispatch: Test Strategist

Read `./subagents/test-strategist.md` and dispatch the test-strategist
subagent with the execution brief path and the execution plan path.

The test strategist will:

- Analyse the business requirements from the execution brief.
- Define a list of behaviour-driven tests (not implementation-detail tests).
- Produce a test specification that the task-executor will implement.
- **Write the spec to `docs/<TICKET_KEY>-task-<N>-test-spec.md`.**

Collect its output as the `TEST_SPEC_SUMMARY`.

**On re-plan:** Pass the per-task decisions file as additional context.

### 4. Dispatch: Refactoring Advisor

Read `./subagents/refactoring-advisor.md` and dispatch the refactoring-advisor
subagent with the execution brief path, execution plan path, and test spec
path.

The refactoring advisor will:

- Evaluate whether existing code needs changes to accommodate the task cleanly.
- Identify refactoring opportunities that prevent code rot.
- Produce a refactoring recommendation (which may be "no refactoring needed").
- **Write the plan to `docs/<TICKET_KEY>-task-<N>-refactoring-plan.md`.**

Collect its output as the `REFACTORING_SUMMARY`.

**On re-plan:** Pass the per-task decisions file as additional context.

### 5. Report to user

```
Task <N> planning complete: <Title>

Planning artifacts produced:
- Brief: docs/<KEY>-task-<N>-brief.md
- Execution plan: docs/<KEY>-task-<N>-execution-plan.md
- Test spec: docs/<KEY>-task-<N>-test-spec.md
- Refactoring plan: docs/<KEY>-task-<N>-refactoring-plan.md

Key decisions made by the planners:
- Approach: <1-2 sentences on the recommended approach>
- Skills: <skills recommended by the execution-planner>
- Tests: <N behaviour-driven tests defined>
- Refactoring: <what was recommended, or "none needed">

These artifacts will now be critiqued before implementation begins.
```

## Re-Plan Cycle

When Phase 6 critique triggers a re-plan, the orchestrator re-dispatches
this skill with the same `TICKET_KEY` and `TASK_NUMBER`, plus:

- `RE_PLAN=true` — signals this is a re-dispatch
- `DECISIONS_FILE=docs/<KEY>-task-<N>-decisions.md` — the per-task decisions
  file containing the user's resolved decisions from the critique

On re-plan:

1. **All four subagents are re-dispatched.** Even if only the execution plan
   was invalidated, all subagents re-run to ensure consistency.
2. **Each subagent receives its prior artifact** (already on disk) plus the
   decisions file. It updates its output based on the new decisions while
   preserving unaffected work.
3. **Artifact files are overwritten** with the updated versions.
4. **The orchestrator informs the user** about what changed in this iteration.

**Maximum re-plan cycles:** 3 iterations. If Phase 6 critique still has
unresolved HIGH-severity concerns after 3 cycles, escalate to the user with
the accumulated critique and ask how to proceed.

## Safety Rules

- **Planning only.** This skill produces planning artifacts. It does NOT
  implement anything, write tests, modify source code, or make commits.
- **Scope discipline.** Plan only what is needed for the specified task.
  Do not plan for future tasks or suggest scope expansion.
- **Fail loudly.** If any subagent encounters ambiguity or a blocker, surface
  it to the user immediately rather than making assumptions.
- **Respect the pipeline order.** Do not skip subagent steps or reorder them.
  Each step depends on the output of the previous one.
- **Preserve artifacts.** Planning artifacts are NEVER deleted and NEVER
  committed to git.

## Handling BLOCKED Verdicts (Missing Required Skills)

Every subagent checks for its required skills as its absolute first step
(defense-in-depth). If a subagent returns a `BLOCKED — MISSING REQUIRED
SKILL` verdict:

1. **Do NOT proceed** to the next pipeline step. The blocked subagent's
   output is required by downstream steps.
2. **Present the missing skill(s)** to the user with install commands from
   the subagent's report.
3. **Wait for the user** to confirm the skill(s) have been installed.
4. **Re-dispatch the blocked subagent from the beginning.** Do not attempt
   to resume from a partial state — the subagent performs no work before
   the skill check, so there is nothing to resume.

```
⚠️ Missing required skill — pipeline paused

The <subagent-name> subagent requires the following skill(s):

- `/<skill-name>` — <purpose>
  Install: `skills install <path>`

Please install the skill(s) and let me know when ready to continue.
```

After the user confirms installation, re-dispatch the same subagent with the
same inputs it was originally given.
