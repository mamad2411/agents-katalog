---
name: frontend-design-guardrails
description: "Use when page, component, form, table, dashboard, responsive layout, or UI review work needs product-quality implementation guardrails. DO NOT USE FOR: backend-only changes or scripts with no user-visible surface."
---

# Frontend Design Guardrails

## Goal

Build usable interfaces that match the target repository's existing UI system and can be verified reliably.

## Reference Principles

- Ant Design baseline: optimize for natural interaction, certainty, meaningful task progress, and systems that can grow without visual drift.
- Design patterns beat freestyle UI: prefer established page patterns, reusable components, tokens, layout rules, copy conventions, feedback patterns, and data-entry/data-display patterns.
- Design-system packets beat vague style adjectives: record the minimum explicit tokens and component decisions needed to make the result repeatable.
- Preview culture matters: make the result inspectable through browser evidence, screenshots, or a clear static fallback.

## Rules

- Prefer the repository's existing component library, theme tokens, layout primitives, icon set, routing, and state patterns.
- If the repository uses Ant Design, Ant Design Pro, Pro Components, or compatible tokens, use their components and interaction patterns first; only build custom controls when the library cannot express the workflow.
- For operational tools, favor dense, calm, scannable layouts over marketing-style hero sections.
- Use semantic controls: buttons for commands, inputs for text, selects/menus for option sets, tabs for views, toggles for binary settings.
- Provide loading, empty, error, disabled, success, and partial states when the workflow needs them.
- Avoid magic pixel offsets, absolute-positioned main layouts, clipped text, overlapping controls, and layout shifts.
- Ensure controls have stable accessible labels or text so browser tests can locate them.
- For mobile and desktop, verify that text fits and primary actions remain reachable.
- Do not invent metrics, testimonials, brand claims, screenshots, or business data. Use real data, labelled placeholders, or explicit empty states.
- Avoid generic AI-looking UI: ungrounded purple gradients, decorative blob backgrounds, arbitrary glass cards, over-rounded nested cards, lorem ipsum, and icon-only controls without accessible names.

## Before Implementation

Freeze:

- target user and workflow
- existing UI library/patterns
- page structure
- critical states
- responsive breakpoints
- validation method
- brand source or visual direction
- data density and hierarchy
- accessibility-critical labels and keyboard path

## Design System Packet

For non-trivial UI work, generate a small design-system packet before coding, inspired by UI UX Pro Max and Open Design's active-design-system workflow:

- `product_type`
- `surface`
- `audience`
- `style_direction`
- `brand_source`
- `color_tokens`
- `typography`
- `spacing`
- `components`
- `data_density`
- `states`
- `accessibility_rules`
- `test_plan`
- `anti_patterns`

Store this in the task plan or component notes only when useful; do not create a persistent design-system folder unless the user or spec asks for it.

If the visual direction is underspecified, propose 2-3 concrete directions with tradeoffs before coding. For implementation tasks with an existing product style, derive the packet from current code and screenshots rather than replacing the product identity.

## Craft Review

Before delivery, self-review the UI across five dimensions:

- hierarchy: primary action, data priority, and scan path are clear
- consistency: spacing, typography, components, and feedback match the system
- function: core workflow works with realistic loading/error/empty data
- accessibility: labels, contrast, keyboard path, and focus states are adequate
- implementation: no layout shifts, clipped text, console errors, or endpoint leaks

## Before Completion

Run or request a browser/visual check through `web-experience-audit`, or state why runtime verification is unavailable and provide static fallback evidence.
