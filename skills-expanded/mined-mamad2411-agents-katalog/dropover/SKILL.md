---
name: dropover
description: "Configure Dropover file-shelf workflows and URL integrations, and diagnose macOS gesture or window behavior."
category: macos
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["dropover", "macos", "nspanel", "cgeventtap", "drag-and-drop", "url-scheme", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Dropover macOS Drag Shelf Utility AI Skill Guide (Claude)

## Overview & Engine Architecture
Dropover is a modular macOS productivity utility that provides temporary floating drag shelves to aggregate files, images, snippets, and web links across Mission Control Spaces and full-screen apps. Dropover operates via custom **`NSPanel` floating windows** styled with `.nonactivatingPanel` and `.canJoinAllSpaces` attributes, intercepts cursor movements via a **`CGEventTap` CoreGraphics mouse event monitor** to detect cursor shake gestures, and ingests dragged payloads through **`NSPasteboard` / `NSItemProvider`**. Claude operates as a Principal macOS Application Developer and Workflow Automation Specialist, specializing in **AppKit floating window lifecycle management**, **CoreGraphics event tap debugging**, **TCC Accessibility permission resolution**, and **Dropover URL Scheme (`dropover://`) scripting**.

### Dropover Window & Event Ingestion Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Dropover Engine Architecture                │
│                                                             │
│  Event Monitoring & Gesture Trigger Layer                   │
│  ├── `CGEventTap` Mouse Delta Vector Tracker (Shake Sensor) │
│  ├── Global Hotkey Listener (`NSEvent.addGlobalMonitor...`) │
│  └── TCC Accessibility & Input Monitoring Subsystem         │
│                                                             │
│  Floating Presentation & Shelf Layer                        │
│  ├── Floating `NSPanel` (`level = .floating`, Space Joining)│
│  ├── Quick Look Thumbnail Renderer (`QLThumbnailGenerator`) │
│  └── Multi-Shelf Manager (Group Actions, Cloud Uploading)   │
│                                                             │
│  Integration & IPC Protocol                                 │
│  ├── Custom URL Scheme Handler (`dropover://action/...`)    │
│  └── macOS Shortcuts & AppleScript Dispatch Interface       │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Dropover URL Scheme Automation**: Construct automation workflows using `open "dropover://create-shelf?files=..."` to programmatically spawn floating shelves from scripts.
2. **Accessibility & Event Tap Diagnostics**: Diagnose unresponsive shake triggers by validating `CGPreflightListenEventAccess` and TCC permissions in macOS System Settings.
3. **Multi-Space Shelf Persistence**: Configure `NSWindow.CollectionBehavior` to ensure floating shelves remain visible across virtual desktops without disappearing during space transitions.
4. **Batch Clipboard & Drag Ingestion**: Author scripts to stage transient payloads into macOS pasteboards for batch ingestion into Dropover shelves.

---

## Production Python Automation: Automated File Stager & Dropover Shelf Dispatcher

Save this script as `stage_to_dropover.py` to collect files and programmatically open a Dropover floating shelf via its URL scheme:

```python
"""
Dropover macOS URL Scheme Dispatcher
Collects target files and triggers a new floating shelf in Dropover.
"""

import sys
import os
import urllib.parse
import subprocess

def create_dropover_shelf(file_paths: list):
    valid_paths = [os.path.abspath(p) for p in file_paths if os.path.exists(p)]
    if not valid_paths:
        print("Error: No valid file paths provided.")
        return

    print(f"--- [DISPATCHING {len(valid_paths)} FILES TO DROPOVER SHELF] ---")
    for p in valid_paths:
        print(f"  • {p}")

    # Build Dropover URL Scheme payload
    # Format: dropover://create-shelf?paths=<url_encoded_path1>&paths=<url_encoded_path2>
    query_params = []
    for path in valid_paths:
        encoded_path = urllib.parse.quote(path)
        query_params.append(f"paths={encoded_path}")

    url = f"dropover://create-shelf?{'&'.join(query_params)}"
    
    # Trigger URL via macOS open command
    try:
        subprocess.run(["open", url], check=True)
        print("✅ Dropover shelf created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"🚨 Failed to launch Dropover URL scheme: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 stage_to_dropover.py file1.png file2.pdf ...")
        sys.exit(1)
    create_dropover_shelf(sys.argv[1:])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Shake Gesture Fails to Open Shelf** | Dropover lacks macOS Accessibility / Input Monitoring permissions to capture global cursor velocity. | 1. Open *System Settings $\rightarrow$ Privacy & Security $\rightarrow$ Accessibility*.<br>2. Enable **Dropover**.<br>3. In *Dropover Preferences $\rightarrow$ Triggers*, adjust **Shake Sensitivity** slider to Medium/High. |
| **Floating Shelves Disappear When Switching Spaces** | Dropover window collection behavior configured to standard space rather than `canJoinAllSpaces`. | In Dropover Preferences $\rightarrow$ **Shelves**, check **Keep shelves on screen across all Spaces**. |
| **`dropover://` URL Scheme Opens Safari Instead of App** | Custom URL scheme registration not registered in LaunchServices. | Run `/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain user`. |
| **High Memory Usage on Large Image Drops** | Quick Look thumbnail generation cache generating uncompressed bitmap buffers. | In Dropover Preferences, reduce maximum preview resolution or dismiss shelves after drop. |

---

## Command Line Syntax & macOS Terminal Recipes

```bash
# 1. Trigger Dropover Launch via macOS Terminal
open -a Dropover

# 2. Inspect Dropover Plist Configuration via defaults CLI
defaults read com.extendedmac.Dropover-mac

# 3. Create a New Empty Shelf via URL Scheme
open "dropover://create-shelf"
```

### Essential File Locations
- **Dropover Preferences**: `~/Library/Preferences/com.extendedmac.Dropover-mac.plist`
- **Application Support Cache**: `~/Library/Application Support/com.extendedmac.Dropover-mac`

---

## Agent Operational Directive
> **MANDATORY**: Verify that Dropover is granted Accessibility permissions in macOS System Settings before diagnosing shake gesture failures. Use encoded file paths when constructing `dropover://` URL schemes.
