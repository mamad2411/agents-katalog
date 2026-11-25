---
name: install-codex-chrome-mcp
description: Install and verify ChromeWire MCP, the local bridge between the official Codex Chrome Extension and MCP-compatible AI CLI tools.
---

# Install ChromeWire MCP

Use this when a user wants an agent to install ChromeWire MCP on a local machine for GSD/Pi, Codex CLI, Claude Code, Cursor, Windsurf, or another MCP-compatible client.

## Official extension first

The user must have the official Codex Chrome Extension installed and enabled:

```text
https://chromewebstore.google.com/detail/hehggadaopoacecdllhhajmbjkdcmajg
```

If the Chrome Web Store listing is unavailable in the user's region, tell them that a USA IP via VPN/proxy may be required to install the official extension. Use only legal, policy-compliant access methods. Do not install random third-party mirrors.

## Agent install steps

1. Verify Node.js 20+ is installed.
2. Verify Google Chrome is installed.
3. Verify or ask the user to install the official Codex Chrome Extension from the link above.
4. Run `npm install`.
5. Run `npm run install:codex-native-host` when the local Codex app is installed and the native host manifest is missing.
6. Run `npm test` and `npm run check`.
7. Run `npm run doctor`.
8. Prefer stdio MCP config when the client can launch local commands. For Codex CLI on macOS, use `/Applications/Codex.app/Contents/Resources/node` plus `src/stdio.js` so Codex owns the MCP subprocess and the browser socket accepts the peer.
9. Use HTTP MCP only when the client supports Streamable HTTP and the bridge is started separately with `npm start`; keep it on `http://127.0.0.1:8962/mcp`.
10. Run `npm run smoke`.
11. Use `codex_chrome_health` to verify the extension pipe is reachable.
12. If multiple Chrome profiles exist, use `codex_chrome_list_profiles` and `codex_chrome_set_profile`.

## MCP config: Codex CLI on macOS

```toml
[mcp_servers.chromewire]
command = "/Applications/Codex.app/Contents/Resources/node"
args = ["/absolute/path/to/chromewire-mcp/src/stdio.js"]
startup_timeout_sec = 20.0
tool_timeout_sec = 180.0
```

## MCP config: Codex CLI on Windows/Linux/Ubuntu

```toml
[mcp_servers.chromewire]
command = "node"
args = ["/absolute/path/to/chromewire-mcp/src/stdio.js"]
startup_timeout_sec = 20.0
tool_timeout_sec = 180.0
```

## MCP config: Streamable HTTP clients

```json
{
  "mcpServers": {
    "chromewire": {
      "type": "http",
      "url": "http://127.0.0.1:8962/mcp"
    }
  }
}
```

## Security rules for agents

- Keep the server bound to `127.0.0.1`.
- Never expose the endpoint through a public tunnel.
- Do not read cookies, passwords, browser history, localStorage, sessionStorage, auth headers, or unrelated tabs.
- Do not take destructive browser actions unless the user explicitly asks.
- Do not commit local files such as `profile-preference.json`, `.env`, logs, or user profile dumps.
