---
name: paperzilla-mcp
description: Help users migrate a retired Paperzilla MCP plugin or API-key connection to the current OAuth setup.
---

# Migrate Paperzilla MCP to OAuth

If the user has an old Paperzilla MCP entry configured with an API key, ask them to remove that entry from their client. Direct them to the [Codex setup guide](https://docs.paperzilla.ai/guides/codex) or the [MCP setup guide](https://docs.paperzilla.ai/guides/mcp) for other clients.

Have them add `https://paperzilla.ai/api/mcp` as a Streamable HTTP server and sign in to Paperzilla to review the OAuth permissions. Once connected, they can try a read-only request such as “Find public Paperzilla digests about machine learning.”

For shell workflows, direct them to the [Paperzilla CLI guide](https://docs.paperzilla.ai/guides/cli).
