---
name: electron-build-deploy
description: "Build and deploy Electron app before Playwright verification so tests run against newly-built code. Triggered by test-flow when buildDeploy is configured. Triggers on: electron build, electron deploy, desktop app build, build before test."
---

# Electron Build-Deploy Skill

> **Trigger:** test-flow Step 3.5 detects `apps.desktop.buildDeploy` in `project.json`
> **Purpose:** Build the Electron app, deploy to the test app location, and relaunch — so Playwright verifies newly-built code, not stale code.

## When This Skill Loads

test-flow loads this skill at Step 3.5 when ALL of these are true:
1. `project.json` has `apps.desktop.buildDeploy` configured
2. Changed files match at least one pattern in `buildDeploy.triggerPaths`
3. Typecheck, lint, and unit tests have already passed

## Configuration Reference

Read these fields from `project.json` → `apps.desktop.buildDeploy`:

| Field | Example | Description |
|-------|---------|-------------|
| `buildCommand` | `"pnpm build"` | Command to build the Electron app |
| `buildOutputApp` | `"apps/desktop/dist/mac-universal/Helm.app"` | Path to the built `.app` bundle (relative to project root) |
| `testApp` | `"/Applications/Helm Preview.app"` | Absolute path to the installed test app |
| `buildTimeoutMs` | `300000` | Build timeout in ms (default: 5 minutes) |
| `autoDeployAfterStory` | `true` | Whether to auto-deploy (default: true) |
| `triggerPaths` | `["apps/desktop/electron/**"]` | Glob patterns — if changed files match, rebuild is needed |

## Execution Sequence

> ⛔ **CRITICAL: Execute ALL steps in order. Do NOT skip any step.**
> Builder has a pattern of skipping deploy/relaunch steps. This skill exists specifically to prevent that.
> Every step below is REQUIRED. Skipping any step means Playwright tests verify stale code.

### Step 1: Report Start

```
🔨 Building Electron app...
   Build command: {buildCommand}
   Timeout: {buildTimeoutMs / 1000}s
```

### Step 2: Run Build Command

```bash
{buildCommand}
```

- Run from the **project root directory**
- Timeout: `buildTimeoutMs` (default 300000ms / 5 minutes)
- **If build fails → STOP. Report failure. Do NOT proceed to deploy or Playwright.**
- **If build times out → STOP. Report timeout. Do NOT proceed.**

### Step 3: Kill Running Test App

> ⛔ **Do NOT skip this step.** The `.app` bundle cannot be overwritten while the process is running.

Derive the process name from the `testApp` path (strip `/Applications/` and `.app`):

```bash
killall "{processName}" 2>/dev/null || true
```

Example: `testApp: "/Applications/Helm Preview.app"` → `killall "Helm Preview"`

- Wait 2 seconds after kill to ensure the process fully exits
- `|| true` because the app may not be running — that's fine

```bash
sleep 2
```

### Step 4: Copy Built App to Test Location

> ⛔ **Do NOT skip this step.** Without this copy, the installed app still has the old code.

```bash
cp -R "{buildOutputApp}/." "{testApp}/"
```

- Uses `/.` to copy the **contents** of the bundle, not the bundle itself
- The target path MUST be quoted (app names typically contain spaces)
- **If copy fails → STOP. Report failure. Do NOT proceed to Playwright.**

Verify the copy succeeded:

```bash
ls -la "{testApp}/Contents/MacOS/"
```

### Step 5: Relaunch Test App

> ⛔ **Do NOT skip this step.** Playwright-Electron launches the installed app. If it's not running or was just killed, Playwright needs a fresh instance.

```bash
open "{testApp}"
```

- Wait 3 seconds after launch for the app to initialize
- This step ensures the app is running with the new code before Playwright connects

```bash
sleep 3
```

### Step 6: Report Success

```
✅ Electron build-deploy complete
   Built: {buildOutputApp}
   Deployed to: {testApp}
   Build time: {elapsed}s
   Status: Ready for Playwright verification
```

## Error Handling

| Error | Action |
|-------|--------|
| Build command fails (non-zero exit) | STOP. Report build error with full output. Return failure to test-flow. |
| Build times out | STOP. Report timeout. Return failure to test-flow. |
| `killall` fails | Ignore (app may not be running). Continue to Step 4. |
| `cp -R` fails | STOP. Report copy error (permissions? disk space?). Return failure to test-flow. |
| `open` fails | STOP. Report launch error. Return failure to test-flow. |

## Return Value

Report back to test-flow:

| Result | test-flow behavior |
|--------|-------------------|
| **Success** | Proceed to Playwright verification |
| **Failure** | Treat as test-flow failure. Enter fix loop (max 3 attempts). |
| **Skipped** (no trigger paths matched) | Proceed to Playwright — no rebuild needed |

## What This Skill Does NOT Do

- Does NOT run Playwright tests (test-flow handles that after this skill succeeds)
- Does NOT handle code signing or notarization
- Does NOT handle CI/CD builds
- Does NOT handle cross-platform builds (macOS only for now)
- Does NOT modify source code
