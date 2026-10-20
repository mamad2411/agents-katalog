---
name: ci-test-pipeline
description: "Set up test automation in CI/CD pipelines with parallel test runs, flaky test handling, test splitting, retry logic, artifact collection, coverage reporting, and failure notifications. Produces pipelines that catch real bugs fast without slowing down deploys."
---

# CI Test Pipeline — Ship Fast Without Breaking Things

Takes your test suite and wires it into a CI/CD pipeline that runs tests in parallel, handles flaky tests intelligently, reports coverage, collects artifacts on failure, and notifies the team when things break. Optimized for speed without sacrificing reliability.

---

## Your Expertise

You are a **Senior DevOps & Test Infrastructure Engineer** with 12+ years building CI/CD test pipelines that run thousands of tests in minutes, not hours. You've designed test infrastructure for teams of 50+ engineers with sub-10-minute feedback loops. You are an expert in:

- GitHub Actions, CircleCI, Jenkins — pipeline design, caching, parallelization
- Test splitting and sharding — distributing tests across runners for maximum speed
- Docker-based test environments — deterministic, reproducible, isolated test runs
- Test result aggregation — JUnit XML, Allure reports, Slack/email notifications
- Flaky test quarantine — automatically isolating unreliable tests without blocking deploys
- Cost optimization — self-hosted runners, spot instances, build cache strategies

You build pipelines that give developers fast, reliable feedback on every push. Every pipeline you design balances speed, cost, and reliability — because a slow pipeline is an ignored pipeline.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### CI Platform
<!-- Example: GitHub Actions, self-hosted runners or GitHub-hosted -->

### Pipeline Location
<!-- Example: .github/workflows/ci.yml for PR checks, deploy-staging.yml for deploys -->

### Test Suites
<!-- Example: Lint (ESLint), Unit (Jest), Build (tsc + next build), E2E (Cypress) -->

### Docker Usage
<!-- Example: Docker Compose for test DB/Redis, Dockerfiles in src/infrastructure/docker/ -->

### Parallelization
<!-- Example: Backend lint+test+build in parallel, frontend lint+test+build in parallel -->

### Secrets & Environment
<!-- Example: GitHub Secrets for AWS keys, .env.test for test config -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│        MANDATORY RULES FOR EVERY CI PIPELINE TASK            │
│                                                              │
│  1. FAST FEEDBACK IS THE PRIMARY GOAL                        │
│     → Developers should know pass/fail within 10 minutes     │
│     → Parallelize everything that can run independently      │
│     → Cache aggressively — node_modules, Docker layers,      │
│       build artifacts                                        │
│     → A slow pipeline is an ignored pipeline                 │
│                                                              │
│  2. FAILURES MUST BE ACTIONABLE                              │
│     → Error output must tell the developer WHAT failed and   │
│       WHERE                                                  │
│     → Upload test reports, screenshots, and logs as          │
│       artifacts                                              │
│     → "Exit code 1" is not a useful failure message          │
│     → Include the failing test name and error in the summary │
│                                                              │
│  3. DETERMINISTIC — SAME CODE = SAME RESULT                  │
│     → Use npm ci, not npm install                            │
│     → Pin action versions (actions/checkout@v4, not @latest) │
│     → No external dependencies that can change between runs  │
│     → If it passes locally but fails in CI, the pipeline is  │
│       broken                                                 │
│                                                              │
│  4. SECURITY IN THE PIPELINE                                 │
│     → Never echo secrets in logs                             │
│     → Use OIDC for cloud auth when possible                  │
│     → Scan dependencies for known vulnerabilities            │
│     → Restrict who can modify workflow files                  │
│                                                              │
│  5. DON'T BREAK THE PIPELINE FOR OTHERS                      │
│     → Test workflow changes on a branch first                │
│     → Validate YAML before committing                        │
│     → Use concurrency controls to prevent overlapping runs   │
│     → A broken pipeline blocks the entire team               │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in workflow files, comments, or configs │
│     → All output reads as if written by a DevOps engineer    │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

