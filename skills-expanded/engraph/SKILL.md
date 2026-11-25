---
name: engraph
description: Index and search document collections using hybrid semantic + graph + full-text search. Use when users need to search knowledge bases, find connections between documents, discover related content via link graphs, or query indexed markdown collections.
license: MIT
compatibility: Requires engraph CLI. Install via `brew install devwhodevs/tap/engraph` or from GitHub releases.
metadata:
  author: jsynowiec
  version: "1.0.0"
allowed-tools: Bash(engraph:*), mcp__engraph__*
---

# Engraph — Hybrid Semantic & Graph Search for Document Collections

Local knowledge engine for markdown document collections. Combines semantic embeddings, full-text search (BM25), wikilink graph traversal, temporal scoring, and cross-encoder reranking.

## Status

!`engraph --version 2>/dev/null || echo "Not installed: brew install devwhodevs/tap/engraph"`

## Indexing

```bash
engraph index /path/to/documents        # Incremental; only changed files re-embedded
engraph index /path/to/documents --rebuild
engraph status                          # File count, stats, index freshness
engraph clear                           # Drop the index (--all also removes models)
```

## Search

```bash
engraph search "how does the auth flow work"
engraph search "performance regressions last month" --explain
engraph search "architecture decisions" -n 5 --json
```

| Flag              | Description                                    |
| ----------------- | ---------------------------------------------- |
| `-n, --top-n <N>` | Number of results (default: from config or 10) |
| `--explain`       | Show per-lane RRF score breakdown              |
| `--json`          | Machine-readable JSON output                   |

### Query Tips

- **Conceptual / vague**: Use natural language. The orchestrator classifies intent and boosts semantic weight automatically.
- **Keyword-heavy**: Exact terms, identifiers, and names work well via the BM25 lane.
- **Temporal**: "last week", "yesterday", "March 2026" — the temporal lane activates automatically.

## Graph Inspection

```bash
engraph graph show "path/to/note.md"    # Connections for a document
engraph graph show "#docid"             # By document ID
engraph graph stats                     # Nodes, edges, density
```

## Context Queries

```bash
engraph context topic "authentication" --budget 8000
engraph context who "Person Name"
engraph context project "Project Name"
engraph context vault-map                 # Collection structure overview
engraph context read "path/to/note.md"    # Full content + metadata
engraph context list --tags architecture  # Filter by tags, folder, created_by, etc.
```

> Health diagnostics (orphans, broken links, stale notes, tag hygiene) are exposed through the MCP `health` tool and the HTTP `GET /api/health` endpoint — see `references/http-rest-api.md`.

## Setup

```bash
engraph index /path/to/documents
engraph search "your query"
```

## References

- `references/mcp-setup.md` — configure engraph as an MCP server (Claude Code, Claude Desktop).
- `references/http-rest-api.md` — HTTP REST API endpoints, authentication, and examples for web agents and scripts.
