---
name: inbox-triage-digest
description: Inbox triage digest — scan unread/important mail since the last run, summarise and categorise it, and email a concise digest.
---

Scan your inbox for unread and important mail since the last run, summarise and categorise each message, and email yourself a concise triage digest.

> Placeholders: `{{USER_EMAIL}}` = recipient, `{{EIDETIC_OS}}` = the Eidetic OS repo
> path. Inbox (IMAP) and SMTP credentials come from env vars
> (`IMAP_HOST` / `IMAP_USER` / `IMAP_APP_PASSWORD`, `SMTP_APP_PASSWORD` /
> `SENDER_EMAIL`) — never inline them. This runs unattended: read-only on the
> inbox, never delete, archive, or reply to mail.

**Email details:**
- Send command: `EIDETIC_TRIGGER=scheduled eidetic email --json '...'` (routes through the CLI so the run is audited)
- To: `{{USER_EMAIL}}`
- Subject: `📥 Inbox Triage — [Day] [DD] [Month] [YYYY]`

**Step 1 — Gather new mail since the last run:**

1. Read the watermark from `$STATE_DIR/inbox_triage_last_run.txt` (the UID/date
   of the last processed message). If it's missing, default to the last 24 hours.
2. Fetch candidate messages (read-only) — prefer a connected email MCP tool
   (e.g. the Gmail `search_threads` tool) with a query like
   `is:unread OR is:important newer_than:1d`; otherwise connect over IMAP using
   `IMAP_HOST` / `IMAP_USER` / `IMAP_APP_PASSWORD` and select `INBOX`.
3. For each message collect: sender, subject, date, a short snippet, and any
   unread/important/starred flags. Skip anything at or before the watermark.
4. Cap the batch (e.g. newest 50) so the digest stays concise.

**Step 2 — Build the triage digest:**

1. Categorise each message into one of: **Action Required**, **Awaiting Reply**,
   **FYI / Newsletter**, **Receipts & Admin**, **Likely Noise**.
2. Within each category, sort by importance then recency; write a one-line
   summary per message (sender — subject — what it wants / why it matters).
3. Flag time-sensitive items (deadlines, meeting requests, invoices due) at the
   top under **⚠️ Needs Attention Today**.
4. Compose an HTML email with:
   - A header banner with the date and counts (Total new | Action | Awaiting | FYI | Noise)
   - One card/section per category, each message as a row with a coloured status
     pill (red=action, amber=awaiting, blue=FYI, grey=noise)
   - A short **Summary** line at the bottom (e.g. "8 new, 2 need action today")
   - Keep summaries terse — no raw message bodies, no quoted threads

**Step 3 — Send the digest and advance the watermark:**

1. Send via SMTP:
   ```bash
   EIDETIC_TRIGGER=scheduled eidetic email --json '{"to":"{{USER_EMAIL}}","subject":"...","body_html":"..."}'
   ```
2. On success, write the newest processed message's UID/date back to
   `$STATE_DIR/inbox_triage_last_run.txt` so the next run starts where this one
   finished.
3. If no new mail since the last run, skip the email and leave the watermark
   unchanged — don't send an empty digest.

**Constraints:**
- Read-only on the inbox — never delete, archive, mark as read, move, or reply.
- Never inline credentials; read them from the env vars above.

Sign off as Eidetic.
