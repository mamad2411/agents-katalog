---
name: openvas-mcp-connector
description: "MCP connector for OpenVAS vulnerability scanner – enables AI-powered vulnerability scanning, report analysis, and remediation planning through Claude"
license: GPL
tags: ["security","vulnerability","mcp","openvas","scanning"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Openvas MCP Connector

## Overview

This skill enables Claude to interact with **Openvas** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Openvas's GMP (Greenbone Management Protocol), allowing natural language control of Openvas operations, intelligent automation, and AI-powered assistance for Openvas workflows.

## When to Use This Skill

- Scan target and task configuration via AI
- Vulnerability report analysis and prioritization
- Remediation plan generation from scan results
- Scan scheduling and policy management
- Compliance audit configuration

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Openvas          │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (GMP (Greenbone)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Openvas operations as tools Claude can invoke. The server translates natural language intentions into GMP (Greenbone Management Protocol) calls.

### Key Endpoints/Interfaces

`create_target`, `create_task`, `start_task`, `get_results`, `get_reports`

### Implementation

```typescript
// Openvas MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "openvas-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Openvas resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Openvas GMP (Greenbone Management Protocol)
    const response = await fetch(`${BASE_URL}create_target`, {
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
  "Create a new resource in Openvas",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}create_target`, {
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
  "AI-powered analysis of Openvas data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}create_target`, {
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
    "openvas-mcp-connector": {
      "command": "node",
      "args": ["path/to/openvas-mcp-connector/index.js"],
      "env": {
        "OPENVAS_API_KEY": "your-api-key",
        "OPENVAS_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Openvas API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Openvas API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Run a full vulnerability scan on the production subnet and generate a prioritized remediation report"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Openvas Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
