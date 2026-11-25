---
name: kb-testing-nextjs
description: Portable testing patterns for Next.js + Vitest + React Testing Library — factory-function mocks around hoisted `vi.mock()`, thenable chainable mocks for Drizzle-style query builders, `ActionResult`-shape assertions over `.rejects.toThrow`, and RTL query priority with `userEvent.setup()`. Use when writing unit or component tests in any Next.js + Vitest project. → `sk-testing-nextjs`
last-verified: 2026-04-23
---

# kb-testing-nextjs — Portable Next.js + Vitest + RTL Patterns

> Stack: Next.js 16+ + Vitest + React Testing Library.
> **Portable** — these patterns work in any Next.js + Vitest project, with or without the Starter Kit.
>
> **Pair:** for kit-shipped infra (exact `vitest.config.ts`, coverage exclusion table, kit-barrel mock targets, `createChain()` full implementation, `ActionResult`-shape rule, `pnpm test*`/`verify` commands) see [`sk-testing-nextjs`](../sk-testing-nextjs/SKILL.md). For universal principles (AAA, FIRST, pyramid theory) see [`kb-testing-patterns`](../kb-testing-patterns/SKILL.md). For E2E / Playwright → [`sk-e2e`](../sk-e2e/SKILL.md).

---

## 1. Factory-function mocks — the Vitest hoisting rule

`vi.mock(path, factory)` is **hoisted** to the top of the file before any imports run. Variables referenced inside the factory must exist at hoist time. This is the single most common source of `ReferenceError` in Vitest tests.

```ts
// ❌ BREAKS — vi.mock hoists above `mockAuth`, which doesn't exist yet
import { auth } from '@/lib/auth';
vi.mock('@/lib/auth', () => ({ auth: mockAuth }));
const mockAuth = vi.fn(); // too late

// ✅ Correct — declare the mock OUTSIDE the factory, wrap inside a function
const mockAuth = vi.fn();
vi.mock('@/lib/auth', () => ({
  auth: () => mockAuth(), // invoked at call time, not at hoist time
}));
```

**The pattern:**

1. `const mockFn = vi.fn()` at module top-level.
2. `vi.mock(path, () => ({ exportName: () => mockFn() }))` — the factory returns an object where each exported function invokes the mock. This indirection is why hoisting doesn't break.
3. Import the module under test AFTER the mocks via top-level `await import()`:

```ts
const { createUser } = await import('@/lib/actions/users');
```

Without the dynamic import, the action module evaluates its own imports before the mocks bind, and you're testing the real module.

---

## 2. React Testing Library — philosophy and query priority

RTL's philosophy: **test behavior, not structure.** Query the DOM the way a user would perceive it. The canonical priority order:

