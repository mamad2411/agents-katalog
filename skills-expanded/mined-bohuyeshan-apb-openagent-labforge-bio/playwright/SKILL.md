---
name: playwright
description: "Browser automation via Playwright MCP server. Uses MCP tools (browser_navigate, browser_click, etc.). If Playwright MCP is not available, fall back to `agent-browser` skill (CLI, always works)."
category: browser
exposure: standard
---

# Playwright Browser Automation

**When to use this skill**: Complex browser automation needing full Playwright API. Only works when `browser_puppeteer` MCP is enabled.

**If MCP is not available**: Use `agent-browser` skill instead — it works via CLI without any MCP.

**Other browser skills** (pick the right one):
- `agent-browser` — standalone CLI, always works (recommended default)
- `playwright-cli` — playwright via CLI commands (no MCP)
- `dev-browser` — persistent page state with Node.js scripts

## Quick Start

When MCP is available, use Playwright MCP tools directly:
- `browser_navigate` — navigate to URL
- `browser_click` — click element
- `browser_type` — type text
- `browser_screenshot` — take screenshot
- `browser_snapshot` — get page accessibility tree
