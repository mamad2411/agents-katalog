---
name: run-parallel-agents-feature-build
version: 2.0.0
description: |
  Run 3+ genuinely INDEPENDENT build tasks concurrently on Claude Code's real parallel agent runtime
  — throughput without file conflicts or fake orchestration. Proves independence (disjoint write
  scope, no dependency edges) before launching, matches each lane to the best specialized agent,
  writes a complete self-contained brief per fresh agent, launches them all in one message with
  background execution and worktree isolation, then conflict-checks and reviews each finished lane
  before treating it as merged. Refuses to parallelize fewer than 3 lanes or lanes that share write
  scope or dependencies, never assumes fresh agents inherit context, and reports partial success per
  lane rather than a blurred merged summary. Use when an approved plan or the user gives 3+
  independent build lanes.
allowed-tools:
  - Agent
  - Skill
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
effort: high
argument-hint: "[plan path or parallel-build request]"
arguments:
  - request
when_to_use: |
  Use when the user explicitly asks to build in parallel, split execution across agents, or an
  approved task list has 3 or more independent implementation lanes. Do NOT use for research or
  debugging (run-parallel-agents-feature-debug), for tightly coupled work that shares files, state,
  or sequencing, or for fewer than 3 lanes — just do those inline; confirm the decomposition first
  when parallel safety is ambiguous.
---

<EXTREMELY-IMPORTANT>
This skill orchestrates real Agent tool executions. Non-negotiable rules:
1. Verify independence before launching anything.
2. Write a complete prompt for every spawned agent because fresh `subagent_type` agents do not inherit task context.
3. Launch all parallel agents in a single assistant message with multiple `Agent(...)` tool uses.
4. Use `run_in_background: true` for independent lanes and do not poll or tail background output.
5. Use `isolation: "worktree"` for code-writing lanes unless the task is explicitly read-only.
</EXTREMELY-IMPORTANT>

# Run Parallel Agents Feature Build

## Inputs

- `$request`: Optional plan path, task selection, or user direction such as `execute layer 0 from .ulpi/plans/foo.json` or `build these three features in parallel`.

## Goal

Exploit Claude Code's real parallel agent runtime to execute independent build tasks concurrently without file conflicts, missing context, or fake orchestration.

## Step 0: Resolve the candidate work set

Identify the source of truth for the work:

- an approved DAG plan
- an explicit user task list
- a clearly decomposed set of independent implementation lanes

Then determine:

- task count
- dependency edges
- write scope overlap
- whether each lane is build work rather than research or debugging

Do not use this skill if:

- there are fewer than 3 independent lanes
- any lane depends on another lane's result
- multiple lanes write the same file or the same narrow subsystem surface
- the task is still at planning or exploration stage

Use `AskUserQuestion` only if the decomposition is ambiguous and safe parallelization depends on a user choice.

**Success criteria**: You have a concrete set of parallel-safe build lanes.

## Step 1: Prove independence, do not assume it

For each candidate lane, verify:

- required inputs are already available
- no output from another lane is needed first
- write scope is disjoint
- validation can be run per lane or after merge without ambiguity

If a plan exists, treat its dependency graph and write scope as the primary source.

If there is no plan, derive equivalent temporary structure:

- lane name
- scope
- expected files
- acceptance criteria
- validation command

Load `references/agent-runtime-semantics.md` for the runtime rules that make or break parallel execution.

**Success criteria**: Every lane is independently executable without merge-race risk.

## Step 2: Match each lane to the right agent

Choose the most appropriate specialized agent for each lane based on:

- repository technology
- target files and directories
- framework-specific patterns
- whether the work is implementation or general support

Load `references/agent_matching_logic.md` for detailed matching rules and edge cases.

Practical defaults:

- use the most specific framework/domain agent available
- use `general-purpose` only when no stronger fit exists
- do not invent agent types

**Success criteria**: Every lane has a justified agent assignment.

## Step 3: Build full agent briefs

Because fresh `subagent_type` agents start without the main thread's task context, every prompt must contain:

