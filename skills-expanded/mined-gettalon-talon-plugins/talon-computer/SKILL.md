---
name: talon-computer
description: Control the macOS desktop — move mouse, click, type, press keys, scroll, drag, take screenshots, list windows/displays, clipboard. Uses usecomputer CLI for native Quartz event automation. For desktop UI automation, form filling, app control, and AI computer-use.
allowed-tools: Bash
---

# Computer Use

Control the macOS desktop using the `usecomputer` CLI. 17 commands for mouse, keyboard, screenshots, windows, displays, clipboard, and coordinate mapping.

## Setup

```bash
npm install -g usecomputer
```

Requirements: macOS, Accessibility permissions enabled for your terminal, Node.js 18+.

## Core Workflow

1. **Screenshot** → see what's on screen
2. **Analyze** → find the target coordinates
3. **Act** → click, type, or press keys (use `--coord-map` from screenshot)
4. **Verify** → screenshot again to confirm

## Commands (17 total)

### Screenshot
```bash
usecomputer screenshot /tmp/screen.png --json
usecomputer screenshot /tmp/region.png --region 0,0,800,600 --json
usecomputer screenshot /tmp/win.png --window 1234 --json
usecomputer screenshot /tmp/screen.png --display 1 --json
usecomputer screenshot /tmp/annotated.png --annotate --json
```
Options: `--region x,y,w,h`, `--display N`, `--window ID`, `--annotate`, `--json`
Returns JSON: `path`, `coordMap`, `desktopIndex`, `imageWidth`, `imageHeight`, `hint`

**Always pass `--coord-map` from screenshot output when clicking/hovering/dragging.**

### Click
```bash
usecomputer click -x 500 -y 300 --coord-map "0,0,1792,1120,1568,980"
usecomputer click -x 500 -y 300 --button right --coord-map "..."
usecomputer click -x 500 -y 300 --count 2 --coord-map "..."
usecomputer click -x 500 -y 300 --modifiers ctrl,shift --coord-map "..."
```
Options: `--button left|right|middle`, `--count N`, `--modifiers ctrl,shift,alt,meta`, `--coord-map`

### Hover — Move cursor without clicking
```bash
usecomputer hover -x 500 -y 300 --coord-map "..."
```

### Mouse Move
```bash
usecomputer mouse move -x 500 -y 300 --coord-map "..."
```

### Mouse Down / Up — Press and hold / release
```bash
usecomputer mouse down --button left
usecomputer mouse up --button left
```
Options: `--button left|right|middle`

### Mouse Position
```bash
usecomputer mouse position --json
```

### Type
```bash
usecomputer type "Hello world"
usecomputer type "slow text" --delay 20
cat file.txt | usecomputer type --stdin --chunk-size 4000 --chunk-delay 15
usecomputer type "limited" --max-length 1000
```
Options: `--delay ms`, `--stdin`, `--chunk-size N`, `--chunk-delay ms`, `--max-length N`

### Press — Keyboard shortcuts
```bash
usecomputer press "cmd+s"
usecomputer press "cmd+shift+p"
usecomputer press "enter" --count 3 --delay 100
```
Options: `--count N`, `--delay ms`

### Scroll
```bash
usecomputer scroll down 3
usecomputer scroll up 5
usecomputer scroll left 2
usecomputer scroll right 2
usecomputer scroll down 3 --at 500,300
```
Syntax: `scroll <direction> [amount]`. Options: `--at x,y`

### Drag
```bash
usecomputer drag 100,200 500,400 --coord-map "..."
usecomputer drag 100,200 500,400 --duration 500 --button left --coord-map "..."
```
Syntax: `drag <from> <to>`. Options: `--duration ms`, `--button`, `--coord-map`

### Debug Point — Visualize click target
```bash
usecomputer debug-point -x 400 -y 220 --coord-map "0,0,1792,1120,1568,980"
usecomputer debug-point -x 400 -y 220 --coord-map "..." --output /tmp/debug.png --json
```
Draws a red marker on a fresh screenshot. Use to verify coordinates before clicking.

### Display List
```bash
usecomputer display list
usecomputer display list --json
```
Lists connected displays with index, size, position, scale, name.

### Desktop List
```bash
usecomputer desktop list
usecomputer desktop list --windows
usecomputer desktop list --windows --json
```
Lists desktops. `--windows` groups open windows by desktop.

### Window List
```bash
usecomputer window list
usecomputer window list --json
```
Lists all windows with id, app, pid, size, position, title.

### Clipboard Get
```bash
pbpaste
```

### Clipboard Set
```bash
echo "text to copy" | pbcopy
```

## Coordinate Mapping

Screenshots are scaled (max 1568px longest edge). **Always pass `--coord-map` from the screenshot output** when using click, hover, drag, or mouse move with screenshot coordinates.

```bash
# Take screenshot, get coordMap
usecomputer screenshot /tmp/screen.png --json
# Output includes: "coordMap": "0,0,1792,1120,1568,980"

# Click using screenshot coordinates + coordMap
usecomputer click -x 400 -y 220 --coord-map "0,0,1792,1120,1568,980"
```

The `--coord-map` flag automatically maps image pixels to real screen coordinates.

## Anthropic Computer Use Integration

| Claude Action | usecomputer Command |
|--------------|-------------------|
| `screenshot` | `usecomputer screenshot /tmp/screen.png --json` |
| `left_click` | `usecomputer click -x X -y Y --coord-map "..."` |
| `double_click` | `usecomputer click -x X -y Y --count 2 --coord-map "..."` |
| `right_click` | `usecomputer click -x X -y Y --button right --coord-map "..."` |
| `mouse_move` | `usecomputer hover -x X -y Y --coord-map "..."` |
| `type` | `usecomputer type "text"` |
| `key` | `usecomputer press "key_combo"` |
| `scroll` | `usecomputer scroll down 3` |

## Examples

### Open app and interact
```bash
usecomputer press "cmd+space" && sleep 0.5
usecomputer type "Safari" --delay 30 && sleep 0.5
usecomputer press "enter" && sleep 1
usecomputer screenshot /tmp/screen.png --json
# Use coordMap from output for all subsequent clicks
usecomputer click -x 784 -y 52 --coord-map "0,0,1792,1120,1568,980"
```

### Fill a form
```bash
usecomputer click -x 400 -y 300 --coord-map "..."
usecomputer press "cmd+a"
usecomputer type "hunter@example.com"
usecomputer press "tab"
usecomputer type "MyPassword123"
usecomputer press "enter"
```

### Drag and drop
```bash
usecomputer drag 200,300 600,300 --coord-map "..." --duration 300
```

### Window management
```bash
usecomputer window list --json
usecomputer screenshot /tmp/win.png --window 1234 --json
```

### Clipboard operations
```bash
usecomputer click -x 400 -y 300 --count 3 --coord-map "..."
usecomputer press "cmd+c"
usecomputer clipboard get
```

## Tips

- **Always screenshot first** and pass `--coord-map` to click/hover/drag
- **Use `--json`** on screenshot for machine-readable coordMap
- **Use debug-point** to verify coordinates before clicking important targets
- **Add `sleep`** between actions for apps that need time to respond
- **Use `--delay` for typing** in apps that drop fast keystrokes
- **Use `window list`** to find window IDs for targeted screenshots
- **Use `hover`** instead of `mouse move` when working with screenshot coords
