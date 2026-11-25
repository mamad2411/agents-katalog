---
name: leaddocket-leads
description: >
  Core skill for reading, querying, and updating Leads in LeadDocket via the
  REST API. Covers listing leads by status, fetching individual leads (full,
  basic, and detailed variants), updating lead properties, looking up leads by
  Case Tracker Code or Opportunity ID, paginated sync via laststatuschangesince
  and lastupdatedsince, and the case-management export workflow
  (pendingexportids / markasprocessed / updatecode). Use for any task that
  involves getting or changing lead data. For status changes use
  leaddocket-lead-status; for notes use leaddocket-lead-notes; for files use
  leaddocket-lead-files.
---

# LeadDocket — Leads (Core CRUD)

All endpoints require API key authentication via the `X-API-Key` header (or
as configured on the instance). Base URL: `https://{instance}.leaddocket.com`.

## Reference
- API Explorer: `https://{instance}/api/explore/index.html`
- OpenAPI spec: `https://{instance}/api/v1/docs`

---

## List leads by status (paged)

```http
GET /api/leads?status={statusId}&page={n}&itemsPerPage={max500}&sortOrder={Ascending|Descending}
```

| Param | Required | Notes |
|-------|----------|-------|
| `status` | No | Status ID integer. Omit to return all. |
| `subStatusIds` | No | Comma-separated sub-status IDs to filter |
| `page` | No | Defaults to 1 |
| `itemsPerPage` | No | Max 500, defaults to 500 |
| `sortOrder` | No | `Ascending` or `Descending` by last status change date |

Returns `LeadApiFlatApiPagedResponse` — flat lead records with pagination metadata.

---

## Get a single lead

### Full detail (throttled — 25 req/min)
```http
GET /api/leads/{id}
```
Returns full `LeadApi` object including notes, messages, files, calls.

> ⚠️ This endpoint is strictly throttled at **25 requests per minute**. For
> batch processing, prefer `/basic/{id}` or `/detailed/{id}` instead.

### Basic (no notes/messages/lists)
```http
GET /api/leads/basic/{id}
```
Same `LeadApi` shape but omits heavy nested lists. Use for high-throughput polling.

### Detailed (opt-in flags)
```http
GET /api/leads/detailed/{id}?flags={flag1}&flags={flag2}
```

Available `flags` values (combine multiple):

| Flag | What it adds |
|------|-------------|
| `Sources` | Lead source info |
| `SeverityLevel` | Severity level |
| `PhoneCalls` | Phone call records |
| `Office` | Office info |
| `Opportunity` | Opportunity info |
| `Creator` | Lead creator |
| `ReferredTo` | Referred-to contact |
| `ReferredBy` | Referred-by contact |
| `LeadStatusHistory` | Full status history |
| `RelatedContacts` | Related contacts |
| `ContactCustomFields` | Contact custom fields |
| `LeadCustomFields` | Lead custom fields |
| `LeadNotes` | Notes |
| `Tasks` | Tasks |
| `Messages` | Messages |
| `LeadFiles` | Attached files |
| `EsignDocuments` | E-sign documents |
| `Settlements` | Settlements |
| `CollectionSectionEntries` | Collection section entries |

---

## Look up leads by alternate key

```http
# By Case Tracker Code (external system ID)
GET /api/leads/getbycode?code={caseTrackerCode}

# By Opportunity ID
GET /api/leads/getbyopportunityid?opportunityId={id}
```

---

## Sync — leads changed since a date

```http
# By last status change
GET /api/leads/laststatuschangesince?date={ISO8601}&page={n}&itemsPerPage={max500}&sortOrder={order}

# By any update (status change OR edit)
GET /api/leads/lastupdatedsince?date={ISO8601}&page={n}&itemsPerPage={max500}&sortOrder={order}
```

Both return `LeadApiFlatApiPagedResponse`. Paginate until `next_page` is null.

---

## Update lead properties (partial)

```http
PATCH /api/leads/{id}
Content-Type: application/json

{
  "AssignedUserId": 42,
  "CaseTypeId": 3,
  "SeverityLevelId": 2,
  "SubStatusId": 7
}
```

Only fields sent are updated (`LeadUpdateApi` schema). Does not replace the whole record.

---

## Case management export workflow

```http
# 1. Get IDs ready to export
GET /api/leads/pendingexportids
# → [123, 456, 789]

# 2. Fetch each lead
GET /api/leads/detailed/{id}?flags=LeadCustomFields&flags=RelatedContacts

# 3. After importing to case management, mark as processed
PUT /api/leads/markasprocessed?id={leadId}&markprocessed=true

# 4. Store the external case ID back on the lead
PUT /api/leads/updatecode?id={leadId}&externalId={cmsId}
```

---

## Best Practices

- **Batch sync**: Use `lastupdatedsince` with ascending sort, process page by page, store the last `UpdatedDate` as a cursor. Re-run from that cursor on the next poll.
- **Avoid `/api/leads/{id}` in loops**: Use `/basic/{id}` or `/detailed/{id}` with only the flags you need to stay under the 25 req/min cap.
- **Paging**: `itemsPerPage` max is 500. Always check `next_page` in the response before stopping.
- **Throttling**: If you hit 429, back off with exponential retry starting at 2 seconds.
