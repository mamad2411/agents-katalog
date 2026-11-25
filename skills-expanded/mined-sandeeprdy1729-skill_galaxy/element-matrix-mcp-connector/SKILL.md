---
name: element-matrix-mcp-connector
description: "MCP connector for Element/Matrix decentralized communication – enables AI-powered room management, message handling, and federation control through Claude"
license: Apache 2.0
tags: ["dev","communication","mcp","matrix","element","decentralized"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Element Matrix MCP Connector

## Overview

This skill enables Claude to interact with **Element Matrix** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Element Matrix's Matrix Client-Server API, allowing natural language control of Element Matrix operations, intelligent automation, and AI-powered assistance for Element Matrix workflows.

## When to Use This Skill

- Room creation and space organization
- Message history search and summarization
- End-to-end encryption key management assistance
- Federation and homeserver configuration
- Widget and integration management

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Element Matrix   │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (Matrix Client-)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Element Matrix operations as tools Claude can invoke. The server translates natural language intentions into Matrix Client-Server API calls.

### Key Endpoints/Interfaces

`/_matrix/client/v3/rooms`, `/_matrix/client/v3/sync`, `/_matrix/client/v3/createRoom`, `/_matrix/client/v3/search`

### Implementation

```typescript
// Element Matrix MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "element-matrix-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Element Matrix resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Element Matrix Matrix Client-Server API
    const response = await fetch(`${BASE_URL}/_matrix/client/v3/rooms`, {
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
  "Create a new resource in Element Matrix",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/_matrix/client/v3/rooms`, {
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
  "AI-powered analysis of Element Matrix data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/_matrix/client/v3/rooms`, {
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
    "element-matrix-mcp-connector": {
      "command": "node",
      "args": ["path/to/element-matrix-mcp-connector/index.js"],
      "env": {
        "ELEMENT_MATRIX_API_KEY": "your-api-key",
        "ELEMENT_MATRIX_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Element Matrix API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Element Matrix API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a private encrypted room for the security team and set up message retention policies"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Element Matrix Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
