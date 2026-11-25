---
name: "react-web-test-stabilization"
description: "Stabilize React web tests (Vitest/Jest + React Testing Library): provider wrappers, router/query mocks, async findBy/waitFor, MSW for network. Use during build/validation when web tests fail."
version: 1
created: "2026-06-27"
updated: "2026-06-27"
---

# React Web Test Stabilization (Vitest/Jest + RTL)

- Use `renderWithProviders` wrapping Router + QueryClient + store + theme.
- Network: MSW handlers shaped from `tsa.api_integration`; assert correct base URL/endpoint/method.
- Async: prefer `findBy*`/`waitFor`; `await userEvent...`; fake timers flushed.
- Router: use `MemoryRouter`/`createMemoryRouter` with the route under test; assert navigation.
- Coverage: per-route component tests + integration tests for each requirement.json scenario.
- Gate: `tsc --noEmit` + ESLint + tests + `vite build` before success.

## ESM / dynamic imports (common HARD failure)
- Never use `await import('...')` in a Jest test — it throws `A dynamic import callback was invoked without --experimental-vm-modules`. Use a static top-of-file import; to reset modules use `jest.resetModules()` + `require()`. Vitest supports dynamic import natively, but prefer static imports regardless. If dynamic ESM under Jest is unavoidable: run `node --experimental-vm-modules node_modules/.bin/jest` + set `extensionsToTreatAsEsm`.
