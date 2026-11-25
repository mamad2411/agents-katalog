---
name: leaddocket-contacts
description: >
  Create, read, update, and search Contacts in LeadDocket via the REST API.
  Covers adding new contacts, fetching by ID or Case Tracker Code, full-record
  updates, searching by name/email/phone, finding recent lead activity by phone
  (useful for phone system integrations), paginated sync via lastupdatedsince,
  and associating contacts with external systems. For custom fields and tags use
  leaddocket-contact-custom-fields; for adding a contact to a lead as a related
  party use leaddocket-lead-relationships.
---

# LeadDocket — Contacts (Core CRUD)

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## Add a new contact

```http
POST /api/contacts
Content-Type: application/json

{
  "FirstName": "Jane",
  "LastName": "Smith",
  "Email": "jane@example.com",
  "Phone": "555-123-4567",
  "Address": "123 Main St",
  "City": "Austin",
  "State": "TX",
  "Zip": "78701"
}
```

Uses the `ContactUpdateApi` schema. Returns the created `ContactApi` object with the new `Id`.

---

## Get a contact by ID

```http
GET /api/contacts/{id}
```

Returns full `ContactApi` object.

---

## Update a contact (full replace)

```http
PUT /api/contacts/{id}
Content-Type: application/json

{
  "FirstName": "Jane",
  "LastName": "Smith-Jones",
  "Email": "jane@newdomain.com",
  ...all fields...
}
```

> ⚠️ **All fields must be sent.** Any field omitted will be overwritten with an empty value. Fetch the existing contact first, mutate, then PUT the full record back.

---

## Look up by Case Tracker Code

```http
GET /api/contacts/getbycode?code={caseTrackerCode}
```

The Case Tracker Code is typically the contact's ID in an external case management system. Set it via `updatecode`.

---

## Search contacts

```http
GET /api/contacts/search?searchTerm={query}
```

| Notes |
|-------|
| Minimum 3 characters required |
| Searches name, email, and phone |
| Results limited to 500 records |

---

## Find recent lead activity by phone (phone system integration)

```http
GET /api/contacts/checkforrecentbyphone?phone={phoneNumber}
```

Returns array of `CheckForRecentByPhoneModel`. Useful for screen-pop integrations — caller ID lookup that surfaces the most recent lead or open opportunity.

- If multiple leads match, returns the newest by `CreatedDate`
- If multiple unresolved opportunities match, returns the newest
- Requires at least 7 digits

---

## Sync — contacts updated since a date

```http
GET /api/contacts/lastupdatedsince?date={ISO8601}&page={n}&itemsPerPage={max500}&sortOrder={order}
```

Returns `LeadApiFlatApiPagedResponse`. Paginate until `next_page` is null.

---

## Associate contact with external system

```http
# Set the Case Tracker Code (external ID)
PUT /api/contacts/updatecode?id={contactId}&externalId={cmsContactId}
```

---

## Best Practices

- **PUT is a full replace** — always GET first, update the fields you need, PUT the full object back to avoid data loss.
- **Search before create** — use `/search` with name/email/phone to check for duplicates before adding a new contact.
- **Phone screen pop**: `checkforrecentbyphone` is designed for real-time use during inbound calls. It normalizes phone number format automatically.
- **lastupdatedsince cursor**: Store the most recent `UpdatedDate` returned; use it as `date` on the next poll to avoid re-processing.
