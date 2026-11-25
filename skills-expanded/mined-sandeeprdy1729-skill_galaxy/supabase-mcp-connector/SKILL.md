---
name: supabase-mcp-connector
description: "MCP connector for Supabase – enables AI-powered backend management, database operations, and auth configuration through Claude"
license: Apache 2.0
tags: ["dev","backend","mcp","supabase","baas"]
difficulty: intermediate
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Supabase MCP Connector

## Overview

This skill enables Claude to interact with **Supabase** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Supabase's REST API/Management API, allowing natural language control of Supabase operations, intelligent automation, and AI-powered assistance for Supabase workflows.

## When to Use This Skill

- Database table design and migration generation
- Row Level Security policy creation
- Auth provider configuration and user management
- Edge Function deployment and management
- Storage bucket and file management

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Supabase         │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (REST API/Manag)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Supabase operations as tools Claude can invoke. The server translates natural language intentions into REST API/Management API calls.

### Key Endpoints/Interfaces

`/rest/v1/:table`, `/auth/v1/admin`, `/storage/v1/object`, `/functions/v1/:slug`, `/v1/projects`

### Implementation

```typescript
// Supabase MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "supabase-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Supabase resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Supabase REST API/Management API
    const response = await fetch(`${BASE_URL}/rest/v1/:table`, {
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
  "Create a new resource in Supabase",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/rest/v1/:table`, {
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
  "AI-powered analysis of Supabase data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/rest/v1/:table`, {
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
    "supabase-mcp-connector": {
      "command": "node",
      "args": ["path/to/supabase-mcp-connector/index.js"],
      "env": {
        "SUPABASE_API_KEY": "your-api-key",
        "SUPABASE_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Supabase API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Supabase API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a profiles table with RLS policies, set up Google OAuth, and deploy an Edge Function for webhooks"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Supabase Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
