---
name: zapier-mcp-client
description: Using Zapier as an MCP client to ingest external MCP servers into your Zapier workflows.
---

# Zapier MCP Client Integration Skill

While Zapier has an MCP Server for external AI clients, Zapier also acts as an **MCP Client**. This allows you to connect remote or self-hosted MCP servers into your Zapier automated workflows.

## Overview
If you have a proprietary internal database or a custom tool exposed via an MCP server, you can connect it to Zapier. Zapier can then trigger workflows based on data from your MCP server or use your MCP server as an action step in a larger Zapier automation.

## Setup Steps
1. **Host your MCP Server:** Ensure your custom MCP server is accessible via the web (e.g., using SSE - Server-Sent Events).
2. **Connect in Zapier:** In your Zapier account, navigate to your app connections or create a new Zap, and select the MCP app integration.
3. **Provide Connection Details:** Provide the URL to your external MCP server endpoint and any required authentication tokens.
4. **Build the Zap:** You can now map the tools exposed by your custom MCP server to triggers and actions in your Zapier workflows, linking them with thousands of other apps.

## Best Practices
- Ensure your custom MCP server has strict authentication since Zapier will be calling it remotely.
- Map the input schemas of your MCP tools carefully so that Zapier can provide the correct fields in its visual editor.
