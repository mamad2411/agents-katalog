# Vector DB Tuning Runbook

## Summary

**One-sentence:** Produces a tuning runbook for a vector store: HNSW / IVF parameters, ef_search vs recall, shard sizing, refresh cadence, with rollback steps and recall-vs-latency targets.

**Ефективно для:** RAG engineers tuning a production vector store on latency / recall regression; SREs running capacity reviews on pgvector / Qdrant / Weaviate / Milvus; ML-ops setting refresh cadence after a re-embed.

**One-paragraph:** This methodology pins the recurring decision around "vector-db-tuning-runbook" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Vector store backs a production RAG surface with traffic.
- Recall and latency targets exist for the surface.
- Recent regression observed OR upcoming load change.
- Owner exists for the index after tuning.

## Skip If (ANY kills it)

- Index has <100k vectors — brute-force is fine, tuning overhead unjustified.
- Vendor manages tuning end-to-end (managed serverless RAG).
- Surface is experimental with no traffic.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current index parameters | config (yaml / json) | ops repo |
| Recall + latency telemetry (30d) | metrics dump | observability |
| Eval ground-truth set | JSONL ≥100 queries | RAG owner |
| Capacity headroom | GB / vCPU | SRE |
| Runbook owner | handle / email | team roster |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[embedding-spike-runbook]]` | embedding-side issues triaged first |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_parameter_sweep` | haiku | Template fill from current parameters. |
| `synthesize_tradeoff` | sonnet | Recall vs latency tradeoff per surface. |
| `escalate_replatform` | opus | Cross-store replatform decision. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vector-db-tuning-runbook.json` | JSON Schema for the Vector DB Tuning Runbook output contract |
| `templates/vector-db-tuning-runbook.md.j2` | Markdown skeleton with the required fields |
| `templates/vector-db-tuning-runbook.md` | Markdown skeleton with the required fields Generated from `templates/vector-db-tuning-runbook.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-tuning-runbook.py` | Enforce the Vector DB Tuning Runbook output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[embedding-spike-runbook]] — incident sibling on the embedding pipeline.
- [[weekly-rag-spotcheck-protocol]] — feeds recall regression signal.
- [[methodology-corpus-licence-bundle]] — corpus-licence trail upstream.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.
