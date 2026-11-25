---
name: leaddocket-lead-sources
description: >
  Retrieve the configured Lead Source list from LeadDocket — the marketing
  channels (Google Ads, Billboard, Referral, etc.) that leads are attributed
  to. Use to populate source dropdowns in intake forms, validate source names,
  or sync lead source data with marketing attribution systems.
---

# LeadDocket — Lead Sources

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

A **Lead Source** is the marketing channel or origin attributed to a lead (e.g., "Google Search", "TV Ad", "Referral", "Website Form"). Sources are configured by admins and selected on leads at intake.

---

## List all lead sources

```http
GET /api/leadsources/list
```

Returns array of `LeadSourceApi`:

```json
[
  { "Id": 1, "Name": "Google Search" },
  { "Id": 2, "Name": "TV Commercial" },
  { "Id": 3, "Name": "Referral Attorney" },
  { "Id": 4, "Name": "Website - Organic" },
  { "Id": 5, "Name": "Billboard" }
]
```

---

## Best Practices

- **Cache this list**: Lead sources change only when an admin adds or removes them. Cache per session.
- **Use IDs for lead updates**: When setting a lead's source from an external system, pass the `LeadSourceId` (from this list) in the lead update payload via `leaddocket-leads` (`PATCH /api/leads/{id}`).
- **Validate before writing**: Cross-reference incoming source names from your marketing platform against this list to prevent invalid source assignments.
- **Prefer lookups for more types**: Some instances expose additional marketing metadata via `GET /api/lookups?type=LeadSources` (see `leaddocket-lookups`) — compare the two lists if needed.
