---
name: mobile-responsive-ux-ui
description: "Use for comprehensive mobile and responsive UX/UI work: auditing broken layouts, fixing bad formatting, building from scratch, converting desktop designs to mobile, and hardening design systems across web and native mobile."
---

# Mobile Responsive UX/UI

Use this skill whenever the user asks for mobile UI, responsive design, bad
mobile formatting fixes, desktop-to-mobile conversion, design-system UI work,
touch/accessibility hardening, Flutter responsive layout, React Native UI,
or a new frontend screen that must work across devices.

## Source First

Before editing UI, inspect the project stack and styling system. Do not mix
styling systems. Reuse Tailwind, CSS modules, CSS variables, component
primitives, tokens, breakpoints, icon libraries, and motion conventions that
already exist.

Load only the references needed for the current task:

- `../../references/operating-model.md` for mode routing and source-pack map.
- `../../references/responsive-audit-checklist.md` for audits and QA.
- `../../references/mobile-repair-playbook.md` for overflow, forms, nav, tables, charts, and modal repairs.
- `../../references/desktop-to-mobile-conversion.md` for porting dense desktop screens.
- `../../references/design-system-and-tokens.md` for token, Tailwind, CSS variable, radius, shadow, and motion rules.
- `../../references/accessibility-touch.md` for keyboard, screen reader, touch, safe-area, and mobile a11y.
- `../../references/framework-playbooks.md` for web, React, Next.js, Tailwind, React Native, Flutter, iOS, and Android notes.
- `../../references/verification-matrix.md` for screenshots, Playwright, container widths, and handoff language.
- `../../references/source-material-index.md` to locate the copied original files under `../../references/source-material/`.

## Required Workflow

1. Map the UI surface: routes, components, styling files, tokens, data states,
   current mobile behavior, and any parallel mobile components.
2. Identify states: idle, hover, pressed, focus-visible, loading, disabled,
   error, success, empty or skeleton, long content, reduced motion, and
   permission or partial-data states when relevant.
3. Choose the smallest clean patch that preserves product meaning and
   improves the responsive behavior at the source of the problem.
4. Verify with checks that can fail. For rendered UI, inspect screenshots or
   browser output at mobile and desktop widths before claiming visual success.
5. Report exactly what was verified and what was not.

## Non-Negotiables

- No `transition-all`.
- No default `ease`, `ease-in`, or generic `ease-in-out` unless the project token maps to it explicitly.
- Every keyboard control needs a visible `focus-visible` state.
- Every clickable control needs a pressed or tactile state.
- Motion changes need reduced-motion behavior.
- Radius, shadow, spacing, color, and motion values should come from existing tokens or a documented token extension.
- Never use `max-height: 9999px` for reveal behavior; use grid rows or measured height.
- Do not use clickable `div` or `span` elements when a semantic button/link is correct.
- Use `tabular-nums` or the project equivalent for metrics, finance values, timers, and dense tables.
- Avoid fixed desktop widths, layout-affecting animation, text overlap, clipped controls, and unbounded horizontal overflow.

## Task Modes

- Audit mode: run the static audit script when useful, inspect real render
  output, rank issues by user impact, and propose or implement focused fixes.
- Repair mode: trace the root cause before patching symptoms. Prefer
  intrinsic layout, wrapping, minmax, container queries, overflow strategy,
  and content hierarchy changes over brittle width overrides.
- Build mode: create the actual usable UI as the first screen. Include
  responsive states, real controls, accessible labels, loading/empty/error
  paths, and mobile-first layout from the start.
- Conversion mode: inventory the desktop surface, preserve core tasks, then
  reflow into mobile navigation, progressive disclosure, bottom actions,
  compact tables/cards, and touch-safe controls without hiding critical work.
- System mode: update tokens, primitives, and shared patterns before
  repeating one-off styling.

## Helpful Scripts

From a repository root:

```bash
python <plugin-root>/scripts/audit_responsive_static.py .
python <plugin-root>/scripts/make_viewport_matrix.py --format markdown
```

The static audit does not replace visual verification. Treat it as a fast
triage pass for common responsive and interaction hazards.
