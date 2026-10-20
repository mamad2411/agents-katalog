---
name: vector-database-operations-pinecone-weaviate-milvus
description: >
  Guides day-to-day operation of vector databases — index configuration,
  sharding/replication for scale and availability, and upsert/query
  performance tuning — with concrete equivalents across Pinecone, Weaviate,
  and Milvus. Use when a user asks to "configure a vector index," "scale
  our vector DB for more vectors/QPS," "tune HNSW parameters," "set up
  sharding or replication for Pinecone/Weaviate/Milvus," "our vector
  queries got slow," or "upserts are timing out/backing up."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Vector Database Operations (Pinecone, Weaviate, Milvus)

## Purpose

A vector database's default configuration works fine for a demo and starts
showing real operational pain exactly when it matters most: at production
scale, under real query load, with a corpus that keeps growing. This skill
covers operating a vector database day to day — configuring the index
correctly for its workload, scaling it horizontally (sharding) and for
availability (replication), and tuning upsert and query performance — with
concrete, comparable guidance across the three most common choices
(Pinecone as a managed service, Weaviate and Milvus as commonly
self-hosted or managed alternatives). It assumes the index schema and
dimension are already correct and validated (see
[vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md))
and that data is already flowing in via an ingestion pipeline (see
[vector-database-ingestion-pipeline-for-rag](../vector-database-ingestion-pipeline-for-rag/SKILL.md));
this skill is specifically the operate-and-tune layer underneath a RAG
system's retrieval stage (see
[rag-pipeline-design](../rag-pipeline-design/SKILL.md) for the retrieval
pattern itself, which this skill doesn't repeat).

## When to use

- Standing up a new vector index/collection in Pinecone, Weaviate, or
  Milvus and choosing its core configuration.
- Query latency has degraded as the corpus or query volume has grown, and
  it needs concrete tuning, not just "add more hardware."
- Deciding how to shard or partition a large corpus (by tenant, by data
  recency, by content type) across index namespaces/collections.
- Setting up replication for read throughput or availability during
  upgrades/maintenance.
- Upserts are slow, timing out, or backing up during a bulk load or a
  re-indexing run.
- Capacity planning before a corpus grows significantly (more documents,
  more tenants, higher QPS).

## Prerequisites & environment

- A known embedding dimension and distance metric already fixed for the
  corpus (changing either requires a full re-embed and a new index, not a
  config tweak — see
  [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md)).
- Estimated corpus size (vector count), expected query QPS, and expected
  write (upsert) rate — sizing decisions below depend on having real
  numbers, not guesses.
- For Pinecone: an account with pod-based or serverless index access
  (capacity/scaling mechanics differ between the two — check current
  Pinecone documentation for which applies to your plan, since this has
  changed over time).
- For Weaviate/Milvus: a self-hosted or managed cluster with enough nodes
  to support the replication/sharding plan you choose — these are
  self-operated systems, so cluster sizing is your responsibility in a way
  it isn't with a fully managed Pinecone index.
