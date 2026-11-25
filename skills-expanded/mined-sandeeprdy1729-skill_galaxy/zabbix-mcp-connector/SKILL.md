---
name: zabbix-mcp-connector
description: "MCP connector for Zabbix network monitoring – enables AI-powered host management, trigger configuration, and event analysis through Claude"
license: AGPL
tags: ["cloud","monitoring","mcp","zabbix","network"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Zabbix MCP Connector

## Overview

This skill enables Claude to interact with **Zabbix** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Zabbix's JSON-RPC API, allowing natural language control of Zabbix operations, intelligent automation, and AI-powered assistance for Zabbix workflows.

## When to Use This Skill

- Host and template configuration via AI
- Trigger and action rule creation
- Event correlation and root cause analysis
- Dashboard and screen generation
- Maintenance window management

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Zabbix           │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (JSON-RPC API  )│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Zabbix operations as tools Claude can invoke. The server translates natural language intentions into JSON-RPC API calls.

### Key Endpoints/Interfaces

`host.create`, `trigger.create`, `event.get`, `template.create`, `dashboard.create`

### Implementation

```typescript
// Zabbix MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "zabbix-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Zabbix resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Zabbix JSON-RPC API
    const response = await fetch(`${BASE_URL}host.create`, {
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
  "Create a new resource in Zabbix",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}host.create`, {
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
  "AI-powered analysis of Zabbix data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}host.create`, {
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
    "zabbix-mcp-connector": {
      "command": "node",
      "args": ["path/to/zabbix-mcp-connector/index.js"],
      "env": {
        "ZABBIX_API_KEY": "your-api-key",
        "ZABBIX_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Zabbix API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Zabbix API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Set up monitoring for 10 web servers with disk, CPU, memory triggers and email escalation"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Zabbix Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
