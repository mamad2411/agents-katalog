---
name: vector-database-ingestion-pipeline-for-rag
description: >
  Builds and operates the ingestion pipeline that feeds a vector
  database for RAG — document chunking as a pipeline stage, batch
  embedding jobs, idempotent/resumable upserts, and re-indexing
  triggered by source-document updates. Use when a user asks to "build
  a pipeline to embed and load documents into our vector DB," "re-index
  when source documents change," "batch-embed a large corpus,"
  "the vector DB is missing/duplicating documents after a load job," or
  "our re-indexing job failed partway through and we're not sure what
  landed."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Vector Database Ingestion Pipeline for RAG

## Purpose

Getting a RAG system's vectors into its index reliably is a data
pipeline engineering problem, distinct from the retrieval design
question of *how* chunks should be shaped for good retrieval (covered
in [rag-pipeline-design](../rag-pipeline-design/SKILL.md)) and from the
index's own operational tuning (covered in
[vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md)).
This skill is specifically about the pipeline that runs chunking as a
production job stage, batches embedding calls reliably at scale,
upserts idempotently so a retried or partially-failed run doesn't
corrupt the index, and re-indexes when source documents change — the
plumbing that has to work correctly every single run, not the design
choices about what a good chunk or a good index configuration look
like. A RAG system with excellent chunking and retrieval design still
gives stale or duplicated answers if the pipeline feeding it is
unreliable.

## When to use

- Building a new ingestion pipeline to take a document source (a CMS, a
  file store, a ticketing system, a repo) and load embedded chunks into
  a vector index for the first time.
- Implementing re-indexing that triggers on source-document
  create/update/delete events, or designing a scheduled batch fallback
  when event-driven triggers aren't available for a given source.
- A bulk embedding/backfill job is slow, times out, or fails partway
  through, and it's unclear what state the index was left in.
- The vector index contains duplicate, missing, or stale chunks for
  documents that were re-published or deleted at the source.
- Scaling an ingestion pipeline from a one-time backfill to a
  continuously running production job.
- Changing the embedding model or chunking parameters and needing to
  re-process the entire corpus as a controlled operation rather than an
  ad hoc script run.

## Prerequisites & environment

- A source system that can report what changed and when — a webhook/
  event stream (preferred) or, at minimum, a reliable
  "last modified" timestamp or version field to poll on a schedule; a
  source with no change signal at all forces a full re-scan on every
  run, which doesn't scale.
- A stable, unique document identifier from the source system that
  chunk IDs can be deterministically derived from — this is what makes
  idempotent upserts and clean deletes possible (see step 2).
- The embedding model and vector index already chosen, with dimension/
  metric already validated (see
  [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md))
  — this pipeline assumes the target index configuration is correct,
  it does not validate it.
- A job runner/orchestrator (a workflow engine, a scheduled batch job,
  or a queue-consumer worker) capable of retrying a failed batch without
  reprocessing an entire run from scratch, and capable of running
  batches with bounded concurrency against both the embedding API and
  the vector index's write path.
