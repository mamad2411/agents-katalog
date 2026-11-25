---
name: backend-search
description: "Search in an application: when the database's full-text search is enough, Postgres tsvector and trigram indexes, when to add Meilisearch, Typesense or OpenSearch, keeping the index in sync, relevance, filters and facets, typo tolerance, highlighting, permission-aware results, semantic and hybrid search with vectors, and reindexing without downtime. Read before building search or when search is slow or poor."
---

# Search

The generated search box runs `WHERE name ILIKE '%' || $1 || '%'` over the
whole table with no index, returns rows the user may not see, finds nothing
for a typo or a plural, and when it gets slow a search engine is bolted on,
fed by a second write in the request handler that quietly drifts. This skill
gives the order to climb (the database first, an engine for a named need),
how to keep an index in sync, relevance, permissions and vectors. One part
of the backend; the whole is in the `backend` skill, SQL depth in
`database-queries` and `database-postgres`.

## 1. Decide what search it is

| Need | Start with |
|---|---|
| A record by code, email or exact name | a B-tree index (on `lower(email)` where case varies), `=` or prefix `LIKE 'abc%'` |
| Substrings and near matches in short fields (names, SKUs, cities) | Postgres `pg_trgm` |
| Words in longer text (articles, descriptions, tickets), ranked | Postgres full-text search (`tsvector`) |
| Typo tolerance in free text, facets with counts, results on every keystroke, synonyms, tuned relevance | a search engine (section 4) |
| Meaning rather than words ("something like this", questions) | embeddings, combined with keyword search (section 8) |

- Stay in the database until a need from the fourth row appears, or latency
  measured on real volumes says otherwise: one system, no sync, and the
  query's own filters for permissions.
- Collect 30 to 100 real queries (search logs, support tickets, the people
  who will search) before designing anything; they decide the design and
  later test it (section 10).

## 2. Postgres full-text search

```sql
ALTER TABLE articles ADD COLUMN search tsvector GENERATED ALWAYS AS (
  setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
  setweight(to_tsvector('english', coalesce(body, '')), 'B')
) STORED;
CREATE INDEX articles_search_idx ON articles USING gin (search);

SELECT id, title, ts_rank(search, q) AS rank
FROM articles, websearch_to_tsquery('english', $1) AS q
WHERE search @@ q AND tenant_id = $2 AND status = 'published'
ORDER BY rank DESC, id
LIMIT 20;
```

- A generated column (Postgres 12+) keeps the vector in step with the row.
  The configuration is written out (`'english'`): the one-argument
  `to_tsvector` is not immutable and cannot be used there or in an index.
  Never compute `to_tsvector` per row at query time.
- `websearch_to_tsquery` accepts what people type (quoted phrases, `or`,
  `-word`) and never raises a syntax error. For search as you type, build a
  prefix query from the sanitised words (`kopi:* & susu:*` for
  `to_tsquery`), never from raw input.
- One configuration per language: `english`, `indonesian`, `simple` for
  names and codes that must not be stemmed (`\dF` in psql lists them).
  Rows in several languages keep a `regconfig` column used in the
  expression.
- Weights A to D rank the title above the body; `ts_rank_cd` also rewards
  words close together. Ranking runs for every match, so narrow with filters
  first, and blend recency or popularity into the `ORDER BY` only as tuned
  on the query set.
- Highlights with `ts_headline` on the page of results only (it re-parses
  each text): `ts_headline('english', body, q, 'MaxFragments=2, MaxWords=20')`.
- Accents: the `unaccent` extension, through an immutable wrapper function
  when used in a generated column or an index.

## 3. Trigrams for names and near matches

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX products_name_trgm_idx ON products USING gin (name gin_trgm_ops);

-- substring, any case, served by the index ($1 with % _ \ escaped)
SELECT id, name FROM products
WHERE tenant_id = $2 AND name ILIKE '%' || $1 || '%'
LIMIT 20;

