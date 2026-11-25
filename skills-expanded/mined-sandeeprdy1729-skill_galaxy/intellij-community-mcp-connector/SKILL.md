---
name: intellij-community-mcp-connector
description: "MCP connector for IntelliJ IDEA Community Edition – enables AI-assisted Java/Kotlin development, refactoring, inspections, and project management through Claude"
license: Apache 2.0
tags: ["dev","ide","mcp","intellij","java"]
difficulty: advanced
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Intellij Community MCP Connector

## Overview

This skill enables Claude to interact with **Intellij Community** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Intellij Community's Plugin API, allowing natural language control of Intellij Community operations, intelligent automation, and AI-powered assistance for Intellij Community workflows.

## When to Use This Skill

- AI-driven code inspections and refactoring suggestions
- Project structure analysis and dependency management
- Run configuration generation and test execution
- Code generation with IntelliJ's PSI tree awareness
- Build tool integration (Maven/Gradle) through Claude

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Intellij Community   │
│   (Client)   │◀────│   (Kotlin/Java)  │◀────│   (Plugin API    )│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Intellij Community operations as tools Claude can invoke. The server translates natural language intentions into Plugin API calls.

### Key Endpoints/Interfaces

`PSI tree access`, `InspectionManager`, `RefactoringActionHandler`, `RunManager`, `ProjectManager`

### Implementation

```typescript
// Intellij Community MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "intellij-community-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Intellij Community resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Intellij Community Plugin API
    const response = await fetch(`${BASE_URL}PSI tree access`, {
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
  "Create a new resource in Intellij Community",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}PSI tree access`, {
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
  "AI-powered analysis of Intellij Community data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}PSI tree access`, {
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
    "intellij-community-mcp-connector": {
      "command": "node",
      "args": ["path/to/intellij-community-mcp-connector/index.js"],
      "env": {
        "INTELLIJ_COMMUNITY_API_KEY": "your-api-key",
        "INTELLIJ_COMMUNITY_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Intellij Community API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Intellij Community API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Analyze all deprecated API usages in this project and suggest modern replacements"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Intellij Community Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
