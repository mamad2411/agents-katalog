---
name: visual-direction
description: Locks a visual direction before a UI build by exploring 3 options, picking one, writing a banned-moves list + Design System Document. Use when UI keeps coming out generic or before a handoff.
profiles:
  - design-engineer
---

# visual-direction

Use this skill at the start of a design build, before any component is written, to lock the personality so everything built afterward inherits it. This is what stops the build from drifting to stock — the constraint layer the rest of the work references.

## Triggers

- A new project or screen is starting and the visual direction isn't set
- Generated UI keeps coming back generic because the direction was never locked
- A banned-moves list or design tokens don't exist yet
- Handing off to a build (figma-to-code) and needing a single reference document

## Required behavior

1. The agent MUST explore at least three *distinct* directions — not three shades of the same safe answer — before one is chosen.
2. Each direction MUST be concrete: a two-word name, the movements it draws on, 5 style descriptors, a palette in words, three named references, and three things it would NOT do.
3. The agent MUST produce a banned-moves list of 10–15 specific items before building starts, and MUST keep them concrete ("no rounded-square pastel icons", not "no generic icons").
4. The agent MUST consolidate the chosen direction, tokens, banned moves, and per-screen content into one Design System Document the build references.
5. The agent MUST NOT reopen the direction once locked; later drift is corrected against it, not by re-litigating it.

## Step 1 — explore three directions

```text
My project is [brief]. Brainstorm 3 distinct visual directions. For each, give me:
a 2-word name, the design movements it draws on, 5 concrete style descriptors, a
palette in words, 3 designers or studios whose work fits, and 3 things this
direction would NOT do.
```

## Step 2 — lock the banned moves

```text
Based on the chosen direction "[name]" and the references I love, draft a
banned-moves list — specific moves I will not allow. Cover shapes, color moves,
type behaviors, interaction clichés, and generic copy words. 10–15 items. Be
concrete: not "no generic icons" but "no rounded-square icons in pastel boxes."
```

## Step 3 — the Design System Document

Consolidate everything into one file the build references from here on:

```text
Consolidate the below into a Design System Document — one file I'll reference for
the rest of the build.

Visual direction: [paste]
Banned moves: [paste]
Tokens: [paste tokens, or "propose a token system from the direction above"]
Per-screen content: [paste real content]

Cover: the full visual system (colors, type scale, spacing, radii), the art
direction in plain language, the banned moves as hard constraints, and a
screen-by-screen breakdown with layout hierarchy and real content. Be specific
enough to generate each screen consistently without defaulting to generic
SaaS aesthetics. Where anything is too vague to execute, ask me one question at a
time before writing that section.
```

## Completion checklist

- At least 3 genuinely distinct directions were explored — different movements and personalities, not shades of one safe answer.
- Each direction carries all six attributes: 2-word name, movements it draws on, 5 style descriptors, palette in words, 3 named references, 3 things it would NOT do.
- One direction is locked and stays locked — drift is corrected against it, never re-litigated.
- The banned-moves list has 10–15 items and every item is concrete: each passes the specificity test ("no rounded-square icons in pastel boxes," not "no generic icons").
- A single Design System Document consolidates the locked direction, tokens, banned moves, and per-screen real content — and the build references it.

## When NOT to use

- A direction and tokens already exist — go straight to figma-to-code
- Reviewing or fixing already-built UI (use design-critique)
- Picking the first idea and skipping the alternatives — that defeats the skill
