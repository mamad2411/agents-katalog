---
name: ui-test-electron
description: "Patterns for Playwright E2E tests for Electron applications. Use when testing desktop apps built with Electron. Triggers on: Electron tests, desktop E2E, Electron app testing."
---

# UI Test Electron Testing Skill

This skill provides patterns and instructions for writing Playwright E2E tests for Electron applications.

## Triggers

Load this skill when:
- `apps[*].framework === 'electron'`
- `apps[*].testing.framework === 'playwright-electron'`
- `apps[*].type === 'desktop'` and Electron detected in `package.json`

## Launch Target Resolution (MANDATORY)

> ⛔ **CRITICAL: Before writing ANY Electron E2E test, read `project.json → apps[].testing` to determine the launch target.**
>
> The launch target determines EVERYTHING: test directory, launch pattern, Playwright config, and binary path.
> Getting this wrong produces tests that compile but test the wrong thing.

### Step 1: Read Launch Configuration

```
function resolveLaunchConfig(project):
  for appName, appConfig in project.apps:
    if appConfig.type == "desktop" and appConfig.testing:
      testing = appConfig.testing
      return {
        launchTarget: testing.launchTarget or "dev",      # "installed-app" | "dev"
        executablePath: testing.executablePath or null,    # platform-specific paths
        testDir: testing.testDir or "e2e/desktop/",       # where tests live
        playwrightConfig: testing.playwrightConfig or null # which config to use
      }
  return { launchTarget: "dev", executablePath: null, testDir: "e2e/", playwrightConfig: null }
```

### Step 2: Apply Launch Target Rules

| `launchTarget` | Test Directory | Launch Pattern | Playwright Config |
|----------------|---------------|----------------|-------------------|
| `"installed-app"` | `{testDir}` (often `e2e/desktop/installed-app/`) | `_electron.launch({ executablePath: ... })` with binary path | `{playwrightConfig}` (often `playwright.installed-app.config.ts`) |
| `"dev"` (default) | `e2e/desktop/` or `e2e/` | `electron.launch({ args: ['./path/to/main.js'] })` from source | `playwright.electron.config.ts` or `playwright.config.ts` |

### Step 3: Resolve Executable Path

When `launchTarget: "installed-app"`:

```typescript
// Read executablePath from project.json → apps[].testing.executablePath
// It's platform-specific — use the correct one for the current OS

function getAppPath(executablePath: Record<string, string>): string {
  const platform = process.platform;
  const path = executablePath[platform === 'darwin' ? 'darwin' : platform === 'win32' ? 'win32' : 'linux'];
  if (!path) throw new Error(`No executablePath configured for platform: ${platform}`);
  
  // Expand ~ to home directory
  return path.replace(/^~/, os.homedir());
}
```

> ⛔ **NEVER use `launchElectronApp()` or `electron.launch({ args: [...] })` when `launchTarget: "installed-app"`.**
> These launch from dev source — you must use `_electron.launch({ executablePath: ... })` with the installed binary.

### Step 4: Verify Before Writing

Before creating any test file:

```
□ Read project.json → apps[].testing.launchTarget
□ If "installed-app": test goes in installed-app subdirectory, uses binary launch
□ If "dev" or missing: test goes in standard directory, uses source launch  
□ Playwright config resolved from project.json or filesystem search
□ executablePath resolved for current platform (if installed-app)
```

## Zombie Process Cleanup (CRITICAL)

> ⛔ **Electron apps leave zombie processes when tests fail or are interrupted.**
>
> **Symptoms:**
> - Multiple dock icons on macOS
> - "App already running" errors
> - Tests hang indefinitely
> - CPU usage from orphaned Electron processes
>
> **Fix:** Use `globalSetup.ts` to clean up before EVERY test run.

### globalSetup.ts Pattern (MANDATORY)

Create `playwright/globalSetup.ts`:

