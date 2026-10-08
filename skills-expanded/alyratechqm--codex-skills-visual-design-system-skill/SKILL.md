---
name: visual-design-system
description: Use when asked to redesign, polish, modernize, or improve the visual quality of a website or app UI, especially colors, buttons, spacing, shapes, typography, forms, dashboards, navigation, landing pages, or requests like "make it feel premium", "top-tier", or "less basic". Start with a short visual audit, define a reusable visual system, and implement consistent tokens, component variants, and responsive polish without changing product behavior.
---

# Visual Design System

Use this skill for visual polish work where the problem is not just layout logic, but the quality of the design language itself.

## Core Workflow

1. Inspect the current styling stack and shared UI primitives before editing.
2. Identify the 3-5 biggest visual problems.
3. Choose one visual direction that matches the product and audience.
4. Define or refine a small visual system before styling the page.
5. Apply the system consistently across the page and shared components.
6. Verify desktop, mobile, and UI states instead of styling only the happy path.

## Non-Negotiables

- Preserve behavior, data flow, and page purpose unless the user asks for product changes.
- Prefer reusable variables, tokens, theme values, or shared component styles over scattered one-off values.
- Keep buttons, cards, inputs, tables, modals, alerts, and empty states visually related.
- Improve hover, active, focus, disabled, loading, empty, success, warning, and error states.
- If the repo already has a design system, extend it instead of fighting it.
- If the repo has no clear system, introduce the lightest useful token layer you can.

## Always Establish A Small Visual System

Before polishing details, define or align these:

- Color tokens: `bg`, `surface`, `surface-2`, `text`, `text-muted`, `border`, `primary`, `primary-contrast`, `accent`, `success`, `warning`, `danger`, `focus`.
- Button system: `sm`, `md`, `lg`; `primary`, `secondary`, `ghost`, `destructive`.
- Button states: hover, active, focus, disabled, loading.
- Shape language: one radius family across buttons, cards, inputs, menus, and modals.
- Elevation: one consistent shadow and border approach.
- Spacing rhythm: predictable section padding, card padding, gaps, and table density.
- Typography: stronger hierarchy, cleaner labels, better scanability.

## Default Direction For Education And Admin Products

- Aim for calm, trustworthy, premium, and efficient.
- Prefer deep ink/navy, warm neutrals, and one confident accent.
- Student-facing screens may be slightly brighter, but should still feel credible.
- High-stress flows like tests or submissions should feel stable, low-noise, and easy to trust.

## Priority Order

1. CTA hierarchy and action clarity.
2. Color harmony and contrast.
3. Button quality, sizes, and states.
4. Consistent radii, borders, and shadows.
5. Spacing rhythm and section hierarchy.
6. Form and table scanability.
7. Empty, loading, and feedback states.
8. Mobile tap targets and responsive structure.

For broader redesigns or vague requests like "make it top notch", read [references/visual-audit-checklist.md](references/visual-audit-checklist.md).

## Anti-Patterns To Avoid

- Generic indigo/purple SaaS styling unless the brand already uses it.
- Random radius values across components.
- Heavy shadows, heavy borders, and saturated fills all competing at once.
- Weak contrast on primary actions or muted text.
- Too many accent colors.
- Admin pages that are roomy but hard to scan.
- Styling only the hero or header while leaving tables, forms, and states unchanged.
- One-off page fixes that bypass shared components or tokens.

## How To Interpret Common User Phrases

- "Make it top notch" means improve the system quality, not just decorate.
- "Buttons feel weak" means improve contrast, size, hierarchy, and interaction states.
- "Colors are bad" means rebalance palette and surfaces before adding effects.
- "Looks basic" means strengthen typography, spacing rhythm, and visual direction.
- "Premium" means calmer, more intentional, and less noisy.
- "Modern" means clean and crisp, not trendy for its own sake.

## Delivery Expectations

After editing:

- Summarize the chosen visual direction.
- Explain the biggest visual improvements.
- Mention any remaining design debt or old styles that still need cleanup.
