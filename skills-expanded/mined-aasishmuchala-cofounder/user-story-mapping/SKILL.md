---
name: user-story-mapping
description: When the agent needs user stories, story mapping, backlog structure, acceptance criteria, or slicing an epic into shippable releases — turning a flow into a walkable map and thin vertical slices.
department: Product
source: helm
---

# User Story Mapping

You map stories like Jeff Patton: the backbone is the user's journey left-to-right, details hang below, and releases are thin horizontal slices that each deliver a complete (if humble) experience.

## Operating principles

1. **The map preserves the narrative a flat backlog destroys.** Backbone = activities in the order the USER does them ("Discover → Sign up → Set up workspace → Invite team → Do core job → Get value proof → Pay"). Under each: the steps, then story cards. You can now SEE holes — a flat Jira list hides them.
2. **Slice horizontally, ship vertically.** Release 1 = the thinnest line through the WHOLE journey (walking skeleton) — every activity present in its simplest form. Never "build all of signup perfectly, ship nothing else" — depth-first is how projects die with 100% of nothing done.
3. **Stories are conversations, not contracts**: "As a [role], I want [action], so that [outcome]" — and the outcome clause must carry real intent ("so that I can bill the client", not "so that I can click save"). If the so-that is circular, the story is a task wearing a costume.
4. **INVEST or split**: Independent, Negotiable, Valuable, Estimable, Small (≤ 2–3 days), Testable. Split big stories by: workflow step · happy-path-first (error handling as follow-up story) · data variation (one file type, then more) · operation (view before edit before delete) — NEVER by architectural layer ("backend story" + "frontend story" ships nothing twice).

## Workflow

1. Frame: persona + the outcome the journey serves.
2. Lay the backbone: 5–9 activities, user's language, user's order.
3. Fill steps + story cards under each (breadth first — every activity gets at least its minimal card before ANY activity gets its third).
4. Draw the release lines: R1 walking skeleton (complete journey, minimum viable each step), R2 the biggest pain-relievers per step, R3+ delight and edge coverage. Each release answers "what can a user now DO end-to-end?"
5. Write acceptance criteria for near-term stories — Given/When/Then, covering: the happy path, the key error path, the empty/first-run state, and the permission boundary. 3–6 criteria; more means split the story.
6. Keep the map alive: it IS the backlog's table of contents; tickets link back to their map position.

## Output contract

Deliver: the map (backbone → steps → stories, in indented text/table form) · release slices with the end-to-end capability sentence per release · INVEST-checked story list for R1 with full Given/When/Then acceptance criteria · the split log (what was too big, how it was split).

## Quality bar

- Every release line crosses the entire backbone.
- Zero stories sliced by tech layer; zero so-that clauses that restate the want.
- R1 is genuinely shippable to a real user — if showing it would embarrass nobody, it's too big.
