---
name: specification-agent-readiness
description: "Guidelines from The Website Specification on preparing a site for AI agents, covering llms.txt, Markdown negotiation, and MCP."
---

# Agent Readiness Specification

According to [The Website Specification](https://specification.website/spec/agent-readiness/), a modern website must be optimized not just for human browsers and search crawlers, but for autonomous AI agents.

## Core Requirements

### 1. The `llms.txt` File
Provide a concise, Markdown-formatted summary of your project at `/llms.txt`. 
*   **Purpose:** Gives agents immediate context on what the site is, core documentation links, and how to navigate the technical resources.
*   **Optional:** You can also provide `/llms-full.txt` containing concatenated documentation for deep context injection.

### 2. Markdown Content Negotiation
Agents process text, not DOM elements. You should support Markdown content negotiation:
*   When a client requests `Accept: text/markdown`, your server should return a clean, Markdown-formatted version of the requested page (stripping navbars, footers, and visual cruft).

### 3. MCP and Tool Discovery
If your site offers an API or tools for agents:
*   Host a Model Context Protocol (MCP) server.
*   Expose its location via `/.well-known/mcp/server-card.json`.
*   Include the `Link: <...>; rel="mcp"` HTTP response header on relevant pages to broadcast the server's availability natively.
