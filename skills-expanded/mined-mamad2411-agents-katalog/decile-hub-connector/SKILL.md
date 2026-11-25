---
name: decile-hub-connector
description: How augment-it (and any Lossless VC-client workspace) talks to the Decile Hub API — the first per-client custom connector. Use whenever pulling from or pushing to Decile Hub (people, organizations, pipeline prospects, deal shares, deal memos, funds/entities, portfolio companies, capital accounts, notes, tasks, files, events), wiring the Decile connector for a new client, building or maintaining the decile-mcp server, mapping Decile records into the SurrealDB canonical layer, or when the user mentions "Decile", "DecileHub", "DECILE_API_URL", "DECILE_HUB_API_KEY", or a per-client CRM connector. Encodes the auth (raw API token in the Authorization header — no Bearer), the per-tenant subdomain base URL, the THREE distinct pagination patterns, the upsert-by-natural-key write semantics, the custom_data_points / variables (merge-tag) system, and the mapping of Decile people/organizations onto the SurrealDB canonical persons/organizations tables. The authoritative contract is the on-disk OpenAPI spec; this skill is the operating guide on top of it.
---

# Decile Hub Connector

Decile Hub is a VC fund-management + CRM platform. The **Decile Hub API v1** is the first
**per-client custom connector** in the Lossless tree: each VC client has its own Decile
tenant (subdomain), its own API token, and its own `clients/<slug>/.env`. This skill is the
operating guide for pulling from and pushing to that API, and for mapping its records into
our SurrealDB canonical layer.

> **Source of truth.** The authoritative contract is the on-disk OpenAPI 3.0.1 spec:
> `ai-labs/augment-it/clients/humain-vc/inputs/decilehub/202506_decilehub-docs_swagger.yaml`
> (11,970 lines). The full endpoint inventory lives in [`references/endpoint-inventory.md`](references/endpoint-inventory.md).
> When in doubt, read the spec — do not paraphrase Decile's API from memory.

## When to use this skill

