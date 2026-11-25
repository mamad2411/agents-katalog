---
name: Design
description: Design and build a clean, responsive interface. Use for pages, components, dashboards, landing screens, or any request about visual design, layout, typography or polish.
---

# Design

Design is editing decisions, not painting decoration. Aim for a screen that feels calm and obvious.

## 1. Read before drawing

- Inspect the project's existing tokens, components and layout first. Extend that language; don't import a second one.
- Identify the audience and the one thing the screen must do.
- Name the hierarchy: primary action, then supporting content, then secondary detail.

## 2. Compose

- **Space** — pick one spacing scale (4 / 8 / 12 / 16 / 24 / 32 / 48) and stay on it. Generous outer margin, tighter inner rhythm.
- **Type** — two weights and three sizes cover most screens. Body at least 14px, line-height 1.5–1.65. Use color and weight for hierarchy, not extra font families.
- **Color** — neutral surfaces, one accent, semantic success/warning/danger. Check contrast: 4.5:1 for body, 3:1 for large text and UI borders.
- **Layout** — a single clear column or a predictable grid. Align edges; avoid centered body text longer than two lines.
- **Motion** — short (120–220ms) and purposeful. Respect `prefers-reduced-motion`.

## 3. Avoid AI-slop

- No purple-to-pink gradient heroes, glowing blobs, floating 3D shapes or glassmorphism on every card.
- No emoji as interface icons. No uppercase tracked-out labels everywhere.
- No fake stats, fake testimonials or lorem ipsum in a real screen.
- Borders and one soft shadow beat heavy decoration. If a visual element has no function, remove it.

## 4. Build

- Semantic HTML first: `header`, `nav`, `main`, `section`, `button`, `label`.
- Style with variables and reusable classes, not one-off inline styles.
- Make it responsive by construction: fluid widths, sensible max-widths, toolbars that wrap, nothing clipped at 360px.
- Keyboard: visible focus, logical order, Escape closes overlays, inputs have labels.

## 5. Verify

- Open the result in a browser, preview or screenshot at a desktop and a narrow width.
- Check overflow, contrast, empty states and long text.
- Fix what looks off before reporting. Describe the final direction in one or two concrete sentences.
