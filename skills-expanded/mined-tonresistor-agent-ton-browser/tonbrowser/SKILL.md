---
name: tonbrowser
description: Browse .ton sites on the TON decentralized network using agent-tonbrowser CLI. Automate Tonnet Browser via Chrome DevTools Protocol : navigate to .ton domains, take screenshots, read page content, click elements, fill forms, and extract data. Use when the user asks to visit a .ton site, take a screenshot of a .ton page, read content from the TON network, interact with a .ton website, or automate browsing on TON. Triggers include "go to X.ton", "open X.ton", "screenshot X.ton", "what's on X.ton", "browse TON", "navigate to .ton", "check .ton site", "read .ton page".
allowed-tools: Bash(agent-tonbrowser:*), Bash(curl:*), Bash(timeout:*), Bash(sleep:*), Bash(pgrep:*), Bash(pkill:*)
---

# TON Browser Automation

Automate Tonnet Browser to navigate .ton sites via `agent-tonbrowser` CLI.

## Setup

Locate the binary first. Check common paths in order:
1. `which agent-tonbrowser` (if installed globally or in PATH)
2. `../agent-tonbrowser/agent-tonbrowser` (sibling directory)
3. `find ~ -name agent-tonbrowser -type f -executable 2>/dev/null | head -1`

Store the result as `ATB` for all subsequent commands.

## Launching Tonnet Browser

The browser must be running with `--remote-debugging-port` for CDP automation.

### Linux (AppImage)
```bash
# Find and launch the AppImage
APPIMAGE=$(find ~/Applications ~/.local/bin /opt -name "*onnet*rowser*.AppImage" -o -name "*on-browser*" 2>/dev/null | head -1)
pgrep -f ton-browser || { "$APPIMAGE" --remote-debugging-port=9222 &>/dev/null & sleep 6; }
```

### macOS (DMG : no code signing)
Tonnet Browser is **not code-signed**. macOS will block it on first launch.
```bash
# Remove quarantine attribute first (required : no code signing)
xattr -cr "/Applications/TON Browser.app"
# Then launch
open -a "TON Browser" --args --remote-debugging-port=9222
sleep 6
```

### Windows (NSIS installer : no code signing)
```powershell
# Remove SmartScreen block (required : no code signing)
Unblock-File -Path "$env:LOCALAPPDATA\Programs\TON Browser\TON Browser.exe"
# Launch
& "$env:LOCALAPPDATA\Programs\TON Browser\TON Browser.exe" --remote-debugging-port=9222
```

## Core Workflow

```
1. ENSURE browser running    → launch or detect via pgrep
2. ENSURE TON connected      → click "Connect to TON Network" if needed
3. NAVIGATE to .ton site     → fill address bar + press Enter
4. WAIT for page load        → sleep 5-10s
5. IDENTIFY correct target   → check /json/list for tab index
6. READ / INTERACT / CAPTURE → eval, screenshot, click, fill
```

## Quick Start

```bash
# 1. Ensure browser running
pgrep -f ton-browser || echo "Launch Tonnet Browser with --remote-debugging-port=9222 first"

# 2. Connect to TON network
$ATB --tab 0 eval '(() => { const b = document.querySelector("button"); if (b && b.textContent.includes("Connect")) { b.click(); return "connecting" } return "already connected" })()'
sleep 10

# 3. Navigate
$ATB --tab 0 fill "input" "piracy.ton"
$ATB --tab 0 press Enter
sleep 8

# 4. Identify target
curl -s http://127.0.0.1:9222/json/list | python3 -c "
import sys,json
for i,t in enumerate(json.load(sys.stdin)):
    if not t.get('url','').startswith('devtools://'):
        print(f'[{i}] {t.get(\"title\",\"\")} : {t.get(\"url\",\"\")[:80]}')
"

# 5. Read content (tab 1 = .ton page)
$ATB --tab 1 eval 'document.body.innerText.substring(0, 2000)'

# 6. Screenshot
$ATB --tab 1 screenshot /tmp/page.png
$ATB --tab 0 screenshot /tmp/browser-ui.png
```

