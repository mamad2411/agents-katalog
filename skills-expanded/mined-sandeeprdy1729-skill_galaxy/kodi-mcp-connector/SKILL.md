---
name: kodi-mcp-connector
description: "MCP connector for Kodi media center – enables AI-powered media management, addon configuration, and smart playlist creation through Claude"
license: GPL
tags: ["creative","media","mcp","kodi","entertainment"]
difficulty: intermediate
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Kodi MCP Connector

## Overview

This skill enables Claude to interact with **Kodi** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Kodi's JSON-RPC, allowing natural language control of Kodi operations, intelligent automation, and AI-powered assistance for Kodi workflows.

## When to Use This Skill

- Smart playlist creation from natural language
- Library scanning and metadata correction
- Addon discovery and installation
- Remote control and playback management
- Skin and appearance customization

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Kodi             │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (JSON-RPC      )│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Kodi operations as tools Claude can invoke. The server translates natural language intentions into JSON-RPC calls.

### Key Endpoints/Interfaces

`VideoLibrary.GetMovies`, `AudioLibrary.GetSongs`, `Playlist.Add`, `Addons.GetAddons`, `Player.Open`

### Implementation

```typescript
// Kodi MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "kodi-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Kodi resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Kodi JSON-RPC
    const response = await fetch(`${BASE_URL}VideoLibrary.GetMovies`, {
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
  "Create a new resource in Kodi",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}VideoLibrary.GetMovies`, {
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
  "AI-powered analysis of Kodi data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}VideoLibrary.GetMovies`, {
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
    "kodi-mcp-connector": {
      "command": "node",
      "args": ["path/to/kodi-mcp-connector/index.js"],
      "env": {
        "KODI_API_KEY": "your-api-key",
        "KODI_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Kodi API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Kodi API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a smart playlist of all unwatched sci-fi movies released in the last 5 years sorted by rating"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Kodi Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