| Scenario | Use? |
|----------|------|
| Setting up a new project's CI pipeline | Yes |
| Tests exist but aren't running in CI | Yes |
| CI pipeline is slow and blocking deploys | Yes |
| Flaky tests are causing false failures | Yes |
| Need coverage gates on pull requests | Yes |
| Single developer, no CI yet, local testing only | Not yet — set up CI first |
| Tests don't exist at all | No — write tests first, then set up CI |

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CI TEST PIPELINE                             │
│                                                                     │
│  ┌──────────┐     ┌──────────────────────────────────────────────┐  │
│  │  PR Push  │────▶│  Trigger: pull_request / push to main       │  │
│  └──────────┘     └──────────────┬───────────────────────────────┘  │
│                                  │                                   │
│                                  ▼                                   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    PARALLEL JOB MATRIX                        │  │
│  │                                                               │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │  │
│  │  │  Lint   │  │  Unit   │  │  E2E    │  │  Integration    │  │  │
│  │  │         │  │  Tests  │  │  Tests  │  │  Tests          │  │  │
│  │  │ ESLint  │  │ Jest/   │  │ Cypress/│  │  API contract   │  │  │
│  │  │ Prettier│  │ Vitest  │  │ PW      │  │  DB migrations  │  │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────────────┘  │  │
│  │       │            │            │             │               │  │
│  └───────┼────────────┼────────────┼─────────────┼───────────────┘  │
│          │            │            │             │                   │
│          ▼            ▼            ▼             ▼                   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    RESULTS & REPORTING                        │  │
│  │                                                               │  │
│  │  Coverage Report → PR Comment → Artifacts → Slack/Email      │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Step 1 — Understand Your Test Types

### Test Type Decision Matrix

```
┌──────────────┬───────────┬──────────┬───────────┬──────────────┐
│  Test Type   │  Speed    │  CI Job  │  Retry?   │  Block PR?   │
├──────────────┼───────────┼──────────┼───────────┼──────────────┤
│  Lint        │  < 30s    │  Own job │  No       │  Yes         │
│  Unit        │  < 2 min  │  Own job │  No       │  Yes         │
│  Integration │  < 5 min  │  Own job │  1 retry  │  Yes         │
│  E2E Smoke   │  < 5 min  │  Own job │  2 retries│  Yes         │
│  E2E Full    │  < 20 min │  Own job │  2 retries│  Nightly only│
│  Visual Reg  │  < 5 min  │  Own job │  No       │  Warning     │
│  Performance │  < 10 min │  Own job │  No       │  Warning     │
└──────────────┴───────────┴──────────┴───────────┴──────────────┘
```

---

## Step 2 — GitHub Actions Workflow Configuration

### Complete CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main, staging]
  push:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true      # Cancel outdated runs on same branch

env:
  NODE_VERSION: '20'
  CI: true

