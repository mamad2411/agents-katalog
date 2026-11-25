---
name: Flaky Test Detector
slug: flaky-test-detector
description: "Detect, analyze, and fix flaky tests across any test runner. Use when tests intermittently fail in CI, tests pass locally but fail on CI, tests fail non-deterministically, or need to stabilize a flaky test suite. Also for 'flaky test', 'flaky', 'intermittent failure', 'unstable test', 'test flakiness', 'test retry', 'CI flaky', 'non-deterministic test'."
license: MIT
compatibility: opencode, claude-code, cursor, windsurf, copilot
metadata:
  category: testing
  audience: developers
---

# Flaky Test Detector

Identify, diagnose, and eliminate flaky tests. Runs your test suite multiple times, isolates non-deterministic failures, categorizes root causes, and applies targeted fixes.

## Pipeline

1. **Detect** runner & configuration
2. **Harvest** flaky candidates via repeated runs
3. **Analyze** failure patterns to identify root cause
4. **Fix** each flakiness category with proven strategies
5. **Verify** fixes by re-running the detection loop

---

## Phase 1: Detect runner and configuration

Read project setup:

```bash
cat package.json
```

Identify the test runner:

| Indicator | Runner | Base command |
|---|---|---|
| `"vitest"` in devDependencies | **Vitest** | `npx vitest` |
| `"jest"` in devDependencies | **Jest** | `npx jest` |
| `"react-scripts"` in devDependencies | **react-scripts** | `npx react-scripts test` |
| `"@playwright/test"` in devDependencies | **Playwright** | `npx playwright test` |
| `"cypress"` in devDependencies | **Cypress** | `npx cypress run` |
| `"mocha"` in devDependencies | **Mocha** | `npx mocha` |
| `"ava"` in devDependencies | **AVA** | `npx ava` |

Check existing retry/flaky config:

- **Vitest**: `retry` in `vitest.config.ts`
- **Jest**: `testRetry` in `jest.config.ts` or `jest.retryTimes()` in setup
- **Playwright**: `retries` in `playwright.config.ts`
- **Cypress**: `retries` in `cypress.config.ts`
- **Mocha**: `--retries` CLI flag or `retries` in `.mocharc.json`
- **AVA**: no built-in retry — check for a custom retry helper around `t.try()`
- **react-scripts (CRA)**: inherits Jest under the `jest` key in `package.json`; retry needs `jest-retry` wired through `setupFilesAfterEnv`

---

## Phase 2: Harvest flaky candidates

Run the full suite multiple times and collect failures:

```bash
# Run 3+ times, log each result
for i in 1 2 3; do
  echo "=== RUN $i ==="
  npx vitest --reporter=json 2>/dev/null | tee ".flaky-run-$i.json"
done
```

For a quick flaky check on the last failed run:

```bash
npx vitest --reporter=json 2>/dev/null | tee ".flaky-last-run.json"
```

For Jest:
```bash
for i in 1 2 3; do
  echo "=== RUN $i ==="
  npx jest --json 2>/dev/null | tee ".flaky-run-$i.json"
done
```

For Playwright:
```bash
for i in 1 2 3; do
  echo "=== RUN $i ==="
  npx playwright test --reporter=json 2>/dev/null | tee ".flaky-run-$i.json"
done
```

For Cypress:
```bash
for i in 1 2 3; do
  echo "=== RUN $i ==="
  npx cypress run --reporter json 2>/dev/null | tee ".flaky-run-$i.json"
done
```

For Mocha:
```bash
for i in 1 2 3; do
  echo "=== RUN $i ==="
  npx mocha --reporter json 2>/dev/null | tee ".flaky-run-$i.json"
done
```

For AVA:
```bash
for i in 1 2 3; do
  echo "=== RUN $i ==="
  npx ava --tap 2>/dev/null | tee ".flaky-run-$i.tap"
done
```

For react-scripts (CRA):
```bash
for i in 1 2 3; do
  echo "=== RUN $i ==="
  CI=true npx react-scripts test --json 2>/dev/null | tee ".flaky-run-$i.json"
done
```

Collect test results across runs and identify:
- **Always passes** — stable, exclude from analysis
- **Always fails** — broken test, report separately
- **Sometimes passes, sometimes fails** — FLAKY candidate

---

## Phase 3: Analyze root cause

For each flaky candidate, categorize by symptom:

### Category A: Async timing

**Symptoms:**
- Test passes locally but fails on CI (slower environments)
- Failure mentions timeout, `setTimeout`, `setInterval`, `requestAnimationFrame`
- DOM assertions fail intermittently in browser tests

