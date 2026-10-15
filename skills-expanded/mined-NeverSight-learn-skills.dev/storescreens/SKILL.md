---
name: storescreens
description: "Set up and run storescreens-cli to automate App Store screenshot capture for iOS apps. Also supports targeted screenshots for quick visual checks during development. Use this skill when the user wants to install storescreens-cli, configure screenshot automation for an Xcode project, add UI tests that capture screenshots, write or update ScreenshotTests.swift, run storescreens capture, take a quick screenshot of the simulator, or troubleshoot screenshot automation. Triggers for requests like 'set up App Store screenshots', 'automate screenshots with storescreens', 'add screenshot UI tests', 'capture screenshots for App Store Connect', 'configure storescreens', 'take a screenshot of the simulator', or 'show me what the app looks like'."
---

# storescreens

storescreens-cli runs XCUITest-based UI tests across simulators, extracts named `XCTAttachment` screenshots from the `.xcresult` bundle, and organizes them by device size.

Follow the steps below in order. Each step checks state before acting - skip steps that are already complete.

---

## Step 1: Check / Install storescreens-cli

Run:

```bash
storescreens --help 2>&1
```

Print the full output - it shows the available subcommands and options so the user knows what's available. If the command is not found, install it:

```bash
brew tap ciscoriordan/tap && brew install storescreens
# or
curl -fsSL https://raw.githubusercontent.com/ciscoriordan/storescreens-cli/main/install.sh | sh
```

---

## Step 1b: MCP Server Setup (REQUIRED - do this before anything else)

**The storescreens MCP server is the preferred way to run captures.** It gives you structured tools (`capture`, `get_capture_status`, `list_screenshots`, `get_screenshot`, etc.) instead of parsing CLI output in Bash. **Always set this up.**

**Check if already connected:** Look at your available MCP tools. If you see `capture`, `get_capture_status`, `list_screenshots`, etc. from a `storescreens` MCP server, it's already working - skip to Step 2.

**If MCP is NOT connected, you MUST set it up now:**

1. Check if `.mcp.json` exists in the project root. If it does, read it.

2. **If `.mcp.json` doesn't exist**, create it:

```json
{
  "mcpServers": {
    "storescreens": {
      "command": "storescreens-mcp",
      "args": []
    }
  }
}
```

3. **If `.mcp.json` already exists** but doesn't have a `storescreens` entry, add the `storescreens` server to the existing `mcpServers` object. Do not overwrite other MCP servers.

4. **After creating or updating `.mcp.json`, STOP and tell the user:**

> **Action required: Please exit and relaunch Claude Code from this project directory.**
>
> I just created/updated `.mcp.json` to add the storescreens MCP server. Claude Code only reads project-level `.mcp.json` files on startup - running `/mcp` inside the current session won't pick it up.
>
> After relaunching, run `/storescreens` again and I'll continue from where we left off.

**Do not continue with further steps until MCP is confirmed working.** The MCP server provides `capture`, `get_capture_status`, `check`, `list_screenshots`, `get_screenshot`, `take_screenshot`, `read_config`, `write_config`, and other tools that make the entire workflow dramatically better. Without it, you're stuck parsing raw xcodebuild output in Bash.

---

## Step 2: Detect project

Find the `.xcworkspace` or `.xcodeproj` in the working directory. Identify the scheme name (usually matches the app name). You'll need both for `storescreens.yml` and the `xcodebuild` verify command later.

---

## Step 3: Check for existing `storescreens.yml`

**If `storescreens.yml` already exists, skip `storescreens init` and proceed directly to Step 4.** Do not re-run init or ask config questions unless the user explicitly asks to change devices, locales, or appearances.

Only run `storescreens init` when:
- `storescreens.yml` does not exist yet (fresh project), or
- the user explicitly asks to reconfigure or reinitialise

When you do run init:

```bash
storescreens init
```

Print the full output. If `.mcp.json` was created or updated, tell the user: **exit and relaunch Claude Code from this project directory** to pick up the new MCP config. Running `/mcp` inside the current session is not enough - project-level `.mcp.json` files are only read on startup.

After running `storescreens init`, read `storescreens.yml` and review the config with the user. Show the current values and ask:

1. **Devices** - Are these the right simulators? (Show the current list)
2. **Appearances** - Currently set to `[current value]`. Light only, or both light and dark?
3. **Locales** - Currently `[current value or "not set"]`. Do you need screenshots in multiple languages?

