---
description: "Guide users through Chrome extension setup for browser control. Use when user asks about setup, installing the extension, connecting Chrome, or when browser_control tools return 'No browser connected'."
allowed-tools: [Bash]
---

# Browser Control Setup Guide

Help the user set up the Talon Chrome extension so Claude Code can control their browser and chat from Chrome.

## Steps

### 1. Install the Chrome Extension

Run the install script to copy the extension to Downloads:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/install-extension.sh"
```

This copies the extension to `~/Downloads/talon-browser-control` and opens Chrome's extensions page.

### 2. Load in Chrome

Guide the user through these steps:

1. Open Chrome and go to `chrome://extensions`
2. Enable **Developer Mode** (toggle in the top right)
3. Click **"Load unpacked"**
4. Select `~/Downloads/talon-browser-control`
5. The Talon extension icon should appear in the Chrome toolbar

### 3. Verify Connection

Once loaded, the extension will auto-connect to the MCP server. Verify by running:

```
browser_control with action: "get_tabs"
```

If it returns tabs, the connection is working.

### 4. Enable Chat (Claude Code Channels)

This plugin uses Claude Code's **channels** feature (research preview, requires v2.1.80+) for two-way chat between the Chrome extension and Claude Code.

**Requirements:**
- Claude Code v2.1.80 or later
- claude.ai login (Console/API key auth not supported)
- Team/Enterprise orgs must have channels enabled by admin

**Start with channels enabled:**

Since this is a custom channel (not on the official allowlist yet), use the development flag:

```bash
claude --dangerously-load-development-channels plugin:browser-control@gettalon-talon-plugins
```

You can combine with other channels:

```bash
claude --dangerously-load-development-channels plugin:browser-control@gettalon-talon-plugins --channels plugin:telegram@claude-plugins-official
```

**Once started with channels:**
- Open the extension's side panel (click the Talon icon or right-click → "Open side panel")
- Type a message — it arrives in Claude Code as a `<channel source="talon-browser">` notification
- Claude can reply back to the side panel
- Claude's browser tool actions also appear in the side panel in real-time

**Without the flag**: Browser control tools (navigate, click, screenshot, etc.) still work normally. Only the two-way chat requires the channels flag.

### 5. Troubleshooting

**"No browser connected"**: The extension isn't connected. Check:
- Is the extension loaded and enabled in `chrome://extensions`?
- Is Chrome running?
- Try reloading the extension (click the reload icon in `chrome://extensions`)

**"Cannot access a chrome:// URL"**: The active tab is a Chrome internal page. Switch to a regular tab first using `switch_tab`.

**"Debugger is not attached"**: The CDP debugger needs to attach. Navigate to a URL first — the debugger attaches automatically.

**Chat not working**: Make sure Claude Code was started with `--dangerously-load-development-channels plugin:browser-control@gettalon-talon-plugins`

### 6. What You Can Do

**Browser Control** (40 actions):
- Navigate, click, fill forms, type text, keyboard shortcuts
- Screenshots (compressed JPEG), execute JavaScript
- Manage tabs — open, close, switch
- Read pages — page info, extract content, accessibility tree snapshots
- Monitor — network requests, console logs, errors
- Emulate — device metrics, geolocation, media type, offline mode
- And more — drag/drop, viewport, headers, cookies, dialogs

**Chat from Chrome** (requires channels flag):
- Two-way messaging between Chrome side panel and Claude Code
- Real-time display of Claude's browser tool actions
- Send messages with page context (URL, title, selected text)
