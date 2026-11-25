---
description: 
globs: 
alwaysApply: true
---
# Frontend Rules (FSD/FCA, Thorough, Terse)

## Architecture
- Use FSD/FCA: `app/`, `pages/`, `processes/`, `widgets/`, `features/`, `entities/`, `shared/`.
- Each slice: colocate components, hooks, types, utils; expose only via `index.ts`/`public-api.ts`.
- Only import from other slices' public API.
- No cross-boundary imports (e.g., features→widgets).
- Kebab-case for files/folders. One export per file. Name files after export.
- Functional components only, as `const`. Event handlers: `handleX`.
- Split components >100 lines. No business logic in UI.
- Use absolute imports from `src/` and `@ui-kit`.

## State & Data
- Use hooks/context for state. Local state for local, context for shared.
- RO-RO for multi-param/return functions. Prefer default params.
- Types/interfaces colocated or in `types/`. No `any` (except temp stubs, remove before merge).
- Use `as const` for literals.

## UI & Styling
- Use MUI and SCSS modules. No Tailwind, CSS-in-JS, or styled-components.
- Only MUI/SCSS in `className`. No `class:` directive. Inline styles only in MUI `sx`.
- Use semantic HTML. All interactive elements: `tabIndex`, `aria-label`, `role`, `onClick`, `onKeyDown`.

## Logic & Functions
- All functions as `const`, verb+object names. No inline JSX functions unless trivial.
- Use map/filter/reduce. Early returns. No blank lines in functions.
- Magic values as UPPERCASE constants, in `constants/` or `constants.ts`.

## Testing
- Use Vitest. Unit test all components/hooks/utils. Add accessibility tests. E2E/integration for flows.
- Arrange-Act-Assert. Clear test var names. No skipped/incomplete tests.

## Docs
- JSDoc for all public APIs. Document props/returns/side effects.

## Misc
- No TODOs, stubs, or dead/commented code. All code must be complete.
- Standardize exports: named except for pages/stories.

## FSD/FCA Details
- Slices: `app/` (entry/routing), `pages/` (routes), `processes/` (cross-feature flows), `widgets/` (page UI), `features/` (feature logic/UI), `entities/` (domain models/UI), `shared/` (utils, types, design system).
- Each slice: public API only. Never import internals from another slice.

## UI-Kit
- Use `@ui-kit` for shared UI. Extend via composition only. All new UI: Storybook story required.

## State
- Prefer context/hooks. No new state libs without team OK.

## Error Handling
- Use error boundaries. Show user-friendly error UI. Handle async errors with try/catch.

## Async/Data
- Use consistent fetch (fetch/axios/React Query/SWR). Always handle loading/error. Cache as needed.

## Performance
- Use `React.memo`, `useMemo`, `useCallback` for perf. Lazy load/code split big components/pages.

## Env Vars
- UPPERCASE, prefixed (e.g., `VITE_APP_`). Document in `.env.example`.

## Security
- Sanitize/validate all user input. Never interpolate user input into DOM. No sensitive data in frontend.

## Deprecation
- Mark deprecated code with `@deprecated` JSDoc. Remove after transition.

## Accessibility Testing
- Use axe/jest-axe in CI/local.

## CI/CD
- Lint, format, test in CI. Block merges on failure.

## Code Review
- All code reviewed by another dev. Use PR template with checklist.

## Constants
- All constants in separate files (`constants/` or `constants.ts`). UPPERCASE. Import where needed.

## Advanced
- TypeScript: strict mode, no implicit any, no unuseds.
- ESLint + Prettier. No `// @ts-ignore` or `// eslint-disable` without reason.
- Keep deps up to date (Renovate/Dependabot). No deep node_modules imports.
- Components: minimal, typed props. Use unions for variants. Avoid prop drilling.
- Custom hooks: prefix `use`, colocate, no side effects outside `useEffect`.
- i18n: externalize all user strings. Use i18n lib if needed.
- Analytics: isolate in module, not UI.
- Logging: use central util. No `console.log`/`error` except for errors.
- Images/assets: use modern formats, optimize, lazy load below fold.
- Responsive: test all breakpoints, mobile-first.
- Perf budgets: enforce in CI.
- CSP headers. Validate all external data.
- Releases: semver, tag, maintain CHANGELOG.
- Onboarding: keep guide and ADRs up to date.
- No default exports. Use named exports only.
- Windows PowerShell doesn't support && for chaining commands like bash.







