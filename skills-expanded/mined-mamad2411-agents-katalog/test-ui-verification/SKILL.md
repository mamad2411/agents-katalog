---
name: test-ui-verification
description: "Playwright-based UI verification for all projects. Use when verifying UI changes in browser, generating verification tests, or handling selector strategies. Triggers on: ui verification, playwright required, browser verification, verification test, visual verification."
---

# Test UI Verification

> Load this skill when: verifying UI changes in browser, generating verification tests, or managing verification mode.

## UI Verification (Automatic for All Projects)

> 🎯 **Playwright browser verification is MANDATORY for all UI changes.**
>
> UI verification is **automatic** — no opt-in config required. All projects are treated as
> having UI that needs verification. Playwright always runs as part of the quality check pipeline.
>
> - All UI changes must be visually verified in a browser/app before task completion
> - Verification generates reusable test scripts in `tests/ui-verify/`
> - Screenshots are captured for visual confirmation

### Configuration

Read verification settings from `project.json`:

```json
{
  "agents": {
    "verification": {
      "selectorStrategy": "strict",
      "testDir": "tests/ui-verify",
      "screenshotDir": "ai-tmp/verification/screenshots",
      "reviewGeneratedTests": true
    }
  }
}
```

| Setting | Values | Description |
|---------|--------|-------------|
| `selectorStrategy` | `strict` / `flexible` | `strict` requires data-testid attributes |
| `testDir` | path | Where to save generated verification tests |
| `screenshotDir` | path | Where to save verification screenshots |
| `reviewGeneratedTests` | boolean | Whether @quality-critic reviews generated tests |

---

## Architecture-Aware Verification

> 🎯 **Before running verification, detect app architecture to choose the optimal strategy.**
>
> Desktop apps ALWAYS use `playwright-electron`, NEVER browser-based verification.
> The `webContent` field determines whether a rebuild is needed, not whether to use Electron.

### Step 0: Read App Architecture

```
function determineVerificationStrategy(project, changedFiles):
  # Check for postChangeWorkflow override first
  if project.postChangeWorkflow:
    return { strategy: "custom-workflow", steps: project.postChangeWorkflow.steps }
  
  for appName, appConfig in project.apps:
    if anyFileMatchesPath(changedFiles, appConfig.path):
      
      if appConfig.type == "desktop":
        if !appConfig.webContent:
          return { strategy: "error", message: "Missing 'webContent' field for desktop app. Add webContent: 'bundled' | 'remote' | 'hybrid' to apps[].'" }
        
        match appConfig.webContent:
          case "bundled":
            return { strategy: "rebuild-then-launch-app",
                     rebuild: true,
                     buildCommand: project.commands.build or appConfig.commands?.build,
                     devCommand: project.commands.dev or appConfig.commands?.dev,
                     playwright: "electron",
                     notes: "Electron loads bundled files — must rebuild + relaunch for changes to appear" }
          case "remote":
            return { strategy: "ensure-electron-running",
                     rebuild: false,
                     devCommand: project.commands.dev or appConfig.commands?.dev,
                     playwright: "electron",
                     notes: "HMR via dev server handles code changes, but Electron must be running for Playwright-Electron to connect" }
          case "hybrid":
            return { strategy: "rebuild-then-launch-app",
                     rebuild: true,
                     buildCommand: project.commands.build or appConfig.commands?.build,
                     devCommand: project.commands.dev or appConfig.commands?.dev,
                     playwright: "electron",
                     notes: "Hybrid app has both bundled and remote content — rebuild to be safe" }
      
      if appConfig.type == "mobile":
        if !appConfig.webContent:
          return { strategy: "error", message: "Missing 'webContent' field" }
        match appConfig.webContent:
          case "remote":
            return { strategy: "verify-web-url", baseUrl: appConfig.remoteUrl }
          default:
            return { strategy: "no-automated-verify", notes: "Mobile native verification not yet supported" }
      
      # Native Apple apps — XCUITest, not Playwright
      if appConfig.type == "desktop" and appConfig.framework in ["swiftui", "appkit", "swiftui-appkit"]:
        return { strategy: "xcuitest",
                 notes: "Native macOS app — use XCUITest via @swift-dev with ui-test-xcuitest skill, NOT Playwright browser verification" }
      
      if appConfig.type == "mobile" and appConfig.framework in ["swiftui", "uikit", "swiftui-uikit"]:
        return { strategy: "xcuitest",
                 notes: "Native iOS app — use XCUITest via @swift-dev with ui-test-xcuitest skill, NOT Playwright browser verification" }
      
      if appConfig.type in ["frontend", "fullstack"]:
        return { strategy: "browser", baseUrl: resolveTestBaseUrl(project) }
  
  return { strategy: "not-required" }
```

