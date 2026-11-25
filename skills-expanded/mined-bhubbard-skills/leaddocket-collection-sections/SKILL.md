---
name: leaddocket-collection-sections
description: >
  Read and write Collection Section entries on Leads in LeadDocket. Collection
  Sections are repeating structured data groups (e.g., multiple accident
  vehicles, multiple medical providers, multiple injuries) attached to leads.
  Covers fetching all entries for a section, inserting new entries, updating
  existing entries, and deleting entries. Use when a lead captures repeated
  structured records in a named section.
---

# LeadDocket — Collection Sections

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

A **Collection Section** is a named group of repeating field rows on a lead. For example, a Personal Injury intake may have a "Vehicles Involved" section where each row captures VIN, make, model, and year for each vehicle in the accident.

---

## Get all collection sections for a lead

```http
GET /api/leads/{leadId}/collectionsections
```

Returns array of `CollectionSectionApiWrapper`:

```json
[
  {
    "SectionId": 10,
    "SectionName": "Vehicles Involved",
    "Entries": [
      {
        "EntryId": 1001,
        "Fields": [
          { "FieldId": 301, "FieldName": "VIN", "Value": "1HGBH41JXMN109186" },
          { "FieldId": 302, "FieldName": "Make", "Value": "Honda" },
          { "FieldId": 303, "FieldName": "Model", "Value": "Accord" },
          { "FieldId": 304, "FieldName": "Year", "Value": "2019" }
        ]
      }
    ]
  }
]
```

---

## Insert new entries into a section

```http
POST /api/leads/{leadId}/collectionsections/{sectionId}
Content-Type: application/json

{
  "Entries": [
    {
      "Fields": [
        { "FieldId": 301, "Value": "2T1BURHE0JC045871" },
        { "FieldId": 302, "Value": "Toyota" },
        { "FieldId": 303, "Value": "Corolla" },
        { "FieldId": 304, "Value": "2018" }
      ]
    }
  ]
}
```

`CollectionSectionInsertApi` — returns `200 OK` with the updated section.

---

## Update existing entries in a section

```http
PATCH /api/leads/{leadId}/collectionsections/{sectionId}
Content-Type: application/json

{
  "Entries": [
    {
      "EntryId": 1001,
      "Fields": [
        { "FieldId": 302, "Value": "Honda" },
        { "FieldId": 303, "Value": "Accord EX" }
      ]
    }
  ]
}
```

`CollectionSectionUpdateApi` — include `EntryId` to identify the entry. Only send fields you want to change. Returns `200 OK`.

---

## Delete entries from a section

```http
DELETE /api/leads/{leadId}/collectionsections/{sectionId}
Content-Type: application/json

{
  "EntryIds": [1001, 1002]
}
```

`CollectionSectionDeleteApi` — deletes the specified entries. Returns `200 OK`.

---

## Best Practices

- **Fetch before write**: Call `GET /api/leads/{leadId}/collectionsections` first to get current `SectionId`, field `FieldId`s, and existing `EntryId`s before modifying.
- **FieldIds are section-specific**: Section field IDs are defined in the LeadDocket admin. They vary by instance and section. Fetch them from the GET response — don't hardcode.
- **Insert vs. Update**: Use `POST` to add new rows; use `PATCH` with `EntryId` to modify existing rows. Don't use POST with data already in an EntryId — it will create a duplicate row.
- **Bulk insert**: Send multiple entries in one POST call's `Entries` array rather than one entry per request.
- **Section IDs**: `SectionId` is also instance-specific. Retrieve from the GET response to ensure you're targeting the correct section.
