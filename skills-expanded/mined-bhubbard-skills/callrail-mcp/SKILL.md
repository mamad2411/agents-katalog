---
name: callrail-mcp
description: Integrating CallRail with AI assistants using the Model Context Protocol (MCP) server.
---

# CallRail Model Context Protocol (MCP) Server

## Overview
The CallRail MCP Server allows AI assistants (like Claude Desktop or other MCP-compatible agents) to interact with your CallRail data using natural language. It acts as a bridge, giving the AI specific "tools" to retrieve call logs, transcripts, and marketing attribution data.

## Connection Options
1. **Third-Party Integrations**: Platforms like Zapier or Adzviser offer pre-built MCP servers that connect CallRail to AI tools without code.
2. **Open Source/Custom**: Open-source implementations (e.g., `pghdma/callrail-mcp` on PyPI) allow you to host the server yourself and interact with the CallRail REST API v3.

## Key Features
- **Natural Language Analysis**: Ask questions like "Summarize my missed calls from today" in plain English.
- **Operational Tools**: Tools to create caller IDs, retrieve SMS threads, or update call notes.
- **Secure Access**: Authenticates via OAuth 2.0 or API keys, ensuring data access is scoped correctly.

## Configuration (Claude Desktop Example)
If hosting locally, add the server to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "callrail": {
      "command": "uvx",
      "args": ["callrail-mcp"],
      "env": {
        "CALLRAIL_API_KEY": "YOUR_API_KEY",
        "CALLRAIL_ACCOUNT_ID": "YOUR_ACCOUNT_ID"
      }
    }
  }
}
```

## Best Practices
- Provide precise context when prompting the AI so it uses the MCP tools effectively (e.g., specifying dates or company IDs).
- Only provide the AI with the permissions necessary for its tasks.
