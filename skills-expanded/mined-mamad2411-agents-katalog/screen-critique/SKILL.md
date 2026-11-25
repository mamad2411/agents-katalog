---
name: screen-critique
description: Critique a rendered screen, screenshot, Figma frame, or built page across seven visual-quality dimensions and return a prioritised P1/P2/P3 fix list. Use for "what is wrong with this screen", "why does this look off", "review this design", or a critique of visual hierarchy, composition, typography, colour, affordance, information density, or brand consistency. For a WCAG conformance audit use `accessibility-audit`; for reviewing UI changes in a diff, PR, or branch use `interface-review`; for applying fixes rather than judging them use `better-layout`, `taste-skill`, or `perception-laws`; for a full redesign use `impeccable-bridge`.
---

# Screen Critique

You judge a single rendered screen and say what is wrong with it, in priority order, working from named criteria rather than taste alone.

The input is whatever shows the screen: a screenshot, a Figma frame, a URL you can render, or a described view. The output is a prioritised fix list, not a rewrite. Applying the fixes is a separate job.

## The seven dimensions

Each dimension has its own sidecar with the criteria, the questions to ask, and the failure patterns to look for.

- [critique-visual-hierarchy.md](critique-visual-hierarchy.md) - entry point, eye flow, weight distribution, and emphasis. Reach for it when attention lands in the wrong place.
- [critique-composition.md](critique-composition.md) - balance, whitespace, rhythm, and gestalt grouping. Reach for it when the layout feels off but the hierarchy is fine.
- [critique-typography.md](critique-typography.md) - scale usage, readability, consistency, and token compliance.
- [critique-color.md](critique-color.md) - contrast ratios, palette coherence, semantic colour use, and colour accessibility.
- [critique-affordance.md](critique-affordance.md) - what looks clickable, state visibility, CTA clarity, and action discoverability.
- [critique-information-density.md](critique-information-density.md) - cognitive load, content priority, scanning patterns, and progressive disclosure. Reach for it when a screen feels overwhelming.
- [critique-brand-consistency.md](critique-brand-consistency.md) - mood, voice, and token compliance against the project's own `mood.md`, `voice.md`, and `tokens.md`. Skip it when those files do not exist rather than inventing brand rules.

## How to run a critique

Load only the sidecars you need. A question about one dimension ("is the type on this screen right?") loads one sidecar. A general ask ("critique this screen", "why does this look off?") loads all seven and runs them in the order listed above.

Work each loaded sidecar to its own output format first: an observation, the problem, and a fix per sub-dimension, with each sub-dimension rated `pass` / `minor issue` / `major issue`. Then collect every flagged issue across the dimensions you ran and rank them.

## Prioritisation

- P1 Critical: breaks usability, accessibility, or brand compliance. Fix before shipping.
- P2 Important: degrades the experience or creates inconsistency. Fix in the current sprint.
- P3 Polish: minor visual refinement. Address when capacity allows.

## Output format

A single prioritised fix list grouped by priority level. Each item carries:

- Issue: what is wrong.
- Dimension: which critique area it came from (Hierarchy / Brand / Composition / Typography / Colour / Affordance / Density).
- Fix: the specific change required.

Conclude with a one-paragraph overall assessment naming the strongest and the weakest dimension.

Name what you actually saw. An issue you cannot point at on the screen does not belong on the list, and a dimension you did not run should be reported as not run rather than as a pass.

---

_Forked from [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills) - MIT License. See original repository for full license text._
