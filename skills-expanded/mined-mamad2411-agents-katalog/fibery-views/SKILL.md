---
name: fibery-views
description: Build and edit Fibery views - grids, boards, timelines, gantts, calendars, maps, galleries, feeds, forms, and standalone documents, with filters, grouping, sorting, and color coding. Use when the user wants to see their Fibery data a particular way, asks for a kanban board or roadmap or calendar, needs an intake form, or wants an existing view changed.
---

# Fibery views

A View is a saved way of looking at one or more Databases. `create_view` builds
them, and the `config` shape depends entirely on `viewType`.

**Call `get_fibery_skill` with `{skill: "views"}` before building anything
beyond a flat grid.** That reference carries the complete per-type config
shapes, the full FilterNode operator matrix, and worked examples. This skill
covers choosing a type, the workflow, and the traps that cause retries.

## Choosing a type

| Want | Type |
|---|---|
| Spreadsheet-like table, many fields, hierarchy | `grid` |
| Kanban by status or owner | `board` |
| Roadmap or schedule with bars | `timeline` |
| Roadmap with hierarchy and dependencies | `gantt` |
| Single-date events by month or week | `calendar` |
| Things with addresses | `map` |
| Cards with cover images | `gallery` |
| Rich-text posts, release notes | `feed` |
| Data entry or intake | `form` |
| Plain writing, no data | `document` |
| External page inside Fibery | `embed` |
| Charts and metrics | not here, see `fibery-reports` |

`list` exists but `grid` is better in nearly every case. Prefer grid unless the
user explicitly asks for a list.

## Workflow

1. `schema` for database names.
2. `schema_detailed` for field names, types, and, critically, the **UUIDs of
   enum options and workflow states**. Every reference-type filter value is an
   array of UUIDs, not names.
3. `get_fibery_skill({skill: "views"})` for the config shape.
4. `create_view`.
5. Read it back with `query_views`, or `fetch_view_data` to confirm it returns
   the rows the user expected.

To change an existing view: `query_views` or `search` (with `viewType`) to find
it, then `update_view`. `delete_views` removes views without touching data, and
the user can restore them from the Activity Log.

## The minimum viable view

A flat grid needs no reference lookup at all:

```json
{
  "viewType": "grid",
  "name": "All Features",
  "config": {"items": [{"database": "Product/Feature",
                        "fields": [{"field": "Product/Name"}, {"field": "workflow/state"}]}]}
}
```

A document view takes no `config`, just top-level `content` markdown.

By default the view lands in the space inferred from its databases. Pass
`space` to override, or `"Private"` to keep it to yourself.

## Traps

### Every items database needs its own axis entry

On boards, galleries, timelines, and gantts, the axis arrays are keyed by
`forDatabase`, and there must be exactly one entry per `items[].database`.
Missing one fails with "Unable to find axis config for X".

### Workflow axis databases have a special name

Grouping a board by state means the axis `database` is
`"workflow/state_<Space>/<Database>"`, for example
`"workflow/state_SoftDev/Task"`. It is not `"workflow/state"`.

For grouping by user through assignees, the axis `database` is `"fibery/user"`.

### Axis fields must be relations or enums

A primitive field on an axis is rejected. You cannot make a board column out of
a text or number field.

Mixing enum and relation axes within one axis is also an error. Multiple
databases on one axis works only when all of them are enums (board, gallery,
and gantt only) or all are relations sharing the same target `database`.

### Filter nodeType must match the field type

`FilterNode` is a discriminated union. A workflow field takes
`nodeType: "workflow"` with an array of state UUIDs, not
`nodeType: "text"` with a name.

```json
{"nodeType": "workflow",
 "args": {"fieldPath": ["workflow/state"], "operator": "is-not", "value": ["<done-uuid>"]}}
```

Combine with `nodeType: "logical"` and `operator: "and"` or `"or"`.

For date-range fields, wrap the path: `{"fieldPath": ["q/start", "Space/Dates"]}`.

Relative dates use `{"amount": 7, "unit": "day", "isBeforeNow": true}` as the
value, where `isBeforeNow: true` means N units ago.

### Dependency fields must be marked in the UI first

`timeline` and `gantt` accept a `dependencyField`, but only a relation that has
been explicitly marked as a Dependency in the workspace (Field Settings then
Dependency). A plain relation fails with "is not a dependency field".

When this happens, tell the user which field needs marking and ask them to do
it. Do not retry, and do not silently drop the dependency from the config
without saying so.

### Field type constraints

- `map` `location` must be a `fibery/location` field
- `feed` `post` must be a `Collaboration~Documents/Document` field
- `gallery` `cover` must be a `fibery/file` field
- timeline, gantt, and calendar date fields must be a date, date-time,
  date-range, or date-time-range type

### Hierarchy

`groupBy` nests one items entry under another: `parentIndex` points at the
parent's position in `items`, and `parentField` is a collection field on the
parent's database whose relation targets the child's database. It must be a
one-to-many or many-to-many field.

```json
"items": [
  {"database": "Product/Area", "fields": [{"field": "Product/Name"}]},
  {"database": "Product/Feature", "fields": [{"field": "Product/Name"}],
   "groupBy": {"parentIndex": 0, "parentField": "Product/Features"}}
]
```

### Color coding stacks

All matching `colorCoding` rules apply to an item at once, so overlapping
conditions produce stacked colors. Write mutually exclusive conditions. Use the
standard Fibery palette (`#D40915`, `#FBA32F`, `#4FAF54`, `#2978FB`, `#673DB6`
and the rest listed in the views reference) so the view looks native.

## Forms

Forms are for input, not display. Each field entry takes `displayName`,
`required`, `hidden`, and `defaultValue`, and the `defaultValue` format follows
the field type: a bare value for text, number, bool, and dates;
`{"id": "<uuid>"}` for single relations, single selects, and workflow;
an array of those objects for collections and multi-selects.

A hidden field with a default is the idiom for pinning new submissions to a
starting state.

## Reporting back

Say which view was created, in which space, and what it shows. Confirm it works
by calling `fetch_view_data` with its `publicId` and reporting the row count,
rather than assuming the config did what you intended.
