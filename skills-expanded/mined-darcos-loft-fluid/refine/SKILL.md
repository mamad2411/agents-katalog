---
name: refine
description: A shared vocabulary of named refine commands for existing UI (typeset, colorize, animate, settle, flow, bolder, quieter, distill, regroup, glass, iconify, deslop, brandward, productward, audit, critique, harden, polish). Use when the user asks to improve, fix, tighten, calm, strengthen, or polish a UI with a precise verb instead of a vague "make it better". Each command is one scoped move wired to the rest of the suite.
license: MIT
---

# Refine

A shared vocabulary of small, named moves you make on UI that already exists. Each command is one verb with one job. "Make it better" is vague and drifts; `typeset` then `quieter` then `polish` is precise, repeatable, and reviewable.

This is the granular layer of the suite. `design-system` creates an identity, `fluid` sets the motion, `output` gates the ship. `refine` is the set of verbs you use in between to push a screen from done to right.

## How to invoke

The user names the verb, in their words or as a slash command:
- "typeset this", "make the hero bolder", "calm the motion", "/polish the pricing section"

Apply exactly that move, nothing else. Do not `colorize` when asked to `typeset`. If the user named a region (a section, a component, a selection), scope to it; otherwise apply to the current view. State the change in one line, then run `audit` if motion or color was touched.

Commands compose. Chain them in the order the user implies, or in the natural order: structure, then type, then color, then motion, then polish. Full definitions, with what each one enforces and leaves alone, are in [reference/commands.md](reference/commands.md).

## The vocabulary

Type
- **typeset** — repair typography: a distinctive pairing from the database, a real scale, measure under ~75 characters, tracking eased on large headings. Kills justified, sub-10px, and crushed text.
- **recase** — fix casing tics: drop all-caps body, keep uppercase kickers to one if at all.

Color
- **colorize** — apply or repair the palette: commit to a dominant with one rationed accent, near-black not pure black, no purple-wash gradient, body contrast 4.5:1.
- **tone** — shift the mood (warmer, cooler, darker, more muted) without breaking the locks.

Motion
- **animate** — add motion on purpose, with the house easings and a reduced-motion path. Reveals, heroes, hovers, counters.
- **settle** — calm janky or excessive motion: instant on frequent interactions, named transitions over `transition: all`, `scale(0.93)` not `scale(0)`, fixed `transform-origin`.
- **flow** — give many small animations one shared physics source (one scroll velocity, one progress value) so they read as one system.

Emphasis
- **bolder** — increase force: widen the type jump, raise contrast, give one element a real moment.
- **quieter** — dial it down: ration the accent, hairlines over fills, more whitespace, fewer effects.

Structure
- **distill** — strip slop structure: flatten nested cards, vary identical card grids, drop the icon-tile-above-every-heading and the 01/02/03 markers. Cut copy to the essential.
- **regroup** — fix hierarchy and sectioning: correct heading order, group what belongs together, separate brand from product.

Surface
- **glass** — apply the liquid-glass treatment to signal depth or dismissal, not as decoration.
- **iconify** — replace emoji and stock icons with a consistent bespoke SVG set.

Copy
- **deslop** — kill marketing buzzwords, manufactured "not X but Y" contrast, and em or en dashes. Say the concrete thing.

Register
- **brandward** — push toward impression-led brand work (a landing page): more air, more type, a stronger hero moment.
- **productward** — push toward task-led product UI (a dashboard): denser, calmer, faster, information-first.

Gates
- **audit** — run the deterministic detector (29 rules) and report.
- **critique** — qualitative review against the by-hand catalog (the structural and semantic tells the detector cannot see).
- **harden** — accessibility and robustness: reduced-motion in CSS and JS, visible focus, contrast, color-scheme.
- **polish** — the final craft micro-pass: press and hover feedback, optical alignment, consistent radii and spacing, the details that separate a demo from a shipped build.

## Composition

- New screen lands generic: `distill` → `typeset` → `colorize` → `polish`.
- Motion feels off: `audit` → `settle` → `flow`.
- Hero is flat: `bolder` → `animate` → `polish`.
- Landing page reads like a dashboard: `brandward` → `typeset` → `glass`.
- Before shipping: `audit` → `harden` → `polish`, then the `output` gate.

## Wiring

These commands are not new rules. They are named entry points into rules the suite already holds.

- `typeset` and `colorize` draw from `design-system/data/` (the palette and type-pairing database) and `design-system/reference/rules.md`.
- `animate`, `settle`, and `flow` apply the `fluid` SKILL rules and the house easings.
- `glass` and `iconify` use `design-system/reference/glass.md` and `reference/icons.md`.
- `audit` runs `fluid/detector/detect.mjs`. `critique` reads `fluid/reference/anti-patterns.md`.
- `harden` and `polish` enforce the `output` checklist.

Pairs with: every skill in the suite. `refine` is the verb layer over all of them.
