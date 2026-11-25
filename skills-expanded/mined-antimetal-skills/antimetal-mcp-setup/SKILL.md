---
name: antimetal-mcp-setup
description: "Configure the Antimetal MCP server connection. Use when the user needs to set up Antimetal in their AI editor, is getting authentication errors, or wants to verify the connection is working. Also triggers for: 'how do I connect Antimetal', 'set up MCP', 'authentication failed', 'configure API key', 'configure OAuth'."
---

# Antimetal MCP Setup

You are helping the user connect their AI editor to the Antimetal MCP server at `https://mcp.antimetal.com`.

## Primary path: OAuth (recommended)

Most modern AI editors handle OAuth automatically when you connect to a remote MCP server. No manual configuration is needed:

1. The editor opens a browser window with Antimetal's login page
2. The user logs in (SSO or email/password)
3. The editor receives a token and stores it securely
4. Done. `/investigate` and `/fix` are ready to use

**If your editor opened a browser login and it succeeded, you're done.** Run `search_issues` to verify connectivity.

## Fallback path: API key

If OAuth isn't working or your editor doesn't support it, use an API key:

1. **Generate a key**: go to `https://overlook.antimetal.com/settings/api-keys` and create a new API key
2. **Set the environment variable**:
   ```bash
   export ANTIMETAL_API_KEY=your_key_here
   ```
   Add it to your shell profile (`~/.zshrc`, `~/.bashrc`) to persist across sessions.
3. **Configure your editor** (if the env var isn't picked up automatically):

   **Claude Code**: add to `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "antimetal": {
         "type": "http",
         "url": "https://mcp.antimetal.com",
         "headers": { "Authorization": "Bearer ${ANTIMETAL_API_KEY}" }
       }
     }
   }
   ```

   **Cursor**: add to `mcp.json`. Cursor only expands `${env:NAME}`; a plain `${ANTIMETAL_API_KEY}` is sent as literal text and fails:
   ```json
   {
     "mcpServers": {
       "antimetal": {
         "url": "https://mcp.antimetal.com",
         "headers": { "Authorization": "Bearer ${env:ANTIMETAL_API_KEY}" }
       }
     }
   }
   ```

   **VS Code**: add to `.vscode/mcp.json`:
   ```json
   {
     "servers": {
       "antimetal": {
         "type": "http",
         "url": "https://mcp.antimetal.com",
         "headers": { "Authorization": "Bearer ${ANTIMETAL_API_KEY}" }
       }
     }
   }
   ```

4. **Restart your editor** after changing the config.

## Verify the connection

Call `search_issues` with no arguments. A successful response (even an empty list) confirms the MCP server is connected and authenticated.

A missing, expired or revoked token makes the editor show the server as needing login, or makes tool calls fail with `401`. With OAuth, log in again. With an API key, check that the variable is set and expanded (in Cursor, `${env:ANTIMETAL_API_KEY}`), and that the key still exists in API Keys Settings.

The tools you see depend on your organization's setup, so another teammate's list can differ from yours.