### Verification Strategy Table

| App Type | webContent | Strategy | How Verification Works |
|----------|------------|----------|------------------------|
| frontend/fullstack | n/a | `browser` | Standard Playwright against dev server (HMR) |
| desktop (Electron) | `bundled` | `rebuild-then-launch-app` | **Build** → **relaunch Electron** → verify with Playwright-Electron |
| desktop (Electron) | `remote` | `ensure-electron-running` | Ensure Electron process is running (HMR handles code changes) → verify with Playwright-Electron |
| desktop (Electron) | `hybrid` | `rebuild-then-launch-app` | **Build** → **relaunch Electron** → verify with Playwright-Electron |
| desktop (swiftui/appkit) | n/a | `xcuitest` | Route to `@swift-dev` with `ui-test-xcuitest` skill — **NOT** Playwright |
| mobile (swiftui/uikit) | n/a | `xcuitest` | Route to `@swift-dev` with `ui-test-xcuitest` skill — **NOT** Playwright |
| mobile | `remote` | `verify-web-url` | Test web URL directly in browser |
| mobile | other | `no-automated-verify` | No automated UI verify yet |
| backend/cli | n/a | `not-required` | No UI verification |

> ⛔ **CRITICAL: ALL desktop strategies use `playwright: "electron"`. NEVER use browser-based verification for desktop apps.**
>
> Even `webContent: "remote"` (where HMR delivers changes via dev server) requires connecting Playwright to the Electron process. Opening `localhost` in a browser is NOT the same as testing inside Electron — Electron has its own window chrome, IPC, and process model.

> ⛔ **`webContent: "remote"` means NEVER run a frontend build step for UI/renderer changes.**
>
> HMR (Hot Module Replacement) delivers code changes to the running app in real-time via the dev server.
> The only time an Electron app with `webContent: "remote"` needs a rebuild is for **main process changes** (electron main, preload scripts, IPC handlers) — and even then, only a relaunch, not a frontend build.
>
> | Change Type | webContent: "remote" Action |
> |-------------|----------------------------|
> | UI/renderer (components, styles, services) | **Nothing** — HMR delivers changes automatically |
> | Main process (electron main, preload, IPC) | **Relaunch Electron only** — no frontend build |
> | Shared packages (if compiled to dist/) | **Rebuild package** → HMR picks up changes |

### Custom Workflow Override

When `postChangeWorkflow` exists in `project.json`, execute its steps instead of auto-inferring.

> ⛔ **CRITICAL: Evaluate `condition` fields on each step.** Do NOT run all steps unconditionally.
> Many projects have conditional steps (e.g., "only rebuild UI if UI files changed"). Ignoring conditions wastes time and causes confusion.

```
if strategy == "custom-workflow":
  for step in steps:
    # Check condition BEFORE executing
    if step.condition:
      if !evaluateCondition(step.condition, changedFiles):
        log("Skipping step '{step.name}': condition not met ({step.condition})")
        continue
    
    match step.type:
      case "command":
        run(step.command)
        if step.required and exitCode != 0: BLOCK
      case "process":
        startProcess(step.command)
        waitForReady()
      case "playwright-check":
        runPlaywrightVerification()
        if step.required and failed: BLOCK
```

#### Condition Evaluation

| Condition Pattern | Meaning | Example |
|-------------------|---------|---------|
| `files-changed-in:{path}` | At least one changed file matches `{path}/**` | `files-changed-in:packages/ui/src/` |
| `always` | Always run (same as no condition) | `always` |

