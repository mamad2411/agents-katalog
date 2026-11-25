---
name: ghost-mcp-connector
description: "MCP connector for Ghost publishing platform – enables AI-powered content creation, newsletter management, and member administration through Claude"
license: MIT
tags: ["writing","blogging","mcp","ghost","publishing"]
difficulty: intermediate
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Ghost MCP Connector

## Overview

This skill enables Claude to interact with **Ghost** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Ghost's Admin API/Content API, allowing natural language control of Ghost operations, intelligent automation, and AI-powered assistance for Ghost workflows.

## When to Use This Skill

- Post creation and scheduling via natural language
- Newsletter campaign management
- Member and subscription management
- Theme and design customization
- SEO optimization and metadata management

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Ghost            │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (Admin API/Cont)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Ghost operations as tools Claude can invoke. The server translates natural language intentions into Admin API/Content API calls.

### Key Endpoints/Interfaces

`/ghost/api/admin/posts`, `/ghost/api/admin/members`, `/ghost/api/admin/newsletters`, `/ghost/api/admin/tags`, `/ghost/api/content/posts`

### Implementation

```typescript
// Ghost MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "ghost-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Ghost resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Ghost Admin API/Content API
    const response = await fetch(`${BASE_URL}/ghost/api/admin/posts`, {
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
  "Create a new resource in Ghost",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/ghost/api/admin/posts`, {
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
  "AI-powered analysis of Ghost data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/ghost/api/admin/posts`, {
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
    "ghost-mcp-connector": {
      "command": "node",
      "args": ["path/to/ghost-mcp-connector/index.js"],
      "env": {
        "GHOST_API_KEY": "your-api-key",
        "GHOST_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Ghost API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Ghost API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a blog post series on AI fundamentals with SEO-optimized titles and schedule weekly publication"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Ghost Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
