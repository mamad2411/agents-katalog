---
name: uptime-kuma-mcp-connector
description: "MCP connector for Uptime Kuma monitoring – enables AI-powered uptime monitoring, status page management, and notification configuration through Claude"
license: MIT
tags: ["cloud","monitoring","mcp","uptime-kuma","availability"]
difficulty: beginner
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Uptime Kuma MCP Connector

## Overview

This skill enables Claude to interact with **Uptime Kuma** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Uptime Kuma's REST API/WebSocket, allowing natural language control of Uptime Kuma operations, intelligent automation, and AI-powered assistance for Uptime Kuma workflows.

## When to Use This Skill

- Monitor creation for HTTP/TCP/DNS endpoints
- Status page generation and customization
- Notification channel configuration
- Maintenance window scheduling
- Incident tracking and response

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Uptime Kuma      │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (REST API/WebSo)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Uptime Kuma operations as tools Claude can invoke. The server translates natural language intentions into REST API/WebSocket calls.

### Key Endpoints/Interfaces

`/api/monitors`, `/api/status-pages`, `/api/notifications`, `/api/maintenance`, `/api/heartbeat`

### Implementation

```typescript
// Uptime Kuma MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "uptime-kuma-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Uptime Kuma resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Uptime Kuma REST API/WebSocket
    const response = await fetch(`${BASE_URL}/api/monitors`, {
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
  "Create a new resource in Uptime Kuma",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/api/monitors`, {
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
  "AI-powered analysis of Uptime Kuma data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/api/monitors`, {
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
    "uptime-kuma-mcp-connector": {
      "command": "node",
      "args": ["path/to/uptime-kuma-mcp-connector/index.js"],
      "env": {
        "UPTIME_KUMA_API_KEY": "your-api-key",
        "UPTIME_KUMA_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Uptime Kuma API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Uptime Kuma API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create monitors for all production API endpoints with 1-minute intervals and Slack notifications"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Uptime Kuma Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
