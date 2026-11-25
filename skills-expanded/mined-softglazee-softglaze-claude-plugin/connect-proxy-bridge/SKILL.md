---
name: connect-proxy-bridge
description: Step-by-step setup of the SoftGlaze Proxy Bridge so Claude can use the SoftGlaze Proxy Switcher extension (download, pair with the extension, add it to Claude Code, Cowork or Claude Desktop). Use when the user wants to connect Claude to SoftGlaze Proxy, or when softglaze-proxy tools are missing or fail to connect.
argument-hint: "[path to the bridge folder]"
arguments: [folder]
---

# Connect the SoftGlaze Proxy Bridge

Bridge folder: $folder (if empty, ask the user where they unzipped the bridge).

The user does every step on their own computer. The pairing code is shown by the extension and works
once, for 10 minutes; the user types it into their own terminal, not into this chat.

1. **Requirements.** The SoftGlaze Proxy Switcher extension in Chrome or Edge, and Node.js 20 or
   newer (`node --version` in a terminal).
2. **Download the bridge** from the SoftGlaze website (the extension's "AI apps (MCP)" settings link
   to it) and unzip it to a folder that will stay put, for example `C:\SoftGlaze\softglaze-proxy-bridge`.
   It already contains its packages; there is no `npm install`.
3. **Pair it.** In the extension: Settings, "AI apps (MCP)", turn on "Let AI apps connect", type the
   bridge folder, and press **Pair**. The extension shows a one-time code and the exact command, for
   example: `node "C:\SoftGlaze\softglaze-proxy-bridge\bin\softglaze-proxy-bridge.js" pair ABCDE-FGHJK`.
   The user runs it in a terminal; it ends once the extension has paired.
4. **Add the bridge to Claude.**
   - Claude Code (one command, all projects):
     `claude mcp add --transport stdio --scope user softglaze-proxy -- node "<folder>/bin/softglaze-proxy-bridge.js"`
     You may run this command for the user with their folder filled in, after they confirm the path.
     Then they run `/mcp` to check that `softglaze-proxy` is connected.
   - Claude Desktop: Settings, Developer, Edit Config (`claude_desktop_config.json`), add
     `"softglaze-proxy": { "command": "node", "args": ["<folder>/bin/softglaze-proxy-bridge.js"] }`
     inside `"mcpServers"`, then quit and reopen the app. Anthropic's articles differ on whether
     Cowork tasks can use servers from this file; if the tools do not show up in Cowork, use Claude
     Code or a Claude Desktop chat.
   - If the app cannot find `node`, use its full path (`where node` on Windows).
5. **Check it.** Ask Claude to call get_status. If it fails: the browser must be open with the
   extension enabled, "Let AI apps connect" must be on, and the pairing must be done. The bridge
   listens on 127.0.0.1 ports 47615 to 47617 only; another program on all three ports blocks it.
   `node "<folder>/bin/softglaze-proxy-bridge.js" status` shows whether it is paired.

Nothing goes to SoftGlaze's servers: the AI app talks to the bridge over stdio, and the bridge talks
to the extension over a local WebSocket that only the paired extension may open.
