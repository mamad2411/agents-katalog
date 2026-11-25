---
name: design-validate
description: "Validate visual design changes across screen sizes, themes, content variants, readability, and brand coherence. Use for visual regression and design acceptance checks."
---

# Validate visual design changes and screenshot outcomes

## Scope

Verify rendered visual outcomes and regressions; treat aesthetic judgment separately from accessibility and usability evidence.

## Procedure

1. Translate each design finding to a concrete acceptance condition: intended focal element, consistent semantic role, improved grouping, correct image crop, token reuse, robust text wrapping, or matching brand brief. Record the baseline and the change under test.
2. Test relevant variants: mobile/desktop widths, available themes, light/dark, zoom/text-spacing overrides, localization, long/error/empty data, component interaction states and image-load failures. Do not claim coverage for variants not actually rendered.
3. Use automated visual diff where available, but inspect important differences manually to separate intentional improvements from regressions. Check layout overflow and token usage via code; use grayscale or a short exposure to test hierarchy. Inspect at least one responsive transition rather than merely checking fixed endpoints.
4. Check cross-lens issues with `wcag-validate` (actual WCAG criteria, keyboard and AT) and `ux-validate` (task outcome and behavior). Visual checks cannot replace either.
5. Compare against `references/visual-test-matrix.md`, record `passed`, `failed`, or `not-tested`, link evidence, and report remaining brand/product judgment separately. Do not invent numeric aesthetic scores.

## Output

A concise per-finding table: hypothesis → variant(s) tested → method/evidence → observed result → regression notes → status/untested gaps. A report with no screenshots or browser rendering must explicitly describe its limitation.
