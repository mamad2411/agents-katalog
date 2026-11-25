---
name: arkon-query
description: "Answer questions using the Arkon knowledge base. Searches wiki first, drills into raw sources only when needed. Supports quick, standard, and deep modes. Triggers on: what do we know about, find in KB, look up, query:, arkon query, search the wiki, tell me about, based on the KB."
allowed-tools: mcp__arkon__search_wiki mcp__arkon__read_wiki_index mcp__arkon__read_wiki_page mcp__arkon__list_wiki_pages mcp__arkon__list_knowledge_types mcp__arkon__get_knowledge_type_docs mcp__arkon__list_sources mcp__arkon__get_source mcp__arkon__get_source_outline mcp__arkon__get_source_pages
---

# arkon-query: Query the Knowledge Base

The wiki has already done the synthesis work. Read strategically, answer precisely. Raw sources are a fallback — not the first stop.

---

## Query Modes

| Mode | Trigger | Tools used | Best for |
|------|---------|-----------|---------|
| **Quick** | `query quick: ...` or simple factual Q | `search_wiki` only | Direct lookups, names, dates |
| **Standard** | default | `search_wiki` → 2-4 pages | Most questions |
| **Deep** | `query deep: ...` or "thorough", "find everything" | Full wiki traverse + source drill-down | Cross-cutting synthesis |

---

## Quick Mode

1. Call `search_wiki(query, top_k=5)`. If the top result has high similarity (≥ 80%) and its summary answers the question, respond immediately.
2. If not satisfied, call `read_wiki_page(slug)` for the top 1-2 results.
3. If still not found, say "Not in quick cache — run as standard query?"

Do not call `read_wiki_index` or source tools in quick mode.

---

## Standard Query Workflow

1. **`search_wiki(query)`** — ranked list of pages. Read summaries.
2. **`read_wiki_page(slug)`** for the 2-4 most relevant results. Follow wikilinks `[[slug]]` at depth 1 only if they look essential.
3. Synthesize the answer in chat. Cite with page slugs: _(Source: `concept/onboarding`)_.
4. If the question reveals a gap: "I don't have enough on X in the KB. Want to check the raw sources?"

---

## Deep Mode

1. `search_wiki` + `read_wiki_index` to map coverage.
2. Read all relevant pages. Follow wikilinks at depth 2 if needed.
3. If wiki coverage is thin for a specific claim, drill into raw sources (see below).
4. Always cite both wiki pages and source documents used.

---

## Source Drill-Down (citations or precise text)

Use when: the wiki has paraphrased something and you need the exact wording, or the user asks "what does the document actually say."

```
list_sources(knowledge_type=...)     → find source IDs by category
get_source(source_id)                → check metadata and page count
get_source_outline(source_id)        → find the right section (TOC)
get_source_pages(source_id, "5-7")   → read exact pages
```

Do not call `get_source_pages` without first checking `get_source_outline` on documents > 10 pages.

---

## Browsing by Category

When the user asks "what's in the X category" or wants to explore a knowledge type:

```
list_knowledge_types()               → see all categories + doc counts
get_knowledge_type_docs(slug)        → docs in that category
list_wiki_pages(knowledge_type=slug) → wiki pages tagged to that category
```

---

## Token Discipline

| Start with | When to stop |
|-----------|-------------|
| `search_wiki` | If summary has the answer |
| 2-4 wiki pages | Usually sufficient for standard queries |
| `get_source_outline` | Before reading pages of a long source |
| `get_source_pages` | Read only the specific pages needed |

Never read more than 6 wiki pages for a standard query. For deep mode, cap at 15 unless the question explicitly demands full coverage.

---

## RBAC Notes

- Your MCP token determines which knowledge types you can access.
- `search_wiki`, `read_wiki_page`, and `list_wiki_pages` automatically filter to your allowed types.
- `list_sources` and `get_source_pages` enforce per-source scope.
- If you get "Access denied" or "out of scope", the content exists but is outside your token's permissions — tell the user and suggest they contact an admin.
