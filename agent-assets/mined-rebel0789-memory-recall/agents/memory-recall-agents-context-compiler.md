# Context Compiler Agent Rules

Selection behavior is versioned and evaluation-gated. Preserve exact exclusion reasons, deterministic tie-breaking, scope filtering before ranking, and hard failure for missing required governance. Never optimize solely for more tokens or similarity.

Candidate sources are discovery only. Keep source logic provider-neutral,
workspace-scoped, policy-filtered, provenance-preserving, and deterministic.
Do not move global reranking, diversity selection, token-budget reservation,
context assembly, embeddings, graph traversal, external search, or adapter
activation into source implementations.

OAF-011 selection traces are internal contracts. Keep the public context
manifest schema-compatible for existing callers, and keep raw record text,
secrets, local paths, SQL, hidden reasoning, source bodies, and provider
configuration out of `selection.scoreBreakdowns`, selected decisions, and
excluded decisions.

OAF-012 durable manifests persist selected assembly and safe summaries. Keep
`compileContext(request, records)` synchronous and pure; add persistence only
through the durable composition path. Durable manifests may include selected
text exactly as assembled, but excluded decisions must not store raw text.
