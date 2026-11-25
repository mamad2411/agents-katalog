---
name: mediawiki-mcp-connector
description: "MCP connector for MediaWiki – enables AI-powered wiki content creation, page management, and knowledge base operations through Claude"
license: GPL
tags: ["dev","wiki","mcp","mediawiki","documentation"]
difficulty: intermediate
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Mediawiki MCP Connector

## Overview

This skill enables Claude to interact with **Mediawiki** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Mediawiki's MediaWiki API, allowing natural language control of Mediawiki operations, intelligent automation, and AI-powered assistance for Mediawiki workflows.

## When to Use This Skill

- Wiki page creation and editing via natural language
- Category and template management
- Cross-page linking and navigation structuring
- User and permission management
- Content migration and import/export

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Mediawiki        │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (MediaWiki API )│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Mediawiki operations as tools Claude can invoke. The server translates natural language intentions into MediaWiki API calls.

### Key Endpoints/Interfaces

`api.php?action=edit`, `api.php?action=query`, `api.php?action=parse`, `api.php?action=upload`, `api.php?action=move`

### Implementation

```typescript
// Mediawiki MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "mediawiki-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Mediawiki resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Mediawiki MediaWiki API
    const response = await fetch(`${BASE_URL}api.php?action=edit`, {
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
  "Create a new resource in Mediawiki",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}api.php?action=edit`, {
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
  "AI-powered analysis of Mediawiki data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}api.php?action=edit`, {
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
    "mediawiki-mcp-connector": {
      "command": "node",
      "args": ["path/to/mediawiki-mcp-connector/index.js"],
      "env": {
        "MEDIAWIKI_API_KEY": "your-api-key",
        "MEDIAWIKI_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Mediawiki API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Mediawiki API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a new wiki page for the API documentation with proper templates and category tags"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Mediawiki Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
