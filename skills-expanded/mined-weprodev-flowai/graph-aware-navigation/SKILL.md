---
name: graph-aware-navigation
version: "1.0"
description: >
  Navigate the codebase via FlowAI's compiled knowledge graph instead of
  searching raw files. Mandatory context for all pipeline agents.
---

# Graph-Aware Navigation

## Overview

This project maintains a **compiled knowledge graph** of its codebase under
`.flowai/wiki/`. The graph engine always runs a **structural** pass (imports,
links, spec traceability, function nodes). An optional **semantic** pass (LLM-driven
concepts and inferred edges) runs only when `graph.semantic_enabled` is `true` in
`.flowai/config.json` — it adds cost and latency, so keep it off unless you need it.

**Always navigate via the graph first.** Raw file reads are for drilling into
specific locations the graph has already pointed you to.

## Navigation Protocol

### 1. Start at GRAPH_REPORT.md

Before any task, read `.flowai/wiki/GRAPH_REPORT.md`. It contains:
- **God nodes** — the highest-degree hubs in the codebase (the files everything depends on)
- **Community summaries** — clusters of closely-related modules
- **Suggested queries** — pre-generated questions about the architecture
- **Contradiction flags** — relationships the system marked as ambiguous

This is your architectural map. Reading it before touching any file is mandatory.

### 2. Use index.md as a Catalog

`.flowai/wiki/index.md` lists every wiki page with a one-line summary and its
source count. Before asking "where is X implemented?", scan the index for a page
about X. If a page exists, read it. If it doesn't, check GRAPH_REPORT.md for
which god node or community is most likely to contain it.

### 3. Use graph.json for Multi-Hop Reasoning

For questions like "what does module A depend on transitively?" or "which files
import the Config struct?", query `graph.json` directly. Edges have three
provenance tags:

- **EXTRACTED** — relationship is directly present in source (imports, function calls). High confidence.
- **INFERRED** — relationship was inferred from context by the semantic pass. Treat as a strong hypothesis.
- **AMBIGUOUS** — relationship was flagged for review. Do not assume it is correct.

### 4. Read Raw Files Surgically

After the graph directs you to a specific location (a god node, a community,
a wiki page that cites a file and line range), *then* read that file. Do not
start by reading files — the graph is your GPS.

### 5. Contribute Back to the Graph

If you discover a relationship, pattern, or architectural decision that is not
represented in the wiki, include it clearly in your response. The human can
run `flowai graph update` to integrate it. This is how the knowledge base
compounds over time.

## Token Efficiency

Reading the graph is dramatically more efficient than grepping raw files:
- GRAPH_REPORT.md gives you an architectural overview in ~2K tokens
- A typical wiki page gives you targeted knowledge in ~500 tokens
- graph.json lets you answer dependency questions without reading any source

Prefer this order:
```
GRAPH_REPORT.md  →  index.md  →  wiki/<topic>.md  →  graph.json  →  source files
```

## Announcements

When starting work that involves navigating the codebase, announce:
> "Reading .flowai/wiki/GRAPH_REPORT.md to orient via the knowledge graph."

This keeps the human informed and confirms you are following the graph-first protocol.
