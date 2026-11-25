---
name: notch-kit
description: Build macOS notch apps that live in the MacBook camera notch. Use when a user wants to create a menu bar / notch utility app for macOS. Provides the NotchPanel, NotchShape, hover expand/collapse, notch detection, and a SwiftUI template to customize.
---

# NotchKit — Agent Skill for macOS Notch Apps

Build macOS apps that live in the MacBook notch. This skill gives you the foundation — notch detection, floating panel, hover expand/collapse, curved shape — so you focus on the app logic.

## When to Use

Activate this skill when the user wants to:
- Build a macOS notch app / notch widget
- Create a utility that lives in the MacBook notch
- Build something similar to BoringNotch, NotchNook, or Alcove
- Add a notch-hugging UI to an existing macOS app

## Architecture Overview

```
NotchKit/
  NotchApp.swift           App entry point (@main, SwiftUI lifecycle)
  NotchAppDelegate.swift   Menu bar icon + app lifecycle + clean quit
  NotchPanel.swift         NSPanel (floating, non-activating, .mainMenu + 3)
  NotchShape.swift         Curved shape matching notch (animatable radii)
  NotchWindow.swift        Notch detection, expand/collapse, hover tracking
  NotchContentView.swift   THE FILE TO CUSTOMIZE (collapsed + expanded UI)
  Info.plist               LSUIElement = true (agent app, no dock icon)
```

## Key Concepts

### NotchPanel
A floating `NSPanel` that:
- Sits above all windows (level: `.mainMenu + 3`)
- Never steals focus (`canBecomeKey = false`)
- Visible on all spaces and in fullscreen
- Transparent background — content defines the visible shape

### NotchShape
A SwiftUI `Shape` with quad curves matching the MacBook notch:
- Small top corner radius (curves inward, matching the real notch)
- Large bottom corner radius (smooth tray expansion)
- `animatableData` for smooth transitions between collapsed and expanded

Default radii:
- Collapsed: top = 6, bottom = 14
- Expanded: top = 19, bottom = 24

### NotchWindow
Detects the actual notch dimensions via `NSScreen.auxiliaryTopLeftArea` and `auxiliaryTopRightArea`. Falls back to 185x32 for non-notch Macs.

Two states:
- **Collapsed**: Window = notch width + wing extension. Content on both sides of camera.
- **Expanded**: Window grows to custom size. Full tray UI appears.

Hover triggers expand (0.4s spring). Mouse leave triggers collapse (0.8s delay + 0.35s animation).

### NotchContentView
The only file the user needs to edit. Two sections:
- `collapsedContent` — Left wing + camera gap + right wing
- `expandedContent` — Full tray panel

## Phase 1: Understand What the User Wants

Ask the user:
1. **What app?** — What should the notch app do? (timer, monitor, widget, etc.)
2. **Collapsed view** — What should always be visible on each side of the notch? (app name, status, icon, counter)
3. **Expanded view** — What UI appears when hovering? (buttons, stats, settings, content)
4. **Theme** — Dark only, light only, or both with toggle?

## Phase 2: Clone and Set Up

```bash
git clone https://github.com/aishwaryaashok14/notch-kit.git <project-name>
cd <project-name>
```

Rename the package if needed:
- `Package.swift`: Change package name
- `Info.plist`: Change `CFBundleName` and `CFBundleIdentifier`
- `build-app.sh`: Change binary name and app name

## Phase 3: Build the Collapsed View

Edit `NotchContentView.swift` — the `collapsedContent` property.

Structure is always: left wing + camera gap + right wing.

