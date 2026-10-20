---
name: sk-e2e
description: Kit-shipped Playwright infrastructure for the TimeKast Starter Kit — the `e2e-runner.ts` wrapper that spins an isolated Neon branch per run, dynamic `auth.setup.ts` that writes storageState per role from `@/config/roles`, fully parametrized RBAC route specs over `ROUTE_ACL × ROLES`, and stability rules (semantic selectors, hydration waits, hex-random humanIds). Use when authoring E2E specs, debugging flakiness, or touching auth/RBAC E2E infra.
last-verified: 2026-04-23
---

# sk-e2e — Kit-shipped E2E Testing Infrastructure

> **Not stack-agnostic — this is kit-shipped infrastructure.** Travels with the Starter Kit. Grounded in actual files: `playwright.config.ts`, `scripts/tools/e2e-runner.ts`, `tests/e2e/auth.setup.ts`, `tests/fixtures/{auth,auth-files,rbac}.ts`, and `tests/e2e/rbac-routes.spec.ts`. Without the kit, this skill is inoperative — derived projects without the kit should use generic Playwright docs instead.
>
> **Pair:** for generic testing principles see [`kb-testing-patterns`](../kb-testing-patterns/SKILL.md). For Vitest / mocks see [`kb-testing-nextjs`](../kb-testing-nextjs/SKILL.md) + [`sk-testing-nextjs`](../sk-testing-nextjs/SKILL.md).

---

## 1. How E2E actually runs here

**Three moving parts** — all must be in sync:

1. **`scripts/tools/e2e-runner.ts`** (the wrapper, entry point of `pnpm test:e2e`)
   - Creates a temporary **Neon DB branch** for isolation.
   - Starts the Next.js dev server with that branch's `DATABASE_URL`.
   - Invokes Playwright.
   - Cleans up branch + server on exit.
2. **`playwright.config.ts`**
   - **No `webServer` block** — intentionally. The runner starts the server. If you add `webServer`, Playwright evaluates config BEFORE `globalSetup`, so the server starts with the wrong `DATABASE_URL`.
   - Two projects: `setup` (runs `auth.setup.ts` once) + `chromium` (depends on `setup`).
3. **`tests/e2e/auth.setup.ts`**
   - Iterates `Object.values(ROLES)` from `@/config/roles` and creates a test user per role.
   - Logs in via UI and saves the session as `tests/.auth/{role}.json` (gitignored).
   - Specs consume via `test.use({ storageState: AUTH_FILES[role] })`.

```
pnpm test:e2e
     │
     └─► scripts/tools/e2e-runner.ts
              │ 1. neon-branch create
              │ 2. spawn `next dev` with branch URL
              │ 3. wait for server
              │ 4. invoke `playwright test`
              │        └─► project "setup" → auth.setup.ts (per-role users + storageState)
              │        └─► project "chromium" → *.spec.ts (auth via storageState)
              │ 5. on exit: kill server, delete branch
```

**Commands:**

| Command                | Does                                                        |
| ---------------------- | ----------------------------------------------------------- |
| `pnpm test:e2e`        | Full flow — Neon branch + server + tests (CI + local)       |
| `pnpm test:e2e:direct` | Raw `playwright test` — requires `pnpm dev` already running |
| `pnpm test:e2e:ui`     | Playwright UI mode (also raw, no wrapper)                   |

> Use `test:e2e:direct` when debugging a single spec — faster feedback, no branch churn. The tradeoff: you share your dev DB with the tests.

---

## 2. Playwright config — the real one

