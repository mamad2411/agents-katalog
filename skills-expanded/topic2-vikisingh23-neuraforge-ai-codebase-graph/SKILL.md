---
name: codebase-graph
description: Build a queryable knowledge graph of the codebase before generating or reviewing code, so "does this already exist?" is answered by evidence instead of a quick grep
category: developer-tools
triggers:
  - "use codebase-graph"
  - "map the codebase"
  - "what connects to"
---

# Codebase Graph

Backs the Reuse Decision Tree's first step — "search codebase, does something
similar exist?" (`ARCHITECTURE_PRINCIPLES.md` §3) and the Minimal Solution
Principle's second rung (`MINIMAL_SOLUTION.md`) — with a tool built for that
exact question: [graphify](https://github.com/Graphify-Labs/graphify)
(package name on PyPI: `graphifyy`). Entirely optional — every forge/reviewer
agent works without it, this just makes "search first" scale past what grep
can reliably answer on a large or unfamiliar codebase.

## When to Use It

Before generating code in a codebase you haven't already mapped this session,
and especially before creating a new file, entity, or service — this is where
"I didn't realize X already does this" gets caught before it ships as a
duplicate.

## Setup (once per machine)

```bash
uv tool install graphifyy
# or: pipx install graphifyy / pip install graphifyy
```

If `graphify` isn't on `$PATH`, skip this skill and fall back to plain
search (Grep/Glob) — don't block on it.

## Usage

```bash
# Build the graph (local AST parsing only, no LLM/API key needed, no network call)
graphify update . --code-only

# Ask it directly instead of re-reading files by hand
graphify query "what handles order creation?"
graphify explain "OrderService"
graphify path "OrderController" "PaymentGateway"
```

Output lands in `graphify-out/` (`graph.json`, `graph.html`, `GRAPH_REPORT.md`)
— add `graphify-out/` to `.gitignore` if it isn't already there, it's a local
cache, not something to commit.

## How to Fold This Into Generation/Review

1. Run `graphify update . --code-only` once at the start of a session touching
   an unfamiliar part of the codebase.
2. Before creating a new entity/service/component, `graphify query` for it by
   name or responsibility instead of assuming it doesn't exist.
3. Check `GRAPH_REPORT.md`'s "God Nodes" and "Surprising Connections" sections
   when reviewing architecture — they surface coupling a reviewer skimming
   diffs would miss.
4. Re-run `graphify update .` (same flags) after a batch of changes — it's
   incremental, not a full re-scan.

## What This Doesn't Replace

Anti-pattern checks (`rules/anti-patterns/{stack}.md`), the architecture
reviewer, and the eval suite are unaffected — this is purely a *search* tool,
not a correctness check. A clean graph doesn't mean the code is right, only
that you know what else touches it before you change it.
