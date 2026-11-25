---
name: chrome-devtools-setup
description: "Guidelines for installing and configuring the official Chrome DevTools MCP server across various clients."
---

# Chrome DevTools MCP Setup

The `chrome-devtools-mcp` server gives AI coding assistants the ability to natively control, inspect, and debug a live Google Chrome browser via the Model Context Protocol.

## Installation Configuration

To connect, add the following to your MCP client configuration (e.g., `.mcp.json` or `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

### Advanced Arguments
You can pass additional arguments in the `args` array to customize the server:
*   `--slim`: Runs in slim mode exposing only basic navigation and screenshot tools.
*   `--headless`: Runs the Chrome browser silently in the background without a UI.
*   `--isolated`: Creates a temporary `user-data-dir` that is destroyed when the browser closes, ensuring a clean session.
*   `--channel=canary`: Targets a specific Chrome release channel.
*   `--browserUrl=http://127.0.0.1:9222`: Connects the server to an *existing* running Chrome instance rather than launching a new one.

## Using with Claude Code
If you use Claude Code, you can install it seamlessly as a plugin which bundles both the MCP server and predefined prompt skills:
```bash
/plugin marketplace add ChromeDevTools/chrome-devtools-mcp
/plugin install chrome-devtools-mcp@chrome-devtools-plugins
```