- Monitoring for index-level metrics (query latency, upsert throughput,
  index/memory fullness) wired to a dashboard — see
  [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  for the metrics-pipeline mechanics if self-hosting Weaviate/Milvus.

## Step-by-step guidance

1. **Configure the index's core parameters deliberately, not with
   defaults.** All three support HNSW as the common ANN (approximate
   nearest neighbor) index type; Milvus additionally supports IVF-family
   indexes, which trade some recall for lower memory at very large scale.
   Confirm the distance metric matches what the embedding model expects
   (cosine similarity is the common default; some models are tuned for dot
   product) — a mismatch here degrades relevance silently, not with an
   error (see
   [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md)
   for the validation gate on this specifically).

2. **Tune HNSW's core knobs deliberately — they trade recall, latency, and
   memory against each other:**
   - `M` (max connections per node): higher improves recall, increases
     memory and index build time. Common starting range: 16-32.
   - `ef_construction` (candidate list size during index build): higher
     improves recall at index-build-time cost only (a one-time or
     per-upsert cost, not a per-query cost). Common starting range:
     100-200.
   - `ef_search` (candidate list size at query time): higher improves
     recall at direct query-latency cost, tunable per query without
     rebuilding the index. This is usually the first knob to adjust when
     tuning the recall/latency trade-off after launch.

   ```yaml
   # Weaviate collection config (illustrative — verify field names against
   # your Weaviate version's current API)
   vectorIndexConfig:
     distance: cosine
     ef: 128            # ef_search, tunable post-launch
     efConstruction: 128
     maxConnections: 32  # M
   ```
   ```python
   # Milvus index params (illustrative)
   index_params = {
       "index_type": "HNSW",
       "metric_type": "COSINE",
       "params": {"M": 24, "efConstruction": 200},
   }
   search_params = {"ef": 128}  # tuned separately at query time
   ```
   ```python
   # Pinecone: HNSW internals are managed for you on pod-based indexes;
   # the primary tunable is pod type/size and top_k at query time rather
   # than raw M/ef parameters — check current Pinecone docs for what's
   # exposed on your index type (pod-based vs. serverless).
   ```

3. **Shard/partition the corpus deliberately, not by default.** Options
   map roughly across vendors:
   - **Pinecone namespaces**: logical partitions within one index, common
     for per-tenant isolation in a multi-tenant application — queries are
     scoped to one namespace at a time.
   - **Weaviate multi-tenancy / sharding**: dedicated tenant partitions
     within a collection, or manual sharding across multiple collections
     for very large single-tenant corpora.
   - **Milvus partitions within a collection**: similar per-tenant or
     per-category logical split; Milvus also supports sharding a
     collection across multiple query nodes for horizontal scale.

   Partition by **tenant** when the workload is naturally multi-tenant
   (each query only ever needs one tenant's data — this also gives you
   access-control isolation for free). Partition by **data recency or
   category** when queries are commonly scoped that way (e.g. "search only
   this year's documents") — this reduces the search space per query
   directly rather than relying on a metadata filter over an unpartitioned
   index.

4. **Configure replication for both availability and read throughput.**
   Pinecone (pod-based) supports replica pods that both increase query
   throughput and provide failover; Weaviate and Milvus support a
   configurable replication factor per collection/shard. Set replication
   high enough to survive a node loss during a rolling upgrade without a
   query-serving gap, not just to hit an arbitrary throughput number.

   ```yaml
   # Milvus collection replication (illustrative)
   collection: product_docs
   replica_number: 2   # survives one query-node loss without downtime
   ```

5. **Tune upsert (write) performance separately from query performance —
   they compete for the same resources.** Batch upserts rather than
   single-vector calls (all three vendors expose a batch upsert API);
   tune batch size empirically (too small wastes round-trips, too large
   risks request timeouts or memory pressure on the server side). Avoid a
   single hot partition/shard absorbing all writes during a bulk load —
   spread a large backfill across partitions/time rather than one burst
   against one shard.

   ```python
   # Generic batch-upsert pattern applicable across vendors' SDKs
   BATCH_SIZE = 200
   for batch in chunked(vectors_with_metadata, BATCH_SIZE):
       index.upsert(vectors=batch, namespace=tenant_id)
   ```

6. **Tune query performance with pre-filtering vs. post-filtering in
   mind.** When a query combines a vector search with a metadata filter
   (e.g. "only documents from `product_line=payments`"), check whether
   your vendor/index applies the filter *before* the ANN search
   (pre-filtering, generally more accurate and often faster when the
   filter is selective) or *after* (post-filtering the ANN result set,
   which can silently return fewer results than `top_k` if the filter
   excludes most of the initial candidates). This behavior differs by
   vendor and by whether the filtered field is indexed — verify against
   current documentation for your specific setup rather than assuming.

7. **Size capacity with an explicit formula, not a guess.** A rough
   working estimate for HNSW memory footprint:

   ```
   memory_per_vector ≈ (dimension × bytes_per_dim) × (1 + hnsw_overhead_factor)
   total_memory ≈ memory_per_vector × vector_count + metadata_overhead
   ```

   `bytes_per_dim` is typically 4 (float32) unless the vendor supports
   quantization (e.g. lower-precision or product-quantized storage, which
   trades some recall for meaningfully lower memory — check whether your
   chosen vendor supports it and at what recall cost before assuming free
   savings). Re-check actual per-vendor overhead figures against current
   documentation before finalizing a sizing decision — don't treat the
   formula's constant as vendor-verified without confirming.

8. **Monitor operational metrics continuously, not just at launch**: query
   latency (p50/p95), upsert throughput and error rate, index/memory
   fullness relative to the tier or node's capacity, and (for
   replicated setups) replica lag. Alert on index fullness well before
   the hard ceiling — performance commonly degrades before an index is
   literally full, not only at 100%.

9. **Plan backup/restore and index migration as a first-class operation,
   not an afterthought.** Snapshot/export support differs by vendor —
   confirm your chosen vendor's current backup mechanism and test a
   restore before you need it for real. For a config change that requires
   a new index (a new HNSW parameter set, a new sharding scheme), build
   the new index alongside the old one and cut over via an alias/pointer
   swap rather than deleting and rebuilding in place (see
   [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md)
   for the validation gate before that cutover).

## Best practices

- Start `ef_search` conservatively and raise it only if a recall
  evaluation (see
  [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md))
  shows it's needed — raising it blindly trades latency for recall you
  may not need.
- Partition by the dimension your queries actually filter on most often
  (tenant, recency, category) rather than an arbitrary hash — a partition
  scheme that doesn't match query patterns adds operational complexity
  without a performance payoff.
- Keep replication factor high enough to survive routine maintenance
  (rolling upgrades, node replacement) without a query-serving gap, and
  test failover deliberately rather than assuming it works.
- Separate the write path (bulk ingestion, backfills) from the live query
  path operationally — a large backfill job should not be allowed to
  starve production query latency; throttle or schedule bulk upserts
  during lower-traffic windows where possible.
- Track index/memory fullness as a leading indicator, not a lagging one —
  most vector indexes degrade in latency and/or recall well before hitting
  a hard capacity wall.
- Re-validate recall and latency after any HNSW parameter change, sharding
  change, or vendor-tier change — these are configuration changes with
  real correctness and performance implications, not routine tuning knobs
  to flip without re-testing.

## Common pitfalls

- **Symptom:** Query recall silently drops (returning technically valid
  but less relevant results) after scaling the corpus up, with no error
  or alert.
  **Fix:** `ef_search` that was adequate at a smaller corpus size often
  needs to increase as the corpus grows, since more candidates compete for
  the same approximate search — re-run a labeled recall evaluation (see
  [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md))
  after significant corpus growth, don't assume a fixed `ef_search` scales
  forever.

- **Symptom:** A metadata-filtered query returns fewer results than
  `top_k` (sometimes zero), even though matching documents clearly exist
  in the corpus.
  **Fix:** This is usually post-filtering: the ANN search returned
  `top_k` candidates first and the metadata filter then excluded most of
  them. Check whether your vendor/index config supports pre-filtering for
  this field, or increase the initial candidate count before filtering, or
  index the filtered field so it can be applied more efficiently.

- **Symptom:** A large backfill/bulk-upsert job causes production query
  latency to spike for the duration of the load.
  **Fix:** The bulk load and live queries are competing for the same
  compute/IO resources on a shared index or shard. Throttle upsert batch
  rate, schedule large backfills during lower-traffic windows, or (for
  self-hosted Weaviate/Milvus) scale write-serving nodes independently
  from query-serving nodes where the deployment topology supports it.

- **Symptom:** A single shard/partition absorbs a disproportionate share
  of writes (a "hot partition"), backing up upserts while other shards sit
  idle.
  **Fix:** Review the partition key — a scheme partitioned by a
  low-cardinality or skewed field (e.g. a single dominant tenant) will hot
  spot regardless of total shard count; choose a partition key with more
  even distribution, or split the dominant tenant's data further.

- **Symptom:** An index configured with no replicas has a multi-minute
  query outage during a routine node upgrade or restart.
  **Fix:** Set a replication factor of at least 2 for any index serving
  production queries, and treat "does failover actually work" as
  something to test deliberately (e.g. by draining a node/replica and
  confirming queries keep succeeding), not something to assume from the
  configuration alone.

## Worked example

**Scenario:** A support-knowledge-base RAG system needs to scale from a
100K-vector pilot to a 20-million-vector, multi-tenant production corpus
(1536-dimension embeddings, cosine similarity), serving ~150 QPS with
occasional large backfills when new customers onboard.

Configuration decisions:

```
Capacity estimate:
  memory_per_vector ≈ 1536 × 4 bytes × (1 + ~0.2 hnsw_overhead) ≈ ~7.4 KB
  total ≈ 7.4 KB × 20,000,000 ≈ ~148 GB (before metadata/final-tier
  overhead — verify against the chosen vendor's current sizing guidance
  before committing to a specific tier/node count)

Sharding: partition by tenant_id (Pinecone namespace / Weaviate
multi-tenant collection / Milvus partition) — matches the actual query
pattern (every query is scoped to one customer's knowledge base) and
gives per-tenant data isolation as a side effect.

HNSW config: M=24, efConstruction=200 at index-build time;
ef_search=128 as the initial production value, re-validated against a
50-query labeled recall set at the full 20M-vector scale before cutover
(see vector-database-configuration-validation).

Replication: replica_number=2 (Milvus) / equivalent replica pods
(Pinecone) — survives one node loss during rolling upgrades with no
query-serving gap.

Write path: new-customer backfills (up to ~500K vectors each) batched
at 200 vectors/upsert call, throttled to run during off-peak hours and
isolated from the live query path so onboarding a new customer doesn't
degrade existing customers' query latency.

Monitoring: p95 query latency, upsert error rate, and per-partition
memory fullness alerted at 75% of the provisioned tier's documented
capacity — well before the hard ceiling.
```

## Cross-references

- [vector-database-configuration-validation](../vector-database-configuration-validation/SKILL.md) — the pre-cutover gate for dimension/metric/recall validation referenced throughout this skill's tuning steps.
- [vector-database-ingestion-pipeline-for-rag](../vector-database-ingestion-pipeline-for-rag/SKILL.md) — the upstream pipeline whose batch upsert behavior this skill's write-path tuning operates on.
- [rag-pipeline-design](../rag-pipeline-design/SKILL.md) — the retrieval pattern (chunking, re-ranking, hybrid search) this operational layer serves; not repeated here.
- [agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md) — triaging a sudden query latency spike that may originate at this operational layer.
- [capacity-planning-and-load-testing](../../../site-reliability-engineering/skills/capacity-planning-and-load-testing/SKILL.md) — general load-testing methodology applicable to validating query throughput at target scale.