-- tolerant of typos, best first
SELECT id, name, similarity(name, $1) AS score
FROM products
WHERE tenant_id = $2 AND name % $1
ORDER BY score DESC, id
LIMIT 20;
```

- `%` matches above `pg_trgm.similarity_threshold` (0.3 by default);
  `<%` (word similarity) finds a word inside a longer name. Ordering by
  distance (`ORDER BY name <-> $1 LIMIT 20`) is served directly by a GiST
  index (`gist_trgm_ops`), not by GIN.
- Trigrams need 3 characters to be selective: search from 2 or 3 characters,
  not 1.
- A name box and a text body in one search: trigram score and full-text
  rank combined in one query, or two queries merged (section 8).

## 4. When to add a search engine

Add one for a named need: typo tolerance across free text, facets with
counts over many attributes, results under 50 ms on every keystroke,
synonyms and merchandising rules, or volumes where Postgres ranking no
longer fits the time budget.

| Engine | Choose when |
|---|---|
| Meilisearch | simplest to run and tune; typo tolerance and good relevance by default; small to medium collections |
| Typesense | similar simplicity, in memory and fast; scoped keys for direct client search |
| OpenSearch or Elasticsearch | large volumes, complex queries and aggregations, analytics beside search; more to operate |
| Algolia | hosted and quick to ship; priced per search and record |
| ParadeDB `pg_search` | BM25 ranking inside Postgres, where the extension can be installed (not on every managed Postgres) |

- The index is a copy, never the source of truth: it can be dropped and
  rebuilt from the database at any time (sections 5 and 9).
- Index only what is searched, filtered, sorted or shown, plus ids and the
  permission fields; never whole records with private columns.

## 5. Keeping the index in sync

- Never a second write in the request handler (`db.save(); search.index()`):
  when it fails, or the process dies between the two, the index drifts and
  nobody notices.
- After the commit, a job indexes the record by id from its current state
  (`backend-jobs`). Upserts and deletes by id are idempotent, so retries and
  duplicates do no harm. When no change may be lost, write an outbox row in
  the same transaction; at larger scale, change data capture from the
  database log (Debezium, Postgres logical replication).
- Batch writes (100 to 1,000 documents a request): engines index batches far
  faster than single documents. Meilisearch applies writes as asynchronous
  tasks, and OpenSearch makes them searchable after the refresh interval (1 s
  by default): tests wait for the task or refresh before asserting.
- Deletes and permission changes are indexed like any update: a record made
  private leaves public results now, not at the next rebuild.
- A scheduled reconciliation compares counts or `updated_at` watermarks and
  reindexes the difference, so drift is found and repaired.

## 6. Relevance, typos, filters and facets

- Order of importance, tuned on the query set rather than by instinct: exact
  over partial, title over body (the order of `searchableAttributes` in
  Meilisearch, field boosts in OpenSearch), then business signals (in stock,
  popularity, recency) as a tie-breaker or gentle boost, never a hidden
  filter.
- Synonyms and stop words per language, taken from what users type (`sofa`
  and `couch`); pinned or buried results for a query live in engine
  configuration, recorded with who set them and why.
- Typo tolerance scaled to word length (Meilisearch allows one typo from 5
  characters and two from 9) and turned off for codes, SKUs and numbers.
- No results: try a fallback (drop the least important word, allow prefixes)
  before the empty state, which then offers a way on (`ui-part-search`).
- Filters are exact conditions on attributes declared filterable
  (`filterableAttributes` in Meilisearch, `facet: true` in Typesense,
  `keyword` fields in OpenSearch). Facet counts come from the same query and
  reflect the other active filters; in Postgres, `GROUP BY` counts on the
  filtered set, cached when expensive.
- Page numbers with a hard cap: Meilisearch's `maxTotalHits` is 1,000 and
  OpenSearch's `max_result_window` 10,000 by default, and nobody reads page
  400; offer filters instead. `search_after` for exports.
- Highlights: ask the engine for unusual markers (`highlightPreTag`), escape
  the whole string as HTML, then turn the markers into `<mark>`. Engine
  output rendered as raw HTML is a stored XSS.

## 7. Permissions in every query

- Search returns only what the caller may see, filtered inside the query:
  tenant, visibility and the caller's groups on every search
  (`tenant_id = 12 AND (visibility = 'public' OR group_ids IN [3, 7])`).
  Filtering results afterwards breaks pages (a page of 20 shows 3) and
  leaks through counts, facets and totals.
- The filter is built on the server from the session, never taken from the
  client. When the browser queries the engine directly for instant search,
  it gets a key with the filter embedded that it cannot remove: Algolia's
  secured API keys, Meilisearch tenant tokens, Typesense scoped search keys,
  each with a short expiry.
- Permission fields live in every document and are reindexed when sharing
  changes. Access lists of thousands of users do not fit in documents:
  index group or team ids instead.
- A test searches as two tenants and as a user without access, and checks
  results, counts and facets reveal nothing of the other.

## 8. Semantic and hybrid search

- Embeddings find by meaning ("cheap laptop for school" matches a
  description that uses none of those words) and miss exact terms (SKUs,
  names, error codes) that keyword search finds. Use both.
- pgvector in the database you have until the collection or query rate
  outgrows it; a dedicated vector store (Qdrant, Weaviate, Pinecone) only
  then, or the vectors of an engine you already run.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
ALTER TABLE articles ADD COLUMN embedding vector(1536);
CREATE INDEX articles_embedding_idx ON articles USING hnsw (embedding vector_cosine_ops);
```

