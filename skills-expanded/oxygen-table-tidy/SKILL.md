---
name: oxygen-table-tidy
description: Inspect and improve OXYGEN Table structure, visibility and formatting while preserving raw data, dependencies and record identity.
---

# Make the Table usable

Read [the runtime contract](../../../docs/runtime-contract.md). Use [oxygen-dedupe](../oxygen-dedupe/SKILL.md) for identity matching; this skill handles columns and presentation.

Discover `oxygen commands get "tables tidy-suggest" --json` and run the suggestion pass read-only on the named Table. Inspect its actual schema, dependencies and a bounded sample.

Group findings by overlapping columns, order, types, formatting, visibility and suspicious values. Similar names do not prove identical semantics. Record the consumers of a proposed change before applying it.

Separate workspace `hiddenByDefault` curation from the user's empty-column collapse. Hidden columns still exist and may feed downstream formulas or AI inputs; hidden is not archived. Prefer a visibility change when the goal is a cleaner view, and keep raw evidence when adding a cleaned/derived value.

A completely blank enrichment column may never have run for older rows. Inspect run/provenance and current backfill preview instead of immediately forcing every row to rerun. Paid backfill requires the selected row scope and current cap.

Apply requested reversible formatting/order/visibility fixes within scope. Present data-changing retypes, archival or paid cleanup concretely before any additional authorization needed. Do not merge records or overwrite raw values as a cosmetic tidy operation.

Re-describe the Table and inspect representative rows after changes. Return what changed, affected dependencies, held suggestions and the Table link.
