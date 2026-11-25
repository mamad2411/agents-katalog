---
name: playwright-mcp-setup
description: "Guides setup of @playwright/mcp MCP server to give Claude direct browser control for automated testing and web interaction. Trigger with: playwright MCP, setup playwright MCP, browser control, Claude browser, @playwright/mcp, MCP browser testing, give Claude browser, playwright mcp server."
metadata:
  category: dev
  version: "1.0"
---

## Purpose

Guide the complete setup of `@playwright/mcp` as an MCP server so Claude gains direct browser control for automated testing, web scraping, and UI interaction tasks.

## Trigger

Apply when user requests:
- "Playwright MCP", "setup playwright MCP", "@playwright/mcp"
- "give Claude browser control", "Claude browser automation", "MCP browser testing"
- "configure browser tools for Claude", "browser control via MCP"

Do NOT trigger for:
- Writing Playwright test scripts without MCP — use `playwright-pro`
- General MCP server setup — use `mcp-maker`
- Running existing Playwright tests

## Prerequisites

- Node.js 18+ installed (`node --version`)
- Claude Desktop application installed (or Claude Code CLI configured)
- `npx` available (bundled with Node.js)

## Steps

1. **Install `@playwright/mcp`** — the package is run via `npx`, no global install required. Optionally install browsers:

   ```bash
   # Install Playwright browsers (Chromium is sufficient for most tasks)
   npx playwright install chromium
   ```

2. **Configure the MCP server in Claude Desktop** — edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       }
     }
   }
   ```

   For a headed browser (visible window) — useful for debugging:

   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest", "--headed"]
       }
     }
   }
   ```

3. **Configure for Claude Code CLI** — if using Claude Code rather than Claude Desktop, add to the project's MCP config (`.claude/mcp.json`):

   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       }
     }
   }
   ```

4. **Restart Claude** — fully quit and reopen Claude Desktop (or restart the Claude Code session) for the new MCP server to be loaded

5. **Verify browser tools are available** — in a new Claude session, check that browser tools appear. Claude should now have access to tools such as:
   - `browser_navigate` — navigate to a URL
   - `browser_click` — click an element
   - `browser_type` — type text into an input
   - `browser_screenshot` — capture a screenshot
   - `browser_evaluate` — execute JavaScript in the page
   - `browser_wait_for` — wait for an element or condition

6. **Test the setup** — ask Claude: "Take a screenshot of https://example.com" — Claude should use `browser_navigate` then `browser_screenshot` and return the image

7. **Optional: Pin a version** — for reproducibility, pin to a specific version instead of `@latest`:

   ```json
   "args": ["@playwright/mcp@1.50.0"]
   ```

## Output Format

Step-by-step instructions with configuration JSON blocks. After setup confirmation, provide usage examples demonstrating what Claude can now do with browser control.

```
## Playwright MCP Setup

### 1. Install browsers
npx playwright install chromium

### 2. Configure claude_desktop_config.json
{
  "mcpServers": {
    "playwright": { "command": "npx", "args": ["@playwright/mcp@latest"] }
  }
}

### 3. Restart Claude Desktop

### 4. Verify
Ask Claude: "Take a screenshot of https://example.com"
Expected: Claude uses browser_navigate → browser_screenshot → returns image

### Available browser tools
browser_navigate, browser_click, browser_type, browser_screenshot,
browser_evaluate, browser_wait_for
```

## Rules

### Must
- Verify Node.js 18+ is installed before proceeding
- Provide platform-specific config file paths (macOS vs. Windows vs. Linux)
- Include the restart step — MCP servers only load on startup
- Provide a test command to verify the setup works
- Explain headed vs. headless mode trade-offs

### Never
- Recommend installing `@playwright/mcp` globally (`npm install -g`) — `npx` is the correct usage pattern
- Skip the restart step — a common setup failure is forgetting to restart Claude
- Configure MCP servers with hardcoded absolute paths to `npx` — use the command name so the shell resolves it from PATH
- Instruct users to run `@playwright/mcp` as a standalone server manually — Claude manages the server lifecycle

## Examples

### Good Example

User: "How do I give Claude browser control with Playwright MCP?"

Claude provides the full setup: installs Chromium via `npx playwright install chromium`, shows the exact JSON config for `claude_desktop_config.json` with the `npx @playwright/mcp@latest` command, explains headed vs. headless, instructs to restart Claude Desktop, and provides a test prompt to verify the tools are available.

### Bad Example

User: "Set up Playwright MCP."

Claude responds: "Install Playwright with `npm install playwright` and configure the MCP server."

> Why this is bad: Wrong package name (`@playwright/mcp` not `playwright`). No config JSON shown. No restart instruction. No verification step. The user still can't complete the setup from this response.