- Storage for pipeline run state (a database table, or the vector
  index's own metadata) tracking, per source document: last-processed
  version/timestamp, chunk IDs produced, and last successful embed/
  upsert time — required for the idempotency and partial-failure
  recovery patterns below.

## Step-by-step guidance

1. **Run chunking as a discrete, versioned pipeline stage** with its
   configuration (strategy, size, overlap) tracked as pipeline config,
   not inline logic scattered across the ingestion script — chunking
   parameters are effectively part of the index's schema, and changing
   them (per
   [rag-pipeline-design](../rag-pipeline-design/SKILL.md)) means
   re-processing the whole corpus, not incrementally patching it:
   ```python
   def chunk_document(doc, chunk_size=400, overlap=60):
       # deterministic chunker — same doc + same config always
       # produces the same chunk boundaries and count
       return recursive_character_split(doc.text, chunk_size, overlap)
   ```

2. **Derive deterministic chunk IDs from the source document ID and
   chunk index**, never a random/generated ID — this is the single
   change that makes upserts idempotent and stale-chunk deletion
   possible:
   ```python
   def chunk_id(source_doc_id, chunk_index):
       return f"{source_doc_id}::chunk-{chunk_index:04d}"
   ```
   With deterministic IDs, re-running the pipeline against an unchanged
   document upserts the same IDs with the same content — a no-op in
   effect, not a duplicate. Without them, every re-run (including a
   retried failed run) creates new, duplicate vectors for the same
   content.

3. **Batch embedding calls, and make each batch idempotent and
   independently retryable** — a single failed batch in a 10,000-
   document backfill should not force reprocessing the other 9,999:
   ```python
   BATCH_SIZE = 100

   def process_batch(doc_batch, run_id):
       chunks = [c for doc in doc_batch for c in chunk_document(doc)]
       ids = [chunk_id(c.source_doc_id, c.index) for c in chunks]
       try:
           embeddings = embedding_model.embed_batch([c.text for c in chunks])
       except EmbeddingAPIError as e:
           log_batch_failure(run_id, doc_batch, e)
           raise  # let the orchestrator retry only this batch
       vector_index.upsert(
           vectors=list(zip(ids, embeddings)),
           metadata=[c.metadata for c in chunks],
       )
       mark_batch_complete(run_id, doc_batch, ids)
   ```
   Track batch completion state (`mark_batch_complete`) so a resumed
   run after a crash skips already-completed batches instead of
   re-embedding (and re-paying for) work that already succeeded.

4. **Use a provider batch API for large, non-time-sensitive backfills**
   rather than synchronous per-chunk embedding calls — most embedding
   providers offer a batch endpoint trading higher latency for lower
   per-token cost, which is the right trade for an overnight or
   one-time bulk load (see
   [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md)
   for the same batch-vs-synchronous trade-off applied to generation
   calls).

5. **Delete stale chunks explicitly when a source document is deleted
   or its content shrinks**, not just upsert new content — an upsert-
   only pipeline accumulates orphaned chunks from deleted documents and
   from documents that produce fewer chunks after an edit:
   ```python
   def reindex_document(doc, previous_chunk_count):
       new_chunks = chunk_document(doc)
       new_ids = {chunk_id(doc.id, i) for i in range(len(new_chunks))}
       old_ids = {chunk_id(doc.id, i) for i in range(previous_chunk_count)}
       stale_ids = old_ids - new_ids
       if stale_ids:
           vector_index.delete(ids=list(stale_ids))
       vector_index.upsert(vectors=embed_and_pair(new_chunks, new_ids))
   ```
   For a hard source-document deletion, delete all chunk IDs for that
   document ID outright rather than leaving them to be "overwritten
   eventually."

6. **Trigger re-indexing on source-document change events**, with a
   scheduled full/incremental scan as a fallback safety net, not the
   primary mechanism:
   ```
   preferred: source system webhook (on publish/update/delete) →
              queue → single-document re-index job (steps 1-5 above)

   fallback: nightly scan for documents with modified_at > last_run_time
             → batch re-index job for the delta only
   ```
   Event-driven re-indexing keeps the index close to real-time current;
   a purely scheduled batch (with no event trigger at all) means
   retrieval can confidently return content that's stale by up to the
   schedule's full interval — flag this trade-off explicitly if a
   source system genuinely has no event/webhook mechanism available.

7. **Throttle bulk re-indexing runs so they don't compete with live
   query traffic** on the same index — a large backfill or full
   re-embed is a write-heavy burst that can degrade production query
   latency if run unthrottled during peak hours (see
   [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md)
   for the index-side write/query resource contention this throttling
   is protecting against):
   ```python
   for batch in chunked(documents, BATCH_SIZE):
       process_batch(batch, run_id)
       time.sleep(THROTTLE_SECONDS)  # or use a token-bucket rate limiter
   ```

8. **Record ingestion run metrics and alert on regressions** — chunk
   count produced, embedding API error rate, upsert error rate, and
   run duration, compared against the run's own recent baseline:
   ```
   metric                      this_run    7d_avg     delta
   documents_processed            2,050      2,010      flat
   chunks_produced                18,400     9,300     +98%  <-- signal
   embedding_api_errors               0          0      flat
   run_duration_minutes               42         21     +100%
   ```
   A sudden jump in chunks-per-document without a corresponding source
   content change usually indicates a chunking regression (e.g. a
   parser change that stopped detecting section boundaries) — see
   [agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md)
   for the general shape of this kind of correlation-against-recent-
   changes investigation, applied here to the ingestion pipeline
   specifically.

9. **Version and re-run the full corpus on any chunking or embedding-
   model change**, treating it as a new index build (see
   [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md)
   for validating the result before cutover) rather than an incremental
   patch — mixing chunks produced under two different chunking
   configs, or embeddings from two different model versions, in the
   same index degrades retrieval silently.

## Best practices

- Derive every chunk ID deterministically from `(source_doc_id,
  chunk_index)` — this single decision is what makes retries,
  idempotent re-runs, and stale-chunk cleanup all tractable; a random or
  content-hash-only ID scheme forfeits all three.
- Track per-batch and per-document completion state so a crashed run
  resumes from where it left off instead of restarting the whole
  corpus, and so a partial-failure investigation can answer "which
  documents actually landed" precisely.
- Prefer event-driven re-indexing per source-document change over a
  schedule-only approach; keep a scheduled scan only as a fallback
  safety net for sources with no event mechanism, not the primary path.
- Explicitly delete stale chunk IDs on document update/delete — an
  upsert-only pipeline is a slow, silent leak of orphaned vectors that
  degrades retrieval precision over time.
- Use a provider batch embedding API for large backfills where latency
  doesn't matter, reserving synchronous per-request embedding for
  small, time-sensitive incremental updates.
- Throttle bulk/backfill runs to avoid competing with live query
  traffic on the same index, and schedule large backfills during
  lower-traffic windows where possible.
- Re-process the entire corpus (not incrementally) on any chunking-
  config or embedding-model change, and validate it before cutover per
  [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md) —
  never let two chunking/embedding generations coexist silently in one
  index.

## Common pitfalls

- **Symptom:** After a bulk backfill job fails partway through and is
  re-run, the vector index ends up with duplicate chunks for the same
  content.
  **Fix:** Chunk IDs weren't deterministic (e.g. randomly generated or
  timestamp-suffixed), so the re-run's upserts created new vectors
  instead of overwriting the same IDs. Derive chunk IDs from
  `(source_doc_id, chunk_index)` so re-running an upsert for unchanged
  content is a no-op rather than a duplicate.