```swift
var collapsedContent: some View {
    HStack(spacing: 0) {
        // LEFT WING (your app name, icon, status)
        HStack(spacing: 4) {
            // Your content here
        }
        .frame(maxWidth: .infinity, alignment: .center)

        // CAMERA GAP — never put content here
        Color.clear.frame(width: viewModel.notchWidth - 30)

        // RIGHT WING (counter, timer, status indicator)
        HStack(spacing: 4) {
            // Your content here
        }
        .fixedSize()
        .frame(maxWidth: .infinity, alignment: .center)
    }
    .frame(maxWidth: .infinity, maxHeight: .infinity)
    .background(Color.black)  // Always black to merge with the notch
    .clipShape(NotchShape(topCornerRadius: 6, bottomCornerRadius: 14))
}
```

Important rules:
- Background MUST be black (merges with the hardware notch)
- Keep content minimal — wings are ~90px each
- Use monospaced fonts at 8-10pt for readability
- The camera gap width uses `viewModel.notchWidth - 30`

## Phase 4: Build the Expanded View

Edit `NotchContentView.swift` — the `expandedContent` property.

This is a normal SwiftUI view. Design freely. Common patterns:

```swift
var expandedContent: some View {
    VStack(spacing: 10) {
        // Top: main content (character, timer, info)
        // Middle: action buttons
        // Bottom: toolbar / tabs
    }
    .frame(maxWidth: .infinity, maxHeight: .infinity)
}
```

Adjust the expanded panel size in `NotchWindow.swift`:
```swift
var expandedWidth: CGFloat = 420    // Default 420
var expandedHeight: CGFloat = 240   // Default 240
var wingExtension: CGFloat = 180    // Default 180
```

## Phase 5: Add App Logic

Create new Swift files for your app's logic:
- Data models
- Timers / state management (use `ObservableObject` + `@Published`)
- Persistence (`UserDefaults` for settings, JSON file for data)
- Notifications (`UNUserNotificationCenter`)

Pass your state into `NotchContentView` by:
1. Create it in `NotchAppDelegate`
2. Pass it through `NotchWindow` to the content view

## Phase 6: Add Menu Bar Items

Edit `NotchAppDelegate.swift` to add menu items:

```swift
func setupMenuBar() {
    // Change the icon
    button.image = NSImage(systemSymbolName: "your.icon", accessibilityDescription: "Your App")

    // Add your menu items
    let action = NSMenuItem(title: "Your Action", action: #selector(yourMethod), keyEquivalent: "")
    action.target = self
    menu.addItem(action)
}
```

## Phase 7: Build and Test

```bash
chmod +x build-app.sh
bash build-app.sh
open dist/<AppName>.app
```

First launch on a new Mac: right-click the app, click Open, click Open again (one-time macOS Gatekeeper step).

## Phase 8: Package for Distribution

Create a DMG:
```bash
hdiutil create -volname <AppName> -srcfolder dist -ov -format UDZO <AppName>.dmg
```

## Common Patterns

### Adding a theme toggle
Read `NotchKit/NotchContentView.swift` for the base, then create a `ThemeManager` ObservableObject with `@Published var mode: ThemeMode` and CSS-variable-style color properties.

### Adding persistence
Use `UserDefaults` for settings. For structured data, write JSON to `~/Library/Application Support/<AppName>/`.

### Handling sleep/wake
Observe `NSWorkspace.willSleepNotification` and `NSWorkspace.didWakeNotification` for apps that track time.

### Clean quit (preventing ghost windows)
Always implement `applicationWillTerminate` in your AppDelegate:
```swift
func applicationWillTerminate(_ notification: Notification) {
    notchWindow?.destroy()
    if let item = statusItem {
        NSStatusBar.system.removeStatusItem(item)
    }
}
```

## Requirements

- macOS 13+
- Swift 5.9+
- No Xcode project needed (Swift Package Manager)
- Works on MacBooks with and without a notch

## Example: WalkOS

[WalkOS](https://walkos.aishashok.com) is a walking reminder app built entirely on NotchKit. It adds: walk timer, quick-log buttons, streak tracking, work hours, pause, sleep/wake handling, weekly summary, dark/light theme, and walk history — all on top of this same foundation.
