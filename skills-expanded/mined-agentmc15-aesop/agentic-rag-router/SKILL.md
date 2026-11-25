---
name: agentic-rag-router
description: Choose the cheapest sufficient retrieval strategy for a query before answering. Use whenever the system has multiple retrievers (vector, hybrid, graph, metadata, summary) and needs to decide how to fetch evidence for a question. Trigger on any retrieval/QA task where query types are mixed.
---
# agentic-rag-router

The point of agentic RAG isn't "more agents" — it's **adaptive retrieval**: use the cheapest
sufficient behavior for the query at hand. This skill is the router.

## Routing rules
- exact names / IDs / error codes / config keys / quoted strings → `hybrid_search`
- simple conceptual / single-hop lookup → `vector_search`
- relationship / dependency / impact / lineage / "connected to" → `graph_search`
- scoped by region / tenant / version / date / department → `metadata_filtered_search`
- broad summary / theme → `hierarchical_summary_search`
- ambiguous wording → multi-query expansion
- weak evidence after retrieval → corrective retry (regrade, switch retriever, decompose)
- high-risk answer → add a critic/verification pass

## Output (JSON, user-safe — no hidden chain-of-thought)
```json
{"query_type": "...", "selected_tool": "...", "tool_args": {}, "decision_reason": "brief", "needs_fallback": false}
```

## Notes
- Don't answer the user here; only return the routing decision.
- This is the runtime cousin of the comparison harness in `evals/python/rag_compare/`, which
  measures which strategy actually wins per query class at what cost/latency.