```typescript
import { execSync } from 'child_process';

/**
 * Playwright global setup for Electron tests.
 * Kills any zombie Electron processes from previous runs.
 * 
 * CRITICAL: This prevents "app already running" errors and zombie processes.
 */
export default async function globalSetup(): Promise<void> {
  const appName = process.env.ELECTRON_APP_NAME || 'Electron';
  
  console.log(`[globalSetup] Cleaning up zombie ${appName} processes...`);
  
  if (process.platform === 'darwin') {
    // macOS cleanup
    try {
      // Kill Electron helper processes
      execSync('pkill -9 -f "Electron Helper" || true', { stdio: 'ignore' });
      // Kill main Electron process
      execSync('pkill -9 -f "Electron" || true', { stdio: 'ignore' });
      // Kill named app if different from "Electron"
      if (appName !== 'Electron') {
        execSync(`killall -9 "${appName}" || true`, { stdio: 'ignore' });
      }
      // Brief delay to ensure processes are fully terminated
      await new Promise(resolve => setTimeout(resolve, 500));
      console.log('[globalSetup] Cleanup complete');
    } catch {
      // Ignore errors — processes may not exist
    }
  } else if (process.platform === 'win32') {
    // Windows cleanup
    try {
      execSync(`taskkill /F /IM "${appName}.exe" /T || exit 0`, { stdio: 'ignore' });
      execSync('taskkill /F /IM "electron.exe" /T || exit 0', { stdio: 'ignore' });
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch {
      // Ignore errors
    }
  } else {
    // Linux cleanup
    try {
      execSync('pkill -9 -f "electron" || true', { stdio: 'ignore' });
      if (appName !== 'Electron') {
        execSync(`pkill -9 -f "${appName}" || true`, { stdio: 'ignore' });
      }
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch {
      // Ignore errors
    }
  }
}
```

### Integration with Playwright Config

Update `playwright.config.ts` to use the global setup:

```typescript
import { PlaywrightTestConfig } from '@playwright/test';
import path from 'path';

const config: PlaywrightTestConfig = {
  testDir: './e2e',
  testMatch: '**/electron.spec.ts',
  timeout: 60000,
  retries: 1,
  workers: 1,
  
  // CRITICAL: Global setup runs before all tests
  globalSetup: path.join(__dirname, 'playwright/globalSetup.ts'),
  
  use: {
    trace: 'on-first-retry',
    video: 'on-first-retry',
  },
};

export default config;
```

### Environment Variable for App Name

Set `ELECTRON_APP_NAME` to your app's exact name as it appears in the process list:

```bash
# In your test script (package.json)
"test:e2e:electron": "ELECTRON_APP_NAME='MyApp' npx playwright test e2e/electron.spec.ts"
```

### Pre-Test Zombie Detection (test-flow Integration)

The `test-flow` skill checks for zombie processes before starting tests. If zombies are detected:

1. **Warning shown** with count of running processes
2. **Auto-cleanup offered** if count > 1
3. **Proceeds after cleanup** or user confirmation

Example output when zombies detected:
```
⚠️ ZOMBIE ELECTRON PROCESSES DETECTED

Found 3 Electron-related processes:
  PID 12345: Electron Helper (Renderer)
  PID 12346: Electron Helper (GPU)
  PID 12347: MyApp

[K] Kill all and continue
[S] Skip cleanup (may cause test failures)
```

## Prerequisites

Ensure the project has Playwright installed with Electron support:

```bash
npm install -D @playwright/test playwright
```

No additional packages are needed — Playwright has built-in Electron support via `_electron` API.

## Electron App Structure

Understand the Electron architecture before testing:

```
apps/desktop/
├── src/
│   ├── main/           # Main process (Node.js)
│   │   ├── index.ts    # Entry point
│   │   └── preload.ts  # Preload script (bridge)
│   └── renderer/       # Renderer process (Chromium)
│       └── index.html
├── package.json
└── electron-builder.yml
```

**Key concepts:**
- **Main process**: Node.js process that creates windows, handles system integration
- **Renderer process**: Chromium browser that displays UI (your React/Vue/etc app)
- **Preload script**: Bridge between main and renderer (secure context)

## Test Setup

### Basic Test Configuration

Create a test file (e.g., `e2e/electron.spec.ts`):

```typescript
import { test, expect, ElectronApplication, Page } from '@playwright/test';
import { _electron as electron } from 'playwright';
import path from 'path';

let electronApp: ElectronApplication;
let window: Page;

test.beforeAll(async () => {
  // Launch Electron app
  electronApp = await electron.launch({
    args: [path.join(__dirname, '../apps/desktop/dist/main/index.js')],
    // Or if using electron-builder output:
    // executablePath: path.join(__dirname, '../apps/desktop/dist/mac/YourApp.app/Contents/MacOS/YourApp'),
  });

  // Wait for first window
  window = await electronApp.firstWindow();
  
  // Wait for app to be ready (adjust selector to your app's ready state)
  await window.waitForSelector('[data-testid="app-ready"]', { timeout: 30000 });
});

test.afterAll(async () => {
  await electronApp.close();
});

test('app window opens', async () => {
  const title = await window.title();
  expect(title).toBe('Your App Name');
});
```

