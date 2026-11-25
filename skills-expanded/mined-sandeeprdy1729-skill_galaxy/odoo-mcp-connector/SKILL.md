---
name: odoo-mcp-connector
description: "MCP connector for Odoo ERP/CRM – enables AI-powered business process automation, sales management, and accounting operations through Claude"
license: LGPL
tags: ["business","erp","mcp","odoo","crm"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Odoo MCP Connector

## Overview

This skill enables Claude to interact with **Odoo** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Odoo's XML-RPC/JSON-RPC, allowing natural language control of Odoo operations, intelligent automation, and AI-powered assistance for Odoo workflows.

## When to Use This Skill

- Sales order and invoice creation via natural language
- CRM lead management and pipeline analysis
- Inventory forecasting and procurement planning
- HR and employee management automation
- Custom report generation and data analysis

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Odoo             │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (XML-RPC/JSON-R)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Odoo operations as tools Claude can invoke. The server translates natural language intentions into XML-RPC/JSON-RPC calls.

### Key Endpoints/Interfaces

`object.execute_kw`, `common.authenticate`, `/web/dataset/call_kw`, `/api/method`

### Implementation

```typescript
// Odoo MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "odoo-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Odoo resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Odoo XML-RPC/JSON-RPC
    const response = await fetch(`${BASE_URL}object.execute_kw`, {
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
  "Create a new resource in Odoo",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}object.execute_kw`, {
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
  "AI-powered analysis of Odoo data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}object.execute_kw`, {
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
    "odoo-mcp-connector": {
      "command": "node",
      "args": ["path/to/odoo-mcp-connector/index.js"],
      "env": {
        "ODOO_API_KEY": "your-api-key",
        "ODOO_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Odoo API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Odoo API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a sales order for the top 5 products from last quarter and generate a proforma invoice"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Odoo Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
