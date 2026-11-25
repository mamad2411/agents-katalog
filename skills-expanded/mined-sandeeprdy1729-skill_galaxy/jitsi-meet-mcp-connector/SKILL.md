---
name: jitsi-meet-mcp-connector
description: "MCP connector for Jitsi Meet video conferencing – enables AI-powered meeting management, transcription, and conference control through Claude"
license: Apache 2.0
tags: ["dev","communication","mcp","jitsi","video"]
difficulty: intermediate
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Jitsi Meet MCP Connector

## Overview

This skill enables Claude to interact with **Jitsi Meet** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Jitsi Meet's REST API/SRTP, allowing natural language control of Jitsi Meet operations, intelligent automation, and AI-powered assistance for Jitsi Meet workflows.

## When to Use This Skill

- Meeting room creation and configuration
- Participant management and moderation
- Meeting transcription and summary generation
- Recording management and distribution
- Calendar integration and scheduling

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Jitsi Meet       │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (REST API/SRTP )│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Jitsi Meet operations as tools Claude can invoke. The server translates natural language intentions into REST API/SRTP calls.

### Key Endpoints/Interfaces

`/api/v1/rooms`, `/api/v1/conferences`, `/prosody http api`, `/jibri record`, `/jicofo stats`

### Implementation

```typescript
// Jitsi Meet MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "jitsi-meet-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Jitsi Meet resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Jitsi Meet REST API/SRTP
    const response = await fetch(`${BASE_URL}/api/v1/rooms`, {
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
  "Create a new resource in Jitsi Meet",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/api/v1/rooms`, {
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
  "AI-powered analysis of Jitsi Meet data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/api/v1/rooms`, {
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
    "jitsi-meet-mcp-connector": {
      "command": "node",
      "args": ["path/to/jitsi-meet-mcp-connector/index.js"],
      "env": {
        "JITSI_MEET_API_KEY": "your-api-key",
        "JITSI_MEET_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Jitsi Meet API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Jitsi Meet API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Schedule a team standup meeting for tomorrow at 10am with recording enabled and send invites"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Jitsi Meet Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