| Priority | Query                           | When                                                    |
| -------- | ------------------------------- | ------------------------------------------------------- |
| 1        | `getByRole('button', { name })` | Any interactive element — buttons, links, inputs        |
| 2        | `getByLabelText`                | Form fields (the label is what the user reads)          |
| 3        | `getByPlaceholderText`          | Inputs without a visible label (rare, discouraged)      |
| 4        | `getByText`                     | Non-interactive content (paragraphs, headings)          |
| 5        | `getByDisplayValue`             | Inputs pre-filled with a known value                    |
| 6        | `getByAltText` / `getByTitle`   | Images, icons with `title`                              |
| 7        | `getByTestId` (**last resort**) | Only when nothing above works; smells of tight coupling |

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('invokes onClick when clicked', async () => {
  const user = userEvent.setup(); // once per test
  const handleClick = vi.fn();

  render(<Button onClick={handleClick}>Save</Button>);
  await user.click(screen.getByRole('button', { name: 'Save' }));

  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

**Rules:**

- `userEvent.setup()` **once per test** — it installs realistic timing/focus/pointer-event behavior. Don't use raw `fireEvent` for user interactions — it skips focus/pointer events the real browser would fire.
- Don't mock the component itself. Mock its **dependencies** (auth, router, feature flags).
- For components that use context providers, wrap with the provider in the test render.

**When to write a component test:**

- Component has `onClick`, form handlers, `useState`, or conditional render → **component test required**.
- Purely presentational (props → JSX, no interaction) → rely on E2E or skip.

---

## 3. Chainable thenable mocks — mocking fluent query builders

Fluent APIs (Drizzle, Prisma, Mongoose query builders) return objects that chain `.where().limit().returning()` and resolve when awaited. Recreating this with nested `vi.fn().mockReturnValue({...})` is noisy and brittle. Use a `thenable` chain helper:

```ts
/**
 * Chainable mock that resolves to `result` at the end of the chain.
 * Supports arbitrary chain calls and is thenable so `await query` works directly.
 */
function createChain(result: unknown = []) {
  const chain: Record<string, unknown> = {};
  const resolve = () => Promise.resolve(result);

  // methods that continue the chain
  for (const m of ['from', 'where', 'limit', 'set', 'values', 'orderBy', 'offset']) {
    chain[m] = vi.fn(() => chain);
  }
  // method that resolves the chain
  chain.returning = vi.fn(() => resolve());
  // thenable — so `await chain` resolves without calling .returning()
  chain.then = (onFulfilled?: (v: unknown) => unknown, onRejected?: (r: unknown) => unknown) =>
    resolve().then(onFulfilled, onRejected);

  return chain;
}
```

**Rules:**

- Use one `createChain(result)` per mock return. For multi-step query flows (select → update → returning) return a **fresh** `createChain` per call — chains are mutable.
- Don't assert on internal chain calls (`expect(chain.where).toHaveBeenCalledWith(...)`) unless the test is specifically about query shape. Assert on observable output.

> Adapt the chain methods to the ORM — Prisma would need `.findMany()`/`.create()` terminators; Mongoose needs `.exec()`. Same thenable trick.

---

## 4. Assert on return shape, not thrown errors

When the code under test uses a wrapper that catches and returns a discriminated union (`{ data }` | `{ error }`), assert on the **shape**, not on throws:

```ts
// ❌ Wrong — the wrapper catches, so nothing propagates
await expect(createUser(input)).rejects.toThrow('UNAUTHORIZED');

// ✅ Right — assert on the returned shape
const result = await createUser(input);
expect(result).toEqual({ error: 'Debes iniciar sesión' });
```

Use `.rejects.toThrow` only for throws from non-wrapped code (pure helpers, raw route handlers without try/catch, etc.).

---

## 5. Pure-function tests — no mocks when there's no side effect

When the unit under test is a pure function (permissions matrix, Zod validator, pure selector), don't mock anything — just call it:

```ts
import { describe, it, expect } from 'vitest';
import { hasPermission, requirePermission } from '@/lib/auth/permissions';

describe('hasPermission', () => {
  it('allows admin to create users', () => {
    expect(hasPermission('admin', 'users', 'create')).toBe(true);
  });

  it('denies user from deleting users', () => {
    expect(hasPermission('user', 'users', 'delete')).toBe(false);
  });

  it('returns false for undefined role', () => {
    expect(hasPermission(undefined, 'users', 'read')).toBe(false);
  });
});

describe('requirePermission', () => {
  it('does not throw when allowed', () => {
    expect(() => requirePermission('admin', 'users', 'create')).not.toThrow();
  });

  it('throws when denied', () => {
    expect(() => requirePermission('user', 'users', 'delete')).toThrow(/Permission denied/);
  });
});
```

> If you find yourself mocking three modules to test a function, the function probably isn't pure — either extract the pure core, or move the test up the pyramid to integration/E2E.

---

## 6. Vitest mocking cheatsheet

| Scope                       | Pattern                                                           |
| --------------------------- | ----------------------------------------------------------------- |
| Module with functions       | `const mockFn = vi.fn(); vi.mock(path, () => ({ fn: mockFn }))`   |
| Module with exported object | `vi.mock(path, () => ({ db: { select: ... } }))`                  |
| Next.js cache               | `vi.mock('next/cache', () => ({ revalidatePath: vi.fn() }))`      |
| Observe a specific export   | `vi.spyOn(module, 'fn').mockResolvedValue(...)`                   |
| Time-dependent code         | `vi.useFakeTimers()` + `vi.setSystemTime(new Date('2026-01-01'))` |
| Reset between tests         | `vi.clearAllMocks()` in `beforeEach`                              |

```ts
beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date('2026-01-15'));
});
afterEach(() => vi.useRealTimers());
```

> Don't mock what you don't transitively own. If your action calls `db.insert()`, mock the DB barrel in your project — **not** `drizzle-orm` itself. Mocking library internals couples tests to implementation details of code you don't control.

---

## 7. Common Vitest + RTL pitfalls

| Pitfall                                                       | Fix                                                                            |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `vi.mock(...)` references a scope variable → `ReferenceError` | Declare `const mockFn = vi.fn()` at module top, wrap inside factory (§1)       |
| Testing a wrapper-caught action with `.rejects.toThrow`       | Assert on `{ error }` shape instead (§4)                                       |
| `vi.mocked(db.insert).mockReturnValue({ values, returning })` | Use a thenable `createChain(result)` helper (§3)                               |
| Tests leak state across files                                 | `vi.clearAllMocks()` in `beforeEach`; global `cleanup()` via `vitest.setup.ts` |
| `fireEvent.click` missing focus/pointer events                | Use `userEvent.setup()` + `user.click(...)`                                    |
| `getByTestId` as the default query                            | Try role/label/text first — testid is last resort                              |
| Module under test imported BEFORE the mocks bind              | Use top-level `await import(...)` after all `vi.mock` calls                    |
| Mocking what you don't own (e.g., `drizzle-orm` internals)    | Mock your own barrel that wraps the library                                    |

---

## 8. Portable commands

```bash
pnpm test                # Vitest run (depending on project setup)
pnpm test:watch          # Watch mode
pnpm test <filter>       # Filter by filename substring
pnpm test:coverage       # Vitest with v8 coverage
```

> Kit projects also ship `pnpm test:e2e`, `pnpm test:e2e:direct`, `pnpm test:e2e:ui`, `pnpm verify` — see [`sk-testing-nextjs`](../sk-testing-nextjs/SKILL.md) §6.

---

## 9. E2E / Playwright — see sibling skill

Portable Playwright fundamentals (storageState auth pattern, `auth.setup.ts`, Page Object Model decisions, selectors strategy) y la infra del kit (e2e-runner con Neon branch isolation, dynamic role iteration, `AUTH_FILES` generation, `createTestUser`) viven en [`sk-e2e`](../sk-e2e/SKILL.md).

No duplicates acá — este skill cubre **unit + component** testing patterns; E2E es dominio de `sk-e2e`.

---

_Cross-reference: [`sk-testing-nextjs`](../sk-testing-nextjs/SKILL.md) for kit-shipped `vitest.config.ts`, coverage exclusion strategy, and kit-barrel mock targets. [`kb-testing-patterns`](../kb-testing-patterns/SKILL.md) for AAA / FIRST / pyramid principles. [`sk-e2e`](../sk-e2e/SKILL.md) for Playwright infra._
