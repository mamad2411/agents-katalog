---
name: using-snow
description: Use when doing anything in ServiceNow via the servicenow MCP tools — incidents, changes, catalog orders, knowledge, approvals, record queries. Establishes the capability probe (read-only? which packages?), encoded-query syntax, attachments, and the error playbook. Load this before the first ServiceNow tool call of a session.
---

# Using ServiceNow (snow-mcp)

Every tool call runs **as the authenticated user** under their normal
ServiceNow ACLs — what they can see and change here matches the UI.

## Step 0 — Orient (once per session)

Call `connection_info`, and `whoami` if identity matters. Read two fields:

| Field | How to act on it |
|---|---|
| `read_only: true` | Say so up front. Never attempt or promise creates/updates/orders/state changes — those tools are not registered. Offer the read path instead (queries, reports, lookups). |
| `tool_packages` | Lists what's deployed (`full` = everything). If a package is absent its tools don't exist — don't hunt for them. |

Older servers lack these fields: then infer mode by whether a write tool
(e.g. `create_incident`) appears in the tool list.

**Missing-package fallbacks:** basic reads always work through the generic
table tools — changes via `query_records` on `change_request`, catalog items
via `sc_cat_item`, KB via `kb_knowledge`. What can NOT be emulated without
the package: change state logic/conflicts/scheduling (`change`), ordering
with variables/carts (`catalog`).

## Queries

`query_records` takes ServiceNow encoded-query syntax (same as UI list
filters): clauses joined with `^`, no spaces around `=`, `^OR` for
disjunction, `ORDERBYDESC<field>` for sorting, dot-walking through reference
fields (`caller_id.department=...`), full-text via `123TEXTQUERY321=<terms>`.
Field names come from `describe_table`; results return display values.

For the full operator set (LIKE/IN/BETWEEN, relative-date helpers,
`javascript:` idioms) read `references/encoded-queries.md`.
For which table holds what (task hierarchy, request chain, approvals,
users/groups) read `references/common-tables.md`.

## Attachments (any record)

`list_attachments(table, sys_id)` → pick an attachment →
`get_attachment(attachment_sys_id)` returns text content inline (size-capped;
oversized files return metadata only). `upload_attachment` attaches a file —
pass binary content base64-encoded with `content_is_base64: true`.

## Error playbook

| Symptom | Meaning / next move |
|---|---|
| 401 | Token expired/revoked — user re-authenticates via `/mcp`. |
| 403 or suspiciously empty results | The *user's* ACLs (same as the UI). Not a server bug; say whose permissions ruled. |
| "…is not available on this instance" / "Requested URI does not represent any resource" | That scoped API isn't enabled. Use the table-tool fallback the error names. |
| "Invalid sys_id … not a number like INC0010001" | You passed a record number. Resolve it first: `query_records(table, query="number=INC0010001", limit=1)`. |

## Limits (REST, not this server)

No background scripts; no UI-action buttons (set the underlying fields — the
convenience tools do this); client scripts/UI policies don't run, but
server-side business rules and validation always do.

## Task skills

`snow-triage` (queue/incidents/SLAs/approvals) · `snow-change` (change
lifecycle) · `snow-order` (catalog ordering) · `snow-report` (counts/trends)
· `snow-kb` (knowledge lifecycle).
