---
name: model-delegation
description: Initiate the orchestrator-worker cost model for this session. The main-loop model (expensive, metered) orchestrates, specs, verifies, and validates only; ALL drafting and mechanical work (code, docs, tests, sweeps, research) runs in Opus 4.8 subagents billed to plan allowance. Invoke at session start or whenever token cost matters.
author: Erhan Tezakar
---

# Model delegation (orchestrator thinks, workers write)

Purpose: when the main-loop model bills to metered usage credits and
subagent models bill to a subscription plan, the expensive model must never
do the writing. Output tokens are the costly side; drafting is output-heavy;
verification is read-heavy. So the orchestrator reads and decides, the
workers write.

On invocation, adopt this operating mode for the rest of the session.

## Model policy

| model | role | billing |
|---|---|---|
| main loop (e.g. Fable 5) | decompose, spec, review, validate, decide, talk to the user | metered credits, minimize output |
| opus-4.8 subagents | write code/docs/tests, mechanical sweeps, research, exploration | plan allowance |
| sonnet / haiku | never, regardless of task size | - |

These are defaults with one standing override: if a worker's output does not
meet the bar after one revision round, the orchestrator redoes that piece
itself. Judge the output, not the price tag; escalating costs less than
shipping mediocre work.

## Mechanics

- Spawn workers via the Agent tool with `model: "opus"`. Choose
  `subagent_type` per task: `general-purpose` for implementation, `Explore`
  for read-only search, `Plan` for design drafts.
- Independent tasks launch in ONE message so they run in parallel.
- Workers mutating files in parallel get `isolation: "worktree"`.
- Continue an existing worker with SendMessage instead of re-spawning; a
  fresh Agent call starts with zero context.
- Multi-agent Workflow runs only when the user opts in; pin `model: "opus"`
  on every agent there too.

## Division of labor

The orchestrator keeps for itself, and ONLY these:

- task decomposition and the self-contained spec each worker receives
- verification and validation of returned work
- decisions, trade-offs, and everything the user reads
- tiny surgical edits where writing a spec would cost more than the edit

Workers do everything else, including first drafts of user-facing copy;
the orchestrator reviews for taste before it ships.

## Spec quality (the leverage point)

A worker gets NO conversation context. Every spawn prompt must carry:

- absolute paths: files to read first, files to produce or modify
- exact requirements, interfaces, and edge cases, not vibes
- the project rules that bind the work (style, frozen paths, wording rules,
  locale obligations, anything the repo's own docs declare binding)
- an explicit boundary: which files or directories must NOT be touched
- what to return: a terse factual report (files touched, decisions made,
  anything skipped or deviated), never prose

## Verification ladder (cheap before expensive)

1. Free local checks first: syntax checks, linters, test suites, grep
   residue scans, schema applies against a scratch database.
2. Targeted reads of the critical hunks (money paths, auth gates, anything
   the spec marked sensitive), not whole-file re-reads.
3. Full orchestrator re-read only for billing-critical, locked, or
   client-served surfaces.
4. Functional equivalence tests where two implementations must agree
   (derivations, protocol counterparts): prove it with a script, not by
   eyeballing.
5. Failing work gets ONE revision round via SendMessage with the precise
   defects listed; still failing, the orchestrator redoes it.

## Reporting

The user-facing summary states what was delegated, what was verified and
how, and anything corrected. Worker claims are never presented as fact
until verified. Token usage of workers is reported when the user is
watching costs.
