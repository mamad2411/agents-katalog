---
name: ui-test-flow
description: "PRD and ad-hoc UI test execution flows. Use when running E2E tests, handling deferred tests, or managing E2E test execution. Triggers on: run e2e, e2e tests, deferred e2e, prd e2e, playwright tests."
---

# UI Test Flow

> Load this skill when: running E2E tests, handling PRD/ad-hoc mode E2E execution, or managing deferred E2E tests.

## PRD Mode Test Flow

**After each story completion, run the mandatory per-task quality checks** (see `test-flow` skill — Skip Gate → Activity Resolution → Quality Check Pipeline).

### Additional PRD-Specific Behavior

After the mandatory checks pass, PRD mode handles E2E based on **automatic activity resolution**:

| E2E Resolution | Behavior |
|----------------|----------|
| `immediate` | Run E2E tests now (including scoped Playwright via `postChangeWorkflow` pipeline), before marking story complete |
| `deferred` | Queue E2E tests for PRD completion |
| `skip` | No E2E (docs, config, type definitions) |

> ℹ️ **Playwright Integration:** For projects with Playwright in `postChangeWorkflow.steps[]`,
> `apps.*.testing.framework`, or `apps.*.type` of `frontend`/`desktop`, E2E resolves as
> `immediate` for ALL file types (not just auth/payment/API). This means components, hooks,
> pages, and styling changes trigger per-story Playwright verification instead of being deferred.
> `testing.autoGenerate` is NOT a gate — if the project has existing Playwright tests, they run
> regardless of the autoGenerate setting.

### PRD Story Completion Flow

```
Story complete
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ RESOLVE ACTIVITIES (automatic)                                      │
│ Based on files changed in this story                                │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ MANDATORY: Run resolved activities                                   │
│ (baseline, unit, critics, E2E if immediate)                         │
└─────────────────────────────────────────────────────────────────────┘
    │
    ├─── Any check fails ──► Fix loop ──► Still failing? STOP
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ If E2E = deferred: Queue for PRD completion                          │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
Next story (or PRD completion)
```

**After ALL stories complete:**

1. **Run all deferred E2E tests**
2. **If E2E tests fail:** Run @developer to fix (up to 3 attempts)
3. **Clear E2E queue** — Remove `deferredTo` flag, mark as passed

---

## Ad-hoc Mode Test Flow

**After each ad-hoc task completes, run the mandatory per-task quality checks.**

### Ad-hoc Task Completion Flow

```
Task complete
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ MANDATORY: Per-Task Quality Checks                                   │
│ (typecheck, lint, unit tests, critic)                               │
└─────────────────────────────────────────────────────────────────────┘
    │
    ├─── Any check fails ──► Fix loop ──► Still failing? STOP
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Show completion prompt                                               │
│ [C] Commit  [N] Next task                                            │
└─────────────────────────────────────────────────────────────────────┘
```

### E2E Deferral (During PRD)

After generating E2E tests in ad-hoc mode during PRD:

```
📝 E2E tests generated:
   • e2e/[test-name].spec.ts

Options:
   [R] Run E2E tests now (then return to PRD)
   [D] Defer to PRD completion (run with PRD's E2E tests)
   [S] Save for later (queue without deferring)
```

---

## Running E2E Tests

### Step 0: Detect Execution Mode (MANDATORY)

Before running any E2E tests, determine if this project uses Electron or browser-based testing:

```bash
# Check for Electron-only architecture
DEPLOYMENT=$(jq -r '.architecture.deployment // empty' docs/project.json)
ELECTRON_APP=$(jq -r '.apps | to_entries[] | select(.value.framework == "electron") | .key' docs/project.json 2>/dev/null)
ELECTRON_TESTING=$(jq -r '.apps | to_entries[] | select(.value.testing.framework == "playwright-electron") | .value.testing' docs/project.json 2>/dev/null)

if [ "$DEPLOYMENT" = "electron-only" ] || [ -n "$ELECTRON_APP" ]; then
  echo "ELECTRON_MODE=true"
  # Extract Electron-specific config
  TEST_DIR=$(jq -r '.apps | to_entries[] | select(.value.framework == "electron") | .value.testing.testDir // "e2e/desktop"' docs/project.json)
  EXEC_PATH=$(jq -r '.apps | to_entries[] | select(.value.framework == "electron") | .value.testing.executablePath.macos // empty' docs/project.json)
  
  # Look for Electron Playwright config
  ELECTRON_CONFIG=""
  for cfg in playwright.electron.config.ts e2e/playwright.electron.config.ts e2e/desktop/playwright.config.ts; do
    if [ -f "$cfg" ]; then
      ELECTRON_CONFIG="$cfg"
      break
    fi
  done
else
  echo "ELECTRON_MODE=false"
fi
```

**If ELECTRON_MODE=true:**
- Skip Steps 1 and 2 (no base URL or dev server needed — Electron launches the app directly)
- Jump to **Step 3E: Run Electron Tests** (below)
- Load the `ui-test-electron` skill for test writing patterns

**If ELECTRON_MODE=false:**
- Continue with existing Steps 1, 2, 3 (browser flow)

### Step 1: Resolve Test Base URL (MANDATORY)

Before running any Playwright tests:

```bash
# Resolution priority:
# 1. project.json → agents.verification.testBaseUrl (explicit override)
# 2. Preview URL env vars (Vercel, Netlify, Railway, Render, Fly.io)
# 3. project.json → environments.staging.url
# 4. http://localhost:{devPort} (from projects.json)

TEST_BASE_URL=$(jq -r '.agents.verification.testBaseUrl // empty' docs/project.json)

if [ -z "$TEST_BASE_URL" ]; then
  if [ -n "$VERCEL_URL" ]; then
    TEST_BASE_URL="https://${VERCEL_URL}"
  elif [ -n "$DEPLOY_URL" ]; then
    TEST_BASE_URL="$DEPLOY_URL"
  elif [ -n "$RAILWAY_PUBLIC_DOMAIN" ]; then
    TEST_BASE_URL="https://${RAILWAY_PUBLIC_DOMAIN}"
  elif [ -n "$RENDER_EXTERNAL_URL" ]; then
    TEST_BASE_URL="$RENDER_EXTERNAL_URL"
  elif [ -n "$FLY_APP_NAME" ]; then
    TEST_BASE_URL="https://${FLY_APP_NAME}.fly.dev"
  fi
fi

if [ -z "$TEST_BASE_URL" ]; then
  TEST_BASE_URL=$(jq -r '.environments.staging.url // empty' docs/project.json)
fi

if [ -z "$TEST_BASE_URL" ]; then
  DEV_PORT=$(jq -r '.projects[] | select(.path == "'$(pwd)'") | .devPort' ~/.config/opencode/projects.json)
  if [ -n "$DEV_PORT" ] && [ "$DEV_PORT" != "null" ]; then
    TEST_BASE_URL="http://localhost:${DEV_PORT}"
  fi
fi

if [ -z "$TEST_BASE_URL" ]; then
  echo "⏭️  E2E skipped: No test URL available"
  exit 0
fi

export TEST_BASE_URL
```

### Step 2: Ensure Test Environment is Accessible

```bash
if [[ "$TEST_BASE_URL" == http://localhost:* ]]; then
  ~/.config/opencode/scripts/check-dev-server.sh --project-path "$(pwd)"
else
  if ! curl -sf --max-time 10 "$TEST_BASE_URL" > /dev/null 2>&1; then
    echo "❌ Remote test URL not reachable: $TEST_BASE_URL"
    exit 1
  fi
fi
```

### Step 3: Run Tests

```bash
export TEST_BASE_URL
npx playwright test --reporter=list [list of test files]
```

### Step 3E: Run Electron Tests (Electron Mode Only)

> This step replaces Steps 1-3 when ELECTRON_MODE=true.

```bash
# Use Electron config if found, otherwise default
if [ -n "$ELECTRON_CONFIG" ]; then
  npx playwright test --config="$ELECTRON_CONFIG" --reporter=list [list of test files]
else
  # Fallback: run from Electron test directory
  npx playwright test --reporter=list "$TEST_DIR"/**/*.spec.ts
fi
```

**Key differences from browser mode:**
- No `TEST_BASE_URL` needed — Electron app launches directly via `_electron.launch()`
- No dev server check — the Electron app IS the server
- Workers must be 1 (`--workers=1`) — Electron tests cannot parallelize
- Timeout should be 60s+ (Electron apps take longer to start)
- Global setup should kill zombie Electron processes (see `ui-test-electron` skill)

**If executablePath is configured in project.json:**
```bash
# Pass to tests via environment variable
export ELECTRON_EXECUTABLE_PATH="$EXEC_PATH"
npx playwright test --config="$ELECTRON_CONFIG" --workers=1 --reporter=list
```

### Playwright Config: No webServer

> ⚠️ **Electron projects:** Do NOT use the browser config below. Electron tests use `_electron.launch()` 
> instead of `baseURL`. See the `ui-test-electron` skill for the correct Playwright config pattern.

> ⚠️ **Do NOT use Playwright's `webServer` config option.**
>
> Playwright's default `webServer` behavior kills the dev server when tests complete.

**Correct pattern:**

```typescript
import { defineConfig, devices } from '@playwright/test';

const TEST_BASE_URL = process.env.TEST_BASE_URL || `http://localhost:${process.env.DEV_PORT || '3000'}`;

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  reporter: 'list',
  
  use: {
    baseURL: TEST_BASE_URL,
    trace: 'on-first-retry',
  },

  // NO webServer config — dev server is managed externally

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } },
  ],
});
```

---

## E2E Auditor Integration

The `@ui-test-full-app-auditor` agent provides **proactive full-app E2E auditing**.

### When to Use E2E Auditor

| Scenario | Use @ui-test-full-app-auditor |
|----------|------------------|
| Full regression testing before release | ✅ |
| Periodic coverage audits | ✅ |
| After large refactors | ✅ |
| Testing a specific story change | ❌ Use @ui-tester-playwright |

### Key Differences from Story-Driven Testing

| Aspect | Story-Driven | Audit Mode |
|--------|--------------|------------|
| Trigger | Code change | User request |
| Scope | Changed files only | Entire application |
| Retries | 3 attempts | 5 attempts |
| On failure | Stop, report | Log, continue |
| Commits | Batch at end | After each passing test |

### Invoking E2E Auditor

```
Run @ui-test-full-app-auditor with:
  project: {project path}
  mode: full-audit | resume | prd-driven
  prd: {prd path, if prd-driven mode}
```

---

## State Updates During Test Flow

**When generating tests:**
```json
{
  "pendingTests": {
    "unit": {
      "generated": ["src/__tests__/Component.test.tsx"],
      "status": "pending"
    },
    "e2e": {
      "generated": ["e2e/feature.spec.ts"],
      "status": "pending",
      "deferredTo": "prd-completion"
    }
  }
}
```

**When running tests:**
```json
{
  "pendingTests": {
    "unit": {
      "generated": ["src/__tests__/Component.test.tsx"],
      "status": "passed",
      "lastRunAt": "ISO8601",
      "failureCount": 0
    }
  }
}
```
