---
name: acumatica-assistant
description: "Acumatica ERP assistant for consultants and integrators. Use for anything Acumatica, even if the user only says \"Acumatica\", an endpoint path (/entity/Default/24.200.001, /api/odata/dac), an entity or DAC name (SalesOrder, SOOrder), a form ID (SO301000), Contract Version 4/5, OData, Excel or Power BI feeds, push notifications or connected apps. Capabilities - (1) REST integration development: generate and review requests and code against the contract-based REST API from a bundled extraction of the Integration Development Guide (2026 R2): sign-in and OAuth, endpoint and contract versions, JSON shape, $filter/$expand/$select, CRUD, actions, inquiries, custom fields, license limits, push notifications, webhooks, 187 documented examples, exact names from a Default/25.200.001 contract snapshot. (2) OData data access: DAC-based and inquiry-based OData v4 reads from the Reporting Tools Guide (2026 R2) plus a 2026 R2 DAC $metadata snapshot for exact DAC, field and navigation names. Trigger on any Acumatica question."
compatibility: "Runtime needs file read + grep over the bundled references. Refreshing references needs web access to beacon.acumatica.com, a clean Acumatica instance for swagger.json and the OData $metadata, and Python 3.10+ (scripts/); none of that is needed to answer questions."
metadata:
  author: Francois Taljaard
  version: "2026.10.3"
  domain: Acumatica ERP
---

# Acumatica Assistant

> **Version disclaimer:** the bundled references are extracted from the **2026 R2** editions of Acumatica's
> Integration Development Guide and Reporting Tools Guide (both edition 2026-09-30). The REST examples use the
> `Default/26.200.001` endpoint and **Contract Version 5**; the OData examples use the
> `/t/<TenantName>/api/odata/{dac,gi}` URLs. A client on an earlier release has older `Default` endpoints with
> **Contract Version 4** syntax and may use the pre-2026 `/OData` (OData 3.0) and `/ODatav4` paths, and every
> instance has its own custom endpoints, customizations, inquiries and user-defined fields. State which release,
> endpoint or interface and contract version you assumed in every answer, and tell the user to confirm entity, DAC,
> field and action names on their instance (`swagger.json`, the Web Service Endpoints (SM207060) form, or
> `/api/odata/dac/$metadata`). The bundled contract snapshot (`references/endpoints/`) is exact for
> **`Default/25.200.001`** (2025 R2, Contract Version 4) only, and the DAC metadata snapshot
> (`references/odata/metadata/`) is a **clean 2026 R2** instance; elsewhere their names are a starting point to
> confirm, not a fact.

Reference-backed assistant for Acumatica ERP consultants and integrators. The rule that makes it trustworthy:
**every material claim comes from a bundled reference and is cited** — never from memory alone. URL shapes,
parameter syntax, header names, status-code meanings, OAuth scopes and DAC or field names are exactly the things a
model guesses plausibly and wrongly.

## 1. Route the request

| Request looks like | Go to |
|---|---|
| write, **review** or fix code or requests against the Acumatica **REST API**: sign in, OAuth / connected applications, read or query records, create or update a sales order / customer / item, run an action (release, confirm shipment), poll a long-running operation, processing forms, generic inquiry data, reports, attachments, custom or user-defined fields, `$filter` / `$expand` / `$select`, "why does my PUT not save", 422 / 429 / 412 errors, endpoint or contract versions, "which endpoint version for 2024 R2", license API limits | § 3 REST integration development |
| "stop polling, get notified of changes", push notifications, SignalR hub, "send data from HubSpot/Zapier into Acumatica", webhooks | § 3, using `references/rest/push-and-webhooks.md` |
| "is there an example of X in the docs", "how does Acumatica document creating a shipment" | § 3 step 3, `references/rest/examples-catalogue.md` |
| an exact REST name: "which entity is screen SO301000", "what fields does SalesOrder have", "is it `CustomerID` or `Customer`", "what can I `$expand` on Shipment", "which action releases a payment and what parameters does it take" | § 3 step 4, `references/endpoints/INDEX.md` |
| **read** Acumatica data for BI, reporting or sync through **OData**: `/api/odata/dac`, `/api/odata/gi`, `/OData`, `/ODatav4`, `$metadata`, Excel or Power BI "From OData Feed", expose a generic inquiry via OData, `_WithParameters`, `$filter` / `$expand` on DACs, deleted or archived records (`PX-ApiDeleted`, `px.GetDeletedRecords()`), CORS for OData, OData licence or roles, "review my Power Query / OData URL", "OData or REST for this?" | § 4 OData data access |
| an exact **DAC, field or navigation-property name**: "fields of SOOrder", "what type is InventoryItem.ItemStatus", "which DACs have LastModifiedDateTime", "how do I join SOOrder to the customer", "what is the OData entity set for Stock Items" | § 4 step 3, `references/odata/metadata/` |

