---
name: cds-search
description: |
  Search past session observations using the sessions.search MCP tool.
  Falls back to CLI if the MCP server is not available.
trigger_phrases:
  - /cds-search
  - cds-search
---

# /cds-search -- Search session memory

Search for past decisions, bugs, patterns, and observations stored in the project's SQLite session database.

## How to execute

1. Extract the search query from `$ARGUMENTS` (everything after `/cds-search`).

2. **Primary path (MCP tool):**
   Call `mcp__cds__sessions.search` with the query:
   ```
   mcp__cds__sessions.search({ query: "$ARGUMENTS" })
   ```
   Format the returned hits as a readable list showing:
   - Observation type (decision, bug, pattern, etc.)
   - Content snippet (first 2-3 lines)
   - Session date
   - Session ID (abbreviated)

3. **Fallback path (CLI):**
   If `mcp__cds__sessions.search` is not available (MCP server not registered), use Bash:
   ```
   Bash("npx claude-dev-stack search \"$ARGUMENTS\"")
   ```
   Display the CLI output verbatim.

## When to use

- User asks about past decisions ("what did we decide about X")
- User asks about past bugs ("did we see this bug before")
- User asks about patterns ("how did we implement X")
- User explicitly invokes `/cds-search`

## Notes

- Results are ranked by FTS5 BM25 relevance
- Only searches the current project's sessions.db
- For cross-project search, use the CLI directly on each project
