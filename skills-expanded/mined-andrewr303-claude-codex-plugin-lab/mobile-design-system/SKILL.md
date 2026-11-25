---
name: mobile-design-system
description: "Use to create, audit, extend, or repair design systems for mobile and responsive UI, including tokens, Tailwind themes, CSS variables, primitives, motion, radius, shadows, typography, and theming."
---

# Mobile Design System

Use this skill when a responsive fix or UI build should happen through
tokens, primitives, or reusable component patterns instead of one-off
styling.

## Required References

Read `../../references/design-system-and-tokens.md` and
`../../references/responsive-audit-checklist.md`.

## System Rules

- Search for `:root`, `--color`, `--radius`, `--shadow`, `--duration`,
  `--ease`, `tailwind.config`, `globals.css`, theme files, and component
  primitives.
- Extend the existing naming system instead of inventing a parallel one.
- Add motion tokens before adding transitions if the project has no motion
  vocabulary.
- Keep component-level values proportional to component size.
- Prefer layered shadows or hairline rings over one-off drop shadows.
- Document any new token with the behavior it unlocks and where it is used.
- Do not introduce a new styling framework to solve a local styling problem.
