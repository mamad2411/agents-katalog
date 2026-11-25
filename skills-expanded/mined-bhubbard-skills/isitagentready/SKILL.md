---
name: isitagentready
description: "Guidelines for scanning websites for AI Agent readiness using the WebMCP tool embedded in IsItAgentReady.com."
---

# IsItAgentReady WebMCP Tool

The website `isitagentready.com` features a natively embedded WebMCP (Web Model Context Protocol) tool that AI agents can use to scan any URL and determine if it is properly configured for AI bot consumption and commerce.

## The `scan_site` Tool

When interacting with this site, agents can invoke the `scan_site` tool.

**Input parameters:**
*   `url` (string): The URL of the website to scan. Must be a valid URI.

**What it returns:**
The tool performs a battery of checks across 5 core categories and returns a readiness level (0-5) along with specific results and fix instructions for any failing checks.

### Checked Categories:
1.  **Discoverability**: Checks for valid `robots.txt`, XML Sitemaps, Link headers, and DNS for AI Discovery (DNS-AID).
2.  **Content Accessibility**: Checks if the site supports Markdown content negotiation for AI agents.
3.  **Bot Access Control**: Verifies AI bot rules in `robots.txt`, Content Signals, and Web Bot Auth implementation.
4.  **Protocol Discovery**: Looks for an MCP Server Card (`.well-known/mcp/server-card.json`), Agent Skills, WebMCP implementations, API Catalogs, and OAuth protected resources.
5.  **Commerce**: Checks for Agentic Commerce protocols (x402, MPP, UCP, ACP).

## Usage
Agents can use this tool to automatically audit a user's website and provide them with a direct "fix sheet" (the exact prompts and instructions needed to make their site more agent-friendly) based on the scan results.
