---
name: graphify
description: "any input (code, docs, papers, images) → knowledge graph → clustered communities → HTML + JSON + audit report. Use when user asks any question about a codebase, project content, architecture, or file relationships — especially if graphify-out/ exists. Provides persistent graph with god nodes, community detection, and BFS/DFS query tools."
trigger: /graphify
---

# /graphify

Turn any folder of files into a navigable knowledge graph with community detection, an honest audit trail, and three outputs: interactive HTML, GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md.

## Usage

```
/graphify <path>                         # full pipeline (use . for current dir)
/graphify <path> --mode deep             # richer INFERRED edges
/graphify <path> --update                # incremental re-extraction
/graphify <path> --cluster-only          # rerun clustering on existing graph
/graphify <path> --no-viz                # skip visualization
/graphify <path> --svg / --graphml       # additional export formats
/graphify <path> --neo4j / --neo4j-push  # Neo4j export or direct push
/graphify <path> --mcp                   # start MCP stdio server
/graphify <path> --watch                 # auto-rebuild on file changes
/graphify add <url>                      # fetch URL, save to ./raw, update graph
/graphify query "<question>" [--dfs] [--budget N]   # BFS or DFS traversal
/graphify path "A" "B"                   # shortest path between concepts
/graphify explain "Node"                 # plain-language node explanation
```

## What graphify is for

Three things your AI assistant alone cannot:
1. **Persistent graph** — relationships in `graphify-out/graph.json` survive across sessions.
2. **Honest audit trail** — every edge tagged EXTRACTED, INFERRED, or AMBIGUOUS.
3. **Cross-document surprise** — community detection finds connections across files you'd never ask about.

## What You Must Do When Invoked

If invoked with `--help` or `-h` only, print the Usage section above verbatim and stop. Do not run commands.

If no path given, use `.`. Do not ask for a path.

If `graphify-out/` exists, use `graphify query`/`explain`/`path` for orientation before broad grep. Dirty artifacts are expected; skip only if the task is about stale graph output or the user says not to use it.

### Step 0 — Load pipeline reference

Read [references/pipeline.md](references/pipeline.md) for the full extraction pipeline (Steps 1-9).

Read [references/subcommands.md](references/subcommands.md) for subcommand docs (`--update`, `--cluster-only`, `query`, `path`, `explain`, `add`, `--watch`, hook, CLAUDE.md integration).

Execute the pipeline steps from those files exactly as written.

### Step 10 — Final report

After the pipeline finishes, paste from GRAPH_REPORT.md: God Nodes, Surprising Connections, Suggested Questions. Do NOT paste the full report.

Then pick the most interesting suggested question — the one crossing the most community boundaries — and ask:

> "The most interesting question this graph can answer: **[question]**. Want me to trace it?"

If yes, run `/graphify query "[question]"` and walk them through the answer. End each answer with a natural follow-up so the session feels like navigation, not a one-shot report.

## Honesty Rules

- Never invent an edge. If unsure, use AMBIGUOUS.
- Never skip the corpus check warning.
- Always show token cost in the report.
- Never hide cohesion scores behind symbols.
- Never run HTML viz on >5,000 nodes without warning.
