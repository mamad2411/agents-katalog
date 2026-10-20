---
name: "mcp-dynamic-discovery"
description: "Claude Code MCP Dynamic Discovery: zero-config external tool integration. Automatically scans system configuration directories for active Model Context Protocol (MCP) servers and configures them locally"
---

# MCP Dynamic Discovery — Zero-Config Tool Integration

## When to activate
- Integrating with external tools (Slack, Jira, GitHub, Figma, Linear, databases) in a new workspace.
- When you want to reuse existing MCP configurations from Claude Desktop, Cursor, or other IDEs without manual copying.
- Connecting to local services (PostgreSQL, Redis, Docker) that expose MCP endpoints.
- Minimizing setup friction for team members checking out a repository.

## When NOT to use
- Purely offline coding sessions with no external APIs or integrations.
- High-security environments where dynamic discovery of local configs or outbound network connections is restricted.
- Shared systems where other users' configs shouldn't be read.

## Instructions

The MCP Dynamic Discovery skill automates the detection, import, and wiring of Model Context Protocol (MCP) servers located on the user's system into the active Claude Code CLI session.

```
       Local Configuration Directories (Desktop, Cursor, Windsurf)
                               │
                               ▼
               ┌───────────────────────────────┐
               │    1. Scan Configuration      │
               │ (Search configs/SQLite DBs)   │
               └───────────────┬───────────────┘
                               │
                               ▼
               ┌───────────────────────────────┐
               │  2. Extract Servers & Tools   │
               │ (Parse commands/envs/tokens)  │
               └───────────────┬───────────────┘
                               │
                               ▼
               ┌───────────────────────────────┐
               │      3. Dynamic Injector      │
               │ (Merge into .claude/settings) │
               └───────────────────────────────┘
```

### 1. Config Directories to Scan
Scan the standard operating system paths where AI clients store MCP server configurations:

*   **Mac OS:**
    *   Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   Cursor global storage: `~/Library/Application Support/Cursor/User/globalStorage/saantiagoo.mcp-connector/mcp-servers.json`
*   **Windows:**
    *   Claude Desktop: `%APPDATA%\Claude\claude_desktop_config.json`
    *   Cursor global storage: `%APPDATA%\Cursor\User\globalStorage\saantiagoo.mcp-connector\mcp-servers.json`
*   **Linux:**
    *   Claude Desktop: `~/.config/Claude/claude_desktop_config.json`

### 2. Auto-Discovery Script
To discover and list servers, run this quick check command:

```bash
# Locate and view server configurations
if [ -f "$HOME/Library/Application Support/Claude/claude_desktop_config.json" ]; then
  echo "Found Claude Desktop MCP configs:"
  cat "$HOME/Library/Application Support/Claude/claude_desktop_config.json" | grep -A 5 -B 1 '"mcpServers"'
fi
```

### 3. Merging Settings
Once target server definitions are extracted, write/merge them directly into the current repository's `.claude/settings.json`:

```json
{
  "mcpServers": {
    "discovered-postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/my_db"]
    },
    "discovered-slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-xxxx-xxxx"
      }
    }
  }
}
```

### 4. Connection Verification
Run `/mcp` in Claude Code to verify that the newly wired servers are alive, their connection statuses are green, and their schemas are successfully exposed.

---

## Example

**Claude Code dynamically configuring Slack and Figma tools during a session:**

1.  **Prompt:** "Connect to my Slack and Figma tools so I can send the QA report."
2.  **Action:** Claude searches typical system locations and detects a configured Slack token and command inside the Claude Desktop config.
3.  **Result:** Claude Code merges the server definitions into `.claude/settings.json` and prompts the user to refresh the session:
    ```
    ✅ Dynamically discovered 2 MCP servers from Claude Desktop:
       - 'slack-server'
       - 'figma-server'
    
    Writing configurations to local .claude/settings.json...
    Run '/mcp reload' to activate the new tools.
    ```
4.  **Verification:** The user runs `/mcp list` and sees Slack channels and Figma file inspection tools ready to use.
