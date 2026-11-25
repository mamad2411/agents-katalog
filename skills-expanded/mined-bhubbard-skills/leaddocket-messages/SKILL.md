---
name: leaddocket-messages
description: >
  Send and log communications on leads in LeadDocket: outbound email via the
  API, outbound SMS text messages, and creating internal message log entries
  on a lead. Use when automating client communications, logging inbound
  messages from external systems, or sending texts from integrations. For
  configuring email sender domains and auto-reply rules see
  leaddocket-email-config.
---

# LeadDocket — Messages (Email & SMS)

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

> ⚠️ SMS messages sent beyond the plan limit incur overage charges.

---

## Log a message on a lead

Creates an internal message record (does not send externally).

```http
POST /api/messages
Content-Type: application/json

{
  "LeadId": 1234,
  "Subject": "Follow-up from consultation",
  "Body": "Thank you for speaking with us today...",
  "Direction": "Inbound",
  "MessageType": "Email"
}
```

`MessageAddApi` key fields:

| Field | Required | Description |
|-------|----------|-------------|
| `LeadId` | Yes | Lead to associate the message with |
| `Subject` | No | Message subject line |
| `Body` | Yes | Message body (HTML or plain text) |
| `Direction` | No | `Inbound` or `Outbound` |
| `MessageType` | No | `Email`, `Text`, etc. |

Returns `201 Created` with the new `MessageApi` object.

---

## Send an email

Sends an actual email and logs it on the lead.

```http
POST /api/messages/sendemail
Content-Type: application/json

{
  "LeadId": 1234,
  "SendTo": "client@example.com",
  "SendFrom": "attorney@lawfirm.com",
  "SendFromName": "Jane Attorney",
  "Subject": "Your case intake is complete",
  "Body": "<p>Dear Client,</p><p>We have received your intake...</p>",
  "Attachments": [
    {
      "Filename": "intake-summary.pdf",
      "Base64Data": "JVBERi0x..."
    }
  ]
}
```

`SendEmailMessageApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `LeadId` | Yes | Lead to log message on |
| `SendTo` | Yes | Must be email of a lead contact |
| `SendFrom` | Yes | Must be email of a lead role user assigned to this lead |
| `SendFromName` | No | Display name for sender |
| `Subject` | Yes | Email subject |
| `Body` | Yes | HTML or plain text body |
| `Attachments` | No | Array of `{Filename, Base64Data}` objects |

Returns `201 Created`.

---

## Send an SMS text

```http
POST /api/messages/sendtext
Content-Type: application/json

{
  "LeadId": 1234,
  "Body": "Hi Jane, just a reminder about your consultation tomorrow at 2pm.",
  "SendFrom": "+15551234567"
}
```

`SendTextMessageApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `LeadId` | Yes | Lead to send text to |
| `Body` | Yes | Text message content |
| `SendFrom` | No | SMS number to send from. Defaults to the lead's default SMS number if omitted. |

Returns `201 Created`.

---

## Best Practices

- **`SendTo` must be a contact on the lead** — the API validates the email belongs to a contact associated with that lead.
- **`SendFrom` must be an assigned lead role user** — the sender must already be assigned to the lead in a role.
- **Attachments**: Base64-encode the file content. Keep individual files reasonable in size; large payloads may time out.
- **SMS overages**: Check the account plan before sending bulk texts. The API does not block over-limit sends, it just charges overage.
- **Log inbound messages**: Use `POST /api/messages` with `Direction: Inbound` to log messages received outside of LeadDocket (e.g., from a third-party chat tool).
