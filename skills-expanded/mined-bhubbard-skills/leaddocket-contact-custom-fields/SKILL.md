---
name: leaddocket-contact-custom-fields
description: >
  Read and write custom field values and tags on Contacts in LeadDocket.
  Covers listing available contact custom fields, bulk-updating custom field
  values, adding tags to contacts, and removing tags. Use for contact data
  enrichment, CRM sync, and segmentation workflows. For lead custom fields use
  leaddocket-lead-custom-fields.
---

# LeadDocket — Contact Custom Fields & Tags

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## List all contact custom fields

```http
GET /api/contactcustomfields/list
```

Returns array of `CustomFieldsApi`:

```json
[
  { "Id": 201, "Name": "Date of Birth" },
  { "Id": 202, "Name": "Primary Language" },
  { "Id": 203, "Name": "Preferred Contact Method" }
]
```

Cache this list — it changes only when an admin modifies the field configuration.

---

## Update custom fields on a contact

```http
PATCH /api/contacts/updatecustomfields
Content-Type: application/json

{
  "Id": 5678,
  "CustomFields": [
    { "Id": 201, "Value": "1985-04-22" },
    { "Id": 202, "Value": "Spanish" },
    { "Id": 203, "Value": "Text" }
  ]
}
```

`CustomFieldsUpdateApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `Id` | One of | LeadDocket Contact ID |
| `Code` | One of | Case Tracker Code (alternative to `Id`) |
| `CustomFields` | Yes | Array of `{Id, Value}` pairs |

Only fields included are updated. Returns `200 OK`.

---

## Add a tag to a contact

```http
PUT /api/contacts/{id}/tags/{tagId}
```

`tagId` comes from the tags lookup: `GET /api/lookups?type=Tags` (see `leaddocket-lookups`).

Returns `200 OK`.

---

## Remove a tag from a contact

```http
DELETE /api/contacts/{id}/tags/{contactTagId}
```

Note: `contactTagId` is the **contact-tag relationship ID**, not the tag definition ID. Retrieve it from the contact's `Tags` array (fetch contact with `GET /api/contacts/{id}` — the Tags field contains both the `TagId` and the `ContactTagId`).

Returns `200 OK`.

---

## Best Practices

- **Fetch field IDs first**: Always call `GET /api/contactcustomfields/list` to get current IDs — never hardcode them across instances.
- **Tag lookup**: Get the list of defined tags via `GET /api/lookups?type=Tags` before adding. The `tagId` in `PUT /tags/{tagId}` is the tag definition ID.
- **Removing tags**: The `contactTagId` for the DELETE is different from the `tagId` — it's the per-contact assignment ID. Fetch the contact first and find the right `ContactTagId` in the `Tags` array.
- **Values are strings**: Send all values as strings regardless of field type. Dates: `YYYY-MM-DD`. Booleans: `"true"` / `"false"`.
