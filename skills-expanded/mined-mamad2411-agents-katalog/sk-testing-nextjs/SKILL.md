---
name: sk-testing-nextjs
description: Kit-shipped Vitest infrastructure for the TimeKast Starter Kit — the `vitest.config.ts` jsdom + 4-way `@` alias + v8 coverage exclusions, `vitest.setup.ts` RTL wiring, the 3-layer pyramid layout, and factory-function mock targets for kit barrels (`@/lib/auth`, `@/lib/db/drizzle`, `@/lib/db/schema/**`, `next/cache`). Use when writing unit or component tests that mock kit auth or DB. → `kb-testing-nextjs`
last-verified: 2026-04-23
---

# sk-testing-nextjs — Kit-shipped Testing Infrastructure

> **Kit-shipped — not portable.** Travels with the TimeKast Starter Kit. Grounded in real files: `vitest.config.ts`, `vitest.setup.ts`, `tests/unit/**`, `tests/e2e/**`, `scripts/tools/e2e-runner.ts`, `@/lib/auth`, `@/lib/auth/permissions`, `@/lib/db/drizzle`, `@/lib/db/schema/**`.
>
> **Pair:** for portable testing patterns (AAA, pyramid theory, generic Vitest mocking techniques, RTL philosophy) see [`kb-testing-nextjs`](../kb-testing-nextjs/SKILL.md) + [`kb-testing-patterns`](../kb-testing-patterns/SKILL.md). For E2E / Playwright infra → [`sk-e2e`](../sk-e2e/SKILL.md). For the action patterns under test → [`sk-api`](../sk-api/SKILL.md) / [`kb-api`](../kb-api/SKILL.md). For the DB helpers → [`sk-db`](../sk-db/SKILL.md).

---

## 1. Vitest config (what the kit ships)

The repo's `vitest.config.ts` is already set up. **Don't re-invent it.** Key decisions:

```ts
// vitest.config.ts
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.ts'],
    include: ['**/*.test.{ts,tsx}'],
    exclude: ['node_modules', '.next', 'tests/e2e'],
    coverage: {
      provider: 'v8',
      include: ['src/**', 'config/**'],
      exclude: [
        /* UI layer → E2E, DB → E2E, auth config → E2E, shadcn primitives */
      ],
    },
  },
  resolve: {
    alias: {
      '@/components': path.resolve(__dirname, './src/components'),
      '@/lib': path.resolve(__dirname, './src/lib'),
      '@/config': path.resolve(__dirname, './src/config'),
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

```ts
// vitest.setup.ts
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';
afterEach(() => cleanup());
```

**Coverage exclusion strategy** (already documented inline in `vitest.config.ts`):

| Excluded from unit coverage | Tested by           |
| --------------------------- | ------------------- |
| React components (`*.tsx`)  | E2E (Playwright)    |
| `src/app/api/**`            | E2E (Playwright)    |
| Pages / layouts             | E2E (Playwright)    |
| `src/lib/db/**`             | E2E (Neon branches) |
| `auth.ts` / `auth.config`   | E2E (auth flows)    |
| shadcn primitives           | Library itself      |

Unit tests cover: `config/`, `src/lib/actions/helpers`, `src/lib/validations/`, `src/lib/email/templates/`, `src/lib/utils/`, `src/lib/auth/permissions`, `src/lib/logger`.

### Directory layout (real, per-kit)

```
tests/
  unit/                  # Vitest (jsdom) — `pnpm test` runs these
    components/          # RTL component tests
    notifications/       # feature-grouped when they grow
    *.test.ts(x)
  e2e/                   # Playwright — `pnpm test:e2e` runs these
  fixtures/              # E2E auth states, RBAC helpers
  global-setup.ts        # Playwright
  global-teardown.ts     # Playwright
```

> There is **no `tests/integration/`** and **no `tests/factories/`** directory in this repo. Unit tests mock the DB; DB-touching flows are covered by E2E against Neon preview branches.

---

## 2. Server Action tests — factory-function mocks (house style)

Pattern used across the repo (`tests/unit/helpers.test.ts`, `tests/unit/notifications/*`). Mock the kit's `withAuth`/`withSelf` upstream dependencies — auth, permissions, cache — so each test controls the return value:

```ts
// tests/unit/lib/actions/users.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { z } from 'zod';

// --- Mocks (hoisted by vi.mock) ---------------------------------------------
const mockAuth = vi.fn();
vi.mock('@/lib/auth', () => ({
  auth: () => mockAuth(),
}));

const mockRequirePermission = vi.fn();
vi.mock('@/lib/auth/permissions', () => ({
  requirePermission: (...args: unknown[]) => mockRequirePermission(...args),
}));

vi.mock('next/cache', () => ({ revalidatePath: vi.fn() }));

// --- Import AFTER mocks ------------------------------------------------------
const { createUser } = await import('@/lib/actions/users');

// --- Helpers -----------------------------------------------------------------
function mockSession(overrides?: Partial<{ id: string; role: string; email: string }>) {
  return {
    user: {
      id: overrides?.id ?? 'user-123',
      role: overrides?.role ?? 'admin',
      email: overrides?.email ?? 'admin@test.com',
      ...overrides,
    },
  };
}

// --- Tests -------------------------------------------------------------------
describe('createUser', () => {
  beforeEach(() => vi.clearAllMocks());

  it('returns error when not authenticated', async () => {
    mockAuth.mockResolvedValue(null);
    const result = await createUser({ name: 'Test', email: 'test@test.com' });
    expect(result).toEqual({ error: 'Debes iniciar sesión' });
  });

  it('returns error when no permission', async () => {
    mockAuth.mockResolvedValue(mockSession({ role: 'user' }));
    mockRequirePermission.mockImplementation(() => {
      throw new Error('Permission denied');
    });
    const result = await createUser({ name: 'Test', email: 'test@test.com' });
    expect(result.error).toContain('No tienes permiso');
  });

  it('returns data on success', async () => {
    mockAuth.mockResolvedValue(mockSession());
    mockRequirePermission.mockImplementation(() => {});
    const result = await createUser({ name: 'Test', email: 'test@test.com' });
    expect(result.data).toBeDefined();
  });
});
```

**Rules (kit-specific):**

- Declare `const mockFn = vi.fn()` **outside** the `vi.mock()` call. `vi.mock` is hoisted — variables captured inside the factory must exist at hoist time.
- Mock at the kit's module boundary (`@/lib/auth`, `@/lib/auth/permissions`, `@/lib/db/drizzle`, `next/cache`) — not internals.
- Import the action under test **after** the mocks via `await import(...)` at top level, so mocks bind before the module initializes.
- Assert on the **`ActionResult` shape** (`{error}` / `{data}`), not on thrown errors — `withAuth`/`withSelf` catch internally and return the error as data. Use `.rejects.toThrow` only for throws from non-action code.
- `vi.clearAllMocks()` in `beforeEach` — otherwise call history accumulates across tests.

---

## 3. Mocking Drizzle `db` — `createChain()` thenable helper

Drizzle's query builder returns chainable objects ending in `await`. Recreating the chain with `vi.fn().mockReturnValue({...})` is noisy and brittle. Use the repo's `createChain` pattern (see `tests/unit/notifications/notification-service.test.ts`):

```ts
import { describe, it, expect, vi, beforeEach } from 'vitest';

const mockSelect = vi.fn();
const mockInsert = vi.fn();
const mockDelete = vi.fn();

/**
 * Chainable mock that resolves to `result` at the end of the chain.
 * Supports .from / .where / .limit / .set / .values / .returning / .orderBy / .offset
 * and is thenable so `await query` works directly.
 */
