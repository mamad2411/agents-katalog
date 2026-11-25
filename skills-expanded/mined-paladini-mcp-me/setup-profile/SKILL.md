---
name: setup-profile
description: Initialize and populate a mcp-me personal profile from public APIs. Use when the user needs to set up, generate, or refresh their mcp-me profile.
---

# Setup mcp-me Profile

Guide the user through creating and populating their personal profile.

## Prerequisites

- Node.js 20+
- `npm install -g mcp-me` or use `npx mcp-me`

## Step 1 — Initialize

```bash
mcp-me init
```

Creates `~/.mcp-me/` with YAML templates and `.mcp-me.yaml` config.

## Step 2 — Configure sources

Edit `~/.mcp-me/.mcp-me.yaml` and uncomment generators/plugins:

```yaml
generators:
  github: your-username
  devto: your-username

plugins:
  github:
    enabled: true
    username: your-username
```

## Step 3 — Generate profile data

```bash
mcp-me generate
```

Pulls data from public APIs listed in `.mcp-me.yaml`. No API keys needed for most sources.

CLI flags also work as overrides: `mcp-me generate --github octocat --devto myuser`

## Step 4 — Validate

```bash
mcp-me validate
```

Checks all YAML files against the Zod schema.

## Step 5 — Start MCP server

```bash
mcp-me serve
```

Defaults to `~/.mcp-me`. Override with `MCP_ME_PROFILE_DIR` or pass a path: `mcp-me serve ~/my-profile`.

## Step 6 — Connect to AI assistant

Add to `.cursor/mcp.json` or use the one-click install badge from the README:

```json
{
  "mcpServers": {
    "me": {
      "command": "npx",
      "args": ["-y", "mcp-me", "serve"]
    }
  }
}
```

## Profile location

| Method | Path |
|---|---|
| Default | `~/.mcp-me` |
| Env var | `MCP_ME_PROFILE_DIR=/path/to/profile` |
| CLI arg | `mcp-me serve /path/to/profile` |
