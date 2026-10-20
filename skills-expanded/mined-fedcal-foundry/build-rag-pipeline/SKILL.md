---
name: build-rag-pipeline
description: Stand up or repair a retrieval pipeline the measurable way — audit the corpus, build a labelled query set before the index exists, baseline with lexical search, then add embeddings, hybrid fusion and reranking one variable at a time with recall@k recorded for each. Use when starting a RAG feature, when a RAG system returns wrong or empty answers, before changing an embedding model or chunker, or when someone proposes fixing retrieval by editing the prompt. Produces docs/rag/<index>.md, a versioned query set and a CI retrieval gate.
allowed-tools: Read Grep Glob Bash Write Edit
argument-hint: "[corpus-path] [--diagnose]"
user-invocable: true
model: sonnet
effort: medium
metadata:
  foundry.vertical: ai
  foundry.io: "requirement.v1 -> plan.v1 + docs/rag/<index>.md"
license: Apache-2.0
---

# Build a retrieval pipeline

One index at a time. The deliverable is a pipeline whose quality is a number someone can
reproduce tomorrow, not a demo that answered three questions correctly.

The order below is not a suggestion. Steps 1–3 exist because teams that skip them cannot tell
whether anything they did afterwards helped.

## When not to use this

- **The corpus is small enough to fit in the context window.** Then do not build a retrieval
  system: put the documents in the prompt. Retrieval is a cost you pay when you must.
- **The questions are answerable by a database query.** Text search over a rendered report is a
  worse version of `SELECT`. Build the query tool instead — see `agent-architect` step 4.
- **The documents have no text layer** (scanned images). OCR first; it is a separate project
  with its own error rate, and RAG on top of bad OCR fails invisibly.
- **You need answer-quality measurement** (faithfulness, tone, helpfulness) → `build-eval-suite`.
  This skill measures retrieval only, on purpose.

## Step 1 — audit the corpus before designing anything

```bash
CORPUS="${1:-./data}"
find "$CORPUS" -type f | wc -l
find "$CORPUS" -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head
find "$CORPUS" -type f -printf '%s\n' | sort -n | awk '{a[NR]=$1} END {print "p50",a[int(NR*0.5)],"p95",a[int(NR*0.95)],"max",a[NR]}'
find "$CORPUS" -type f -exec sha256sum {} + | awk '{print $1}' | sort | uniq -d | wc -l   # exact dupes
```

Then extract text from **three documents by hand** — the largest, one table-heavy, one that
looks like a scan — and read the output. Every RAG project that shipped garbage skipped this.

Record in the design doc: document count, format mix, size distribution, duplicate ratio,
language mix, whether tables survive extraction, whether any document needs OCR, and the access
boundaries (tenants, roles) the retriever must enforce.

**Gate:** if extraction produces unreadable text for a document class, that class is out of
scope until the parser is fixed. Say it now, in writing.

## Step 2 — write the labelled query set *before* the index

This is the artefact that makes everything else measurable, and it must not be produced by the
system you are about to measure.

- **≥ 50 queries**, phrased the way users actually phrase them (mine support tickets, search
  logs, chat history). Copy their typos and their jargon.
- **Stratify** and record the stratum: single-fact lookup, multi-document synthesis, comparison,
  temporal ("current policy"), identifier lookup (codes, part numbers), and **unanswerable**.
- **At least 15% unanswerable.** A retriever is graded on what it does not return as much as on
  what it does; without this stratum you cannot detect a system that never abstains.
- Label the **chunk-independent** ground truth: the source document id(s), and where possible the
  section/heading that answers it. Labelling document ids means the set survives a rechunk;
  labelling chunk ids does not.
- Store as JSONL at `evals/retrieval/<set>.v1.jsonl`, one object per line:

```json
{"id":"q-014","query":"quale versione del contratto vale dopo la proroga","stratum":"temporal","relevantDocs":["doc-882#sec-4"],"note":"answer only in the 2024 annex"}
```

Full construction protocol, including how to mine queries and how to label multi-hop questions:
`references/eval-set-construction.md`.

