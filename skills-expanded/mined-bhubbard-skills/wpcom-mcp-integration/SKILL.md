---
name: wpcom-mcp-integration
description: "Seamlessly Connect AI Agents to WordPress.com with MCP. Guidelines for using the Model Context Protocol (MCP) on WordPress.com, including setup, tools, and permissions."
---

# WordPress.com MCP Integration

The **Model Context Protocol (MCP)** enables AI agents to securely connect to and interact with WordPress.com sites. This skill outlines how to configure, authenticate, and utilize MCP servers specifically for the WordPress.com ecosystem.

## Core Concepts
1. **MCP Architecture**: MCP standardizes how AI agents communicate with data sources. On WordPress.com, MCP allows agents to perform actions like querying posts, managing plugins, or executing WP-CLI commands without needing direct backend access.
2. **WordPress Studio & MCP**: The easiest way to test and develop MCP integrations is via WordPress Studio, which has built-in support for MCP servers.
3. **Agent Skills**: Agent Skills (defined via `SKILL.md` files) can leverage MCP tools to perform complex, multi-step actions on WordPress.com environments.

## Setup & Configuration

### Prerequisites
* A WordPress.com site (plugin-enabled plans are required for advanced custom API/MCP integrations).
* An AI agent client that supports MCP (e.g., Claude Desktop, Cursor, or custom local agents).
* Appropriate API credentials (OAuth2 tokens or Application Passwords) to authenticate the MCP server against the WordPress.com REST API.

### Starting an MCP Server for WordPress.com
When developing a custom MCP server for WP.com, you typically run it via `npx` or directly from source. Ensure your environment variables are configured with the necessary WP.com endpoints and authentication keys.

```bash
# Example of running a generic MCP server tailored for WP
npx @example/wpcom-mcp-server --site=yoursite.wordpress.com --token=YOUR_TOKEN
```

## Available Tools & Resources
A typical WordPress.com MCP integration exposes the following capabilities:

### Resources (Read-Only Data)
* **`posts://`**: Read access to published posts, pages, and custom post types.
* **`site-settings://`**: Read access to site metadata (title, description, timezone).
* **`logs://`**: Access to PHP error logs and web server logs (on supported plans).

### Tools (Actionable Commands)
* **`create_post`**: Draft or publish new content directly to the WordPress.com site.
* **`manage_plugins`**: Install, activate, or deactivate plugins.
* **`run_wp_cli`**: Execute arbitrary WP-CLI commands (e.g., `wp user list`) securely through the MCP bridge.
* **`clear_cache`**: Purge the site's edge and object cache.

## Security & Permissions
* **Least Privilege**: Always configure your MCP server with the minimum required permissions. Use Application Passwords restricted to specific roles (e.g., Editor instead of Administrator) if full admin access isn't necessary.
* **Approval Workflows**: Ensure your AI agent client (like Claude Desktop) prompts the user before executing destructive tools (like `run_wp_cli` or `manage_plugins`).
* **OAuth2**: For production or multi-tenant MCP servers connecting to WordPress.com, implement the standard WordPress.com OAuth2 flow rather than relying on static application passwords.

## Example Usage
When the agent has access to the WP.com MCP, the user can prompt:
> "Draft a new blog post summarizing our latest product release, then clear the site cache."

The agent will automatically map this to the `create_post` and `clear_cache` tools provided by the MCP server.

## Troubleshooting
* **Connection Refused / 401 Unauthorized**: Verify your API tokens. Ensure the WordPress.com site is not set to "Private" if the MCP server requires public API access.
* **Tool Execution Fails**: Confirm that the site is on a plugin-enabled plan if the tool requires advanced backend capabilities (like WP-CLI).
