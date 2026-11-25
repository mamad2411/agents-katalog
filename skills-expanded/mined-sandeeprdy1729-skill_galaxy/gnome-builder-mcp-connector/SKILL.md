---
name: gnome-builder-mcp-connector
description: "MCP connector for GNOME Builder IDE – enables AI-assisted GNOME/GTK application development, Flatpak integration, and Meson build management through Claude"
license: GPL
tags: ["dev","ide","mcp","gnome","gtk","flatpak"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Gnome Builder MCP Connector

## Overview

This skill enables Claude to interact with **Gnome Builder** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Gnome Builder's D-Bus/CLI, allowing natural language control of Gnome Builder operations, intelligent automation, and AI-powered assistance for Gnome Builder workflows.

## When to Use This Skill

- Flatpak manifest generation and configuration
- Meson build system setup and management
- GTK widget hierarchy analysis
- GNOME API usage suggestions and migration help
- Application packaging and distribution

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Gnome Builder    │
│   (Client)   │◀────│   (Python/TypeScript)  │◀────│   (D-Bus/CLI     )│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Gnome Builder operations as tools Claude can invoke. The server translates natural language intentions into D-Bus/CLI calls.

### Key Endpoints/Interfaces

`org.gnome.Builder`, `flatpak-builder`, `meson setup`, `gtk-inspector`

### Implementation

```typescript
// Gnome Builder MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "gnome-builder-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Gnome Builder resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Gnome Builder D-Bus/CLI
    const response = await fetch(`${BASE_URL}org.gnome.Builder`, {
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
  "Create a new resource in Gnome Builder",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}org.gnome.Builder`, {
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
  "AI-powered analysis of Gnome Builder data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}org.gnome.Builder`, {
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
    "gnome-builder-mcp-connector": {
      "command": "node",
      "args": ["path/to/gnome-builder-mcp-connector/index.js"],
      "env": {
        "GNOME_BUILDER_API_KEY": "your-api-key",
        "GNOME_BUILDER_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Gnome Builder API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Gnome Builder API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a new GTK4 application with Flatpak manifest and Meson build system"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Gnome Builder Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
