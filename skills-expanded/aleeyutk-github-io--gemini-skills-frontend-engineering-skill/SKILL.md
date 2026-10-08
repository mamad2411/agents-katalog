---
name: frontend-engineering
description: Senior frontend engineering expertise for React, TypeScript, Vite, Tailwind CSS, routing, reusable components, responsive implementation, performance, and maintainable portfolio architecture.
---

# Frontend Engineering Skill

Act as a senior frontend engineer.

Primary technologies:

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router where already used

## First Rule

Inspect the existing codebase before changing architecture.

Do not replace working technology without a compelling reason.

## Architecture

Prefer:

- reusable components
- typed project data
- centralized content
- clear component boundaries
- predictable props
- composable UI

Avoid:

- giant components
- duplicated project markup
- deeply nested conditionals
- unnecessary abstraction
- global state without need
- unused dependencies

## TypeScript

Prefer explicit types for:

- projects
- navigation
- case studies
- technology lists
- component props

Avoid:

any

unless there is a documented reason.

## React

Prefer:

- functional components
- hooks
- composition
- semantic HTML

Avoid unnecessary effects.

Do not use useEffect for derived values.

## Styling

If Tailwind is already present:

Use Tailwind consistently.

Do not mix several styling systems without reason.

Create reusable design tokens where practical.

## Responsive

Test:

320
375
390
430
768
1024
1280
1440
1920

Check for:

- overflow
- broken grids
- text wrapping
- image cropping
- navigation issues
- oversized typography

## Performance

Optimize:

- images
- fonts
- component rendering
- bundle size
- unnecessary dependencies

Do not optimize prematurely.

## Accessibility

Every interactive element must be keyboard accessible.

Use semantic elements.

Buttons should be buttons.

Links should be links.

Images require meaningful alt text.

Forms require labels.

Focus states must be visible.

## Routing

If project case studies use routes:

Verify every route.

Ensure GitHub Pages deployment does not break routing.

## Implementation Rule

Before changing an existing component:

1. inspect it
2. understand dependencies
3. identify what can be preserved
4. modify minimally
5. test

Never rewrite simply for stylistic preference.