Anything else (screen-based SOAP API, customization / graph / DAC development, SQL against the database, versions
and upgrades, how-to procedures in the UI) is a planned capability, see `MAINTENANCE.md`. Say so, answer what you can
with the caveat that it is not reference-backed, and note that the skill could be extended.

## 2. Ground rules

- **Verify, then cite.** Every URL pattern, parameter, header, status code, scope, role and rule you state must come
  from a file under `references/rest/` or `references/odata/`; say which file (and the guide topic it names). If the
  references do not cover something, say so rather than filling the gap from memory.
- **Never invent an entity, DAC, field, navigation-property or action name.** REST names come from the contract
  snapshot of `Default/25.200.001` (`references/endpoints/`, exact for that endpoint) or from the guide's own
  examples (`examples-catalogue.md`, `Default/26.200.001`). Name only entities, fields and actions found there, say
  which source and endpoint version each came from, and tell the user to confirm them on their endpoint's
  `swagger.json` or `$adHocSchema` (see `rest-api-guide.md` § 2) whenever their endpoint is not the one the name
  was read from. OData names come from the 2026 R2 DAC metadata snapshot (`references/odata/metadata/`): say
  "verified in the 2026 R2 snapshot" and ask for confirmation on the client's `$metadata`; inquiry column names are
  tenant-specific, so derive them from the user's inquiry and the naming rules. Mark anything else as "to confirm on
  your instance".
- **Pin the release, endpoint or interface, and contract version first.** REST: the syntax of `$filter` /
  `$expand` / `$select`, drop-down values and custom fields differs between Contract Version 5
  (`Default/26.200.001`, custom endpoints created from scratch) and Contract Version 4 (`Default/25.200.001` and
  earlier). OData: the DAC-based and inquiry-based interfaces take different URLs, syntax and limits, and pre-2026
  releases document other paths. Ask which Acumatica release and which endpoint or interface the client uses if it
  changes the answer; otherwise default to 2026 R2 (`Default/26.200.001` / Contract Version 5;
  `/t/<TenantName>/api/odata/dac`) and say so. `GET <instance>/entity` and `GET <base>/$metadata` list what an
  instance exposes.
- **Writes go through the REST or SOAP API, never OData and never the database.** OData is read-only. Acumatica's
  supported integration paths are the REST, SOAP and OData APIs, push notifications and webhooks; do not propose SQL
  inserts or updates against the Acumatica database.
- **Prefer OAuth 2.0 / OIDC for new work** and say why: the guide announces that username/password sign-in
  will be discontinued. When the user insists on cookie sign-in, show it with the mandatory sign-out. For OData the
  guide documents basic auth; say what each choice costs in licence terms (conventional user versus API user).
- **Never put real credentials, client secrets, tokens or cookies in examples or logs.** Use placeholders.
- If the user reports a fact the references lack or contradict, say the reference should be updated
  (`MAINTENANCE.md`) rather than silently preferring either.

## 3. REST integration development

Generate or review HTTP requests and client code (any language) against the **contract-based REST API**.

1. **Pin the request**: Acumatica release and endpoint (`Default/<version>`, custom endpoint, `MANUFACTURING`),
   contract version (4 or 5), tenant and branch, authentication (cookie or OAuth flow), the business operation
   (read / query / create / update / action / inquiry / report / file), and what already exists (client,
   session handling). Ask when the release or the contract version changes the answer.
2. **Read** `references/rest/INDEX.md`, then `references/rest/rest-api-guide.md`; for the request shape read
   `references/rest/query-parameters.md`, for sign-in and tokens `references/rest/authentication.md`, for
   version questions `references/rest/endpoint-versions.md`, for change notification
   `references/rest/push-and-webhooks.md`. Read `references/rest/common-mistakes.md` before writing code so
   you produce the documented pattern and not the usual wrong one.
3. **Find the documented example** for the operation: grep `references/rest/examples-catalogue.md` by entity
   (`^## SalesOrder`), action (`/ConfirmShipment`), title words or `$expand=` names. The row gives the method,
   URL, query string and features the guide uses; its link gives the request body. Model the answer on it.
