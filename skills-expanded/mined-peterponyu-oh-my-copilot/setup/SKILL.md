---
name: setup
description: "[OMCP] Use first for MCP server configuration and plugin setup"
level: 2
---

# Setup

Use `/omcp:setup` as the setup/configuration entrypoint for this plugin.

## Usage

```bash
/omcp:setup mcp            # MCP server configuration
/omcp:setup mcp github     # GitHub MCP server setup
```

## Routing

Process the request by the **first argument only**:

- `mcp` -> route to `/omcp:mcp-setup` with everything after the `mcp` token
- No argument or unrecognised -> show this help and suggest `/omcp:verify` for diagnostics

Examples:

```bash
/omcp:setup mcp github       # => /omcp:mcp-setup github
```

## Notes

- `/omcp:mcp-setup` remains a valid direct entrypoint.
- To diagnose the plugin install, run `bash scripts/run-validation.sh` from the repo root, or use `/omcp:verify`.
- Prefer `/omcp:setup` in new documentation and user guidance.

Task: {{ARGUMENTS}}
