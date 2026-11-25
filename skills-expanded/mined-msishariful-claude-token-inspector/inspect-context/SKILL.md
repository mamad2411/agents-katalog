---
name: inspect-context
description: Analyze the current context window and report a breakdown of what's consuming tokens — system prompts, files, conversation history, skills, and MCP configs. Use when the user wants to understand their token budget.
disable-model-invocation: true
---

# Context Window Inspector

Analyze everything currently loaded in this conversation's context and produce a structured, actionable report.

## What to analyze

1. **System prompt & instructions** — CLAUDE.md content, project instructions, and any system-level directives
2. **Loaded files** — every file in context with line counts and token estimates
3. **Conversation history** — turn count and token cost of prior messages
4. **Skills & plugins** — active skill instructions currently loaded
5. **MCP server configs** — tool definitions from any connected MCP servers
6. **Embedded documents** — pasted code blocks, documents, or large text from the user

## Output format

Start with a one-line status banner:

```
📊 Context snapshot — ~XX,XXX tokens used  |  ~YYY,YYY remaining  |  ZZ% full
```

Then a table sorted by estimated token usage (largest first):

| # | Source | Type | Est. Tokens | % of Budget | Keep? |
|---|--------|------|-------------|-------------|-------|
| 1 | `src/api/routes.ts` | File | ~4,200 | 2.1% | ✅ Yes |
| 2 | Conversation (turns 1–12) | History | ~8,500 | 4.3% | ⚠️ Partial |
| 3 | `CLAUDE.md` | Instructions | ~1,800 | 0.9% | ✅ Yes |

Then three sections:

### 🔥 Top bloat candidates
The 3 largest items that may not be needed for the current task — with a one-line reason each.

### ✅ Essential context
A short bullet list of items that are clearly needed and should not be touched.

### 💡 Quick wins
Specific, copy-paste-ready actions to immediately reduce token usage (e.g., `/clear`, unloading a file, splitting the conversation).

Be precise: use real file names, skill names, and turn numbers. Estimate tokens as 1 token ≈ 4 characters for English prose, slightly fewer for dense code.

$ARGUMENTS
