---
name: research
description: >-
  Launch an autonomous research agent that iterates toward a goal through
  proofs, code, simulations, tests, and counterexample search.
  Fire-and-forget: the agent runs on its own and writes all results to
  .research/ in the target project.
argument-hint: "<goal> [eval script at <path>] [budget: N cycles, H hours]"
---

# Autonomous Research Agent

Launch the researcher on: $ARGUMENTS

## Step 1: Parse the Request

Extract from the arguments (or the user's message):

1. **Goal** (required): the natural-language research objective, the main content of the request.
2. **Eval script** (optional): a path to an executable script ("eval script at ...", "use ... as eval", or a path ending in `.sh`, `.py`, or similar).
3. **Budget** (optional): a cycle cap and/or a wall-clock cap ("at most 30 cycles", "stop after 4 hours"). Omitted means unbounded; the agent still concludes on its own stall rule.

If the goal is unclear, ask the user to clarify before proceeding. If no eval script is mentioned, the agent self-evaluates.

## Step 2: Verify Eval Script (if provided)

Verify the path exists (Read tool). If it does not, tell the user and ask whether to proceed with self-evaluation instead.

## Step 3: Check for an Existing Run

If `.research/` exists in this directory (Glob tool), do not launch fresh:

- Read `.research/run.json` if present. The run is **live** when `status` is `running` or `stopping` and `heartbeat` is less than `stale_after_minutes` old (compare against `date -u +%Y-%m-%dT%H:%M:%SZ`). If live, refuse: another researcher is working here. Point at `/research-agent:status` and `/research-agent:synthesize`. Never archive a live run.
- Otherwise offer `/research-agent:resume` to continue it, or archiving it before starting fresh. Archive only on the user's explicit confirmation, with Bash: `mkdir -p .research-archive && mv .research .research-archive/<UTC-timestamp>`.

The agent itself refuses to start a fresh run on top of an existing `.research/`.

## Step 4: Launch the Agent

Spawn the researcher (Agent tool, `subagent_type: research-agent:researcher`) with:

    <goal>
    {the user's research goal, verbatim}
    </goal>

    <eval>
    {path to eval script, or "none - use self-evaluation"}
    </eval>

    <budget max_cycles="{N}" max_hours="{H}"/>   (omit the tag, or either attribute, when not given)

    <working_directory>
    {absolute path to current working directory}
    </working_directory>

    Begin your research per your fresh-mode initialization.

Then inform the user:

> Research agent launched. It works autonomously in this directory, writing progress to `.research/`. When it finishes, the synthesis will be at `.research/synthesis.md`.
>
> While it runs:
> - `/research-agent:status` shows cycle progress, current focus, budget, and eval trend (read-only)
> - `/research-agent:synthesize` asks it to wrap up and write the synthesis now
> - `/research-agent:resume` continues the run after an interruption or session restart
> - `/research-agent:branch <name> [focus]` forks a competing strategy
