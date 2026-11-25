# Agent Team Builder (Claude Code)

This project builds **other** Claude Code agent-team projects — from a
conversation, not from a Python build step. You describe a team; this workspace
designs the roster, makes the hire / no-hire calls, and writes the project.

You (the main Claude Code session) are the **build orchestrator**. The role
design and hiring judgment are delegated to the `team-architect` subagent.

## How to build a team

Run `/new-team <description of the team and its goal>`.

The flow:

1. Read `reference/conventions.md` and `reference/templates.md`.
2. Delegate to the `team-architect` subagent with the description. It returns a
   proposed roster (each role with tools + prompt), the loop, and the memory
   plan — and the hire / no-hire reasoning behind the roster.
3. **Present the plan to the human and STOP.** Do not write files until approved.
4. On approval, write the project under `teams/<slug>/`, following
   `reference/templates.md` exactly.

To review an existing team's roster, run `/audit-team teams/<slug>`.

## Non-negotiable rules for every generated team

These come from `reference/conventions.md` — read it, don't paraphrase from
memory:

- Context isolation: each role is its own subagent; hand off via files, never
  shared context.
- File-based memory: a `state/` blackboard, durable vs working, read at session
  start, no chat replay.
- Human-approval gate: no generated agent or script posts, sends, authenticates,
  or does anything irreversible without a human.
- Least-privilege tools per agent.
- Every generated team includes a `recruiter` agent for role gaps found at run
  time (see the recruiter template).
- Every generated team can remember standing instructions across restarts:
  `state/standing-orders.md` + a `/remember` command + a `SessionStart` hook that
  reloads it (see the standing-instructions template).

## What this is not

This is the conversational counterpart to the Python `agent-team-forge`
generator. Use this when you want Claude Code to design a team for you; use forge
when you want a deterministic, testable, CI-able build from a fixed spec. You can
also do both: draft here, then freeze the result into a forge spec for
reproducible regeneration.
