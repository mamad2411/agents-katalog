---
name: design-balance-and-proportion
description: "Analyze and improve symmetrical/asymmetrical visual weight, hero balance, image-to-text proportions, modular scales and responsive ratios without treating golden ratio as a requirement."
---

# Balance and proportion

## Scope

Use this specialist when the actual task involves balance issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **balance**. Related governing principles: balance, proportion. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **lopsided-hero**: Reduce media area or saturation, move focal content, add counterweight via spatial grouping. Verify: At three responsive widths the hero conveys intended priority and does not collapse.
- **ratio-inconsistency**: Choose documented ranges for proportions; constrain with min/max not rigid ratios; align to content priority. Verify: Test compact and expanded data; sidebar remains useful and content readable.
- **asymmetry-unintended**: Check whether intentional asymmetry supports focal point; if not redistribute density or move supporting elements. Verify: Review paired wide/narrow compositions with intended hierarchy stated.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
