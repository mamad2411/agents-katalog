---
name: connect-another-client
description: Connect the same Opsphere account to another MCP app without sharing tokens or changing workspace.
---

# Connect another client

Ask which destination the user wants and whether its configuration should be global or per project. Show only the relevant destination's instructions.

Read the MCP resource `opsphere://clients/connect` (or `opsphere://clients/warp` for Warp) when available. Otherwise read [the generated connection guide](references/connect.md). This is the maintained fallback from the same canonical source; do not invent configuration, callbacks or availability.

If available, use `ops_my_usage` to verify the current account. Complete independent OAuth in the destination, then verify `ops_my_usage` and `ops_accounts_list` there. Never request or copy OAuth tokens, choose a workspace without consent, or promise that a public package exists without checking its publication.
