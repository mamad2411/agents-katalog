---
name: gmail-unread-autodraft
emoji: ✉️
description: gmail-unread-autodraft lets the user scan their Gmail inbox for unread messages and automatically create draft replies on each thread on a schedule, which is useful when they want to acknowledge emails, stay top-of-mind with contacts, or maintain an inbox-zero workflow without manually typing responses to every message.
version: 1.0.0
maintainer: James (OpenClaw agent)
requires:
  bins:
    - gog
prerequisites:
  - Google OAuth set up for gog (credentials + token stored)
  - Environment variable GOG_KEYRING_PASSWORD is available to unlock gog token store
  - A target Gmail account is set via GOG_ACCOUNT or passed with --account
---

# Gmail Unread Auto‑Draft (Skill)

This skill schedules and runs a daily sweep of a Gmail inbox to:
- Find unread messages (in:inbox label:unread)
- Create a draft reply on each thread (do NOT send)
- Emit a concise run report back to the initiating chat/session

It is designed to be safe-by-default (no sending, idempotent drafts, capped batch size) and easy to adapt (template body, schedule, labels).

## What This Skill Does

This skill gmail-unread-autodraft lets the user scan their Gmail inbox for unread messages and automatically create draft replies on each thread on a schedule, which is useful when they want to acknowledge emails, stay top-of-mind with contacts, or maintain an inbox-zero workflow without manually typing responses to every message.

## When to use
- You want automatic acknowledgement drafts queued for review each morning
- You need a lightweight triage layer before manual responses
- You want consistent reply copy with a custom signature

## Inputs
- schedule.tz: IANA timezone (default: America/New_York)
- schedule.cron: Cron expression (default: 0 4 * * *)
- gmail.account: Gmail address to operate on (e.g., JamesClawBot@gmail.com)
- env.keyringPassword: Value for GOG_KEYRING_PASSWORD
- search.query: Gmail query for selection (default: in:inbox label:unread)
- search.max: Max messages per run (default: 50)
- reply.subjectPrefix: Usually "Re: "
- reply.bodyTemplate: Plain-text body appended to every draft

Example default body template:

Hi there,

Acknowledging receipt of your message. Please confirm details for my records (where applicable):
- Timestamp (UTC)
- Source IP and approximate geolocation
- Device / user agent

Status: This was me / This was NOT me (please keep one and act accordingly)
- If NOT me: Please revoke active sessions and require password reset + 2FA.

To Your Extraordinary Success,
Charles Blair - The Mad Scientist

## Outputs (per run)
- Summary posted to the chat/session:
  - Time window (e.g., Today 4:00 AM ET)
  - Unread found (N)
  - Drafts created (M)
  - Skipped (already drafted) (K)
  - Errors (E)
  - Up to 10 sample thread links (https://mail.google.com/mail/u/0/#inbox/<threadId>)

## Rules & Constraints
- Never send email from this skill; drafts only
- Idempotent: if a draft already exists on a thread, skip
- Fail fast on CLI errors (--no-input) and include brief error summary
- Respect per-run cap (default 50) to avoid runaway processing
- Prefer plain-text bodies; use --body-file for multi-line content

## Step-by-step (what the skill does)
1) Ensure environment for gog:
   - export GOG_KEYRING_PASSWORD=<password>
   - export GOG_ACCOUNT=<gmail-address>
2) Query unread messages:
   - gog gmail messages search "in:inbox label:unread" --max <N> --json --no-input --results-only --select id,threadId
3) For each result messageId/threadId:
   - Fetch thread: gog gmail thread get <threadId> --json --no-input --results-only
   - Parse Subject header from the first message (fallback: "(no subject)")
   - Create a reply draft on messageId:
     gog gmail drafts create \
       --subject "Re: <Subject>" \
       --reply-to-message-id <messageId> \
       --body-file - \
       --json --no-input --results-only <<'EOF'
<Body template>
EOF
   - Optional: apply a label (e.g., "auto-drafted") to the thread to exclude on subsequent runs
4) Count created, skipped, errors; print a concise report

## OpenClaw Cron: install this skill (template)
Use an isolated cron job that performs the steps above. Replace placeholders in braces.

openclaw cron add --json <<'JSON'
{
  "name": "Gmail unread auto-draft ({gmail.account})",
  "schedule": {
    "kind": "cron",
    "expr": "{schedule.cron}",
    "tz": "{schedule.tz}"
  },
  "sessionTarget": "isolated",
  "enabled": true,
  "payload": {
    "kind": "agentTurn",
    "timeoutSeconds": 180,
    "message": "Task: Daily Gmail sweep to draft replies (do NOT send), then post a concise report.\n\nEnvironment:\n- Set env for gog: GOG_KEYRING_PASSWORD={env.keyringPassword}, GOG_ACCOUNT={gmail.account}\n\nLogic:\n1) Search: gog gmail messages search '{search.query}' --max {search.max} --json --no-input --results-only --select id,threadId\n2) For each message id, get thread, extract Subject, and create a draft via stdin with body template below.\n\nBody template:\n{reply.bodyTemplate}\n\nCommand pattern:\n gog gmail drafts create --subject 'Re: <Subject>' --reply-to-message-id <messageId> --body-file - --json --no-input --results-only <<'EOF'\n{reply.bodyTemplate}\nEOF\n\n3) Track counts and sample thread links.\n4) Output report:\n- Time window: Today {schedule.tz} {schedule.cron}\n- Unread found: <N>, Drafts created: <M>, Skipped: <K>, Errors: <E>\n- Samples: <links>\n\nNotes:\n- Do NOT send any email.\n- Idempotent: skip if a draft already exists.\n- Include brief error summary if any." 
  }
}
JSON

Tip: You can also configure this via the OpenClaw cron tool UI or API; ensure the sessionTarget is "isolated" for best reliability.

## Testing the skill
- One-time manual dry-run:
  - export GOG_KEYRING_PASSWORD=...; export GOG_ACCOUNT=...
  - gog gmail messages search "in:inbox label:unread" --max 5 --json --no-input --results-only --select id,threadId
  - Pick one id; create a draft using the body template above
- Trigger the cron immediately to validate end-to-end:
  - openclaw cron run <jobId>
  - If a gateway timeout occurs, the job is still installed; it will run on schedule

## Customization
- Change search.query to exclude previously processed threads, e.g.: in:inbox label:unread -label:auto-drafted
- Add a label after drafting via gog gmail thread modify
- Swap in a different signature or a full contact block
- Adjust schedule.cron and timezone

## Troubleshooting
- Missing --account or auth prompt: set GOG_ACCOUNT and GOG_KEYRING_PASSWORD; verify `gog auth list`
- Keyring prompt in non-TTY: export GOG_KEYRING_PASSWORD before running
- CLI changes: consult `gog ... --help` for your installed version
- Cron delivery errors: re-run the job or check gateway connectivity; the job remains saved unless explicitly removed
