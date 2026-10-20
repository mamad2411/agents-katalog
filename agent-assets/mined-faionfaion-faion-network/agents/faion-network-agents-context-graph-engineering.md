# Context Graph Engineering

## Summary

**One-sentence:** Produces a Graph Design Record that first proves a graph is warranted at all, then constrains edge construction, traversal budget and integrity checks so the graph never costs more than the retrieval it replaces.

**One-paragraph:** Graph retrieval is sold as an upgrade over search. On the only shared benchmark it is not: flat retrieval with reranking beats graph retrieval on fact-shaped questions while costing 1/40th the query tokens, and graph-global search costs ~380x flat. Graphs earn their keep on a narrow band — multi-hop synthesis over data that genuinely has M:N structure, cross-branch links, cycles or temporal validity. This methodology makes that gate explicit and machine-checkable. Most honest records terminate at the gate with `warrant: none`, which is the correct and cheapest outcome. When a warrant does hold, seven rules keep construction derived rather than extracted, traversal bounded rather than open, and integrity gated in CI rather than assumed.

**Ефективно для:**

- Anyone about to adopt GraphRAG or a knowledge graph because it sounds like the mature choice.
- Retrieval that already costs graph-level tokens while delivering tree-level capability — the common silent case.
- Agent memory where facts expire and "was true" must be distinguishable from "is true".
- Code navigation over a repo large enough that grep-and-dump has stopped fitting the context window.

## Applies If (ALL must hold)

- A retrieval or agent-memory structure is being chosen or replaced.
- Query cost per lookup is measurable and someone is paying it.
- The corpus is large enough that dumping it whole is not an option.

## Skip If (ANY kills it)

- The corpus fits in the context window — structure is irrelevant, dump it.
- Retrieval is single-hop lookup by known identifier — a map wins.
- No one has measured the incumbent structure's cost per query yet; measure first, this methodology needs that number as input.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules. R1 is the gate most systems fail; R2-R7 apply only after it passes. |
| `content/02-output-contract.xml` | The Graph Design Record: every field, the stop condition, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six production failure modes with symptom, cause and the rule that prevents each. |
| `content/06-decision-tree.xml` | Routing from observable data properties to graph / tree / flat. |
| `scripts/validate-context-graph-engineering.py` | Validates a record; enforces the gate, the traversal arithmetic, and the CI integrity checks. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/graph-design-record.yaml` | Fill-in record for a proven warrant; ships valid against the contract. |
| `templates/graph-design-record-no-graph.yaml` | The gate-stop record — four fields, the most common correct outcome. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `multi-agent-design-patterns` — pattern choice for the orchestration graph; this methodology is about the knowledge graph, a different object under the same word.
- `mcp-resource-vs-tool-vs-prompt` — how retrieved context reaches the agent once the structure is chosen.
- `architecture-decision-records` — the Graph Design Record is an ADR with a fixed schema; log it the same way.
