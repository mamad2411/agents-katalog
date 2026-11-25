---
name: localwp-mcp-integration
description: Integrate LocalWP with MCP using the mcp-local-wp server.
---

# LocalWP MCP Integration

This skill guides you through setting up and using the MCP server for WordPress database access via Local by Flywheel (`@verygoodplugins/mcp-local-wp`).

## Overview
The `mcp-local-wp` server provides Model Context Protocol tools to interact with local WordPress databases managed by LocalWP.

## Setup Instructions
1. Ensure LocalWP is installed and running.
2. Install the server:
   ```bash
   npx -y @verygoodplugins/mcp-local-wp
   ```
3. Configure your MCP client to use this server. In your Gemini/Claude configuration, add the server details:
   - Command: `npx`
   - Args: `[-y, "@verygoodplugins/mcp-local-wp"]`

## Capabilities
Once connected, the MCP server provides tools to:
- List available LocalWP sites.
- Query the WordPress database for specific sites.
- Retrieve posts, options, and user data securely via local database connections.

## Troubleshooting
- **Connection Refused**: Ensure the LocalWP site is running and the database socket/port is accessible.
- **Path Issues**: The server attempts to automatically locate LocalWP's configuration directory. If it fails, ensure LocalWP is installed in the default location.
