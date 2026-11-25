---
name: modeling-patterns
description: Patterns for creating and changing Dataverse tables, columns and relationships (Tabellen, Spalten anlegen/aendern; One-to-Many, Many-to-Many, lookup strategies, naming conventions). Use when the user is designing or modifying a Dataverse / Dynamics 365 schema, adding tables/columns, planning a data model, or considering relationship choices.
---

# Dataverse modeling patterns

The plugin provides tools to read, compare and change Dataverse schemas.
Default approach: read first, then change.

## Workflow for new components

1. **Understand the schema** — check existing tables and naming conventions before creating new ones.
2. **Naming convention** — a consistent publisher prefix (in this example `sample_`) for custom entities and columns. Table names singular, columns in `lower_snake_case_logical_name`.
3. **Choose the primary column** — for lookup-focused tables often `sample_name`, for order/transaction tables a business-relevant identifier.
4. **Plan relationships** — decide deliberately between One-to-Many and Many-to-Many:
   - One-to-Many: 1 parent referenced by N children. The default.
   - Many-to-Many: only if both sides are symmetric and there are no extra attributes per relation. Otherwise prefer a junction entity.
5. **Consider cascade behaviors** — with `delete: cascade`, always check whether the children really should be deleted along with the parent.

## Recommendations

- Before a schema change you are unsure about, call the tool with `dryRun: true` (offered by
  `table_*`, `column_*`, `view_*` and `role_*` writes). Nothing is changed; the result lists the
  exact requests — show them to the user before running the call for real. An update's dry run
  contains the full merged definition it would PUT.
- A write refused with "production environment" is the production guard. Do not work around it:
  plan the change with `dryRun: true`, build it in a dev environment, promote the solution.
- New tables should land in a dedicated standard solution, not in the Default Solution.
- Create `picklist` fields (choices) globally rather than locally per table when reuse is foreseeable.

## Traps that cost time

Everything here has been verified against a real environment or the Microsoft documentation.

### Managed properties are not booleans

`IsValidForAdvancedFind`, `IsAuditEnabled`, `IsCustomizable`, `IsRenameable`,
`CanModifyAdditionalSettings`, `IsGlobalFilterEnabled`, `IsSortableEnabled` and `RequiredLevel` are
managed properties on a **column** and expect an object. `column_add`, `column_update` and
`table_update` now normalise a bare value themselves and report it under
`normalizedManagedProperties` — the table of `ManagedPropertyLogicalName` values is in
[`docs/tools/tables.md`](../../docs/tools/tables.md#managed-properties).

The difference that is easy to miss: `IsValidForAdvancedFind` is a managed property on a **column**,
but an ordinary `Edm.Boolean` on a **table**.

### `componentId` is always the `objectid`, never the `solutioncomponentid`

For tables and columns that means the `MetadataId`. The `solutioncomponentid` is the primary key of the
membership row and makes `solution_remove_component` fail with
`0x8004f021 Cannot find solution component`. `solution_get` returns both separately.

### `rootcomponentbehavior` decides which solution carries the change

0 = include subcomponents (forms and columns travel along automatically and get **no**
membership row of their own), 1 = do not include, 2 = shell only. The same table regularly sits
in several solutions with different behavior — which is why "add the column to the
solution" is a no-op in one and necessary in the next. `solution_get` returns the value
per root component, and `solution_add_component` reports afterwards whether a row was actually
created.

### A PCF update needs a version bump

A solution import only takes over a code component if the version in the `ControlManifest` is
**higher** than the stored one — and reports success in both cases. `solution_import` compares
this after the import and warns (`customControlWarnings`). `pac pcf push` deliberately bypasses the
version check, which is why it "works" in exactly this situation.

### Do not touch forms through raw FormXML

`form_get` returns the structure (tabs → columns → sections → cells → controls) instead of XML and in
the process resolves which code component is attached to a cell — the cell itself only holds a generic
classid plus `uniqueid`, the rest lives in a separate `controlDescription`. `form_add_control`,
`form_replace_control` and `form_remove_tab` encapsulate the four details that otherwise trip you up:
the publisher prefix in the component name, all three form factors, the generic classid together with
`uniqueid`, and a bound column must be published beforehand. Details in
[`docs/tools/forms.md`](../../docs/tools/forms.md).

### `systemform` has no `modifiedon`

Dataverse answers a `$select=modifiedon` with
`0x80060888 Could not find a property named 'modifiedon'`. `modifiedby` and `_modifiedby_value`
are missing as well. To compare states, use `versionnumber` (BigInt), `version`,
`overwritetime` and `publishedon`.

### Reading back right after writing proves nothing

**A read-back without waiting or without a publish is no proof that the write was
discarded.** There are two different mechanisms, and they behave differently —
measured against a real environment:

| Write operation | Read-back without publish |
|---|---|
| `systemform.formxml` (`PATCH`, HTTP 204) | **never becomes current** — after 120 s still the old `formxml` and old `versionnumber` |
| the same form after `publish_customizations` | current immediately, `versionnumber` jumped 12345678 → 23456789 |
| Create metadata | visible after ~3 s |
| Change metadata (`PUT`) | current after ~3 s |
| Delete metadata | gone after ~16 s |

**For forms it is not a cache.** A `PATCH` writes the *unpublished* version, a `GET`
returns the *published* one — until the publish, these are simply two different states. Waiting does
not help here, only `publish_customizations(entities='<table>')`.

**For metadata it is eventual consistency.** `EntityDefinitions` catches up on its own, without any
publish. The publish is still needed so that *clients* see the change.

In practice: after a form write, publish and then read; after a
metadata write, wait briefly and read again. The metadata-writing tools have a
`publish` flag for this and report in the result when they did not publish.

## Local MCP

This MCP runs as a local C# console application. The binary is not started directly,
but through the launcher `scripts/run-server.ps1`, which on every
server start brings it to the version pinned in `scripts/BINARY_VERSION` and downloads it from
the matching GitHub release. If startup fails, check
`release_repo` and the `${CLAUDE_PLUGIN_DATA}/bin/` path.
