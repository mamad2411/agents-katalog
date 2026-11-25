---
name: specification-website-mcp
description: "Guidelines for querying The Website Specification via their public MCP server."
---

# The Website Specification MCP Server

The Website Specification (specification.website) provides a public, stateless, read-only MCP server that allows agents to query the complete specification of what makes a technically good website.

## Connection Details
The MCP server communicates over Streamable HTTP (2025-03-26 revision) and requires no authentication or API keys.

**URL:** `https://mcp.specification.website/mcp`

## Available Tools

1.  **`search(query, limit?)`**: Returns ranked spec pages containing the title, status, category, URL, and body excerpts. Use this for general topic discovery (e.g., "CSP" or "robots.txt").
2.  **`list_topics({ category?, status?, limit? })`**: Returns a filtered index of topics (slug, title, summary, URL).
3.  **`get_topic({ slug })`**: Returns the full canonical Markdown for a specific page, including its frontmatter and sources.
4.  **`get_checklist({ category?, status? })`**: Generates a tickable Markdown checklist grouped by category, perfect for appending to an audit plan.
5.  **`get_categories()`**: Returns the top-level categories and their topic counts.
6.  **`audit_url(url, focus?)`**: Generates a tailored audit plan for a target URL against the required spec items. Can be optionally narrowed to a specific category focus (like `security` or `seo`).

## Usage Pattern
Agents should use this MCP server to ground their knowledge when a user asks for best practices on website development, security, accessibility, or agent-readiness. Instead of relying on training data, the agent can fetch the authoritative, CC BY 4.0 licensed specification directly from the source.
