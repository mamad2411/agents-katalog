---
name: resume
description: >-
  Resume an interrupted research-agent run from .research/. Re-launches the
  researcher to reload its structured state and continue from the current
  focus, optionally on a named branch or with a new budget. Use after a
  session restart, crash, or explicit pause.
argument-hint: "[branch-name] [budget: N cycles, H hours]"
---

# Resume Research

Resume the research run per: $ARGUMENTS

## Step 1: Resolve the Run Root

- If the user names a branch, the run root is `.research/branches/<name>/`; it must exist (Glob tool).
- Otherwise the run root is `.research/`.
- `.research/goal.md` marks a research run. If it is absent, there is nothing to resume: suggest `/research-agent:research`.

Parse an optional new budget (cycle cap and/or hours). Without one, the agent keeps the budget persisted in the run root's `run.json`.

## Step 2: Refuse if a Researcher Is Live

Read `<run root>/run.json` if present. The run is **live** when `status` is `running` or `stopping` and `heartbeat` is less than `stale_after_minutes` old (compare against `date -u +%Y-%m-%dT%H:%M:%SZ`). If live, do not launch a second researcher: tell the user one is already working (with the heartbeat age) and point at `/research-agent:status` or `/research-agent:synthesize`. The single exception: the user states the earlier session is gone (for example, it was closed moments ago) and confirms they want to proceed (AskUserQuestion).

## Step 3: Handle a Concluded Run

If `<run root>/synthesis.md` exists, the run has concluded. Ask the user (AskUserQuestion) whether to reopen it. On yes, include `<reopen/>` in the launch prompt (the agent archives the old synthesis); suggest a larger budget if the previous one ran out. On no, point at synthesis.md and stop.

## Step 4: Preview

Show a one-paragraph preview of what the researcher will pick up:

> Resuming research on "{goal}". Current focus: {current_focus}. Last cycle was {N} on {date}: {modality} -> {result}. Open sub-problems: {count}. Untested hypotheses: {count}. Budget: {used}/{max} cycles.

Sources, structured first:
- goal: the body of `.research/goal.md` (below its frontmatter)
- current focus and counts: the YAML frontmatter of `<run root>/state.md`
- last cycle: the last line of `<run root>/cycles.jsonl`
- budget: `<run root>/run.json`

Legacy fallback (a run from an older plugin version: state.md without frontmatter, or no cycles.jsonl): use the prose "Current focus" section of state.md and the last `### Cycle` entry of log.md, and note that the researcher will migrate the run to the structured format. If state.md is missing entirely, say the researcher will rebuild it from goal.md and log.md.

## Step 5: Launch the Researcher

Spawn the researcher (Agent tool, `subagent_type: research-agent:researcher`) with only these tags; the agent's resume-mode initialization defines the steps:

    <mode>resume</mode>
    <branch>{name}</branch>                       (only when resuming a branch)
    <budget max_cycles="{N}" max_hours="{H}"/>    (only when the user gave a new budget)
    <reopen/>                                     (only when the user confirmed a reopen)
    <working_directory>
    {absolute path to current working directory}
    </working_directory>

Do not pass `isolation`: a resumed branch reuses the worktree recorded in its run.json.

## Step 6: Inform the User

> Researcher resumed from {run root}. Use `/research-agent:status` to check progress, or `/research-agent:synthesize` to ask it to conclude.
