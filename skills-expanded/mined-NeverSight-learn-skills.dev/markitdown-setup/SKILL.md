---
name: markitdown-setup
description: Installs markitdown-mcp and registers it as an MCP server in Claude Code settings. Run once before using /convert.
argument-hint: ""
allowed-tools: Bash
---

Run the setup script to install markitdown-mcp and register it in Claude Code:

```
!`bash "${CLAUDE_SKILL_DIR}/scripts/setup.sh"`
```

After the script completes successfully, tell the user to restart Claude Code to activate the MCP server.
