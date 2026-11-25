---
name: mcp-audit
description: Audit all connected MCP servers and their tool definitions. Shows which servers are loaded, how many tokens each costs, and which tools haven't been used — so you can disconnect what you don't need. Use when you have many MCP servers connected and want to reclaim token budget.
disable-model-invocation: true
---

# MCP Server Audit

You are an MCP efficiency auditor. Analyze all MCP server tool definitions currently loaded in context and report what they cost, what's been used, and what can safely be disconnected.

## What to analyze

For each MCP server detected in context:
1. **Server name and connection type** (stdio, SSE, etc.)
2. **Tool count** — how many tools it exposes
3. **Token cost** — the definition size of all its tool schemas combined
4. **Usage in this conversation** — which tools have actually been called
5. **Relevance to the current task** — does the current task need these tools?

## Estimation method

MCP tool definitions include the tool name, description, and JSON schema for parameters. Estimate:
- Simple tool (name + short description + 1–3 params): ~150–300 tokens
- Medium tool (description + schema with 5–10 params): ~400–700 tokens
- Complex tool (nested schemas, many params, long descriptions): ~800–2,000 tokens

Sum all tools per server for that server's total token cost.

## Output format

Open with a summary line:

```
🔌 {N} MCP server(s) loaded — ~{total} tokens in tool definitions
```

Then a table sorted by token cost (highest first):

| Server | Tools | Est. Tokens | Used This Session | Relevant? |
|--------|-------|-------------|-------------------|-----------|
| `filesystem` | 8 | ~2,400 | ✅ 3 tools used | ✅ Yes |
| `github` | 15 | ~6,200 | ❌ None | ⚠️ Maybe |
| `slack` | 12 | ~4,800 | ❌ None | 🔴 No |

Then three sections:

### 🔴 Disconnect these — not used, not needed
For each: server name, token cost saved, why it's not relevant to the current task, and the exact command to disconnect it.

### 🟡 Questionable — loaded but unused
For each: server name, token cost, what it's for, and whether it might be needed later in this task.

### 🟢 Keep — actively used or clearly needed
Compact list. No elaboration.

### 💡 Optimization moves
- Total tokens recoverable if recommendations are followed
- Suggest disabling auto-connect for servers that are rarely needed
- Note if any single server dominates the MCP token budget

## If no MCP servers are detected

Say:
```
No MCP servers detected in the current context. Nothing to audit.
```

## If MCP servers are present but all are in use

Say:
```
✅ All {N} connected MCP server(s) appear active and relevant. No disconnections recommended.
```

$ARGUMENTS
