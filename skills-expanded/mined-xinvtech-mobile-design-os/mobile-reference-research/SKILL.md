---
name: mobile-reference-research
description: Find, inspect, compare, and shortlist native mobile product references for a new app or feature. Use when Codex needs evidence-backed reference research, a source matrix, competitor or pattern comparison, style-family inputs, or a clear borrow/transform/reject boundary before UX or UI design.
---

# Mobile Reference Research

Build a small, traceable reference field that informs product and interface decisions without turning the target into a clone.

## Choose the research mode

- **Discover**: find a focused set of current, first-party mobile references from a product brief and search terms.
- **Compare**: compare supplied references across mechanics, task flow, platform behavior, visual grammar, and risks.
- **Shortlist**: reduce a larger board or source set to the references that should influence the next design stage.

Use `analyze-mobile-ui` after this Skill when screenshots or source products need detailed Design DNA extraction. Use `mobile-ui-design` when the user wants visual directions or rendered screens.

## Establish the research question

Record the target product, primary user/job, platform, core task, usage frequency, and what decision the references must inform. Do not search for “beautiful apps” without a decision to make.

## Build the evidence set

1. Prefer official App Store/Google Play pages, first-party product pages, platform surfaces, and supplied screenshots.
2. Record a stable `RF` ID, source URL or local path, platform, product state, access date, and evidence limitations for every source.
3. Keep native-mobile and platform-surface references at or above 60% of the set, including at least one real native-mobile product.
4. Inspect screenshots and boards directly; treat store marketing frames as presentation evidence, not proof of runtime behavior.
5. Mark current, versioned, or time-sensitive claims with their date. Use `unknown` when a source does not establish behavior.

## Compare reusable qualities

For each selected reference, record:

- One concrete product or interaction quality to borrow.
- One visual or behavioral boundary not to copy.
- The target-product decision it may inform.
- Whether the transfer is `transfer`, `transform`, or `reject`.
- Confidence and the evidence IDs supporting the conclusion.

Compare the same task across references whenever possible: entry, action, feedback, durable result, and recovery. Separate product mechanics from visual decoration.

## Produce the research package

Create:

- `reference-research.md` using [assets/reference-research-template.md](assets/reference-research-template.md).
- `reference-research.json` using [assets/reference-research-template.json](assets/reference-research-template.json) and [references/reference-research-schema.md](references/reference-research-schema.md).

Run `python3 scripts/validate_reference_research.py <path-to-reference-research.json>` and fix every error. Treat warnings or evidence gaps as inputs to the next Skill, not as permission to invent behavior.

## Enforce the output order

1. Research question and target context.
2. Evidence inventory and coverage gaps.
3. Reference comparison matrix.
4. Transfer, transform, and reject decisions.
5. Shortlist for UX, platform, and visual work.
6. Open questions, freshness, and confidence.

Do not finish with a gallery of names only. Every shortlisted reference must change a concrete design decision or be removed.
