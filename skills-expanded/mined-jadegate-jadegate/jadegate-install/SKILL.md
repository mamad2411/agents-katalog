---
name: jadegate-install
description: Auto-install JadeGate security proxy into all MCP client configurations. One command to protect Claude Desktop, Cursor, Windsurf, Cline, Continue, and Zed.
---

# MCP Protection Installer

Auto-install JadeGate security proxy into all MCP client configurations. One command to protect Claude Desktop, Cursor, Windsurf, Cline, Continue, and Zed.

## When to Use

- User wants to protect their MCP tool calls
- User wants to install JadeGate on their AI clients
- User asks about securing Claude Desktop, Cursor, or other MCP clients

## Usage

```bash
pip install jadegate                   # Install the package
jadegate install                       # Protect all detected MCP clients
jadegate status                        # Check protection status
jadegate uninstall                     # Remove protection (restore backups)
```

## How It Works

1. Detects installed MCP clients and their config files
2. Creates backup of each config (`.jadegate-backup`)
3. Wraps each MCP server command with JadeGate proxy
4. All tool calls now pass through 6 security layers

## Fully Reversible

`jadegate uninstall` restores all original configurations from backup.