### Launch Options (Choose Based on `launchTarget`)

**When `launchTarget: "dev"` (or not set):**
```typescript
// Development mode (from source)
electronApp = await electron.launch({
  args: ['./apps/desktop/src/main/index.ts'],
  env: {
    ...process.env,
    NODE_ENV: 'test',
  },
});
```

**When `launchTarget: "installed-app"` (read `executablePath` from project.json):**
```typescript
import os from 'os';

// Read executablePath from project.json → apps[].testing.executablePath
// The paths are platform-specific — resolve for current OS
function getAppPath(executablePaths: Record<string, string>): string {
  const key = process.platform === 'darwin' ? 'darwin' : process.platform === 'win32' ? 'win32' : 'linux';
  const p = executablePaths[key];
  if (!p) throw new Error(`No executablePath for platform: ${key}`);
  return p.replace(/^~/, os.homedir());
}

// Production mode — launch the installed binary
electronApp = await electron.launch({
  executablePath: getAppPath(executablePaths),
});
```

> ⛔ **NEVER mix these patterns.** If `launchTarget: "installed-app"`, you MUST use `executablePath`. Using `args` launches from dev source and tests a completely different build.

## Common Test Patterns

### Testing the Renderer Process

The renderer is just a browser window — use standard Playwright patterns:

```typescript
test('can interact with UI', async () => {
  await window.click('[data-testid="new-project-button"]');
  await window.fill('[data-testid="project-name-input"]', 'Test Project');
  await window.click('[data-testid="create-button"]');
  
  await expect(window.locator('[data-testid="project-list"]')).toContainText('Test Project');
});
```

### Testing Main Process (IPC)

Use `electronApp.evaluate()` to run code in the main process:

```typescript
test('main process returns correct app version', async () => {
  const version = await electronApp.evaluate(async ({ app }) => {
    return app.getVersion();
  });
  
  expect(version).toMatch(/^\d+\.\d+\.\d+$/);
});

test('can access electron APIs', async () => {
  const appPath = await electronApp.evaluate(async ({ app }) => {
    return app.getAppPath();
  });
  
  expect(appPath).toContain('desktop');
});
```

### Testing IPC Communication

```typescript
test('renderer can call main process via IPC', async () => {
  // Trigger IPC call from renderer
  await window.click('[data-testid="fetch-system-info"]');
  
  // Wait for response to be displayed
  await expect(window.locator('[data-testid="system-info"]')).not.toBeEmpty();
});

// Or test IPC directly
test('IPC handler responds correctly', async () => {
  const result = await electronApp.evaluate(async ({ ipcMain }) => {
    // This runs in main process
    return new Promise((resolve) => {
      // Simulate IPC call
      ipcMain.emit('get-system-info', { sender: { send: resolve } });
    });
  });
  
  expect(result).toHaveProperty('platform');
});
```

### Testing Native Dialogs

Native dialogs (file picker, message box) need special handling:

```typescript
test('can open file dialog', async () => {
  // Mock the dialog before triggering
  await electronApp.evaluate(async ({ dialog }) => {
    dialog.showOpenDialog = async () => ({
      canceled: false,
      filePaths: ['/mock/path/to/file.txt'],
    });
  });
  
  // Trigger the dialog
  await window.click('[data-testid="open-file-button"]');
  
  // Verify the file was "opened"
  await expect(window.locator('[data-testid="file-path"]')).toHaveText('/mock/path/to/file.txt');
});
```

### Testing Window Management

```typescript
test('can open new window', async () => {
  const windowCount = await electronApp.windows().length;
  
  await window.click('[data-testid="new-window-button"]');
  
  // Wait for new window
  await expect(async () => {
    expect(electronApp.windows().length).toBe(windowCount + 1);
  }).toPass({ timeout: 5000 });
});

test('window has correct dimensions', async () => {
  const bounds = await electronApp.evaluate(async ({ BrowserWindow }) => {
    const win = BrowserWindow.getFocusedWindow();
    return win?.getBounds();
  });
  
  expect(bounds?.width).toBeGreaterThanOrEqual(800);
  expect(bounds?.height).toBeGreaterThanOrEqual(600);
});
```

## Common Gotchas

### 1. App Lifecycle

Electron apps take time to initialize. Always wait for a ready indicator:

```typescript
// BAD: Race condition
const window = await electronApp.firstWindow();
await window.click('button'); // App might not be ready!

// GOOD: Wait for ready state
const window = await electronApp.firstWindow();
await window.waitForSelector('[data-ready="true"]', { timeout: 30000 });
await window.click('button');
```

