---
name: autonomous-webserial-loop
description: Use as a workflow skill when AI should plan, draft, judge, red-team, and revise mystery-heavy strategic webserial chapters until they satisfy architecture, intelligence, consequence, and payoff criteria.
---

# Autonomous Webserial Loop

Use this workflow skill when you want AI to keep working on a strategic mystery chapter or arc until it crosses a clear quality bar instead of stopping at the first plausible draft.

## Quick Start

Use this skill to coordinate:

- `$strategic-webserial-architecture`
- `$faction-power-consequence-engine`
- `$strategic-cast-intelligence-engine`
- `$mystery-payoff-and-fairness-judge`

Load `references/loop-contracts.md` when you need the exact output shape for an autonomous run.

## Default Loop

Strict mode is the default.

1. Establish the target unit: scene, chapter, arc beat, reveal, or system revision.
2. Run `$strategic-webserial-architecture` if the promise stack, clue ladder, or reveal order is unclear.
3. Run `$faction-power-consequence-engine` if power logic, organizations, or consequences are under-defined.
4. Run `$strategic-cast-intelligence-engine` to map the best moves, countermoves, and blind spots.
5. Draft only after the architecture and pressure model are stable enough to support prose.
6. Run `$mystery-payoff-and-fairness-judge` on the result.
7. Run one red-team pass that tries to break the draft by asking:
   - what feels convenient?
   - what reveal is under-seeded?
   - who acted below their intelligence?
   - what changed too little?
8. Choose the highest-level repair needed:
   - prose fix
   - scene fix
   - chapter fix
   - arc fix
   - system fix
9. Revise only at that level, then score again.
10. Stop when the chapter clears the quality bar or when the remaining weaknesses require new author intent rather than more iteration.

## Quality Bar

The loop can stop when all of these are true:

- no category in the judge scorecard is below `3`
- causal integrity and strategic intelligence are both `4` or better
- at least one major question sharpened or changed
- at least one meaningful cost, gain, or irreversible discovery occurred
- the ending hook comes from consequence or revelation, not vagueness alone

## Operating Rules

- Do not polish sentences while architecture is failing.
- Do not rewrite the whole chapter if the real problem is a missing seed two scenes earlier.
- Do not let the loop drift into lore inflation. New material must solve an identified weakness.
- Preserve productive weirdness and dread. The goal is not bland neatness.
- If the draft still fails because the premise itself is weak, stop and recommend a premise-level repair.

## Guardrails

- Use Reverend Insanity and Lord of the Mysteries as benchmarks for structural ambition, mystery layering, and consequence design, not as templates to copy.
- Do not imitate names, plot events, sequence of reveals, factions, or proprietary setting elements from existing works.
- Prefer explicit rubrics and revision gates over vibe-based approval.