```ts
// playwright.config.ts (actual values)
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1,
  workers: process.env.CI ? 1 : 2,
  reporter: 'html',
  timeout: 60_000,
  globalSetup: './tests/global-setup.ts',
  globalTeardown: './tests/global-teardown.ts',
  use: {
    baseURL: `http://localhost:${E2E_PORT}`, // E2E_PORT from pkg.ports.e2e ?? 3005
    trace: 'on-first-retry',
    actionTimeout: 15_000,
    navigationTimeout: 30_000,
  },
  projects: [
    { name: 'setup', testMatch: /auth\.setup/ },
    { name: 'chromium', use: { ...devices['Desktop Chrome'] }, dependencies: ['setup'] },
  ],
  // NO webServer block — the runner handles it
});
```

**Why these values:**

| Value                       | Reason                                               |
| --------------------------- | ---------------------------------------------------- |
| `timeout: 60_000`           | Cold-compile of first Turbopack route can exceed 30s |
| `actionTimeout: 15_000`     | Hydration-aware element interactions                 |
| `navigationTimeout: 30_000` | Slower SSR + Neon cold starts                        |
| `workers: CI ? 1 : 2`       | CI serializes to avoid Neon branch contention        |
| `retries: CI ? 2 : 1`       | Catch true flakes without masking real bugs          |
| `trace: 'on-first-retry'`   | Debug evidence only when needed (cheap on green)     |

**Port SSOT:** `E2E_PORT` is read from `package.json` via `pkg.ports?.e2e ?? 3005`. The runner, config, and app must agree — keep it in `package.json` only.

---

## 3. Dynamic auth setup — per role, zero maintenance

`tests/e2e/auth.setup.ts` loops over ALL roles from `@/config/roles`:

```ts
// tests/e2e/auth.setup.ts (actual)
import { test as setup } from '@playwright/test';
import { createTestUser } from '../fixtures/auth';
import { ROLES } from '@/config/roles';
import { AUTH_DIR, AUTH_FILES, AUTH_META_FILE } from '../fixtures/auth-files';
import fs from 'fs';

setup.describe('Auth Setup', () => {
  setup('create shared test users and save auth state', async ({ page }) => {
    fs.mkdirSync(AUTH_DIR, { recursive: true });
    const users: Record<string, { id: string; email: string; plainPassword: string }> = {};

    for (const role of Object.values(ROLES)) {
      const user = await createTestUser({
        role,
        email: `e2e-${role}-${Date.now()}@test.com`,
        name: `E2E ${role.charAt(0).toUpperCase() + role.slice(1)}`,
      });
      users[role] = { id: user.id, email: user.email, plainPassword: user.plainPassword };

      // Turbopack cold-compile on first /login visit — 30s timeout
      await page.goto('/login', { waitUntil: 'networkidle' });
      await page.waitForSelector('#email', { timeout: 30_000 });
      await page.fill('#email', user.email);
      await page.fill('#password', user.plainPassword);
      await page.click('button[type="submit"]');
      await page.waitForURL(/dashboard|settings/, {
        timeout: 30_000,
        waitUntil: 'domcontentloaded',
      });

      await page.context().storageState({ path: AUTH_FILES[role] });
      await page.context().clearCookies();
    }

    fs.writeFileSync(AUTH_META_FILE, JSON.stringify(users, null, 2));
  });
});
```

**`AUTH_FILES` is generated, not hand-maintained:**

```ts
// tests/fixtures/auth-files.ts (actual)
export const AUTH_FILES = Object.fromEntries(
  Object.values(ROLES).map((role) => [role, path.join(AUTH_DIR, `${role}.json`)])
) as Record<Role, string>;
```

> Add a role to `@/config/roles` → `auth.setup` creates a user + `storageState` for it → `AUTH_FILES[newRole]` works in specs. **Zero maintenance.**

---

## 4. `createTestUser` — the real factory

```ts
// tests/fixtures/auth.ts (actual signature)
export async function createTestUser(overrides: Partial<typeof users.$inferInsert> = {}) {
  const email = overrides.email || `test-${crypto.randomBytes(4).toString('hex')}@example.com`;
  const password = overrides.password || 'Test1234!';
  const hashedPassword = await hashPassword(password);
  const humanId =
    overrides.humanId || `USR-T${crypto.randomBytes(4).toString('hex').toUpperCase()}`;

  const [user] = await db
    .insert(users)
    .values({
      email,
      name: 'Test User',
      password: hashedPassword,
      role: 'user',
      emailVerified: new Date(),
      humanId,
      ...overrides,
    })
    .returning();

  return { ...user, plainPassword: password }; // plainPassword for UI login
}

export async function cleanupTestUser(userId: string) {
  /* deletes tokens + user */
}
```

**Use in specs:**

```ts
test('admin creates then deletes a user', async ({ page }) => {
  const target = await createTestUser({ role: 'user', name: 'Target' });
  try {
    await page.goto('/settings/users');
    // ...
  } finally {
    await cleanupTestUser(target.id);
  }
});
```

---

## 5. RBAC route tests — parametrized from SSOT

`tests/e2e/rbac-routes.spec.ts` is **fully driven by `ROUTE_ACL` + `ROLES`**. Adding a route to the ACL or a role to the config auto-expands coverage.

```ts
// tests/e2e/rbac-routes.spec.ts (actual shape)
import { AUTH_FILES } from '../fixtures/auth-files';
import {
  TESTABLE_ROLES, // all roles except super_admin
  PROTECTED_ROUTES, // Object.entries(ROUTE_ACL)
  getBlockedRoutes, // filter !isRouteAllowed(path, role)
  getAllowedRoutes, // filter isRouteAllowed(path, role)
  hasProtectedRoutes, // true if ROUTE_ACL has entries
} from '../fixtures/rbac';

