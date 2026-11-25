---
name: using-infino
description: How to retrieve from and write to Infino through the Infino MCP server, including choosing keyword vs semantic vs hybrid search, SQL, creating tables, adding and replacing documents, and when to use the CLI instead. Use when the user wants to search, query, recall, store, or manage data in Infino or on object storage (S3/Azure) or Infino Cloud.
---

# Using Infino

Infino is a retrieval engine over data on object storage: full-text (BM25),
vector, hybrid, and SQL search over one copy of the data, embedded in-process
against a local path or bucket, or against a hosted Infino Cloud database.
These tools (from the Infino MCP server) operate on a connected catalog of
tables. The full toolset is always available; you are responsible for the
data you change, and on Infino Cloud the API key's capabilities decide what
the connection may do.

## 1. Discover before you search

- **`infino_list_tables`**: list the tables in the catalog. Start here when you
  don't already know the table name. On a hosted connection a 404 here means
  the database does not exist yet: call `infino_create_database`.
- **`infino_describe_table`**: a table's columns and types, so you know which
  column to target and what each result row carries. It does not report
  indexes; a search on a column with no index says so in its error.

## 2. Pick the search tool by the question shape

- **`infino_keyword_search`**: literal terms such as identifiers, error codes,
  product names, exact phrases. Ranked BM25. Use when the wording is known.
- **`infino_semantic_search`**: meaning or paraphrase when the exact wording is
  unknown. Pass `filter` (`{column, query}`) to first restrict to rows whose
  keyword column matches, then rank semantically within them.
- **`infino_hybrid_search`**: the query has *both* specific terms and an intent.
  Fuses keyword + vector in one ranking pass. A good default when unsure.
- **`infino_sql`**: structural or analytical questions: counts, GROUP BY, joins,
  aggregates, filtering by exact column value. The search functions are
  callable inside SQL too (`bm25_search(...)`, and `vector_search(...)` with a
  `{{name}}` placeholder plus `embed: {name: "text"}`).
- **`infino_token_match` / `infino_exact_match` / `infino_count`**: unranked
  filters and a tally, when you need the set or the number, not an order.

Prefer the dedicated search tools over hand-written SQL for retrieval; they
embed the query and project results for you.

## 3. Write data

The write path, in order. Every write is one commit, durable when the tool
returns.

1. **Create the table** with `infino_create_table`. Use this shape:
   - a stable **key column of type `utf8`** (for example `key` or `doc_id`),
     so rows can be replaced or removed later by predicate;
   - **`large_utf8`** for every text you want to search; these get full-text
     indexes by default;
   - **`vector: true`** if you want semantic or hybrid search. The server adds
     an `embedding` column sized to its own embedder; never type a dimension.
   Keep the result: its `indexes` field is the only record of which columns
   are indexed.
2. **Add rows** with `infino_add_documents`, tens of rows per call, always
   including the key. Rows that omit `embedding` are embedded from their text
   automatically, in one batch. A key that is not a column is an error, not
   silently dropped. Integers for `int64` columns are fine as plain numbers.
3. **Replace rows**: `infino_delete_documents` with a key predicate
   (`key IN ('a', 'b')`), then `infino_add_documents` again. That is two
   commits with a brief window in between; say so if it matters.
4. **Remove rows**: check the predicate first with `infino_count` or
   `infino_sql`, then `infino_delete_documents`. There is no dry run.
5. **Start over**: `infino_drop_table` (with `purge: true` to reclaim storage),
   then create again. Irreversible.

`infino_update_documents` replaces matched rows 1:1 with the rows you pass;
the match count must equal the row count. Use it for in-place edits of a
known number of rows; use delete-then-add otherwise.

## 4. Bulk loads are not for this server

A tool call carries tens of documents. For a whole corpus, files, or a
directory, use the `infino` CLI against the same URI (`infino ingest <table>
--file data.parquet` or `.ndjson`; `infino create-table --from-parquet` to
bootstrap a table from data) or an Infino SDK. The CLI is bring-your-own-
vectors like the engine, so include the `embedding` column in the rows, or
load text-only and search by keyword. Its own skills (`infino skills
install`) cover the commands.

## Tips

- Vectors are embedded by the server (local model by default, no API key);
  the table's vector width must match the embedder. A mismatch is reported
  with both numbers; fix `INFINO_MCP_EMBED_MODEL` or recreate the table.
- `_id` comes back as a string; the engine assigns it. Use your own key column
  to address rows.
- A 403 on a hosted connection means the API key lacks that capability; ask
  for a key with write capability rather than retrying.
- A 409 on add/update/delete means another writer won the commit race and
  nothing was written: reissue the call. A 409 on create means it exists.
- If a tool reports "no vector column" or "no text column", call
  `infino_describe_table` and pass the column explicitly.
