---
name: leaddocket-lead-custom-fields
description: >
  Read and write custom field values on Leads in LeadDocket. Covers listing
  all available lead custom fields (to get IDs), getting a single field value
  on a lead, updating a single field, and bulk-updating multiple fields at
  once. Use when syncing lead data with external systems, capturing intake
  data in custom fields, or building dynamic field-update workflows. For
  contact custom fields use leaddocket-contact-custom-fields; for collection
  sections (repeating field groups) use leaddocket-collection-sections.
---

# LeadDocket — Lead Custom Fields

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## List all lead custom fields

Fetch the field catalog to get IDs before reading or writing values.

```http
GET /api/customfields/list
```

Returns array of `CustomFieldsApi`:

```json
[
  { "Id": 101, "Name": "Date of Incident", "Location": "Intake" },
  { "Id": 102, "Name": "Insurance Carrier", "Location": "Case Details" },
  { "Id": 103, "Name": "Medical Records Received", "Location": "Documents" }
]
```

Cache this list — it changes only when an admin adds or removes fields.

---

## Get a single custom field value on a lead

```http
GET /api/leads/getcustomfield?id={fieldId}&leadId={leadId}
```

Returns the raw value for that field on the lead. Returns `200 OK` with the value.

---

## Update a single custom field on a lead

```http
PUT /api/leads/updatecustomfield?id={fieldId}&leadId={leadId}&value={value}
```

Returns `200 OK`. Simple, good for one-off field updates.

---

## Bulk update custom fields on a lead

```http
PATCH /api/leads/updatecustomfields
Content-Type: application/json

{
  "Id": 1234,
  "CustomFields": [
    { "Id": 101, "Value": "2026-03-15" },
    { "Id": 102, "Value": "State Farm" },
    { "Id": 103, "Value": "true" }
  ]
}
```

`CustomFieldsUpdateApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `Id` | One of | Lead Docket Lead ID |
| `Code` | One of | Case Tracker Code (alternative to `Id`) |
| `CustomFields` | Yes | Array of `{Id, Value}` pairs |

Only the fields included in the request are updated — other fields are untouched. Returns `200 OK`.

---

## Best Practices

- **Always use `/customfields/list` first**: Never hardcode field IDs — they vary per instance. Cache and refresh on demand.
- **Prefer bulk update**: When setting multiple fields, `PATCH /updatecustomfields` is more efficient and atomic than multiple `PUT /updatecustomfield` calls.
- **Values are always strings**: Even for dates, booleans, or numbers — send as string. The platform handles type coercion based on the field definition.
- **Use Code for external-initiated updates**: If your system knows the Case Tracker Code but not the Lead Docket Lead ID, use the `Code` field in `PATCH /updatecustomfields` to avoid a lookup round-trip.
- **Date format**: For date fields, use `YYYY-MM-DD`. LeadDocket accepts ISO date strings.
