---
name: search-integration
description: Adds and tunes full-text search - choosing database full-text search vs a search engine, Elasticsearch/OpenSearch mappings and analyzers, keeping the index in sync with the database (outbox, CDC, bulk indexing), zero-downtime reindexing with aliases, bool queries with filters, deep pagination with search_after, aggregations and facets, measured relevance tuning, security and monitoring. Use when building search, autocomplete or facets, search results are wrong or slow, changing an index mapping, or the index drifts from the database. Not for vector-only retrieval for LLMs (see rag-systems).
license: MIT
---

# Search Integration

The database is the source of truth; the search index is a derived copy you must be able to rebuild at any time. Design the mapping on purpose, keep the index in sync through a reliable pipeline, and tune relevance against measured judgments, not impressions from a few test queries.

## When to use

- Adding search, autocomplete, filtering or facets to a product.
- Search results are irrelevant, missing recent changes, or slow.
- Changing an index mapping or analyzer, or upgrading the engine.
- The search index and the database disagree.

Not for: embedding-based retrieval for LLM features (see the rag-systems skill, which covers hybrid search for RAG), or SQL query tuning (see sql-optimization).

## Database full-text search or a search engine?

| Need | Database full-text (e.g. PostgreSQL `tsvector` + GIN, `pg_trgm`; MySQL `FULLTEXT`) | Search engine (Elasticsearch, OpenSearch, Solr, Meilisearch, Typesense) |
| --- | --- | --- |
| Simple keyword search on one or two tables | Good | Overkill |
| Strong consistency with writes | Native (same transaction) | Eventually consistent (refresh delay plus sync lag) |
| Typo tolerance, synonyms, per-language analysis | Limited | Built in |
| Relevance tuning (boosts, function scoring) | Limited | Rich |
| Facets and aggregations over large result sets | Slow at scale | Built for it |
| Isolate heavy search load from the primary database | No | Yes |
| Operational cost | None extra | A cluster to run, secure, monitor and keep in sync |

Default: start with database full-text search when the corpus is modest and needs are simple. Move to an engine when you need relevance tuning, typo tolerance, facets at scale, or load isolation.

Engines in brief: **Elasticsearch / OpenSearch** (Lucene-based, most flexible, most to operate), **Solr** (Lucene-based, mature), **Meilisearch / Typesense** (simpler, typo-tolerant instant search for smaller datasets). Managed offerings exist for most of them. The rest of this skill uses Elasticsearch/OpenSearch terms; the principles carry over.

## Workflow

