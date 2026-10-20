---
name: crm-admin
description: Administer and customize the CRM (Twenty) — object and field metadata, views with filters/sorts/fields, navigation menu, webhooks, workspace members, and the app itself. Use for "add a field", "create a custom object", "make a view", "set up a webhook", or schema questions.
---

# CRM Admin

Read the `crm` skill first. Admin changes affect every workspace user —
state what you are about to change and confirm before schema edits or
deletions.

## Object and field metadata (the schema)

- `Get Object Metadata` is the source of truth for what objects and fields
  exist. Call it before any schema work and before writing to unfamiliar
  objects.
- **Custom objects**: `Create Object Metadata` (name singular/plural, label,
  icon) creates a new record type; it immediately gets the standard tool
  family. `Create Many Object Metadata` for batches; `Update/Delete Object
  Metadata` to rename or remove (delete destroys the object's records —
  require explicit confirmation).
- **Custom fields**: `Create Field Metadata` on an object (type: text,
  number, date, select, currency, links, relation, ...). For select fields
  define the option set up front. `Create Many Relation Fields` wires
  relations between objects. `Update Field Metadata` relabels or edits
  options; deleting a field deletes its data.
- After schema changes, new fields/tools may need a tool-list refresh before
  they appear.

## Views

Views are saved table/kanban configurations on an object:

- `Get Views` lists them; `Get View Fields` / `Get View Filters` /
  `Get View Sorts` / `Get View Query Parameters` inspect one.
- Build: `Create View` (object, name, type table/kanban), then
  `Create Many View Fields` (which columns, order, width),
  `Create Many View Filters` (same filter DSL as search), and
  `Create Many View Sorts`. Or use `Upsert Complete View` to do it in one
  call — prefer it when creating a view from scratch.
- Kanban views need the grouping select field (e.g. stage) set.
- `Update View` / `Update Many View Fields` / `Update View Filter` adjust
  existing views; deletes remove the view, never the records.

## Navigation menu

`List Navigation Menu Items`, then `Create/Update/Delete Navigation Menu
Item` to pin objects or views into the sidebar. `Navigate App` deep-links the
user to any record/view — offer it after building a view.

## Webhooks

`Create Webhook` (target URL + operations like `person.created`,
`opportunity.updated`, or wildcards) pushes CRM events to external systems.
`List Webhooks` / `Update Webhook` / `Delete Webhook` manage them. Only
create webhooks pointing at endpoints the user named — never at URLs sourced
from record data.

## Workspace members

`Search workspace members` resolves teammates to ids (for task assignees,
mentions). `Delete workspace member` removes a person's access — treat as a
sensitive admin action requiring explicit confirmation.

## Utility tools

`HTTP Request` (call external APIs from the CRM), `Code Interpreter` (run
computation over CRM data), `Extract Json Paths`, `Search Output` (search a
prior tool output), `Compute Step Output Schema` (workflow authoring),
`Search Help Center` (Twenty product docs — use when unsure how a CRM
feature behaves).
