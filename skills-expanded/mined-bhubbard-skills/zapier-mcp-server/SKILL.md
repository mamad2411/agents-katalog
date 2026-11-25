---
name: zapier-mcp-server
description: Using the Zapier MCP (Model Context Protocol) Server to allow AI clients like Claude or Cursor to execute Zapier actions.
---

# Zapier MCP Server Integration Skill

Zapier provides an MCP server endpoint that acts as a universal translator between your AI client and over 9,000+ external tools in Zapier's ecosystem. 

## Overview
By connecting an AI assistant (like Claude, Cursor, or ChatGPT) to Zapier MCP, the AI can perform real-world tasks through natural language commands (e.g., sending Slack messages, updating CRMs). Zapier handles the authentication, encryption, and rate limiting.

## Setup Steps

1. **Generate the Endpoint:** Go to [mcp.zapier.com](https://mcp.zapier.com/) and create a new MCP server endpoint.
2. **Select AI Client:** Choose your preferred AI client from the dropdown menu to get tool-specific setup instructions.
3. **Configure Allowed Actions:** Using the Zapier MCP interface, browse and enable the specific apps and actions your AI is allowed to trigger.
4. **Connect the Client:** Copy the generated MCP server URL and paste it into your AI client's configuration file (e.g., `claude_desktop_config.json` for Claude Desktop).

## Usage
Once configured, you can prompt your AI directly to execute tasks. For example:
> "Find the latest email from John and create a Trello card with its contents."

The AI will automatically route the request through the Zapier MCP server to perform the actions securely.
