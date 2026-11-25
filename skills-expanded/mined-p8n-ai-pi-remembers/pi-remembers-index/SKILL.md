---
name: pi-remembers-index
description: >
  Index project files into Cloudflare AI Search for searchable project knowledge.
  Use when the user asks to "index files", "make files searchable", "index the project",
  "index docs", or when memory_search returns no results and the user likely hasn't
  indexed files yet. Also use when the user asks what files are indexed or wants to
  re-index after making changes.
---

# Pi Remembers Index Skill

Index project files into Cloudflare AI Search so the agent can search them
with the `memory_search` tool using hybrid vector + keyword search.

## Indexing Files

Use the `/memory-index` command:

```
/memory-index                  # Index all files (respecting .gitignore)
/memory-index src              # Index files under src/
/memory-index README.md docs   # Index specific files or directories
```

### What gets indexed
- Source code: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, etc.
- Documentation: `.md`, `.mdx`, `.txt`
- Configuration: `.json`, `.yaml`, `.yml`, `.toml`, `.env.example`
- Other: `.sql`, `.graphql`, `.prisma`, `.html`, `.css`
- Named files: `Dockerfile`, `Makefile`, `README`, `LICENSE`

### Limits
- Max file size: 100KB per file
- Respects `.gitignore` (uses `git ls-files`)

## When to Suggest Indexing

1. **`memory_search` returns no results** → Suggest: "No results found. Run `/memory-index` to index project files first."
2. **User asks "can you search my code"** → Suggest indexing first
3. **After major project changes** → Suggest re-indexing to update the search index

## Related Commands

| Command | Purpose |
|---------|---------|
| `/memory-index [paths]` | Index files into AI Search |
| `/memory-status` | Check how many files are currently indexed |
| `/memory-settings` | Toggle hooks including auto-ingest on compaction |

## After Indexing

Once files are indexed, use `memory_search` to find relevant information:
```
memory_search(query: "database connection setup")
memory_search(query: "error handling patterns")
memory_search(query: "authentication middleware")
```
