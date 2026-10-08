---
name: cursor-discord-docs
description: |
  Retrieve up-to-date Cursor and Discord developer documentation via the
  Context7 MCP before writing or modifying code that touches Cursor internals
  or the Discord API. Use proactively when configuring MCP servers, writing
  Cursor rules/skills/agents, building Discord bots, or integrating with the
  Discord gateway or REST API.
paths:
  - "**/*.ts"
  - "**/*.js"
  - "**/*.py"
  - "**/*.json"
  - ".cursor/**/*"
---

# Cursor & Discord docs retrieval

This skill ensures the agent consults the current published documentation for
Cursor and Discord before generating code, rather than relying on possibly-
stale model memory.

## Libraries and their Context7 IDs

| Target | Context7 library ID | Notes |
| --- | --- | --- |
| Cursor editor/agent docs | `/websites/cursor` | MCP, rules, skills, agents, cloud agents, hooks. ~3000 snippets. |
| Discord API docs | `/discord/discord-api-docs` | Bot auth, gateway, REST, voice, SDKs. ~4000 snippets. |
| Discord developer platform | `/llmstxt/discord_llms_txt` | Broader developer platform + SDKs. ~4600 snippets. |

## Procedure

1. **Identify the target.** Is this about Cursor internals or the Discord API?
   Pick the matching library ID from the table above.
2. **Query with a specific question.** Good: "How to configure an SSE MCP
   server in mcp.json." Bad: "mcp". The Context7 API ranks by relevance, so
   specificity improves results.
3. **Read the returned snippets.** Each result includes a source URL. Use
   those URLs as citations when explaining the code to the user.
4. **Write code consistent with the retrieved docs.** If the docs contradict
   your memory, follow the docs and note the discrepancy.
5. **Stop after 3 calls per question.** Reuse earlier results rather than
   re-querying. If you still lack what you need, fall back to your knowledge
   and flag the uncertainty.

## What to avoid

- Do not paste secrets into the query field. Context7 queries are sent to a
  third-party API.
- Do not treat the docs MCP as authoritative for anything beyond Cursor and
  Discord. It is a context-enrichment tool, not a general oracle.
- Do not silently ignore empty results. Report them so the user can decide
  whether to proceed from memory.

## Example flow

```
User: "Add a Discord bot that connects to the gateway and logs READY."

Agent:
1. Call Context7 QUERY_DOCS with libraryId=/discord/discord-api-docs
   and query="How to authenticate a bot and connect to the gateway".
2. Receive: bot token auth header, Get Gateway URL, wss connection string,
   Identify/Heartbeat event list.
3. Write the bot using those specifics, citing the source URLs.
```
