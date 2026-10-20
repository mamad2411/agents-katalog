---
name: biswodip-design-review
description: Review or build a UI so it is complete across every state, responsive, accessible, purposeful in motion and free of generic AI styling and slop copy, using the Taste, Emil Kowalski and No AI Slop skills. Use when asked to design, redesign, polish, improve the UI or UX, check accessibility, or make an interface not look AI-generated.
license: Apache-2.0
metadata:
  author: Biswodip Goj
  version: 2.2.0
  homepage: https://github.com/Biswadipgoj
---
# Design review — complete, accessible, and not obviously AI-made

Phase 6. Applies to any meaningful UI change. It never overrides security, correctness, accessibility or performance.

## Integrations

**Taste** — `design-taste-frontend` (new UI), `redesign-existing-projects` (audit before changing), `minimalist-ui`, `high-end-visual-design`, `full-output-enforcement`.
**Emil Kowalski** — `emil-design-eng`, `animate`, `review-animations`, `improve-animations`, `pick-ui-library` (before adding any UI dependency), `mobile-native`.
**No AI Slop** — `no-ai-slop` for every word that ships.

They are guidance, never permission to add visual complexity.

## Pipeline

1. **Understand the task** — the user's job and the business goal, not the screen.
2. **Audit what exists** — components, spacing, type, colour, states, patterns. Do not replace working UI blindly.
3. **Decide intent** — hierarchy, density, composition, motion. One direction, chosen deliberately.
4. **Build the smallest token/primitive set** the work needs.
5. **Implement every state** — loading, slow, empty, partial, large, error, validation, auth expiry, permission denied, rate limited, retry, duplicate submit, offline, success.
6. **Responsive with real content** — mobile, tablet, desktop; long text; localisation expansion.
7. **Review motion** — enter, exit, hover, focus, press, transition. Consistent easing and duration families, compositor-friendly `transform`/`opacity`, nothing perpetual, nothing that delays the task.
8. **Anti-slop pass** — remove meaningless gradients, glassmorphism, decorative 3D, random animation, fake dashboards, fake data, badge noise, fake progress.
9. **Copy pass** — `no-ai-slop`: lead with the point; actionable errors; no puffery ("enterprise-grade"), no weasel attribution, no fake-profound endings.
10. **Accessibility** — keyboard path, visible focus and sane order, semantic HTML, labelled fields, announced errors, WCAG 2.2 AA contrast, 24×24 min touch targets (44 preferred), accessible dialogs (trap, return, Escape), live regions, 200% zoom reflow, `prefers-reduced-motion` with an equally usable experience. Automated checks find a fraction — do the manual keyboard pass.
11. **Performance** — bundle impact, image sizes, layout shift, animation cost, unnecessary client JS.
12. **Security and regression** — visual work never becomes the authorization path; optimistic UI never implies a completed financial or security operation; business behaviour unchanged.

## Never

Fake data to fill a screen · fake loading percentages · fake analytics · "AI-powered" labels with nothing behind them · client-side checks described as authorization · animation hiding weak information architecture · a design system package where a few tokens would do.

## Exit gate

- [ ] Every interaction has real loading, empty, error and success states.
- [ ] Keyboard-only walkthrough done.
- [ ] Reduced motion verified.
- [ ] Copy passed through `no-ai-slop`.
- [ ] Screenshots or notes recorded as evidence.

Detail: `references/06-design-engineering-and-distribution.md` §14.3 (12-step pipeline) and §15.3 (25-state completeness gate). Procedure: `lifecycle/06-design.md`.