**Diagnosis:**
```bash
# Grep the test file for async patterns
grep -n "setTimeout\|setInterval\|waitFor\|delay\|sleep\|requestAnimationFrame\|transition\|animation" <test-file>
```

Look for:
- Fixed timeouts instead of polling/retrying
- Missing `waitFor` or `expect.poll` in Vitest
- Missing `waitFor` / `findBy*` in Testing Library
- Assertions before async operations complete

### Category B: Shared mutable state

**Symptoms:**
- Failures depend on test order (run `--shard` or `--bail 1` changes results)
- Tests pass in isolation but fail in full suite
- Module-level variables, singletons, globals

**Diagnosis:**
```bash
# Check for shared state patterns
grep -n "let [a-z]* = \|var [a-z]* = \|const [a-z]* = \|global\." <test-file> | head -20
```

Look for:
- Test-level variables not reset between tests
- Mock state leaking across tests (`vi.fn()` / `jest.fn()` not cleared)
- Environment variable mutations without restore
- Filesystem or database state not cleaned up

### Category C: Test isolation

**Symptoms:**
- Test passes with `--testPathPattern=<single-file>` but fails in full suite
- Test fails when specific other tests run before it

**Diagnosis:**
Run tests in random order to confirm:
```bash
# Vitest (sequential + random)
npx vitest --sequence=sequential --reporter=json 2>/dev/null
npx vitest --sequence=random --reporter=json 2>/dev/null
```

Look for:
- Missing `beforeEach` / `afterEach` cleanup
- Tests modifying DOM or globals without restoring
- Database/seeded data not isolated per test
- Mock implementations leaking (`vi.restoreAllMocks()` / `jest.restoreAllMocks()` missing)

### Category D: Environment sensitivity

**Symptoms:**
- Fails on CI only (never locally)
- Fails on certain OS/browser combinations
- Fails at specific times (timezone, date-dependent)

**Diagnosis:**
Look for:
- Hardcoded time/date values
- Locale-specific formatting
- Timezone-dependent assertions
- Screen resolution, viewport size assumptions
- Node.js/Python version-specific behavior
- Network-dependent tests (API calls, rate limiting)

### Category E: Race conditions

**Symptoms:**
- Failures involve concurrent operations, Web Workers, or parallel requests
- `Promise.all`, `Promise.race`, `setTimeout` with 0ms delay
- Event listeners on shared emitters

**Diagnosis:**
```bash
grep -n "Promise\.all\|Promise\.race\|Promise\.any\|Promise\.allSettled\|setTimeout\|setImmediate\|process\.nextTick" <test-file>
```

---

## Phase 4: Apply fixes

Apply fix based on the detected category:

### Fix A: Async timing

Replace brittle timing patterns:

```diff
- await new Promise(r => setTimeout(r, 1000))
- expect(screen.getByText('Loaded')).toBeInTheDocument()
+ await waitFor(() => {
+   expect(screen.getByText('Loaded')).toBeInTheDocument()
+ }, { timeout: 5000, interval: 100 })
```

For Vitest, use `expect.poll` or `waitFor`:
```ts
import { waitFor } from '@testing-library/react'
// or Vitest built-in:
await expect.poll(() => getStatus(), { timeout: 5000, interval: 100 }).toBe('done')
```

For Playwright, use auto-waiting locators:
```ts
// Bad:
await page.waitForTimeout(2000)
expect(await page.textContent('.status')).toBe('done')

// Good:
await expect(page.locator('.status')).toHaveText('done', { timeout: 10000 })
```

### Fix B: Shared mutable state

```diff
+ import { vi } from 'vitest'
+
+ beforeEach(() => {
+   vi.clearAllMocks()
+ })
+
+ afterEach(() => {
+   vi.restoreAllMocks()
+ })
```

Reset module-level state:
```ts
beforeEach(() => {
  // Reset counters, caches, singletons
  counter = 0
  cache.clear()
})
```

Isolate runtime configuration mutations:
```ts
const ORIGINAL_RUNTIME_MODE = getRuntimeMode()
afterEach(() => {
  setRuntimeMode(ORIGINAL_RUNTIME_MODE)
})
```

### Fix C: Test isolation

```diff
+ beforeEach(() => {
+   document.body.innerHTML = ''
+   localStorage.clear()
+ })
+
+ afterEach(() => {
+   vi.restoreAllMocks()
+   vi.useRealTimers()
+ })
```

For database-backed tests:
```ts
beforeEach(async () => {
  await db.migrate.latest()
  await db.seed.run()
})

afterEach(async () => {
  await db.migrate.rollback()
})
```

