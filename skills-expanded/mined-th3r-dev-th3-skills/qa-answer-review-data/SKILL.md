---
name: qa-answer-review-data
description: >-
  Data lens of qa-answer-review: check the fields, keys, units and cardinalities a prepared meeting
  answer names — do they exist in the API DTOs and the database tables, with that meaning, and can
  they join (matching key, transaction ↔ measurement, parent ↔ child document). Use WHENEVER the
  work is "data review of a prepared answer", "does the field we say they must send exist", "what
  can be the matching key", "field นี้มีในระบบจริงไหม", or when qa-answer-review fans out its lenses.
  Read-only.
---

# Data lens

Per row: **does every field, key and unit named here exist, mean what the answer implies, and join?**

## Check

1. **Field lists.** Map each named field to the external DTO and to its table column. Column
   comments or the ORM entity often carry the user-facing label — search there first. Missing field,
   renamed field, extra required field → `ADJUST` with the exact list.
2. **Units and bases.** Litres vs kg, temperature-corrected vs observed, local vs UTC, AD vs BE
   years. Quote the column / DTO name and its unit.
3. **Keys and joins.** What links a child record to its parent, and an API record to the document
   it ends up in. Write down the facts already paid for (a key that is unique only per company, a
   table that has no foreign key back to the header). A "matching key" proposal that ignores them
   is `ADJUST`.
4. **Cardinality.** 1 : many where the answer assumes 1 : 1 — check the schema (FK direction,
   unique constraints).
5. **Counts.** When the answer implies data exists today, report the global count and the one
   filtered to this customer. One without the other is how "no data" gets mistaken for "broken".

Quote identifiers exactly as the database needs them (case, quoting). Backup / temp tables with the
same columns are not the live ones. `N/A` for rows that name no field, key or unit. Output contract
and tone rules: `answer-review/SKILL.md` §1.
