---
name: academic-slide-refiner
description: Refines and restructures existing presentations into concise, high-impact versions suitable for short academic conference talks (e.g., 20 minutes). Focuses on logical flow, information density, and visual consistency.
license: Complete terms in LICENSE.txt
---

# Academic Slide Refiner

Use this skill to transform a dense, paper-like presentation into a concise and compelling short academic talk.

## Knowledge And Tool Interaction

1. Use the provided slide deck, paper, and local visual assets as the primary knowledge source for refinement decisions.
2. If the task first needs shared KB or tool lookup before choosing reusable slide-generation helpers, delegate that lookup to `eda-context-accessor`.
3. Reuse bundled diagram scripts and templates before inventing new visualization helpers.

## Operational References

1. Load `references/core-principles.md` when setting slide density, one-idea-per-slide discipline, or visual consistency rules.
2. Load `references/external-report-constraints.md` when refining advisor-facing or externally shareable decks.
3. Load `references/refinement-workflow.md` when restructuring the deck narrative, splitting dense slides, or refining content and layout.
4. Load `references/page-specific-practices.md` when handling motivation, mechanism-synergy, or limitations slides.
5. Load `references/bundled-resources.md` when deciding whether to reuse existing diagram-generation scripts.
