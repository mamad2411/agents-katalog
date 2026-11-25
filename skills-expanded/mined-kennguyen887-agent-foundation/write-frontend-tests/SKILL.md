---
name: write-frontend-tests
description: Use when writing frontend tests — a test-worthiness gate first (no 1:1 per-file test mirroring), then Jest + React Testing Library for components/hooks/utils that earn a test, and Cypress + Cucumber for e2e user flows. Where tests live, what to test, mocking the router, and the lint/type/test gates. React/Next.js reference.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Write frontend tests

Two layers; pick by what you're verifying. principle → **▸ Example (Jest/RTL/Cypress)** → **▸ Other stacks**.

| Layer | Tool | For |
|---|---|---|
| Unit / component | Jest + React Testing Library | utils, hooks, component behavior in isolation |
| E2E | Cypress + Cucumber (BDD) | real user flows through the running app |

## 0. Gate — does this deserve a test? (test behaviors, not files)
A suite maps to **behaviors/contracts, not the file tree**. Never create a test file 1:1 with a
source file by default — per-util mirror tests (`foo.utils.ts` → `foo.utils.test.ts`) bury real
failures, slow every run, and are maintained forever.
- **Direct util/hook test only when** the logic is genuinely complex AND matters (money, dates,
  parsing, non-trivial business rules) or it pins a regression that actually occurred.
- **Skip it when** a component/page/e2e test already exercises the behavior, or the code is trivial
  glue (mapping, prop plumbing, re-exports) whose breakage is instantly visible in dev.
- Prefer proving a util **through the component that uses it**; a separate util test duplicating
  that coverage is junk. When in doubt → don't write it ("Test only what matters", `~/.claude/CLAUDE.md`).

## 1. Unit / component (Jest + RTL)
- **Colocate** `*.test.ts(x)` next to source (or under `src/test/`). Test **behavior through the
  public surface**: render the component, query by role/text, fire user events, assert what the user
  sees — not internal state. Pure utils/hooks that pass the §0 gate are tested directly.
- **Mock the framework + externals only:**
  `jest.mock('next/router', () => ({ useRouter: () => ({ query: {} }) }))`, mock service classes;
  never mock the unit under test.
- **AAA + specific assertions** (`toEqual`/`toMatchObject` with real expected values, not `toBeTruthy()`).
  ```ts
  describe('convertObjectToArray', () => {
    it('flattens primitive values', () => {
      expect(convertObjectToArray({ a: 1, b: 'x' })).toEqual(['a', '1', 'b', 'x']);
    });
  });
  ```
  ▸ *Other stacks:* Vitest + RTL — identical patterns.

## 2. E2E (Cypress + Cucumber)
- **Gherkin feature files** under `cypress/e2e/<feature>/*.feature` describe flows in
  Given/When/Then; **step definitions** implement them; `Scenario Outline` + `Examples` cover input
  variations. Keep **API helpers** in `cypress/services/`, **test data** in `cypress/constants/`,
  and custom commands in `cypress/support/`.
  ```gherkin
  Scenario: Create a listing
    Given User logged in
    When User submits the new-listing form
    Then The listing appears in the list
  ```
  ▸ *Other stacks:* Playwright (+ optional BDD) — same user-flow-level coverage.

## 3. Gates
Lint/format = **Biome** (warning-first rollout, promoted to errors over time). A git-hook runner
(e.g. lefthook) runs `biome check`/`format` on staged files pre-commit, and `type-check` + `jest`
pre-push. Run `pnpm test` (unit) and the e2e suite before opening a PR.

## Verification
- Important new behavior is covered at the outermost sensible layer (component via RTL; Cypress for
  a user-facing flow); any direct util/hook test passes the §0 gate — no 1:1 mirror files, no
  mock-only tests. Tests assert observable behavior with specific values, not truthiness.
- `pnpm type-check`, `pnpm test`, and Biome all pass.

## Related
- `structure-a-frontend-app` · `write-frontend-code` · `write-unit-tests` (backend equivalent).