Make any requested changes by editing `storescreens.yml` directly, then continue to Step 4.

If `storescreens.yml` does not exist yet (fresh project), ask the user these questions before running `storescreens init`:

1. **iPhone devices** - Present these options and ask the user to choose:

   - **6.9" only (recommended)** - `iPhone 17 Pro Max`. App Store Connect auto-fills the 6.5" slot from 6.9" screenshots, so this single device covers both. This is all most apps need.
   - **6.9" + 6.5"** - Add `iPhone 11 Pro Max` or `iPhone Xs Max` if they want *distinct* screenshots in the 6.5" slot rather than the auto-scaled 6.9" ones. Note: no current simulator produces 6.5" (1242×2688) - only these older simulators do.
   - **More sizes** - App Store Connect also has slots for 6.3", 6.1", 5.5", 4.7", 4", and 3.5". Ask if they want any of these. Corresponding simulators: `iPhone 17 Pro` (6.3"), `iPhone 16` (6.1"), `iPhone 8 Plus` (5.5"), `iPhone SE (3rd generation)` (4.7"). Sizes smaller than 4.7" are very old and rarely needed.
   - **Skip iPhone for now** - valid choice; they can add iPhone later.

   Note: App Store Connect has **no 6.7" slot** - do not suggest `iPhone 16 Plus`.

2. **Appearances** - Light mode only, or also dark mode?

Once you have the iPhone answers, write `storescreens.yml` with the iPhone devices. See `references/config-reference.md` for the full schema. The `test_target` and `test_class` should be `<AppName>UITests` and `ScreenshotTests` - you'll confirm these in Step 4.

**IMPORTANT: Always include `derived_data_path` in the config.** Without it, every capture run recompiles everything from scratch (including all SPM packages), which can add 3-5+ minutes to each run. Set it to `~/.storescreens-cache/<AppName>`:

```yaml
derived_data_path: ~/.storescreens-cache/<AppName>
```

If `storescreens.yml` already exists but is missing `derived_data_path`, add it now.

---

## Step 3b: iPad devices (separate question)

Ask the user separately whether they want iPad screenshots. Don't push it - it's fine to skip and add later.

App Store Connect iPad slots:
- **13"** (required when iPad is supported) → `iPad Pro 13-inch (M5)` - **recommend this as the starting point**
- **11"** → `iPad Pro 11-inch (M5)`
- **12.9"**, **10.5"**, **9.7"** - legacy slots requiring older simulator runtimes; rarely needed

If they want iPad, add the chosen simulators to `devices` in `storescreens.yml`. Also note: if their app has iPad support disabled in Xcode (Supported Destinations), they'll need to re-enable it there first (General tab → Supported Destinations → add iPad).

---

## Step 4: Check for a UI test target

Look for an existing UI test target by searching for `*UITests` directories or `.swift` files containing `XCTestCase` in a test target folder.

**If a UI test target already exists:**

Check whether `ScreenshotTests.swift` exists inside it. If it does, skip to Step 6. If it doesn't, proceed to Step 5 to write the test file.

**If no UI test target exists:**

Tell the user they need to create one manually in Xcode (this cannot be done from code):

> Please add a UI test target in Xcode:
> 1. File → New → Target → UI Testing Bundle
> 2. Name it `<AppName>UITests`
> 3. Set "Target to be Tested" to your app
> 4. Click Finish
>
> Xcode will generate a placeholder `<AppName>UITestsLaunchTests.swift` - delete that file.
> Then come back and I'll write `ScreenshotTests.swift` for you.

Wait for the user to confirm before continuing.

---

## Step 4b: Preflight check (run by the setup wizard)

The `storescreens setup` wizard automatically runs `storescreens check` before generating the test file. If it finds issues:

- **Errors** (e.g. unguarded CloudKit, missing `.toolbarVisibility` iPad guard): the wizard asks `Continue setup anyway? [y/N]`. Default is **No** - fix errors first, then re-run `storescreens setup`.
- **Warnings** (e.g. missing accessibility identifiers, unguarded review prompts): the wizard asks `Continue setup with warnings? [Y/n]`. Default is **Yes** - warnings are informational and don't block setup, but should be addressed before capture.

The `missing-accessibility-identifier` warning fires when a UI test file references an identifier (e.g. `waitForElement(id: "saveButton")` or `app.buttons["saveButton"]`) that has no corresponding `.accessibilityIdentifier("saveButton")` in the app source. Help the user add the missing identifier to their view before continuing.

