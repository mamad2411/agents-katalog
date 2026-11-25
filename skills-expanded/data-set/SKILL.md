---
name: data-set
description: Create and manage Process Street Data Sets — the lookup tables backing conditional routing, role assignment, and reference data. CRUD on sets + records (incl. bulk CSV import), wire workflow lookup fields, and create dataset incoming webhooks. Use when someone says "create a data set", "create data set", "add records to [dataset]", "wire a lookup field", "data set lookup", "data set webhook", "update data set record", or "data set api".
---

# PS Data Sets & Lookups Skill

## Purpose

Create and manage Process Street Data Sets — the lookup tables that back conditional routing, role assignment, and reference data inside workflows. Handles CRUD on data sets + records, wires lookup fields into workflows, and creates dataset incoming webhooks.

---

## When to Use

- Creating a new lookup table (e.g. county → inspector, plan → SLA tier)
- Bulk-adding records to an existing data set
- Wiring a workflow form field to a data set lookup
- Setting up an incoming webhook so an external system can update records
- Debugging a lookup that's returning empty / wrong records

---

## Reference

- the API reference (`reference/api-reference.md`) — endpoints + filter syntax
- Example pattern: a county→inspector lookup table backing conditional routing

---

## Data Set Anatomy

A Data Set has:
- **Fields** — columns (each with `id`, `name`, `type`)
- **Records** — rows (each record is `{ field_<id>: value, ... }`)
- **Incoming webhooks** — optional; let external systems push record upserts
- **Linked widgets** — workflow form fields can lookup against a data set

---

## Tool Map

| Action | Tool |
|---|---|
| Create a data set | `createDataSet` |
| Read a data set | `getDataSet` |
| Update name/fields | `updateDataSet` |
| Delete | `deleteDataSet` |
| List records | `listDataSetRecords` (paginate) |
| Create a record | `createDataSetRecord` |
| Read a record | `getDataSetRecord` |
| Update a record | `updateDataSetRecord` |
| Delete a record | `deleteDataSetRecord` |
| Bulk import records (CSV) | `importDataSetRecords` — `POST /data-sets/{id}/records/import`, strategy Append/Upsert/Sync |
| Create incoming webhook | `createDataSetIncomingWebhook` |
| List incoming webhooks | `listDataSetIncomingWebhooks` |
| Get / update / delete incoming webhook | `getDataSetIncomingWebhook` / `updateDataSetIncomingWebhook` / `deleteDataSetIncomingWebhook` |

---

## Standard Flows

### Create + Populate a Data Set

1. **Define fields up front** — name + type for each column. Common types: `Text`, `Number`, `Date`, `Email`, `Url`, `Members`
2. `createDataSet` — capture the returned `dataSetId` and the `field.id` for each column
3. For each row of source data, call `createDataSetRecord` with `{ "field_<id>": value, ... }`
4. Verify with `listDataSetRecords` — confirm count matches input

For large loads, use **bulk CSV import** — `importDataSetRecords` (`POST /data-sets/{id}/records/import`, multipart CSV) with strategy `Append` / `Upsert` / `Sync` (Upsert/Sync need a key column). *(verified 2026-06-16 — bulk record creation IS supported now; per-record `createDataSetRecord` is only needed for small/incremental adds.)*

### Wire a Lookup Field to a Workflow

1. Identify the workflow form field that will trigger the lookup (the "key" field, e.g. County)
2. Identify the data set + which field stores the matching key
3. In the code task that fires after the key field, query the data set:
   ```javascript
   const res = await fetch(
     `${API_BASE}/data-sets/${dataSetId}/records?filter[field_${keyFieldId}]=${encodeURIComponent(value)}`,
     { headers: { "X-API-KEY": apiKey } }
   );
   ```
4. Take the first matching record and write the lookup values back into the run via `POST /workflow-runs/{runId}/form-fields`
5. Configure the Code task via `ps-edit` / the CLI `task-config --type Code` for the full code task scaffold

### Set Up an Incoming Webhook

1. `createDataSetIncomingWebhook` — returns a URL the external system POSTs to
2. Share the URL with the source system (Zapier, PA, etc.)
3. Test with a sample payload — confirm the record lands via `listDataSetRecords`

---

## Gotchas

- **Field ID is what writes — name is what humans read.** Always reference records by `field_<id>` in filters and writes.
- **Update is a partial patch by default** — but field deletes require explicit removal via `updateDataSet`, not just omitting in a write.
- **Lookup empty?** Check the filter encoding — `&` and `=` in values break the query string. URL-encode aggressively.
- **Member field** — value is a member id (uuid), not an email. Resolve via `listUsers` first.
- **Pagination** — `listDataSetRecords` returns a cursor; loop until the cursor is null/missing. Don't assume one page is everything.

---

## Output

After any data set operation, return:
- `dataSetId` (and incoming webhook URL if created)
- Record count after the change
- The field map (`field_<id>` → human name) — needed for downstream code tasks
- Any warnings (encoding fixes, missing fields, etc.)

---

## Related Skills

- `ps-search` — find existing data sets first to avoid duplicates
- `ps-edit` / the CLI `task-config --type Code` — for the code task that actually queries the data set inside a workflow
- `ps-build` — when wiring a lookup field into a fresh workflow
