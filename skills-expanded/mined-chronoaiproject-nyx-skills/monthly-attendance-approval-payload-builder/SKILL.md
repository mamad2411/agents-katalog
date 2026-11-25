---
name: monthly-attendance-approval-payload-builder
version: "1.1"
description: Builds Lark monthly attendance approval/reminder payloads and, when asked, runs the full attendance flow through a NyxID service instead of direct Lark credentials.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - attendance
    - lark-approval
    - nyxid-service-runner
    - payload-builder
  clawdbot:
    emoji: "calendar"
    files:
      - "references/*"
      - "scripts/*"
---

# Monthly Attendance Approval Payload Builder

Use this skill for monthly attendance approval and reminder flows. It supports two modes:

1. **Payload-builder mode**: build connector-ready Lark approval/reminder payloads from already fetched attendance records.
2. **NyxID service runner mode**: given a NyxID service slug, read the service-backed attendance configuration, fetch Bitable records through NyxID proxy, build the payload, submit the Lark approval or send the reminder through NyxID proxy.

Do not ask the user for raw Lark tokens, app secrets, tenant access tokens, or OAuth credentials. Use NyxID service/proxy access for all Lark I/O.

## Mode A: payload-builder

Use this mode after the caller has fetched monthly attendance records from Lark Bitable through NyxID or another trusted connector.

Required for approval mode:

- `records`
- `year`
- `month`
- `docUrl`
- `submitterId`
- `approvalCode`

Optional fields include widget ids and notification user id. Defaults are defined in `references/monthly-attendance-contract.md`.

For reminder mode, pass:

```json
{
  "mode": "reminder",
  "year": 2026,
  "month": 5,
  "notifyUserId": "user_id"
}
```

## Mode B: NyxID service runner

Use this mode when the caller provides a NyxID service slug, for example:

```json
{
  "serviceSlug": "monthly-attendance-cn",
  "mode": "approval"
}
```

The NyxID service is the configuration and credential boundary. It must hold the Lark credential and attendance configuration. The runner must call Lark only through NyxID proxy for that service.

Expected NyxID service default headers are defined in `references/nyxid-service-runner-contract.md`.

Runner behavior:

- `mode: "approval"` or omitted: read Bitable attendance records, build the approval payload, submit `POST /open-apis/approval/v4/instances`, then optionally send a DM notification if `x-attendance-notify-user-id` is configured.
- `mode: "reminder"`: build and send the reminder card to `x-attendance-notify-user-id`.
- `dryRun: true`: read/build only and do not submit approval or send messages.

Never call Lark directly. Never send or log downstream credentials. Never ask the user to paste Lark secrets.

## Output

Payload-builder mode returns JSON with:

- `stats`
- `description`
- `lark.approvalBody`
- optional `lark.notificationBody`
- optional `lark.reminderBody`

Runner mode returns JSON with:

- `serviceSlug`
- `mode`
- `dryRun`
- `submitted`
- `notified`
- `instanceCode` when approval submission returns one
- `approvalResponse` / `notificationResponse` when calls are made
- `payload`

## Determinism requirement

Follow `references/monthly-attendance-contract.md`. If executing code is allowed, use `scripts/build_monthly_attendance_payload.js` as the payload reference implementation and `scripts/run_monthly_attendance_nyxid_service.js` for the full NyxID-backed runner.

Do not invent attendance records, submitter ids, approval definitions, Lark credentials, receiver ids, or service slugs.
