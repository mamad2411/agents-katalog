---
name: mcp-scaffolding-mcp-server-scaffold
description: "Tool schema design, transport choice, error contracts, and test harness for Model Context Protocol servers."
---
# Scaffold an MCP server agents can trust

> Tool schema design, transport choice, error contracts, and test harness for Model Context Protocol servers.

**Track:** 🤖 AI Engineering · **Domain:** MCP Server Building · **Level:** intermediate · **~45 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Tool schema design, transport choice, error contracts, and test harness for Model Context Protocol servers.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Model each capability as a tool with JSON-Schema'd inputs and typed outputs
2. Choose stdio transport for local tools, Streamable HTTP for remote services
3. Return structured errors agents can self-correct from; never raw stack traces
4. Cap response payloads; paginate lists instead of dumping unbounded results
5. Write an inspector-based smoke test: list tools, call each once, assert schemas
6. Version tool names deliberately; renaming breaks every client integration

## Common Pitfalls

- Tools that wrap entire CLIs instead of one verb-noun responsibility
- Secrets passed as plain tool parameters logged in traces

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill mcp-scaffolding-mcp-server-scaffold
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill mcp-scaffolding-mcp-server-scaffold -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills