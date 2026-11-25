---
name: repo-browser-mcp-configuration
description: Reviews browser MCP setup and server choice. Use when configuring Chrome DevTools MCP, Playwright MCP, browser debug ports, headless mode, isolated profiles, or browser automation MCP boundaries.
---


# Browser MCP Configuration

Use this skill when setting up or reviewing browser MCP configuration.

## Included MCP Servers

- `chrome-devtools`
- `chrome-devtools-antigravity-browser`
- `playwright`

All are disabled by default.

## Selection Guidance

- Use `chrome-devtools` for console/network/performance/DevTools-focused browser debugging.
- Use `chrome-devtools-antigravity-browser` only when intentionally connecting to a running local browser debug port.
- Use `playwright` for structured browser automation and repeatable interaction flows.

## Required Behavior

- Keep MCPs disabled until intentionally enabled.
- Prefer one browser MCP server per task.
- Never include real credentials.
- Do not expose remote debugging ports to non-loopback interfaces.
- Explain privacy implications before connecting to authenticated sessions.
- Validate config before enabling.

## Workflow

Use `workflows/browser-mcp-setup-review-workflow.md`.

## Scripts

This skill owns:

```text
scripts/validate-browser-mcp-config.py
```