```
function evaluateCondition(condition, changedFiles):
  if condition starts with "files-changed-in:":
    prefix = condition.removePrefix("files-changed-in:")
    return changedFiles.any(f => f.startsWith(prefix))
  if condition == "always":
    return true
  # Unknown condition → run the step (fail open)
  log("WARNING: Unknown condition format '{condition}' — running step")
  return true
```

### Rebuild + Relaunch Flow (for `bundled` and `hybrid`)

```
1. Run build command:
   $ {buildCommand}        # e.g., "pnpm --filter desktop build"
   
2. Kill existing Electron process (if running):
   $ pkill -f electron     # or project-specific kill command
   
3. Launch Electron in dev mode:
   $ {devCommand} &        # e.g., "pnpm --filter desktop dev"
   
4. Wait for Electron ready signal (window visible, IPC ready)

5. Connect Playwright-Electron to the running process

6. Run verification assertions
```

### Ensure-Running Flow (for `remote`)

```
1. Check if Electron process is already running
   
2. If not running:
   $ {devCommand} &        # Launch Electron
   Wait for ready signal

3. If running:
   No action needed (HMR handles code changes automatically)

4. Connect Playwright-Electron to the running process

5. Run verification assertions
```

---

## Verification Flow

```
Task complete (file changes detected)
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 0: Determine Verification Strategy (Architecture Check)        │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: Check if UI verification required                           │
│                                                                     │
│ Check changed files:                                                 │
│   • UI files (*.tsx, *.jsx, *.vue, *.css, *.scss) → Continue        │
│   • Non-UI files only → Return { status: "not-required" }           │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Generate verification test                                   │
│                                                                     │
│ Run @ui-tester-playwright with mode: "verification"                       │
│   • Generates test in testDir                                        │
│   • If selectorStrategy: "strict", adds data-testid to components  │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: Run verification test                                       │
│                                                                     │
│ Execute: npx playwright test <generated-test>                       │
│ Capture screenshot to screenshotDir                                 │
└─────────────────────────────────────────────────────────────────────┘
    │
    ├─── PASS ──► Return { status: "verified" }
    │
    └─── FAIL ──► Fix loop (max 3 attempts)
                      │
                      └─── Still failing ──► User prompt [F/S/A]
```

---

## Verification Status Returns

```typescript
interface VerificationResult {
  status: "verified" | "unverified" | "skipped" | "not-required";
  reason: string;
  details: {
    testsGenerated?: string[];
    screenshotsCaptured?: string[];
    testsPassed?: boolean;
    attemptCount?: number;
    errors?: string[];
  };
}
```

| Status | When | Task Can Complete? |
|--------|------|-------------------|
| `verified` | UI change verified via Playwright | ✅ Yes |
| `unverified` | UI change not yet verified | ❌ No (blocked) |
| `skipped` | User explicitly skipped verification | ⚠️ Yes (with debt) |
| `not-required` | No UI changes detected in changed files | ✅ Yes |

---

## Verification Test Format

Generated verification tests include rich documentation headers:

```typescript
/**
 * @verification-test
 * @component PaymentForm
 * @location src/components/PaymentForm.tsx
 * @reach /checkout → click "Proceed to Payment"
 * 
 * @prerequisites
 *   - User must be logged in
 *   - Checkout page must load successfully
 * 
 * @feature-assertions
 *   - Form renders with all required fields
 *   - Card number field accepts valid input
 *   - Submit button is disabled until form is valid
 * 
 * @generated-at 2026-03-03T10:30:00Z
 */
import { test, expect } from '@playwright/test';

test.describe('PaymentForm verification', () => {
  test('renders and accepts valid input', async ({ page }) => {
    // ═══════════════════════════════════════════════════════════════
    // PREREQUISITES
    // ═══════════════════════════════════════════════════════════════
    await page.goto('/checkout');
    await page.click('text=Proceed to Payment');
    
    // ═══════════════════════════════════════════════════════════════
    // FEATURE ASSERTIONS
    // ═══════════════════════════════════════════════════════════════
    await expect(page.locator('[data-testid="payment-form"]')).toBeVisible();
    await expect(page.locator('[data-testid="card-number"]')).toBeVisible();
    
    await page.screenshot({ path: 'ai-tmp/verification/screenshots/payment-form.png' });
  });
});
```

---

## Selector Strategy Enforcement

