---
name: document-code
description: Read undocumented functions and store one-sentence summaries into Loom. Prioritizes hot functions and missing-summary suggestions. Makes every future session faster.
argument-hint: "[module or keyword to focus on]"
allowed-tools:
  - mcp__loom__search_code
  - mcp__loom__get_context
  - mcp__loom__store_understanding
  - mcp__loom__store_understanding_batch
  - mcp__loom__suggest_questions
  - mcp__loom__god_nodes
  - mcp__loom__get_savings
  - Read
  - Glob
---

# Document Code

Read undocumented functions and write summaries back to Loom. Every summary you store eliminates a future file read.

## Steps

### 1. Find documentation gaps

Call `suggest_questions(limit=7)` — look for `MISSING_SUMMARY` type entries. These are hot functions (many callers) with no cached summary.

Call `god_nodes(limit=20)` — most-called functions. Cross-reference with search results to find which ones have null summaries.

If the user specified a keyword/module argument:
```
search_code("<argument>", limit=20)
```
Filter results where `summary` is null.

### 2. Prioritize

Work in this order:
1. Hot functions with no summary (`god_nodes` + null summary)
2. `suggest_questions` `missing_summary` results
3. Functions with `summary_stale: true` (source changed, summary outdated)
4. Any function you have to read for other reasons

### 3. For each undocumented function

First try `get_context(node_id)` — often enough to write a good summary without reading source:
- Signature tells you inputs/outputs
- Callers tell you how it's used
- Callees tell you what it relies on

If `get_context` is insufficient, read the source:
```
Read("<path>", offset=<start_line>, limit=<end_line - start_line + 10>)
```

### 4. Write the summary

```
store_understanding(
    node_id="<exact node_id>",
    summary="<one sentence: what it does AND why it exists>"
)
```

Quality check:
- Under 120 characters
- Describes WHAT + WHY (not HOW)
- Includes key behavior: return value, side effects, preconditions if important
- Not vague ("handles X"), not implementation-level ("calls jwt.decode()")

### 5. Batch when ready

After every 5–10 individual stores, switch to batch for efficiency:
```
store_understanding_batch([
    {"node_id": "...", "summary": "..."},
    {"node_id": "...", "summary": "..."}
])
```
Max 50 per batch call.

### 6. Check savings at end

```
get_savings()
```

Report to user: agent-written summaries (file reads provably saved), auto-summary hits, total tokens saved.

## Summary Quality Examples

| Function | Good Summary |
|----------|-------------|
| `validate_token` | "Validates JWT tokens against the configured secret, returns False if expired or signature is invalid." |
| `bulk_upsert_nodes` | "Upserts a list of Node objects into SQLite, preserving existing agent summaries when content hash is unchanged." |
| `_row_to_node` | "Converts a raw SQLite row dict into a typed Node object, defaulting missing metadata fields to empty dict." |
| `index_repo` | "Walks a repository with tree-sitter, extracts all symbols, and writes them into the Loom SQLite graph." |
