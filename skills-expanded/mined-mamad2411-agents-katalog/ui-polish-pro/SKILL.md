---
name: ui-polish-pro
description: Professional UI beautification and product visual refinement for desktop and web apps. Use when the user asks to make an interface more beautiful, premium, polished, modern, professional, refined, or visually consistent, especially for API-driven tools, dashboards, SaaS, admin panels, and desktop software. Incorporates high-taste anti-generic UI rules.
---

# UI Polish Pro

## Purpose

Improve product feel without hiding weak structure behind decoration.

Use with `ui-taste-pro` for taste critique, `frontend-design-pro` for screen structure, and `design-review-pro` for review.

## Workflow

1. Diagnose hierarchy: what should the user notice first, second, and last?
2. Fix structure before styling: grouping, alignment, density, navigation, and scan paths.
3. Establish visual system: typography, spacing, color, surfaces, borders, shadows, icons, and motion.
4. Polish states: hover, active, focus, pressed, selected, loading, empty, error, disabled, success.
5. Verify desktop and mobile: text fit, contrast, scroll behavior, responsive density, and no overlap.

## Taste Rules

- Make the interface specific to its product category.
- Use fewer, stronger visual decisions.
- Prefer rhythm, alignment, spacing, and typography over decoration.
- Operational apps should be calm, scannable, and efficient.
- Empty/error/loading states must feel intentionally designed.
- Color accents should communicate hierarchy, state, or brand, not random energy.

## Checklist

- Primary action is visually clear without overpowering the screen.
- Secondary actions are available but quiet.
- Tables, forms, filters, and panels are scan-friendly.
- Border radius, shadow, border, and surface treatment follow one system.
- Icons use one set, consistent size, and clear affordance.
- Typography scale matches context; compact UI uses compact headings.
- Layout avoids nested cards and visual clutter.
- Text does not overflow buttons, tabs, cards, or sidebars.

## Common Fix Patterns

- Replace scattered spacing with a 4/8px scale.
- Convert vague gray blocks into purposeful surfaces and separators.
- Group related controls into toolbars, panels, or fieldsets.
- Make destructive and irreversible actions visually distinct.
- Add subtle motion only where it clarifies causality or state changes.

## Avoid

- Generic purple/blue gradient defaults.
- Decorative blobs, orbs, and bokeh backgrounds.
- Card-in-card layouts.
- Oversized marketing hero treatments inside operational apps.
- Visual polish that ignores workflow, hierarchy, or accessibility.

## Output

State visual diagnosis, design direction, concrete changes, files touched, and viewport verification. Include screenshot/browser checks when available.

## Bundled Resources

- `references/visual-system.md`: polish order, token examples, and anti-AI-slop checks. Read before substantial UI beautification.
- `assets/dashboard-css-tokens.css`: reusable warm editorial dashboard token seed. Adapt to project brand; do not paste blindly.
