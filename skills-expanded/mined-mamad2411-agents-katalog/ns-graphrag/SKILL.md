---
name: ns-graphrag
description: "(NS) Build a complete GraphRAG process — closed ontology, semantic text units, schema-locked extraction with citations, entity resolution, logical edges with evidence and mentions, filtered sets and aggregate answers with per-row citations, path traversal, optional discovery hypotheses, dual embeddings (units + entity descriptions), ACL-before-search, cited answers. Use whenever the user wants GraphRAG, a knowledge graph over documents, multi-hop retrieval, entity/relationship extractors, indirect-link or grouping analytics, or grounded structured extraction from unstructured files — even if they only say RAG, NER, knowledge graph, or cited Q&A. Do NOT use for Postgres schema/mode choice alone (`ns-postgres-rag` first). Do NOT use for competing vector stores, free graph query languages, or co-occurrence-as-edge designs."
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.1"
depends:
  - ns-harness
  - ns-postgres-rag
---

# GraphRAG process

End-to-end **process knowledge** to construct GraphRAG on the retrieval layer designed by `ns-postgres-rag`.

**Analyze. Specify the pipeline. No application language or product names.**

Storage, indexes, hybrid rank, recursive hop caps, evidence/mention DDL, and the Retrieval Design Report live in `ns-postgres-rag`. This skill owns **how knowledge is extracted, persisted, queried, and cited**.

## Central rule

A hop is a **stored typed edge** with evidence rows. Similarity proposes **candidates**. Co-occurrence does not create edges. Every operator answer cites **verbatim source spans** (or refuses). Denied records are **omitted**, never explained as “no access.”

Canonical hop (**illustration only**): `company → contract → invoice → payment`. Derive the corpus chain in P0.

## Split with ns-postgres-rag

| Question | Owner |
| -------- | ----- |
| Vector vs hybrid vs GraphRAG? DDL, HNSW, hop CTE, evidence/mention tables, return fields | `ns-postgres-rag` |
| Ontology, extractor contract, document typing, answer shapes, citations, ACL-before-search, discovery gate | **this skill** |

If Gate 2 is not relational GraphRAG, **stop**. Do not invent graph tables “for later.”

## Language ban

Instructions, reports, and extractor contracts name **concepts** (text unit, surviving identity, logical edge, evidence, mention, answer shape). Do **not** name programming languages, frameworks, UI kits, container runtimes, or vendor model SKUs. Model **roles** only: `extract`, `embed`, `classify`, `summarize`, `compose`.

SQL/DDL shapes stay in `ns-postgres-rag` snippets.

## Boot (mandatory)

1. `../../ns-harness/references/session-boot.md` — Session boot (blocking).
2. Read `../ns-postgres-rag/SKILL.md` routing + Gates 1–2. If no approved Retrieval Design Report and mode is GraphRAG, fill or demand that report first.
3. Scan corpus formats, existing cadastre keys, permission model, question archetypes.
4. Continue this skill.

**Success:** inventory + GraphRAG mode justified. **Failure:** extractor prompt before ontology, or graph without N≥2 split-chain need.

## Flow

boot → **P0** ontology lock → **P1** unstructured → text units + quality gate → **P2** schema-locked extract → **P3** resolve identity → **P4** persist logical edges + evidence + mentions → **P5** embed units + entity descriptions → **P6** answer shapes + graph contract → **P7** GraphRAG Process Report → human approve → `ns-spec-driven`.

Opt-in **discovery** (cited hypotheses, no write-back) only when a declared archetype is outside the six answer shapes — `references/discovery-layer.md`.

Interactive query **preempts** ingest jobs. Ingest is staged, idempotent, retry-per-stage.

## P0 — Ontology lock (blocking)

Fixed vocabularies. Extractor may not invent types. Derivation procedure (not a canned list): `references/ontology.md`.

Lock before any extract batch:

- Entity types (closed list) aligned to host registry schema.
- Relation types (closed list, directed meaning) derived from declared question hop chains.
- Optional claim/covariate types (default **off** until prompts tuned).
- Surviving-identity keys per type (identity ladder); mention-only types declared.
- Ontology version id on every extract batch.

