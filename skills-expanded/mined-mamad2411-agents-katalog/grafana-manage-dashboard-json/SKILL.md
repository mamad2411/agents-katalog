---
name: grafana-manage-dashboard-json
description: Work directly with Grafana dashboard JSON and dashboards-as-code workflows. Use when editing exported dashboard JSON, provisioning dashboards, preparing HTTP API payloads, managing schema or version fields, or generating safe template dashboards from existing Grafana structures.
---

# Grafana Manage Dashboard JSON

Work with Grafana dashboard JSON deliberately. Route the task by dashboard shape first, then by delivery path. Keep edits structural and reversible, and do not invent semantics for managed fields.

## When to Apply

Reference this skill when:

- Editing exported Grafana dashboard JSON directly
- Converting a dashboard between UI export/import, file provisioning, or API payloads
- Preparing legacy `/api/dashboards/db` bodies
- Preparing new Grafana resource-style API bodies
- Sorting out `uid`, `id`, `schemaVersion`, `version`, or `resourceVersion`

## Routing Matrix

Start by identifying the dashboard shape:

| If the artifact looks like | Treat it as | Edit here | Read next |
| --- | --- | --- | --- |
| A dashboard object with `rows`, `panels`, `gridPos`, `targets`, `templating`, `annotations` | Classic dashboard JSON | Root `rows[]`, root `panels[]`, row containers, layout, variables, top-level dashboard fields | `references/dashboard-json-model.md`, `references/panel-json-fields.md` |
| A resource/spec structure with `elements`, `layout`, `timeSettings`, `variables` | Schema v2 | `elements`, layout spec, time settings, variables | `references/dashboard-json-model.md`, `references/schema-and-version-handling.md` |

Then route by delivery path:

| Workflow | Expect | Main concern | Read next |
| --- | --- | --- | --- |
| UI import/export | Classic JSON, V1 Resource, or V2 Resource export shapes | Import/export mode and datasource remapping | `references/import-export-workflows.md` |
| File provisioning | Provisioned files and provider workflow, not API wrappers | Provisioning ignores dashboard `version` | `references/provisioning-and-http-api.md` |
| Legacy API | `POST /api/dashboards/db` with `dashboard` wrapper | Dashboard `version` optimistic concurrency | `references/provisioning-and-http-api.md` |
| New API | Kubernetes-style resource body with `metadata` and `spec` | `metadata.resourceVersion` vs dashboard revision fields | `references/provisioning-and-http-api.md`, `references/schema-and-version-handling.md` |

## Workflow

1. Identify whether the input is classic JSON or schema v2. For classic JSON, first determine whether the layout is root `rows[]`, root `panels[]`, or nested row containers. Do not apply classic panel-editing rules to schema v2 resources.
2. Identify whether the output must be UI-importable JSON, a provisioned file, a legacy API payload, or a new API resource body.
3. Edit the smallest JSON surface that solves the task. Separate layout edits from query or identity edits when possible.
4. Keep identity and version semantics explicit:
   - `uid` is the durable dashboard identity.
   - `schemaVersion` is the dashboard schema revision.
   - `version` is the dashboard revision used by classic dashboard workflows.
   - `id` is database-generated and should not be treated as stable identity.
   - `resourceVersion` is a resource concurrency token for the new API, not the same thing as dashboard `version`.
   - Do not use `schemaVersion` as a proxy for whether panels are modern.
5. Call out Grafana-managed fields before returning a patch or payload.

## Reference Map

- `references/dashboard-json-model.md` -> classic JSON versus schema v2 structure.
- `references/panel-json-fields.md` -> classic panel editing and schema v2 element/layout routing.
- `references/schema-and-version-handling.md` -> `uid`, `id`, `schemaVersion`, `version`, and `resourceVersion`.
- `references/import-export-workflows.md` -> Classic, V1 Resource, and V2 Resource UI import/export paths.
- `references/provisioning-and-http-api.md` -> provisioning, legacy API, and new API payload behavior.
- `references/safe-editing.md` -> Grafana-managed fields and safe hand-editing rules.

## Output

Return the smallest correct JSON change or payload, which workflow it is for, which fields were intentionally preserved or omitted, and how to verify it after import, provisioning, or API submission.
