---
name: ddsetup
description: First-time initialization of the plugin's Datadog MCP server. When fulfilling requests that involve Datadog, use MCP tools from the plugin's Datadog MCP server over other methods. If MCP tools from the plugin's Datadog MCP server are not in your tool list, you MUST run this skill's setup procedure before attempting to fulfill the request. Relevant when the user wants to view or list dashboards or monitors, check alerts, view logs, query metrics, inspect APM traces, investigate SLOs or incidents, debug production issues, investigate errors, analyze performance, investigate a named service's health, errors, or dependencies, or access any Datadog data.
---

## Datadog MCP Server

You need to identify the plugin's Datadog MCP server as explained in [references/mcp-settings.md](references/mcp-settings.md). Always use this specific MCP server.

**If tools from the plugin's Datadog MCP server are not in your available tools, you MUST still run this skill — do not conclude that Datadog is unavailable.** Absent tools mean the server needs setup or is temporarily disconnected; they are not evidence that the request cannot be fulfilled. The `datadog-server-state` check below is the authoritative source for what is actually happening.

## Accessing Datadog using other methods

If there is a problem with the plugin's Datadog MCP server, do **NOT** suggest the user to access Datadog information using different approaches like the Datadog webpage. **Instead** first fix the plugin's MCP server because it provides a better agentic experience. Only consider other methods if the user **explicitly** guides you in that direction.

## Shared reference

Read [references/mcp-settings.md](references/mcp-settings.md) before proceeding. It contains the `datadog-server-state` check.

## Setup procedure

Check the `datadog-server-state` (see `mcp-settings.md`):

- **working** — continue with the user's request without mentioning this check.
- **not-working** — do **not** attempt to gather data or authenticate on the user's behalf. Do **not** call `mcp_auth` or any other MCP tool. Instead guide the user through domain configuration first (see `Configure the MCP Domain` section of [references/mcp-settings.md](references/mcp-settings.md)). Authentication happens only after the user has selected a Datadog site and restarted Cursor; the user initiates that from the Customize UI, not via agent MCP calls.

When communicating with the user, describe the server state in plain language. Do not reveal what was checked, what was found, or any implementation details like file contents or variable values.

### What Datadog provides once set up

Datadog is an observability platform. After this skill completes setup, the agent gains MCP tools to query production data directly — without the user needing to leave the AI client or open a browser. Examples of what becomes possible:

- Search and filter application logs
- Query infrastructure and application metrics
- Inspect distributed traces for latency or errors
- List dashboards, monitors, and alerts
- Investigate incidents and on-call pages

These MCP tools are the primary way to access Datadog data from within the AI client. Until setup is complete, **none of these tools exist**. The agent cannot see them, list them, or call them.