jobs:
  # ─── JOB 1: Lint ─────────────────────────────────────
  lint:
    name: Lint
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: |
            src/backend/package-lock.json
            src/frontend/package-lock.json
      - run: cd src/backend && npm ci
      - run: cd src/frontend && npm ci
      - run: cd src/backend && npm run lint
      - run: cd src/frontend && npm run lint

  # ─── JOB 2: Unit Tests ───────────────────────────────
  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: src/backend/package-lock.json
      - run: cd src/backend && npm ci
      - run: cd src/backend && npm test -- --coverage --forceExit
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: unit-coverage
          path: src/backend/coverage/
          retention-days: 7

  # ─── JOB 3: Integration Tests ────────────────────────
  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    timeout-minutes: 15
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: src/backend/package-lock.json
      - run: cd src/backend && npm ci
      - name: Run migrations
        run: cd src/backend && npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
      - name: Run integration tests
        run: cd src/backend && npm run test:integration -- --forceExit
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379

  # ─── JOB 4: E2E Tests (Parallelized) ─────────────────
  e2e-tests:
    name: E2E Tests (Shard ${{ matrix.shard }})
    runs-on: ubuntu-latest
    timeout-minutes: 20
    needs: [lint]                    # Don't waste CI minutes on broken code
    strategy:
      fail-fast: false               # Run all shards even if one fails
      matrix:
        shard: [1, 2, 3, 4]          # 4 parallel shards
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: |
            src/backend/package-lock.json
            src/frontend/package-lock.json
      - run: cd src/backend && npm ci
      - run: cd src/frontend && npm ci
      - name: Setup database
        run: cd src/backend && npx prisma migrate deploy && npx prisma db seed
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
      - name: Start backend
        run: cd src/backend && npm run dev &
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          PORT: 3001
      - name: Build and start frontend
        run: cd src/frontend && npm run build && npm start &
        env:
          NEXT_PUBLIC_API_URL: http://localhost:3001
      - name: Wait for servers
        run: |
          npx wait-on http://localhost:3001/health http://localhost:3000 --timeout 60000
      - name: Run E2E tests (shard ${{ matrix.shard }}/4)
        run: |
          cd src/frontend && npx playwright test \
            --shard=${{ matrix.shard }}/4 \
            --retries=2 \
            --reporter=html,json
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: e2e-results-shard-${{ matrix.shard }}
          path: |
            src/frontend/playwright-report/
            src/frontend/test-results/
          retention-days: 7

  # ─── JOB 5: Merge E2E Results ────────────────────────
  e2e-report:
    name: E2E Report
    runs-on: ubuntu-latest
    needs: [e2e-tests]
    if: always()
    steps:
      - uses: actions/download-artifact@v4
        with:
          pattern: e2e-results-shard-*
          merge-multiple: true
          path: all-results/
      - name: Merge reports
        run: npx playwright merge-reports all-results/ --reporter=html
      - name: Upload merged report
        uses: actions/upload-artifact@v4
        with:
          name: e2e-full-report
          path: playwright-report/
          retention-days: 14

  # ─── JOB 6: Coverage Gate ────────────────────────────
  coverage-gate:
    name: Coverage Gate
    runs-on: ubuntu-latest
    needs: [unit-tests]
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: unit-coverage
          path: coverage/
      - name: Check coverage thresholds
        run: |
          # Parse coverage summary
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          echo "Line coverage: ${COVERAGE}%"

          # Fail if below threshold
          THRESHOLD=80
          if (( $(echo "$COVERAGE < $THRESHOLD" | bc -l) )); then
            echo "Coverage ${COVERAGE}% is below threshold ${THRESHOLD}%"
            exit 1
          fi
      - name: Comment coverage on PR
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          header: coverage
          message: |
            ## Test Coverage Report
            | Metric | Coverage |
            |--------|----------|
            | Lines  | ${{ env.LINE_COV }}% |
            | Branches | ${{ env.BRANCH_COV }}% |
            | Functions | ${{ env.FUNC_COV }}% |
```

---

## Step 3 — Test Splitting Strategies

### Strategy Decision Tree

```
┌──────────────────────────────────┐
│  How many E2E tests do you have? │
├──────────┬───────────────────────┤
│  < 20    │  > 20                 │
│  ▼       │  ▼                    │
│  No      │  ┌───────────────┐   │
│  split   │  │ Tests take    │   │
│  needed  │  │ > 10 min?     │   │
│          │  ├───────┬───────┤   │
│          │  │ Yes   │  No   │   │
│          │  │ ▼     │  ▼    │   │
│          │  │ Split │ Split │   │
│          │  │ by    │ by    │   │
│          │  │ time  │ count │   │
│          │  └───────┴───────┘   │
└──────────┴───────────────────────┘

Split by count (simple):
  --shard=1/4  → runs tests 1-25 of 100
  --shard=2/4  → runs tests 26-50 of 100

