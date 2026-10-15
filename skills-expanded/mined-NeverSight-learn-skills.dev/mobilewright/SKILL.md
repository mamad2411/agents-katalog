---
name: mobilewright
description: Mobile device automation, testing, and UI verification for iOS and Android. Use before writing mobilewright tests, automation scripts, or verifying mobile UI implementations.
---

# Mobilewright Skill

Mobile device automation, testing, and development verification using [mobilewright](https://github.com/mobile-next/mobilewright) — a Playwright-inspired framework for iOS and Android.

Use this skill when:
- Writing mobile app tests (E2E, regression, smoke)
- Automating mobile device interactions (scraping, screenshots, repetitive tasks)
- Verifying UI implementation during mobile app development — take screenshots, dump the view tree, and confirm the code you wrote produces the expected result

## First Steps

Before writing any code, gather context:

1. **What are you doing?** Ask the user: testing, automation script, or verifying a UI you just built?
2. **What platform?** Ask the user: iOS, Android, or both?
3. **TypeScript or JavaScript?** Ask the user. Both are supported.
4. **Find the bundle ID automatically.** Don't ask — look for it:
   - iOS: search for `PRODUCT_BUNDLE_IDENTIFIER` in `*.pbxproj` files, or `bundleIdentifier` in Expo's `app.json` / `app.config.js`
   - Android: search for `applicationId` in `build.gradle` or `build.gradle.kts`, or `package` in `AndroidManifest.xml`
   - React Native / Expo: check `app.json` for `expo.ios.bundleIdentifier` and `expo.android.package`
   - If none found, check if there's already a `mobilewright.config.ts` with a `bundleId` set
   - Only ask the user if you cannot find it automatically
5. **Is there an existing `mobilewright.config.ts`?** If not, create one.

## Project Setup

Scaffold a new project:

```bash
npx mobilewright init
```

This creates `mobilewright.config.ts` and `example.test.ts`. Verify the environment:

```bash
npx mobilewright doctor
```

### CLI Commands

```bash
npx mobilewright init                              # scaffold config + example test
npx mobilewright doctor                            # verify environment setup
npx mobilewright devices                           # list connected devices/simulators
npx mobilewright test                              # run tests
npx mobilewright screenshot                        # take a screenshot of a connected device
npx mobilewright screenshot -o login.png           # save to specific file
npx mobilewright screenshot -d <device-id>         # target a specific device
```

### Configuration

```typescript
import { defineConfig } from 'mobilewright';

export default defineConfig({
  platform: 'ios',                // 'ios' or 'android'
  bundleId: 'com.example.myapp',  // app bundle ID
  deviceName: 'iPhone 16',        // regex to match device name (optional)
  timeout: 10_000,                // global timeout in ms (optional)
});
```

## UI Inspection — Do This First

**Before writing any locator, always inspect the UI tree.** Do not guess at element names, labels, or types. Use `screen.viewTree()` to get the live accessibility hierarchy, then choose the best locator strategy based on what you see.

```typescript
const tree = await screen.viewTree();
console.log(JSON.stringify(tree, null, 2));
```

This returns the full view hierarchy as JSON. Examine it to find:
- Accessibility identifiers (`testId`)
- Accessibility labels (`label`)
- Element types (`type`)
- Text content (`text` / `value`)
- Placeholder text

Then pick the locator using this priority order:

### Locator Priority (best to worst)

| Priority | Locator | Why |
|----------|---------|-----|
| 1 | `getByTestId('login-btn')` | Most stable. Set by developers, won't change with copy or i18n. |
| 2 | `getByRole('button', { name: 'Sign In' })` | Semantic and cross-platform. Maps to native types on both iOS and Android. |
| 3 | `getByLabel('Sign In')` | Accessibility label. Stable if accessibility is maintained. |
| 4 | `getByPlaceholder('Search...')` | Good for text fields. Only available on Locator, not on Screen. |
| 5 | `getByText('Sign In')` | Fragile. Changes with copy updates, i18n, or minor rewording. |
| 6 | `getByType('Button')` | Platform-specific. Ties your code to iOS or Android element types. |

## Test File Structure

Use `@mobilewright/test` which extends Playwright Test with mobile fixtures.

```typescript
import { test, expect } from '@mobilewright/test';

test.use({ bundleId: 'com.example.myapp', video: 'on' });

test.beforeEach(async ({ device, bundleId }) => {
  // Fresh app state for every test
  await device.terminateApp(bundleId).catch(() => {});
  await device.launchApp(bundleId);
});

test.describe('login flow', () => {
  test('user can sign in with valid credentials', async ({ screen }) => {
    await screen.getByLabel('Email').fill('user@example.com');
    await screen.getByLabel('Password').fill('password123');
    await screen.getByRole('button', { name: 'Sign In' }).tap();

    await expect(screen.getByText('Welcome back')).toBeVisible();
  });
});
```

Run tests:

```bash
npx mobilewright test
npx mobilewright test login.test.ts              # specific file
npx mobilewright test --grep "sign in"           # run a single test by name
npx mobilewright test --reporter list            # line-by-line output, good for CI/agents
npx mobilewright test --reporter json            # machine-readable JSON output
```

### Available Fixtures

| Fixture | Scope | Description |
|---------|-------|-------------|
| `screen` | test | The device screen — use this for all element interactions |
| `device` | worker | Device connection — use for app lifecycle, orientation, URLs |
| `bundleId` | test | The configured bundle ID string |

### Test Options via `test.use()`

```typescript
test.use({
  bundleId: 'com.example.app',    // override app bundle ID
  platform: 'android',            // override platform
  deviceId: '5A5FCFCA-...',       // target specific device
  video: 'on',                    // record video ('on' | 'retain-on-failure')
});
```

## Automation Script Structure

For standalone scripts that don't need a test runner:

```typescript
import { ios, android } from 'mobilewright';

const device = await ios.launch({ bundleId: 'com.example.myapp' });
const { screen } = device;

// Do your work
const tree = await screen.viewTree();
const screenshot = await screen.screenshot();
await screen.getByRole('button', { name: 'Start' }).tap();

// Always close when done
await device.close();
```

### Launch Options

```typescript
// Auto-discover first booted simulator
const device = await ios.launch();

// Launch a specific app
const device = await ios.launch({ bundleId: 'com.example.app' });

// Match device by name (regex)
const device = await ios.launch({ deviceName: 'My.*iPhone' });

// Target exact device
const device = await ios.launch({ deviceId: '5A5FCFCA-...' });

// List available devices
const devices = await ios.devices();
const devices = await android.devices();
```

## Development Verification

When developing a mobile app, use mobilewright to verify your UI implementation:

```typescript
import { ios } from 'mobilewright';

const device = await ios.launch({ bundleId: 'com.example.myapp' });
const { screen } = device;

// Take a screenshot to verify the UI looks correct
const screenshot = await screen.screenshot();

// Dump the view tree to verify elements exist and have correct properties
const tree = await screen.viewTree();

// Verify specific elements are present and have expected content
const title = await screen.getByRole('text', { name: 'Welcome' }).getText();
const isButtonEnabled = await screen.getByTestId('submit-btn').isEnabled();

await device.close();
```

## API Quick Reference

### Screen — Locator Factories

```typescript
screen.getByLabel('Email')                          // accessibility label
screen.getByTestId('login-button')                  // accessibility identifier
screen.getByText('Welcome')                         // exact text match
screen.getByText(/welcome/i)                        // regex match
screen.getByText('welcome', { exact: false })       // substring match
screen.getByType('TextField')                       // native element type
screen.getByRole('button', { name: 'Sign In' })     // semantic role + name
```

### Screen — Direct Actions

```typescript
await screen.screenshot()                            // PNG buffer
await screen.screenshot({ format: 'jpeg', quality: 80 })
await screen.swipe('up')                             // scroll down
await screen.swipe('down', { distance: 300, duration: 500 })
await screen.pressButton('HOME')
await screen.goBack()                                // press BACK (Android only, no-op on iOS)
await screen.viewTree()                              // full view hierarchy as JSON
```

### Locator — Actions

All actions auto-wait for the element to be visible, enabled, and stable.

```typescript
await locator.tap()
await locator.doubleTap()
await locator.longPress({ duration: 1000 })
await locator.fill('hello@example.com')              // tap to focus + type
```

### Locator — Queries

```typescript
await locator.getText()       // visible text / label
await locator.getValue()      // input value
await locator.isVisible()     // boolean
await locator.isEnabled()     // boolean
await locator.isSelected()    // boolean
await locator.isFocused()     // boolean
await locator.isChecked()     // boolean
```

### Locator — Collection

Work with multiple matching elements:

```typescript
await locator.count()         // number of matching elements
await locator.all()           // array of Locator, one per match
locator.first()               // first matching element
locator.last()                // last matching element
locator.nth(2)                // element at index (0-based, negative counts from end)
```

Example — tap the third item in a list:

```typescript
await screen.getByType('Cell').nth(2).tap();
```

Example — verify the number of search results:

```typescript
const count = await screen.getByType('Cell').count();
expect(count).toBe(5);
```

### Locator — Chaining

Scope queries within a parent element's bounds:

```typescript
const row = screen.getByType('Cell');
await row.getByRole('button', { name: 'Delete' }).tap();
await row.getByPlaceholder('Enter name').fill('Arthur');
```

Note: `getByPlaceholder` is only available on Locator (chained), not directly on Screen.

### Locator — Waiting

```typescript
await locator.waitFor({ state: 'visible' })
await locator.waitFor({ state: 'hidden' })
await locator.waitFor({ state: 'enabled' })
await locator.waitFor({ state: 'disabled', timeout: 10_000 })
```

### Assertions

All assertions auto-retry until satisfied or timeout. Use `.not` for negation.

```typescript
await expect(locator).toBeVisible();
await expect(locator).not.toBeVisible();
await expect(locator).toBeEnabled();
await expect(locator).toBeDisabled();
await expect(locator).toHaveText('Welcome back!');
await expect(locator).toHaveText(/welcome/i);
await expect(locator).toContainText('back');
await expect(locator).toHaveValue('user@example.com');
await expect(locator).toBeHidden();
await expect(locator).toBeChecked();
await expect(locator).toBeSelected();
await expect(locator).toBeFocused();
await expect(locator).toBeVisible({ timeout: 10_000 });
```

### Device

```typescript
// App lifecycle
await device.launchApp('com.example.app');
await device.launchApp('com.example.app', { locale: 'fr_FR' });
await device.terminateApp('com.example.app');
await device.installApp('/path/to/app.ipa');
await device.uninstallApp('com.example.app');
const apps = await device.listApps();
const foreground = await device.getForegroundApp();

// Navigation / deep links
await device.goto('myapp://settings');
await device.openUrl('https://example.com');

// Orientation
await device.setOrientation('landscape');
const orientation = await device.getOrientation();

// Recording
await device.startRecording({ output: 'recording.mp4' });
await device.stopRecording();

// Cleanup
await device.close();
```

## Role Mapping

`getByRole` maps semantic roles to platform-specific types:

| Role | iOS | Android |
|------|-----|---------|
| `button` | Button, ImageButton | Button, ImageButton, ReactViewGroup* |
| `textfield` | TextField, SecureTextField, SearchField | EditText, ReactEditText |
| `text` | StaticText | TextView, Text, ReactTextView |
| `image` | Image | ImageView, ReactImageView |
| `switch` | Switch | Switch, Toggle |
| `checkbox` | -- | Checkbox |
| `slider` | Slider | SeekBar |
| `list` | Table, CollectionView, ScrollView | ListView, RecyclerView, ReactScrollView |
| `header` | NavigationBar | Toolbar |
| `link` | Link | Link |

\* ReactViewGroup matches `button` only when `clickable="true"` or `accessible="true"`.

Falls back to direct type matching if no mapping exists.

## Common Patterns

### Fresh App State Per Test

```typescript
test.beforeEach(async ({ device, bundleId }) => {
  await device.terminateApp(bundleId).catch(() => {});
  await device.launchApp(bundleId);
});
```

### Screenshot on Failure (automatic)

The `@mobilewright/test` fixture automatically captures a screenshot when a test fails. For manual screenshots:

```typescript
test.afterEach(async ({ screen }, testInfo) => {
  const screenshot = await screen.screenshot();
  await testInfo.attach('screenshot', { body: screenshot, contentType: 'image/png' });
});
```

### Scrolling to Find Off-Screen Elements

```typescript
await screen.swipe('up');  // scroll down to reveal content below
await expect(screen.getByText('Footer Content')).toBeVisible();
```

### Extracting Helpers for Repeated Flows

```typescript
async function login(screen: any, email: string, password: string) {
  await screen.getByLabel('Email').fill(email);
  await screen.getByLabel('Password').fill(password);
  await screen.getByRole('button', { name: 'Sign In' }).tap();
}

test('logged in user sees dashboard', async ({ screen }) => {
  await login(screen, 'user@test.com', 'pass123');
  await expect(screen.getByText('Dashboard')).toBeVisible();
});
```

## Rules

### Always Do

- **Inspect the UI tree first.** Run `screen.viewTree()` before writing locators. Never guess.
- **Use retry assertions.** `await expect(locator).toBeVisible()` retries automatically. `await locator.isVisible()` does not.
- **Use locators, not coordinates.** Locators are resilient to layout changes.
- **Relaunch the app between tests.** `terminateApp` + `launchApp` ensures clean state.
- **Use `{ exact: false }` for flexible text matching** when exact wording may vary.
- **Extract repeated navigation into helper functions** to keep tests readable.

### Never Do

- **Never use `screen.tap(x, y)` for element interaction.** Raw coordinates break across devices, screen sizes, and OS versions. Always find the element with a locator.
- **Never hardcode timeouts.** Don't `await sleep(2000)` hoping an element appears. Use auto-waiting actions and retry assertions — they handle timing automatically.
- **Never use `waitFor` before an action.** Actions like `tap()` and `fill()` already auto-wait. Writing `await locator.waitFor({ state: 'visible' }); await locator.tap();` is redundant — just `await locator.tap()`.
- **Never use `isVisible()` for test assertions.** It returns a boolean at one instant. Use `expect(locator).toBeVisible()` which retries until the assertion is satisfied.
- **Never screenshot and parse images to find elements.** Use `screen.viewTree()` to inspect the accessibility tree programmatically.
- **Never hardcode platform-specific types when a role exists.** Use `getByRole('button')` instead of `getByType('UIButton')`.
