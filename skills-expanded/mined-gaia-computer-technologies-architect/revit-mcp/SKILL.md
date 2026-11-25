---
name: revit-mcp
description: Query and carefully edit a Revit model for an architect, either through a connected Revit MCP server (Autodesk's official Revit Public MCP for Revit 2027.2, read-only by default, or a community server for older versions) or by writing pyRevit / Dynamo / Revit API scripts to run by hand. Pulls schedules, rooms and areas, parameters, warnings, and sheet lists; any write is preceded by a dry-run list of affected element IDs. Use when the architect wants to "ask my Revit model", "export a room schedule", "find empty parameters", "list model warnings", "batch rename sheets", "write a pyRevit script", or "Dynamo for this". Hands to area-check for area maths, ifc-query for openBIM files, drawing-register-qa for sheet issue checks, and tool-setup to connect the MCP.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Revit via MCP

A Revit model is a shared, contractual record. Treat it that way: read freely, write rarely, and never write to a live central model without the architect seeing exactly what will change.

## When to use

- Questions answered from model data: room areas, door counts, unplaced rooms, empty mandatory parameters, warnings, sheets and views.
- Bulk housekeeping: renumbering, renaming sheets or views, filling parameters from a table.
- Writing or fixing a pyRevit, Dynamo, or Revit API (C# / Python) script.

## Two modes

**Live (MCP connected).** Use the server's tools. Prefer the official Autodesk Revit Public MCP **Read** add-on; treat its Write add-on as a preview. Community servers cover older Revit versions but the ecosystem is fragmented. See [references/tool-notes.md](references/tool-notes.md). If nothing is connected, hand to `tool-setup`.

**Script (no MCP).** Write pyRevit (IronPython 2.7 or CPython via pyRevit's engine; ask which) or a Dynamo graph described node by node. The architect runs it. You cannot see the result, so say so.

## Input

- Revit version (it determines which MCP and API features exist).
- Is this a workshared central model, a local copy, or a detached file?
- The question or change, in the architect's terms ("all doors on Level 2 without a fire rating value").
- For edits: the source data (a CSV of new sheet names, a parameter mapping).

## Process

1. **Establish the model context.** Version, worksharing state, active document name, project units. If workshared and the request involves writes, stop and ask them to work on a detached copy or confirm they have synchronised and backed up.
2. **Read first.** Answer from the model with the tool or a read-only script. Report the counts and the filter used ("Doors category, Level = 'Level 2', parameter 'Fire Rating' empty: 14 elements"). Numbers come from the model, never from estimates.
3. **Writes: dry run, then confirm.** Before any modification, produce a table of element ID, category, current value, and proposed value. Wait for an explicit yes. Then apply inside a single transaction (or the MCP's equivalent) so one undo reverts it.
4. **Verify after writing.** Re-query the changed elements and report before and after.
5. **Report what you could not check.** Linked models, design options, phases, and worksets can hide elements. Say which filters you did and didn't apply.

## Scripting rules

- **Never invent API members.** The Revit API is large and version-specific. Use well-known classes (`FilteredElementCollector`, `BuiltInCategory`, `BuiltInParameter`, `Transaction`, `SpatialElement`). If unsure, say so and point to the docs: revitapidocs.com (community index) or Autodesk's API reference for the version.
- **One transaction per logical change**, named clearly, so the undo history reads well.
- **Handle units.** Revit stores lengths in decimal feet and areas in square feet internally. Convert with `UnitUtils.ConvertFromInternalUnits` (API 2021+ uses `UnitTypeId`). State the conversion.
- **Rooms:** an unplaced or unbounded room has zero area. Exclude it and report it separately, never silently.
- **Dynamo:** list nodes by their exact names, packages required (name and version), and the wiring. Prefer out-of-the-box nodes.

## Domain knowledge

- **Room vs Area vs Space.** Rooms (architectural) are bounded by walls and room separators. Areas belong to area schemes (gross, rentable). Spaces are MEP. Ask which the brief means.
- **Area measurement rules differ** by jurisdiction and scheme (e.g. RICS / IPMS in the UK and internationally, BOMA in the US, DIN 277 in Germany). Revit computes geometry; whether it matches the measurement standard is a separate check: hand to `area-check`.
- **Warnings** cluster: overlapping walls, room separation lines on walls, duplicate marks, and elements slightly off axis. Report counts by warning type, and the top offenders by element ID.
- **Sheets:** sheet number, name, current revision, and "Appears in Sheet List" are the fields that drive an issue. Hand register checks to `drawing-register-qa`.

## Output format

```
## Revit: [question]

**Model:** [file] · Revit [version] · [central / local / detached] · units [project units]
**Mode:** [live MCP: server name / script]

**Answer:**
[table or counts, with the filter used]

**Excluded / not checked:** [unplaced rooms, linked models, design options, phases]

**Proposed changes (only if writing):**
| Element ID | Category | Current | Proposed |
|---|---|---|---|
Awaiting your confirmation before applying.
```

After a confirmed write: the same table with an "Applied" column and the transaction name.

## What you don't do

- Don't write to a workshared central model without a confirmed backup or detached copy, and an explicit yes on the dry-run table.
- Don't delete elements as a side effect of anything. Deletion is its own request.
- Don't infer code compliance from parameters. A door with "Fire Rating = 60" is a parameter value, not a fire rating. Flag fire, egress, and accessibility questions for a qualified professional.
- Don't claim a script works if you couldn't run it.
- Don't invent API members or Dynamo nodes.
