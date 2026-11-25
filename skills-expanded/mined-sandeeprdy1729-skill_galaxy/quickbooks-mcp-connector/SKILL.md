---
name: quickbooks-mcp-connector
description: "MCP connector for QuickBooks – enables AI-powered accounting, invoice management, and financial reporting through Claude"
license: Proprietary/API
tags: ["business","accounting","mcp","quickbooks","finance"]
difficulty: intermediate
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Quickbooks MCP Connector

## Overview

This skill enables Claude to interact with **Quickbooks** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Quickbooks's REST API (OAuth 2.0), allowing natural language control of Quickbooks operations, intelligent automation, and AI-powered assistance for Quickbooks workflows.

## When to Use This Skill

- Invoice creation and payment tracking
- Expense categorization and reporting
- Customer and vendor management
- Tax preparation and compliance
- Cash flow analysis and forecasting

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Quickbooks       │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (REST API (OAut)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Quickbooks operations as tools Claude can invoke. The server translates natural language intentions into REST API (OAuth 2.0) calls.

### Key Endpoints/Interfaces

`/v3/company/:id/invoice`, `/v3/company/:id/customer`, `/v3/company/:id/account`, `/v3/company/:id/reports`

### Implementation

```typescript
// Quickbooks MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "quickbooks-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Quickbooks resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Quickbooks REST API (OAuth 2.0)
    const response = await fetch(`${BASE_URL}/v3/company/:id/invoice`, {
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
  "Create a new resource in Quickbooks",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/v3/company/:id/invoice`, {
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
  "AI-powered analysis of Quickbooks data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/v3/company/:id/invoice`, {
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
    "quickbooks-mcp-connector": {
      "command": "node",
      "args": ["path/to/quickbooks-mcp-connector/index.js"],
      "env": {
        "QUICKBOOKS_API_KEY": "your-api-key",
        "QUICKBOOKS_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Quickbooks API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Quickbooks API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create invoices for all time entries from last week and send payment reminders for overdue invoices"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Quickbooks Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
