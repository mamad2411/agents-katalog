---
name: erpnext-mcp-connector
description: "MCP connector for ERPNext – enables AI-powered business management, workflow automation, and reporting through Claude"
license: GPL
tags: ["business","erp","mcp","erpnext","frappe"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Erpnext MCP Connector

## Overview

This skill enables Claude to interact with **Erpnext** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Erpnext's REST API (Frappe), allowing natural language control of Erpnext operations, intelligent automation, and AI-powered assistance for Erpnext workflows.

## When to Use This Skill

- Document creation and workflow management via AI
- Financial report generation and analysis
- Supply chain and inventory management
- HR module operations and payroll processing
- Custom doctype and script development

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Erpnext          │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (REST API (Frap)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Erpnext operations as tools Claude can invoke. The server translates natural language intentions into REST API (Frappe) calls.

### Key Endpoints/Interfaces

`/api/resource/:doctype`, `/api/method/:method`, `/api/resource/:doctype/:name`, `/api/method/frappe.client.*`

### Implementation

```typescript
// Erpnext MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "erpnext-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Erpnext resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Erpnext REST API (Frappe)
    const response = await fetch(`${BASE_URL}/api/resource/:doctype`, {
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
  "Create a new resource in Erpnext",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/api/resource/:doctype`, {
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
  "AI-powered analysis of Erpnext data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/api/resource/:doctype`, {
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
    "erpnext-mcp-connector": {
      "command": "node",
      "args": ["path/to/erpnext-mcp-connector/index.js"],
      "env": {
        "ERPNEXT_API_KEY": "your-api-key",
        "ERPNEXT_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Erpnext API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Erpnext API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Generate a monthly P&L report and identify the top 3 expense categories with year-over-year growth"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Erpnext Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
