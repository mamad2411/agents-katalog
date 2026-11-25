---
name: developer-quality
description: >-
  Code quality bar for implementation work: linting, formatting, tests, and
  test coverage for new features and bug fixes. Use when frontend-developer or
  backend-developer (or PM) delegates or reviews implementation.
---

# Developer Quality Bar

**Applies to:** `frontend-developer`, `backend-developer`, and any agent implementing application code.

Implementation is not done until **lint passes**, **formatting is clean**, **automated tests pass**, and **new or changed behavior is covered by tests**.

Also follow `.agents/skills/typescript/SKILL.md` and `.agents/skills/clean-code/SKILL.md`.
When shipping testable UI with the optional Next.js skill, add `data-testid` on key elements per `.agents/skills/optional/nextjs-frontend/SKILL.md`.

---

## Mandatory before handoff

1. **Lint** — Run lint for every package you touched; fix all reported issues.
2. **Format** — Format touched files; CI should enforce a format check when configured.
3. **Typecheck** — Ensure TypeScript compiles for affected packages when types or build-affecting code changed.
4. **Tests** — Run the relevant test commands for affected packages; **all must pass** before writing `05-implementation-*.md`.
5. **Coverage** — Add or update automated tests for every **new feature** and **bug fix**. Do not hand off without tests unless PM explicitly scoped test debt in `00-intake.md`.

---

## Test coverage expectations

| Change type                                           | Minimum expectation                                                                 |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **New feature**                                       | Tests that prove the happy path and at least one meaningful edge or validation case |
| **Bug fix**                                           | A regression test that fails on the old behavior and passes with the fix            |
| **Pure logic** (validators, transforms, domain rules) | Unit tests colocated with the module (`*.spec.ts` / equivalent)                     |
| **API endpoints**                                     | Service/controller tests and/or API-level tests; document curl smoke in handoff     |
| **User-facing flows**                                 | E2E specs when the flow is critical or regression-prone                             |

**Do not** skip tests because the change is "small". If a bug could recur, lock it in with a test.

**Do not** rely on QA alone for coverage — developers own tests for the code they ship.

---

## Commands

Document exact commands in `project-context` or the root README. Typical pnpm monorepo pattern:

| Check            | Example                                         |
| ---------------- | ----------------------------------------------- |
| Lint (all)       | `pnpm lint`                                     |
| Lint one package | `pnpm --filter @your-scope/api lint`            |
| Format           | `pnpm format` / `pnpm format:check`             |
| Unit tests       | `pnpm --filter @your-scope/api test`            |
| E2E              | `pnpm test:e2e` (if Playwright pack is enabled) |

If optional Playwright skill is present, see `.agents/skills/optional/playwright-e2e/SKILL.md`.

---

## Handoff documentation

In `05-implementation-frontend.md` or `05-implementation-backend.md`, include:

- **Quality checks** — lint/typecheck commands run and result (pass / N/A)
- **Tests added** — file paths and what each test covers
- **Test commands run** — exact commands and pass/fail

PM should not advance to `/qa-tester` if implementation handoffs omit tests for non-trivial behavior or report failing lint/tests.

---

## PM gate

Before invoking `/qa-tester` after implementation:

- [ ] Developer ran lint on touched packages
- [ ] All automated tests for affected packages pass
- [ ] New features and bug fixes include test coverage (or documented exception in intake)
- [ ] `05-implementation-*.md` lists quality checks and tests added
