---
name: design-movement-and-flow
description: "Improve static visual scan paths and composition movement from headline through evidence to action; repair confusing layout sequencing without contradicting keyboard or screen-reader order."
---

# Movement and visual flow

## Scope

Use this specialist when the actual task involves flow issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **flow**. Related governing principles: movement, emphasis. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **scan-path-dead-end**: Reorder content blocks and align landmarks; use directional image crops only if they support task flow. Verify: Observed scan and task completion reach intended conclusion.
- **visual-dom-order-conflict**: Preserve meaningful DOM sequence and use CSS only to reflow, not semantically reorder tasks. Verify: Tab and screen-reader sequence agree with visible logical flow.
- **dense-progress-story**: Introduce clear subheads, grouping, whitespace and step-specific emphasis; avoid ornamental arrows. Verify: Task walkthrough can explain what is next at each section.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
