---
name: sqlx
description: "Applies when building or reviewing SQLx database code in Rust. Covers compile-time queries, connection pooling, transactions, migrations, and testing."
---

# SQLx

## Compile-time queries

1. **`sqlx::query!` and `query_as!` for compile-time SQL checking.** Catches typos, type mismatches, invalid SQL before runtime.
2. **Offline mode for CI:** `cargo sqlx prepare` locally, commit `.sqlx/`, `SQLX_OFFLINE=true` in CI.
3. **`query_scalar!` for single-value queries** (COUNT, EXISTS).

## Connection pooling

4. **Pool once at startup, share via Arc/State.** `max_connections`, `acquire_timeout`. Never per-request.
5. **Nullable columns as `Option<T>`.** Missing Option = runtime error.

## Fetching

6. **`fetch_one`** exactly one. **`fetch_optional`** zero or one. **`fetch_all`** small sets. **`fetch`** streaming for large.

## Transactions

7. **`pool.begin()`, `&mut *tx` as executor, `tx.commit()` explicitly.** Drop = auto-rollback.
8. **Migrations with `sqlx::migrate!()` at startup** or sqlx-cli.

## Types and batch ops

9. **`#[derive(sqlx::Type)]` for enum mapping.** `#[sqlx(type_name = "my_enum")]`.
10. **`QueryBuilder` with `push_values` for batch inserts.** Not looped inserts.
11. **Handle `sqlx::Error` variants explicitly.** RowNotFound (404), unique violation (409), others (500).

## Testing

12. **`#[sqlx::test]`** creates temp DB, runs migrations, provides pool, drops after.
13. **Never `format!` to build SQL.** Always bind parameters.