The `localized-nav-button` warning fires when a test uses `navigationBars.buttons["Back"]` (or any title-cased label) to find a navigation bar button. Localized titles change per locale - "Back" becomes "Atrás" in Spanish, "Zurück" in German, etc. - causing test failures when running multi-locale screenshot capture. Fix: use `app.navigationBars.buttons.element(boundBy: 0)` for the system back button (it is always the first/leftmost button), or add an `.accessibilityIdentifier` to a custom button and query by that instead.

**When reporting findings, handle each warning/error category separately** - present one category, ask if the user wants to fix it now, fix it if yes, then move to the next category. Do not bundle multiple categories into a single question.

---

## Step 5: Check / configure screenshot mode in the app

Before writing the test file, check whether the app already handles a screenshot mode launch argument (search for `--uitesting` or `--uitesting` in the Swift source).

If it does not, explain what needs to be added and help the user add it to the appropriate place (app `init`, `@main` struct, or root view `.task`):

```swift
if ProcessInfo.processInfo.arguments.contains("--uitesting") {
    // Force premium/subscriber access - skip StoreKit verification
    // subscriptionService.isSubscribed = true

    // Disable animations for fast, deterministic captures
    UIView.setAnimationsEnabled(false)

    // Reset persisted UI state if needed
    // UserDefaults.standard.removeObject(forKey: "onboardingDone")
}
```

Also guard any `checkEntitlements()` or StoreKit calls so they don't run in screenshot mode. **Wrap the specific call - do not add a `guard...return` at the top of the function.** An early return silently skips everything below it, including state setup like `isInitialized = true`, which can leave the app in a broken state during tests.

```swift
// Good - wraps just the entitlement call:
if !ProcessInfo.processInfo.arguments.contains("--uitesting") {
    checkEntitlements()
}

// Bad - skips ALL code below this line, including isInitialized = true:
// guard !ProcessInfo.processInfo.arguments.contains("--uitesting") else { return }
```

Confirm with the user which (if any) subscription/entitlement service needs to be bypassed.

---

## Step 6: Write `ScreenshotTests.swift`

Ask the user to describe the screens they want to capture and the navigation flow between them. Use their description to write a tailored test file.

Key requirements for the test file:

- `app.launchArguments = ["--uitesting"]`
- Wait for the app to fully load before the first screenshot: `XCTAssertTrue(element.waitForExistence(timeout: 20))`
- Name screenshots with a numeric prefix: `"01_Home"`, `"02_Detail"`, etc.
- Use **accessibility identifiers** for all element lookups - ask the user what identifiers exist or help them add them. Avoid fragile text/position-based queries.
- Always `waitForExistence(timeout:)` before tapping any element
- Clean up any state changed during the test (e.g. delete test permits/data added during the flow) at the end

Use `assets/ScreenshotTests.swift.template` as a starting point. Place the file inside the `<AppName>UITests/` folder.

After writing the file, tell the user:

> Add `ScreenshotTests.swift` to the Xcode target:
> Right-click the `<AppName>UITests` group → Add Files to "[project]" → select `ScreenshotTests.swift` → confirm the target membership checkbox is checked.

---

## Step 7: Verify the build

Pipe xcodebuild output to a log file so you can inspect errors:

```bash
xcodebuild build-for-testing \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro' \
  2>&1 | tee build.log
```

If this fails, check `build.log` for the full error output and fix before running capture.

---

## Step 8: Capture

### Targeted screenshot (quick visual check)

When you need to verify a UI change visually, **do NOT run the full screenshot suite.** Use the `take_screenshot` MCP tool instead. It captures the current simulator screen in under a second - no build, no tests.

**When to use `take_screenshot`:**
- You edited a SwiftUI view and want to see the result
- You want to confirm a layout change before committing
- The simulator is already running your app

**When to use full `capture` instead:**
- You need final App Store screenshots
- You need multiple devices or locale variants
- The app is not running and you need it built from source

**Using the MCP tool:**

If the simulator is already running your app:

```
take_screenshot(simulator: "iPhone 17 Pro")
```

The image renders inline immediately. If no simulator name is given, it uses the first booted simulator.

If the simulator is not booted:

```
take_screenshot(simulator: "iPhone 17 Pro", boot: true)
```

**Using the CLI (if MCP is not available):**

