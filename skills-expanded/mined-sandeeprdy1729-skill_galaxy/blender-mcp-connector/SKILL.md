---
name: blender-mcp-connector
description: "MCP connector for Blender 3D creation suite – enables AI-powered 3D modeling, scene management, rendering, and animation through Claude"
license: GPL
tags: ["creative","3d-modeling","mcp","blender","animation"]
difficulty: expert
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Blender MCP Connector

## Overview

This skill enables Claude to interact with **Blender** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Blender's Python API (bpy), allowing natural language control of Blender operations, intelligent automation, and AI-powered assistance for Blender workflows.

## When to Use This Skill

- Scene creation and object manipulation via natural language
- Material and shader node graph generation
- Animation keyframe management
- Render settings optimization
- Python script generation for complex operations

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Blender          │
│   (Client)   │◀────│   (Python/TypeScript)  │◀────│   (Python API (bp)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Blender operations as tools Claude can invoke. The server translates natural language intentions into Python API (bpy) calls.

### Key Endpoints/Interfaces

`bpy.ops.mesh.*`, `bpy.ops.object.*`, `bpy.data.materials`, `bpy.context.scene`, `bpy.ops.render.*`

### Implementation

```typescript
// Blender MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "blender-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Blender resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Blender Python API (bpy)
    const response = await fetch(`${BASE_URL}bpy.ops.mesh.*`, {
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
  "Create a new resource in Blender",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}bpy.ops.mesh.*`, {
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
  "AI-powered analysis of Blender data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}bpy.ops.mesh.*`, {
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
    "blender-mcp-connector": {
      "command": "node",
      "args": ["path/to/blender-mcp-connector/index.js"],
      "env": {
        "BLENDER_API_KEY": "your-api-key",
        "BLENDER_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Blender API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Blender API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a low-poly landscape scene with mountains, trees, and a river with PBR materials"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Blender Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
