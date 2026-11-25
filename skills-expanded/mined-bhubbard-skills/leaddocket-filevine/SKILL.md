---
name: leaddocket-filevine
description: >
  Integrate LeadDocket with Filevine for bidirectional lead-to-case sync.
  Covers the lead export workflow (converting accepted leads to Filevine
  projects), user ID mapping between systems, and using the LeadDocket API
  endpoints that have Filevine-specific fields. Use when setting up or
  maintaining the LeadDocket ↔ Filevine integration.
---

# LeadDocket — Filevine Integration

LeadDocket's primary case management integration is with **Filevine**. When a lead is accepted, it can be exported/converted to a Filevine project. Contact and user data is synchronized between the two systems.

> Support section: [Filevine](https://support.leaddocket.com/hc/en-us/sections/360009904132-Filevine)

---

## How the Integration Works

```
LeadDocket (Lead) ──export──▶ Filevine (Project/Case)

1. Lead is created and managed in LeadDocket during intake
2. Lead is accepted (status moved to Active Client or equivalent)
3. Lead appears in the "Pending Export" queue
4. Integration exports the lead to Filevine as a new project
5. Filevine project ID is written back to the lead via updatecode
6. Contact and user cross-references are maintained
```

---

## API Endpoints Used in Filevine Integration

### 1. Get leads ready to export

```http
GET /api/leads/pendingexportids
```

Returns array of Lead IDs that have been accepted and are ready to push to Filevine.

### 2. Fetch full lead data

```http
GET /api/leads/detailed/{id}?flags=RelatedContacts&flags=LeadCustomFields&flags=CollectionSectionEntries
```

Fetch the complete lead data to map to a Filevine project.

### 3. Mark lead as processed (after Filevine project created)

```http
PUT /api/leads/markasprocessed?id={leadId}&markprocessed=true
```

### 4. Store the Filevine project ID on the lead

```http
PUT /api/leads/updatecode?id={leadId}&externalId={filevineProjectId}
```

### 5. Cross-reference users between systems

```http
# Get LeadDocket user by Filevine User ID
GET /api/users/getuserbyfilevineuserid/{filevineUserId}

# Get all LeadDocket users (to build a mapping table)
GET /api/users
# → each user has a FilevineUserId field
```

### 6. Cross-reference contacts

```http
# After creating the Filevine contact, store the Filevine contact ID back
PUT /api/contacts/updatecode?id={contactId}&externalId={filevineContactId}

# Later, look up the LeadDocket contact by the Filevine contact code
GET /api/contacts/getbycode?code={filevineContactId}
```

---

## User Mapping

Build a bidirectional user map at startup:

```js
const users = await fetch('/api/users', { headers: { 'X-API-Key': key } });
const userMap = {};
for (const user of users) {
  if (user.FilevineUserId) {
    userMap[user.FilevineUserId] = user.Id; // Filevine → LeadDocket
  }
}
```

---

## Best Practices

- **Export workflow is one-way**: LeadDocket is the intake system; Filevine is the case management system. Data flows LD → FV, not back.
- **Store cross-references immediately**: After creating a Filevine project, immediately call `updatecode` and `markasprocessed` on the lead to prevent re-export.
- **Map users at startup**: Fetch the user mapping once and cache it — user assignments rarely change.
- **Handle missing Filevine user IDs**: Some LD users may not have a Filevine counterpart. Log these for manual review rather than failing silently.
- **Test with a single lead first**: Before running bulk export, test the full pipeline with a single lead and verify data integrity in Filevine.
