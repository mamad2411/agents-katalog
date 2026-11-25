---
name: leaddocket-opportunities
description: >
  Manage intake Opportunities in LeadDocket — the pre-lead records created
  when a potential client first contacts the firm. Covers fetching by ID,
  paginated sync by created or updated date, listing unprocessed opportunities,
  appending and clearing notes, disregarding, and locking/unlocking for
  concurrent processing. Use for opportunity intake workflows, automated
  triage, and case management system integrations. When an opportunity becomes
  a lead, use leaddocket-leads.
---

# LeadDocket — Opportunities

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

An **Opportunity** is an inbound inquiry or intake record — created before the firm decides to accept the lead. Once accepted, opportunities are converted to Leads.

---

## Get an opportunity by ID

```http
GET /api/opportunities/{id}
```

Returns `OpportunityApi` object.

---

## Sync — opportunities created since a date

```http
GET /api/opportunities/createdsince?date={ISO8601}&page={n}&itemsPerPage={max500}
```

Returns `OpportunityApiFlatApiPagedResponse`. Paginate until `next_page` is null.

---

## Sync — opportunities updated since a date

```http
GET /api/opportunities/lastupdatedsince?date={ISO8601}&page={n}&itemsPerPage={max500}
```

Same response shape. Use this for ongoing sync after initial load.

---

## Get all unprocessed opportunities

```http
GET /api/opportunities/getlistunprocessed
```

Returns array of `OpportunityApiFlat`. "Unprocessed" means not yet converted to a lead or disregarded. Use as a work queue for intake staff or automation.

---

## Append a note to an opportunity

```http
PATCH /api/opportunities/appendnote?opportunityId={id}&note={text}
```

Adds text to the opportunity's notes field. Only works on **unprocessed** opportunities. Returns `200 OK`.

---

## Clear the note on an opportunity

```http
PATCH /api/opportunities/clearnote?opportunityId={id}
```

Removes all note text from the opportunity. Returns `200 OK`.

---

## Disregard an opportunity

```http
PATCH /api/opportunities/disregard?id={id}&reason={text}
```

Marks the opportunity as disregarded (rejected/not pursuing). Returns `OpportunityApi`.

---

## Lock an opportunity (concurrent processing guard)

```http
PATCH /api/opportunities/lock?id={id}
```

Locks the opportunity for **30 minutes**, preventing interactive UI users from opening it. Use when an automated system is processing the record. Returns `OpportunityApi`.

---

## Unlock an opportunity

```http
PATCH /api/opportunities/unlock?id={id}
```

Releases the lock before the 30-minute expiry. Always unlock after processing completes. Returns `OpportunityApi`.

---

## Best Practices

- **Lock before processing**: When an automated workflow picks up an opportunity from `getlistunprocessed`, immediately call `lock` to prevent a UI user from editing it concurrently.
- **Always unlock on error**: Wrap processing in a try/finally and call `unlock` even if processing fails.
- **Use `appendnote` for audit trails**: Log what your system did (e.g., "Screened via intake bot — qualified") before converting or disregarding.
- **Paginate sync**: `createdsince` and `lastupdatedsince` both max at 500 per page. Store a cursor date to resume from after interruptions.
- **`getlistunprocessed` vs. sync**: Use `getlistunprocessed` for queue-style processing of new intakes; use `lastupdatedsince` for downstream sync to other systems.
