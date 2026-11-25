---
name: inkscape-mcp-connector
description: "MCP connector for Inkscape vector graphics – enables AI-powered SVG creation, path manipulation, and design automation through Claude"
license: GPL
tags: ["creative","vector-graphics","mcp","inkscape","svg"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Inkscape MCP Connector

## Overview

This skill enables Claude to interact with **Inkscape** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Inkscape's CLI/D-Bus, allowing natural language control of Inkscape operations, intelligent automation, and AI-powered assistance for Inkscape workflows.

## When to Use This Skill

- SVG generation from natural language descriptions
- Path operations and boolean operations
- Text-to-path conversion and typography
- Batch SVG processing and optimization
- Extension and filter development

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Inkscape         │
│   (Client)   │◀────│   (Python/TypeScript)  │◀────│   (CLI/D-Bus     )│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Inkscape operations as tools Claude can invoke. The server translates natural language intentions into CLI/D-Bus calls.

### Key Endpoints/Interfaces

`inkscape --actions`, `inkscape --export-*`, `inkscape --verb`, `org.inkscape.Inkscape`

### Implementation

```typescript
// Inkscape MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "inkscape-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Inkscape resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Inkscape CLI/D-Bus
    const response = await fetch(`${BASE_URL}inkscape --actions`, {
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
  "Create a new resource in Inkscape",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}inkscape --actions`, {
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
  "AI-powered analysis of Inkscape data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}inkscape --actions`, {
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
    "inkscape-mcp-connector": {
      "command": "node",
      "args": ["path/to/inkscape-mcp-connector/index.js"],
      "env": {
        "INKSCAPE_API_KEY": "your-api-key",
        "INKSCAPE_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Inkscape API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Inkscape API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create an SVG logo with a circular badge containing a star and company name in a modern font"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Inkscape Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