### When `selectorStrategy: "strict"`

1. **Before generating verification test**, check for `data-testid` attributes
2. **If missing**, @ui-tester-playwright:
   - Identifies components that need test IDs
   - Adds `data-testid` attributes to source code
   - Commits: "chore: add data-testid attributes for e2e testing"
3. **Then generates test** using the `data-testid` selectors

### When `selectorStrategy: "flexible"`

- Tests may use role-based selectors, text content, or test IDs
- No requirement to add `data-testid` attributes

---

## Integration with Workflows

**Ad-hoc workflow:**
```
if verificationResult.status == "unverified":
    BLOCK task completion
    
if verificationResult.status == "skipped":
    WARN user
    Log to test-debt.json
```

**PRD workflow:**
```
if verificationResult.status == "unverified":
    BLOCK story completion
    Story remains in_progress
```

---

## Recording Verification Results

Update the current chunk's `chunk.json` → `verification`:

```json
{
  "verification": {
    "status": "verified",
    "results": [
      {
        "activity": "ui-verification",
        "status": "pass",
        "testsGenerated": ["tests/ui-verify/payment-form.spec.ts"],
        "screenshotsCaptured": ["ai-tmp/verification/screenshots/payment-form.png"],
        "attempts": 1,
        "completedAt": "2026-03-03T10:35:00Z"
      }
    ]
  }
}
```

---

## Skipping Verification (Escape Hatch)

```
User: "skip verification"

⚠️ SKIPPING UI VERIFICATION

This will:
- Mark task as complete WITHOUT browser verification
- Add this file to test-debt.json for escalated future testing
- Log the skip reason

Are you sure? [Y/N]
```

If confirmed:
1. Return `{ status: "skipped", reason: "User requested skip" }`
2. Add changed UI files to `test-debt.json`
3. Allow task completion with warning

---

## Flaky Test Detection

### Detection Criteria

A test is **flaky** when it:
- Passes on some runs but fails on others
- Fails with timing-related errors
- Fails with non-deterministic assertion failures

### Detection Method

```
Test fails on first run
    │
    ▼
Re-run the SAME test 2 more times
    │
    ├─── All 3 fail consistently ──► NOT flaky (genuine failure)
    │
    └─── Mixed results ──► FLAKY
```

### Flakiness Response

```
⚠️ FLAKY TEST DETECTED

Test: payment-form.spec.ts → "renders and accepts valid input"
Results: 1/3 passes (66% failure rate)

Failure pattern:
- Run 1: FAIL — Timeout waiting for selector
- Run 2: PASS
- Run 3: FAIL — Timeout waiting for selector

Analysis: Likely timing issue

Action: Escalating to @ui-tester-playwright for fix...
```

### Verification After Fix

After the delegate agent fixes the flaky test:

1. **Re-run the test 3 times consecutively**
2. **All 3 must pass** to consider the fix successful
3. **If still flaky**, offer quarantine option

### Quarantine Option

For persistently flaky tests:

1. Move test file to `tests/quarantine/`
2. Add entry to `test-debt.json`
3. Quarantined tests excluded from CI but tracked for follow-up

---

## Analysis Probe Mode (Pre-Implementation Verification)

> 🎯 **Use this mode during ad-hoc Analysis Gate (Phase 0) to confirm code analysis conclusions against live app state.**
>
> Analysis probes are lightweight, fast, ephemeral checks — NOT full E2E tests.
> They verify that the elements, pages, and states referenced in the analysis actually exist at runtime.

### When to Use

This mode is invoked by Builder during the ad-hoc workflow **Step 0.1b** — after code analysis (Step 0.1) and before showing the ANALYSIS COMPLETE dashboard (Step 0.2).

**Trigger:** `@ui-tester-playwright` with `mode: "analysis-probe"`

### Architecture-Aware Probe Dispatch (MANDATORY)

> ⛔ **CRITICAL: Before generating the probe spec, check `project.json` → `apps` for desktop app configuration.**
>
> Desktop apps MUST use `playwright-electron` for analysis probes — never browser-based probing.
> A headless browser hitting `localhost:{devPort}` is NOT testing the Electron app. It's testing bare web content without the Electron shell, IPC bridge, preload script, or desktop-specific behavior.
>
> **Trigger:** Before generating probe-spec in Step 0.1b.
> **Evidence:** Probe spec must contain `transport: "electron"` for desktop apps.
> **Failure behavior:** If a desktop app's probe spec contains `baseUrl` without `transport: "electron"`, the probe is misconfigured — STOP and regenerate.