4. **Look up every exact name, never invent it.** Read `references/endpoints/INDEX.md` once, then grep the
   snapshot of `Default/25.200.001`, one entry per line: `entities.md` (entity, form ID, screen title),
   `fields.md` (`Schema.Field : Type`, e.g. `^SalesOrder\.`), `expand-paths.md` (`Entity: Path -> Schema`, what
   `$expand` accepts and which schema holds a nested entity's fields) and `actions.md`
   (`Entity.Action(Parameter: Type, ...)`). Never read `fields.md` whole. The snapshot is **one endpoint
   version**: for `Default/26.200.001` or an older `Default`, check the renames, removals and additions in
   `references/rest/endpoint-versions.md` § 3 and say the name must be confirmed on the instance; for a custom
   endpoint or `MANUFACTURING` it does not apply. It holds names and types only: no key fields, no mandatory
   flags, no drop-down values, no custom or user-defined fields.
5. **Build the request from the rules**: base URL `<instance>/entity/<Endpoint>/<Version>/`; PUT to create or
   update, PATCH for selected fields, GET by keys or ID or with `$filter`, DELETE by keys or ID, POST for
   actions with `{"entity": ..., "parameters": ...}`; `{"value": ...}` wrappers; **every nested entity in
   `$expand`**; contract-version-correct literals and nesting; headers `Accept` / `Content-Type` /
   `Cookie` or `Authorization: Bearer`; `If-None-Match: *` / `If-Match: *` when create-only / update-only
   matters; `PX-CbApiBranch` / `PX-CbApiBusinessDate` when the document must post to another branch or date.
6. **Handle the lifecycle**: 204 from an action means done (no `Location`); 202 means poll the `Location` URL
   with a delay and a ceiling until 204, then re-read the record and check its status; make creates idempotent
   with a deterministic reference of your own;
   422 bodies carry per-field `error`; 429 means the license limits (throttle, do not hammer); PUT/PATCH 200
   does not prove the save, so re-read fields that matter; sign out (or manage the OAuth session) in
   `finally`.
7. **Deliver**: one code or ```http block per request, then a short note: the endpoint and contract version
   assumed, which reference backed each protocol fact, which entity / field / action names are from the
   `Default/25.200.001` contract snapshot, which from the guide's examples and which still need confirmation on
   the instance (`swagger.json`, `$adHocSchema`, Inspect Element), and the feature switches the example requires.
   Offer a test plan (Postman or curl) as a follow-up.
8. **Reviewing existing code** ("review / audit / clean up my Acumatica integration"): grep the code for the
   "Looks like" patterns in `references/rest/common-mistakes.md`, verify each hit against the rule, check the
   entity, field and action names it uses against the snapshot (step 4) when the endpoint matches, and report
   data-affecting defects first (silent non-saves, wrong contract-version syntax, unhandled 202/422), then
   session and license hygiene (sign-out, scopes, throttling), then the rest. Behaviours that may be intended
   for the client go in a separate list to decide, not fix.

## 4. OData data access

Read data (never write) through the **DAC-based** (`/t/<TenantName>/api/odata/dac`) or **generic-inquiry-based**
(`/t/<TenantName>/api/odata/gi`) OData interface: BI feeds (Excel, Power BI), reporting extracts, delta syncs,
"which DAC or field holds X", and reviews of OData URLs or Power Query.

1. **Pin the request**: Acumatica release (2026 R2 URLs, or the 2024 R1 `/OData` OData 3.0 and `/ODatav4` paths),
   interface (DAC or inquiry), tenant login name, authentication (basic or OAuth), the consumer (browser, Postman,
   Excel, Power BI, code), the data (form or DAC, inquiry, fields, filters, delta, deletions), and whether the user
   can send their instance's `$metadata` or inquiry definition. Ask when the release or interface changes the answer.
2. **Read** `references/odata/INDEX.md`, then `references/odata/odata-guide.md` (§ 4–5 for DACs, § 6 for
   inquiries, § 2 for auth / roles / licence, § 7 for CORS, § 8 for Excel and Power BI, § 9 to choose between OData
   and REST). Read `references/odata/common-mistakes.md` before writing or reviewing a request.
3. **Look up every DAC, field and navigation name** in `references/odata/metadata/` (read its `INDEX.md` once):
   `entity-sets.md` for the URL names (`PX_Objects_SO_SOOrder`, `SalesOrder`, `SOOrder`), the key and the
   **non-filterable** fields; `api/INDEX.md` for the type's `File` / `Line` / `Lines`, then read that range of
   `api/members-NN.md`, or grep the bundles for `^PX\.Objects\.SO\.SOOrder\.` (all fields and navigations of a DAC)
   or `\.LastModifiedDateTime : ` (every DAC with that field). Never read a bundle whole. Field lines carry the UI
   display name in quotes, so map the user's wording through it; a `BaseType` means the key and most fields are on
   the base DAC; a navigation line `A.BAccountByCustomerID -> PX.Objects.CR.BAccount (CustomerID=BAccountID)` is the
   `$expand` name and the join. Inquiry columns are tenant-specific: derive names from the inquiry's captions by the
   naming rules (guide § 6) or ask for its `$metadata`. Mark each name "verified in the 2026 R2 snapshot" or "to
   confirm on your instance".
4. **Build the URL from the rules**: base URL and tenant; entity set (DAC) or inquiry title / `<Title>_WithParameters(...)`;
   `$select` of the needed fields only; `$expand=Nav($select=...)` within depth 3; `$filter` with stored values,
   integer foreign keys, navigation paths and `Any` / `All` / `$count` lambdas, bare OData 4.01 literals (`%2b` for
   `+`); `$orderby` with `$top` / `$skip`; headers `PX-ApiDeleted: SHOW`, `PX-ApiArchive: SHOW`, `Accept-Language`
   or `locale`; `px.GetDeletedRecords()` for deletions. Check every `$select` / `$filter` field against the entity
   set's non-filterable list and inquiry filters against the formula-column rule.
5. **Deliver**: one ```http block per request (for Excel or Power BI, the feed URL and the sign-in steps instead),
   then a short note: the release and interface assumed, which reference backed each fact, which names are
   snapshot-verified and which need confirmation on the instance, the licence impact (basic auth = conventional user,
   OAuth = API user) and the reminder that OData is read-only (writes: § 3). Offer the equivalent REST request when the
   user also needs to write.
6. **Reviewing existing requests** ("review my OData / Power Query / BI extract"): grep for the "Looks like"
   patterns in `references/odata/common-mistakes.md`; report wrong-data defects first (unbound inquiry parameters,
   200 without a body, formula-column filters, missing deletions in a delta sync, non-filterable fields), then
   authentication / licence / CORS, then the rest.

## 5. Gotchas (things a careful engineer still gets wrong)

REST API:

- **PUT creates and updates; POST runs actions.** A `POST .../Customer` is not a create. (`rest-api-guide.md` § 5–6.)
- **No `$expand`, no details.** Nothing nested comes back unless named, also on PUT/PATCH responses.
- **Contract Version 5 changed the shapes.** Drop-downs are `{"value": {"id": "CL", "description": "..."}}`
  and filter by ID; date-only fields are `YYYY-MM-DD`; custom fields need `type` and live in `$select`
  (`$custom` is CV4); nested `$select`/`$expand` use parentheses, not slash paths; `contains` replaces
  `substringof`; bare date-time literals replace `datetimeoffset'...'`. (`query-parameters.md`.)
- **PUT writes only what differs and graph logic wins**; PATCH submits regardless; **200 can mean nothing was
  saved** (view-only user, field not settable). Re-read. (`rest-api-guide.md` § 5.)
- **Filtering on detail lines is unsupported**; results are unpredictable.
- **Generic inquiries are read with PUT**, never GET, and need `$expand=<Results entity>`.
- **202 is "in progress"**: poll `Location` with a delay and a ceiling until 204; **204 straight away means done
  and carries no `Location`**, so never index that header unconditionally. Other requests on that form in the
  same session fail meanwhile. Processing forms need the filter PUT and the Process POST in the **same session**.
- **Detail-line and inquiry-row IDs are session-scoped**; only top-level entities have persistent IDs (NoteID).
- **Detail lines are deleted with PUT + `"delete": true`**, not DELETE.
- **No count parameter**: page with `$top`/`$skip` until a short page.
- **Sign out, always.** Unclosed sessions linger 10 minutes and exhaust the license's API session limit;
  trial licenses allow two sessions. OAuth with `api` only also opens a session (closes with the token after
  one hour); `api:concurrent_access` sessions must each be signed out. (`authentication.md`.)
- **The OAuth client ID is `<GUID>@<Tenant>`**, the shared secret is shown once, HTTPS is mandatory, and the
  Resource Owner Password flow is discouraged by Acumatica itself; discover endpoints via
  `/identity/.well-known/openid-configuration`.
- **Rate limiting is silent queuing**: past 50 % of the per-minute limit requests are delayed; more than 20
  queued or 10 minutes waiting is declined (429 on data requests).
- **Push notifications are retried up to five times when you answer with an error** (duplicates) and the
  SignalR destination loses messages with no client connected. Dedupe on `Id`.
- **Multilingual values**: the `[{en:..},{fr:..}]` form in `value` blanks unlisted languages; use the
  `Translations` property.
- **The schema name is not the name you send.** A detail is addressed by its field on the parent (`Details`,
  `$expand=Details/Allocations`), not by its schema (`SalesOrderDetail`). (`references/endpoints/INDEX.md`.)
- **Contract action names are longer than the form's.** `Default/25.200.001` names `Payment.ReleasePayment` and
  `ProjectTask.ActivateProjectTask`, while the guide's examples post to `Payment/Release` and
  `ProjectTask/Activate`, which the contract does not define (workflow-action route). Say which you used.
- **A name from one `Default` version is not a name on another.** `SalesOrder.LastModified` (25.200.001) is
  `LastModifiedDateTime` on 26.200.001; drop-downs are `StringValue` on Contract Version 4 and select types on 5.
- **A system endpoint version appears with its release** (`Default/26.200.001` with 2026 R2) and keeps
  working on later releases; Contract Versions 2–3 died in 2023 R2. Check `GET /entity`. (`endpoint-versions.md`.)

OData (`odata-guide.md`, `odata/common-mistakes.md`):

- **OData is read-only**, and there are **two interfaces with two base URLs**: DACs at `/api/odata/dac`, exposed
  inquiries at `/api/odata/gi`, both under `/t/<TenantName>/` (tenant login name, space as `%20`). 2024 R1 documents
  `/OData/<Tenant>` as **OData 3.0** (`$format=json`, `datetime'...'`) and `/ODatav4/<Tenant>`; on 2026 R2
  `/odatav4/<Tenant>` still works as an undocumented alias of the DAC URL (owner-verified), the inquiry path is
  untested: probe `$metadata`.
- **An inquiry with parameters must be called as `<Title>_WithParameters(Param='x')`**; the plain entity set does not
  bind parameters and returns an empty result without an error.
- **200 with no body is not "no rows"** on the inquiry interface: it means an unsupported query, typically a filter or
  sort on a formula column. Empty results come back as `{"value": []}`.
- **Non-filterable fields are also non-selectable** on DACs (`Cap.FilterRestrictions`; `NoteText`, `DocBal`,
  `CuryRate` and other unbound fields); `Filterable=false` bars every field a derived DAC declares itself.
- **DAC filters use stored values and integer keys** (`ItemStatus eq 'AC'`, `InventoryID eq 41`); inquiry filters use
  the displayed values (`'Active'`). Codes such as `InventoryCD` live on the related DAC: `$expand` it.
- **Inquiries have no `$expand` or `$count`**; DAC expansion stops at depth 3 (`maxExpansionDepth`); aggregation
  (`$apply`) is unsupported everywhere; `+` in a date-time offset is `%2b`.
- **Deletions do not show in a `LastModifiedDateTime` delta.** Track the DAC on SM207010 and read
  `<DAC>/px.GetDeletedRecords()`; `PX-ApiDeleted: SHOW` reveals soft-deleted rows, `PX-ApiArchive: SHOW` archived ones.
- **Basic-auth OData sign-ins are conventional users** (Concurrent Users on SM604000), not API users; OAuth sessions
  are API users. Roles: `BI` for the predefined `BI-*` inquiries, `OData4 User` for DAC-based access, View Only on
  an exposed inquiry; the username carries no tenant suffix.
- **Derived DACs inherit**: `Customer` lists only the fields it adds to `BAccount`; read the base entry too.

## 6. Layout

```
references/rest/   INDEX.md (sources, verified dates, known limits), rest-api-guide.md (start here), query-parameters.md,
                   authentication.md, endpoint-versions.md, examples-catalogue.md (generated), push-and-webhooks.md,
                   common-mistakes.md
references/endpoints/  INDEX.md (lookup recipes, sources, limits) and Default-25.200.001/ (generated from the
                   endpoint's swagger.json): entities.md, fields.md, expand-paths.md, actions.md
references/odata/  INDEX.md, odata-guide.md (start here), common-mistakes.md, and metadata/ (generated from a clean
                   2026 R2 instance's /api/odata/dac/$metadata): INDEX.md, entity-sets.md, api/INDEX.md,
                   api/members-01..06.md, enums.md
scripts/           maintenance only: fetch_beacon_guide.py (cache a guide from beacon.acumatica.com),
                   build_examples_catalogue.py (regenerate the catalogue), build_endpoint_reference.py (regenerate
                   an endpoint snapshot from its swagger.json), build_odata_metadata_ref.py + bundle_util.py
                   (regenerate the DAC metadata snapshot), package_skill.py — never needed to answer
evals/evals.json   test prompts per capability
MAINTENANCE.md     how to refresh the references for a new Acumatica release, add a capability
```

Every `references/` folder has an `INDEX.md` with sources and verified dates per file — read it first, open
only what the request needs.