function createChain(result: unknown = []) {
  const chain: Record<string, unknown> = {};
  const resolve = () => Promise.resolve(result);

  chain.from = vi.fn(() => chain);
  chain.where = vi.fn(() => chain);
  chain.limit = vi.fn(() => chain);
  chain.set = vi.fn(() => chain);
  chain.values = vi.fn(() => chain);
  chain.returning = vi.fn(() => resolve());
  chain.orderBy = vi.fn(() => chain);
  chain.offset = vi.fn(() => chain);
  chain.then = (onFulfilled?: (v: unknown) => unknown, onRejected?: (r: unknown) => unknown) =>
    resolve().then(onFulfilled, onRejected);

  return chain;
}

vi.mock('@/lib/db/drizzle', () => ({
  db: {
    select: (...args: unknown[]) => mockSelect(...args),
    insert: (...args: unknown[]) => mockInsert(...args),
    delete: (...args: unknown[]) => mockDelete(...args),
  },
}));

// Schema modules referenced by the code under test must also be mocked —
// Drizzle schemas import postgres-js at module load, which jsdom can't run.
vi.mock('@/lib/db/schema', () => ({
  users: { id: 'id', email: 'email', name: 'name' },
}));

describe('someService', () => {
  beforeEach(() => vi.clearAllMocks());

  it('selects users by email', async () => {
    mockSelect.mockReturnValue(createChain([{ id: 'u-1', email: 'a@b.com' }]));

    const result = await findUserByEmail('a@b.com');

    expect(result).toEqual([{ id: 'u-1', email: 'a@b.com' }]);
    expect(mockSelect).toHaveBeenCalled();
  });

  it('inserts and returns the new row', async () => {
    mockInsert.mockReturnValue(createChain([{ id: 'u-2' }]));
    // ...
  });
});
```

**Rules:**

- Mock **every schema module** imported by the code under test (`@/lib/db/schema`, `@/lib/db/schema/notifications`, etc.). Schemas transitively import the Postgres driver, which crashes in jsdom.
- For queries with `.returning()` or final `.limit()`, `createChain(result)` covers both — the result resolves at `.returning()`, or when awaited directly.
- For multi-step query flows (select → update → returning) return a **fresh** `createChain` per mock return — chains are mutable.
- Don't assert on internal chain calls (`expect(chain.where).toHaveBeenCalledWith(...)`) unless the test is specifically about query shape. Assert on observable output.

---

## 4. Component tests — kit's RTL setup

Pattern used in `tests/unit/components/button.test.tsx` (RTL wired via `vitest.setup.ts`):

```tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '@/components/ui/button';

