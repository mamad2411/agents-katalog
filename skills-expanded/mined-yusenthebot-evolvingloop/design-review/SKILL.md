---
name: design-review
description: Raise UI / visual / UX / game-feel quality from "it works" toward "it looks intentional." Screenshot the real interface, critique it against a concrete rubric, and adopt proven design patterns instead of inventing. Use on any round that changes visuals or UX, and before calling a visual feature done.
---

# design-review — be your own design critic (rubric + references)

The agent has no innate taste, but it CAN apply known-good patterns and self-critique against a checklist. That converts "ugly default" into "clean and intentional." (It will not produce designer-grade originality — that ceiling stays; this just stops things from looking amateur.)

## 1. Look at the real thing
Screenshot the actual rendered UI/scene and **Read it back** — eyes on screen, not a guess from the code.

## 2. Critique against the rubric
- **hierarchy** — is the most important thing the most prominent?
- **spacing & alignment** — consistent scale, a grid, generous whitespace (cramped reads as amateur)
- **typography** — a real type scale, few fonts/weights, readable line length
- **color & contrast** — limited palette, semantic colors, WCAG-legible contrast
- **consistency** — the same component looks and behaves the same everywhere
- **states** — empty / loading / error / hover / disabled all designed, not forgotten
- **motion / game-feel** (interactive/games) — feedback on every action, easing, juice

## 3. Don't invent — adopt
Pull proven patterns instead of hand-rolling: an established component library / design system, common layout patterns, documented game-feel principles. Research a reference first if unsure what "good" looks like here.

## 4. Iterate, then re-screenshot
Fix the worst rubric failures, screenshot again, confirm it actually improved. Don't call a visual feature done until it passes the rubric on a real screenshot.