- **Symptom:** A document was deleted (or heavily shortened) at the
  source days ago, but retrieval still occasionally surfaces its old
  content.
  **Fix:** The pipeline only upserts, it never deletes stale chunk IDs
  when a document is removed or produces fewer chunks after an edit.
  Add explicit stale-chunk deletion (step 5) as part of every
  re-index, not just new-content upsert.

- **Symptom:** A large re-indexing/backfill run causes live RAG query
  latency to spike for its duration.
  **Fix:** The bulk write and live queries are competing for the same
  index resources with no throttling. Throttle batch rate, schedule
  large backfills during lower-traffic windows, and see
  [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md)
  for separating write-path from query-path resource contention at the
  index-operations layer.

- **Symptom:** After switching to a new embedding model, some retrieval
  results seem to come from stale, oddly-scored old-model vectors mixed
  in with the new ones.
  **Fix:** The re-embed was only applied incrementally (new/changed
  documents got new-model vectors, untouched documents kept old-model
  vectors) instead of re-processing the entire corpus. Any embedding-
  model change requires a full corpus re-embed into a new index,
  validated before cutover — never let two embedding-model generations
  coexist in one index.

- **Symptom:** A pipeline run crashes partway through a 5,000-document
  backfill, and it's unclear which documents were actually embedded and
  upserted successfully versus which still need processing.
  **Fix:** No per-batch/per-document completion tracking was in place.
  Add a run-state table recording completion per batch (step 3) so a
  resumed run can skip already-completed work deterministically instead
  of guessing or reprocessing everything from scratch.

- **Symptom:** Retrieval quality degrades slowly and steadily over
  weeks with no single identifiable cause.
  **Fix:** Chunk-count-per-document or embedding-error-rate metrics
  weren't tracked, so a gradual chunking regression (e.g. a source
  format change that broke section-boundary detection, silently
  producing many small, low-quality chunks) went unnoticed. Track
  ingestion run metrics against a rolling baseline (step 8) so this
  class of regression is caught as a trend, not discovered only once
  it's severe.

## Worked example

**Scenario:** A support-knowledge-base RAG system's documents live in a
CMS that supports webhooks on publish/update/delete. The team needs a
production ingestion pipeline: chunk on publish, batch-embed, upsert
idempotently, and clean up stale chunks — plus a one-time backfill for
the existing ~2,000-document corpus.

Backfill (one-time, batch API, throttled):
```python
BATCH_SIZE = 100
THROTTLE_SECONDS = 2
run_id = "backfill-2026-07-28"

for batch in chunked(all_cms_documents(), BATCH_SIZE):
    process_batch(batch, run_id)   # step 3 pattern, using the provider batch embed API
    time.sleep(THROTTLE_SECONDS)
```
Run metrics: 2,050 documents, 18,400 chunks, 0 embedding errors, 41
minutes — recorded as the pipeline's first baseline for future
regression comparison (step 8).

Ongoing event-driven re-indexing:
```python
def on_cms_webhook(event):
    if event.type in ("publish", "update"):
        doc = fetch_document(event.doc_id)
        previous_chunk_count = get_stored_chunk_count(event.doc_id)
        reindex_document(doc, previous_chunk_count)   # step 5 pattern
        store_chunk_count(event.doc_id, len(chunk_document(doc)))
    elif event.type == "delete":
        stale_ids = get_all_chunk_ids_for_document(event.doc_id)
        vector_index.delete(ids=stale_ids)
        forget_document(event.doc_id)
```
A nightly fallback scan checks for any document whose `modified_at`
timestamp is newer than the pipeline's last recorded run for that
document, catching the rare case of a missed/failed webhook delivery —
the CMS's webhook is the primary trigger, this scan is strictly a
safety net (step 6).

Six months later, the team adopts a newer embedding model. Rather than
letting new documents get new-model vectors while old documents keep
old-model vectors, the entire corpus is re-chunked and re-embedded into
a new collection under a new `run_id`, validated for recall against the
existing production collection (see
[vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md))
before the application's index alias is repointed.

## Cross-references

- [rag-pipeline-design](../rag-pipeline-design/SKILL.md) — the retrieval-quality design decisions (chunk size/overlap, metadata to attach, re-index-on-change principle) this pipeline implements operationally without repeating the design rationale.
- [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md) — index-side write-path tuning (batch upsert sizing, avoiding hot partitions) that this pipeline's batching and throttling steps feed into.
- [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md) — the pre-cutover recall/latency validation gate to run before repointing traffic to a corpus this pipeline fully re-processed.
- [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md) — the batch-vs-synchronous cost/latency trade-off referenced in step 4, applied there to generation calls and here to embedding calls.
- [agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md) — triaging a RAG workflow's cost/latency spike that correlates with a recent re-indexing run from this pipeline.
