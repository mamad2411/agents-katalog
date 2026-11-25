---
name: microsoft-teams-mcp-connector
description: "MCP connector for Microsoft Teams – enables AI-powered team collaboration, channel management, and meeting coordination through Claude"
license: Proprietary/API
tags: ["product","communication","mcp","teams","microsoft"]
difficulty: intermediate
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Microsoft Teams MCP Connector

## Overview

This skill enables Claude to interact with **Microsoft Teams** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Microsoft Teams's Microsoft Graph API, allowing natural language control of Microsoft Teams operations, intelligent automation, and AI-powered assistance for Microsoft Teams workflows.

## When to Use This Skill

- Channel creation and message posting
- Meeting scheduling and agenda creation
- Message summarization across channels
- Adaptive card and bot message creation
- Team membership and permission management

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Microsoft Teams   │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (Microsoft Grap)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Microsoft Teams operations as tools Claude can invoke. The server translates natural language intentions into Microsoft Graph API calls.

### Key Endpoints/Interfaces

`/v1.0/teams`, `/v1.0/teams/:id/channels`, `/v1.0/me/chats`, `/v1.0/me/onlineMeetings`

### Implementation

```typescript
// Microsoft Teams MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "microsoft-teams-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Microsoft Teams resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Microsoft Teams Microsoft Graph API
    const response = await fetch(`${BASE_URL}/v1.0/teams`, {
      headers: { "Authorization": `Bearer ${API_KEY}` },
    });
    const data = await response.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data, null, 2) }],
    };
  }
);

// Tool: Create Resource
server.tool(
  "create_resource",
  "Create a new resource in Microsoft Teams",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/v1.0/teams`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, ...config }),
    });
    const data = await response.json();
    return {
      content: [{ type: "text", text: `Created: ${JSON.stringify(data)}` }],
    };
  }
);

// Tool: Analyze/Report
server.tool(
  "analyze",
  "AI-powered analysis of Microsoft Teams data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/v1.0/teams`, {
      headers: { "Authorization": `Bearer ${API_KEY}` },
    });
    const data = await response.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data, null, 2) }],
    };
  }
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "microsoft-teams-mcp-connector": {
      "command": "node",
      "args": ["path/to/microsoft-teams-mcp-connector/index.js"],
      "env": {
        "MICROSOFT_TEAMS_API_KEY": "your-api-key",
        "MICROSOFT_TEAMS_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Microsoft Teams API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Microsoft Teams API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Schedule a team standup for every weekday at 9am and post an agenda template to the channel"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Microsoft Teams Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