// Skip cleanly if SK default (empty ROUTE_ACL)
test.skip(!hasProtectedRoutes(), 'No protected routes in ROUTE_ACL — RBAC tests skipped');

test.describe('RBAC Route Access', () => {
  for (const role of TESTABLE_ROLES) {
    const blocked = getBlockedRoutes(role);
    if (blocked.length === 0) continue;

    test.describe(`${role}: blocked routes`, () => {
      test.use({ storageState: AUTH_FILES[role] });
      for (const route of blocked) {
        test(`should redirect ${role} away from ${route.label}`, async ({ page }) => {
          await page.goto(route.path);
          await page.waitForURL(/dashboard/, { timeout: 10_000 }); // redirect, not 403
          expect(page.url()).not.toContain(route.path);
        });
      }
    });
  }

  // ... allowed routes loop + super_admin smoke test
});
```

**Design contract:**

| Decision                              | Why                                           |
| ------------------------------------- | --------------------------------------------- |
| `TESTABLE_ROLES` excludes super_admin | Always bypasses ACL; tested as separate smoke |
| Middleware redirects to `/dashboard`  | UX: better than 403                           |
| `test.skip` when ACL empty            | SK ships with empty ACL — no flakes           |
| `ROUTE_ACL` is SSOT                   | Add a route → tests expand automatically      |

---

## 6. Stability rules — 9 hard rules (grounded)

> Violating any → flaky suite.

### R1: Semantic selectors only

```
❌ page.locator('.btn-primary')
❌ page.locator('div > div > button')
✅ page.getByRole('button', { name: 'Submit' })
✅ page.getByLabel('Email')
```

### R2: Hex-random humanIds for test data

The real factory uses `USR-T${crypto.randomBytes(4).toString('hex').toUpperCase()}` — avoids collisions with seeds and parallel workers. **Don't use sequential integers.**

```
❌ humanId: 'USR-0001'
❌ id: 9_000_001
✅ humanId: `USR-T${crypto.randomBytes(4).toString('hex').toUpperCase()}`
```

### R3: Independent tests

Each test creates + cleans up its own data. No shared state between specs (except storageState, which is read-only auth).

```ts
let target: Awaited<ReturnType<typeof createTestUser>>;
test.beforeEach(async () => {
  target = await createTestUser();
});
test.afterEach(async () => {
  await cleanupTestUser(target.id);
});
```

### R4: storageState for auth (never UI login inside specs)

```
❌ Inside a *.spec.ts: await page.goto('/login'); await page.fill(...)
✅ test.use({ storageState: AUTH_FILES[role] });
```

UI login lives exclusively in `auth.setup.ts`. Specs consume sessions, never create them.

**Role switching mid-test** — use a fresh context:

```ts
const userCtx = await browser.newContext({ storageState: AUTH_FILES.user });
const userPage = await userCtx.newPage();
try {
  /* test from user POV */
} finally {
  await userCtx.close();
}
```

### R5: Deterministic factory, not production data

```
❌ const users = await db.select().from(users); // whatever is there
✅ const user = await createTestUser({ role: 'admin', name: 'Test Admin' });
```

### R6: No conditional flake-skips

```
❌ test.skip(process.env.CI, 'flaky on CI');
✅ test.skip(!hasProtectedRoutes(), 'No ROUTE_ACL configured');  // structural
```

Structural skips are fine (feature not configured → nothing to test). Runtime flake-skips hide bugs.

### R7: Dialog handlers before the trigger

```ts
// Native browser dialog
page.on('dialog', (dialog) => dialog.accept());
await page.click('#delete-btn');

// Radix AlertDialog (the common case in this repo — via ConfirmDialog)
await page.click('#delete-btn');
await page.locator('[role="alertdialog"]').waitFor();
await page.getByRole('button', { name: 'Eliminar' }).click();
```

### R8: Hydration-aware waits

Next.js App Router SSR renders HTML before React hydrates. Clicking a button before hydration → silent no-op.

```
❌ await page.goto('/users');
❌ await page.click('#create-btn');  // may fire before hydration

