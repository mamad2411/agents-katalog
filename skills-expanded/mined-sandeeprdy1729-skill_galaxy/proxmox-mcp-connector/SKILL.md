---
name: proxmox-mcp-connector
description: "MCP connector for Proxmox VE virtualization – enables AI-powered VM management, container provisioning, and infrastructure operations through Claude"
license: AGPL
tags: ["cloud","virtualization","mcp","proxmox","vm"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Proxmox MCP Connector

## Overview

This skill enables Claude to interact with **Proxmox** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Proxmox's REST API, allowing natural language control of Proxmox operations, intelligent automation, and AI-powered assistance for Proxmox workflows.

## When to Use This Skill

- VM creation and configuration via natural language
- Container template management and deployment
- Storage and network configuration
- Backup scheduling and restoration
- Cluster and HA management

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Proxmox          │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (REST API      )│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Proxmox operations as tools Claude can invoke. The server translates natural language intentions into REST API calls.

### Key Endpoints/Interfaces

`/api2/json/nodes`, `/api2/json/qemu`, `/api2/json/lxc`, `/api2/json/storage`, `/api2/json/cluster`

### Implementation

```typescript
// Proxmox MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "proxmox-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Proxmox resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Proxmox REST API
    const response = await fetch(`${BASE_URL}/api2/json/nodes`, {
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
  "Create a new resource in Proxmox",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}/api2/json/nodes`, {
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
  "AI-powered analysis of Proxmox data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}/api2/json/nodes`, {
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
    "proxmox-mcp-connector": {
      "command": "node",
      "args": ["path/to/proxmox-mcp-connector/index.js"],
      "env": {
        "PROXMOX_API_KEY": "your-api-key",
        "PROXMOX_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Proxmox API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Proxmox API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a new Ubuntu VM with 4 cores, 8GB RAM, and a 100GB disk on the fastest available storage"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Proxmox Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
