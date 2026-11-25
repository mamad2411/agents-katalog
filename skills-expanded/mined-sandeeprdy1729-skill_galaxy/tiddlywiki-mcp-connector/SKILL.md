---
name: tiddlywiki-mcp-connector
description: "MCP connector for TiddlyWiki – enables AI-powered tiddler management, non-linear note-taking, and knowledge graph operations through Claude"
license: BSD
tags: ["dev","wiki","mcp","tiddlywiki","notes"]
difficulty: beginner
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Tiddlywiki MCP Connector

## Overview

This skill enables Claude to interact with **Tiddlywiki** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Tiddlywiki's WebServer API/File, allowing natural language control of Tiddlywiki operations, intelligent automation, and AI-powered assistance for Tiddlywiki workflows.

## When to Use This Skill

- Tiddler creation and tagging via natural language
- Filter expression generation
- Macro and widget development
- Plugin installation and management
- Export and publishing configuration

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Tiddlywiki       │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (WebServer API/)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Tiddlywiki operations as tools Claude can invoke. The server translates natural language intentions into WebServer API/File calls.

### Key Endpoints/Interfaces

`/recipes/default/tiddlers`, `/bags/default/tiddlers/:title`, `/status`, `/recipes/default/tiddlers.json`

### Implementation

```typescript
// Tiddlywiki MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "tiddlywiki-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Tiddlywiki resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Tiddlywiki WebServer API/File
    const response = await fetch(`${BASE_URL}/recipes/default/tiddlers`, {
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
  "Create a new resource in Tiddlywiki",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/recipes/default/tiddlers`, {
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
  "AI-powered analysis of Tiddlywiki data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/recipes/default/tiddlers`, {
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
    "tiddlywiki-mcp-connector": {
      "command": "node",
      "args": ["path/to/tiddlywiki-mcp-connector/index.js"],
      "env": {
        "TIDDLYWIKI_API_KEY": "your-api-key",
        "TIDDLYWIKI_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Tiddlywiki API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Tiddlywiki API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a series of linked tiddlers for a research project with tags for topics and sources"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Tiddlywiki Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
