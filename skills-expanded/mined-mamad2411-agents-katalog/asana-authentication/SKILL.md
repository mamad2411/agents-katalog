---
name: asana-authentication
description: "Set up Asana MCP integration with OAuth for Claude Code. Connects to official Asana MCP V2 server. Use before any Asana operations."
---

# Asana Authentication Skill

Connect to Asana using the official Asana MCP V2 server with OAuth authentication.

## Setup Instructions

When this skill is invoked, follow these steps IN ORDER.

### Step 1: Check if Asana MCP is already connected

Try calling the Asana MCP tool:

```
mcp__asana__asana_list_workspaces
```

- If it **returns workspace data**: Authentication is working. Display the workspace name and confirm success. No further action needed.
- If the **tool is not found** or returns an error: Continue to Step 2.

**IMPORTANT:** Do NOT use `claude mcp list` to check registration — it does not work reliably from within Claude Code. The only reliable check is calling the MCP tool directly (above).

### Step 2: Set up the Asana MCP server

Ask the user if they already have an Asana OAuth app. If not, guide them:

1. Go to https://app.asana.com/0/my-apps
2. Click **Create new app**
3. Name it "Claude Code"
4. In the OAuth section, note the **Client ID** and **Client Secret**
5. Add this **Redirect URI**: `http://localhost:8080/callback`
6. Save the app

Once the user provides their **Client ID** and **Client Secret**, run the setup script:

```bash
bash resources/asana_auth.sh setup <CLIENT_ID> <CLIENT_SECRET>
```

To use a different callback port (e.g., if 8080 is in use):

```bash
bash resources/asana_auth.sh setup <CLIENT_ID> <CLIENT_SECRET> --port 8081
```

Replace `<CLIENT_ID>` and `<CLIENT_SECRET>` with the values the user provided.

### Step 3: Restart and authenticate

After the setup script succeeds, the server is registered but **not yet loaded or authenticated**. Tell the user:

> "Asana MCP server registered! To complete setup:
> 1. **Restart Claude Code** (the MCP server needs to load on startup)
> 2. After restart, type `/mcp` in the chat, find the **asana** server, and authenticate
>
> Once done, all Asana skills will work automatically."

After the user confirms they've authenticated via `/mcp`, proceed to Step 4.

### Step 4: Verify connection

Call `mcp__asana__asana_list_workspaces` to confirm the connection works.

## Commands Reference

| Command | Description |
|---------|-------------|
| `bash resources/asana_auth.sh setup <ID> <SECRET>` | Register Asana MCP server |
| `bash resources/asana_auth.sh setup <ID> <SECRET> --port 8081` | Register with custom port |
| `bash resources/asana_auth.sh remove` | Remove Asana MCP server |

## Troubleshooting

### "Tool not found" after setup
- Type `/mcp` in Claude Code, find the asana server, and make sure it's enabled and authenticated.
- If that doesn't work, restart Claude Code. MCP servers are loaded at startup.

### OAuth flow didn't open in browser
- Check that port 8080 is not in use by another application
- If port 8080 is taken, remove and re-add with a different port:
  ```bash
  bash resources/asana_auth.sh remove
  bash resources/asana_auth.sh setup <CLIENT_ID> <CLIENT_SECRET> --port 8081
  ```
  Also update the redirect URI in your Asana app to `http://localhost:8081/callback`

### "redirect_uri does not match"
- In your Asana app settings, ensure the redirect URI is exactly `http://localhost:8080/callback`

### "client_id and client_secret must authorize the app"
- Verify the client secret is correct. Re-check at https://app.asana.com/0/my-apps
- Remove and re-add the MCP server with the correct secret

### "does not support dynamic client registration"
- You must provide `--client-id` when adding the server

## Next Steps

Once authenticated, use the `asana-actions` skill to:
- Create and manage tasks
- Search and filter tasks
- Organize projects
- Add comments and collaborate
