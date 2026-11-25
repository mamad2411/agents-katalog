---
name: discover-frontend
description: "Self-contained router for bundled frontend skills. Use when working with frontend web or mobile UI tasks and choose the appropriate skill under skill-library/frontend without relying on external skill roots."
---

# Discover Frontend

Self-contained frontend skill router for the bundled `bx-dev` public skill library.

Use this skill when a task involves React, Next.js, UI components, layouts, themes, Tailwind, accessibility, animation, frontend data fetching, Vercel frontend patterns, Remotion, React Native, or general web design quality.

## Bundled Routing Source

From the repository root:

1. Read `skill-library/INDEX.md` for the grouped library overview.
2. Choose from the existing bundled frontend skills listed below.
3. Load the chosen entrypoint at `skill-library/frontend/<skill-name>/SKILL.md`.

Do not reference external skill roots or non-bundled frontend files. This public package is intended to work from the repository checkout alone.

## Existing Bundled Frontend Skills

- `skill-library/frontend/accessibility-design/SKILL.md`
- `skill-library/frontend/discover-frontend/SKILL.md`
- `skill-library/frontend/frontend-design/SKILL.md`
- `skill-library/frontend/native-data-fetching/SKILL.md`
- `skill-library/frontend/react-view-transitions/SKILL.md`
- `skill-library/frontend/remotion-best-practices/SKILL.md`
- `skill-library/frontend/tailwind-design-system/SKILL.md`
- `skill-library/frontend/theme-factory/SKILL.md`
- `skill-library/frontend/ui-ux-pro-max/SKILL.md`
- `skill-library/frontend/vercel-composition-patterns/SKILL.md`
- `skill-library/frontend/vercel-react-best-practices/SKILL.md`
- `skill-library/frontend/vercel-react-native-skills/SKILL.md`
- `skill-library/frontend/web-design-guidelines/SKILL.md`

## Routing Guide

| Need | Use |
|---|---|
| Accessibility audits, keyboard support, ARIA, contrast | `accessibility-design` |
| High-quality web UI design and implementation | `frontend-design` |
| Frontend data fetching strategy | `native-data-fetching` |
| React View Transitions API usage | `react-view-transitions` |
| Remotion video composition | `remotion-best-practices` |
| Tailwind tokens, themes, and design systems | `tailwind-design-system` |
| Theme generation and color modes | `theme-factory` |
| UI/UX pattern, palette, typography, and stack guidance | `ui-ux-pro-max` |
| Component composition patterns | `vercel-composition-patterns` |
| React application best practices | `vercel-react-best-practices` |
| React Native frontend work | `vercel-react-native-skills` |
| General web design guidelines | `web-design-guidelines` |

## Workflow

1. Identify the frontend problem area from the user request.
2. Pick the most specific bundled skill from the routing guide.
3. Read only that skill's `SKILL.md`, plus `skill-library/INDEX.md` if you need the category overview.
4. Apply the selected skill's instructions using the current repository and runtime evidence.
5. Verify the resulting frontend work with the appropriate local check, such as tests, build, lint, browser smoke, screenshots, or accessibility checks.

