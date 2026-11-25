---
name: supabase-schema-drift
description: Detect drift between Supabase SQL migrations and TypeScript code references. Flags columns/tables referenced in .select()/.eq()/.from() that no longer exist after DROP COLUMN or never existed. Use when: new migration merged, before deploying schema changes, after reviews/bookings/providers schema incident.
---

# Supabase Schema Drift Detector

## When to use

- After merging a new migration in `supabase/migrations/`
- When you suspect a `.select('col')` references a dropped column (TS cannot detect this)
- Before a release that touches DB schema
- When getting runtime errors like "column X does not exist"

Real incident this would have caught: **reviews schema drift 2026-04-12** (migrations 385-388 renamed to 414-417, code referenced dropped columns).

## How it works

1. Parse all `supabase/migrations/*.sql` to build the **current schema**:
   - Track `CREATE TABLE` → active table + columns
   - Track `ALTER TABLE ... ADD COLUMN` → add column
   - Track `ALTER TABLE ... DROP COLUMN` → remove column
   - Track `ALTER TABLE ... RENAME COLUMN` → rename
   - Track `DROP TABLE` → remove table
   - Later migrations override earlier ones (chronological order by filename prefix)

2. Scan `src/**/*.{ts,tsx}` for Supabase queries:
   - `supabase.from('X')` → table reference
   - `.select('a, b, c')` / `.select('a, b, nested(x, y)')` → column references
   - `.eq('col', …)`, `.gt(…)`, `.lt(…)`, `.ilike(…)`, `.order('col')` → column references
   - `.insert({a, b})` / `.update({a, b})` → column references

3. Cross-reference: flag every column/table referenced in TS that does NOT exist in the final schema.

## Execution

Run the scanner script:

```bash
npx tsx scripts/schema-drift-check.ts
```

Exit codes:

- `0` — no drift detected
- `1` — drift detected (list printed)

## Report format

```
DRIFT DETECTED — 3 issue(s):

[HIGH] src/components/reviews/ReviewsSection.tsx:48
  Table: reviews
  Column 'author_name' does not exist (dropped in migration 388_reviews_cleanup.sql)
  Suggestion: use 'profiles.full_name' via join

[MED] src/app/api/artisan/claim/route.ts:72
  Table: providers
  Column 'company_name' does not exist (never added, dropped migration 210)

[LOW] src/lib/admin-auth.ts:23
  Table: subscriptions
  Table does not exist in any migration
```

## Limitations

- Dynamic `.select()` strings (template literals with variables) are flagged as "unchecked" not drift
- RPC calls `.rpc('fn_name')` are not validated (would require parsing function bodies)
- Nested selects `provider:provider_id(name)` are parsed but FK validation is best-effort
- Does not validate RLS policies

## Files

- `scripts/schema-drift-check.ts` — the scanner (root of servicesartisans repo)
- This SKILL.md — spec + usage

## Related rules

- `CLAUDE.md` → "Schema Supabase — Règle CRITIQUE" section lists known-dropped columns
- Memory: `servicesartisans-reviews-schema-drift.md` (incident 2026-04-12)