- HNSW over IVFFlat: better recall, no training step. Defaults `m = 16`,
  `ef_construction = 64`; raise `hnsw.ef_search` (40 by default) for recall
  at some cost in speed. A filter can leave an approximate scan with fewer
  rows than the `LIMIT`: pgvector 0.8 and later has iterative scans
  (`SET hnsw.iterative_scan = relaxed_order`); before that, fetch more and
  filter.
- Long documents are split by headings or paragraphs into chunks of 200 to
  500 tokens with a small overlap, one row per chunk with its document id;
  short records (products) are embedded whole from a composed text (title,
  category, key attributes).
- Each vector records its model; queries use the same model, and a model
  change means re-embedding everything into a new column, then switching.
- Vectors always return nearest neighbours, even when nothing is relevant:
  pair them with keyword search, or a distance cut-off tuned on the query
  set.
- Hybrid ranking with reciprocal rank fusion: 50 results from each side, a
  score of the sum of 1 / (60 + rank), the top 20 kept. A cross-encoder
  re-ranker (Cohere Rerank, a bge reranker) on the top 50 when quality needs
  it and latency allows.

```sql
WITH kw AS (
  SELECT id, row_number() OVER (ORDER BY ts_rank(search, q) DESC) AS r
  FROM articles, websearch_to_tsquery('english', $1) AS q
  WHERE search @@ q AND tenant_id = $3
  ORDER BY r LIMIT 50
), vec AS (
  SELECT id, row_number() OVER (ORDER BY d) AS r
  FROM (SELECT id, embedding <=> $2 AS d FROM articles
        WHERE tenant_id = $3 ORDER BY d LIMIT 50) AS nearest
)
SELECT id, sum(1.0 / (60 + r)) AS score
FROM (SELECT id, r FROM kw UNION ALL SELECT id, r FROM vec) AS lists
GROUP BY id ORDER BY score DESC LIMIT 20;
```

## 9. Reindexing without downtime

- A full rebuild goes into a new index (`products_v7`) while the old one
  serves. When it is complete and checked (counts, known queries), switch
  atomically: an alias in OpenSearch or Elasticsearch (remove and add in one
  `_aliases` call), a collection alias in Typesense, `swap-indexes` in
  Meilisearch. Keep the old index until the new one has served a while.
- Changes during the rebuild go to both indexes, or the rebuild notes its
  start time and replays later changes before the switch.
- In Postgres, a new index is built with `CREATE INDEX CONCURRENTLY`, and a
  changed `tsvector` expression rewrites the table: plan it like any large
  migration (`database-postgres`).

## 10. Measuring quality

- The query set from section 1, each query with the results that should come
  first, runs after every relevance change; track how often the right result
  is in the top 3 (MRR or nDCG when results are graded).
- Log each search with the normalised query, result count, latency and the
  result clicked, with a user id at most; review zero-result queries each
  week: each is a missing synonym, typo rule or piece of content.
- Server-side budgets: under 100 ms at p95 for search as you type, under
  300 ms for a search page.

## Check it

- `EXPLAIN (ANALYZE, BUFFERS)` on the search query with realistic data: the
  GIN, trigram or HNSW index is used, not a sequential scan.
- The query set passes, and odd input behaves (no error, no timeout): a
  typo, a plural, a quoted phrase, a code, an empty query, one character,
  punctuation only, 1,000 characters.
- Searching as two tenants and as a user without access shows nothing of
  the other in results, counts or facets.
- Change, delete and make private a record: search reflects each within the
  promised delay. Stop the indexer, restart it: it catches up.
- Rebuild the index while searching in a loop: no errors and no empty
  results during the switch.

## Avoid

`ILIKE '%...%'` on a big table without a trigram index; `to_tsvector`
computed per row at query time; an engine added before the database's search
was tried; indexing from the request handler; permissions filtered after the
search; the client choosing its own tenant filter; a public search key with
no embedded filter; deep pagination; highlights rendered as raw HTML;
vectors alone for codes and names; a model change without re-embedding; a
reindex that deletes the live index first.
