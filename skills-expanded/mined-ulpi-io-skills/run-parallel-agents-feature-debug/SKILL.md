---
name: run-parallel-agents-feature-debug
version: 2.0.0
description: |
  Diagnose and fix 3+ genuinely INDEPENDENT failures concurrently on Claude Code's real parallel
  agent runtime — without splitting one root cause into conflicting investigations. Proves the
  failures don't share a root cause (same dependency/config/migration/deploy across traces) before
  launching, matches each lane to the best specialized agent, briefs it with real evidence (failing
  output, stack traces, test names), launches all lanes in one message with background execution and
  worktree isolation, then reruns each original failure and conflict-checks the fixes. Refuses to
  parallelize fewer than 3 lanes or symptoms that may share a cause, consolidates lanes that
  converge on one root cause instead of claiming independent wins, and reports partial success
  honestly. Use when the user gives 3+ clearly independent failures to fix in parallel.
allowed-tools:
  - Agent
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
effort: high
argument-hint: "[debug request or problem set]"
arguments:
  - request
when_to_use: |
  Use when the user explicitly asks to debug or fix multiple unrelated issues in parallel, or there
  are 3 or more clearly independent failures that can be investigated separately. Do NOT use when
  symptoms may share a root cause (diagnose that first), when sequencing matters, for undecomposed
  problems, or to build features (run-parallel-agents-feature-build); confirm clustering first when
  independence is uncertain.
---

<EXTREMELY-IMPORTANT>
This skill orchestrates real Agent tool executions. Non-negotiable rules:
1. Prove the failures do not share a root cause before parallelizing them.
2. Write a complete prompt for every spawned agent because fresh `subagent_type` agents do not inherit task context.
3. Launch all parallel agents in a single assistant message with multiple `Agent(...)` tool uses.
4. Use `run_in_background: true` for independent debug lanes and do not poll background output.
5. Use `isolation: "worktree"` for debug lanes that may modify code.
</EXTREMELY-IMPORTANT>

# Run Parallel Agents Feature Debug

## Inputs

- `$request`: Optional problem set, failure list, or user direction such as `debug these three failing suites in parallel` or `split these bugs across agents`.

## Goal

Exploit Claude Code's real parallel agent runtime to diagnose and fix independent failures concurrently without splitting one root cause into multiple conflicting investigations.

## Step 0: Resolve the candidate debug lanes

Identify the failure set:

- explicit user bug list
- failing test groups
- broken subsystems
- grouped compile, lint, runtime, or performance failures

Then determine:

- failure count
- likely subsystem boundaries
- whether each failure is a symptom or a standalone issue
- whether the lanes are debug/fix work rather than planning or broad exploration

Do not use this skill if:

- there are fewer than 3 independent lanes
- the failures may share one root cause
- one broken dependency, config value, schema change, or deploy event could explain multiple symptoms
- the work still needs decomposition before execution

Use `AskUserQuestion` only if safe clustering depends on user clarification.

**Success criteria**: You have a concrete set of candidate debug lanes worth triaging for independence.

## Step 1: Prove independence and reject shared-root-cause traps

For each candidate lane, check:

- whether the failure started at the same time as other lanes
- whether the same dependency, config, migration, environment, or upstream service appears in multiple traces
- whether one fix could plausibly collapse several symptoms
- whether the write scope is disjoint if multiple lanes reach the fix stage

Parallelize only when:

- root cause is plausibly distinct
- reproduction is lane-local
- expected fixes do not overlap heavily

If there is meaningful doubt, do not parallelize yet. Diagnose the shared root cause first.

Load `references/debug_patterns.md` for root-cause heuristics and framework-specific failure patterns.
Load `references/agent-runtime-semantics.md` for the runtime rules that make or break parallel debug execution.

**Success criteria**: Every selected lane is likely independent at both diagnosis and fix time.

## Step 2: Match each debug lane to the right agent

Choose the most appropriate specialized agent for each lane based on:

- framework and language
- failing files and directories
- error signatures
- whether the lane is runtime, test, build, or performance focused

Load `references/agent_matching_logic.md` for detailed matching rules and edge cases.

Practical defaults:

- use the most specific framework/domain agent available
- use `general-purpose` only when no stronger fit exists
- do not invent agent types

