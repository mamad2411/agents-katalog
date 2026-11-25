---
name: eyebrowse-setup
description: Install, configure, and troubleshoot Eyebrowse browser bridge
---

# Eyebrowse Setup & Diagnostics

When this skill is invoked, run all diagnostic checks below in order and report a status table. Then offer to fix anything that's broken.

## Architecture Quick Reference

Eyebrowse has three parts:
- **Daemon** — Bun HTTP/WS server on `localhost:7890` (manages sessions, bridges MCP ↔ extension)
- **MCP Server** — stdio wrapper that registers with the daemon and exposes browser tools to Claude Code
- **Chrome Extension** — WebSocket client that executes commands in Chrome via CDP

Flow: Claude Code → MCP (stdio) → Daemon (HTTP :7890) → Extension (WS) → Chrome

## Diagnostic Checks

Run these checks and present results as a status table:

### 1. Daemon Health

```bash
curl -sf http://localhost:7890/health
```

- **OK** → daemon is running
- **Connection refused** → daemon is not running (see "Start the Daemon" below)
- **Timeout** → port 7890 may be blocked or daemon is hung

### 2. Extension Connected

Read the daemon token, then query windows:

```bash
TOKEN=$(cat ~/.eyebrowse/daemon.token 2>/dev/null)
curl -sf -H "Authorization: Bearer $TOKEN" http://localhost:7890/api/windows
```

- **Returns JSON array with windows** → extension is connected and Chrome is open
- **Empty array `[]`** → extension is installed but no Chrome windows are open
- **401/no token** → daemon token missing (daemon may need restart)
- **Connection refused** → daemon not running

### 3. MCP Config

Read `~/.claude.json` and check for `mcpServers.eyebrowse`. It should look like:

```json
{
  "mcpServers": {
    "eyebrowse": {
      "command": "bun",
      "args": ["run", "<EYEBROWSE_HOME>/mcp/index.ts"]
    }
  }
}
```

Where `<EYEBROWSE_HOME>` is the path to the eyebrowse repo (e.g. `/Users/evan/memory/eyebrowse`).

- **Present and correct** → MCP is configured
- **Missing** → add the config (see "Configure MCP" below)
- **Wrong path** → update the path to match the actual repo location

### 4. End-to-End Test

If checks 1-3 pass, run a live test:

1. Call `mcp__eyebrowse__open_browser` with url `https://example.com`
2. Call `mcp__eyebrowse__screenshot`
3. Verify the screenshot shows the Example Domain page
4. Call `mcp__eyebrowse__close_window`

If this works, eyebrowse is fully operational.

## Setup Guide

### Install Dependencies

```bash
cd <EYEBROWSE_HOME> && bun install
cd <EYEBROWSE_HOME>/daemon && bun install
cd <EYEBROWSE_HOME>/mcp && bun install
```

### Install the Chrome Extension

1. Open `chrome://extensions` in Chrome
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select `<EYEBROWSE_HOME>/extension/`
5. The eyebrowse icon should appear in the toolbar

### Start the Daemon

**Option A — LaunchD (auto-start on boot, recommended):**

```bash
# Fill in template placeholders
BUN_PATH=$(which bun)
BUN_DIR=$(dirname "$BUN_PATH")
EYEBROWSE_HOME="<EYEBROWSE_HOME>"

sed -e "s|__BUN_PATH__|$BUN_PATH|g" \
    -e "s|__BUN_DIR__|$BUN_DIR|g" \
    -e "s|__EYEBROWSE_HOME__|$EYEBROWSE_HOME|g" \
    "$EYEBROWSE_HOME/com.eyebrowse.daemon.plist" \
    > ~/Library/LaunchAgents/com.eyebrowse.daemon.plist

launchctl load ~/Library/LaunchAgents/com.eyebrowse.daemon.plist
```

**Option B — Manual (foreground, good for debugging):**

```bash
bun run <EYEBROWSE_HOME>/daemon/index.ts
```

### Configure MCP

Read `~/.claude.json`, merge in the eyebrowse MCP server config, and write it back:

```json
{
  "mcpServers": {
    "eyebrowse": {
      "command": "bun",
      "args": ["run", "<EYEBROWSE_HOME>/mcp/index.ts"]
    }
  }
}
```

After adding, restart Claude Code for the MCP server to load.

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| All eyebrowse tools fail with "tool not found" | MCP not configured | Add eyebrowse to `~/.claude.json` mcpServers and restart Claude Code |
| `open_browser` / `screenshot` timeout | Extension not connected | Open Chrome, check extension is loaded and enabled, check popup shows green dot |
| `connection refused` on port 7890 | Daemon not running | Start via launchd or manually: `bun run daemon/index.ts` |
| Daemon starts then immediately exits | Port 7890 in use | `lsof -i :7890` to find the process, kill it, restart daemon |
| `401 Unauthorized` from daemon | Token mismatch | Restart daemon to regenerate token; MCP reads it fresh on next call |
| Extension popup says "Daemon not running" | Daemon unreachable from extension | Verify daemon is running and listening on 7890 |
| Screenshot returns black/blank image | Wrong window paired | Use `list_windows` to see available windows, `pair_window` to pick the right one |
| "Rate limit exceeded" on `open_browser` | >3 opens per minute | Wait 60 seconds and retry |
| Daemon logs show WS errors | Extension crashed or Chrome closed | Reopen Chrome; extension auto-reconnects with backoff |

## Key Paths

| What | Path |
|------|------|
| Daemon token | `~/.eyebrowse/daemon.token` |
| Daemon stdout log | `/tmp/eyebrowse-daemon-stdout.log` |
| Daemon stderr log | `/tmp/eyebrowse-daemon.log` |
| LaunchD plist | `~/Library/LaunchAgents/com.eyebrowse.daemon.plist` |
| Daemon port | `localhost:7890` |
