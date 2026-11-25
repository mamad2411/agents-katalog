---
name: zapier-ai-actions-migration
description: Guide for migrating from the deprecated Zapier AI Actions (Natural Language Actions) API to the new Zapier MCP standard.
---

# Zapier AI Actions to MCP Migration Skill

As of May 29, 2026, Zapier's original **AI Actions** product (also known as Natural Language Actions or NLA) has been sunsetted. Developers must migrate to **Zapier MCP (Model Context Protocol)**.

## Why the Change?
AI Actions (NLA) was a proprietary API that allowed developers to parse natural language to execute Zapier actions. By migrating to MCP, Zapier adopted an open, industry-standard protocol, meaning any MCP-compliant AI client can immediately use Zapier without custom API integrations.

## Migration Path

1. **Stop using the NLA API:** The legacy endpoints (e.g., `nla.zapier.com/api/v1/`) no longer function. Remove these integration points from your custom agents.
2. **Adopt an MCP Client:** If you built a custom AI agent, ensure your agent uses an MCP Client SDK to communicate with MCP servers.
3. **Configure Zapier MCP:** Instead of authenticating via the NLA OAuth flow, direct your users (or your own agent) to generate a server endpoint at [mcp.zapier.com](https://mcp.zapier.com).
4. **Tool Execution:** Your AI will now automatically discover available Zapier tools via the standard MCP `list_tools` method, rather than querying the NLA API for available actions.

## Benefits of MCP
- **Standardization:** Works out-of-the-box with Claude Desktop, Cursor, and other MCP tools.
- **Security:** Maintains Zapier's strict security governance (OAuth, rate limiting, audit logs) while delegating the tool-calling intelligence to the AI model itself.
