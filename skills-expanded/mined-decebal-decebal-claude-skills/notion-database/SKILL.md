---
name: notion-database
description: >-
  Work with a Notion database as a documentation surface — add rows that are pages, change a schema,
  build a view, wire a relation so a filtered view picks a row up. Covers the two irreversible schema
  operations and the filters the view language accepts but discards. Triggers - "add a column to that
  database", "the row isn't showing in the view", "add a select option", "drop that property", "new row
  in the variables database", "build a filtered view", "the filter didn't apply".
---

# Notion databases

What a database is for in a given space, and conventions such as a per-specification variables database,
belong in that space's style guide. This file carries the call shapes.

## Rows are pages

`notion-create-pages` with a `data_source_id` parent takes `properties` and `content` in one call, so a
row and its body land together. Fetch the database first — `notion-fetch` on its URL returns the schema
and the `collection://` URL of each data source, and a database with more than one data source cannot be
addressed by `database_id`.

A filtered view picks a new row up only once the relation its filter reads is set. A row missing from a
view is nearly always a row whose relation was never written.

## Schema changes

`notion-update-data-source` takes SQL-shaped statements. Two are irreversible:

- **`ALTER COLUMN "X" SET SELECT(...)` replaces the whole option list.** Every surviving option must be
  re-listed in the same statement, or its values are dropped from every row that carried them.
- **`DROP COLUMN` has no undo here.** Where the column carries anything worth keeping, migrate it into the
  row bodies first, read one row back to verify, and only then drop.

Rows move between databases with `notion-move-pages` and a `data_source_id` parent, when the schemas
match.

## Views

- **The view DSL accepts filters it cannot express, then discards them** — a verification filter can
  return success with an empty filter group. Read the filter tree back from the response rather than
  trusting it.
- **Formula properties filter as text** whatever they return, so `<` against a date formula is rejected.
  Pair a human-readable date formula with a state-string formula, and filter on the second.
- **Database templates cannot be created.** Change a default template by overwriting the registered
  template page in place.

## Related

`notion-editing` for the edit mechanics every one of these calls inherits. `notion-specification` for the
variables database a specification owns.
