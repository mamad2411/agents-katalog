---
name: ship-prd
description: >
  Kick off the agent swarm pipeline from prd/current.md. Reads the PRD,
  dispatches project-manager to seed _queue.json with track-tagged stories,
  then runs the autonomous pipeline (parallel batches, same as /next,
  including UX design and visual QA for ui/fullstack stories) until BLOCKED,
  all DONE, or stuck. Use when the user types /ship-prd or says "start the
  pipeline", "kick off the swarm", "process the PRD", "run autonomously from
  the PRD".
---

Read `CLAUDE.md` to refresh the orchestration rules and track routing. Then verify:

1. `prd/current.md` exists and is non-empty.
2. `stories/_queue.json` exists and contains an empty stories array.

If `prd/current.md` is missing, tell the user and stop.

If `_queue.json` is non-empty, ask the user whether to overwrite (start fresh) or merge
(decompose only the new sections of the PRD). Do not proceed without an answer.

If both conditions are clean, dispatch the `project-manager` subagent at **xhigh** effort
(Task `model`: `claude-opus-4-8[effort=xhigh]` or account-equivalent). Reinject identity:

> Identity: role_id=project-manager, marker=PM. Non-negotiables: do not invent PRD answers;
> tag every story backend|ui|fullstack; touch only stories/.
>
> Decompose `prd/current.md` into user stories, tagging each with a `track`
> (backend/ui/fullstack). Read `stories/_schema.json` before writing `stories/_queue.json`.
> Follow your subagent definition exactly. Surface any ambiguities as `questions_for_human`.
> End with the mandatory `<status>` block (`notes` must start with `PM:`).

After the project-manager returns, parse the `<status>` block, update `stories/_queue.json`
accordingly, and announce the queue state.

**Autonomous continuation:** Immediately run the **same autonomous pipeline loop** as the
`next` skill: keep dispatching in priority order with parallel batches (cap 7), track-routing
to the right implementer and through UX design / visual QA for `ui`/`fullstack` stories,
updating `_queue.json` after each batch, until BLOCKED, all `DONE`, or no dispatchable work.
Do **not** wait for a separate `/next` between stages.