describe('Button', () => {
  it('renders with the provided label', () => {
    render(<Button>Save</Button>);
    expect(screen.getByRole('button', { name: 'Save' })).toBeInTheDocument();
  });

  it('invokes onClick when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(<Button onClick={handleClick}>Save</Button>);
    await user.click(screen.getByRole('button', { name: 'Save' }));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not invoke onClick when disabled', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(
      <Button onClick={handleClick} disabled>
        Save
      </Button>
    );
    await user.click(screen.getByRole('button', { name: 'Save' }));

    expect(handleClick).not.toHaveBeenCalled();
  });
});
```

**Kit-specific rules:**

- `cleanup()` is wired in `vitest.setup.ts` via `afterEach` — no need to call it manually.
- `@testing-library/jest-dom/vitest` matchers are imported once in setup — don't re-import per test.
- For components that use `useFormContext` or other kit providers, wrap with the provider in the test render.

> Behavioral rules (query by role, userEvent.setup, test behavior not structure) are portable — see [`kb-testing-nextjs`](../kb-testing-nextjs/SKILL.md) §2.

---

## 5. Schema-module mocking — avoid Postgres driver in jsdom

Drizzle schemas (`@/lib/db/schema/*`) transitively import the Neon / Postgres driver, which throws in jsdom. When the code under test imports schema tables, mock the schema module with a plain object whose keys mirror column names:

```ts
vi.mock('@/lib/db/schema', () => ({
  users: { id: 'id', email: 'email', role: 'role', isActive: 'is_active' },
}));

vi.mock('@/lib/db/schema/notifications', () => ({
  notifications: {
    id: 'id',
    userId: 'user_id',
    title: 'title',
    body: 'body',
    channels: 'channels',
    read: 'read',
    createdAt: 'created_at',
  },
  notificationPreferences: {
    userId: 'user_id',
    category: 'category',
    enabled: 'enabled',
  },
}));
```

> String values ('id', 'user_id'...) are placeholders — the chainable `db` mock ignores them. Only the **shape** matters so that `eq(users.id, ...)` etc. don't crash on `undefined.id`.

---

## 6. Commands (kit-specific)

```bash
pnpm test                # Vitest run (unit + component, jsdom)
pnpm test:watch          # Watch mode
pnpm test <filter>       # Filter by filename substring
pnpm test:coverage       # Vitest with v8 coverage
pnpm test:e2e            # tsx scripts/tools/e2e-runner.ts (wraps Playwright with env + seed)
pnpm test:e2e:direct     # Raw Playwright (skip the wrapper)
pnpm test:e2e:ui         # Playwright UI mode
pnpm verify              # lint + typecheck + test (DoD gate)
```

> `pnpm test:e2e` uses a **custom runner** (`scripts/tools/e2e-runner.ts`) that seeds the DB, sets env flags, and invokes Playwright (see [`sk-e2e`](../sk-e2e/SKILL.md)). For ad-hoc debugging use `test:e2e:direct` or `test:e2e:ui`.

---

## 7. Kit-specific pitfalls

| Pitfall                                                                 | Fix                                                                       |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Schema import crashes jsdom (`Cannot find module '@neondatabase/...'`)  | Mock `@/lib/db/schema/*` with plain objects (§5)                          |
| Test uses `.rejects.toThrow('UNAUTHORIZED')` for a `withAuth` handler   | Assert `{ error: '...' }` instead — `withAuth` catches and returns        |
| `vi.mocked(db.insert).mockReturnValue({ values: ..., returning: ... })` | Use `createChain(result)` (§3) — cleaner and matches real `await`         |
| `@testing-library/jest-dom` matchers not found                          | Already wired in `vitest.setup.ts` — don't re-import per test             |
| Component test for a shadcn primitive                                   | Don't — shadcn primitives are library-tested; test the wrapper, not `ui/` |

---

_Cross-reference: [`kb-testing-nextjs`](../kb-testing-nextjs/SKILL.md) for portable patterns (generic Vitest mocking, RTL philosophy, AAA, pyramid). [`kb-testing-patterns`](../kb-testing-patterns/SKILL.md) for universal testing principles. [`sk-e2e`](../sk-e2e/SKILL.md) for the `e2e-runner.ts` wrapper. [`sk-api`](../sk-api/SKILL.md) for the action patterns under test. [`sk-db`](../sk-db/SKILL.md) for the DB helpers mocked here._
