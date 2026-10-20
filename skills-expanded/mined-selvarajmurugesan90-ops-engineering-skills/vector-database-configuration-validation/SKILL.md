---
name: vector-database-configuration-validation
description: >
  Validates a vector index's schema/dimension/distance-metric config and
  its actual recall/query-performance behavior before a production
  cutover — catching a mismatch that returns wrong-but-plausible results
  or degraded recall instead of an error. Use when a user asks to
  "validate my vector index config before we go live," "will this
  embedding dimension/metric mismatch break retrieval," "test recall
  before cutting over to the new index," "check this Pinecone/Weaviate/
  Milvus schema for mistakes," or reports retrieval quality that
  silently dropped after a re-index or embedding-model change.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Vector Database Configuration Validation

## Purpose

A vector index with the wrong dimension, distance metric, or HNSW
parameter set for its embedding model doesn't fail loudly — it either
rejects vectors with a dimension-mismatch error (the easy case) or,
worse, silently accepts vectors and returns technically valid but
degraded or nonsensical similarity results (the hard case, because
nothing in the API response signals anything is wrong). This skill
covers validating a vector index's configuration and actual
query-performance behavior **before** it takes production traffic:
confirming dimension and distance-metric agreement with the embedding
model, running a labeled recall evaluation against real queries, and
gating a cutover behind that evaluation rather than a visual "looks
right" review. It assumes the index's operational tuning (sharding,
replication, HNSW parameter selection) is handled in
[vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md)
and that vectors are arriving via
[vector-database-ingestion-pipeline-for-rag](../vector-database-ingestion-pipeline-for-rag/SKILL.md) —
this skill is specifically the pre-cutover validation gate sitting
between those two.

## When to use

- Before cutting a RAG system's retrieval traffic over to a new or
  reconfigured vector index (new embedding model, new HNSW parameters,
  new sharding scheme, vendor migration).
- Standing up a new index/collection and confirming its schema
  (dimension, distance metric, indexed metadata fields) actually matches
  what the embedding model and query patterns require.
- Retrieval quality (recall, relevance) degraded after a re-index or an
  embedding-model change, and you need to confirm whether the index
  configuration itself is the cause.
- Reviewing a Pinecone/Weaviate/Milvus index/collection definition in a
  PR before it's applied, to catch a dimension or metric mistake before
  it reaches production.
- Migrating a corpus to a new vendor or a new index within the same
  vendor, and needing a go/no-go gate before the alias/pointer swap.

## Prerequisites & environment

- The embedding model's actual output dimension and the distance metric
  it was trained/tuned for (cosine vs. dot product vs. Euclidean) —
  get this from the model's own documentation, not assumed from a
  different model's defaults; a mismatch here is the single most common
  root cause this skill catches.
- A labeled evaluation set of `(query, expected relevant document ids)`
  pairs representative of real production queries — at minimum 30-50
  pairs covering the corpus's main topics; without this, "does the new
  index work" can only be answered by vibes, not a number.
- Access to both the candidate (new/changed) index and, when validating
  a re-index or migration, the existing production index, so recall can
  be compared side by side rather than evaluated in isolation.
- The vendor SDK/CLI for the index in question (Pinecone, Weaviate, or
  Milvus client) to run schema inspection and query calls directly,
  rather than only reading the config file that was intended to produce
  it.
- Familiarity with your vendor's current alias/pointer-swap or
  blue-green index mechanism, since the recommended cutover pattern
  below depends on it (Pinecone: create-new-then-repoint; Weaviate/
  Milvus: alias support varies by version — confirm current
  documentation).

## Step-by-step guidance

1. **Confirm the index's configured dimension matches the embedding
   model's actual output dimension** — check this against a real
   embedding call, not the model's marketing/spec-sheet number alone,
   since some models expose a configurable output dimension
   (e.g. Matryoshka-style truncation) that can silently differ from the
   nominal default:
   ```python
   sample_vector = embedding_model.embed("sanity check")
   assert len(sample_vector) == index_config["dimension"], (
       f"embedding model outputs {len(sample_vector)} dims, "
       f"index configured for {index_config['dimension']}"
   )
   ```
   A dimension mismatch is usually caught immediately as a hard error on
   upsert — treat that as the *good* outcome; the dangerous case is a
   vendor/index configuration that silently pads or truncates instead
   of rejecting (verify current vendor behavior rather than assuming
   it errors).

2. **Confirm the distance metric configured on the index matches what
   the embedding model expects.** This is the silent-failure case: a
   model tuned for cosine similarity queried with a dot-product or
   Euclidean index still returns a similarity-ranked result set — it's
   just the wrong ranking, with no error anywhere:
   ```yaml
   # Weaviate collection (illustrative — verify current field names)
   vectorIndexConfig:
     distance: cosine     # must match the embedding model's trained metric
   ```
   ```python
   # Milvus
   index_params = {"index_type": "HNSW", "metric_type": "COSINE", "params": {...}}
   ```
   If you cannot find explicit confirmation of which metric a given
   embedding model was tuned for, treat cosine as the safer default
   assumption but confirm before finalizing — don't guess silently on a
   production cutover.

