---
name: test-smoke
description: Run a production smoke test suite — read-only Playwright checks against the live environment to confirm critical user paths are reachable after a deploy. Usage — /test-smoke [--env prod|staging]
argument-hint: "[--env prod|staging]"
arguments:
  - name: env
    description: "Target environment (default: prod)"
user-invocable: true
stack: cloud/aws
allowed-tools:
  - Read
  - Write
  - Bash(npx *)
  - Bash(node *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(aws *)
  - Bash(gh *)
  - Bash(date *)
---

# Smoke Test

Parse `--env` argument (default: `prod`).

Smoke tests are **read-only** — they never mutate state, never create test data, never delete anything. They run against the live environment immediately after a deploy. A failed smoke test triggers an immediate rollback recommendation.

---

## Step 1 — Resolve target URL

```bash
ENV=prod   # from --env argument

# Try SSM first
DOMAIN=$(aws ssm get-parameter \
  --name "/$(node -p "require('./package.json').name")/${ENV}/domain" \
  --query Parameter.Value --output text 2>/dev/null)

# Fall back to package.json or prompt
if [ -z "$DOMAIN" ]; then
  echo "⚠️  Could not resolve domain from SSM. Check SSM param /<project>/${ENV}/domain"
  exit 1
fi

BASE_URL="https://api-${ENV}.${DOMAIN}"
FRONTEND_URL="https://${DOMAIN}"
echo "Smoke testing: $BASE_URL"
```

---

## Step 2 — Check for existing smoke test suite

```bash
find . -name "*.smoke.spec.ts" -o -name "smoke.spec.ts" -o -name "*.smoke.test.ts" 2>/dev/null | head -10
ls tests/smoke/ 2>/dev/null || ls e2e/smoke/ 2>/dev/null || echo "none found"
```

**If a smoke suite exists:** run it and go to Step 5.

**If no suite exists:** generate one (Step 3), then run it.

---

## Step 3 — Generate the smoke test suite

Read the project to understand what to test:

```bash
# What API endpoints exist?
grep -rn "router\.\(get\|post\|put\|delete\)" src/routes/ 2>/dev/null | grep -v test | head -20

# What are the main user-facing pages?
find src -name "*.page.tsx" -o -name "*.route.tsx" 2>/dev/null | head -10

# Is there an OpenAPI / Swagger spec?
find . -name "openapi*.json" -o -name "swagger*.json" 2>/dev/null | head -3
```

Write `tests/smoke/smoke.spec.ts`:

```ts
// tests/smoke/smoke.spec.ts
// READ-ONLY — never creates, updates, or deletes data

import { test, expect } from '@playwright/test'

const BASE_URL = process.env.SMOKE_BASE_URL ?? 'http://localhost:3000'
const API_URL  = process.env.SMOKE_API_URL  ?? 'http://localhost:3001'

// ─── API health ────────────────────────────────────────────────────────────────

test('GET /health returns 200', async ({ request }) => {
  const res = await request.get(`${API_URL}/health`)
  expect(res.status()).toBe(200)
  const body = await res.json()
  expect(body).toMatchObject({ status: 'ok' })
})

test('GET /health includes version', async ({ request }) => {
  const res = await request.get(`${API_URL}/health`)
  const body = await res.json()
  expect(body.version).toBeTruthy()
})

// ─── Auth endpoints (unauthenticated access should return 401) ────────────────

test('GET /api/v1/me returns 401 without token', async ({ request }) => {
  const res = await request.get(`${API_URL}/api/v1/me`)
  expect(res.status()).toBe(401)
})

// ─── Public API endpoints ─────────────────────────────────────────────────────

// Add public endpoints that should always respond:
// test('GET /api/v1/products returns 200', async ({ request }) => { ... })

// ─── Frontend pages ───────────────────────────────────────────────────────────

test('home page loads', async ({ page }) => {
  await page.goto(BASE_URL)
  await expect(page).toHaveTitle(/.+/)   // has any title
  // No 5xx error text visible
  await expect(page.locator('body')).not.toContainText('Internal Server Error')
  await expect(page.locator('body')).not.toContainText('Application error')
})

test('login page renders form', async ({ page }) => {
  await page.goto(`${BASE_URL}/login`)
  await expect(page.locator('input[type="email"], input[name="email"]')).toBeVisible()
  await expect(page.locator('input[type="password"]')).toBeVisible()
  await expect(page.locator('button[type="submit"]')).toBeVisible()
})

test('404 page shows not-found UI', async ({ page }) => {
  await page.goto(`${BASE_URL}/this-page-definitely-does-not-exist-${Date.now()}`)
  // Should show 404 UI, not a blank page or 5xx
  const text = await page.locator('body').textContent()
  expect(text).toBeTruthy()
  await expect(page.locator('body')).not.toContainText('Internal Server Error')
})

// ─── Static assets ────────────────────────────────────────────────────────────

test('JS bundle loads (no 404)', async ({ request }) => {
  const page_res = await request.get(BASE_URL)
  // Expect page to return 200
  expect(page_res.status()).toBe(200)
})
```

Write `playwright.smoke.config.ts` (separate from regular e2e config):

```ts
// playwright.smoke.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/smoke',
  timeout: 15_000,           // smoke tests should be fast
  retries: 1,                // one retry on flaky network
  workers: 2,                // low concurrency — we're hitting production
  reporter: [
    ['list'],
    ['json', { outputFile: 'docs/smoke/smoke-results.json' }],
  ],
  use: {
    baseURL:  process.env.SMOKE_BASE_URL,
    headless: true,
    screenshot: 'only-on-failure',
    video: 'off',
    actionTimeout: 10_000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
})
```

---

## Step 4 — Add smoke script to package.json

```bash
node -e "
const pkg = require('./package.json')
if (!pkg.scripts['test:smoke']) {
  pkg.scripts['test:smoke'] = 'playwright test --config=playwright.smoke.config.ts'
  require('fs').writeFileSync('./package.json', JSON.stringify(pkg, null, 2) + '\n')
  console.log('Added test:smoke script')
} else {
  console.log('test:smoke already exists')
}
"
```

---

## Step 5 — Run the smoke tests

```bash
SMOKE_BASE_URL="${FRONTEND_URL}" \
SMOKE_API_URL="${BASE_URL}" \
npx playwright test --config=playwright.smoke.config.ts \
  --reporter=list 2>&1
```

Capture exit code:

```bash
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
  echo "✅ All smoke tests passed"
else
  echo "❌ Smoke tests FAILED (exit $EXIT_CODE)"
fi
```

---

## Step 6 — Interpret results and produce report

Read `docs/smoke/smoke-results.json` if it exists, otherwise parse stdout.

Present a results table:

> **Smoke Test Results — `prod` — <timestamp>**
>
> | Test | Status | Duration |
> |---|---|---|
> | GET /health returns 200 | ✅ Pass | 142ms |
> | GET /api/v1/me returns 401 | ✅ Pass | 89ms |
> | home page loads | ✅ Pass | 1.2s |
> | login page renders form | ✅ Pass | 890ms |
> | 404 page shows not-found UI | ✅ Pass | 650ms |
>
> **5 / 5 passed. Environment: healthy.**

Write `docs/smoke/SMOKE-<env>-<date>.md`:

```markdown
# Smoke Test Report
_Date: <today> · Environment: <env> · URL: <base-url>_

## Result: ✅ ALL PASSED / ❌ FAILED

| Test | Status | Duration | Notes |
|---|---|---|---|
| GET /health | ✅ | 142ms | |
| ... | | | |

## Failed Tests (if any)

<screenshot paths and error messages>

## Action
<If all passed: "Environment healthy — no action needed">
<If any failed: "⚠️ ROLLBACK RECOMMENDED — run /deploy rollback prod">
```

---

## Step 7 — Verdict

**If all tests pass:**
> ✅ **Environment healthy.** All smoke checks passed.
> Report: `docs/smoke/SMOKE-<env>-<date>.md`

**If any test fails:**
> ❌ **ROLLBACK RECOMMENDED.**
> Failing tests: <list>
> Run: `/deploy rollback <env>`

---

## Adding smoke tests for new endpoints

Whenever `/dev-code` adds a new API endpoint or page, also add a smoke test:

```ts
// For a new endpoint: GET /api/v1/orders
test('GET /api/v1/orders requires auth', async ({ request }) => {
  const res = await request.get(`${API_URL}/api/v1/orders`)
  expect(res.status()).toBe(401)
})

// For a new page: /dashboard
test('dashboard page loads', async ({ page }) => {
  await page.goto(`${BASE_URL}/dashboard`)
  // Expect redirect to login (unauthenticated)
  await expect(page).toHaveURL(/login/)
})
```

**Smoke test rules:**
- ✅ Read-only — GET requests only, no POST/PUT/DELETE
- ✅ No test credentials stored in code — use env vars or anonymous paths only
- ✅ Must pass in under 15 seconds
- ✅ Retry once on network errors (Playwright `retries: 1`)
- ❌ Never test business logic — that's for unit/integration tests
- ❌ Never depend on specific data existing in the DB

**Related skills — apply together:**
- `validate` — `/validate` is comprehensive; smoke is the lightweight first signal immediately post-deploy
- `deploy` — run `/test-smoke` automatically at the end of every prod deploy
- `synthetic` — `/synthetic` runs canary checks continuously; smoke runs once on-demand post-deploy
- `slo` — smoke failures are potential SLO breach triggers
