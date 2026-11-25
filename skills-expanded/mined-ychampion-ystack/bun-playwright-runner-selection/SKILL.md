---
name: bun-playwright-runner-selection
description: >-
  Fix the error "Playwright Test did not expect test() to be called here" when a Playwright spec file is
  run with Bun's unit-test runner instead of the Playwright CLI. Use when: (1) a `*.spec.ts` file
  contains `import { test, expect } from '@playwright/test'`, (2) `bun test` was run on that file, and
  (3) the suite fails before any test runs. Run the suite with `bunx playwright test` instead.
---

# Bun: run Playwright specs with the Playwright runner

## Problem

In Bun-based repos it is easy to run a Playwright spec with the wrong runner. Passed to `bun test`, a
file that defines Playwright tests is treated as a Bun unit-test file instead of going to Playwright
Test. The suite fails before any test runs, with an error that points somewhere else.

## Trigger conditions

All of these hold:

- The repo uses Bun for package management and scripts.
- The test file imports from `@playwright/test`.
- It was run with something like `bun test path/to/file.spec.ts`.
- The failure looks like:

```text
Playwright Test did not expect test() to be called here.
Most common reasons include:
- You are calling test() in a configuration file.
- You are calling test() in a file that is imported by the configuration file.
- You have two different versions of @playwright/test.
```

The message invites you to chase duplicate dependencies or bad imports when the only problem is the
runner.

## Solution

1. Confirm the file is a Playwright spec, not a Bun unit test: it imports from `@playwright/test` and
   uses fixtures such as `page` or `request`.
2. Don't run it with `bun test`.
3. Run the Playwright CLI through Bun's package runner:

```bash
bunx playwright test path/to/file.spec.ts
```

4. To pick specific tests, use Playwright's flags, not Bun's (`-t` is a Bun flag):

```bash
bunx playwright test "path/to/file.spec.ts" --grep "test name"
```

5. Keep using Bun for installs and scripts; use the Playwright CLI for Playwright suites. A
   `package.json` script such as `"e2e": "playwright test"` (run with `bun run e2e`) stops the mistake
   from recurring.

## Verification

- The `test()` error is gone.
- Playwright reports the expected number of tests (`Running N tests using M workers`).
- The run ends with Playwright's normal summary (`N passed`).

## Example

Wrong:

```bash
bun test tests/checkout.e2e.spec.ts -t "applies discount"
# error: Playwright Test did not expect test() to be called here.
```

Right:

```bash
bunx playwright test tests/checkout.e2e.spec.ts --grep "applies discount"
# 1 passed
```

## Notes

- This is about runner choice, not a broken Playwright install.
- `bunx` is Bun's equivalent of `npx` or `pnpm exec` for package CLIs, and it honours Node shebangs, so
  `bunx playwright ...` runs the Playwright CLI as intended.
- If the error persists under `bunx playwright test`, then look at the usual Playwright causes: two
  versions of `@playwright/test`, or `test()` called from a file the config imports.
- To keep `bun test` from picking up e2e specs at all, keep them in a folder Bun's runner doesn't scan,
  or point `bun test` at your unit-test paths explicitly.

## References

- https://playwright.dev/docs/intro
- https://bun.sh/docs/pm/bunx
- https://github.com/microsoft/playwright/issues/38343
