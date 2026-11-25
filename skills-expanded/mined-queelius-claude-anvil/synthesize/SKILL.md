---
name: synthesize
description: >-
  Make a research-agent run conclude and write synthesis.md (outcome, key
  findings, failed approaches, open questions, recommendations). Signals a
  live researcher to wrap up, or launches one in synthesis mode when none is
  running. Use when results are good enough or the agent is stalling.
argument-hint: "[branch-name]"
---

# Synthesize Research

Conclude the research run per: $ARGUMENTS

A main-line synthesis also compares all branches. Naming a branch concludes only that branch (output: `.research/branches/<name>/synthesis.md`).

## When to use

- Current results are good enough; lock them in
- The agent is stalling (eval flat or declining for several cycles)
- A deadline forces a conclusion regardless of completeness
- The user wants a checkpoint before pivoting to a related research line

## Step 1: Resolve the Run Root

- With a branch name, the run root is `.research/branches/<name>/`; it must exist (Glob tool).
- Otherwise the run root is `.research/`.
- `.research/goal.md` marks a research run. If it is absent, tell the user there is nothing to synthesize and suggest `/research-agent:research`. A missing state.md is fine: the researcher reconstructs from log.md.

## Step 2: If a Researcher Is Live, Signal It

Read `<run root>/run.json` if present. The run is **live** when `status` is `running` or `stopping` and `heartbeat` is less than `stale_after_minutes` old (compare against `date -u +%Y-%m-%dT%H:%M:%SZ`).

- `status: stopping` and live: a stop is already pending. Tell the user and stop.
- `status: running` and live: change only that field with the Edit tool, `"status": "running"` to `"status": "stopping"`. Do NOT launch a second researcher. Tell the user:

  > Stop requested. The live researcher will finish its current step, settle its background jobs, and write `{run root}/synthesis.md` itself at its next cycle boundary. `/research-agent:status` shows when `status` becomes `concluded`.

  Then stop; skip the remaining steps.

## Step 3: Check Whether Already Synthesized

If `<run root>/synthesis.md` exists, ask the user whether to re-synthesize (the agent archives the old file as `synthesis-<timestamp>.md`) or stop.

## Step 4: Launch the Researcher in Synthesis Mode

Spawn the researcher (Agent tool, `subagent_type: research-agent:researcher`) with only these tags; the agent's synthesize-mode initialization defines the steps:

    <mode>synthesize</mode>
    <branch>{name}</branch>        (only when concluding a branch)
    <working_directory>
    {absolute path to current working directory}
    </working_directory>

## Step 5: Inform the User

> Researcher synthesizing. It will finalize statuses and write {run root}/synthesis.md without starting new attempts.