- exact scope
- why this task exists
- files or directories to inspect
- write scope
- constraints and patterns to follow
- acceptance criteria
- validation command
- explicit instruction whether the lane should write code or only investigate

If the work came from a DAG plan, preserve:

- task ID
- acceptance criteria
- write scope
- validation command
- review requirement

If the task is identity, routing, registry, or isolation sensitive, require the lane to use `references/task-exit-gate.md` before declaring completion.

**Success criteria**: Each lane prompt is complete enough for a fresh agent to act without asking basic clarifying questions.

## Step 4: Launch all agents in one parallel batch

Launch every lane in a single assistant message containing multiple `Agent(...)` tool uses.

Required launch semantics for code-writing lanes:

- `subagent_type`: matched agent type
- `description`: short 3-5 word description
- `prompt`: full task brief
- `run_in_background: true`
- `isolation: "worktree"`

Runtime-specific rules:

- do not send the agent launches across multiple assistant messages if the user asked for parallel work
- do not rely on agent defaults for async or isolation when code-writing safety matters
- do not use read-only forks here; this skill is for fresh specialized build agents

Load `references/agent-runtime-semantics.md` for the exact source-backed reasons behind these rules.

**Success criteria**: All independent lanes are launched concurrently with explicit, safe runtime settings.

## Step 5: Aggregate completions without polling

After launch:

- continue with non-overlapping coordination work
- wait for completion notifications rather than polling background transcripts
- trust the returned agent summaries unless there is a concrete reason to inspect deeper

When each lane completes, capture:

- status
- files touched
- validation result
- blockers or deviations from brief

If a lane is blocked, do not hide it inside a merged success summary.

**Success criteria**: Every spawned lane has a tracked outcome without unnecessary transcript noise.

## Step 6: Review, conflict check, and closeout

Before treating a lane as merged:

- check for write-scope conflicts across finished lanes
- if the plan specifies a `review` field, invoke the corresponding review skill:
  - `codex` → `codex-review`
  - `claude` → `claude-review`
  - `kiro` → `kiro-review`
- if the lane came from a structured task plan, require the lane to satisfy `references/task-exit-gate.md`

If conflicts exist:

- stop automatic aggregation
- identify the overlapping files
- merge intentionally or escalate to the user

**Success criteria**: Finished lanes are reviewed and conflict-checked before being treated as complete.

## Step 7: Report the consolidated result

Summarize:

- which lanes ran
- which agents handled them
- completion status per lane
- files or areas changed
- reviews performed
- remaining blockers or follow-up sequencing

Be explicit about partial success. Parallel execution is only a win if the user can see which lanes are actually done.

**Success criteria**: The user gets a concise but accurate parallel-execution summary.

## Guardrails

- Do not use this skill for fewer than 3 genuinely independent lanes.
- Do not parallelize tasks with shared write scope or dependency edges.
- Do not keep giant agent catalogs or launch templates inline in `SKILL.md`.
- Do not assume fresh agents know the surrounding task context.
- Do not poll or tail background agent output unless the user explicitly asks.
- Do not rely on default agent `background` or `isolation` settings when explicit launch parameters are safer.
- Do not add `disable-model-invocation`; this skill should remain available when the user asks for parallel execution.
- Do not add `context: fork`; this workflow coordinates fresh specialized agents, not read-only skill forks.
- Do not add `paths:`; this is a generic orchestration skill.

## When To Load References

- `references/agent-runtime-semantics.md`
  Use for source-backed Agent runtime rules: fresh context, single-message parallel launch, background behavior, worktree isolation, and explicit parameter precedence.

- `references/agent_matching_logic.md`
  Use for detailed agent-selection rules and framework-specific edge cases.

- `references/task-exit-gate.md`
  Use when the task came from a structured plan with acceptance criteria, write scope, and validation requirements.

## Output Contract

Report:

1. resolved parallel lane set
2. agent assignment per lane
3. launch status
4. completion and review status per lane
5. conflicts, blockers, or remaining sequential work
