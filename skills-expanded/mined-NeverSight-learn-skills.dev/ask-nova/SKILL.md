---
name: ask-nova
description: Interview-driven flow picker. Use when the user is unsure which skill/flow/pipeline fits — new project kickoff, cross-domain work, or a fuzzy situation. Reads the three routers live and recommends ONE flow. Not for tasks whose owner is already obvious.
disable-model-invocation: true
---

# Ask Nova

Conversational front door to the fleet. The user describes a situation; you
interview them, then recommend ONE flow. You carry NO roster knowledge of your
own — routing truth lives in the routers, read fresh every run:

1. `skills/using-skills/SKILL.md` — the top-level intent map (adopted surface,
   dormant list, lifecycle view).
2. `skills/using-design-skills/SKILL.md` — pipelines for anything visual /
   interface-shaped.
3. `skills/using-workflows/SKILL.md` — loop-shaped work (audit, plan→build,
   consensus, triage) and the recipe roster.

Read all three (deployed copies under `~/.agents/skills/` when not in the
repo) BEFORE asking anything. Never restate or cache their rosters here.

## The interview — batch-grill-me cadence

Map the situation as a decision tree and work it in rounds: each round, ask
the whole current frontier at once — numbered questions, each with your
recommended answer — then wait. Typical first frontier:

- Is there a codebase already, or greenfield?
- One session or multi-session? (multi → a `.workflow/` run dir + handoff seams matter)
- Is the deliverable visual/interface-shaped? (→ using-design-skills owns it)
- Is the work loop-shaped — audit / consensus / triage / plan→build? (→
  using-workflows owns it)
- How settled is the idea? (fuzzy → brainstorming / batch-grill-me first)

Facts discoverable from the environment: look them up, don't ask. Decisions
are the user's: ask and wait.

## The recommendation

Finish with exactly ONE flow, stated as named stations from the routers, in
order — e.g. `batch-grill-me → using-workflows (plan-pipeline) →
verification-before-completion` — plus, in one line each:
what was deliberately skipped and why, and where the flow's first command
starts. If two flows genuinely tie, say the tie-breaker question instead of
hedging. If nothing fits, say so and route to the map's NOT-FOUND rule —
never improvise a half-flow.