Open vocabularies fragment the graph and break identity merge, traversal, and citation integrity.

## P1 — Unstructured → text units

Deterministic extract from bytes. Each **text unit** keeps `document_id`, ordinal, page/span, **character offsets**, content hash, **text-quality band**. Prefer paragraph / section boundaries over mid-sentence cuts. Overlap exists so relations that straddle units still extract. Giant whole-file units forbidden. Degraded text routes to re-extract or failure queue — never silent index.

Detail: `references/unstructured-to-units.md`. Upsert identity: `../ns-postgres-rag/references/ingestion-pipeline.md`.

## P2 — Schema-locked extraction

Per text unit, one structured pass:

1. Entities: `name`, `type` (ontology), `description`, **role-in-context**, **identifier fields** (per-type; do not invent).
2. Relations: `source`, `target`, `type` (ontology), `description`, **source span**, provenance class `EXPLICIT` or `INFERRED`, **`confidence` (0–1)**.
3. Optional document-level fields (title, authors, dates) as **nested** `{ value, sources[], reasoning }` — refuse the field if context is insufficient.
4. Document class + confidence bands (classified / low / unclassified; tie margin demotes).
5. Out-of-vocabulary findings → **unmapped-candidate** queue, not nearest-type coercion.

Extractor instructions are **build artifacts** assembled from the approved ontology — `references/structured-extraction.md`, `templates/extractor-instruction.template.md`.

Cap triplets per unit. Validate types against ontology; drop illegal labels. Descriptions feed anchor mapping and synthesis — bare triples starve composition.

## P3 — Resolve identity

Deterministic block, then vector **candidates**, then confirm — ordered **identity ladder** per type; normalized name is **never** identity for person-like types. Model **extracts identifiers**; deterministic layer **resolves** them.

Unresolved anchors return **ranked candidates** to the caller — no silent guess.

Detail: `references/graph-assembly.md`, `../ns-postgres-rag/references/entity-resolution.md`.

## P4 — Persist logical edges, evidence, mentions

1. **Logical edge** unique by `source + type + target`. Upsert: strongest confidence wins; provenance class does not downgrade; **`review_status`** from relation confidence mapping — `references/structured-extraction.md` § Relation confidence → review_status (lock numbers in report); on conflict promote to `fact` only.
2. **Evidence** append per attestation: document, unit, quoted span, confidence. One edge, many evidences — not one row per attestation.
3. **Mentions**: unit-to-entity with role-in-context — substrate for filtered sets, counts, synthesis; not an edge.
4. **File vs business record**: distinct anchors; explicit file-to-file refs stored; shared entity = discovered path only.
5. **Proposals** (proposed records/links) are not facts, not traversable; confirmation policy declared in report.
6. Persist **`review_status`** from cited mapping; traversal uses **`fact`** only. `DERIVED` paths are query results — never persisted as edges.

Detail: `references/graph-assembly.md`.

## P5 — Embeddings

Embed, with model id + dimension on every row:

| Object | Use |
| ------ | --- |
| Text unit | Vector / hybrid lookup; local evidence |
| Entity description | Anchor mapping for path and set filters |

Reuse existing lexical index for hybrid rank when present — do not propose rebuild without cause.

Versioned re-embed: `../ns-postgres-rag/references/ingestion-pipeline.md`.

## P6 — Answer shapes + graph contract

Route by **answer shape**, not a single global/local switch.

| Shape | When |
| ----- | ---- |
| **Unit / vector** | Topic in one unit; no hop chain |
| **Path** | Named anchors; “how does A reach B”; N≥2 hops |
| **Filtered set** | Entity set with attribute predicates + optional time window |
| **Count / aggregate** | Group-by or totals; **per-row** provenance |
| **Anchor synthesis** | Scoped summary when a record is opened |
| **Document correlation** | Fresh upload vs registry; includes unregistered mentions |

**Scope restriction** (collection, import origin, document type) applies with authorization **before** ranking — never after.

**Temporal predicates** on edge period and record time are first-class filters.

