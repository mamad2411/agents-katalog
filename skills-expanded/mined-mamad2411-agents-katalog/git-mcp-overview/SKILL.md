---
name: git-mcp-overview
description: Discover and safely use the git-mcp server for Git inspection and mutation workflows.
version: 1.0.0
---

# git-mcp Overview

git-mcp is a TypeScript MCP server for local Git workflows. It exposes:

- Read-only resources for status, log, branches, and diff
- Tools for inspect, write, branch, remote, context, lfs, advanced, docs, and git-flow operations

## Safety model

- Inspect-before-mutate workflow
- Explicit controls around destructive Git operations
- Clear handling for detached HEAD, dirty trees, conflicts, and history rewrite paths

## Docs

- Getting started: [https://git-mcp.self.agency/guide/getting-started](https://git-mcp.self.agency/guide/getting-started)
- Tool reference: [https://git-mcp.self.agency/tools/](https://git-mcp.self.agency/tools/)
- Resources: [https://git-mcp.self.agency/guide/resources](https://git-mcp.self.agency/guide/resources)
