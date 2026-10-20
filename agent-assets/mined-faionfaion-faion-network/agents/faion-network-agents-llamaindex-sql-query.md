# Llamaindex Sql Query

## Summary

**One-sentence:** Wires LlamaIndex NLSQLTableQueryEngine with table retrieval, read-only DB, and safety constraints and emits a nlsql-spec.

**One-paragraph:** NLSQLTableQueryEngine translates natural language into SQL via an LLM. Without table retrieval the LLM sees the whole schema and burns tokens; without read-only connection it can drop tables. This methodology converts a DB profile into a deterministic nlsql-spec: connection mode, table-retrieval strategy, allowed-tables list, SQL safety hooks.

**Ефективно для:** solopreneur exposing a SQL DB to users via natural-language queries.

## Applies If (ALL must hold)

- Have a SQLAlchemy-compatible DB.
- ≥1 user-facing natural-language query surface.
- DB has ≥5 tables (else hardcode).
- Read-only connection available.
- LLM tokens are bounded.

## Skip If (ANY kills it)

- Single table, fixed SQL — handcraft.
- Write workload — NL→SQL is read-only by design.
- Need joins across systems — use a federated layer.
- Compliance forbids LLM seeing schema.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `db-profile.yaml` | table_count, read_only_dsn, include_tables, schema_size_chars | author |
| `Read-only DB user` | infra | DB admin |
| `LLM creds` | secret | config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[llamaindex-basics]] | Index + query engine foundations. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for include_tables, read-only, schema retrieval, SQL safety. | ~1250 |
| `content/02-output-contract.xml` | essential | nlsql-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Read-write conn used, full-schema dump, SQL injection via prompt, hallucinated columns. | ~700 |
| `content/04-procedure.xml` | recommended | 6-step wiring procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/db-profile.yaml` | Input. |
| `templates/nlsql-spec.md.j2` | Output. |
| `templates/nlsql-spec.md` | Output. Generated from `templates/nlsql-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/nl_sql.py` | Working NLSQLTableQueryEngine. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llamaindex-sql-query.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llamaindex-basics]]
- [[llamaindex-indexes-queries]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on read_only_required (true → enforce read-only DSN), then on table_count (>20 → ObjectIndex; <=20 → include_tables list), then on max-returned-rows cap. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