**Gate:** the set is committed to the repository and reviewed by someone who knows the domain.
Two labellers on a 20-item sample; disagreement above 20% means the questions are ambiguous, not
that the labellers are careless — rewrite them.

## Step 3 — lexical baseline first

Build BM25 (or your database's full-text search) over the raw documents and measure the set from
step 2. This takes an hour and it settles arguments for the rest of the project.

```sql
-- PostgreSQL full-text baseline; adapt the config to your corpus language
ALTER TABLE documents ADD COLUMN tsv tsvector
  GENERATED ALWAYS AS (to_tsvector('italian', coalesce(title,'') || ' ' || body)) STORED;
CREATE INDEX documents_tsv_idx ON documents USING gin (tsv);
SELECT id, ts_rank(tsv, q) AS rank
FROM documents, websearch_to_tsquery('italian', :query) q
WHERE tsv @@ q ORDER BY rank DESC LIMIT 20;
```

Record `recall@10` and `MRR` per stratum. This number is the bar every later configuration must
beat. It is common for lexical search to win outright on identifier and jargon strata — which is
exactly why hybrid retrieval exists, and why a dense-only design is a decision that must be
justified against data.

## Step 4 — chunk

Pick the strategy per document family (`references/chunking-recipes.md`), then enforce three
invariants at ingestion, failing loudly on violation:

1. Every chunk carries its heading path prepended to the text, so it stands alone.
2. Every chunk's token length is **below the embedding model's real input limit** — measure the
   limit, do not recall it. Over-long text is truncated silently and you will never see an error.
3. Every chunk carries: `source_id`, stable URI, heading path, `doc_version`, `effective_date`,
   `tenant_key`/ACL, `embedding_model`, `chunker_version`.

Sweep 3–4 candidate configurations against the step-2 set and keep the winner **by recall**, not
by intuition. Record every configuration and its score in `docs/rag/<index>.md`.

## Step 5 — embed and index

- Verify the metric matches the model: normalise vectors and use cosine, or use the metric the
  model card specifies. Sanity check: embed the same string twice, assert similarity ≈ 1.0; embed
  a known-related pair and a known-unrelated pair, assert the ordering.
- Apply the query/document instruction prefixes the model requires, in **one shared function**
  used by both the ingestion path and the query path. A prefix applied on one side only is a
  silent, hard-to-find quality loss.
- Stamp `embedding_model` on every row. Then keep this check in CI:

```sql
SELECT embedding_model, count(*) FROM chunks GROUP BY 1;  -- more than one row is an incident
```

- Configure ANN parameters deliberately and **measure approximate against exact** on a sample
  (`ef_search`, `nprobe` and their equivalents trade recall for latency). If you have not run
  that comparison, you do not know what your index is silently dropping.
- Write the reindex procedure now, not later: `.foundry/runbooks/<index>-reindex.md`, covering a
  full rebuild, an embedding-model swap with shadow index and cutover, incremental updates,
  and deletion propagation including caches.

## Step 6 — hybrid fusion and reranking

Add one at a time, measuring after each.

1. **Fusion.** Retrieve independently from lexical and vector search, fuse with Reciprocal Rank
   Fusion (`score(d) = Σ 1/(k + rank_i(d))`). RRF needs no cross-engine score calibration, which
   is why it survives retuning either engine. Sweep the candidate depth per engine.
2. **Filtering.** Apply metadata filters (tenant, date, document type) **inside** the search, not
   after it. Post-filtering silently returns fewer results than requested and looks like a
   retrieval failure. If the store cannot pre-filter, over-fetch and measure the recall loss on
   the most selective filter in your distribution.
3. **Reranking.** Cross-encode `(query, chunk)` over the fused candidates and keep the top n.
   Sweep the candidate count; stop where nDCG stops moving. Remember: a reranker cannot recover a
   chunk that recall never retrieved.

Record after each step: recall@k, MRR, nDCG@10, p95 latency, and cost per query. A configuration
that adds 400 ms for a 1-point nDCG gain is a decision for a human, so present it as one.

## Step 7 — the generation contract

Retrieval work is not finished until the answering side honours it:

- Context is delimited and labelled as data, with provenance per chunk (`prompt-engineer`).
- Every claim cites a chunk id, and **cited ids are validated against the ids actually
  retrieved** — a citation to an unretrieved chunk is a hallucination and must fail a test.
- Below a retrieval-score threshold the system abstains and says what it searched.
- The unanswerable stratum from step 2 is a passing test, not an aspiration.

## Step 8 — gate it in CI

Add a job that runs the retrieval evaluation against the frozen query set and fails on:

- `recall@10` below the recorded baseline minus the agreed tolerance (state the tolerance);
- any stratum regressing by more than the tolerance, even if the aggregate improved;
- more than one `embedding_model` present in the index;
- a cross-tenant leak test returning any row.

Retrieval evaluation is deterministic and needs no judge model, so it belongs on every pull
request that touches ingestion, chunking, the index or the query path.

## Step 9 — write it down

`docs/rag/<index>.md`, in this order: corpus audit with dates; answerable/unanswerable scope;
query set location and version; lexical baseline; every configuration tried with its metrics;
the shipped configuration with its hash; ANN-vs-exact recall measurement; latency and cost per
query; reindex and deletion runbook links; access-control model; open risks; review date ≤ 90
days.

Emit the accompanying `plan.v1` to `.foundry/blackboard/<wave>/build-rag-pipeline.json` with
waves for audit, query set, baseline, indexing, fusion/rerank and gating, and `outOfScope`
naming every document class and question class deliberately excluded.

## Exit criteria

1. Corpus audit recorded, with extraction verified by hand on three documents.
2. Labelled query set ≥ 50 items, ≥ 15% unanswerable, stratified, committed and reviewed.
3. Lexical baseline measured and recorded per stratum.
4. Chunk invariants enforced at ingestion with a loud failure on violation.
5. Embedding metric, prefixes and dimension verified by an executed sanity check.
6. Single-embedding-model check present in CI.
7. ANN recall measured against exact search on a sample.
8. Each of fusion, filtering and reranking measured independently, with latency and cost.
9. Citation validation and abstention behaviour covered by tests.
10. CI gate wired with a stated tolerance and a per-stratum rule.
11. Reindex and deletion runbook written; cross-tenant leak test passing.
12. `plan.v1` validates, `outOfScope` is non-empty, and `docs/rag/<index>.md` exists.

## Degradation

- **No real user queries available** → write them with a domain expert and label the set
  `expert-authored`; do not generate them from the corpus with a model and present the result as
  a measurement of retrieval.
- **No reranker** (no GPU, latency budget) → invest in fusion and chunking, record the accepted
  precision ceiling as a `risk.v1`.
- **Local model serving only** → enumerate the models actually pulled locally rather than
  assuming a catalogue, measure ingestion throughput first (it, not query latency, will be the
  constraint), and record the chosen model as a `decision` fact.
- **Store cannot pre-filter** → over-fetch, measure the recall loss, record it as a finding.
- **`superpowers` installed** → use `superpowers:systematic-debugging` for the `--diagnose` path:
  one hypothesis per stage (parse → chunk → embed → retrieve → fuse → rerank → generate), each
  falsified with a measurement before moving on.

## Deliberately not covered

Answer quality scoring (`build-eval-suite`), prompt wording (`prompt-engineer`), agent loops
around the retriever (`design-agent-tools`), vector-store operations and index sizing
(`foundry-dev:database-architect`), inference cost forecasting
(`foundry-economics:ai-cost-controller`), and lawful basis or retention for the indexed content
(`foundry-legal:privacy-engineer`).

## Bundled references

- `references/chunking-recipes.md` — per document family: contracts and policies, API docs and
  code, support tickets, spreadsheets and tables, transcripts, and long-form manuals.
- `references/eval-set-construction.md` — mining real queries, labelling protocol, strata
  definitions, inter-labeller agreement, and how to keep the set alive as the corpus changes.
- `references/retrieval-failure-modes.md` — nineteen ways retrieval fails, each with its
  diagnostic command or query and the fix that actually addresses it.