**Dispatch logic:**

```
function determineProbeTransport(project):
  for appName, appConfig in project.apps:
    if appConfig.type == "desktop":
      # Native Apple app — NOT a Playwright target
      if appConfig.framework in ["swiftui", "appkit", "swiftui-appkit"]:
        return {
          transport: "xcuitest",
          notes: "Native macOS app — route to @swift-dev with ui-test-xcuitest skill, NOT Playwright"
        }
      
      # Desktop Electron app — MUST use Electron transport
      return {
        transport: "electron",
        executablePath: appConfig.testing?.executablePath?.[platform],
        launchTarget: appConfig.testing?.launchTarget,  # "installed-app" or "dev-build"
        devLaunchArgs: appConfig.testing?.devLaunchArgs,
        authHelper: project.authentication?.headless?.helperModule,
        notes: "Connect Playwright to the Electron process, NOT a browser against localhost"
      }
    
    if appConfig.type == "mobile":
      # Native iOS app — NOT a Playwright target
      if appConfig.framework in ["swiftui", "uikit", "swiftui-uikit"]:
        return {
          transport: "xcuitest",
          notes: "Native iOS app — route to @swift-dev with ui-test-xcuitest skill, NOT Playwright"
        }
  
  # No desktop app — standard browser probe
  return {
    transport: "browser",
    baseUrl: resolveTestBaseUrl(project)
  }
```

| App Type | Transport | How Probe Connects |
|----------|-----------|-------------------|
| Web/fullstack | `browser` | Standard Playwright against `http://localhost:{devPort}` |
| Desktop (any `webContent`) | `electron` | Playwright `_electron.launch()` with `executablePath` from `project.json` → `apps.desktop.testing` |
| Desktop (swiftui/appkit) | `xcuitest` | NOT a Playwright probe — route to `@swift-dev` with `ui-test-xcuitest` skill |
| Mobile (swiftui/uikit) | `xcuitest` | NOT a Playwright probe — route to `@swift-dev` with `ui-test-xcuitest` skill |

> ⛔ **Even `webContent: "remote"` desktop apps use Electron transport.** The web content loads inside Electron's renderer process — probing `localhost` in a browser misses IPC, preload scripts, Electron-specific navigation, and desktop window behavior.

### Configuration

Analysis probe mode uses project-level verification settings but with lighter constraints:

| Setting | Value | Why |
|---------|-------|-----|
| `timeout` | 5 seconds per page | Probes must be fast — analysis is time-boxed |
| `testGeneration` | None — probes are ephemeral | No files saved to `testDir` |
| `screenshots` | Optional — only on contradiction | Save screenshot when probe contradicts analysis |
| `retries` | 0 | Probes are one-shot; failure = useful signal |

### Probe Specification Format

Builder generates a probe specification from Step 0.1 code analysis and passes it to `@ui-tester-playwright`. **The spec format depends on the probe transport determined by Architecture-Aware Probe Dispatch above.**

#### Browser Probe Spec (web apps)

```yaml
<probe-spec>
  mode: analysis-probe
  transport: browser
  baseUrl: "http://localhost:{devPort}"
  timeout: 5000
  assertions:
    - page: "/checkout"
      description: "Submit button exists on checkout page"
      checks:
        - selector: "[data-testid='submit-btn'], button[type='submit']"
          expect: "visible"
        - selector: ".spinner, [data-testid='loading-spinner']"
          expect: "absent"
          description: "No loading indicator currently exists"
    - page: "/checkout"
      description: "Form is interactive"
      checks:
        - selector: "button[type='submit']"
          expect: "enabled"
</probe-spec>
```

#### Electron Probe Spec (desktop apps)

> ⛔ **Use this format when `project.json` → `apps` contains a `type: "desktop"` entry.**
> The probe connects to the running Electron app via `_electron.launch()`, NOT a browser against localhost.

