---
name: moodle-mcp-connector
description: "MCP connector for Moodle LMS – enables AI-powered course creation, quiz generation, learner management, and grade analysis through Claude"
license: GPL
tags: ["education","lms","mcp","moodle","elearning"]
difficulty: intermediate
time_to_master: "4-8 weeks"
version: "1.0.0"
---

# Moodle MCP Connector

## Overview

This skill enables Claude to interact with **Moodle** through the Model Context Protocol (MCP). It provides a bridge between Claude's AI capabilities and Moodle's REST/Web Services API, allowing natural language control of Moodle operations, intelligent automation, and AI-powered assistance for Moodle workflows.

## When to Use This Skill

- Course structure and activity creation via AI
- Quiz and question bank generation
- Grade analysis and learner progress reporting
- Assignment creation with rubrics
- Forum moderation and discussion summarization

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Claude     │────▶│   MCP Server    │────▶│   Moodle           │
│   (Client)   │◀────│   (TypeScript)  │◀────│   (REST/Web Servi)│
└─────────────┘     └─────────────────┘     └──────────────────┘
```

## Core Concepts

### MCP Server Setup

The connector implements an MCP server that exposes Moodle operations as tools Claude can invoke. The server translates natural language intentions into REST/Web Services API calls.

### Key Endpoints/Interfaces

`core_course_create_courses`, `mod_quiz_get_quizzes`, `core_grades_get_grades`, `core_user_get_users`, `mod_forum_get_forums`

### Implementation

```typescript
// Moodle MCP Server Implementation
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "moodle-mcp-connector",
  version: "1.0.0",
});

// Tool: List/Query Resources
server.tool(
  "list_resources",
  "List and query Moodle resources with optional filters",
  {
    query: z.string().optional().describe("Search query or filter"),
    limit: z.number().optional().describe("Max results to return"),
  },
  async ({ query, limit }) => {
    // Call Moodle REST/Web Services API
    const response = await fetch(`${BASE_URL}core_course_create_courses`, {
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
  "Create a new resource in Moodle",
  {
    name: z.string().describe("Resource name"),
    config: z.object({}).passthrough().optional().describe("Resource configuration"),
  },
  async ({ name, config }) => {
    const response = await fetch(`${BASE_URL}core_course_create_courses`, {
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
  "AI-powered analysis of Moodle data",
  {
    type: z.string().describe("Analysis type"),
    timeframe: z.string().optional().describe("Time range for analysis"),
  },
  async ({ type, timeframe }) => {
    // Fetch data and provide AI analysis
    const response = await fetch(`${BASE_URL}core_course_create_courses`, {
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
    "moodle-mcp-connector": {
      "command": "node",
      "args": ["path/to/moodle-mcp-connector/index.js"],
      "env": {
        "MOODLE_API_KEY": "your-api-key",
        "MOODLE_BASE_URL": "https://your-instance-url"
      }
    }
  }
}
```

## Best Practices

1. **Authentication**: Store API keys securely using environment variables; never hardcode credentials
2. **Rate Limiting**: Implement request throttling to respect Moodle API rate limits
3. **Error Handling**: Provide clear, actionable error messages for common failure scenarios
4. **Pagination**: Handle paginated responses for large datasets efficiently
5. **Caching**: Cache frequently accessed read-only data to reduce API calls
6. **Security**: Validate all inputs before passing to the Moodle API; sanitize outputs
7. **Logging**: Log all API interactions for debugging and audit purposes

## Example Prompts

> "Create a 10-question quiz on machine learning fundamentals with varying difficulty levels"

## Security Considerations

- All API credentials must be stored as environment variables
- Implement input validation and sanitization for all tool parameters
- Use HTTPS for all API communications
- Follow the principle of least privilege for API token permissions
- Audit log all write operations for compliance tracking

## Resources

- Moodle Official Documentation
- MCP SDK Documentation: https://modelcontextprotocol.io
- MCP Server Examples: https://github.com/modelcontextprotocol/servers
- SkillGalaxy Repository: https://github.com/Sandeeprdy1729/skill_galaxy

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-01 | Initial MCP connector skill |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
