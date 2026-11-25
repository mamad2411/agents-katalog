---
name: leaddocket-lead-forms
description: >
  Build, manage, and send client-facing intake Lead Forms in LeadDocket.
  Covers full CRUD on LeadForm definitions (create, read, update, delete),
  field management (add, update, delete individual fields), and sending form
  invitations to specific leads. Use for automating client intake questionnaires,
  building custom data-collection forms, and sending invitation links to leads.
---

# LeadDocket — Lead Forms

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

A **LeadForm** is a client-facing intake form. Once defined, the form can be
sent to a lead as an invitation — the client completes it and the data populates
back into the lead's custom fields.

---

## List all LeadForms

```http
GET /api/leads/forms
```

Returns array of `LeadFormApi`.

---

## Get a LeadForm by ID

```http
GET /api/leads/forms/{id}
```

Returns `LeadFormApi` with full field definitions.

---

## Create a new LeadForm

```http
POST /api/leads/forms
Content-Type: application/json

{
  "Name": "Personal Injury Intake",
  "Description": "Initial intake questionnaire for PI cases",
  "IsActive": true
}
```

Returns `200 OK` with `LeadFormApi`.

---

## Update a LeadForm

```http
PATCH /api/leads/forms/{id}
Content-Type: application/json

{
  "Name": "Personal Injury Intake (Updated)",
  "IsActive": true
}
```

Returns `200 OK`.

---

## Delete a LeadForm

```http
DELETE /api/leads/forms/{id}
```

Returns `200 OK`.

---

## Add a field to a LeadForm

```http
POST /api/leads/forms/{id}/field
Content-Type: application/json

{
  "CustomFieldId": 101,
  "Label": "Date of Accident",
  "IsRequired": true,
  "SortOrder": 1
}
```

`LeadFormFieldAddApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `CustomFieldId` | Yes | ID from `GET /api/customfields/list` |
| `Label` | No | Override the field name shown to client |
| `IsRequired` | No | Whether the field is required |
| `SortOrder` | No | Display order on the form |

Returns `200 OK`.

---

## Update a field on a LeadForm

```http
PATCH /api/leads/forms/{id}/field/{fieldId}
Content-Type: application/json

{
  "Label": "Accident Date",
  "IsRequired": true,
  "SortOrder": 2
}
```

Returns `200 OK`.

---

## Delete a field from a LeadForm

```http
DELETE /api/leads/forms/{id}/field/{fieldId}
```

Returns `200 OK`.

---

## Delete all fields of a type from a LeadForm

```http
DELETE /api/leads/forms/{id}/fields?fieldType={type}
```

Removes all fields matching the given type in one operation.

---

## Get a LeadForm invitation for a lead

```http
GET /api/leads/{leadId}/forms
```

Returns `LeadFormInvitationApi` — the current invitation state (sent, completed, link, etc.).

---

## Create/send a LeadForm invitation to a lead

```http
POST /api/leads/{leadId}/forms
Content-Type: application/json

{
  "LeadFormId": 5,
  "SendEmail": true,
  "EmailMessage": "Please complete this intake form at your earliest convenience."
}
```

`LeadFormInvitationCreateApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `LeadFormId` | Yes | Which form to send |
| `SendEmail` | No | `true` sends an invitation email to the lead's primary contact |
| `EmailMessage` | No | Custom message to include in the invitation email |

Returns `200 OK` with `LeadFormInvitationApi`.

---

## Best Practices

- **Form fields must map to custom fields**: Each form field is tied to a `CustomFieldId`. Ensure the custom field exists (`GET /api/customfields/list`) before adding to a form.
- **One active invitation per lead**: Sending a new invitation replaces the previous one for that lead.
- **SortOrder**: Set sequential integers for display order. Fields without a sort order display in creation order.
- **Activate forms before inviting**: Ensure `IsActive: true` on the form before sending invitations, or the link may not work.
