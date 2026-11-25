---
name: app-screenshots
description: >
  Screenshot every view/screen of an app for marketing, product sites, and documentation.
  Use when asked to "screenshot the app", "capture all views", "get marketing screenshots",
  "screenshot every screen", or "product shots". Works with macOS native apps (screencapture),
  web apps (Puppeteer/Playwright), and Electron apps.
---

# App Screenshots

Systematically capture every view/screen of an application for marketing, product sites, README assets, and documentation.

## Workflow

```
1. Discover all views/screens in the app
2. Build + launch the app (if not already running)
3. Navigate to each view and screenshot it
4. Save named screenshots to output directory
5. Generate a manifest (summary.md)
```

## Step 1: Discover Views

Analyze the project to enumerate all distinct views/screens. Methods by project type:

**Swift/SwiftUI macOS apps**: Grep for `View` structs, `WindowGroup`, `Window`, `Settings`, sheets, popovers, menu bar panels. Check for multiple window types, onboarding flows, settings tabs.

**Web apps**: Check routes (React Router, Next.js pages, Express routes). Each route = one screenshot minimum. Also check for modals, drawers, settings panels.

**Electron apps**: Check `BrowserWindow` creation, route handlers, IPC window openers.

Present the discovered view list to the user for confirmation before proceeding:

```
Found 8 views:
1. Main window (default state)
2. Settings > General
3. Settings > Appearance
4. Settings > Shortcuts
5. Popdown menu
6. Onboarding wizard
7. Empty state
8. Active session state

Proceed? Any views to add/skip?
```

## Step 2: Build + Launch

Build and launch the app if it's not already running. If it is, skip this step.

## Step 3: Capture Each View

Navigate to each view and capture it. **Sequential only** -- one view at a time.

### macOS Native Apps (Swift/SwiftUI)

```bash
# Get window ID for the app
WINDOW_ID=$(osascript -e 'tell application "System Events" to get id of first window of (first process whose name is "AppName")')

# Screenshot specific window (no shadow, no sound)
screencapture -l $WINDOW_ID -o -x "$OUTPUT_DIR/view-name.png"
```

For views that require navigation (settings tabs, popovers):
- Use AppleScript or accessibility APIs to click/navigate
- Or instruct the user: "Please open Settings > Appearance, then press Enter"
- Wait, then capture

For menu bar apps:
```bash
# Activate the menu bar item first
osascript -e 'tell application "AppName" to activate'
sleep 1
screencapture -l $WINDOW_ID -o -x "$OUTPUT_DIR/popdown.png"
```

### Web Apps

Use Puppeteer or Playwright to navigate each route and screenshot:

```javascript
for (const route of routes) {
  await page.goto(`${baseUrl}${route.path}`, { waitUntil: 'networkidle2' });
  await page.screenshot({ path: `${outputDir}/${route.name}.png` });
}
```

For modals/drawers, click the trigger element first, wait for animation, then capture.

### Multiple Viewport Sizes (Optional)

If user wants responsive shots (common for marketing):
```
viewports:
  - { name: "desktop", width: 1920, height: 1080 }
  - { name: "laptop",  width: 1440, height: 900  }
  - { name: "tablet",  width: 768,  height: 1024 }
  - { name: "mobile",  width: 375,  height: 812  }
```

## Step 4: Output

Default output directory:
```
{project-dir}/screenshots/{YYYY-MM-DD}/
```

Override with any user-specified path.

### Naming Convention

```
{output-dir}/
  01-main-window.png
  02-settings-general.png
  03-settings-appearance.png
  04-popdown-menu.png
  05-onboarding.png
  ...
  summary.md
```

Number prefix keeps order. Slug from view name.

## Step 5: Summary

Generate `summary.md`:

```markdown
# {App Name} - Screenshots
**Date**: YYYY-MM-DD
**Build**: {git hash or version}

| # | View | File | Notes |
|---|------|------|-------|
| 1 | Main Window | 01-main-window.png | Default state |
| 2 | Settings - General | 02-settings-general.png | |
| ... | | | |
```

## Rules

- Always confirm the view list with user before starting captures
- Number screenshots for consistent ordering
- Include app version or git hash in summary for traceability
- If a view requires user interaction to reach (e.g., login, specific data state), ask the user to navigate there and confirm
- Use whatever capture method fits the project -- don't force a specific tool
- For dark/light mode apps, offer to capture both variants
- For apps with multiple states (empty, loading, error, populated), capture each distinct state
