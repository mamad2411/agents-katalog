---
name: email-inbox-zero
description: Triage email into reply, action, defer, archive, or escalate queues without silent sending.
category: productivity
aliases:
- email
- inbox
- gmail
- mail
triggers:
- Triage my emails
- Process my inbox
- Clean up my email
- Inbox zero
keywords:
- email
- inbox
- triage
- archive
- reply
- action
- organize
dependencies:
- optional:email-access
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- email-inbox-zero
- productivity
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- archive
- email
- inbox
- productivity
- triage
- zero
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Email Inbox Zero

## Purpose
Help users achieve and maintain inbox zero by intelligently triaging emails into
appropriate queues: reply, action, defer, archive, or escalate. The skill never sends
emails without explicit user approval.

## When to Use
- The user wants help processing their inbox
- Batch email organization is needed
- Identifying action items from email is required
- Finding important emails in a cluttered inbox

## When NOT to Use
- The user wants automated replies (require explicit review)
- Processing emails from accounts without proper access
- Handling emails with legal or compliance implications

## Capabilities
- List emails with sorting (date, sender, subject)
- Summarize email content
- Triage into categories: reply, action, defer, archive, escalate
- Draft replies (user must approve before sending)
- Bulk archive low-priority emails
- Identify urgent emails requiring immediate attention
- Track action items from emails

## Inputs
- `action` (required) — one of: list, summarize, triage, draft-reply, archive
- `filter` (optional) — sender, date range, subject keyword
- `limit` (optional) — number of emails to process

## Workflow
1. **List** — Fetch emails matching filter criteria
2. **Analyze** — Summarize each email's content and importance
3. **Triage** — Categorize into queues with reasoning
4. **Present** — Show categorized emails to user
5. **Execute** — Perform actions only with user approval

## Tools
- Email API (Gmail, IMAP, or similar)
- Read-only access by default

## Examples
**User:** "Triage my unread emails"
**Response:**
```
Inbox triage (15 unread emails):

ACTION NEEDED (3):
- [1] Project deadline tomorrow - reply by EOD
- [2] Invoice #1234 - approval required  
- [3] Meeting request - decision needed

DEFER (5):
- Newsletter updates
- System notifications
- ...

ARCHIVE (7):
- Receipts, confirmations, etc.
```

## Safety
- NEVER send emails without explicit user confirmation
- Never delete emails (archive only)
- Respect access permissions and scopes
- Never share email content outside authorized context
- Warn before bulk operations

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical productivity category.
