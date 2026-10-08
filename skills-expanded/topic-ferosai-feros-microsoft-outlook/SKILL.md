---
name: microsoft_outlook
display_name: Microsoft Outlook
description: Send emails, read the inbox, or manage calendar events in Microsoft Outlook
auth_type: oauth2
category: communication
---

# Microsoft Outlook Integration Skill

## When to use
When the user wants their voice agent to send emails or manage calendar events via Outlook.
Common triggers:
- "send a follow-up email after the call"
- "schedule a meeting in Outlook"
- "email the caller a summary"
- "check my Outlook calendar"

## What to do

1. **Check connection** via `check_connection("microsoft_outlook")`.

2. **If not connected**: Use `secret("microsoft_outlook")` in tool scripts. The system
   will automatically emit the correct action card based on the platform
   configuration. Do NOT emit action cards manually.

3. **No discovery needed**: The Graph API uses `/me` for the authenticated user's
   mailbox and calendar.

## Example tool configs

### Send an email

```json
{
  "name": "microsoft_outlook.send_email",
  "description": "Send a follow-up email to the caller via Outlook",
  "params": [
    {"name": "to_email", "description": "Recipient's email address", "type": "string", "required": true},
    {"name": "subject", "description": "Email subject", "type": "string", "required": true},
    {"name": "body", "description": "Email body text", "type": "string", "required": true}
  ],
  "script": "let key = secret('microsoft_outlook');\nlet msg = {message: {subject: subject, body: {contentType: 'Text', content: body}, toRecipients: [{emailAddress: {address: to_email}}]}};\nlet resp = http_post_h('https://graph.microsoft.com/v1.0/me/sendMail', msg, {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'});\nif (resp.status === 202 || (resp.status >= 200 && resp.status < 300)) { return 'Email sent.'; }\nthrow new Error(`Outlook ${resp.status}: ${resp.body}`);",
  "side_effect": true
}
```

### Create a calendar event

```json
{
  "name": "microsoft_outlook.create_event",
  "description": "Create a calendar event in Outlook",
  "params": [
    {"name": "subject", "description": "Event title", "type": "string", "required": true},
    {"name": "start_datetime", "description": "Start time in ISO 8601 format (e.g. '2025-06-15T10:00:00')", "type": "string", "required": true},
    {"name": "end_datetime", "description": "End time in ISO 8601 format", "type": "string", "required": true},
    {"name": "timezone", "description": "Timezone (e.g. 'America/New_York')", "type": "string", "required": false}
  ],
  "script": "let key = secret('microsoft_outlook');\nlet tz = timezone || 'UTC';\nlet body = {subject: subject, start: {dateTime: start_datetime, timeZone: tz}, end: {dateTime: end_datetime, timeZone: tz}};\nlet resp = http_post_h('https://graph.microsoft.com/v1.0/me/calendar/events', body, {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'});\nif (resp.status >= 200 && resp.status < 300) { return 'Event created.'; }\nthrow new Error(`Outlook ${resp.status}: ${resp.body}`);",
  "side_effect": true
}
```

## Rules
- NEVER hardcode OAuth tokens in tool headers
- NEVER ask for credentials in chat
- Always use `secret("microsoft_outlook")` for credentials
- All Graph API calls use base URL `https://graph.microsoft.com/v1.0`
- `sendMail` returns HTTP 202 Accepted on success (not 200)
- Datetime values must include timezone; default to `UTC` if not provided
- For script tools, treat non-2xx HTTP responses as failures and `throw` using `resp.status`/`resp.body`
