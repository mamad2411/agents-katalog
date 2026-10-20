---
name: "react-web-best-practices"
description: "React (web, TypeScript + Vite) standards: routing with React Router, state, API layer, styling, code-splitting, accessibility, testing with Vitest + React Testing Library. Use when generating or reviewing a React web app."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# React Web Best Practices (Vite + TS)

## Layout
```
src/
  routes|pages/   components/   hooks/   store/   services/api/
  styles/   types/   main.tsx   App.tsx
vite.config.ts  tsconfig.json  .eslintrc
```

## Standards
- Functional components + hooks; typed props; no `any`.
- Routing: React Router with typed routes + lazy routes (`React.lazy`/`Suspense`) for code-splitting.
- Server state: React Query; local: `useState`/`useReducer`; global: Redux Toolkit/Zustand if needed.
- API client in `services/api/` from `tsa.api_integration`; base URL from `import.meta.env`.
- Styling: CSS Modules / Tailwind / styled-components (declared in tsa). Tokens from `design_source` -> theme.
- Accessibility: semantic HTML, labels, focus management, keyboard nav.
- Performance: memoization, route-level splitting, image optimization.

## Quality gates
- `tsc --noEmit`, ESLint, Vitest green, `vite build` succeeds, no TODO/STUB, every route+endpoint wired.
