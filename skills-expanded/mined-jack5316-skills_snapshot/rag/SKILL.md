---
name: rag
description: Retrieval-Augmented Generation over your Obsidian vault. Query your knowledge base with hybrid retrieval (keyword + graph expansion via wikilinks). Inspired by LightRAG. Use when you want to ask questions about your notes, search your vault with AI synthesis, or /rag.
---

# RAG Skill

Retrieval-Augmented Generation over your Obsidian vault. Uses Python for retrieval (ripgrep + wikilink graph) and AI only for synthesis.

## Usage

```bash
python3 _scripts/rag_query.py "What do I know about AI agents?"
python3 _scripts/rag_query.py "Summarize my notes on habits" --mode hybrid --save
```

## Options

- `query` — Question to answer (required)
- `--mode {naive,local,hybrid}` — naive: keyword only; local: keyword + wikilink expansion; hybrid: broadest (default)
- `--top-k N` — Max notes to retrieve (default: 12)
- `--depth N` — Graph expansion depth (default: 1)
- `--save` — Save response to vault

## Output

`Sources/RAG Query - YYYY-MM-DD.md` (with `[[wikilinks]]` citations)
