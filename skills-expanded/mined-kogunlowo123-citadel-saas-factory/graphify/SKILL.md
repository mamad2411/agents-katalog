# Graphify — Knowledge Graph Integration

## Description
Build and query a knowledge graph from the codebase using Graphify. Navigate code by structure and relationships instead of raw file search.

## When to Use
- Before exploring an unfamiliar codebase
- When understanding cross-module dependencies
- When answering architectural questions
- Before making changes that span multiple files

## Commands
- `/graphify .` — Build knowledge graph from current directory
- `/graphify . --update` — Incremental update
- `/graphify . --wiki` — Generate wiki documentation
- `/graphify . --obsidian-dir <path>` — Export to Obsidian

## Output
- `graphify-out/graph.html` — Interactive visual graph
- `graphify-out/GRAPH_REPORT.md` — God nodes, connections, suggested questions
- `graphify-out/graph.json` — Queryable graph data

## Integration
The PreToolUse hook ensures Claude consults the graph before every Glob and Grep call, reducing token usage by up to 71x.

## LLM Wiki Integration
Graphify's output feeds directly into the [[../../../docs/vault/wiki/index|LLM Wiki]] entity and concept pages. Run:

```bash
graphify . --obsidian-dir docs/vault/wiki/knowledge-graph
```

This produces backlinked wiki pages from the AST-parsed codebase structure under `docs/vault/wiki/knowledge-graph/`. The `wiki-curator` agent can then cross-link these machine-generated pages into the entity and concept pages it maintains, so the compiled knowledge base stays in sync with the actual code.

The full sync loop:

```bash
make wiki-sync    # graphify + wiki lint
```

See [[../llm-wiki/SKILL|llm-wiki skill]] and [[../../rules/llm-wiki|llm-wiki rule]] for the Karpathy compounding-knowledge pattern this integrates with.

## Vault Links

- [[../llm-wiki/SKILL|llm-wiki skill]]
- [[../../rules/llm-wiki|llm-wiki rule]]
- [[../../agents/wiki-curator|wiki-curator agent]]
- [[../../../docs/vault/wiki/index|Wiki Index]]
- [[../../../docs/vault/SCHEMA|Wiki Schema]]
