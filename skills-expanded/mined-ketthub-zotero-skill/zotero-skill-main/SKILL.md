---
name: zotero
description: >-
  Query your local Zotero library. Supports keyword, fulltext, author, collection, tag, DOI, and recent-additions search.
  Trigger: /zotero, "my papers", "Zotero", "find paper", "references", "citations".
  After installation, verify DEFAULT_DB path in scripts/zotero-search.py points to your zotero.sqlite.
---

# Zotero Local Search

Query a local Zotero library (`zotero.sqlite`), read-only, zero external dependencies.

> **Setup**: The default database path is `~/Zotero/zotero.sqlite` (standard on macOS/Linux).
> Windows users: change `DEFAULT_DB` in `scripts/zotero-search.py` to your Zotero data directory,
> typically `C:\Users\<username>\Zotero\zotero.sqlite`.
> You can also override per-call with `--db PATH`.

## Tool

```bash
python3 .claude/skills/zotero/scripts/zotero-search.py <mode> <query> [options]
```

### Search Modes

| Mode | Command | Description |
|------|---------|-------------|
| Keyword search | `search "query"` | Search title, abstract, journal, authors, notes |
| Fulltext search | `fulltext "word1 word2"` | Search PDF body text (inverted index, exact word match, AND semantics), ranked by metadata relevance |
| Author search | `author "name"` | By author name (partial match) |
| Browse collection | `collection list` / `collection "name"` | List or browse collections |
| Recent additions | `recent [--days N]` | Items added in last N days (default: 30) |
| Tag search | `tag list` / `tag "name"` | List or search by tag |
| DOI lookup | `doi "10.xxxx/..."` | Exact DOI match |
| Get by key | `get KEY1 KEY2 ...` | Batch fetch by itemKey, preserves input order |

### Global Options

| Flag | Default | Description |
|------|---------|-------------|
| `--limit N` | 20 | Max results |
| `--type TYPE` | all | Filter by type: `journalArticle` / `book` / `conferencePaper` / `preprint` |
| `--compact` | false | Compact output (title, authors, year, journal, URI only) — good for scanning |
| `--db PATH` | `~/Zotero/zotero.sqlite` | Override database path |

## Instructions

### 1. Intent Mapping

Map user requests to search modes:

- "find/search + keywords" -> `search`
- "papers by [author]" -> `author`
- "what's in [collection]" -> `collection`
- "recently added" -> `recent`
- "tagged with X" -> `tag`
- "do I have this DOI" -> `doi`
- "paper mentions X" / "body text contains X" -> `fulltext`
- Unsure -> default to `search`

### 2. Search Execution

Run the command, get JSON results.

**Strategy**:
- `search` mode auto-ranks by relevance (phrase match > whole word > substring), output includes `relevance` score
- **Two-stage retrieval**: use `--compact` first to scan results, then `get KEY1 KEY2 ...` to fetch full details for selected items
- For compound terms (e.g. "Neural ODE"), if `search` is noisy, supplement with `fulltext` (exact word match, less noise)

### 3. Fallback

`search` returns nothing -> auto-try `fulltext` (keywords may appear in PDF body, not title/abstract).

### 4. Result Presentation

- **1-3 results**: Show full info (title, authors, year, journal, abstract excerpt, DOI, zoteroURI)
- **4-10 results**: Title + authors + year list, offer to expand
- **10+ results**: Show count + title list, suggest narrowing query
- Always include `zoteroURI` (clickable link to open in Zotero)

### 5. Writing Assistance

When the user is writing a paper/document:
- Proactively provide citation format: `(Author, Year)`
- Include DOI for cross-referencing
- If abstract available, briefly summarize the paper's key contribution

### 6. Combined Queries

No complex SQL needed. For "papers by [author] about [topic]":
- Run `search "topic keywords"`
- Filter results by matching the author field in returned JSON

### Notes

- `fulltext` is **exact word match** (no phrases, no fuzzy, no stemming), multi-word = AND
- Tag coverage varies by library; not the primary search method
- Some items may lack abstracts — this is normal
