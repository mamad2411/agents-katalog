---
name: kg-view
description: Open a knowledge graph in the browser with glassbrain. Works on glassbrain JSON, Graphify graph.json, Understand-Anything knowledge-graph.json, MCP memory.jsonl and markdown notes folders (Obsidian, LLM wikis). Use when asked to show, open or look at a graph, a memory or a notes vault.
---

# kg-view

1. Find the graph if no path was given: `kg/`, `graphify-out/graph.json`, `.ua/knowledge-graph.json` (or `.understand-anything/`), `memory.jsonl`, a notes folder.
2. Run `npx glassbrain validate <path>`. Report errors in a sentence; they do not block viewing.
3. Run `npx glassbrain view <path>`. It writes one self-contained html file and opens it; tell the user the path it printed.

A folder of sub-folders (`1-…`, `2-…`) opens as versions with a "compare with previous" switch. `--out <file.html>` saves the page somewhere to share.
