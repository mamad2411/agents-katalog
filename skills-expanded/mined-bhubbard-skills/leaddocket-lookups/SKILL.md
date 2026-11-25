---
name: leaddocket-lookups
description: >
  Fetch reference and lookup data from LeadDocket — case types, tags, expense
  types, appointment types, and other configurable list values. Covers
  discovering what lookup types are available and fetching the items for a
  given type. Use as a prerequisite to other skills that require type IDs or
  tag IDs as parameters.
---

# LeadDocket — Lookups

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

The Lookups API provides access to administrator-configured reference lists — case types, tags, lead sources, expense types, and more. These are the values that appear in dropdowns in the LeadDocket UI.

---

## Get all available lookup type names

```http
GET /api/lookups/gettypes
```

Returns array of strings — the type names you can query:

```json
[
  "CaseTypes",
  "Tags",
  "ExpenseTypes",
  "AppointmentTypes",
  "Statuses",
  "LeadSources",
  "Relationships",
  "Languages",
  "HearAboutUs"
]
```

Run this first to discover what lookup types are available on this instance.

---

## Get items for a lookup type

```http
GET /api/lookups?type={typeName}
```

Returns array of `LookupItemApi`:

```json
[
  { "Id": 1, "Name": "Motor Vehicle Accident" },
  { "Id": 2, "Name": "Premises Liability" },
  { "Id": 3, "Name": "Medical Malpractice" }
]
```

### Common type queries

```http
# Case types (use Id as CaseTypeId on a lead)
GET /api/lookups?type=CaseTypes

# Contact/lead tags (use Id in PUT /api/contacts/{id}/tags/{tagId})
GET /api/lookups?type=Tags

# Expense types (use Id as ExpenseTypeId when adding expenses)
GET /api/lookups?type=ExpenseTypes

# Appointment types (use Id when scheduling appointments)
GET /api/lookups?type=AppointmentTypes
```

---

## Best Practices

- **Cache lookup results**: These values only change when an admin modifies configurations. Cache per session or for several hours.
- **Always query by type name, not ID**: Lookup IDs are instance-specific. Never hardcode them across different LeadDocket instances.
- **Use `gettypes` to discover**: Instances may have custom lookup types. Always discover what's available rather than assuming a fixed list.
- **Prerequisite for other operations**: Lookups are prerequisites for: `CaseTypeId` (lead update), `TagId` (contact tags), `ExpenseTypeId` (expenses), `AppointmentTypeId` (scheduling).
