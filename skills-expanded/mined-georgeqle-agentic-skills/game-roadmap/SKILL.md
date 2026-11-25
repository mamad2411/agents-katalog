---
name: game-roadmap
description: Use only for video game projects; sequence prototype, vertical slice, demo, store page, festival, launch, and post-launch milestones
type: planning
version: v0.3
context_intake: artifact_only
visual_tier: visual
---

# Game Roadmap

Invoke as `$game-roadmap`.

Turn validated game research into production milestones.

## Output

Write or update `tasks/roadmap.md` with prototype, vertical slice, demo, store page, festival, launch, and post-launch phases.

## Alignment Page

By default, this skill reports results inline and writes only its normal durable artifacts (for example `tasks/*.md`, reports, queues, benchmark notes, status docs, or other skill-specific files). Do not build an alignment page automatically. Create `alignment/game-roadmap-{topic}.html` only when the user explicitly requests an alignment page or when you explicitly identify a concrete clarification/review need that cannot be handled cleanly inline; when you create one, follow `ALIGNMENT-PAGE.md` in this skill's directory.

## Next-Step Routing

After writing or updating `tasks/roadmap.md`:

- If the first milestone needs a concrete execution plan, check `.agents/project.json` for `agent-work-admin`; recommend `$plan-phase <first milestone>` when enabled, or `npx skillpacks install agent-work-admin` from the project shell when it is not enabled.
- If `tasks/todo.md` already contains executable work for the first milestone, check `.agents/project.json` for `exec-loop`; recommend `$exec` when enabled, or `npx skillpacks install exec-loop` from the project shell when it is not enabled.
- If the roadmap is blocked by missing game research or validation evidence, recommend the specific missing game skill from the same pack, such as `$game-core-loop`, `$game-prototype-test`, or `$game-store-page-test`.
- If no project execution work remains, state that no follow-up command is recommended.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