```yaml
<probe-spec>
  mode: analysis-probe
  transport: electron
  executablePath: "{from project.json → apps.desktop.testing.executablePath[platform]}"
  launchTarget: "{from project.json → apps.desktop.testing.launchTarget}"
  devLaunchArgs: ["{from project.json → apps.desktop.testing.devLaunchArgs}"]
  authHelper: "{from project.json → authentication.headless.helperModule}"
  timeout: 10000
  assertions:
    - page: "/settings"
      description: "GitHub connect button exists"
      checks:
        - selector: "[data-testid='github-connect'], button:has-text('Connect GitHub')"
          expect: "visible"
        - selector: "[data-testid='github-connected']"
          expect: "absent"
          description: "Not yet connected"
  electronChecks:
    - description: "IPC handler registered"
      evaluate: "electronApp.evaluate(({ ipcMain }) => ipcMain.listenerCount('github:connect'))"
      expect: "greater-than:0"
</probe-spec>
```

**Key differences from browser probes:**
- `transport: electron` — connects via Playwright's `_electron` API
- `executablePath` — read from `project.json` → `apps.desktop.testing.executablePath`
- `launchTarget` — `"installed-app"` or `"dev-build"` (determines launch method)
- `timeout: 10000` — Electron apps take longer to launch than page navigation
- `electronChecks` — optional main process assertions via `electronApp.evaluate()`
- `authHelper` — helper module for auth injection if the app requires authentication
- **NO `baseUrl`** — the probe connects to the Electron process, not a URL

**Electron probe execution flow:**
1. Read `executablePath` and `launchTarget` from `project.json` → `apps.desktop.testing`
2. Kill any existing instances (see `ui-test-electron` skill → Zombie Process Cleanup)
3. Launch Electron: `_electron.launch({ executablePath })` or `_electron.launch({ args: devLaunchArgs })`
4. Get first window: `electronApp.firstWindow()`
5. Authenticate if needed using `authHelper` module
6. Run assertions against the window (same selectors/expects as browser probes)
7. Run `electronChecks` against the main process if specified
8. Close Electron app

### Probe Assertion Types

| Expect Value | What It Checks | Passes When |
|-------------|----------------|-------------|
| `visible` | Element exists and is visible | `element.isVisible() === true` |
| `absent` | Element does not exist or is hidden | `element.count() === 0` or `!element.isVisible()` |
| `enabled` | Element exists and is not disabled | `element.isEnabled() === true` |
| `disabled` | Element exists and is disabled | `element.isEnabled() === false` |
| `text-contains:{value}` | Element contains specific text | `element.textContent().includes(value)` |
| `exists` | Element exists in DOM (visible or not) | `element.count() > 0` |

### Probe Execution Flow

```
Builder passes probe-spec to @ui-tester-playwright
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 0: Check transport                                              │
│                                                                     │
│ if transport == "electron":                                          │
│   → Go to Electron Probe Flow (below)                               │
│ if transport == "browser" (or unspecified):                          │
│   → Continue to STEP 1                                              │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: Validate probe spec (browser transport)                      │
│   • Ensure baseUrl is reachable                                      │
│   • Validate assertion format                                        │
│   • If baseUrl unreachable → return { status: "error",               │
│     reason: "Dev server not reachable — Builder must start it" }     │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Execute probes (5s timeout per page)                         │
│                                                                     │
│ For each page in assertions:                                         │
│   1. Navigate to page                                                │
│   2. Wait for networkidle (max 3s)                                   │
│   3. Run each check against the DOM                                  │
│   4. Record result: { match: true/false, actual: "..." }            │
│                                                                     │
│ If page navigation fails → record as contradiction                   │
│ If timeout → record as { match: false, actual: "timeout" }          │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: Aggregate results                                            │
│                                                                     │
│ overallStatus:                                                       │
│   • ALL assertions match → "confirmed"                               │
│   • ≥50% match → "partially-confirmed"                               │
│   • <50% match → "contradicted"                                      │
│                                                                     │
│ If "contradicted": capture screenshot of contradicting page          │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
Return ProbeResult to Builder
```

#### Electron Probe Flow

