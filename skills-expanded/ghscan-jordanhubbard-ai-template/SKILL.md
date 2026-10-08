---
name: responsible-vibe
description: >
  Follow the responsible-vibe development workflow when the user selects that
  optional integration and its MCP server is available.
license: MIT
metadata:
  version: '5.3.0'
  repository: https://github.com/mrsimpson/responsible-vibe-mcp
  author: mrsimpson
requires-mcp-servers:
  - name: responsible-vibe-mcp
    package: '@codemcp/workflows'
    description: 'Structured development workflows for AI-assisted coding'
    command: npx
    args: ['@codemcp/workflows@5.3.0']
---



This is an optional integration example. Use it only when the user selects the
responsible-vibe workflow and the required MCP tools are available. If the
repository's `skills/config.yaml` sets
`behavior_switches.responsible_vibe_workflow.enabled: false`, do not activate it
implicitly. Missing configuration is not permission to activate this workflow.
An explicit request to use the workflow takes precedence over its default.

Within a selected workflow, use `whats_next()` to retrieve phase guidance and
record progress in its development plan. Keep guidance within the user's task
and the destination repository's conventions. Do not require the server for
unrelated tasks or replace the user's chosen workflow.