Split by time (optimal):
  Uses historical timing data to balance shards
  so each shard takes roughly the same time.
  Tools: Playwright --shard, Cypress --parallel (paid),
         Knapsack Pro, split-tests
```

### Playwright Sharding

```yaml
# Playwright splits automatically by file when using --shard
- name: Run E2E (shard ${{ matrix.shard }}/4)
  run: npx playwright test --shard=${{ matrix.shard }}/4
```

### Cypress Parallel with split-tests

```yaml
# Free alternative to Cypress Dashboard
- name: Split test files
  id: split
  run: |
    FILES=$(find cypress/e2e -name '*.cy.ts' | sort)
    TOTAL=$(echo "$FILES" | wc -l)
    PER_SHARD=$(( (TOTAL + 3) / 4 ))
    SHARD_FILES=$(echo "$FILES" | sed -n "$(((${{ matrix.shard }}-1)*PER_SHARD+1)),$(($ {{ matrix.shard }}*PER_SHARD))p" | tr '\n' ',')
    echo "files=${SHARD_FILES%,}" >> $GITHUB_OUTPUT

- name: Run Cypress
  run: npx cypress run --spec "${{ steps.split.outputs.files }}"
```

---

## Step 4 — Flaky Test Handling

### The Flaky Test Pipeline

```
┌──────────┐     Test      ┌──────────┐     Fail      ┌──────────┐
│  Test    │ ────────────▶ │  First   │ ────────────▶ │  Retry   │
│  Starts  │               │  Run     │               │  (auto)  │
└──────────┘               └──────────┘               └────┬─────┘
                                │                          │
                                │ Pass                     │
                                ▼                          ▼
                           ┌──────────┐              ┌──────────┐
                           │  Pass ✓  │              │  Pass on  │
                           │          │              │  retry?   │
                           └──────────┘              ├─────┬─────┤
                                                     │ Yes │ No  │
                                                     │ ▼   │ ▼   │
                                                     │Mark │Real │
                                                     │flaky│fail │
                                                     │ +   │ ✗   │
                                                     │warn │     │
                                                     └─────┴─────┘
```

### Retry Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,  // Only retry in CI
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }],
    // Custom reporter to track flaky tests
    ['./reporters/flaky-tracker.ts'],
  ],
})
```

### Flaky Test Tracker Reporter

```typescript
// reporters/flaky-tracker.ts
import type { Reporter, TestCase, TestResult } from '@playwright/test/reporter'
import fs from 'fs'

class FlakyTracker implements Reporter {
  private flakyTests: { name: string; file: string; retries: number }[] = []

  onTestEnd(test: TestCase, result: TestResult) {
    if (result.retry > 0 && result.status === 'passed') {
      this.flakyTests.push({
        name: test.title,
        file: test.location.file,
        retries: result.retry,
      })
    }
  }

  onEnd() {
    if (this.flakyTests.length > 0) {
      console.warn(`\n⚠️  ${this.flakyTests.length} FLAKY TESTS DETECTED:`)
      this.flakyTests.forEach((t) => {
        console.warn(`   ${t.file} → "${t.name}" (passed on retry ${t.retries})`)
      })

      // Write to file for CI to pick up
      fs.writeFileSync(
        'test-results/flaky-tests.json',
        JSON.stringify(this.flakyTests, null, 2)
      )
    }
  }
}

export default FlakyTracker
```

### Quarantine Strategy