Traversal: capped recursive walk (`../ns-postgres-rag/references/multi-hop-traversal.md`). Default **depth ≤ 5**. **Per-hop discipline**: authorization, type/confidence filters, top-N, visited set **inside** each step; denied node is **not** a bridge. **Batch expansion**: one read per hop over anchor set — never per-node reads. **No model call per hop** — model at extract and compose only.

Compose answers only from retrieved units/paths/evidence. If evidence missing: refuse. Every asserted fact carries citations.

Canonical graph query (English wire names):

```
query_knowledge_graph
{ anchor_ids[], anchor_type, edge_types[], max_depth (≤ 5), period?, scope?, limit?, include_evidence? }
→ { nodes[], edges[], paths[], candidates[]?, telemetry }
```

**Telemetry envelope**: hops executed, examined vs returned, cut reason, stage latencies, cache hit.

Forbidden: free SQL/Cypher-style tools; unbounded depth; treating pending_review as facts; denied node as bridge; model per hop.

Operator visualization shows the **query path**, not the whole graph.

Detail: `references/query-modes.md`, `references/access-and-citation.md`.

## Role decomposition

Implementation must separate identity resolver, traversal executor, entity/edge/evidence/mention repositories, authorization service, cache, and telemetry — detail: `references/graph-assembly.md`. Class/module layout = `ns-spec-driven`.

## P7 — GraphRAG Process Report

Copy `templates/graphrag-process-report.md`. Fill every section. Human approve before `ns-spec-driven`.

## Reference map

| Reference | Read when |
| --------- | --------- |
| `references/ontology.md` | P0; derivation; unmapped queue |
| `references/unstructured-to-units.md` | P1; quality gate; offsets |
| `references/structured-extraction.md` | P2; extractor contract |
| `templates/extractor-instruction.template.md` | P2; build artifact shape |
| `references/graph-assembly.md` | P3–P4; evidence; mentions |
| `references/discovery-layer.md` | Opt-in analytics only |
| `references/query-modes.md` | P6; six shapes |
| `references/access-and-citation.md` | ACL, untrusted input, cache |
| `references/process-eval.md` | Golden set, metrics |
| `references/anti-patterns.md` | Before marking report done |
| `../ns-postgres-rag/references/*` | Schema, resolution, hops, scale |

## Handoff to ns-spec-driven

After **human approval** of Retrieval Design Report **and** GraphRAG Process Report:

```markdown
## GraphRAG implementation planning
- Retrieval report: path (approved)
- Process report: path (approved)
- Ontology: entity types / relation types / version id
- Extract stages: units → extract → resolve → persist (edge+evidence+mention) → embed
- Answer shapes: unit | path | filtered set | count | synthesis | document correlation
- Discovery: off | on (archetype + gate)
- Graph query: query_knowledge_graph; max_depth cap; telemetry envelope
- Eval: evidence precision, path accuracy, set completeness, citation faithfulness, refuse-when-empty
- Out of scope for this skill: application source code
```

## Stop conditions

| Condition | Action |
| --------- | ------ |
| Mode is not GraphRAG | Stay on `ns-postgres-rag`; no extractor graph |
| Similarity or co-occurrence proposed as stored edge | Refuse |
| Ontology not locked | Block P2 |
| Free graph query language | Refuse |
| Competing vector store as default | Stay on `ns-postgres-rag` store |
| Human wants app code now | Reports first; then `ns-spec-driven` only |

## Forbidden

- Application languages, frameworks, vendors, model SKUs
- Co-occurrence or embedding distance as `edge`
- Modularity grouping as a pipeline stage without a declared discovery archetype
- One edge row per attestation (use logical edge + evidence append)
- Normalized name as surviving identity for person-like types
- Persisting derived traversal paths as edges
- Answering filtered set / count questions by path-walking alone
- Presenting discovery findings as facts or writing them back as edges
- Scope restriction after ranking
- Denied node as intermediate bridge
- Model call per graph hop
- Per-node reads during batch expansion
- Indexing degraded text without a quality band
- Committing proposed records without declared confirmation policy
- Cache key without authorization context or graph version
- Dumping whole documents into generation
- Answering without citations when a fact is asserted
- Revealing authorization failures to the caller
