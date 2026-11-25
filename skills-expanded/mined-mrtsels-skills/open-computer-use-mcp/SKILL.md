---
name: open-computer-use-mcp
description: Install, configure, and test open-computer-use — an MCP server that provides macOS desktop computer use (screenshot, mouse, keyboard) to any MCP-compatible agent (Claude Desktop, Codex, Gemini, Hermes). Covers npm install, macOS permission grants, MCP config for Claude Desktop and Hermes, and JSON-RPC verification.
tags: [mcp, computer-use, desktop, macos, automation, open-computer-use]
---

# open-computer-use MCP Server Setup

`open-computer-use` is an open-source MCP server that wraps macOS Accessibility APIs to provide computer-use capabilities (screenshots, click, drag, scroll, type, key press) to any MCP-compatible AI agent. It's an open-source alternative to OpenAI's Codex Computer Use.

**Repo**: https://github.com/iFurySt/open-codex-computer-use  
**npm**: `open-computer-use` (global CLI)

## Trigger

- User wants to give an AI agent the ability to control macOS (see screen, move mouse, type, click)
- User wants the Claude Desktop Computer Use feature but without an Anthropic subscription
- User asks about Computer Use alternatives that work with any provider
- User has a non-OpenAI model and wants desktop automation capabilities

## Prerequisites

- Node.js (for npm global install)
- macOS (also supports Linux and Windows)
- npx available (for verification)

## Steps

### 1. Install

```bash
npm install -g open-computer-use
```

Verify:
```bash
open-computer-use --version
```

### 2. Grant macOS Permissions (macOS only)

Run once to trigger permission dialogs:

```bash
open-computer-use
```

Check status:
```bash
open-computer-use doctor
```

Expected output when granted:
```
Permissions: accessibility=granted, screenRecording=granted
```

If missing, open System Settings:
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
```

Manually add the binary at:
```
/Users/<user>/.npm-global/bin/open-computer-use
```

**Both** Accessibility and Screen Recording permissions are required.

### 3. Add to Claude Desktop (3p mode)

Edit `~/Library/Application Support/Claude-3p/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "open-computer-use": {
      "command": "open-computer-use",
      "args": ["mcp"]
    }
  }
}
```

Restart Claude Desktop (Cmd+Q, reopen) to load the new MCP server.

### 4. Add to Hermes Agent

Edit `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  open-computer-use:
    command: open-computer-use
    args: ["mcp"]
    timeout: 300
```

Restart Hermes or reload MCP servers with `/reset`.

### 5. Test the MCP Server

Verify the server responds correctly via JSON-RPC over stdio:

```bash
# List available tools
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | open-computer-use mcp
```

Expected tools in response:
- `list_apps` — List running applications
- `get_app_state` — Get app window state + screenshot + accessibility tree
- `click` — Click by element index or coordinates
- `drag` — Drag from one point to another
- `scroll` — Scroll in a direction
- `type_text` — Type text
- `press_key` — Press keyboard keys
- `set_value` — Set element value directly
- `perform_secondary_action` — Right-click or context menu

Test basic functionality:
```bash
# List running apps
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_apps","arguments":{}}}' | open-computer-use mcp
```

```bash
# Get app state (requires permissions)
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_app_state","arguments":{"app":"Finder"}}}' | open-computer-use mcp
```

### 6. Available MCP Tools

| Tool | Description | Key Parameters |
|------|-------------|---------------|
| `list_apps` | List running apps with bundle IDs, PIDs, usage | None |
| `get_app_state` | Screenshot + AX accessibility tree | `app` (bundle name) |
| `click` | Click by element index or pixel coordinates | `app`, `element_index` or `x`/`y` |
| `type_text` | Type text into focused element | `app`, `text` |
| `press_key` | Press keyboard keys/combos | `app`, `key` (e.g. "cmd+s") |
| `scroll` | Scroll viewport | `app`, `direction`, `pages` |
| `drag` | Drag from one point to another | `app`, `from_x/y`, `to_x/y` |
| `set_value` | Set element value directly | `app`, `element_index`, `value` |
| `perform_secondary_action` | Context menu / right-click | `app`, `element_index`, `action` |

All tools accept the `app` parameter (bundle name like "Finder", "Safari", or bundle ID like "com.apple.Safari").

## Pitfalls

- **Permissions required on first run**: Both Accessibility and Screen Recording must be granted in macOS System Settings. The running process may need to be restarted after granting — if `get_app_state` returns 0-byte screenshots, restart the MCP server.
- **Permission scope**: Permissions are tied to the executable path. If you install via npx or a different path, you may need to re-grant permissions for that specific binary.
- **Permissions persist per-app**: Once granted, they persist across versions. If you reinstall, macOS may ask again.
- **Screenshot may be empty**: In direct pipe-mode testing (`echo ... | open-computer-use mcp`), screenshots may return 0 bytes because the server process exits before completing capture. In actual MCP client use (Claude Desktop, Hermes), the persistent server process handles this correctly.
- **npm global path**: The binary is at `$(npm root -g)/../bin/open-computer-use`. Use this path when adding to System Settings permissions dialog.
- **No authentication**: The MCP server runs on local stdio only — no network port, no auth concern.

## Comparison: `open-computer-use` vs Hermes built-in `computer_use`

| Aspect | open-computer-use (MCP) | Hermes `computer_use` (cua-driver) |
|--------|----------------------|-----------------------------------|
| Interface | MCP stdio server | Direct tool in Hermes toolset |
| Compatible with | Any MCP client (Claude Desktop, Codex, Gemini, Hermes) | Hermes Agent only |
| Installation | `npm i -g open-computer-use` | Built into Hermes (enabled via `hermes tools`) |
| macOS permissions | Manual grant in System Settings | Same, via cua-driver setup |
| Screenshot | Returns base64 PNG in MCP response | Returns PNG bytes in tool result |

## Verification

After setup:
- `open-computer-use doctor` shows `accessibility=granted, screenRecording=granted`
- `list_apps` returns a list of running apps with bundle IDs
- `get_app_state` returns both accessibility tree (~100-700 lines) and screenshot
- Claude Desktop loads the server on restart (check MCP section in settings)
- Hermes shows "Added servers: open-computer-use" in system message
