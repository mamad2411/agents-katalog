---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# mcp builder

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions
- **TypeScript SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- **Python SDK**: Use WebFetch to load `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)

## Available sections

- MCP Server Development Guide
- Overview
- Process
- 馃殌 High-Level Workflow
- Phase 1: Deep Research and Planning
- Phase 2: Implementation
- Phase 3: Review and Test
- Phase 4: Create Evaluations
- Reference Files
- 馃摎 Documentation Library
- Core MCP Documentation (Load First)
- SDK Documentation (Load During Phase 1/2)

## Bundled resources

- reference
- scripts

Open these resources only if the current task needs deeper detail or executable helpers.
