---
name: spyder-ide-mcp-connector
description: "MCP connector for Spyder scientific Python IDE – enables AI-powered scientific computing, variable exploration, and debugging through Claude"
license: MIT
tags: ["data","python","mcp","spyder","science"]
difficulty: intermediate
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Spyder Ide MCP Connector

## Overview

This skill enables Claude to interact with **Spyder Ide** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Spyder Ide's Plugin API/IPython, allowing natural language control of Spyder Ide operations, intelligent automation, and AI-powered assistance for Spyder Ide workflows.

## When to Use This Skill

- Scientific Python script generation
- Variable explorer and data frame analysis
- IPython console integration
- Profiling and optimization assistance
- Plugin and configuration management

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Spyder Ide       │
│   (Client)   │◀────│   (Python/TypeScript)  │◀────│   (Plugin API/IPy)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Spyder Ide operations as tools Claude can invoke. The server translates natural language intentions into Plugin API/IPython calls.

### Key Endpoints/Interfaces

`spyder.api.plugins`, `IPython.kernel`, `spyder.config`, `spyder.editor`, `spyder.explorer`

### Implementation

```typescript
// Spyder Ide MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "spyder-ide-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Spyder Ide resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Spyder Ide Plugin API/IPython
    const response = await fetch(`${BASE_URL}spyder.api.plugins`, {
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
  "Create a new resource in Spyder Ide",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}spyder.api.plugins`, {
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
  "AI-powered analysis of Spyder Ide data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}spyder.api.plugins`, {
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
    "spyder-ide-mcp-connector": {
      "command": "node",
      "args": ["path/to/spyder-ide-mcp-connector/index.js"],
      "env": {
        "SPYDER_IDE_API_KEY": "your-api-key",
        "SPYDER_IDE_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Spyder Ide API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Spyder Ide API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a data analysis script that loads a CSV, performs statistical tests, and generates publication-quality plots"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Spyder Ide Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
