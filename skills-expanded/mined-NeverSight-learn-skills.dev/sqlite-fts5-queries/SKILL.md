---
name: sqlite-fts5-queries
description: Use when writing or debugging SQLite FTS5 queries in Dart (snippet(), bm25(), MATCH) that return empty results or throw. Covers the alias trap (snippet/bm25 are top-level functions taking the table name, not methods on an alias) and the probe-first pattern to isolate SQL from app code.
---

# SQLite FTS5 queries

Debug and write FTS5 queries that return rows. The two traps that cost real debugging time here:

1. **`snippet()` and `bm25()` are top-level functions**, not methods on the alias. `f.snippet(...)` is invalid; correct is `snippet(pages_fts, ...)` — pass the table name, and only reference the alias for columns.
2. **Empty results are usually the query, not the index.** Isolate SQL with a probe before suspecting the rebuild.

## Steps

1. **Probe first.** Write a throwaway script (`tool/fts_probe.dart` style, run with `dart run tool/fts_probe.dart`) that opens the same schema, inserts a row, and runs the candidate SQL variants against an in-memory DB. Completion: the probe prints results (or the exact error) for each variant — SQL bugs are now separated from app-code bugs.
2. **Use top-level `snippet`/`bm25` with the table name**:
   - `SELECT f.title, snippet(pages_fts, 1, '<b>', '</b>', '…', 12) FROM pages_fts f WHERE pages_fts MATCH ? ORDER BY bm25(pages_fts)` — note the alias `f` for columns, the table name inside `snippet()`/`bm25()`.
   - A runtime error like "no such function: f.snippet" is the alias trap.
3. **For natural-language questions use OR semantics.** Split the query into tokens and join with ` OR ` inside MATCH to raise recall; tokenize by stripping punctuation. (Defaults to AND/NEAR behavior can return nothing for multi-word natural-language input.)
4. **Wire the working SQL into the app** and verify end-to-end via the repository layer. Completion: the real search/ask path returns the same rows the probe returned.

## Reference

- FTS5 `snippet(table, col, prefix, suffix, ellipsis, maxTokens)`; column indexes start at 0 for the first column, 1 for the second, etc.
- `bm25(table)` returns lower-is-better rank for `ORDER BY`.
- Rebuild-safe: after a `REBUILD` of the FTS table, re-run the same probe query to confirm the index, not the SQL, was the variable.