> ⛔ **This flow is mandatory when `transport: "electron"` is specified in the probe spec.**
> Loading `localhost:{devPort}` in a headless browser is NOT equivalent to probing the Electron app.

```
Builder passes probe-spec with transport: "electron" to @ui-tester-playwright
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP E1: Kill zombie Electron processes                              │
│   • See ui-test-electron skill → Zombie Process Cleanup                  │
│   • Kill any existing instances of the app                           │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP E2: Launch Electron app                                         │
│                                                                     │
│ if launchTarget == "installed-app":                                   │
│   electronApp = _electron.launch({                                   │
│     executablePath: "{executablePath from probe-spec}"               │
│   })                                                                 │
│ if launchTarget == "dev-build":                                      │
│   electronApp = _electron.launch({                                   │
│     args: devLaunchArgs from probe-spec                              │
│   })                                                                 │
│                                                                     │
│ If launch fails → return { status: "error",                          │
│   reason: "Electron app failed to launch — check executablePath" }  │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP E3: Get window and authenticate                                 │
│                                                                     │
│ window = electronApp.firstWindow()                                   │
│ Wait for app ready (data-ready attribute or reasonable timeout)      │
│                                                                     │
│ if authHelper specified:                                             │
│   Import and call auth helper to inject session                      │
│   (e.g., adminAuthLogin from e2e/desktop/helpers/db.ts)             │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP E4: Execute assertions (10s timeout per page)                   │
│                                                                     │
│ For each page in assertions:                                         │
│   1. Navigate within the app window (window.goto or click nav)      │
│   2. Wait for networkidle (max 5s)                                   │
│   3. Run each check against the window DOM                           │
│   4. Record result: { match: true/false, actual: "..." }            │
│                                                                     │
│ For each electronCheck (if specified):                                │
│   1. Run electronApp.evaluate() with the check code                  │
│   2. Compare result against expected value                           │
│   3. Record result                                                   │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP E5: Aggregate results + cleanup                                 │
│                                                                     │
│ Same aggregation as browser flow (confirmed/partially/contradicted)  │
│ Close Electron app: electronApp.close()                              │
└─────────────────────────────────────────────────────────────────────┘
    │
    ▼
Return ProbeResult to Builder
```

### Probe Result Format

```typescript
interface ProbeResult {
  status: "confirmed" | "partially-confirmed" | "contradicted" | "user-skipped";
  reason?: string;
  assertions: ProbeAssertionResult[];
  discrepancies: ProbeDiscrepancy[];
  screenshotsCaptured?: string[];
  executionTimeMs: number;
}

interface ProbeAssertionResult {
  page: string;
  description: string;
  selector: string;
  expected: string;
  actual: string;
  match: boolean;
}

interface ProbeDiscrepancy {
  page: string;
  description: string;
  expected: string;
  actual: string;
  impact: "analysis-invalid" | "analysis-incomplete" | "minor";
}
```

### How Builder Uses Probe Results

| Probe Status | Effect on Analysis | Dashboard Display |
|-------------|-------------------|-------------------|
| `confirmed` | Analysis proceeds as-is | `Confidence: HIGH ✅ Playwright-confirmed` |
| `partially-confirmed` | Analysis updated with corrections; confidence may remain or lower | `Confidence: HIGH ⚠️ Playwright: N/M assertions confirmed` |
| `contradicted` | Analysis MUST be revised; confidence lowered to MEDIUM minimum | `Confidence: MEDIUM 🔴 Playwright contradicted analysis` |
| `user-skipped` | User explicitly accepted skip on authenticated pages after Builder exhausted all auth approaches and asked for help | `Confidence: [original] ⚠️ User accepted skip` |

### Confidence Impact Rules

> ⛔ **Probe contradictions ALWAYS lower confidence.**

| Original Confidence | Probe Status | Resulting Confidence |
|---------------------|-------------|---------------------|
| HIGH | `confirmed` | HIGH |
| HIGH | `partially-confirmed` | HIGH (if discrepancies are `minor`) or MEDIUM |
| HIGH | `contradicted` | MEDIUM (forces clarifying questions) |
| MEDIUM | `confirmed` | MEDIUM (probe alone cannot raise confidence) |
| MEDIUM | `contradicted` | LOW |
| LOW | any | LOW (already at minimum) |

