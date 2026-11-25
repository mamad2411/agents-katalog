---
name: resend-robot-read
version: 1.0.0
description: |
  Read dev mailbox. Lists sent emails, shows email details, searches by
  recipient or subject. Uses Resend Robot's local Resend shim.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Read Dev Email

You are running the `/resend-robot-read` workflow. Use Resend Robot to inspect emails sent in development.

## Commands

### List recent emails

```bash
bin/rails resend_robot:outbox
```

Shows a table of recent outbound emails: ID, time, recipient, subject.

### Show specific email

Read the JSON file directly for full details:

```bash
# Find the file by ID
ls tmp/resend_robot/outbound/*_rl_XXXX*.json
```

Then use the Read tool on that file to see full HTML/text body, headers, tags, reply-to address.

### Search emails

Use Grep to search `tmp/resend_robot/outbound/` for a recipient email or subject:

```bash
# Search by recipient
grep -l "alice@example.com" tmp/resend_robot/outbound/*.json

# Search by subject
grep -l "Welcome" tmp/resend_robot/outbound/*.json
```

## Storage

- Emails are stored as JSON in `tmp/resend_robot/outbound/`
- Each file has: id, from, to, cc, reply_to, subject, html, text, tags, headers
- Files are named `{timestamp}_{id}.json` — newest files sort last alphabetically
- The dev UI (default: `/dev/email`) shows the same data with HTML preview and reply form

## Rake Tasks Reference

| Task | Description |
|------|-------------|
| `resend_robot:outbox` | List recent outbound emails (table format) |
| `resend_robot:show[ID]` | Show full JSON for a specific email |
| `resend_robot:clear` | Delete all stored emails |
