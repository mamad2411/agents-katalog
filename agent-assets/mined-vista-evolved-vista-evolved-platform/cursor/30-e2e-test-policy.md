# E2E Test Policy

## One spec file per app

Each application under `apps/` gets exactly **one** Playwright spec file in its `e2e/` directory.
Do NOT create multiple spec files per app. Instead, add new `test.describe()` blocks to the existing spec.

| App | Spec file | Tests |
|-----|-----------|-------|
| `apps/tenant-admin` | `e2e/tenant-admin-crud.spec.mjs` | VistA CRUD, UI rendering, auth |
| `apps/control-plane` | `e2e/operator-console.spec.mjs` | Shell, API proxy, lifecycle, UI |

## Rules

1. **Never create a second spec file** for an app that already has one. Expand the existing file.
2. **Never create throwaway/temporary test files.** If a test was needed for debugging, remove it when done.
3. **Test structure:** Group tests using `test.describe()` blocks by domain (e.g., "Auth", "CRUD", "UI Rendering").
4. **Test against real runtimes:** E2E tests run against live servers and Docker, not mocks.
5. **Cleanup test data:** Tests that create records should use unique timestamps/slugs to avoid collisions.
6. **No excessive waits:** Use `waitForTimeout` only when necessary; prefer `waitForSelector` or Playwright auto-wait.

## When to add tests

- New API route added → add a test in the API describe block
- New UI surface added → add a rendering test in the UI describe block
- New lifecycle action → add to the lifecycle describe block
- Bug fix → add a regression test in the most relevant describe block

## When NOT to add tests

- Documentation-only changes
- CSS-only cosmetic changes
- Comment or rename refactors with no behavioral change