## Target Model

| --tab | Target | Use for |
|-------|--------|---------|
| 0 | Main renderer (browser UI) | Address bar, tabs, nav buttons, status |
| 1+ | WebContentsView (.ton page) | Page content, screenshots, interaction |

**Always re-check target order after navigation** : indices can shift. Use the curl snippet or `$ATB tab`.

## Key Patterns

### Read page text
```bash
$ATB --tab 1 eval 'document.body.innerText.substring(0, 2000)'
```

### List all links
```bash
$ATB --tab 1 eval '(() => Array.from(document.querySelectorAll("a")).map(a => a.href + " " + a.textContent.trim()).join("\n"))()'
```

### Click a link or button
```bash
$ATB --tab 1 click "a.nav-link"
$ATB --tab 1 eval '(() => { const a = document.querySelector("a[href*=about]"); if(a){a.click();return "clicked"} return "not found" })()'
```

### Search on a page
```bash
$ATB --tab 1 fill "input[type=search]" "query"
$ATB --tab 1 press Enter
```

### Screenshot
```bash
$ATB --tab 1 screenshot /tmp/output.png        # .ton page
$ATB --tab 0 screenshot /tmp/browser.png        # full browser UI
$ATB --tab 1 screenshot -f /tmp/full-page.png   # full page capture
```

### Navigate to a different .ton site (already connected)
```bash
$ATB --tab 0 fill "input" "newsite.ton"
$ATB --tab 0 press Enter
sleep 8
# Re-check targets : the new page may have a different tab index
```

### Click a link within the .ton page
```bash
$ATB --tab 1 eval '(() => { const a = document.querySelector("a[href*=page2]"); if(a){a.click();return "navigating"} return "link not found" })()'
sleep 5
```

### Extract structured data (table rows, lists)
```bash
$ATB --tab 1 eval '(() => {
  const rows = document.querySelectorAll("table tr");
  return Array.from(rows).map(r => Array.from(r.cells).map(c => c.textContent.trim()).join(" | ")).join("\n");
})()'
```

### Check connection status
```bash
$ATB --tab 0 eval '(() => document.body.innerText.includes("Connected to TON") ? "connected" : "disconnected")()'
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `connect: connection refused` | Browser not running. Launch with `--remote-debugging-port=9222`. |
| `no page target found` | Browser just started : wait a few more seconds for renderer to init. |
| eval/screenshot timeout | Use `timeout 15 $ATB ...`. Retry once : Electron can be slow on first CDP call. |
| Wrong tab content | Re-check targets with curl `/json/list`. Target order can shift. |
| `Disconnected` in status bar | TON proxy not started. Click "Connect to TON Network" button first. |
| Navigation doesn't load | Wait longer (10-15s). TON proxy uses garlic routing : adds latency. |
| macOS: "app is damaged" | Run `xattr -cr "/Applications/TON Browser.app"` : no code signing. |
| Windows: SmartScreen blocks | `Unblock-File -Path "$env:LOCALAPPDATA\Programs\TON Browser\TON Browser.exe"` |

## Rules

- **eval over snapshot**: AX tree is minimal on Electron. Use `eval 'document.body.innerText'` for text.
- **IIFE for eval**: Wrap complex JS in `(() => { ... })()` to prevent redeclaration errors.
- **Wait after navigation**: .ton pages load via garlic-routed TON proxy. Wait 5-10s.
- **React inputs**: `fill` uses Ctrl+A before typing : works with React controlled inputs.
- **Key names for press**: `Enter`, `Tab`, `Escape`, `Backspace`, `Delete`, `ArrowUp/Down/Left/Right`, `Home`, `End`, `PageUp/Down`, `Space`.
- **Browser persists**: agent-tonbrowser does NOT close the browser between commands.
- **timeout wrapper**: Use `timeout 10 $ATB ...` to prevent hanging commands.
- **One instance**: Never launch a second Tonnet Browser if one is already running.
- **No code signing**: macOS needs `xattr -cr`, Windows needs SmartScreen bypass.

For the full command reference, read [references/commands.md](references/commands.md).
