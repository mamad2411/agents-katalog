---
name: design-rhythm-and-pattern
description: "Repair inconsistent visual repetition and pattern across UI cards, icons, spacing, backgrounds and pages while preserving salience and avoiding overwhelming decorative rhythm."
---

# Rhythm and pattern

## Scope

Use this specialist when the actual task involves rhythm issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **rhythm**. Related governing principles: pattern, unity. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **inconsistent-components**: Consolidate component styles and spacing into semantic tokens; permit role-based variants only. Verify: Comparison of three pages reveals consistent role treatments.
- **wall-of-identical-cards**: Preserve component system but vary content weight/featured layout for genuinely different priority. Verify: Viewer can find featured item in a short scanning task.
- **pattern-overpowers-content**: Reduce scale/opacity and remove texture behind readable content; avoid visual flicker. Verify: Body/controls remain legible and attention goes to content, not motif.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
