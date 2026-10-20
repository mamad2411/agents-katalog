---
name: repo-mcp-troubleshooting
description: Troubleshoots MCP startup, authentication, transport, runtime, tool discovery, and disabled-server issues. Use when MCP servers do not appear, fail to start, cannot authenticate, or expose unexpected tools.
---

# Repo MCP Troubleshooting

Use this skill when an MCP server fails to load, authenticate, expose tools, or behave as expected.

## Troubleshooting Areas

- JSON syntax
- wrong config location
- disabled server
- missing runtime such as Node, npx, Python, uvx, or Docker
- bad command or args
- missing credentials
- remote URL/network failure
- OAuth/header issues
- client needs restart/reload
- tools hidden by `disabledTools`
- server exposes unexpected tools

## Workflow

Use `workflows/mcp-troubleshooting-workflow.md` for systematic troubleshooting.

