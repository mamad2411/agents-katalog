---
name: jadegate-scan
description: Scan and audit installed MCP servers for security risks. Discovers servers from Claude Desktop, Cursor, Windsurf, Cline, Continue, and Zed configs, then assesses each for dangerous capabilities.
---

# MCP Security Scanner

Scan and audit installed MCP servers for security risks. Discovers servers from Claude Desktop, Cursor, Windsurf, Cline, Continue, and Zed configs, then assesses each for dangerous capabilities.

## When to Use

- User wants to audit their MCP servers for security risks
- User asks about MCP security or tool call safety
- User wants to know which MCP servers are installed and their risk level
- User mentions security scanning or server auditing

## Usage

```bash
jadegate scan                          # Scan all detected MCP servers
jadegate scan --output report.json     # Save JSON report
jadegate scan --probe                  # Launch servers to test capabilities
```

## What It Detects

- Shell execution capabilities (CRITICAL risk)
- Arbitrary code execution (CRITICAL risk)
- Browser automation (HIGH risk)
- Credential/secret access (HIGH risk)
- File system access (MEDIUM risk)
- Network capabilities (MEDIUM risk)

## Supported Clients

- Claude Desktop
- Cursor
- Windsurf
- Cline (VS Code)
- Continue
- Zed

## Output

Risk levels: CRITICAL, HIGH, MEDIUM, LOW for each detected MCP server.