### 2. Multiple Windows

Electron apps can have multiple windows. Track them properly:

```typescript
test.beforeEach(async () => {
  // Get the main window (first window that's not a splash screen)
  const windows = electronApp.windows();
  window = windows.find(w => !w.url().includes('splash')) || windows[0];
});
```

### 3. Preload Script Context

Code in `evaluate()` runs in main process, not renderer:

```typescript
// This runs in MAIN process
await electronApp.evaluate(({ app }) => app.quit());

// This runs in RENDERER process  
await window.evaluate(() => document.title);
```

### 4. File System Paths

Use cross-platform paths:

```typescript
import path from 'path';

const appPath = path.join(__dirname, '../apps/desktop/dist/main/index.js');
// NOT: '../apps/desktop/dist/main/index.js' (breaks on Windows)
```

### 5. DevTools

DevTools can interfere with tests. Disable in test mode:

```typescript
// In main process
if (process.env.NODE_ENV === 'test') {
  win.webContents.closeDevTools();
}
```

### 6. Single-Instance Lock (CRITICAL)

Electron apps are single-instance by default. If the app is already running, `electron.launch()` will fail or behave unexpectedly.

**Trigger:** Before calling `electron.launch()` in test setup.

**Verification:** Check that no existing app processes are running before launch.

**Failure behavior:** If existing instances are not killed, tests will fail with "app already running" errors or hang indefinitely.

**Always kill existing instances before launching:**

```typescript
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * Kill any existing instances of the app before launching.
 * Required because Electron apps are single-instance by default.
 */
async function killExistingInstances(appName: string): Promise<void> {
  try {
    if (process.platform === 'darwin') {
      // macOS: Use pkill with app name
      await execAsync(`pkill -f "${appName}"`);
    } else if (process.platform === 'win32') {
      // Windows: Use taskkill
      await execAsync(`taskkill /F /IM "${appName}.exe" /T`);
    } else {
      // Linux: Use pkill
      await execAsync(`pkill -f "${appName}"`);
    }
    // Wait for processes to fully exit
    await new Promise(resolve => setTimeout(resolve, 1000));
  } catch {
    // Ignore errors — process may not be running
  }
}

// Usage in test setup
test.beforeAll(async () => {
  await killExistingInstances('YourApp');
  
  electronApp = await electron.launch({
    executablePath: '/Applications/YourApp.app/Contents/MacOS/YourApp',
  });
});
```

**For installed app testing**, this is especially important because:
- The user may have the app open while running tests
- Previous test runs may have left zombie processes
- CI environments may have stale processes from failed runs

**Alternative: Disable single-instance lock in test mode**

If you control the app's source, you can disable single-instance in test mode:

```typescript
// In main process (main.ts)
if (process.env.NODE_ENV !== 'test') {
  const gotTheLock = app.requestSingleInstanceLock();
  if (!gotTheLock) {
    app.quit();
  }
}
```

This allows multiple test instances but requires code changes to the app.

## Playwright Config for Electron

Add to `playwright.config.ts`:

```typescript
import { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
  testDir: './e2e',
  testMatch: '**/electron.spec.ts',
  timeout: 60000, // Electron apps take longer to start
  retries: 1,
  workers: 1, // Run serially — Electron tests can't parallelize well
  use: {
    trace: 'on-first-retry',
    video: 'on-first-retry',
  },
};

export default config;
```

## Running Tests

```bash
# Run Electron tests
npx playwright test e2e/electron.spec.ts

# With headed mode (see the app)
npx playwright test e2e/electron.spec.ts --headed

# Debug mode
npx playwright test e2e/electron.spec.ts --debug
```

## CI/CD Considerations

Electron tests need a display. On Linux CI:

```yaml
# GitHub Actions
- name: Run Electron tests
  uses: coactions/setup-xvfb@v1
  with:
    run: npm run test:e2e:electron
```

Or use `xvfb-run`:

```bash
xvfb-run --auto-servernum npm run test:e2e:electron
```

## Detection Fallback

If Electron is not declared in `project.json`, detect via:

```typescript
// Check package.json for electron dependency
const pkgJson = JSON.parse(fs.readFileSync('apps/desktop/package.json', 'utf-8'));
const hasElectron = 'electron' in (pkgJson.devDependencies || {}) 
                 || 'electron' in (pkgJson.dependencies || {});
```

## Related Skills

- `ui-tester-playwright` — General Playwright patterns (applies to renderer testing)
- `ui-test-ux-quality` — Quality-beyond-correctness patterns (visual stability, etc.)
