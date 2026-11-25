---
name: crm-records
description: Manage CRM record types — people, companies, family offices, campaigns, lists and list members, attachments. Use for creating, updating, deduplicating, enriching, importing, or organizing contact and account data in the CRM (Twenty).
---

# CRM Records

Read the `crm` skill first for connection, naming conventions, composite
fields, and filter syntax.

## People and companies

- **Lookup**: `Search people` / `Search companies` with a text query or a
  filter (`emails.primaryEmail[eq]:jane@acme.com`,
  `domainName.primaryLinkUrl[ilike]:%acme.com%`). `Find person`/`Find company`
  fetches by id with relations.
- **Create**: people need `name.firstName`/`name.lastName`; set
  `emails.primaryEmail`, `phones`, `jobTitle`, `city`, `linkedinLink`, and
  `companyId` to link the employer. Companies take `name`,
  `domainName.primaryLinkUrl`, `address`, `employees`, and any custom fields
  the workspace defines (check `Get Object Metadata`).
- **Dedupe discipline**: before creating, search by primary email (people) or
  domain (companies). If a match exists, `Update` it. For bulk syncs use
  `Upsert people` / `Upsert companies` so re-runs are idempotent.
- **Batch**: `Create people` / `Update companies` (plural) accept arrays; use
  them for any multi-record operation.

## Custom record objects

This workspace also has **family offices**, **campaigns**, **call
recordings**, and **granola connections**, each with the full
Find/Search/Group/Create/Update/Upsert/Delete family. Their fields are
workspace-defined: call `Get Object Metadata` for the object before writing
to it. Treat any other unfamiliar tool family the same way — it is a custom
object with the same verb conventions.

## Lists and list members

Lists are named record collections (e.g. "Q3 outreach"):

- `Create list` with a name and target object type, then `Create list members`
  (plural) to add records by id.
- `Search lists` / `Search list members` to inspect membership;
  `Group list members` for counts per list.
- Removing a record from a list = `Delete list member` (the membership row),
  not the underlying record.

## Attachments

Attachments link files to records: `Create attachment` with the file
reference and the parent record id fields, `Search attachments` filtered by a
record id to list what a record has, `Delete attachment` to remove.

## Enrichment

When PDL enrichment tools are exposed (`enrich-person`, `enrich-company`),
use them to fill missing fields (title, company size, socials) after
creating a bare record — then `Update` the record with what came back.
Never overwrite a human-entered field with enrichment data without asking.

## Reporting on records

`Group people` / `Group companies` aggregate by a field (e.g. people per
company, companies per industry, records created per month). Prefer one
Group call over fetching everything and counting client-side.
