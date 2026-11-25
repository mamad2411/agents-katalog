---
name: design-hierarchy-and-emphasis
description: "Repair frontend visual hierarchy, weak or competing focal points, flat heading scale and misplaced action prominence with contrast, space, scale and clear reading order; review aesthetic emphasis without sacrificing accessibility."
---

# Visual hierarchy and emphasis

## Scope

Use this specialist when the actual task involves hierarchy issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **hierarchy**. Related governing principles: emphasis, contrast. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **primary-message-hidden**: Reduce decorative size/contrast, elevate the H1 and place supporting action near the proposition. Verify: A five-second glance identifies the primary proposition; the DOM reading sequence still makes sense.
- **competing-actions**: Resolve actual user decision; emphasize one task-default and style alternatives as secondary without hiding them. Verify: Participants identify primary action; alternate action remains discoverable and operable.
- **gray-collapsed**: Differentiate sizes, weights, spatial grouping and foreground/background tone. Verify: Greyscale screenshot preserves at least three meaningful hierarchy levels; all required contrasts pass separately.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