1. **Write down the search requirements:** which fields are searched, which are filtered, sorted and faceted, languages, expected corpus size and query rate, and how fresh results must be (seconds vs minutes).
2. **Design an explicit mapping** (below). Set `dynamic` to `strict` (reject unknown fields) or `false` (store but don't index them).
3. **Build the sync pipeline** from the database to the index, plus a full rebuild path.
4. **Write queries** with filters for exact constraints and scoring clauses for text.
5. **Create a judgment list** and measure relevance before and after every tuning change.
6. **Put the index behind an alias** from day one, so mapping changes are zero-downtime reindexes.
7. **Monitor** search latency, indexing errors, sync lag and cluster health.

Concrete mapping JSON, query examples and a step-by-step reindex runbook are in [references/mapping-and-reindex.md](references/mapping-and-reindex.md). Read it when creating an index, writing queries, or changing a mapping.

## Mapping rules

| Field use | Mapping |
| --- | --- |
| Full-text search (titles, descriptions) | `text` with a language analyzer (e.g. `english`) |
| Exact match, filters, sorting, aggregations (status, tenant ID, tags, SKUs) | `keyword` (add a lowercase normalizer for case-insensitive matching) |
| Both search and exact/sort | Multi-field: `text` plus a `.keyword` sub-field |
| Numbers, dates, booleans | Their native types (`integer`, `scaled_float`, `date`, `boolean`) so range filters work |
| Arrays of objects matched per object ("color red AND size M on the same variant") | `nested` (more expensive), otherwise plain `object` |
| Stored but never searched | `"index": false`, or leave it out of the index and load from the database |
| Autocomplete | `search_as_you_type`, edge n-grams, or a completion suggester |

- You cannot change an existing field's type or analyzer in place. It requires a reindex into a new index.
- **Mapping explosion:** dynamic fields from user-defined keys (e.g. arbitrary JSON attributes) create thousands of fields and hit the total fields limit. Model them as `nested` key/value pairs, or use a flattened-object field type (`flattened` in Elasticsearch, `flat_object` in OpenSearch; check your version's docs) instead.
- Use the `_analyze` API to see exactly which tokens an analyzer produces before choosing it.

## Keeping the index in sync

| Approach | Use when | Risk |
| --- | --- | --- |
| **Outbox** table written in the same transaction, consumed by an indexer | Default for application-owned data | Indexer lag; needs monitoring |
| **CDC** from the database log (e.g. Debezium) to an indexer | Many writers, legacy code you can't change | More infrastructure; schema changes affect the pipeline |
| **Periodic batch reindex** of changed rows (`updated_at` watermark) | Minutes of staleness is fine | Misses hard deletes unless tracked |
| **Dual write** from application code (DB then index) | Avoid | Index silently drifts when the second write fails |

Rules:

- Use the database primary key as the document `_id`, so re-indexing the same row overwrites instead of duplicating.
- Prevent out-of-order overwrites with **external versioning** (`version` + `version_type=external`, using a row version or update timestamp), so a delayed old event can't replace a newer document.
- Handle deletes explicitly (tombstones in the outbox, or soft-delete flags).
- Use the **bulk API**, start with a few MB per request and tune. A bulk response can be HTTP 200 while individual items failed: check the `errors` flag and each item's status, and retry or dead-letter failed items.
- Changes become searchable after a refresh (by default about every second, configurable via `refresh_interval`). Don't force `refresh=true` on every write in production. Use `refresh=wait_for` only where a user must see their own write immediately.
- Keep a **full rebuild job** that recreates the index from the database. Run it periodically or compare document counts and checksums to detect drift.

The indexer is a background job: see the background-jobs skill for retries, idempotency and metrics.

## Querying

- Put exact constraints in `bool.filter`: tenant, permissions, status, price ranges. Filters don't affect scoring and are cacheable.
- Put user text in `bool.must` / `should`: `multi_match` across fields with boosts (`title^3`, `description`), `fuzziness: "AUTO"` for typo tolerance, and a `match_phrase` in `should` to reward exact phrases.
- For user-typed queries, use `match`/`multi_match` or `simple_query_string`. Never pass raw user input to `query_string`: it exposes the full query syntax, and malformed input causes errors or expensive queries.
- Avoid leading wildcards (`*shoe`) and regex queries on large fields. Use n-gram fields if you need infix matching.
- Build queries with the client library's builders, never by concatenating strings into JSON.

### Pagination

- `from` + `size` gets slower with depth and is capped by `index.max_result_window` (10,000 by default). Fine for the first pages of results.
- For deep pagination or "load more", use `search_after` with a point in time (PIT) and a sort that ends in a unique tiebreaker field.
- For exporting everything, use PIT + `search_after` (or scroll on older versions), never deep `from`.

### Aggregations and facets

- Aggregate on `keyword` and numeric fields, never on `text`.
- `terms` aggregations return the top N buckets and counts can be approximate across shards. Set `size` deliberately and say "approximately" in the UI if counts must be exact elsewhere.
- Facet counts usually apply all filters except the facet's own (post filters or separate aggregations), so users see other options.

## Relevance tuning

1. **Build a judgment list:** 50-200 real queries from search logs (frequent, long-tail, zero-result), each with documents graded for relevance (e.g. 0-3), labeled by people who know the domain.
2. **Pick offline metrics:** NDCG@10 for graded relevance, precision@k, MRR for "first good result", and the zero-result rate. Elasticsearch has a ranking evaluation API (`_rank_eval`); otherwise script it.
3. **Change one thing at a time:** field boosts, analyzers, synonyms, phrase boosts, function score (recency, popularity), and re-measure the whole list. Keep changes that raise the metric without hurting important queries.
4. **Debug single results** with `explain: true` or the `_explain` API to see why a document scored as it did.
5. **Watch online metrics** after release: click-through on top results, zero-result rate, query reformulation rate, and conversions where relevant.

Synonyms: start with a small, curated list from search logs. Broad synonym lists often hurt precision.

## Security

- Never expose the cluster to the internet or to browsers directly. Clients talk to your API, which builds queries.
- Enable authentication and TLS on the cluster, and give the application a role limited to its indices.
- **Enforce tenant and permission filters in every query** on the server, or use the engine's document-level security. A missing filter leaks other tenants' data.
- Index only fields the search needs. PII in the index needs the same retention, deletion and access rules as in the database (see the data-privacy-retention skill).

## Operations

- **Shard sizing:** too many small shards waste memory; huge shards slow recovery. Follow the vendor's current sizing guidance and start with few primary shards for small indices.
- **Monitor:** cluster status (green/yellow/red), search latency p95/p99, indexing rate and bulk failures, rejected requests, JVM heap, disk usage against watermarks (at the flood-stage watermark, indices become read-only for writes), and **sync lag** (age of the oldest unindexed change).
- Snapshot indices if a rebuild from the database would take too long for your recovery objectives.
- Deleting indices, `_delete_by_query`, closing indices and alias swaps in production change what users see or destroy data. Stop and get explicit confirmation from the user first.

## Anti-patterns

- **Dynamic mapping in production**: wrong types (`text` where you needed `keyword`), and mapping explosion.
- **Index as source of truth**: the data can't be rebuilt after a bad mapping or a lost cluster.
- **Dual writes** from the app: silent drift.
- **Ignoring bulk item errors** because the HTTP status was 200.
- **Querying the concrete index name** instead of an alias: every mapping change becomes downtime.
- **Tenant filter added in the UI layer** only: data leaks through other code paths.
- **Tuning by eyeballing** three queries: fixes one query, breaks fifty others.
- **Deep `from` pagination**: slow queries and the 10,000-result wall.
- **`refresh=true` on every write**: indexing throughput collapses.

## Done when

- The mapping is explicit, with `dynamic` set to `strict` or `false`, and each field's type matches how it is queried.
- Queries go through an alias; a reindex runbook exists and has been rehearsed.
- The database-to-index pipeline is reliable (outbox or CDC), idempotent, versioned against out-of-order updates, and handles deletes; a full rebuild path exists.
- Every query enforces tenant and permission filters on the server.
- A judgment list and an offline metric exist, and tuning changes are measured against them.
- Latency, bulk errors, sync lag and cluster health are monitored with alerts.

## References

- [references/mapping-and-reindex.md](references/mapping-and-reindex.md) — read when creating an index, writing queries or deep pagination, or running a zero-downtime reindex.
