---
name: mcp-documentation
description: Reference and learning guide for the Model Context Protocol (MCP). Use when implementing clients/servers or debugging connection issues. For server listings, see mcp-server-registry.
---

# MCP Documentation Skill

## When to Use

- When needing to understand the underlying architecture of MCP.
- When implementing a custom MCP client or server.
- To research specific protocol features (Resources, Prompts, Tools).

## Reference

[Official MCP Documentation](https://modelcontextprotocol.io/)

## Instructions

### 1. Conceptual Understanding

- **Clients**: Applications like Claude Desktop or IDEs that connect to servers.
- **Servers**: Lightweight programs that expose tools, resources, and prompts.
- **Transports**: The communication layer (usually Stdio or SSE).

### 2. Implementation Guide

- **SDKs**: Use the official SDKs for [TypeScript](https://github.com/modelcontextprotocol/typescript-sdk) or [Python](https://github.com/modelcontextprotocol/python-sdk).
- **Core Components**:
- `Tools`: Executable functions (e.g., `calculate_roi`).
- `Resources`: Data sources (e.g., `database://logs`).
- `Prompts`: Pre-defined templates for LLM interaction.

### 3. Debugging

- Use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to test servers interactively.
- Check transport logs for message parsing errors.

## Quality Gates

- Compliance with the latest [Specification](https://modelcontextprotocol.io/docs/concepts/specification).
- Use of official SDKs for standardized implementations.
- Documentation of custom tools/resources for agent discoverability.
