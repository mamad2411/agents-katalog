---
name: mobile-god
description: Expert mobile formatting and responsive product UI workflow. Use when creating mobile UI from scratch, updating existing mobile layouts, converting desktop screens to mobile, auditing responsive breakage, fixing iOS Safari/safe-area/form/touch issues, or defining mobile QA for dense apps.
---

# Mobile God

Mobile God is a senior mobile design engineer skill for Codex. It handles three core jobs:

- Create a mobile-first screen or component from scratch.
- Repair or polish an existing mobile or responsive implementation.
- Port an existing desktop screen to mobile without turning it into a redesign.

## First Action

For substantial work, read `references/mobile-god-playbook.md` before editing. Read `references/source-map.md` when you need source lineage, rationale, or to explain why the workflow prioritizes a certain pattern.

For a tiny fix, use the checklist in this file and proceed.

## Non-Negotiables

- Inspect the actual code, screenshots, or design frames before changing anything. Do not invent component names, paths, tokens, colors, breakpoints, or routes.
- For a desktop-to-mobile port, the desktop surface is the visual source of truth. Preserve palette, type intent, component identity, information hierarchy, data shown, and brand voice. Change layout, density, stacking, touch behavior, and disclosure only as needed.
- Write mobile-first code. In Tailwind, unprefixed utilities are the mobile base; `sm:`, `md:`, and `lg:` layer upward.
- Separate macro layout from micro layout. Macro shell changes can use viewport media queries. Components should prefer intrinsic layout and container queries so they survive inside sidebars, sheets, modals, cards, and split panes.
- Do not use fixed widths on containers unless the product has a clear reason. Prefer `min()`, `max()`, `clamp()`, `auto-fit`, `minmax()`, flex wrapping, and container-aware sizing.
- No unintentional page-level horizontal scroll. Intentional, bounded, signposted horizontal scrollers are allowed for reference tables, timelines, chip rows, charts, or comparison views when that is the right interaction.
- Primary navigation, primary content, and primary actions remain visible or directly reachable. Progressive disclosure is for secondary detail.
- Inputs must be 16px or larger, use the right `type` or `inputmode`, and include explicit `autocomplete` where possible.
- Fixed headers, bottom navs, sticky CTAs, floating buttons, full-screen sheets, and corner controls must handle safe areas with `viewport-fit=cover` plus `env(safe-area-inset-*)` padding when relevant.
- Hover-dependent UX must get a touch equivalent. Gate decorative hover affordances behind `(hover: hover) and (pointer: fine)`.
- Touch targets should be at least 44px, preferably 44-48px on mobile.
- For SVG, icon, or chart work, keep a valid `viewBox`, avoid clipped graphics and embedded raster payloads, use `currentColor` or tokens when appropriate, and choose `aria-hidden`, `<title>`, or `<desc>` deliberately.

## Operating Loop

1. Restate the target as one mode: create, update, port, audit, or full-app mobile shell.
2. Identify inputs and source of truth: code, design frame, screenshot, existing mobile view, product spec, design system, or route tree.
3. Inventory the screen component by component.
4. Classify each item as macro or micro.
5. For each component, state desktop behavior, target mobile behavior, mechanism, and likely break width.
6. Implement the smallest coherent change in the existing style.
7. Verify with the width matrix and task-specific checks.

## Component Decision Rules

- Metric cards and dashboard panels: use intrinsic grids like `repeat(auto-fit, minmax(min(100%, 16rem), 1fr))`; use bounded type and spacing with `clamp()`.
- Toolbars, filter chips, and button groups: use flex wrapping, visible primary actions, and overflow menus only for secondary actions.
- Sidebars: move to bottom tabs, a top drawer, or a labeled More sheet. Do not shrink a desktop sidebar into an unusable rail.
- Navigation: keep important destinations visible. If there are too many items, use a single-row horizontal scroller with an edge hint or a labeled More target.
- Action tables: render mobile cards or stacked rows from the same row model. Keep primary fields in the card header, status as a pill, label-value pairs for secondary fields, and row actions in a visible button or menu.
- Reference tables: keep table structure inside a bounded `overflow-x: auto` scroller with a clear edge gradient, sticky key column, or scroll hint when comparison matters.
- Charts: simplify instead of shrinking. Reduce series/ticks, use explicit chart height, make tooltips tap-driven, and create a dedicated mobile variant for dense visualizations.
- Forms and wizards: one step per screen when dense, sticky keyboard-safe footer CTA, compact progress, persisted state, correct keyboard attributes, and no iOS input zoom.
- Dialogs and popovers: switch to bottom drawers/sheets on mobile when the interaction is task-like or content-heavy. Verify focus trap, restore focus, close affordance, and safe-area padding.
- Carousels and scrollers: use scroll snap, partial item visibility, lazy media, and no autoplay for reading or workflow content.

## Output Contract

When producing a design, patch, or review, give the user:

1. Responsive strategy: component by component, naming macro or micro, desktop behavior, mobile behavior, mechanism, and break widths.
2. Code or design result: mobile-first, preserving real tokens and names, with no new dependency unless justified.
3. Width-matrix audit: 320, 390, 480, 640, 768, 1024, 1280, 1440, 1920. Include overflow, wrapping, touch-target, density, form, and safe-area findings. If runtime screenshots or browser checks were not possible, say so clearly.

## Verification

Use the strongest available local checks. For code changes, prefer typecheck, lint, targeted tests, Storybook or component stories when present, Playwright/browser screenshots for high-risk layout work, and build when practical. For mobile UI changes, inspect at least one narrow viewport before calling the work done.

If current library, framework, SDK, CLI, or cloud-service behavior matters, fetch current docs with Context7 or the repo-approved docs path before relying on memory.
