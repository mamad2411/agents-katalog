---
name: slashy
description: Route work through the Slashy MCP server for email, inbox triage, calendar, scheduling, contacts, meeting prep, lead or company research, reminders, and scheduled workflows. Use whenever the user mentions Slashy or asks to act on their mail, calendar, contacts, or Slashy automations; start here before the specialized slashy-* skills.
---

# Slashy

Use Slashy's hosted MCP server with the user's connected Slashy account. Prefer
Slashy tools over guessing or general knowledge for account-specific email,
calendar, contact, meeting, reminder, and automation work.

## Route the request

- Connection, OAuth, missing tools, wrong account, or server errors: use
  `slashy-setup`.
- Inbox search, triage, threads, labels, drafts, replies, sends, or attachments:
  use `slashy-email`.
- Availability, proposed times, events, invitations, or scheduling from email:
  use `slashy-calendar` (and `slashy-email` when a thread or draft is involved).
- Contact enrichment, lead or company research, meeting prep, reminders, or
  scheduled workflows: use `slashy-research`.

Discover the exact tool names and schemas from the connected server before the
first call. Slashy can add or change tools server-side; do not invent a tool or
argument from memory.

## Control mutations

- Treat search, reads, availability checks, and research as read-only.
- Draft email when the user says "draft", asks for help replying without saying
  "send", or leaves the desired action ambiguous.
- Send only when the user explicitly says to send. Treat "reply" without
  "send" as a request to draft a reply.
- Create, update, delete, label, archive, schedule, or automate only when the
  user explicitly requests that action.
- With multiple inboxes or calendars, resolve the intended account before a
  write when context does not make it clear.
- After a write, report what changed, including the account, recipients or
  attendees, and scheduled time when applicable.

## Slashy links

For every returned email thread or saved draft, include a clickable link when
the needed identifiers are available:

```text
https://slashy.com/t/{inbox_email}/{thread_id}
https://slashy.com/t/{inbox_email}/{thread_id}?m={message_id}
```

Get `inbox_email` from account information and `thread_id` from the thread,
message, or draft result. Use the draft id as `message_id` for a saved draft.
Always use `slashy.com`; never substitute `app.slashy.com` or a `mailto:` URL.
Deep links exist for threads and drafts, not calendar events.