```bash
storescreens screenshot --simulator "iPhone 17 Pro" --output screenshot.png
# Boot variant:
storescreens screenshot --simulator "iPhone 17 Pro" --boot --output screenshot.png
```

**If you need to navigate to a specific screen** that requires UI test interaction, the old approach still works: temporarily disable the main test, write a focused `testQuickVisual()` method, run `capture`, then clean up. But for a simple "what does the current screen look like" check, `take_screenshot` is much faster.

### Choosing the right screenshot tool

If Xcode 26.3+ is running and its MCP server is available (you'll have tools like `RenderPreview`, `BuildProject`, etc.), you have three options for visual checks:

| Tool | What it captures | When to use |
|------|-----------------|-------------|
| Xcode `RenderPreview` | A single SwiftUI `#Preview` | Checking an individual view's layout. No simulator needed. |
| storescreens `take_screenshot` | The full running app in a simulator | Checking the app with real data, navigation state, and system chrome. |
| storescreens `capture` | Full App Store screenshots across devices | Final screenshots for App Store Connect. Multiple devices, locales, appearances. |

Use `RenderPreview` when you want to check a single view in isolation (it renders SwiftUI previews, not the running app). Use `take_screenshot` when you need to see the actual app running with real state. Use `capture` for the final App Store screenshot suite.

### Full capture

**Use the MCP `capture` tool.** If the storescreens MCP server is not connected, **STOP - go back to Step 1b and set it up.** Do not proceed with Bash capture unless the user explicitly says they don't want MCP. The MCP tools provide structured progress, inline screenshot previews, and eliminate the need to parse raw xcodebuild output.

Check whether the `storescreens` MCP server is connected (you'll have tools like `capture`, `get_capture_status`, `list_screenshots` available). If it is, call the `capture` tool. Only fall back to Bash if the user explicitly declines MCP setup.

**If using MCP:**

1. Call the `capture` tool - it returns a `taskId` immediately and starts capture in the background.
2. **Poll interval: follow what `get_capture_status` tells you.** Each response ends with either "Wait 30 seconds" (build phase) or "Wait 5 seconds" (test phase). Always use the interval the server specifies - never switch on your own based on which devices have finished or what you see in the output.
   ```bash
   sleep 30   # when server says "Wait 30 seconds"
   sleep 5    # when server says "Wait 5 seconds"
   ```
   Then call `get_capture_status(task_id: "<taskId>")`. Repeat until `status: completed` or `status: failed`. Never call `get_capture_status` back-to-back without the sleep in between.
3. **What to show the user while polling:**
   - After each poll, output any **new** `✓ [Device] [Slot] screenshot_name` lines that weren't in the previous poll response. This is the primary progress signal - output them as-is so the user can see screenshots being captured in real time.
   - Also surface these meaningful transitions when they first appear: `Testing started`, `** TEST SUCCEEDED **`, `** BUILD FAILED **`, locale changes (`● Locale: ...`), and device completion lines (`✓ DeviceName: N screenshots`).
   - Do not repeat lines that were already shown in a previous poll. Track what you've output and only emit new lines.
   - **"last activity Xs ago" does NOT mean the run is stuck.** xcodebuild writes build output to stdout (which the MCP tracks), but once the build phase completes and tests start running, xcodebuild writes results directly to the `.xcresult` bundle on disk - **no stdout output is produced during test execution**. A "last activity 300s ago" status is normal and expected during the test phase. Keep polling - do not report a stall to the user unless the run exceeds 20 minutes total. **If the run HAS exceeded 20 minutes and all device tests have already passed** (you saw `Test case '...' passed` for every device in the status output), the MCP server is stuck in a post-test deadlock. Tell the user: "The capture process is stuck. Please run `pkill -f storescreens-mcp` in a terminal, then exit and relaunch Claude Code so the MCP server restarts, then re-run capture."
   - **Detect the stuck-buffer problem.** If the output is identical across any 2 consecutive polls **and** `last activity` has not advanced, immediately call `list_screenshots` AND check the file timestamps (via `ls -la` on the output directory) to verify the screenshots are from the *current* run - not a previous one. Compare the file modification times against when the current capture started. Only report screenshots as complete if they are newer than the capture start time. If timestamps are stale, the run is still in progress - keep polling.
   - **"0 screenshots" for a completed device is a red flag.** If a poll response shows a device reporting "Tests completed" or "0 screenshots", treat this as a likely failure and immediately inspect the per-device log. Do NOT continue polling silently. Read the log:
     ```bash
     cat <output_dir>/logs/test-<UDID-prefix>.log | grep -E "error:|FAILED|fatalError|Could not resolve"
     ```
     If errors are found, report them to the user immediately.
   - **Device failures in logs during polling:** `get_capture_status` will include a "Device failures detected in logs" section if it finds error patterns in any per-device log file. When this appears, immediately report the failure to the user - do not wait for the run to complete. If some devices have failed and others are still running, tell the user: "Device X failed (see error below). Other devices are still running. Do you want to abort or wait for them to finish?" Then wait for the user's answer before taking action.
4. On completion, report results: how many screenshots per device. Output a clickable preview link using the absolute path: `file://<absolute-path-to-project>/<output_dir>/preview.html`. On failure, read the log.

**If using Bash (MCP unavailable):**

```bash
storescreens capture
```

The CLI streams full xcodebuild output to stdout (auto-detected in non-TTY mode). The command output will be large (compile steps + test output).

**IMPORTANT - after the command finishes, ALWAYS print these two messages as your own text output (NOT inside a bash block):**

1. Tell the user they can expand the output block above to see the full xcodebuild build and test log.
2. Show the tail command for the log files using the absolute path to the project's output dir:

```
To follow logs in real time on future runs, open another terminal:
  tail -f <absolute-path-to-project>/<output_dir>/logs/test-*.log
```

Then report the results: how many screenshots captured, whether tests passed/failed. Output a clickable preview link using the absolute path: `file://<absolute-path-to-project>/<output_dir>/preview.html`.

If tests failed, read the log file to diagnose:

```bash
cat <absolute-path-to-project>/<output_dir>/logs/test-*.log
```

Output lands in `storescreens-output/` with device name as a filename prefix. Light and dark mode get separate directories:

```
storescreens-output/
├── preview.html           ← open: file://<absolute-path-to-project>/<output_dir>/preview.html
├── manifest.json
├── logs/
│   └── test-<device>.log  ← one per device
├── light/
│   ├── iPhone_6.9_01_Home.png
│   ├── iPhone_6.9_02_Detail.png
│   ├── iPhone_6.3_01_Home.png
│   └── ...
└── dark/
    ├── iPhone_6.9_01_Home.png
    ├── iPhone_6.9_02_Detail.png
    └── ...
```

---

## Step 9: Upload to storescreens.app (optional, opt-in)

The CLI can upload screenshots to [storescreens.app](https://storescreens.app) for visual editing (device frames, backgrounds, marketing text). This is **disabled by default**.

To enable the upload prompt, add `upload: true` to `storescreens.yml`:

```yaml
upload: true
```

When enabled, the CLI prompts after each capture:

> Would you like to design App Store Connect screenshots at storescreens.app? (y/n)

To suppress the prompt on a single run (e.g. in CI), pass `--no-upload`:

```bash
storescreens capture --verbose --no-upload
```

---

## MCP Server (storescreens-mcp)

The `storescreens-mcp` binary is a Model Context Protocol server that exposes storescreens functionality as structured tools - eliminating the need for Bash calls and providing per-screenshot progress inline.

### Setup

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "storescreens": {
      "command": "storescreens-mcp",
      "args": []
    }
  }
}
```

Or with a full path if not on `$PATH`:

```json
{
  "mcpServers": {
    "storescreens": {
      "command": "/usr/local/bin/storescreens-mcp",
      "args": []
    }
  }
}
```

### Available Tools

| Tool | Description |
|------|-------------|
| `capture` | Start screenshot capture in background; returns `taskId` immediately |
| `get_capture_status` | Poll progress for a running capture; returns live events + status |
| `get_capture_result` | Fetch full manifest once capture is complete |
| `check` | Run preflight scan; returns `[{rule, severity, file, line, message}]` |
| `list_simulators` | List available simulators grouped by App Store slot |
| `list_screenshots` | List screenshots from the last capture (reads `manifest.json`) |
| `get_screenshot` | Load a PNG as base64 (Claude renders it inline) |
| `take_screenshot` | Capture current simulator screen; returns image inline. No build required. |
| `read_config` | Read and parse `storescreens.yml` |
| `write_config` | Write `storescreens.yml` |

### Progressive Disclosure Pattern

`capture` returns a compact summary to avoid token bloat:

```
● Building for testing…
  ✓ iPhone 17 Pro Max [iPhone 6.9"] 01_Home → storescreens-output/light/iPhone_6.9_01_Home.png
  ✓ iPhone 17 Pro Max [iPhone 6.9"] 02_Detail → storescreens-output/light/iPhone_6.9_02_Detail.png
  ● Device complete: iPhone 17 Pro Max - 2 screenshots

captureId: a1b2c3d4
```

Call `get_capture_result` with the `captureId` to get the full manifest including all device sizes, paths, and metadata.

---

## Debugging

When something goes wrong, the xcodebuild output is already in the Bash result (use Ctrl+O to see full output). You can also check the log files directly:

1. **`logs/test-*.log`** - per-device xcodebuild output, element lookup failures, assertion errors
2. **`logs/test-debug-*.log`** - test debug prints (from the named pipe)

If a capture run fails or screenshots are missing, always read the relevant log file before changing code - the root cause is almost always visible in the xcodebuild output.

---

## Common Issues

- **"Element not found"** - use `.accessibilityIdentifier` instead of button titles; always `waitForExistence(timeout:)`. Check `logs/test-*.log` for the full element tree dump.
- **"Test not discovered"** - the `.swift` file isn't in the Xcode target; use "Add Files to" and check target membership
- **StoreKit / entitlement checks override screenshot mode flag** - guard every entitlement check, not just the setter
- **iPad preflight errors** - wrap `.toolbarVisibility(.hidden, for: .tabBar)` with a `UIDevice` idiom check, or pass `--skip-check` for iPhone-only projects
- **Build failures** - check `logs/build-for-testing.log` for the full compiler output
- **"0 screenshots via filesystem" but tests passed** - the breadcrumb file `~/.storescreens-cache-dir` was missing or stale. This file tells the test's `takeScreenshot` helper where to write PNGs. Run `storescreens capture` again (v1.2.1+ writes the breadcrumb correctly). If the file is missing, create it manually: `echo "$PWD/.storescreens-cache" > ~/.storescreens-cache-dir`
- **Wrong/deleted test methods ran (stale DerivedData)** - when using persistent `derived_data_path`, the compiled test binary can become stale if test source files are edited. v1.3.0+ auto-detects this and cleans build products before building. If you see unexpected test methods running, manually clean: `rm -rf ~/.storescreens-cache/<MyApp>/Build/Products`. The `storescreens check` command also warns about stale DerivedData.

## Persistent DerivedData (STRONGLY RECOMMENDED)

**Always configure this.** By default storescreens creates a fresh temp DerivedData directory per run and deletes it afterwards, so every run recompiles all SPM packages from scratch - adding 3-5+ minutes of unnecessary build time. With a persistent cache, incremental builds only recompile changed files.

Add `derived_data_path` to `storescreens.yml`:

```yaml
derived_data_path: ~/.storescreens-cache/<MyApp>
```

Or set it via the MCP `write_config` tool:

```
write_config(derived_data_path: "~/.storescreens-cache/MyApp")
```

You can also pass it as a one-off override on the CLI:

```bash
storescreens capture --derived-data-path ~/.storescreens-cache/MyApp
```

Or via the MCP `capture` tool:

```
capture(derived_data_path: "~/.storescreens-cache/MyApp")
```

**Notes:**
- The directory is created automatically on first use.
- Use a project-specific subdirectory (e.g. `~/.storescreens-cache/MyApp`) if you have multiple projects.
- To force a clean build, delete the directory or don't set this option.
- **Staleness detection (v1.3.0+):** Before each capture, storescreens compares test source file modification times with the compiled test runner binary. If source is newer, it automatically cleans the build products and rebuilds. This prevents stale binaries from running wrong/deleted test methods.

---

## Warmup Run (for apps that need a full launch cycle before capturing)

By default, storescreens runs the test suite **once per device**. xcodebuild parallel test execution is disabled (`-parallel-testing-enabled NO`) to prevent unintended duplicate runs from simulator clones.

Some apps need a full launch cycle before screenshots look correct - for example, apps that seed a CloudKit database, perform On-Demand Resources downloads, or run migrations on first launch. For these, enable the warmup run:

```yaml
warmup_run: true
```

When `warmup_run: true`, storescreens runs the test suite **twice** per device. The first run is a warmup (screenshots are discarded), and the second run captures the real screenshots.

Most apps do **not** need this - leave it unset (default: off).

---

## References

- Full config schema: `references/config-reference.md`
- ScreenshotTests starter template: `../storescreens-cli/Sources/storescreens-cli/Resources/ScreenshotTests.swift.template`
