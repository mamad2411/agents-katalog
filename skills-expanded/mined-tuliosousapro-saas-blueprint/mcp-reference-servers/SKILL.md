---
name: mcp-reference-servers
description: Guidance on using and integrating official reference servers. Use when building custom servers or deploying standard configurations. For server listings, see mcp-server-registry.
---

# MCP Reference Servers Skill

## When to Use

- When building new MCP servers and needing a reference implementation.
- When the user wants robust, community-tested servers for common tools (Filesystem, Google Search, Fetch, etc.).
- When debugging MCP connection issues using standardized servers.

## Reference

[MCP Reference Servers GitHub](https://github.com/modelcontextprotocol/servers)

## Instructions

### 1. Identify Target Server

- Review the `src` directory in the reference repository to see available servers.
- Common servers include:
- `fetch`: For web page scraping.
- `filesystem`: For local file access.
- `google-search`: For web searching capabilities.
- `postgres`: For database interaction.

### 2. Implementation & Setup

- Most reference servers are built with Node.js/TypeScript or Python.
- Follow the `README.md` within each sub-directory for build and run instructions.
- Ensure the appropriate runtime (Node.js 18+ or Python 3.10+) is installed.

### 3. Usage via MCP Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

## Quality Gates

- Use `npx` for quick access without local installation unless performance is a concern.
- Keep environment variables secure in protected configuration files.
- Verify the server's capabilities via `list_tools` command after initialization.
