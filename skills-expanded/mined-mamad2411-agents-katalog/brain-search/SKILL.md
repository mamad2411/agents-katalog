---
name: brain-search
description: |
  Search the brain knowledge base directly for any query.
  Use: /brain-search <query>
user_invocable: true
---

# brain-search

Search everything the brain has indexed for a query. Good for broad keyword lookups across all indexed content.

## Instructions

The user provides a search query as an argument.

Run:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brain_engine.py kb-search "$CLAUDE_PROJECT_DIR" "$ARGS" 5
```

Display results with titles, sources, and relevant snippets.

## What gets searched

| Source | Content | When indexed |
|--------|---------|-------------|
| Session KB | `batch_execute` and `execute` MCP tool output | Each session |
| CLAUDE.md | Project instructions | Session start |
| Git log | Last 20 commits | Session start |
| Config files | package.json, requirements.txt, etc. | Session start |
| Convention files | CONVENTIONS.md, AGENTS.md, .cursorrules | Session start |
| Auto-stack | Seeded conventions (nextjs, fastapi, etc.) | First session |

**Tip:** For role-specific task history and decisions, use `/brain-query <role>` instead — it applies relevance ranking and recency boost specific to that role.

## If nothing is found

Suggest:
1. `/brain-remember <fact>` to manually add important information
2. `/brain-query <role>` to look up role-specific task history
3. Starting an Agent Team session to build up memory automatically