✅ await page.goto('/login', { waitUntil: 'networkidle' });  // cold-compile safe
✅ await page.waitForSelector('#email', { timeout: 30_000 });
✅ await page.fill('#email', ...);

// For post-login navigation:
✅ await page.waitForURL(/dashboard/, { waitUntil: 'domcontentloaded', timeout: 30_000 });
```

| When                     | Use                                |
| ------------------------ | ---------------------------------- |
| First nav (cold compile) | `waitUntil: 'networkidle'` + 30s   |
| Post-auth redirect       | `waitUntil: 'domcontentloaded'`    |
| Interaction-ready check  | `waitForSelector(id, { timeout })` |
| Never                    | `page.waitForTimeout(n)` for logic |

### R9: Serial mode for CRUD flows

```ts
test.describe.configure({ mode: 'serial' }); // CRUD on the same entity
test.describe.configure({ mode: 'parallel' }); // read-only, independent
```

`fullyParallel: true` is the default; opt into `serial` per describe when tests modify shared entity state.

---

## 7. Test organization (real tree)

```
tests/
├── e2e/
│   ├── auth.setup.ts          # Project "setup" — iterates ROLES
│   ├── rbac-routes.spec.ts    # Parametrized from ROUTE_ACL × ROLES
│   ├── user-admin.spec.ts     # Feature specs
│   ├── invite.spec.ts
│   └── password-reset.spec.ts
├── fixtures/
│   ├── auth.ts                # createTestUser, cleanupTestUser, createPasswordResetToken
│   ├── auth-files.ts          # AUTH_FILES map (generated from ROLES)
│   └── rbac.ts                # PROTECTED_ROUTES, getBlockedRoutes, getAllowedRoutes
├── .auth/                     # storageState JSONs + users.json (GITIGNORED)
├── global-setup.ts            # Playwright global — minimal (runner does most)
└── global-teardown.ts         # Cleanup hook
```

> `tests/.auth/` must be gitignored. The runner + setup regenerate it every run.

---

## 8. Anti-patterns (battle-tested)

| ❌ Don't                                  | ✅ Do                                           | Impact                           |
| ----------------------------------------- | ----------------------------------------------- | -------------------------------- |
| Test CSS classes or DOM structure         | `getByRole` / `getByLabel`                      | Survives refactors               |
| `page.waitForTimeout(3000)` to "be safe"  | `waitForSelector` / `waitForURL`                | Eliminates ~80% of flakes        |
| Log in via UI in a spec                   | `test.use({ storageState: AUTH_FILES[role] })`  | 3-5s saved per test              |
| Skip cleanup                              | `afterEach` + `cleanupTestUser`                 | Tests stay independent           |
| Ignore a flake ("it's fine")              | Fix root cause — hydration, selector, or data   | Flakiness compounds              |
| Sequential `USR-0001` humanIds            | `USR-T${hex}` random                            | Avoids seed / parallel collision |
| Add `webServer` to `playwright.config.ts` | Let `e2e-runner.ts` start the server            | Config evaluated before setup    |
| Run CRUD in parallel                      | `test.describe.configure({ mode: 'serial' })`   | Less resource contention         |
| Hardcode port                             | Read from `pkg.ports.e2e` (config, runner, app) | Single SSOT                      |

---

## 9. Debugging workflow

When an E2E fails:

1. **Check the HTML report** — `pnpm exec playwright show-report` opens the last run with traces for retries.
2. **Isolate the spec** — `pnpm test:e2e:direct tests/e2e/foo.spec.ts` (after `pnpm dev` is up).
3. **Run in UI mode** — `pnpm test:e2e:ui` — step through actions, inspect DOM at each step.
4. **Check storageState freshness** — if auth.setup failed mid-way, `tests/.auth/` may be partial. Delete and rerun.
5. **Neon branch stuck?** — `scripts/tools/neon-branch.ts` has a `cleanupZombieBranches()` helper called at startup. If branches accumulate in Neon UI, run the runner once to clean them.
6. **"Element not visible" on a button that's clearly there** — hydration timing. Add `waitForSelector` before interaction; use `networkidle` on first navigation of a route.

---

_Cross-reference: `kb-testing-nextjs` for Vitest unit + component tests. `kb-testing-patterns` for generic pyramid / AAA / RTL principles. `kb-security` for the real `ROUTE_ACL` shape that drives RBAC specs._
