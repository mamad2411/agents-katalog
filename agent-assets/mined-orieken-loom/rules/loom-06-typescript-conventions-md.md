---
paths:
  - "**/*.ts"
---
# TypeScript Conventions

General TypeScript packaging, tooling, and testing-library conventions. Vue-component-specific rules
(Composition API, Tailwind, composables) live separately in the Vue frontend rules. Saturday (E2E/UI) and
Sunday (API) framework patterns — Vitest, Playwright, the `api` fixture, Cucumber.js — live in
`shared/rules/testing-conventions.md`; this file doesn't restate them, only adds what wasn't covered
there yet: fake-data and factory libraries.

## Project Tooling
- **Package manager**: pnpm, monorepo-first (workspaces).
- **Linter/formatter**: ESLint + Prettier. Complexity rule capped at 6 (enforces the framework-wide
  `< 7` cyclomatic complexity rule — see `shared/rules/design-principles.md`).
- **Type strictness**: `strict: true` in `tsconfig.json`, no raw `any` (see
  `shared/rules/architecture-guardrails.md` #4 — use `unknown` with runtime narrowing/Zod validation
  instead).

## Testing & QA Tooling
- **Unit testing framework**: Vitest (see `testing-conventions.md` — already the established default
  for both Saturday and Sunday).
- **Fake/synthetic data (faker-equivalent)**: [`@faker-js/faker`](https://fakerjs.dev/) — NOT the
  original `faker`/`faker.js` npm package, which was deliberately sabotaged and unpublished by its
  original author in 2022. `@faker-js/faker` is the actively maintained community fork and the correct
  current choice.
- **Factories / fixtures (fishery-equivalent)**: [`fishery`](https://github.com/thoughtbot/fishery) —
  pair with `@faker-js/faker` inside factory definitions for realistic generated field values
  (`Factory.define<User>(() => ({ name: faker.person.fullName(), ... }))`).
- **E2E / API testing**: Playwright — official binding, already the framework default (see
  `testing-conventions.md`).
- **Mutation testing** (ADR-008 clause 2): StrykerJS (`@stryker-mutator/core`) — a candidate, **not yet verified** against a
  real project. Verify before relying on its score: a mutant that did not compile, or timed out,
  must never be counted as killed.
- **Performance testing**: k6 — native JS/TS test scripts, no binding needed.
- **Reporting**: Cucumber JSON output feeding the Friday dashboard (see `testing-conventions.md`'s
  Reporting Pipeline section and `shared/rules/approval-gates.md` gate #1); Playwright's own HTML
  reporter for ad-hoc local E2E runs outside the full pipeline.