### Mandatory Enforcement

> ⛔ **The probe always runs. There are no skip conditions. There is no config opt-out.**

**Resolution rules for common obstacles:**

| Obstacle | Resolution |
|----------|------------|
| Dev server unreachable | Start the dev server using `start-dev-server` skill. If the target is a desktop app, download and install it. There must always be a way to get the target running. |
| No page assertions generated | Generate assertions. If analysis cannot produce assertions, the analysis is incomplete — re-analyze. |
| Auth fails | Exhaust all autonomous auth approaches, then ask the user for help. See "Integration with Authentication" below. |

> ⛔ **Common rationalization attempts (Builder MUST reject all of these):**
>
> | Rationalization | Why It's Wrong |
> |-----------------|----------------|
> | Electron/Tauri/desktop app | Desktop apps with `webContent: "remote"` or `"bundled"` have web UI — probe it |
> | "Code analysis is clear" | Probes verify runtime state, not code correctness |
> | "UX/flow restructuring" | If the change affects visible pages, probe those pages |
> | "Screenshot already captured" | Screenshots ≠ probes — probes verify specific assertions |
> | "Backend/config change only" | If the change has any runtime UI impact, probe the affected pages — don't preemptively decide |
> | "Auth is not configured" | Ask the user for help configuring auth — do not skip |
>
> **Rule:** If the app has web content (any `webContent` value or web-based app), the probe MUST run.
> The probe target URL depends on app type — see "Architecture-Aware Verification" above.

### Project Configuration

Projects can configure probe timeout in `project.json`:

```json
{
  "agents": {
    "analysisProbeTimeoutMs": 5000
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `analysisProbeTimeoutMs` | `5000` | Timeout per page probe in milliseconds |

> ⛔ **There is no `analysisProbe` toggle.** The probe is mandatory and cannot be disabled via configuration.

### Integration with Authentication

> ⛔ **Authenticated pages are NOT optional probe targets.**
> If the pages being changed require auth, you MUST authenticate before probing.
> Skipping authenticated pages requires **explicit user acceptance** after all auth approaches are exhausted.

**Authentication escalation ladder** (try each step before moving to the next):

1. **Check `project.json` → `authentication`** for existing auth configuration
2. **If configured:** Load the matching auth skill and authenticate in the Playwright context:
   - `provider: supabase` + `method: passwordless-otp` → load `auth-supabase-otp` skill
   - `provider: supabase` + `method: email-password` → load `auth-supabase-password` skill
   - `provider: nextauth` + `method: email-password` → load `auth-nextauth-credentials` skill
   - `headless: true` → load `auth-headless` skill for faster API-based auth
   - Other providers → load `auth-generic` skill
3. **If NOT configured:** Load the `setup-auth` skill to detect and configure auth autonomously
4. **If `setup-auth` fails** → **Ask the user for help** with specific questions:
   - "What auth provider does this project use?"
   - "Can you provide test credentials?"
   - "Are there env vars I should check?"
5. **If user provides info** → Try again with user-provided guidance
6. **If user cannot help or says "skip"** → Set `probeStatus: "user-skipped"` and proceed with public pages only. Builder cannot set `user-skipped` autonomously — it requires user's explicit `[S]` acceptance.

**Page routing:**

| Page type | Action |
|-----------|--------|
| Public (login, marketing, docs) | Probe directly, no auth needed |
| Authenticated (dashboard, settings, admin) | Authenticate first using escalation ladder above, then probe |
| Mixed (some public, some authenticated) | Probe public pages immediately; authenticate then probe protected pages |

### Example Probe Flow

```
Builder (after code analysis):
  "Analysis says: Submit button exists at /checkout, no spinner present"

Builder generates probe-spec:
  assertions:
    - page: "/checkout"
      checks:
        - selector: "button[type='submit']"  expect: "visible"
        - selector: ".spinner"               expect: "absent"

@ui-tester-playwright runs probe:
  ✅ button[type='submit'] → visible (match)
  ✅ .spinner → absent (match)

Result: { status: "confirmed", assertions: 2/2 match }

Builder shows dashboard:
  📊 UNDERSTANDING                          Confidence: HIGH ✅ Playwright-confirmed
```