- Pulling data from Decile (list/get people, organizations, pipeline prospects, deals, funds, portfolio companies, …)
- Pushing data to Decile (create/upsert people & organizations, add prospects, append notes, create tasks, …)
- Wiring the Decile connector for a **new** client (new tenant subdomain + token in that client's `.env`)
- Building or maintaining the **`decile-mcp`** server (`ai-labs/augment-it/services/decile-mcp/`)
- Reconciling Decile records into SurrealDB `persons` / `organizations`

## Connection contract

| Thing | Value |
|---|---|
| **Base URL** | `https://<tenant>.decilehub.com` — **per-tenant subdomain** (humain-vc → `https://humain.decilehub.com`). All routes are under `/api/v1/`. |
| **Auth** | `Authorization: <token>` — the **raw API token**, **no `Bearer` prefix** (`securitySchemes.api_key` = `type: apiKey, in: header, name: Authorization`). One stale curl example in the docs shows `Bearer` — ignore it; the scheme is a raw apiKey header. |
| **Token source** | Generated in Hub at `/settings/api`. **Legacy tokens are rejected with 403** — must be a current token. |
| **Connection test** | `GET /api/v1/whoami` — returns token kind (`user`/`admin`), the user, the account, `account_user.roles`, and `accessible_pipeline_ids`. Call this first to introspect capabilities. |
| **Content type** | `application/json` (except file upload/download, which is `multipart/form-data` / binary). |

### Env vars (live in the per-client `.env`)

Decile is tenant-scoped, so its config belongs in `clients/<slug>/.env`, resolved through the
workspace connector seam (`services/workspace/`) — **not** in a shared root `.env`.

```
DECILE_API_URL=https://humain.decilehub.com      # the tenant's base URL
DECILE_HUB_API_KEY=<the API token from /settings/api>   # sent raw as the Authorization header
```

> These are Decile's own naming. The earlier spec/README anticipated `DECILE_API_BASE_URL` /
> `DECILE_API_KEY` / `DECILE_TENANT_ID`; we standardize on the **real** names above and the
> tenant is encoded in the URL (no separate tenant id needed).

### The canonical request shape

```ts
const res = await fetch(`${DECILE_API_URL}/api/v1/whoami`, {
  headers: { Authorization: DECILE_HUB_API_KEY, Accept: 'application/json' },
});
```

## Pulling data (reads)

Reads are `GET /api/v1/<resource>` (list) and `GET /api/v1/<resource>/{id}` (show). Two cross-cutting concerns:

### ⚠️ There are THREE pagination patterns — do not assume one

The API is **not uniform**. Detect the pattern per endpoint group (see the inventory for which is which):

| Pattern | Used by | Query params | Response envelope |
|---|---|---|---|
| **A — offset, 0-indexed** | Directory (people/organizations), events, files, tasks, variables, email_templates, account_users, financial_reports | `page` (**0-indexed**; fixed page size, usually 50/100; mostly no `per_page`) | `{ data: [...], pagination: { total_count, current_page, total_pages } }` |
| **B — offset, 1-indexed** | Firm-admin / accounting (entities, capital_accounts, journal_entries, accounting_accounts, capital_calls) | `page` (**1-indexed**, default 1), `per_page` (≤100, default 50) | `{ <resource_key>: [...], page, per_page, total }` — array key varies (`entities`, `capital_accounts`, …); **no nested `pagination`** |
| **C — keyset / cursor** | Newer agent-oriented (activity_entries, deals/shares, deal_memos, portfolio_companies, investments) | `page_token` (opaque, from prior response), `per_page` (≤100, default **25**) | `{ data: [...], pagination: { next_page_token, has_more } }` |
| (D — Base community) | `/base/*` | `page` (1-indexed), `per_page` | `{ items\|posts\|channels: [...], meta: { page, per_page, total, has_more } }` |

### Filtering & custom data points

- Most list endpoints accept resource-specific filters (`name`, `email`, `created_after`, `stage_name`, …) — see the inventory.
- **`custom_data_points`** query param on people/organizations/pipeline_prospects list+show: `*` = all, comma-list = subset, empty = none. Select-type values resolve to **human-readable labels** on read; internal jsonb keys are never returned.
- **`include`** pulls associations (`notes`, `people`, `organizations`, `referred_by`, …); **`fields`** narrows the response.

## Pushing data (writes)

### Prefer the upsert endpoints — they're idempotent and map cleanly to our model

| Endpoint | Natural key | Required fields | Response |
|---|---|---|---|
| `POST /api/v1/person` | **email** | `first_name`, `last_name`, `email` | `201 { status, person_id, changes: { field: [old, new] } }` |
| `POST /api/v1/organization` | **name** | `name` | `201 { status, organization_id, changes }` |
| `POST /api/v1/pipeline_prospect` | person email / org name | `pipeline_id` + `prospect` (exactly one of `person`\|`organization`) | `201 { status, pipeline_prospect_id, changes }` |
| `POST /api/v1/deals/share` | `organization_id` | `organization_id, company_name, the_bet, referring_manager_name, referring_manager_email` | 200 (updated) / 201 (created) |

The singular upsert routes (`/person`, `/organization`, `/pipeline_prospect` — note: **singular**) match-or-create by natural key and return a `changes` diff. This is the right default for sync.

### Bulk create = dedup, not upsert

`POST /api/v1/people`, `/organizations`, `/pipeline_prospects` (plural) process the **first 100** and return `{ created, duplicates, errors }`. Duplicates (by email / name) are **skipped**, not updated — use these for first-load, the singular upserts for ongoing sync.

### Other common writes

- **Notes:** `POST /api/v1/{people|organizations}/{id}/notes` and `/pipeline_prospects/{id}/notes` — body `{ note: { body, context } }`.
- **Tags:** `tag_list` (comma-separated string) adds; `remove_tag_list` removes (upsert routes only).
- **Custom data points (write):** the `custom_data_points` object in person/org/prospect bodies. New fields are defined via `POST /api/v1/pipelines/{pipeline_id}/data_points` (account admin; format enum incl. `string`, `select`, `currency_us`, `url`, …).
- **Not idempotent:** `POST /entities` and journal-entry creates re-create on retry — `GET` first to check.

### Write fields — people & organizations

There is **no standalone Person/Organization schema** — stored fields are dynamic (`data` / `custom_data_points` jsonb). The documented write fields:

- **Person:** `first_name`*, `last_name`*, `email`*, `middle_name`, `phone`, `linkedin`, `tag_list`, `custom_data_points`, `note`, `picture` (base64/URL), `address`, `referred_by`, `organizations: [{ name, title }]`.
- **Organization:** `name`*, `website`, `description`, `tag_list`, `logo`, `custom_data_points`, `note`, `address`, `referred_by`, `people: [associated_person]`.

## Files and attachments — three surfaces, and they are not interchangeable

**Absent from the June 2026 swagger snapshot.** The `/pipeline_prospects/{id}/attachments`
family exists only in the live docs at `https://<tenant>.decilehub.com/docs/api`
— the on-disk spec has just `/api/v1/base/attachments/{id}`. Verified live
2026-08-19; treat live docs as authoritative where the two disagree.

| Surface | Write | Lands in | Data-room copy? |
|---|---|---|---|
| **Prospect / CRM attachment** | `POST /api/v1/pipeline_prospects/{id}/attachments` | The prospect's underlying **organization or person** — the UI's *Files → Organization Attachments* | **No** |
| **Data room** | `POST /api/v1/files` (+ `folder_id`) | A data-room folder; add `attachable_type` + `attachable_id` to *also* show it on the record | Yes |
| **Questionnaire upload** | *(read-only — the founder writes it)* | Arrives via a deal-intake form; readable from the same list endpoint | n/a |

### `POST /api/v1/pipeline_prospects/{pipeline_prospect_id}/attachments`

`multipart/form-data` — `attachment[file]` (binary, required) and optional
`attachment[name]` (defaults to the filename without its extension, matching the
web UI). **No file-type allow-list** is applied here — web-UI parity; the data
room upload endpoint is stricter.

- **`investment`-type pipelines only** — a prospect on a closing/investor pipeline
  returns **403**.
- Requires pipeline **edit** access (`edit_prospects?`), not just read.
- `201` returns the same entry shape as the list endpoint, with `id` and `signed_id`.
- `400` missing `attachment[file]` · `403` wrong pipeline type or no edit access ·
  `404` prospect not in the caller's account · `422` validation.

> **House naming convention for decks:** `<date>_<CompanyName>--<Round>.pdf`
> (`202608_ImpulseLabs--Pre-Seed.pdf`) — `YYYYMMDD` when the send date is known,
> `YYYYMM` when only the month is. VCs see the same company at multiple rounds;
> the round token is what keeps a re-pitch distinguishable from the original.
> Full rule in the `decilehub-interface` skill.

> The `decile-mcp` tool `upload_prospect_attachment` fronts this with
> **`file_data_base64`** instead of multipart — the server does the conversion.
> Don't infer the REST contract from the MCP tool's shape.

### `GET .../attachments` merges two sources — know which you're holding

Entry shape: `signed_id`, `filename`, `content_type`, `byte_size`, `source`,
`name`, `item_id`, `uploaded_at`.

- **`source: "direct"`** — CRM attachments on the org/person, from the Hub UI or
  from `POST /files` with `attachable_type`/`attachable_id`. Carry a `name`.
- **`source: "questionnaire"`** — **files the founder uploaded through a
  deal-intake questionnaire** (e.g. *Submit Your Company*): pitch decks, cap
  tables, supporting docs. Carry an `item_id` matching the filename custom field
  stored on the organization record.

**This is where inbound decks actually live.** A company that pitched through the
intake form has already delivered its deck — check for a `questionnaire` entry
before asking anyone to send one, or uploading your own copy.

Only `direct` entries can be deleted
(`DELETE .../attachments/{attachment_id}`); questionnaire uploads are the
founder's submission and are not yours to remove. Fetch bytes with
`GET .../attachments/{signed_id}/download` — **by `signed_id`, not `id`**.

## Errors

Canonical shape (used on most 4xx):

```json
{ "error": { "code": "validation_failed", "message": "...", "field": null, "valid_values": null, "details": null } }
```

- Common codes: `forbidden`, `bad_request`, `not_found`, `validation_failed`, `invalid_parameter`, `confirmation_required`, `unresolved_variables`, `already_finalized`, …
- **Inconsistency to handle:** a few endpoints (e.g. single `PATCH /pipeline_prospects/{id}` on 400/404/422) return a **bare `{ error: "string" }`** — the client must tolerate both shapes.
- **No rate-limit headers and no webhooks** are defined in the spec. Async jobs poll a `status_url` (e.g. financial reports); some actions return `202` (enqueued).

## Mapping Decile → SurrealDB canonical layer

Decile is a per-client source; everything written into our canonical layer must carry the
client tag (see [[Client-Tagging-on-Canonical-Writes]]). The natural mapping:

| Decile | SurrealDB | Join key | Notes |
|---|---|---|---|
| Person | `persons` | `email` (Decile's natural key) | `data` / `custom_data_points` → person fields; `organizations_with_titles` → affiliation edges |
| Organization | `organizations` | `name` → `slug` (slugify) | `data` / `custom_data_points` → org fields; `logo` (`attached_image`) available |
| PipelineProspect | an `observations`-style relationship | `pipeline_id` + prospectable | stage / probability / rating are pipeline-scoped facts |
| PortfolioCompany | `organizations` (the underlying org) + investment facts | `organization_id` | fund×org pair; investment tranches are separate |

Decile's **upsert-by-natural-key + `changes` diff** mirrors our own upsert discipline (SELECT-by-key → MERGE/CREATE). When syncing Decile → SurrealDB, treat Decile as one `source` and record provenance; do not let a Decile refresh overwrite operator-curated commentary. See the SurrealDB connection contract in [[Connecting-To-And-Using-SurrealDB]].

## The two surfaces this skill backs

1. **This skill** — the operating guide (you're reading it).
2. **The `decile-mcp` server** — `ai-labs/augment-it/services/decile-mcp/` (TypeScript): a typed client that resolves base URL + token from the per-client `.env`, normalizes the three pagination patterns and the error shape, and exposes Decile operations as MCP tools. The spec marks agent-facing operations with `x-agent-tool: true` — those are the tools to expose first. Register with `claude mcp add -s project`.

## See also

- [`references/endpoint-inventory.md`](references/endpoint-inventory.md) — the exhaustive endpoint list, grouped by tag
- The OpenAPI spec: `ai-labs/augment-it/clients/humain-vc/inputs/decilehub/202506_decilehub-docs_swagger.yaml`
- [[Connecting-To-And-Using-SurrealDB]] — the canonical-layer connection + client-tagging contract
- [[Workspaces-as-Tenant-Primitive]] — the per-client connector seam Decile plugs into
- [[Client-Tagging-on-Canonical-Writes]] — every canonical write carries its client
