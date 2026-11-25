---
name: power-platform-prereq-check
description: Checks local prerequisites for Power Platform agent work, including PAC CLI, Azure CLI, Node.js, .NET 10, dnx, and sign-in readiness.
allowed-tools: Bash, Read
---

# Power Platform Prerequisite Check

Run this before live Power Platform authoring, deployment, MCP setup, or any
workflow that depends on PAC, Azure CLI, or local MCP servers.

## Workflow

1. Run:

   ```bash
   node "${PLUGIN_ROOT}/scripts/check-prereqs.js"
   ```

2. Report the result as a compact readiness summary.
3. Do not echo raw `pac auth list` or `az account show` output. Those commands
   can contain real tenant, user, subscription, and environment identifiers.
4. If any check fails, stop before live writes and give the smallest next action
   needed to fix the machine.

## Expected Dependencies

- `pac` for Power Platform CLI operations.
- `az` for Dataverse and Azure-backed authentication flows.
- Node.js for bundled scripts and Power Automate FlowAgent.
- .NET 10 SDK and `dnx` for the Canvas Authoring MCP server.