### Fix D: Environment sensitivity

Mock time-dependent code:
```ts
beforeEach(() => {
  vi.useFakeTimers()
  vi.setSystemTime(new Date('2024-01-15T12:00:00Z'))
})

afterEach(() => {
  vi.useRealTimers()
})
```

For locale-sensitive tests:
```ts
import { locale } from '../i18n'

beforeEach(() => {
  locale.set('en-US')
})
```

For network-dependent tests, mock all external calls:
```ts
vi.mock('../api/client')
// or
global.fetch = vi.fn()
```

### Fix E: Race conditions

Ensure sequential processing in tests:
```ts
// Instead of Promise.all, test sequentially
await operation1()
await operation2()
```

For event emitter tests:
```ts
const events: string[] = []
emitter.on('data', (d) => events.push(d))

emitter.emit('data', 'a')
emitter.emit('data', 'b')
await vi.waitFor(() => {
  expect(events).toEqual(['a', 'b'])
})
```

---

## Phase 5: Add retry configuration

After fixing the root cause, add retry as a safety net. Prefer CI-specific
config files or CI job commands with literal retry values instead of reading
runtime environment variables inside the test config.

**Vitest** — `vitest.ci.config.ts`:
```ts
import baseConfig from './vitest.config'

export default defineConfig({
  ...baseConfig,
  test: {
    ...baseConfig.test,
    retry: 2,
    // Sequential execution for flaky tests:
    sequence: {
      seed: 123,
      shuffle: false,
    },
  },
})
```

Run in CI with `vitest --config vitest.ci.config.ts`.

Or per-test/file with `vi.retry()`:
```ts
vi.retry(2)
describe('flaky file', () => { ... })
```

**Jest** — `jest.ci.config.ts` (requires `jest-retry`):
```ts
const baseConfig = require('./jest.config')

export default {
  ...baseConfig,
  setupFilesAfterEnv: ['jest-retry'],
  retryTimes: 2,
}
```

Run in CI with `jest --config jest.ci.config.ts`.

**Playwright** — `playwright.ci.config.ts`:
```ts
import baseConfig from './playwright.config'

export default defineConfig({
  ...baseConfig,
  retries: 2,
})
```

Run in CI with `playwright test --config playwright.ci.config.ts`.

---

## Phase 6: Verify

Re-run the flaky detection loop:

```bash
for i in 1 2 3; do
  echo "=== RUN $i ==="
  npx vitest --reporter=json 2>/dev/null | tee ".flaky-verify-$i.json"
done
```

Compare results across runs:
- **Zero flaky tests** — success, report fixed count
- **Remaining flaky tests** — iterate back to Phase 3 with deeper analysis

---

## FLAKY_REPORT.md generation

After fixing, generate a summary report:

```markdown
# Flaky Test Report

| Test | Runner | Category | Status | Fix applied |
|------|--------|----------|--------|-------------|
| `auth.test.ts` | Vitest | Async timing | Fixed | Replaced `setTimeout` with `waitFor` |
| `api.test.ts` | Jest | Shared state | Fixed | Added `beforeEach` cleanup |
| `login.spec.ts` | Playwright | Environment | Quarantined | Needs API mock setup |

**Stable rate:** 98/100 tests (98%)
**Next step:** Review remaining flaky tests manually
```

---

## Example

User: "our CI is full of flaky tests, we use vitest"

Agent actions:
1. Run `npx vitest --reporter=json` 3 times with loop
2. Detect 4 tests pass/fail inconsistently across runs
3. For `auth.test.ts`: grep shows `setTimeout(500)` before assertion
4. Replace with `waitFor` — `auth.test.ts` now consistent across 3 runs
5. For `api.test.ts`: module-level auth token leaks between tests
6. Add `beforeEach(() => localStorage.clear())` — stable
7. Configure `vitest.config.ts` with CI retry = 2
8. Verify: all 4 formerly flaky tests pass consistently
9. Show report

User: "playwright e2e tests flaky on CI"

Agent actions:
1. Run `npx playwright test --reporter=json` 3 times, identify `login.spec.ts` flaky
2. Analyze: uses `page.waitForTimeout(3000)` — async timing issue
3. Replace with `await expect(page.locator('.dashboard')).toBeVisible({ timeout: 15000 })`
4. Set `retries: 2` in `playwright.config.ts` for CI
5. Also detect `user-profile.spec.ts` — environment sensitivity (timezone)
6. Mock timezone in test setup
7. Verify: 3/3 runs pass for both tests
