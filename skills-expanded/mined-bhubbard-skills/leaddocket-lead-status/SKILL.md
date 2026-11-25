---
name: leaddocket-lead-status
description: >
  Manages lead pipeline progression in LeadDocket: changing a lead's status,
  advancing through sub-statuses, and scheduling appointments. Use when the
  user needs to move a lead through the intake workflow, set a status from an
  external system, or automate sub-status advancement. For reading lead data
  use leaddocket-leads; for configuring status definitions use
  leaddocket-statuses.
---

# LeadDocket — Lead Status & Workflow

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## Change lead status

```http
PATCH /api/leads/{id}/status/change
Content-Type: application/json

{
  "StatusId": 3,
  "SubStatusId": 12,
  "Note": "Signed retainer — moving to Active Client"
}
```

`ChangeLeadStatusApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `StatusId` | Yes | Target status ID (from `/api/lookups?type=Statuses`) |
| `SubStatusId` | No | Target sub-status ID |
| `Note` | No | Note text added to the lead on status change |

Returns `200 OK` on success.

> Use `/api/lookups?type=Statuses` or `leaddocket-lookups` to discover valid status IDs before calling this endpoint.

---

## Advance to next sub-status

Moves the lead to the **next sub-status** in the configured sequence without needing to know the target ID. Accepts the current status and sub-status as guards to prevent race conditions.

```http
PATCH /api/leads/{id}/substatus/advance?currentStatusId={sid}&currentSubstatusId={ssid}
```

| Param | Required | Description |
|-------|----------|-------------|
| `currentStatusId` | No | Guard — prevents advancing if lead has already moved |
| `currentSubstatusId` | No | Guard — prevents advancing if sub-status has already changed |

Returns `200 OK`. If no next sub-status exists, the lead stays at its current sub-status (no error).

**Pattern**: Poll `GET /api/leads/basic/{id}`, check `SubStatusId`, then call advance if still at the expected position.

---

## Schedule an appointment

```http
PATCH /api/leads/{id}/appointments/schedule
Content-Type: application/json

{
  "AppointmentDate": "2026-07-15T14:00:00Z",
  "AppointmentTypeId": 2,
  "AssignedUserId": 7,
  "Note": "Consultation call"
}
```

`ScheduleAppointmentApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `AppointmentDate` | Yes | ISO 8601 datetime (UTC recommended) |
| `AppointmentTypeId` | No | Appointment type from lookup |
| `AssignedUserId` | No | User responsible for the appointment |
| `Note` | No | Note attached to the appointment |

Returns `200 OK` on success.

---

## Best Practices

- **Always validate status IDs** before calling change — invalid IDs return an error. Fetch valid IDs via `GET /api/lookups?type=Statuses`.
- **Use guards on advance** (`currentStatusId` + `currentSubstatusId`) when multiple systems may write concurrently to avoid skipping sub-statuses.
- **Include a note** on status changes for auditability — it becomes part of the lead's activity log.
- **Appointments vs. tasks**: Appointments are structured scheduling events; for general to-dos use `leaddocket-tasks` instead.