**Success criteria**: Every lane has a justified debug agent assignment.

## Step 3: Build full debugging briefs

Because fresh `subagent_type` agents start without the main thread's task context, every prompt must contain:

- the exact problem statement
- the concrete error or symptom
- reproduction steps, if known
- affected files or directories
- likely scope boundaries
- what counts as success
- required verification command or test
- whether the lane should only diagnose or both diagnose and fix

Prefer real evidence over summaries:

- failing command output
- stack trace excerpts
- failing test names
- impacted file paths

Do not hand a fresh agent vague instructions like "fix this suite" without the actual failure surface.

**Success criteria**: Each lane prompt is complete enough for a fresh agent to diagnose without basic follow-up questions.

## Step 4: Launch all agents in one parallel batch

Launch every lane in a single assistant message containing multiple `Agent(...)` tool uses.

Required launch semantics for fix-capable debug lanes:

- `subagent_type`: matched agent type
- `description`: short 3-5 word description
- `prompt`: full debugging brief
- `run_in_background: true`
- `isolation: "worktree"`

Runtime-specific rules:

- do not split the launches across multiple assistant messages if the user asked for parallel debugging
- do not rely on target-agent defaults for async or isolation when parallel safety matters
- do not use read-only forks here; this skill is for fresh specialized debug agents

Load `references/agent-runtime-semantics.md` for the exact source-backed reasons behind these rules.

**Success criteria**: All independent debug lanes are launched concurrently with explicit, safe runtime settings.

## Step 5: Aggregate completions without polling

After launch:

- continue with non-overlapping coordination work
- wait for completion notifications instead of polling background transcripts
- trust returned agent summaries unless there is a concrete reason to inspect deeper

When each lane completes, capture:

- status
- diagnosed root cause
- files touched
- verification result
- blockers or unresolved scope

If a lane concludes the issue was not independent after all, stop pretending the original clustering was valid and reframe the remaining work.

**Success criteria**: Every spawned lane has a tracked outcome without unnecessary transcript noise.

## Step 6: Validate fixes and check for conflicts

Before treating the parallel debug session as complete:

- rerun the original failing test or validation command for each lane
- confirm the original symptom is actually gone
- check for overlapping file edits or contradictory fixes
- confirm one lane did not silently re-break another lane's subsystem

If conflicts exist:

- stop automatic aggregation
- identify the overlapping files or contradictory fixes
- merge intentionally or escalate to the user

If multiple lanes converged on the same root cause:

- say so explicitly
- consolidate the result instead of pretending they were independent wins

**Success criteria**: The final result reflects real fixes, not just parallel patch attempts.

## Step 7: Report the consolidated result

Summarize:

- which debug lanes ran
- which agents handled them
- root cause and fix status per lane
- verification result per lane
- conflicts, converged root causes, or remaining blockers

Be explicit about partial success. Debugging is only finished when the original failures are actually resolved or clearly re-scoped.

**Success criteria**: The user gets a concise but accurate parallel-debug summary.

## Guardrails

- Do not use this skill for fewer than 3 genuinely independent lanes.
- Do not parallelize symptoms that may share a root cause.
- Do not keep giant examples, scorecards, or framework catalogs inline in `SKILL.md`.
- Do not assume fresh agents know the surrounding task context.
- Do not poll or tail background agent output unless the user explicitly asks.
- Do not rely on default agent `background` or `isolation` settings when explicit launch parameters are safer.
- Do not add `disable-model-invocation`; this skill should remain available when the user asks for parallel debugging.
- Do not add `context: fork`; this workflow coordinates fresh specialized agents, not read-only skill forks.
- Do not add `paths:`; this is a generic orchestration skill.

## When To Load References

- `references/agent-runtime-semantics.md`
  Use for source-backed Agent runtime rules: fresh context, single-message parallel launch, background behavior, worktree isolation, and explicit parameter precedence.

- `references/debug_patterns.md`
  Use for shared-root-cause heuristics, framework-specific error patterns, and triage guidance.

- `references/agent_matching_logic.md`
  Use for detailed agent-selection rules and framework-specific edge cases.

## Output Contract

Report:

1. resolved debug lane set
2. agent assignment per lane
3. launch status
4. root cause and fix status per lane
5. verification results
6. conflicts, shared-cause discoveries, or remaining blockers
