---
name: nagios-mcp-connector
description: "MCP connector for Nagios infrastructure monitoring – enables AI-powered host/service monitoring, check configuration, and alerting through Claude"
license: GPL
tags: ["cloud","monitoring","mcp","nagios","infrastructure"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Nagios MCP Connector

## Overview

This skill enables Claude to interact with **Nagios** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Nagios's CGI/REST API, allowing natural language control of Nagios operations, intelligent automation, and AI-powered assistance for Nagios workflows.

## When to Use This Skill

- Host and service check configuration
- Check command and plugin development
- Contact and notification rule management
- Performance data analysis
- Configuration validation and deployment

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Nagios           │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (CGI/REST API  )│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Nagios operations as tools Claude can invoke. The server translates natural language intentions into CGI/REST API calls.

### Key Endpoints/Interfaces

`/nagiosxi/api/v1/objects`, `/nagiosxi/api/v1/status`, `/nagiosxi/api/v1/config`, `/nagiosxi/api/v1/system`

### Implementation

```typescript
// Nagios MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "nagios-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Nagios resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Nagios CGI/REST API
    const response = await fetch(`${BASE_URL}/nagiosxi/api/v1/objects`, {
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
  "Create a new resource in Nagios",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/nagiosxi/api/v1/objects`, {
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
  "AI-powered analysis of Nagios data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/nagiosxi/api/v1/objects`, {
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
    "nagios-mcp-connector": {
      "command": "node",
      "args": ["path/to/nagios-mcp-connector/index.js"],
      "env": {
        "NAGIOS_API_KEY": "your-api-key",
        "NAGIOS_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Nagios API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Nagios API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Configure service checks for HTTP, SSL certificate expiry, and disk space on all web servers"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Nagios Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
