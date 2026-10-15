---
name: design-ideate
description: Generate several distinct UI directions for a screen or flow before committing to one. Produces 2-4 named interface directions with layout logic, component choices, and tradeoffs, optionally with generated mockup images. Use when the user says "ideate the UI", "give me layout options", "design directions for this screen", "explore the interface", or after context/research and before prototyping. Part of the Product Design set.
---

# Design — Ideate

Produce genuinely different interface directions so the user chooses *deliberately*, not by default. Each direction is a different *organizing principle* for the same goal — not a recolor of one layout. The output makes tradeoffs explicit so the choice is reasoned.

## When to use
- After context/research, before building anything.
- The user wants options ("give me a few layouts") not a single answer.
- A flow could be structured multiple valid ways and you want to surface the tradeoffs.

## When NOT to use
- The brief is unclear → `design-get-context` first.
- One direction is already chosen → go to `design-image-to-code` / `design-prototype`.
- It's a tiny tweak to an existing screen → just do it / `design-audit`.

## Inputs
- `./design/context.md` (goal, user, success) + `./design/research.md` (patterns, pains) if they exist.
- The screen/flow to design.

## Workflow
1. **Diverge on structure.** Propose **2-4 named directions**, each a different organizing principle (e.g. "Dense Dashboard" vs "Guided Wizard" vs "Single Canvas"). If they share layout structure, they're the same direction.
2. For each: **layout logic, primary-action placement, component choices, what it optimizes for, what it sacrifices.**
3. *(Optional)* generate a mockup image per direction with an image tool, UI-mock style, respecting the product's IA + design-system constraints. Save to `./design/ideate/<direction>.png`.
4. **Map each direction to the goal/success criteria** from context — which one best serves the metric?
5. **Recommend one**, state why, ask the user to pick. Winner → `design-image-to-code` or `design-prototype`.

## Worked example
Goal (from context): cut onboarding drop-off; JTBD = create first project in <2 min.
```
## Direction A — "Guided Wizard"
principle: one decision per step, minimal cognitive load
layout: centered card, progress rail, single CTA per step
optimizes: completion rate for novices (directly serves the goal)
sacrifices: speed for power users; feels slow if you know what you want
fits goal: strong — fewer choices per screen = less abandonment
[mock: ./design/ideate/guided-wizard.png]

## Direction B — "Single Canvas"
principle: everything on one screen, progressive reveal
layout: left config panel + live preview right
optimizes: speed + sense of control for confident users
sacrifices: can overwhelm first-timers (the actual target user)
fits goal: weaker — more on screen at once = higher early drop risk

## Direction C — "Template-First"
principle: pick a starting template, then customize
layout: gallery → editor
optimizes: time-to-first-value (start from something, not blank)
sacrifices: needs good templates; wrong template = friction
fits goal: strong — sidesteps blank-canvas paralysis
```
Recommendation: A or C (both serve novice completion); A if flows are linear, C if a template library exists. → user picks A.

## Quality bar
- Directions differ in **structure**, not just color/spacing.
- Each has explicit **optimizes / sacrifices** — every direction trades something.
- Each is mapped to the success criteria so the choice is goal-driven.
- A clear recommendation with reasoning, not just "here are options, you decide".

## Common pitfalls
- **Recolors masquerading as directions** — if the only difference is the accent color, it's one direction.
- **No tradeoffs stated** — every layout sacrifices something; hiding that makes the choice blind.
- **Ignoring DS/IA constraints** — inventing components the product doesn't have creates downstream rework.
- **Too many directions** — 5+ options causes choice paralysis; 2-4 is the sweet spot.

## Handoff
Chosen direction → `design-image-to-code` (if you have a mockup to match) or `design-prototype` (to wire it directly). The losing directions' tradeoffs are useful context to keep.

## Tooling
Mockup images are optional and need an image tool. The core deliverable (named directions + tradeoffs + recommendation) needs no tooling — it's structured thinking.
