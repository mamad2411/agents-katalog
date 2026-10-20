---
description: Vitest and Playwright testing standards
globs:
  - "**/*.spec.ts"
  - "**/*.test.ts"
  - "**/e2e/**"
  - "**/vitest.config.*"
  - "**/playwright.config.*"
alwaysApply: false
---

# Testing

## Purpose

Define what to test, how to test it, and what not to waste CI time on — high signal, low brittleness.

## Required patterns

### Tooling

| Scope | Tool | Location |
|-------|------|----------|
| API unit | Vitest | `apps/api/**/*.spec.ts` |
| Web unit | Vitest | `apps/web/**/*.test.ts` |
| E2E | Playwright | `apps/web/e2e/` |

- Run full suite: `pnpm test` (Turbo across workspace).
- E2E in CI runs after the quality job — pipeline shape is owned by `infra.mdc`.

### API unit tests

- Test **services** and pure functions — not Nest wiring unless integration is explicitly needed.
- Use `@nestjs/testing` to build a testing module when the service has injected dependencies.
- Mock `PrismaService` at the method level; assert calls and return values.
- File naming: `<name>.service.spec.ts` beside the service.

### Web unit tests

- Test `lib/` helpers, formatters, and non-trivial client utilities.
- Do not snapshot entire component trees.

### E2E tests

- Cover critical user journeys (auth, checkout, core CRUD) — not every visual variant.
- Use Playwright locators: `getByRole`, `getByLabel`, `getByText` before `data-testid`.
- Set base URL from env (`NEXT_PUBLIC_APP_URL`); CI sets `CI=true`.

### PR gate

Test commands run as part of the PR gate defined in `infra.mdc`.

## Forbidden patterns

- Snapshot tests of large HTML/JSON blobs.
- Testing framework internals, private methods, or implementation details that change during refactors.
- Flaky tests relying on `setTimeout` without `waitFor` / Playwright auto-wait.
- Hitting production APIs or real external services in unit tests.
- Skipping tests with `.skip` in committed code without a linked issue and expiry plan.
- E2E tests that depend on manual seed data not created in test setup.

## Implementation expectations

- Prefer **one logical assertion per behaviour** — multiple `expect` calls for the same act are fine.
- Use factories or minimal inline fixtures; no shared mystery `test-data.json` without documentation.
- For async service tests: `await expect(promise).rejects.toThrow(...)` for error paths.
- New business rules in services require at least one happy-path and one failure-path test.
- Database integration tests: only in CI with service containers or explicit test DB — not against developer production DBs.

## Consistency expectations

- Follow `apps/api/src/features/health/health.service.spec.ts` as the API test template.
- Follow `apps/web/src/lib/api.test.ts` for web unit test style.
- Follow `apps/web/e2e/home.spec.ts` for E2E structure.

## Examples

**Good — service unit test**

```typescript
describe('OrdersService', () => {
  it('returns null when order not found', async () => {
    prisma.order.findUnique.mockResolvedValue(null);
    await expect(service.findById('missing')).resolves.toBeNull();
  });
});
```

**Bad — testing controller decorator metadata**

```typescript
it('should have Get decorator', () => { /* ❌ no value */ });
```

**Good — Playwright**

```typescript
test('home shows platform title', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
});
```
