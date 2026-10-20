---
name: rectangle
description: "Configure Rectangle window shortcuts and multi-display layouts; troubleshoot macOS Accessibility permissions and URL actions."
category: macos
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["rectangle", "macos-window-manager", "axuielement", "accessibility-api", "window-tiling", "url-scheme", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Rectangle macOS Window Manager AI Skill Guide (Claude)

## Overview & Engine Architecture
Rectangle is an open-source macOS window management utility engineered in Swift and AppKit. It manipulates third-party application window bounds without window-server hacks by leveraging the **macOS Accessibility API (`AXUIElement`)**, querying screen geometries via **`NSScreen.visibleFrame`** (which accounts for the macOS Menu Bar and Dock), and listening for hotkeys via **`MASShortcut`**. Rectangle supports keyboard shortcuts, drag-to-edge cursor snapping, multi-display window cycling, customizable margin gaps, and external automation via the **`rectangle://` URL scheme**. Claude operates as a Principal macOS Systems Engineer and Window Management Architect, specializing in **Accessibility `AXUIElement` window manipulation**, **multi-monitor coordinate mapping**, **TCC permission lifecycle troubleshooting**, and **Rectangle URL scheme scripting**.

### Rectangle Window Server & Accessibility Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Rectangle Engine Architecture               │
│                                                             │
│  Input & Trigger Subsystem                                  │
│  ├── Global Hotkey Listener (`MASShortcut` / Carbon Events) │
│  ├── Drag-to-Edge Cursor Tracker (`NSEvent` Global Monitor) │
│  └── URL Scheme Action Dispatcher (`rectangle://execute...`)│
│                                                             │
│  Geometry Calculation & Coordinate Engine                   │
│  ├── `NSScreen.visibleFrame` (Menu Bar & Dock Offset Math)  │
│  ├── Multi-Display Topology Resolver (Display ID Offsets)   │
│  └── Window Padding / Margin Gap Subtractor                 │
│                                                             │
│  macOS Accessibility Manipulation Tier                      │
│  ├── Target App Accessibility Node (`AXUIElement`)          │
│  ├── Set Window Position (`kAXPositionAttribute`)           │
│  └── Set Window Dimensions (`kAXSizeAttribute`)             │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Rectangle URL Scheme Automation**: Construct terminal and Python automation scripts dispatching commands via `open "rectangle://execute-action?name=<action>"` (*e.g. `left-half`, `right-half`, `maximize`, `first-third`*).
2. **Native `AXUIElement` Window Manipulation**: Author standalone Swift scripts demonstrating direct manipulation of `kAXPositionAttribute` and `kAXSizeAttribute` on running application processes.
3. **Multi-Display Coordinate Triage**: Troubleshoot window jumping and misalignment across mixed DPI Retina and external displays by calculating relative `NSScreen` frame bounds.
4. **TCC Accessibility Permissions Recovery**: Remediate non-responsive shortcuts using `tccutil reset Accessibility com.knollsoft.Rectangle` and system permission verification.

---

## Production Swift Automation: Standalone Native Window Snapper (`AXUIElement`)

Save this file as `snap_window.swift` and execute via `swift snap_window.swift left`:

```swift
// ==============================================================================
// Standalone Swift 5.x Script: Native macOS Window Snapper (AXUIElement)
// Tiles the frontmost application window to Left or Right half without dependencies.
// ==============================================================================
import Cocoa

guard CommandLine.arguments.count > 1 else {
    print("Usage: swift snap_window.swift <left|right|maximize>")
    exit(1)
}

let action = CommandLine.arguments[1].lowercased()

// 1. Verify Accessibility Permissions
guard AXIsProcessTrusted() else {
    print("🚨 Error: Accessibility permissions not granted. Enable Terminal in System Settings -> Accessibility.")
    exit(1)
}

// 2. Get Frontmost Application Process
guard let frontApp = NSWorkspace.shared.frontmostApplication else {
    print("Error: No frontmost application detected.")
    exit(1)
}

let appElement = AXUIElementCreateApplication(frontApp.processIdentifier)
var focusedWindow: AnyObject?
let result = AXUIElementCopyAttributeValue(appElement, kAXFocusedWindowAttribute as CFString, &focusedWindow)

guard result == .success, let window = focusedWindow else {
    print("Error: Could not access focused window on \(frontApp.localizedName ?? "App").")
    exit(1)
}

let windowElement = window as! AXUIElement

// 3. Calculate Target Screen Bounds (Excluding Menu Bar & Dock)
guard let screen = NSScreen.main else {
    print("Error: Main display not detected.")
    exit(1)
}

let visibleFrame = screen.visibleFrame
let screenHeight = screen.frame.height

var targetX: CGFloat = visibleFrame.origin.x
var targetY: CGFloat = screenHeight - visibleFrame.origin.y - visibleFrame.height
var targetW: CGFloat = visibleFrame.width
var targetH: CGFloat = visibleFrame.height

if action == "left" {
    targetW = visibleFrame.width / 2.0
} else if action == "right" {
    targetX = visibleFrame.origin.x + (visibleFrame.width / 2.0)
    targetW = visibleFrame.width / 2.0
} else if action != "maximize" {
    print("Invalid action. Use 'left', 'right', or 'maximize'.")
    exit(1)
}

// 4. Apply Position and Size via Accessibility API
var newPoint = CGPoint(x: targetX, y: targetY)
var newSize = CGSize(width: targetW, height: targetH)

let posValue = AXValueCreate(.cgPoint, &newPoint)!
let sizeValue = AXValueCreate(.cgSize, &newSize)!

AXUIElementSetAttributeValue(windowElement, kAXPositionAttribute as CFString, posValue)
AXUIElementSetAttributeValue(windowElement, kAXSizeAttribute as CFString, sizeValue)

print("✅ Snapped \(frontApp.localizedName ?? "Window") to '\(action)'.")
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Shortcuts Stop Working / Window Refuses to Move** | macOS Accessibility permission revoked after an application update. | 1. In Terminal, run: `tccutil reset Accessibility com.knollsoft.Rectangle`.<br>2. Open *System Settings $\rightarrow$ Privacy & Security $\rightarrow$ Accessibility*.<br>3. Toggle **Rectangle** ON. |
| **Window Snaps to Wrong Display in Multi-Monitor Setup** | "Displays have separate Spaces" setting disabled, confusing `NSScreen` frame origins. | In System Settings $\rightarrow$ *Desktop & Dock*, check **Displays have separate Spaces**, then log out and log back in. |
| **Unwanted Gaps Around Snapped Windows** | Window Margin / Gap Size setting configured in Rectangle preferences. | In Rectangle Preferences $\rightarrow$ **Settings**, set **Gap size** to `0px`. |
| **Certain Windows (Calculator, System Settings) Won't Resize** | Target application window has fixed minimum/maximum constraints in AppKit (`NSWindow.minSize == NSWindow.maxSize`). | This is expected macOS behavior; fixed-dimension utility panels cannot be resized. |

---

## Command Line Syntax & URL Scheme Actions

```bash
# 1. Tile Frontmost Window to Left Half via Rectangle URL Scheme
open -g "rectangle://execute-action?name=left-half"

# 2. Tile Frontmost Window to Right Half
open -g "rectangle://execute-action?name=right-half"

# 3. Maximize Frontmost Window
open -g "rectangle://execute-action?name=maximize"

# 4. Reset Rectangle Accessibility Permissions via CLI
tccutil reset Accessibility com.knollsoft.Rectangle
```

### Essential File Locations
- **Preferences Plist**: `~/Library/Preferences/com.knollsoft.Rectangle.plist`
- **Application Binary**: `/Applications/Rectangle.app`

---

## Agent Operational Directive
> **MANDATORY**: When triggering Rectangle actions via shell scripts, always use the `-g` (background) flag with `open "rectangle://execute-action?name=..."` to avoid stealing focus from the active window being tiled.
