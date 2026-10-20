---
name: redis-query-search
description: Search and query in Redis, the Redis Query Engine (FT.* commands), JSON documents, full-text queries, and vector similarity search. Use when the user wants to index, search, or do vector/semantic retrieval in Redis.
---

# Redis Query and Search

The Redis Query Engine (the FT.* command family, formerly RediSearch) ships
in Redis 8 Open Source by default; on older setups it comes via Redis Stack
or Redis Cloud. Verify with `FT._LIST` (errors if unavailable). It indexes
hashes or JSON documents by key prefix.

## JSON documents

```
JSON.SET product:1 $ '{"name":"Mug","price":12.5,"tags":["kitchen"],"desc":"Ceramic mug"}'
JSON.GET product:1 $.price
JSON.NUMINCRBY product:1 $.price 1
JSON.ARRAPPEND product:1 $.tags '"gift"'
```

JSONPath (`$...`) addresses subfields; writes are atomic per command.

## Create an index

```
FT.CREATE idx:products ON JSON PREFIX 1 product: SCHEMA
  $.name  AS name  TEXT
  $.desc  AS desc  TEXT
  $.price AS price NUMERIC SORTABLE
  $.tags.* AS tags TAG
```

- Indexing is automatic and asynchronous from then on: any key matching the
  prefix is indexed on write. `FT.INFO idx:products` shows doc counts and
  indexing errors (`hash_indexing_failures` is the field-type-mismatch tell).
- For hashes: `ON HASH`, and schema paths are plain field names.
- `TAG` = exact-match categories; `TEXT` = stemmed full text; `NUMERIC` for
  ranges; `SORTABLE` enables fast ORDER BY on that field.

## Query

```
FT.SEARCH idx:products '@name:(ceramic mug)' RETURN 2 name price
FT.SEARCH idx:products '@tags:{kitchen} @price:[10 20]' SORTBY price ASC LIMIT 0 10
FT.SEARCH idx:products '%mugg%'                     # fuzzy (Levenshtein 1)
FT.SEARCH idx:products 'cera*'                      # prefix
FT.AGGREGATE idx:products '*' GROUPBY 1 @tags REDUCE COUNT 0 AS n SORTBY 2 @n DESC
```

Syntax notes: `@field:` scopes a clause; `{...}` for TAG values (escape
special chars with `\`); `[min max]` numeric ranges (`-inf`/`+inf` allowed);
combine with spaces (AND) and `|` (OR); negate with `-@tags:{gift}`.

## Vector search

Index with a VECTOR field (JSON stores the embedding as a number array):

```
FT.CREATE idx:docs ON JSON PREFIX 1 doc: SCHEMA
  $.text AS text TEXT
  $.embedding AS vec VECTOR HNSW 6 TYPE FLOAT32 DIM 1536 DISTANCE_METRIC COSINE
```

KNN query (query vector passed as a binary blob param):

```
FT.SEARCH idx:docs '(*)=>[KNN 10 @vec $qv AS score]'
  PARAMS 2 qv "<1536 float32 little-endian bytes>"
  SORTBY score ASC RETURN 2 text score DIALECT 2
```

Python side:

```python
import numpy as np
qv = np.array(embedding, dtype=np.float32).tobytes()
r.ft("idx:docs").search(Query('(*)=>[KNN 10 @vec $qv AS score]')
    .sort_by("score").return_fields("text", "score").dialect(2), {"qv": qv})
```

Gotchas:
- `DIALECT 2` (or a client that sets it) is required for KNN syntax.
- `DIM` must equal the embedding model's output size; TYPE FLOAT32 must match
  the bytes you send, a mismatch returns garbage distances, not errors.
- Hybrid filtering goes in the pre-filter parens:
  `'(@tags:{kitchen})=>[KNN 10 @vec $qv]'` filters BEFORE the KNN.
- `HNSW` = fast ANN (tune `EF_RUNTIME` for recall); `FLAT` = exact, fine
  below ~100k vectors.
- Lower cosine distance = more similar (it is a distance, not a similarity).

## Operational notes

- Rebuild after schema changes: `FT.DROPINDEX idx` (WITHOUT `DD` keeps the
  data), then FT.CREATE again; it reindexes existing keys in the background.
- Long analytical scans belong in `FT.AGGREGATE` with `LIMIT`; unbounded
  result sets over big indexes will hurt latency for everyone.
