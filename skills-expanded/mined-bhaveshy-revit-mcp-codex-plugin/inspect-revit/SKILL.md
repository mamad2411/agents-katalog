---
name: inspect-revit
description: Inspect, query, audit, or summarize an Autodesk Revit 2024 model through Revit MCP Next on Windows 11. Use for active-model context, selections, elements, rooms, levels, warnings, materials, model readiness, counts, views, sheets, or read-only BIM analysis.
---

# Inspect Revit

Prefer one compact preflight call:

Run only on the same Windows 11 desktop as Revit 2024. Stop if the host is not
native Windows or the Revit application is not local.

1. Call `revit.read_bundle` for status, model readiness, current view, small
   element/selection samples, and diagnostics.
2. Call at most one or two focused read tools before answering or paging.
3. Use explicit fields, low limits, and compact presets.
4. Continue with the opaque cursor from `structuredContent.data.cursor` only
when the user needs another page.

Do not run setup commands, support CLIs, or `doctor` as a routine preflight.
For most inspections, target one bundle call plus one focused read; only spend
more round trips when the requested scope or pagination requires them.

Never infer a total from returned array length. Leave `includeTotalCount=false`
unless an exact count is required. Do not parse or reuse cursors after changing
arguments, document state, or generation.

Useful focused tools include `revit.query`, `revit.get_current_view_elements`,
`revit.get_selection`, `revit.get_model_context`, `revit.analyze_model`,
`revit.get_warnings`, `revit.get_material_quantities`, `revit.get_rooms`,
`revit.get_views`, `revit.get_sheets`, and `revit.get_schedules`.

Carry the active document fingerprint and generation into guarded follow-up
calls. Use `preset="geometrySummary"` for compact location/bounds in millimeters,
`preset="summary"` for warnings, and `preset="schedule"` for room reporting.

Read `../../references/tool-map.md` when tool routing is unclear.