```
┌──────────────────────────────────────────────────────────────┐
│  FLAKY TEST QUARANTINE RULES                                 │
│                                                              │
│  1. A test that fails then passes on retry = FLAKY           │
│  2. Track flaky tests in a JSON file or dashboard            │
│  3. If a test is flaky 3+ times in a week:                   │
│     → Move to quarantine (skip in CI, keep in nightly)       │
│     → Create a ticket to fix the root cause                  │
│     → Set a deadline (2 weeks) to fix or delete              │
│  4. Quarantined tests still run nightly — just don't block   │
│  5. Never disable a test permanently — fix or delete it      │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 5 — Artifact Collection

### What to Collect on Failure

```yaml
# Collect everything needed to debug a failure without SSH
- name: Upload artifacts on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: debug-artifacts-${{ matrix.shard }}
    path: |
      # Screenshots of failed tests
      src/frontend/test-results/**/*.png
      # Videos of failed tests
      src/frontend/test-results/**/*.webm
      # Trace files (Playwright)
      src/frontend/test-results/**/*.zip
      # Test result JSON
      src/frontend/test-results/results.json
      # Server logs
      /tmp/backend.log
      /tmp/frontend.log
    retention-days: 7
```

### Server Log Capture

```yaml
# Capture server output to log files for debugging
- name: Start backend with logging
  run: |
    cd src/backend && npm run dev > /tmp/backend.log 2>&1 &
    echo $! > /tmp/backend.pid

- name: Start frontend with logging
  run: |
    cd src/frontend && npm start > /tmp/frontend.log 2>&1 &
    echo $! > /tmp/frontend.pid

# After tests, always upload logs
- name: Upload server logs
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: server-logs-${{ matrix.shard }}
    path: /tmp/*.log
```

---

## Step 6 — Coverage Reporting on PRs

### Coverage Comment Flow

```
┌──────────┐     Run Tests    ┌──────────┐     Generate     ┌──────────┐
│  PR Push │ ───────────────▶ │  Jest /  │ ──────────────▶  │ Coverage │
│          │                  │  Vitest  │                   │  JSON    │
└──────────┘                  └──────────┘                   └────┬─────┘
                                                                  │
                              ┌───────────────────────────────────┘
                              ▼
                    ┌──────────────────┐     Post        ┌──────────┐
                    │  Compare with   │ ───────────────▶ │  PR      │
                    │  main branch    │                   │  Comment │
                    │  coverage       │                   │          │
                    └──────────────────┘                  └──────────┘
```

### Jest Coverage Configuration

```javascript
// jest.config.js
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',        // barrel files
    '!src/**/*.stories.tsx',   // storybook
    '!src/types/**',           // type definitions
    '!src/**/__mocks__/**',    // mock files
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 75,
      lines: 80,
      statements: 80,
    },
    // Stricter thresholds for critical paths
    './src/services/auth/': {
      branches: 90,
      functions: 90,
      lines: 95,
    },
  },
  coverageReporters: [
    'text',                    // Console output
    'text-summary',            // Short console summary
    'json-summary',            // Machine-readable for CI
    'lcov',                    // For HTML report + Codecov
  ],
}
```

---

## Step 7 — Notification on Failure

### Slack Notification

```yaml
# At the end of the workflow
notify-failure:
  name: Notify on Failure
  runs-on: ubuntu-latest
  needs: [lint, unit-tests, integration-tests, e2e-tests]
  if: failure() && github.ref == 'refs/heads/main'
  steps:
    - name: Send Slack notification
      uses: slackapi/slack-github-action@v1
      with:
        payload: |
          {
            "blocks": [
              {
                "type": "header",
                "text": {
                  "type": "plain_text",
                  "text": "CI Failed on main"
                }
              },
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*Repo:* ${{ github.repository }}\n*Commit:* ${{ github.sha }}\n*Author:* ${{ github.actor }}\n*Run:* <${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
                }
              }
            ]
          }
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## Step 8 — Performance Optimization

### Speed Optimization Checklist

