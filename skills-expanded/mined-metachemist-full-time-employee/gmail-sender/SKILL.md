---
name: gmail-sender
description: |
  Send approved emails via Gmail API. Use after a human has approved an
  APPROVAL_SEND_EMAIL_*.md file by moving it to vault/Approved/. Reads the
  payload, sends the email, logs the result, and moves the approval file to
  vault/Done/. Never send without an approved file present.
---

# Gmail Sender

Execute email sends after human approval using the Gmail API.

## When to Use

Only call this skill when:
1. A file starting with `APPROVAL_SEND_EMAIL_` exists in `vault/Approved/`
2. Its `status` frontmatter field is `pending`

Never send without an approved file. Never send to new contacts without checking
`Company_Handbook.md` first.

## Prerequisites

| Item | Location |
|------|----------|
| OAuth token | `watchers/.state/gmail_token.json` |
| Credentials | `watchers/.secrets/gmail_credentials.json` |
| Python deps | `pip install google-auth google-auth-oauthlib google-api-python-client` |

If `gmail_token.json` is missing or expired, run the Gmail watcher once to re-authorise:
```bash
cd watchers && python gmail_watcher.py ../vault --auth-only
```

## Workflow

### 1. Read the Approved File

```bash
# Find approved email actions
ls vault/Approved/APPROVAL_SEND_EMAIL_*.md
```

Parse the file:
```yaml
---
type: approval_request
action: send_email
source_plan: Plans/PLAN_GMAIL_...md
created: ...
status: pending          # must be "pending" — if "sent" skip it
---

# Payload
- **Action:** `send_email`
- **Target:** Jane Doe <jane@example.com>
- **Subject / Title:** Re: Pricing inquiry

## Message / Content
  Dear Jane,
  ... (the email body to send)
```

Extract:
- **To**: from `Target:` line — `Jane Doe <jane@example.com>`
- **Subject**: from `Subject / Title:` line
- **Body**: everything under `## Message / Content`, strip the 2-space indent

### 2. Send the Email

```bash
python .claude/skills/gmail-sender/scripts/send_email.py \
  --to "Jane Doe <jane@example.com>" \
  --subject "Re: Pricing inquiry" \
  --body-file /tmp/email_body.txt \
  --token watchers/.state/gmail_token.json \
  --credentials watchers/.secrets/gmail_credentials.json
```

Or pass body inline for short messages:
```bash
python .claude/skills/gmail-sender/scripts/send_email.py \
  --to "Jane Doe <jane@example.com>" \
  --subject "Re: Pricing" \
  --body "Dear Jane, Thank you for..."
```

Expected output (JSON):
```json
{"status": "sent", "message_id": "18e4bc...", "to": "jane@example.com", "timestamp": "2026-02-22T..."}
```

On error:
```json
{"status": "error", "error": "Invalid credentials", "timestamp": "..."}
```

### 3. Update the Vault

After a successful send:

1. **Update the approval file** — set `status: sent` and add `sent_at: <ISO timestamp>`
2. **Move approval file** → `vault/Done/<filename>`
3. **Update source plan** → set `status: done` (find via `source_plan` frontmatter field)
4. **Write audit log** entry to `vault/Logs/YYYY-MM-DD.jsonl`:
```json
{"timestamp": "...", "event": "email_sent", "to": "jane@example.com", "subject": "Re: Pricing", "message_id": "18e4bc...", "result": "success"}
```
5. **Update Dashboard.md** counts

### 4. Error Handling

| Error | Action |
|-------|--------|
| `Invalid credentials` | Run auth flow, alert user, do not send |
| `Quota exceeded` | Wait 60 s, retry once, then alert |
| `Invalid recipient` | Write `status: failed` to approval file, move to `vault/Done/` |
| `Network error` | Retry up to 3×, exponential backoff |

Never leave a failed send in `vault/Approved/` — always move it to `vault/Done/` with `status: failed` and the error message noted.

## Dry-Run Mode

Test without sending a real email:
```bash
python .claude/skills/gmail-sender/scripts/send_email.py \
  --to "test@example.com" --subject "Test" --body "Hello" --dry-run
```

Output: `{"status": "dry_run", "would_send_to": "test@example.com", ...}`

## Quick Reference

```bash
# Check for approved emails
ls vault/Approved/APPROVAL_SEND_EMAIL_*.md

# Send and update vault
python .claude/skills/gmail-sender/scripts/send_email.py \
  --to "<recipient>" --subject "<subject>" --body "<body>"

# Verify sent (check Gmail Sent folder)
python .claude/skills/gmail-sender/scripts/send_email.py --list-sent --limit 5
```

## Rules (non-negotiable)

- **Never** send without a file in `vault/Approved/`
- **Never** send to a contact not in the approved file's Target field
- **Always** log every send attempt (success or failure) to `vault/Logs/`
- **Always** move the approval file to `vault/Done/` after execution
- **Rate limit**: max 20 emails per hour; pause and alert if limit reached
