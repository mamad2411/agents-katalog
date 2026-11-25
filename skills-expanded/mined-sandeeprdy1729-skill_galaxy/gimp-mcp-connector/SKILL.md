---
name: gimp-mcp-connector
description: "MCP connector for GIMP image editor – enables AI-powered image editing, filter application, batch processing, and script generation through Claude"
license: GPL
tags: ["creative","image-editing","mcp","gimp"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Gimp MCP Connector

## Overview

This skill enables Claude to interact with **Gimp** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Gimp's Script-Fu/Python-Fu, allowing natural language control of Gimp operations, intelligent automation, and AI-powered assistance for Gimp workflows.

## When to Use This Skill

- Script-Fu and Python-Fu script generation
- Batch image processing and transformation
- Filter chain creation and application
- Layer management and composition
- Color correction and retouching automation

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Gimp             │
│   (Client)   │◀────│   (Python/TypeScript)  │◀────│   (Script-Fu/Pyth)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Gimp operations as tools Claude can invoke. The server translates natural language intentions into Script-Fu/Python-Fu calls.

### Key Endpoints/Interfaces

`gimp-script-fu-console`, `pdb.gimp_image_*`, `pdb.gimp_layer_*`, `pdb.gimp_edit_*`, `pdb.gimp_file_*`

### Implementation

```typescript
// Gimp MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "gimp-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Gimp resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Gimp Script-Fu/Python-Fu
    const response = await fetch(`${BASE_URL}gimp-script-fu-console`, {
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
  "Create a new resource in Gimp",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}gimp-script-fu-console`, {
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
  "AI-powered analysis of Gimp data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}gimp-script-fu-console`, {
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
    "gimp-mcp-connector": {
      "command": "node",
      "args": ["path/to/gimp-mcp-connector/index.js"],
      "env": {
        "GIMP_API_KEY": "your-api-key",
        "GIMP_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Gimp API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Gimp API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Batch resize all PNG images in a folder to 1200x630 with a watermark overlay"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Gimp Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