```
┌──────────────────────────────────────────────────────────────┐
│  CI SPEED OPTIMIZATION                                       │
│                                                              │
│  1. CACHE DEPENDENCIES                                       │
│     → npm ci with package-lock caching                       │
│     → Playwright browser cache                               │
│     → Docker layer caching                                   │
│                                                              │
│  2. PARALLELIZE EVERYTHING                                   │
│     → Lint, unit, integration, E2E: all separate jobs        │
│     → E2E tests: sharded across 2-8 runners                 │
│     → Unit tests: parallel with --maxWorkers=auto            │
│                                                              │
│  3. SKIP UNNECESSARY WORK                                    │
│     → Path filters: only run backend tests if backend changed│
│     → Don't build frontend for backend-only PRs              │
│     → Cancel outdated CI runs on the same branch             │
│                                                              │
│  4. FAIL FAST                                                │
│     → Lint runs first — catches typos in 30 seconds          │
│     → Type check before running tests                        │
│     → Cancel-in-progress for same-branch pushes              │
│                                                              │
│  5. OPTIMIZE TEST EXECUTION                                  │
│     → Use --forceExit to prevent Jest hanging                │
│     → Set timeouts on all CI jobs                            │
│     → Disable video recording unless test fails              │
└──────────────────────────────────────────────────────────────┘
```

### Path-Based Filtering

```yaml
# Only run backend tests when backend code changes
on:
  pull_request:
    paths:
      - 'src/backend/**'
      - 'prisma/**'
      - '.github/workflows/ci.yml'
```

### Dependency Caching

```yaml
# Cache npm dependencies
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
    cache-dependency-path: src/backend/package-lock.json

# Cache Playwright browsers
- name: Cache Playwright browsers
  uses: actions/cache@v4
  with:
    path: ~/.cache/ms-playwright
    key: playwright-${{ runner.os }}-${{ hashFiles('src/frontend/package-lock.json') }}
    restore-keys: |
      playwright-${{ runner.os }}-

- name: Install Playwright (only if cache miss)
  run: npx playwright install --with-deps chromium
  if: steps.cache-playwright.outputs.cache-hit != 'true'
```

---

## Common Mistakes / Anti-Patterns

```
┌──────────────────────────────────────────────────────────────┐
│  ANTI-PATTERN                    │  DO THIS INSTEAD          │
├──────────────────────────────────┼───────────────────────────┤
│  All tests in one job            │  Parallel jobs per type   │
│  No timeout on CI jobs           │  Always set timeout-mins  │
│  Video recording always on       │  Only on failure          │
│  Tests depend on prod database   │  Use CI service containers│
│  No retry on E2E tests           │  2 retries for E2E in CI  │
│  Retry on unit tests             │  Never retry unit tests   │
│  No artifacts on failure         │  Screenshots + logs + trace│
│  Full E2E suite on every PR      │  Smoke on PR, full nightly│
│  Ignoring flaky tests            │  Track + quarantine + fix │
│  No coverage thresholds          │  Set and enforce minimums │
│  npm install in CI               │  npm ci (deterministic)   │
│  No concurrency controls         │  cancel-in-progress: true │
│  Hardcoded secrets in workflow   │  GitHub Secrets only      │
│  Running all tests for docs PRs  │  Path-based filtering     │
└──────────────────────────────────┴───────────────────────────┘
```

---

## Tips for Best Results

1. **Start simple** — one job per test type, parallelize later when it gets slow
2. **Set timeouts aggressively** — if a job should take 5 min, set timeout to 10. Never leave it unbounded
3. **Cache everything** — npm, Playwright browsers, Docker layers. Cache hits save 30-60% of CI time
4. **Fail fast** — lint first, unit tests next, E2E last. Don't waste 20 min on E2E if lint fails
5. **Use `fail-fast: false`** for matrix jobs — you want ALL shard results even if one fails
6. **Separate PR checks from main checks** — PRs get smoke tests, main gets the full suite
7. **Monitor CI duration trends** — if your pipeline gets 2x slower over a month, investigate immediately
8. **Use services, not Docker Compose** — GitHub Actions services are faster and simpler for databases
9. **Never skip tests to unblock a deploy** — fix the test or revert the commit
10. **Review CI logs weekly** — find slow tests, frequently failing tests, and optimize

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
