---
name: document-revit
description: Plan, inspect, create, or place Revit views, sheets, schedules, tags, rooms, and quantity outputs through Revit MCP Next on Windows 11. Use for drawing-set documentation, room/door/wall schedules, sheet composition, annotations, material takeoffs, or BIM reporting.
---

# Document Revit

Start with `revit.read_bundle`, then use focused discovery:

Run only on native Windows 11 with a local Revit 2024 session.

- views and placement: `revit.get_views`, `revit.get_sheets`
- schedules: `revit.get_schedules`, `revit.get_schedule_fields`
- title blocks and annotation types: `revit.catalog`
- rooms and quantities: `revit.get_rooms`, `revit.get_material_quantities`

Discover title-block type IDs, unplaced printable views, schedule field IDs,
tag types, and room/element unique IDs before composing any change set. Note
that placed `titleBlockIds` are instances, not title-block type IDs.

Create sheets, place views, create/add/place schedules, create text notes, load
vetted tag families, and tag rooms/elements only through
`revit.preview_change_set` followed by an exact `revit.apply_change_set`.

Keep reporting calls bounded. Use room `preset="schedule"`, warning
`preset="summary"`, and explicit schedule fields. State the scope, units, and
whether counts are exact or paged. Verify created documentation with the
corresponding read tools after apply.

Dimension creation is not currently supported by Revit MCP Next; do not invent
a tool or fall back to arbitrary code execution.

Keep the connector budget tight: one bundled context call, one focused catalog
or documentation read when needed, preview, apply, and one verification read.
Do not call setup or doctor during normal documentation work.
