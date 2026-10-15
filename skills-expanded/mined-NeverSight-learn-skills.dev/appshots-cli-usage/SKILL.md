---
name: appshots-cli-usage
description: >
  Core CLI reference for the App Screenshots desktop app.
  Commands, flags, JSON output, port discovery, and connection management.
---

# appshots CLI Usage

Controls the running **App Screenshots** desktop app via HTTP commands on `localhost`.

## Prerequisites

- The App Screenshots desktop app must be running
- Install CLI: `dart pub global activate --source path packages/app_screenshots_cli`
- Port auto-discovered from `~/.config/app-screenshots/server.port`

## Connection

```bash
# Check the app is running and server is available
appshots status
```

## JSON Mode

All commands support `--json` for machine-readable output — essential for AI agents and scripted workflows:

```bash
appshots --json editor state
appshots --json translate get-texts
appshots --json library list
appshots --json editor list-overlays
```

## Command Groups

| Group | Count | Description |
|-------|-------|-------------|
| `editor` | 42 | Canvas, backgrounds, device frames, overlays, export |
| `multi` | 11 | Multi-screenshot editor (max 10 slots) |
| `translate` | 10 | AI translation, per-locale overrides, locale images |
| `library` | 10 | Saved designs, folders, import/export .appshots |
| `preset` | 2 | Browse & apply design presets |
| `status` | 1 | Connection check |

## Quick Reference

```bash
# Status & state
appshots status                        # Check connection
appshots editor state                  # Current design state
appshots multi state                   # Multi-editor state
appshots translate state               # Translation state

# Browse resources
appshots editor list-devices           # Available device frames
appshots editor list-fonts --query ""  # Google Fonts (browsable)
appshots editor list-icons --query ""  # Material & SF Symbols
appshots preset list                   # Available presets
appshots library list                  # Saved designs
```

## API Response Format

All responses return JSON:

```json
{"ok": true, "data": { ... }}
```

```json
{"ok": false, "error": "Error message"}
```

## Display Types

| ID | Description | Resolution | Required (2025) |
|----|-------------|------------|-----------------|
| `APP_IPHONE_69` | iPhone 6.9" (Pro Max) | 1320 × 2868 | ✅ Mandatory |
| `APP_IPHONE_67` | iPhone 6.7" (Pro Max) | 1290 × 2796 | Auto-scaled |
| `APP_IPHONE_65` | iPhone 6.5" | 1284 × 2778 | Auto-scaled |
| `APP_IPHONE_55` | iPhone 5.5" | 1242 × 2208 | Auto-scaled |
| `APP_IPAD_PRO_M4_13` | iPad Pro M4 13" | 2064 × 2752 | ✅ Mandatory |
| `APP_IPAD_PRO_6G_129` | iPad Pro 12.9" | 2048 × 2732 | Auto-scaled |
| `APP_MAC` | Mac App Store | 2880 × 1800 | Optional |

> **Tip:** For 2025, design at 6.9" iPhone + 13" iPad as your base — Apple auto-scales to smaller sizes.

## File Format

- Export as **PNG** (recommended for sharp text and fine UI details)
- JPEG also accepted
- Must be RGB color space, no transparency, flattened
