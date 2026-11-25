---
name: smart-import-v2
description: Use when working on the Excel Smart Import v2 pipeline — parsing workbook sheets, upserting projects, preserving hash-based line IDs, or handling override/scenario data. Clarifies that excelParser.ts and importPipeline.ts are legacy; smart-import-routes.ts plus server/imports/ is the current system.
---

# Smart Import v2

## Current vs Legacy

| Status  | Files                                                     |
|---------|-----------------------------------------------------------|
| Current | `server/smart-import-routes.ts` (~163 KB) + `server/imports/` |
| Current | Runs under the new routes in `server/routes/imports.routes.ts` / `server/routes/imports-admin-extracted-routes.ts` |
| Current | Docs: `docs/smart-import-v2-spec.md`, `-operator-guide.md`, `-known-limitations.md`, `-test-matrix.md`, `-spine-alignment.md` |
| Legacy  | `server/excelParser.ts`                                   |
| Legacy  | `server/importPipeline.ts`                                |

Do **not** extend the legacy files for new Smart Import v2 work. Read them
only if debugging historical behaviour.

## Hard Rules

1. **Projects upsert by `projectCode`.** NEVER wipe or truncate the projects
   table — the import writes only to the rows it touches. If a project exists
   with a given code, update it; if not, insert it. Other projects are
   untouched.

2. **Line IDs are hash-based and stable across imports.**
   - `expense_line_id` — deterministic hash of the line's identifying fields
   - `inflow_line_id` — same, for inflows
   - Re-importing the same workbook must produce the same line IDs. If you
     change the hash inputs, you will orphan every existing override.

3. **Imports write snapshots, not mutations.** The snapshot tables
   (`normalizedCostLines`, `normalizedRevenueLines`, `cashflowPoints`,
   `financeRevenueMonthly`, `financeCosMonthly`, `categoryRevenueAllocations`,
   `projectRevenueSummary`) record `effective_from` / `effective_to`. An
   import closes the previous snapshot (`effective_to = now()`) and inserts
   a new live row (`effective_to = NULL`). Reads MUST filter
   `isNull(table.effectiveTo)` — see the `finance-snapshot-queries` skill.

4. **Overrides / scenarios are stored separately with an audit trail.**
   Never overwrite imported baseline rows with override values. Override
   tables reference the baseline row by hash ID and are applied at read time.

5. **Conflict policy lives in `server/imports/import-conflict-policy.ts`.**
   Consult it before changing how conflicting rows (same hash, different
   values) are resolved.

## Parser (ExcelJS)

- Use `exceljs` (already a dependency) — don't add another parser.
- Sheet names are configured, not hardcoded in handlers. Check the current
  spec at `docs/smart-import-v2-spec.md` before assuming a sheet list.
- Row coordinates and header rows are part of the spec — when the workbook
  changes, the spec changes first, then the parser.

## Operator Workflow

Smart Import v2 runs in distinct phases:

1. **Upload** — workbook staged, not yet applied
2. **Parse + validate** — structured diff surfaced to the operator
3. **Approve** — operator confirms before any DB writes
4. **Apply** — snapshots closed, new rows written, audit entries emitted
5. **Reconciliation** — `qa/generate-reconciliation-evidence.ts` +
   `npm run reconciliation:report` compare import output to source-of-truth

If you change any phase, verify the reconciliation step still passes.

## Known Limitations

See `docs/smart-import-v2-known-limitations.md`. Check that file before
promising a feature works — several edge cases (sub-project splits, blank
scenarios, merged cells) have documented workarounds.
