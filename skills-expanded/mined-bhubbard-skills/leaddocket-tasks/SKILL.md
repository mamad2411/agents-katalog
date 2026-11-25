---
name: leaddocket-tasks
description: >
  Create, read, update, complete, and delete Tasks on leads in LeadDocket.
  Covers all task lifecycle operations including listing tasks for a lead,
  creating tasks with type (Mailing, FollowUp, Administrative) and optional
  email notification to the assigned user, and marking tasks complete. Use
  for to-do automation, workflow task creation from external triggers, and
  syncing task state. For scheduled appointments use leaddocket-lead-status.
---

# LeadDocket — Tasks

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## Get task by ID

```http
GET /api/tasks/{id}
```

Returns `TaskApi` object.

---

## Get all tasks for a lead

```http
GET /api/tasks/leads/{leadId}
```

Returns array of `TaskApi` objects.

---

## Create a task

```http
POST /api/tasks
Content-Type: application/json

{
  "LeadId": 1234,
  "Title": "Send retainer agreement",
  "Description": "Email the retainer to client for signature",
  "DueDate": "2026-07-01T17:00:00Z",
  "TaskType": "Administrative",
  "AssignedUserId": 42,
  "AssociateWithEmail": false
}
```

`TaskCreateApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `LeadId` | Yes | Lead to attach the task to |
| `Title` | Yes | Task title/name |
| `Description` | No | Longer description |
| `DueDate` | No | ISO 8601 datetime |
| `TaskType` | No | `Mailing`, `FollowUp`, or `Administrative` |
| `AssignedUserId` | No | User to assign the task to |
| `AssociateWithEmail` | No | `true` sends an email to the assigned user |

Returns `200 OK` with `TaskApi`.

---

## Update a task

```http
PUT /api/tasks
Content-Type: application/json

{
  "Id": 789,
  "Title": "Send retainer agreement (updated)",
  "DueDate": "2026-07-05T17:00:00Z",
  "AssignedUserId": 43
}
```

`TaskUpdateApi` — include `Id` plus any fields to change. Returns `200 OK` with updated `TaskApi`.

---

## Mark a task complete

```http
PUT /api/tasks/markcomplete/{id}
```

Returns `200 OK`. No body required.

---

## Delete a task

```http
DELETE /api/tasks/{id}
```

Returns `200 OK`.

---

## Best Practices

- **Task types**: Use `FollowUp` for client contact tasks, `Administrative` for internal firm tasks, `Mailing` for document send tasks — this affects filtering and reporting inside LeadDocket.
- **Email on assign**: Set `AssociateWithEmail: true` when creating tasks to notify the assigned user automatically — useful for handoff workflows.
- **Due dates in UTC**: Always send `DueDate` in UTC ISO 8601 format to avoid timezone display issues in the LeadDocket UI.
- **List then mark**: Fetch `GET /api/tasks/leads/{leadId}` to check existing tasks before creating duplicates in automated workflows.
