---
name: droid
description: This skill should be used when the user asks to "test Android app", "automate Android emulator", "tap button on Android", "take Android screenshot", "interact with Android UI", "ADB automation", "fill Android form", "swipe on emulator", "validate Android UI flow", or needs to control an Android device/emulator via ADB. Provides a unified CLI with JSON output optimized for LLM consumption.
---

# Droid

Unified Android testing tool with **JSON output** for LLM-friendly automation.

## CLI Discovery

The CLI is located at `./droid-cli/` relative to this SKILL.md file.

| Platform         | Script                                     |
| ---------------- | ------------------------------------------ |
| Unix/Linux/macOS | `droid`                                    |
| Windows          | `droid.cmd` (`droid.ps1` also available)   |

## Prerequisites

- Bun runtime (https://bun.sh)
- ADB (Android Debug Bridge) in PATH
- Connected Android device or running emulator
- USB debugging enabled on device

## Quick Start

```bash
# Check device connection
droid info

# Screenshot + UI elements (most useful command)
droid screenshot

# Tap by text (no coordinates needed!)
droid tap -t "Book Now"

# Fill a form field in one command
droid fill "Email" "user@example.com"

# Wait for element to appear
droid wait-for -t "Success" -s 5
```

## Core Commands

### screenshot
Capture screenshot AND UI elements. Returns element coordinates for tapping.

```bash
droid screenshot
droid screenshot --clickable      # Only clickable elements
droid screenshot --no-ui          # Fast, no element dump
```

**Response:** `{"ok":true,"screenshot":"/tmp/screenshot.png","elements":[{"text":"Book","class":"Button","clickable":true,"x":540,"y":350,"bounds":[400,300,680,400]}]}`

### tap
Tap by text or coordinates.

```bash
droid tap -t "Book Now"           # By text
droid tap -t "State" --prefer-input  # Prefer input fields over labels
droid tap -t "Submit" --clickable    # Only clickable elements
droid tap 540 960                 # By coordinates
```

### fill
Fill text field in one command (tap + clear + type + hide-keyboard).

```bash
droid fill "Enter your email" "user@example.com"
```

### wait-for
Wait for element to appear (with timeout).

```bash
droid wait-for -t "Welcome" -s 10
# Returns: {"ok":true,"found":true,"element":{...}} or {"ok":true,"found":false,"timeout":true}
```

## Form Workflow Commands

### clear / type / hide-keyboard

```bash
droid clear                       # Clear focused field
droid type "hello@example.com"    # Type into focused field
droid hide-keyboard               # Dismiss keyboard (use instead of 'key back')
```

### key
Send key events.

| Key | Purpose |
|-----|---------|
| `back` | Navigate back |
| `enter` | Submit/confirm |
| `move_home` | Cursor to start of text |
| `move_end` | Cursor to end of text |
| `delete` | Backspace |
| `app_home` | Android home screen |

```bash
droid key back
droid key move_home
```

## Other Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `swipe` | Scroll | `droid swipe up` |
| `longpress` | Long press | `droid longpress -t "Item"` |
| `launch` | Launch app | `droid launch com.example.app` |
| `current` | Current activity | `droid current` |
| `info` | Device info | `droid info` |
| `wait` | Wait ms | `droid wait 1000` |
| `select-all` | Select text | `droid select-all` |

See `references/commands.md` for full documentation.

## Testing Workflow

### Recommended Pattern

```bash
# 1. Screenshot to see current state
droid screenshot

# 2. Read the screenshot image with Claude's Read tool
# 3. Tap by text when possible
droid tap -t "Book Now" -w 1000

# 4. Verify the action worked
droid wait-for -t "Booking Confirmed" -s 5
```

### Form Filling Pattern

```bash
# Use fill command for efficiency
droid fill "Email" "user@example.com"
droid fill "Password" "secret123"
droid tap -t "Sign In" --clickable
droid wait-for -t "Welcome" -s 10
```

### Tips

- **Use `--prefer-input`** when tapping form fields to avoid hitting labels
- **Use `--clickable`** when tapping buttons to ensure element is interactive
- **Use `hide-keyboard`** not `key back` to dismiss keyboard
- **Use `wait-for`** instead of blind `wait` for reliable verification

## Error Handling

All errors return JSON with `"ok":false`:

```bash
droid tap -t "NonexistentButton"
# {"ok":false,"error":"No element found matching 'NonexistentButton'"}
```
