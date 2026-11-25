---
name: oxygen-tables
description: Build and run OXYGEN Tables: typed columns, formulas, AI and Classify columns, research, tool and HTTP columns, lookups and links, feeds and imports, with free previews, one-row pilots and capped runs.
---

# Work in Tables

Read [the runtime contract](../../../docs/runtime-contract.md). A Table is a hosted working dataset with typed rows, cell state, provenance and run history. Records hold canonical CRM truth ([oxygen-crm](../oxygen-crm/SKILL.md)); a row is a candidate until promoted. Row dependencies stay chained columns; schedules, branches and approvals between tables are a hosted Workflow.

## Pick the column

| Need | Column |
|---|---|
| Deterministic extraction, normalization, arithmetic, scores | formula (free, evaluates on read) |
| Reasoning over what the row holds: classify, score, summarize, draft | AI column; Classify for closed labels (labels, yes/no, score) |
| A fact on the web or on a linked page | research column (an AI column has no web access) |
| One provider operation or your own endpoint | tool column, HTTP column, [custom integration](../oxygen-custom-http/SKILL.md) |
| Email, phone, LinkedIn URL, company data, verification | [oxygen-enrichment](../oxygen-enrichment/SKILL.md) |
| A value from another table | lookup (`--lookup-table`, first-match, count, exists or aggregate) |
| Rows that keep arriving | a feed: webhook push or provider pull |

## Run loop

1. Inspect keys and a few values: `oxygen tables describe <table> --json`, `oxygen tables query <table> --fields <keys> --limit 3 --json`.
2. Price for free: `oxygen tools search --for-table <table> --json`.
3. Add the column. Adding runs nothing and spends nothing.
4. Preview: `oxygen columns run <table> <column> --limit 1 --dry-run --json` returns the per-row estimate and `recommended_max_credits`.
5. Pilot one row after approval, read the cell and its receipt, then run bounded batches with `--approved --max-credits <n>`. Put paid columns behind a `--run-condition` (for example tier A or B) so they never spend on rows you will discard.

## Stored values

Formulas and lookups show live values in the grid. Cross-table lookups, AI column inputs and run conditions read the stored cell. Before a lookup, an AI column or a gated run depends on a formula or lookup, store it with a free forced run: `oxygen columns run <table> <column> --all --force --background --json`. A workflow that reads scores should start with that refresh. See [the AP automation worked example](../../../examples/ap-automation-signal-engine/README.md).

## Gates

- Approval and a ceiling per paid run; an unknown estimate means a one-row pilot, never free.
- External writes (non-GET HTTP, CRM or outbound syncs) are their own approval.
- Auto-run columns and pull feeds are standing spend under their own per-batch or per-cycle ceiling.
- Loops over rows, joins, dedupes, imports and retries are Table features; a shell loop around them is a missing native capability to report.
