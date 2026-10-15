---
name: pg-table-reconciliation
description: "Use this skill whenever the user needs to compare PostgreSQL tables between source and target databases, validate a PostgreSQL migration, inspect source/target schema drift, compare row counts or deterministic table hashes, reconcile table ranges such as schema.* or schema.table lists, or assess migration risk. Prefer this skill for PG/PostgreSQL data diff, database compare, migration validation, source-target database checks, table structure comparison, prefixed table mapping, and production/staging drift analysis."
---

# PostgreSQL Table Reconciliation

Use this skill to reconcile PostgreSQL tables across a source database and a target database. The skill is designed for migration validation, source/target drift checks, schema comparison, row-count validation, optional deterministic hash checks, and migration-risk reporting.

## Core Rule

Run the bundled deterministic script instead of hand-writing ad hoc SQL comparisons:

```text
scripts/pg_reconcile.py
```

Resolve it relative to the directory containing this `SKILL.md`; do not hardcode a local absolute path.

Use `uv run` when available so the inline Python dependency metadata is honored. If `uv` is unavailable, use a temporary Python environment with `psycopg[binary]>=3.2`.

## First Questions

Ask only for missing operational details. Do not ask the user to paste secrets into chat.

| Detail | Default or example | Notes |
| --- | --- | --- |
| Source DSN environment variable | `PG_RECON_SOURCE_DSN` | Ask for the variable name, not the DSN value. |
| Target DSN environment variable | `PG_RECON_TARGET_DSN` | Source and target can use different users, hosts, and databases. |
| Table scope | `public.*` or `users,roles` | `--tables` means same table names on source and target. Bare names default to `public`. |
| Explicit table pairs | `users=roles,orders=archive_orders` | Use `--table-pairs` when the source and target table names differ per pair. |
| Source table prefix | empty | Use when source physical tables are prefixed, such as `src_user`; added only when missing. |
| Target table prefix | empty | Use when target physical tables are prefixed, such as `edu_user`; added only when missing. |
| Data check level | `row-count` | Use `hash` only for selected or reasonably sized tables. |
| Output | `markdown` | Use `json` for automation. |

## Workflow

1. Confirm the databases are PostgreSQL and the user has read-only credentials available through environment variables.
2. Confirm the environment variables are visible in the same shell or Claude Code runtime that will run the script. On Windows, temporary PowerShell `$env:...` values set after Claude Code starts may not be visible to Claude Code commands.
3. If the request uses passwords or full DSNs in chat, redirect them to set environment variables locally and continue with the variable names.
4. Choose the comparison scope:
   - Use `--tables "users,roles"` or `--tables "public.users,public.roles"` when the user names multiple tables without saying which are source vs target; this compares each source table to the target table with the same name.
   - Use `--table-pairs "users=roles"` when the user explicitly says source `users` should compare to target `roles`.
   - Use comma-separated pairs for multiple explicit mappings, such as `--table-pairs "users=roles,orders=archive_orders"`.
   - Use `schema.*` for broad checks. Expansion is source-driven.
   - With `--source-table-prefix`, wildcard expansion includes only source tables that start with that prefix, then strips the prefix from logical report names.
   - With `--source-table-prefix` or `--target-table-prefix`, prefixes are added only when the table name does not already start with that prefix.
5. Start with `--data-check row-count` unless the user explicitly asks for schema-only checks or hash checks.
6. Use `--data-check hash` only after confirming the table set is small enough or the user accepts the configured `--hash-row-limit`.
7. Produce a short executive summary before detailed table findings. Highlight critical and high risks first.

## Risk Interpretation

Treat these as migration risk signals:

| Severity | Examples |
| --- | --- |
| `critical` | Target missing table, target missing source column, primary-key mismatch, incompatible type family. |
| `high` | Row-count mismatch, target adds required column without default, narrowed string or numeric precision. |
| `medium` | Default changed, nullability changed, datetime precision changed, hash mismatch. |
| `low` | Extra nullable/defaulted target columns or metadata differences that are unlikely to block migration. |

If a source table has no primary key, call that out even when row counts match. Hash checks without a stable key can still be useful, but reviewability and repeatability are weaker.

Markdown table-level sections include both source and target table structure details. When the target table is missing, still show the source structure and explicitly state that no target structure is available.

## Command Reference

For exact command templates, CLI options, DSN examples, report-reading notes, and troubleshooting, read:

```text
references/usage.md
```

Read that file when the user needs runnable commands, prefix examples, JSON output, hash configuration, or troubleshooting guidance.

## Table Intent Rules

- If the user lists tables without assigning source/target roles, treat them as same-name comparisons: `--tables "users,roles"`.
- If the user implies `users` is the source table while `roles` is the target table, use an explicit pair: `--table-pairs "users=roles"`.
- If several combinations are requested, preserve the pair order: source table on the left of `=`, target table on the right.
- Bare table names default to schema `public`; use `--default-schema` when the user specifies a different default schema.
- Prefix rules apply to explicit pairs too. If the target prefix is `edu_`, `--table-pairs "users=roles"` maps to target `edu_roles`, while `--table-pairs "users=edu_roles"` keeps target `edu_roles` and never creates `edu_edu_roles`.

## Safety Notes

- Prefer read-only users for both databases.
- Never put passwords or full DSNs in CLI flags, report files, logs, examples, or chat replies.
- Reports can expose sensitive metadata such as table names, column names, primary keys, and row counts.
- The bundled script only reads database metadata and table data; it does not write to either database.
- Before a broad `schema.*` run, ask whether temporary, migration metadata, audit, or historical tables should be excluded.