3. **Confirm which metadata fields are actually indexed/filterable**,
   not just present on the upserted objects — a field present in payload
   but not indexed for filtering will either error or (for some
   vendors) silently fail to filter, depending on the vendor and query
   type:
   ```python
   # Pinecone example: confirm a metadata field is usable as a filter
   results = index.query(
       vector=sample_vector, top_k=5,
       filter={"product_line": {"$eq": "payments"}},
   )
   assert len(results.matches) > 0 or corpus_actually_has_no_payments_docs
   ```

4. **Build a labeled recall evaluation set and run it against the
   candidate index before cutover** — this is the core validation gate,
   and the only thing that actually answers "will retrieval be as good
   or better than before":
   ```python
   # eval_set: list of (query, set_of_expected_doc_ids)
   def recall_at_k(index, eval_set, k=10):
       hits = 0
       for query, expected_ids in eval_set:
           query_vec = embedding_model.embed(query)
           results = index.query(vector=query_vec, top_k=k)
           returned_ids = {r.id for r in results.matches}
           hits += 1 if expected_ids & returned_ids else 0
       return hits / len(eval_set)

   candidate_recall = recall_at_k(candidate_index, eval_set, k=10)
   baseline_recall = recall_at_k(production_index, eval_set, k=10)
   print(f"candidate recall@10={candidate_recall:.2f} baseline={baseline_recall:.2f}")
   ```
   Set an explicit go/no-go threshold before running the evaluation
   (e.g. "candidate recall@10 must be within 2 points of baseline, or
   strictly higher") — deciding the bar after seeing the number invites
   rationalizing a bad result into a pass.

5. **Check query latency at realistic top_k and filter combinations**,
   not just an unfiltered single-vector query — a filtered query or a
   high `top_k` can behave very differently under the candidate index's
   actual configuration:
   ```python
   import time
   for top_k in (5, 10, 50):
       start = time.monotonic()
       candidate_index.query(vector=sample_vector, top_k=top_k, filter=common_filter)
       print(top_k, (time.monotonic() - start) * 1000, "ms")
   ```

6. **Validate at production-representative scale, not just on a small
   sample**, when the concern is a large migration or a parameter
   change intended to hold at scale — recall and latency measured
   against a 1,000-vector test index do not reliably predict behavior
   at 20 million vectors (see
   [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md)
   for sizing/HNSW-tuning guidance this validation step should be run
   against once applied).

7. **Cut over via alias/pointer swap, not delete-and-rebuild in
   place**, so a validation gap discovered after cutover has an
   immediate rollback path:
   ```
   1. Build the new index alongside the old one (both live).
   2. Run steps 1-6 against the new index while the old index still
      serves production traffic.
   3. Only after the recall/latency gate passes, repoint the
      application's alias/index reference to the new index.
   4. Keep the old index available, unrouted, for a defined rollback
      window before decommissioning it.
   ```
   > **Warning:** deleting the previous index immediately after cutover
   > (to save cost) removes your rollback path. Keep it, unrouted, for
   > at least one full validation/observation window before deleting —
   > treat immediate deletion as a destructive action to avoid, not a
   > routine cleanup step.

8. **Wire this validation into CI/CD for index-config changes** so a
   dimension/metric/schema change is checked automatically on every PR
   touching index configuration, not only remembered manually before a
   big migration:
   ```yaml
   # CI step (illustrative)
   - name: Validate vector index config
     run: python validate_index_config.py --config index-config.yaml --eval-set eval_set.jsonl --min-recall-at-10 0.85
   ```

## Best practices

- Set the recall/latency go/no-go threshold **before** running the
  evaluation, not after seeing the candidate's number.
- Treat a hard dimension-mismatch error as the safe outcome and a
  silently-accepted metric mismatch as the dangerous one — spend
  validation effort proportionally on the failure modes that don't
  announce themselves.
- Always compare candidate recall against the current production
  baseline on the same labeled eval set, not against an absolute number
  alone — a candidate "recall@10 = 0.88" is meaningless without knowing
  whether the current production index scores 0.80 or 0.95 on the same
  queries.
- Re-run this validation after any embedding-model change, HNSW
  parameter change, or sharding change — these are each, individually,
  enough to shift recall, and re-validating only at initial launch
  misses regressions introduced later.
- Cut over via alias/pointer swap with the old index kept live but
  unrouted for a rollback window — never delete-and-rebuild in place.
- Keep the labeled eval set itself under version control and expand it
  over time as new query patterns/topics emerge in production — a
  stale, narrow eval set gives false confidence on corpus areas it
  doesn't cover.
- Validate at a scale representative of production, not a small smoke
  test, before finalizing a decision meant to hold at full corpus size.

## Common pitfalls

- **Symptom:** Retrieval quality drops noticeably after a re-index or
  embedding-model migration, but no error appeared anywhere during the
  migration.
  **Fix:** This is the classic silent distance-metric or partial
  re-embed mismatch — confirm the new index's configured metric matches
  the new embedding model's trained metric (step 2), and confirm the
  entire corpus was re-embedded with the new model rather than mixing
  old and new embeddings in one index (a mixed-embedding index degrades
  silently, with no error, exactly like a metric mismatch).

- **Symptom:** A migration passes a quick manual "looks fine" spot check
  with a couple of test queries, then real production traffic surfaces
  systematic relevance problems within days.
  **Fix:** A handful of manually-eyeballed queries is not a validation
  gate — build and run the labeled recall evaluation (step 4) against a
  representative query set before cutover, with an explicit
  pass/fail threshold decided in advance.

- **Symptom:** A metadata filter that worked correctly in a small test
  environment returns zero or incomplete results once applied against
  the full production index.
  **Fix:** Confirm the filtered field is actually indexed for filtering
  at the vendor/index-config level (step 3), not just present in the
  upserted payload — a field that's present but unindexed can behave
  differently under filtering depending on the vendor and whether it's
  falling back to post-filtering over a smaller candidate set.

- **Symptom:** A validated, passing candidate index degrades in
  production within weeks of cutover, even though nothing else in the
  application changed.
  **Fix:** Validation likely ran against a small or unrepresentative
  test scale rather than production corpus size and query volume (step
  6) — recall/latency behavior at 1,000 vectors does not reliably
  predict behavior at millions; re-validate at representative scale
  before trusting the result for a large migration.

- **Symptom:** After cutting over to a new index, a validation gap is
  discovered, but there's no way to quickly revert because the old
  index was already deleted to save cost.
  **Fix:** This is exactly why cutover must be an alias/pointer swap
  with the old index kept live but unrouted for a defined rollback
  window (step 7) — deleting the previous index immediately after
  cutover is a destructive, hard-to-reverse action; keep it until the
  observation window has passed cleanly.

## Worked example

**Scenario:** A support-knowledge-base RAG system is migrating its
embedding model to a newer, higher-quality model, which also changes
the vector dimension from 1024 to 1536. The team needs to validate the
new index before repointing production traffic.

1. Confirm dimension agreement with a live embed call:
   ```python
   sample = new_embedding_model.embed("refund policy for damaged items")
   assert len(sample) == 1536  # matches new index's configured dimension
   ```
2. Confirm the new model's trained metric is cosine (per its
   documentation) and that the new Weaviate collection is configured
   `distance: cosine` — matches; no mismatch found.
