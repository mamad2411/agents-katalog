---
name: design-typography
description: "Improve frontend typography with font pairing, serif versus sans, fluid type scales, line height, tracking, kerning, measure, localization, font licenses and readable heading/body hierarchy."
---

# Typography

## Scope

Use this specialist when the actual task involves typography issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **typography**. Related governing principles: proportion, contrast. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **type-scale-drift**: Adopt a modest fluid type scale with named roles; test large text and line wrapping before freezing values. Verify: All headings map to named roles; layout tolerates 200% zoom and longer strings.
- **body-text-cramped**: Tune measure (approx. 55–75 characters), line-height, margins and readable body size; adjust by font and task. Verify: Reading in narrow and wide screens has no clipped lines or forced horizontal scrolling.
- **mixed-type-personality**: Choose one versatile family or purposeful display/body pairing; define fallbacks and license-valid loading. Verify: Fonts render consistently under slow network/fallback and in multilingual content.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
