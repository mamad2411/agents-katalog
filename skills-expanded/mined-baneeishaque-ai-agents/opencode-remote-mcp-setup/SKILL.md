---
name: opencode-remote-mcp-setup
description: Composer skill for adding remote MCP servers to OpenCode configuration with authentication and validation.
category: Tool-Infrastructure
---

# OpenCode Remote MCP Server Setup Skill (v1)

This skill provides a standardized procedure for adding remote MCP servers (like UptimeRobot) to OpenCode's configuration.
It enriches the generic MCP management procedure with OpenCode-specific schema knowledge and validation.

***

## 1. Prerequisites

Before adding a remote MCP server, the agent MUST:

- **Verify opencode installation**: Check that `opencode` command is available in PATH
- **Determine config scope**: Ask user whether to modify global (`~/.config/opencode/opencode.json`) or project (`./opencode.json`) config
- **Research server documentation**: Use `webfetch` to retrieve official MCP server documentation for URL and auth methods

## 2. Configuration Schema

### 2.1 Local vs Remote Servers
OpenCode's `mcp` section supports two server types:

**Local (stdio) servers**:
```json
"mcp": {
  "local-server-name": {
    "type": "local",
    "command": "/path/to/binary",
    "args": ["--flag", "value"],
    "env": {
      "API_KEY": "{env:REAL_API_KEY}"
    },
    "enabled": true
  }
}
```

**Remote (HTTP) servers**:
```json
"mcp": {
  "remote-server-name": {
    "type": "remote",
    "url": "https://mcp.example.com/mcp",
    "headers": {
      "Authorization": "Bearer {env:API_KEY}"
    },
    "enabled": true
  }
}
```

### 2.2 Authentication Methods
OpenCode remote MCP servers support:

1. **Bearer Token (recommended for simplicity)**:
   - `headers.Authorization`: `Bearer <token>` or `Bearer {env:ENV_VAR_NAME}`
   - Token can be literal or interpolated from environment variable

2. **OAuth 2.0**:
   - `oauth` object with:
     - `clientId`: string or `{env:OAUTH_CLIENT_ID}`
     - `clientSecret`: string or `{env:OAUTH_CLIENT_SECRET}`
     - `tokenUrl`: string (OAuth token endpoint URL)
     - `scopes`: array of strings (requested permissions)

## 3. Integration Workflow

Follow these steps to add a remote MCP server to OpenCode:

### 3.1 Discovery Phase
1. Use `webfetch` to retrieve MCP server documentation
2. Identify the server's URL endpoint (e.g., `https://mcp.uptimerobot.com/mcp`)
3. Determine available authentication methods (Bearer token, OAuth, API key in headers)

### 3.2 Auth Method Selection
Ask the user to choose authentication method:
- API Key/Bearer token (simplest, recommended for services like UptimeRobot)
- OAuth 2.0 (more complex, suitable for services requiring user authorization)

### 3.3 Credential Collection
Based on selected auth method:
- **Bearer token**: Ask for API key value or environment variable name
- **OAuth**: Ask for client ID, client secret (or env var), token URL, and scopes

### 3.4 Config Scope Selection
Ask user: "Modify global config (`~/.config/opencode/opencode.json`) or project config (`./opencode.json`)?"

### 3.5 Configuration Insertion
1. Read the target `opencode.json` file (handle JSONC format with trailing commas/comments)
2. Locate or create the `mcp` object
3. Add server entry with appropriate fields based on auth method
4. For Bearer token: Add `url`, `headers.Authorization`, `enabled: true`
5. For OAuth: Add `url`, `oauth` object, `enabled: true`
6. Maintain alphabetical order within the `mcp` object
7. Write back to file preserving JSONC format

### 3.6 Validation
1. Validate JSON syntax: `jq empty <config_file>`
2. Verify config structure: `jq '.mcp.<server-name>' <config_file>` returns expected object
3. Confirm required fields are present and correctly formatted

### 3.7 Post-Installation Steps
1. Instruct user to restart opencode client (configuration loaded on startup)
2. Recommend functional test: Ask a question that uses the MCP server's capabilities
3. Example for UptimeRobot: "Show me all monitors" should return monitor list

## 4. Verification Protocol

The agent MUST verify the new configuration before concluding:

1. **JSON Lint Check**: Run `jq empty <config_file>` - must exit with code 0
2. **Config Read-Back**: Run `jq '.mcp.<server-name>' <config_file>` - must return server object
3. **Restart Notification**: Clearly inform user to restart opencode
4. **Functional Test Guidance**: Provide example query to test server functionality

## 5. Traceability & Recording

### 5.1 Redaction & Privacy
- **Absolute Paths**: When recording logs, NEVER include biological or system-specific user prefixes
- **Redaction**: Replace sensitive prefixes (e.g., `/Users/username/`) with `[REDACTED]`
- **Credentials**: NEVER log API keys or tokens; show only `[REDACTED]` or environment variable names

### 5.2 Contextual Documentation
- **Session Logs**: Store all session records in `docs/conversations/` folder
- **Implementation Plans**: Save this workflow as `docs/implementation-plans/<date>-opencode-remote-mcp-setup.md`

## 6. Composition by Higher-Level Skills

When the same remote MCP server needs to be configured for multiple users or environments:
- This skill can be called repeatedly with different credential values
- Consider creating project-specific opencode.json for team-shared MCP server configurations

***

## Design Appendix (Design Fidelity)

| Feature | Change Note | Rationale |
|:---|:---|:---|
| **JSONC Support** | Explicitly handle trailing commas and comments in opencode.json | OpenCode config uses JSONC, not strict JSON |
| **Env Var Interpolation** | Support `{env:VAR_NAME}` syntax in headers and env fields | Enables secure credential handling without hardcoding |
| **Alphabetical Ordering** | Require alphabetical ordering of servers within `mcp` object | Consistency with mcp-management skill and maintainability |
| **Scope Selection** | Explicit global vs project config choice | Respects user's isolation preferences |
| **Clear Restart Requirement** | Mandatory user notification about restart needed | Configuration only loads on opencode startup |
| **Functional Test Guidance** | Provide concrete example queries for verification | Ensures working configuration beyond syntax validity |

## Related Skills
- [`mcp-management`](../mcp-management/SKILL.md) — Base generic MCP server management (enriched by this skill)
- [`mcp-cross-tool-config-sync`](../mcp-cross-tool-config-sync/SKILL.md) — For distributing to multiple tools (future extension)
- [`opencode-permission-config`](../opencode-permission-config/SKILL.md) — For configuring tool permissions
- [`opencode-provider-persistence-config`](../opencode-provider-persistence-config/SKILL.md) — For understanding OpenCode credential storage
- [`opencode-jsonc-util`](../opencode-jsonc-util/SKILL.md) — Base JSONC utility for OpenCode config files
- [`is-this-command-safe`](../is-this-command-safe/SKILL.md) — For validating any custom verification commands