3. Build the new collection alongside the existing production
   collection, fully re-embedding the entire ~2,000-document corpus with
   the new model (no partial/mixed re-embed).
4. Run the existing 50-query labeled eval set (already maintained per
   [rag-pipeline-design](../rag-pipeline-design/SKILL.md)) against both
   collections:
   ```
   candidate (new model, 1536-dim): recall@10 = 0.91
   production (old model, 1024-dim): recall@10 = 0.84
   ```
   Pre-agreed threshold ("candidate must be >= baseline") is met with
   margin.
5. Check filtered-query latency at `top_k=10` with the existing
   `product_line` filter against the new collection — p95 latency
   145ms, within the team's 200ms budget.
6. Cut over via alias swap: application's `product-docs` alias is
   repointed from the old collection to the new one; the old collection
   is kept live, unrouted, for a two-week rollback window before
   decommissioning.
7. The CI check (`validate_index_config.py --min-recall-at-10 0.85`) is
   added so any future embedding-model or HNSW-parameter change to this
   collection is gated the same way automatically.

## Cross-references

- [vector-database-operations-pinecone-weaviate-milvus](../vector-database-operations-pinecone-weaviate-milvus/SKILL.md) — the operational tuning (sharding, replication, HNSW parameters) this validation gate sits in front of before those settings serve production traffic.
- [vector-database-ingestion-pipeline-for-rag](../vector-database-ingestion-pipeline-for-rag/SKILL.md) — the upstream pipeline that produces the vectors and re-embeds the corpus this skill validates before cutover.
- [rag-pipeline-design](../rag-pipeline-design/SKILL.md) — where the labeled (query, expected document) eval set referenced throughout this skill is originally built and maintained.
- [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md) — general evaluation-harness discipline (thresholds decided in advance, regression gating) applied here specifically to retrieval recall.
