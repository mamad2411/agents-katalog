---
name: leaddocket-statuses
description: >
  Configure the lead pipeline in LeadDocket by creating and managing Status
  and Sub-Status definitions. Covers listing all statuses, creating new
  statuses, updating existing ones, and full CRUD on sub-statuses within a
  status. Use when setting up a new LeadDocket instance, adding pipeline stages,
  or automating status configuration from an external source. For moving a lead
  between statuses see leaddocket-lead-status.
---

# LeadDocket — Statuses & Sub-Statuses

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

**Statuses** define the stages in the lead pipeline (e.g., New Inquiry, Active Client, Settled). Each status can have ordered **Sub-Statuses** that define granular steps within the stage.

---

## List all statuses

```http
GET /api/statuses
```

Returns array of `StatusApi` with nested sub-statuses.

---

## Get a status by ID

```http
GET /api/statuses/{id}
```

Returns `StatusApiApiHypermedia` with hypermedia links.

---

## Create a new status

```http
POST /api/statuses
Content-Type: application/json

{
  "Name": "Under Review",
  "Description": "Lead is under case review",
  "SortOrder": 3,
  "IsActive": true,
  "Color": "#4A90E2"
}
```

`StatusCreateApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `Name` | Yes | Display name of the status |
| `Description` | No | Internal description |
| `SortOrder` | No | Display order in the pipeline |
| `IsActive` | No | Whether the status is available |
| `Color` | No | Hex color for UI display |

Returns `200 OK` with `StatusApiApiHypermedia`.

---

## Update a status

```http
PATCH /api/statuses/{id}
Content-Type: application/json

{
  "Name": "Under Review",
  "IsActive": false
}
```

Returns `200 OK`.

---

## Create sub-statuses on a status

```http
POST /api/statuses/{statusId}/substatus
Content-Type: application/json

{
  "SubStatuses": [
    { "Name": "Docs Requested", "SortOrder": 1 },
    { "Name": "Docs Received", "SortOrder": 2 },
    { "Name": "Review Complete", "SortOrder": 3 }
  ]
}
```

`SubStatusCreateApi` — creates multiple sub-statuses at once. Returns `200 OK` with updated status.

---

## Update a sub-status

```http
PATCH /api/statuses/{statusId}/substatus/{subStatusId}
Content-Type: application/json

{
  "Name": "Documents Requested",
  "SortOrder": 1
}
```

`SubStatusUpdateApi` — returns `200 OK` with `StatusApiApiHypermedia`.

---

## Delete a sub-status

```http
DELETE /api/statuses/{statusId}/substatus/{substatusId}
```

Returns `200 OK`.

---

## Best Practices

- **Read statuses before creating**: Fetch `GET /api/statuses` to verify a status with the same name doesn't already exist.
- **SortOrder matters**: The order determines pipeline display and the `advance` endpoint direction in `leaddocket-lead-status`. Set intentional, sequential integers.
- **Color hex**: Provide a valid 6-digit hex color for UI visibility. Skip the `#` or include it — the API normalizes.
- **Sub-status batch create**: Send all sub-statuses for a status in a single `POST /substatus` call for efficiency.
- **Deactivate rather than delete**: Deactivating a status (`IsActive: false`) preserves history. Deleting a status removes it from historical reporting.
