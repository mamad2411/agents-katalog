---
name: filter
description: Precision RAG search over your Obsidian vault. Find exactly and precisely the relevant information on a topic using multi-strategy retrieval, passage-level chunking, and AI reranking. Use when you need exact matches, precise extraction, or to filter vault content to only what's relevant.
---

# Filter Skill

Precision RAG: returns only the most relevant passages on a topic using multi-strategy retrieval, passage-level chunking, and AI reranking.

**Filter vs RAG:** Filter finds exactly where X is discussed (precise passages). RAG answers "what do I know about X?" (broad synthesis).

## Usage

```bash
python3 _scripts/filter_query.py "Alpha Vantage API"
python3 _scripts/filter_query.py "habit tracking" --expand --save
```

## Options

- `query` — Topic to search for (required)
- `--threshold N` — Min relevance score 0–10 (default: 7; use 8+ for stricter)
- `--top-k N` — Max passages to return (default: 15)
- `--expand` — Include wikilink neighbors (hybrid mode)
- `--no-rerank` — Skip AI reranking (faster, less precise)
- `--save` — Save to vault

## Output

`Sources/Filter - YYYY-MM-DD.md` (passages with `[[note]]` citations and relevance scores)
