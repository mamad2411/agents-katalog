---
name: cb-analytics-schema
description: |
  Use this skill when the user wants to inspect, discover, or document the
  structure of Couchbase Analytics dataverses and datasets — listing what
  exists, inferring document shapes, or building a data dictionary. Trigger
  when they mention "schema", "dataverses", "datasets", "what fields are in",
  "what's the structure of", "infer_schema", or "Metadata.\`Dataverse\`".
license: MIT
---

# Schema introspection

Three tools cover dataset discovery:

- `list_dataverses(cluster)` — every dataverse in metadata
- `list_datasets(dataverse, cluster)` — datasets, optionally scoped
- `infer_schema(dataset, sample_size, cluster)` — sample N docs, summarise
  observed top-level fields

## Inferring a useful schema

`infer_schema` reads up to `sample_size` documents (default 100) and
returns:

```json
{
  "dataset": "Default.Users",
  "rows_sampled": 100,
  "fields": {
    "id":         {"present_count": 100, "presence_pct": 100.0, "types": ["str"]},
    "name":       {"present_count": 100, "presence_pct": 100.0, "types": ["str"]},
    "age":        {"present_count":  87, "presence_pct":  87.0, "types": ["int"]},
    "addresses":  {"present_count":  62, "presence_pct":  62.0, "types": ["list"]}
  }
}
```

Notes:

- The sample is **unordered**; don't infer cardinality or ordering from it.
- A field with `presence_pct < 100` is optional in the dataset.
- Multiple entries in `types` mean the dataset is heterogeneous — flag this
  to the user.

## Safety

The dataset name is interpolated into a SQL++ FROM clause because SQL++
doesn't support parameterised identifiers. The server validates the name
with a strict regex first; you don't need to worry about escaping. Names
like `Default.\`my dataset\`.sub` (backtick-quoted) are accepted.

## Building a data dictionary

A typical workflow:

1. `list_dataverses` → choose one
2. `list_datasets(dataverse="X")` → enumerate datasets
3. For each, `infer_schema(dataset="X.Y", sample_size=500)` → table of fields
4. Optionally `execute_query_readonly` with `SELECT VALUE COUNT(*) FROM X.Y`
   to add a row count to each entry

## What to avoid

- Don't call `infer_schema` with `sample_size > 10_000` — it does a full
  document scan and will be slow.
- Don't assume the sample covers every variant of the document shape.
  Treat `infer_schema` output as a starting point, not a contract.

## Rate limits & safety

Schema tools split across two rate-limit categories:

- **`read`** (60/sec): `list_dataverses`, `list_datasets`.
- **`query`** (10/sec): `infer_schema`.

`infer_schema` is `query` category — not `read` — because under the hood
it runs a `SELECT` that scans a sample of documents from the dataset.
That makes it relatively expensive and it shares the **same 10/sec
bucket as every other query tool** (`execute_query`,
`execute_query_readonly`, `execute_query_paginated`, `fetch_next_page`,
`explain_query`).

Practical implication: if you're enumerating schemas across many
datasets, you'll hit the query bucket faster than the read bucket.
Recommended pattern: one `list_dataverses` → one `list_datasets` per
dataverse (read budget) → then `infer_schema` calls spaced ≥ 100ms
apart (query budget).

If `RateLimitExceeded` comes back on an `infer_schema`, the bucket is
probably being shared with concurrent `execute_query*` calls. Honour
`retry_after_sec` and back off.

## Related skills

- `cb-analytics-query` — writing and running SQL++ queries against the discovered datasets
- `couchbase-data-modeling` — document shape, field naming, and embedding decisions (server-side modeling)
