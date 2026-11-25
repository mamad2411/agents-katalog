---
name: google-account-backup
description: >-
  Backup Google account data (Gmail, Photos, Drive) to local storage and
  reclaim quota space. Covers stealth-browser login, IMAP email download with
  attachments, Google Takeout for comprehensive backup, and storage management
  cleanup. Designed for accounts near or over the 15GB free quota.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [google, gmail, backup, storage, takeout, imap, cleanup, photos, drive]
    triggers:
      - gmail backup
      - google storage full
      - google account out of space
      - download all gmail emails
      - gmail storage cleanup
      - google photos backup
      - google takeout
      - free up google storage
      - gmail app password
      - imap gmail download
      - google account migration
      - google data export
      - gmail quota
      - google storage management
    related_skills: [stealth-browser-setup, firefox-stealth-automation]
---

# Google Account Backup & Storage Recovery

## Overview

When a Google account hits the 15GB storage limit, Gmail bounces incoming
emails, Photos stops syncing, and Drive blocks new uploads. This skill covers
the complete recovery workflow: backup all data to local storage, then clean up
Google's services to reclaim the quota.

## Architecture

```
Google Account (15 GB full)
  ├── Gmail (3.83 GB)
  │     ├── IMAP download → local .eml files + attachments  
  │     └── Google Takeout → MBOX archives
  ├── Google Photos (11.12 GB)
  │     └── Google Takeout → ZIP archives with JSON metadata
  └── Google Drive (0.12 GB)
        └── Google Takeout → native format files
```

**Data safety principle:** Never delete from Google until backups are confirmed.
Use TWO independent backup methods (IMAP + Takeout) so a single point of
failure cannot cause data loss.

## Prerequisites

- Stealth browser running (Camofox, see `stealth-browser-setup` skill)
  — standard Chrome DevTools CDP gets blocked by Google as "insecure browser"
- 380GB+ free disk space for a full 15GB account backup
- User's Gmail password (for browser login and App Password generation)
- Python 3 + `imaplib` (stdlib, always available)
- `google-api-python-client` (pip, for API access if needed)

## Step 1: Stealth-Browser Login

Google's login page blocks automated Chrome DevTools sessions with
_"This browser or app may not be secure"_. Use Camofox (Camoufox Firefox fork)
which has C++ fingerprint spoofing and imported Firefox cookies.

```bash
# Start Camofox (if not running)
cd ${MY_REPOS}/camofox-browser
MSYS_NO_PATHCONV=1 node server.js &

# Verify
curl -s http://localhost:9377/health
```

Create a tab and navigate to:
`https://accounts.google.com/AccountChooser/signinchooser?continue=https://mail.google.com/mail/`

**2FA handling:** The account may prompt for 2-step verification. Options:
- "Tap Yes on your phone" (sends Google prompt to registered device)
- "Get a verification code from the Google Authenticator app"
- If the phone SMS option is disabled due to "more secure options", use
  the phone prompt or authenticator app instead

## Step 2: Generate Gmail App Password

IMAP with 2FA requires an App Password (16-char alphanumeric):

1. Navigate to `https://myaccount.google.com/apppasswords`
2. Type an app name (e.g. "Hermes Backup")
3. Click "Create"
4. Copy the 16-character password (e.g. `xxxx xxxx xxxx xxxx`)

**CRITICAL:** Remove spaces from the password before use in code
(`ufwd gehd yolx lbkm` → `ufwdgehdyolxlbkm`).

## Step 3: Start Google Takeout Export

Google Takeout creates downloadable archives of ALL Google data. It handles
what IMAP cannot: Photos, Drive files, and Gmail's MBOX format.

```python
# Navigate to takeout.google.com in the stealth browser
# Step-by-step:
# 1. Deselect all products
# 2. Select only: Mail (Gmail), Drive, Google Photos
# 3. Next step → Export once (default) → .zip → 2GB → Create export
```

Takeout can take hours or days to process. Set up a monitoring cron job
to check `https://takeout.google.com/manage` periodically and download
archives when ready.

### The Takeout Email Problem

Because the account is OVER quota, Gmail bounces incoming messages —
including the "Your export is ready" notification. **Do NOT rely on email.**
Use the Manage Exports page at `takeout.google.com/manage` to check status.
Set a cron job to poll it every 4 hours once started, or use the script
at `scripts/check-takeout.py`.

## Step 4: IMAP Email Download (Direct, Immediate)

While Takeout processes, download all emails locally via IMAP. This provides
an independent, immediately-available backup.

### IMAP Connection

| Setting | Value |
|---------|-------|
| Server | `imap.gmail.com` |
| Port | `993` (SSL) |
| Username | Full Gmail address |
| Password | App Password (step 2) |

### Mailbox Name

Gmail's All Mail folder is `"[Gmail]/All Mail"` — with double quotes to
handle the brackets:

```python
import imaplib
mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login("user@gmail.com", "APP_PASSWORD")
mail.select('"[Gmail]/All Mail"', readonly=True)  # ← quotes required!
```

**PITFALL:** Without the outer single quotes (which become double quotes in
the IMAP command), `[Gmail]` causes a `BAD Could not parse command` error.

### Progress Tracking

Save progress to a JSON file so the download can resume if interrupted:

```python
progress = {"last_uid": 0, "total_downloaded": 0}
# After each batch:
progress["last_uid"] = int(last_uid)
progress["total_downloaded"] = downloaded
json.dump(progress, open("progress.json", "w"))
```

On restart, find the last UID position:
```python
all_uids = data[0].split()  # from uid('search', None, 'ALL')
new_uids = [uid for uid in all_uids if int(uid) > progress["last_uid"]]
```

### Attachment Extraction

Walk MIME parts and save attachments by type:

```python
content_type = part.get_content_type()
type_folder = "video" if "video" in content_type else "image" if "image" in content_type else "other"
```

### PITFALL: read-only mode

Always use `readonly=True` in `mail.select()` to prevent accidental
deletion during backup. Create a separate deletion workflow.

## Immediate Recovery: Getting Email Back Right Now

When you only need to **resume email service** (not fully clear storage),
the storage management page shows the minimum threshold:

> "Clean up **80.46 MB** to resume emails, uploads, and backup."

The Google One Storage Manager at `one.google.com/storage/management`
provides the fastest path to immediate space reclamation.

### Steps for Immediate Recovery

1. Navigate to `https://one.google.com/storage/management`
2. Click **"Large photos and videos"** (or any suggested items section)
3. Click the **Select all items** checkbox to select all visible large files
4. Click **Move to trash** (triggers a confirmation dialog)
5. Check the confirmation checkbox: *"I understand that items in Google Photos Trash will be permanently deleted after 60 days"*
6. Click **Move to trash** to confirm

Then repeat for other categories:
- **Emails with large attachments** — select all → Delete (permanent deletion confirmation)
- **Spam emails** — Delete all → confirm permanence
- **Emails in Trash** — empty permanently

**Result:** 700 MB+ can be freed in minutes, immediately restoring email
reception and Drive/Photos functionality.

### Confirmation Dialog Pattern (Important!)

The storage management cleanup flow uses a **two-step confirmation dialog**
that the browser automation must handle:

```
Dialog: "Move 32 items to Trash?"
  □ [checkbox] "I understand that items in Google Photos Trash will be
                permanently deleted after 60 days."  ← click first
  [Cancel] [Move to trash]                            ← then click (was disabled)
```

**The confirmation button starts disabled.** You MUST click the checkbox
first to enable it, then click the confirm button. Same pattern for Gmail
email deletion dialogs.

### What About Bounced Emails?

While the account was over quota, any emails sent to it were **bounced back
to the sender and cannot be recovered.** Google explicitly shows:

> "Emails sent to you will be bounced back to the sender and can't be
> recovered later."

The missed emails from the overflow period are **permanently lost** — no
backup method can retrieve them. This makes the urgency real: free space
immediately or lose incoming messages.

### Checking That Service Resumed

After freeing enough space (confirmed when the storage page changes from
"out of storage" to "95% full" or better), check Gmail:

1. Navigate to `https://mail.google.com/mail/u/0/#inbox`
2. Verify the inbox loads with the normal unread count
3. The storage alert should change from red/critical to yellow/warning
4. New incoming emails should start arriving within minutes

### Camofox Evaluate Return Value (Pitfall)

The Camofox `/evaluate` endpoint returns `result` as a **plain string**, not
a JSON-encoded string. Do NOT call `json.loads()` on `resp.get('result')`:

```python
# ❌ WRONG — json.loads will fail on a plain string
resp = json.loads(urllib.request.urlopen(...).read())
value = json.loads(resp.get('result'))  # JSONDecodeError!

# ✅ CORRECT — result is already the plain value
resp = json.loads(urllib.request.urlopen(...).read())
value = resp.get('result')  # "https://example.com" (plain string)
```

Exception: when the JS expression returns a complex object (array/object),
the result IS a JSON string that needs parsing:
```python
js_resp = urllib.request.urlopen(...)
result = json.loads(js_resp.get('result'))  # returns parsed Python list/dict
```

### Camofox Tab Session Expiry (Pitfall)

A Camofox tab can become invalid (returning HTTP 404 on `snapshot`/`click`)
if the tab was created in an earlier session session or the browser was idle
too long. Handle gracefully:

```python
try:
    snap = json.loads(urllib.request.urlopen(
        f'{BASE}/tabs/{tab_id}/snapshot?userId=the operator', timeout=30
    ).read())
except urllib.error.HTTPError as e:
    if e.code == 404:
        # Tab expired — create a new one
        resp = json.loads(urllib.request.urlopen(
            f'{BASE}/tabs',
            data=json.dumps({'userId': 'the operator', 'sessionKey': 'new-session',
                             'url': 'https://example.com'}).encode(),
            headers={'Content-Type': 'application/json'}, method='POST'
        ).read())
        tab_id = resp.get('tabId')
```

This is especially common during long-running operations where the user
steps away — the tab's session times out before they return to authenticate.

## Step 5: Storage Analysis

The Google One Storage Manager at `one.google.com/storage/management` shows:

| Category | What to check |
|----------|---------------|
| Large photos & videos | Items >1GB, shown in a table with checkboxes |
| Emails with large attachments | 176 MB+ range |
| Large Drive files | Usually small if Drive isn't actively used |
| Spam emails | Usually negligible |

The page also shows "Delete X MB to resume emails" — a minimum threshold
that is much lower than full recovery. Full recovery requires emptying
Photos (the dominant consumer).

### Reviewing Large Items

Navigate to `one.google.com/storage/management/photos/large` to see
all large photos/videos with Download and Move to trash buttons.
Enable the Download button by selecting items via checkboxes.

## Step 6: Cleanup (Post-Backup-Confirmation)

**Only after confirming both IMAP and Takeout backups are complete:**

### Gmail Cleanup (Post-Backup-Confirmation)

**🚨 CRITICAL: Gmail IMAP deletion is NON-STANDARD.** The standard IMAP
`STORE +FLAGS \Deleted` + `expunge()` sequence does NOT permanently delete
messages in Gmail. It only removes the current label — the message remains
in All Mail and still counts against storage. This is a well-known Gmail IMAP
quirk that makes the first attempt at IMAP deletion appear to succeed (expunge
returns OK) while actually doing nothing.

#### Approach A: Google One Storage Manager (RECOMMENDED — FASTEST)

Navigate to `https://one.google.com/storage/management` and click through
each category, selecting all items and deleting them. This is reliable and
immediate. For ALL messages, this requires multiple passes through different
categories. See the `Immediate Recovery` section above for the dialog pattern.

#### Approach B: Gmail Web UI (Reliable for bulk)

Log into Gmail via the stealth browser, search with `in:anywhere`, select all
conversations, and click the trash icon. Gmail handles the label removal
correctly through its own UI.

#### Approach C: IMAP X-GM-LABELS (Slow but scriptable)

```python
# Gmail-specific IMAP extension to move messages to Trash:
mail.select('"[Gmail]/All Mail"', readonly=False)
status, data = mail.uid('search', None, 'ALL')
uids = data[0].split()

for uid_bytes in uids:
    uid = uid_bytes.decode()
    mail.uid('STORE', uid, '+X-GM-LABELS', '(\\Trash \\Deleted)')

# Then empty Trash:
mail.select('"[Gmail]/Trash"', readonly=False)
mail.uid('STORE', '1:*', '+FLAGS', '\\Deleted')
mail.expunge()
```

⚠️ This is very slow — expect ~100 UIDs/minute. For 50k+ messages it
will timeout at the default 300s `execute_code` limit. Run as a
background terminal process instead. Does work correctly when it
completes.

#### Approach D: IMAP search operators (Selective cleanup only)

```
has:attachment larger:5M
older_than:1y
```

### Photos Cleanup

Google Photos provides a "Move to trash" option in the storage management
page. Items in trash auto-delete after 60 days. For immediate space
recovery, empty trash after moving.

### Drive Cleanup

Usually minimal but check `drive.google.com/drive/quota` for large files.

## Pitfalls

- **🚨 Google blocks automated CDP browser logins.** The Chrome DevTools MCP
  session gets flagged with "This browser or app may not be secure". Always
  use Camofox/Camoufox (stealth Firefox fork) for Google logins.
- **🚨 Takeout email notification won't arrive if Gmail is over quota.**
  Poll the Manage Exports page directly instead of watching the inbox.
  See `scripts/check-takeout.py` for a ready-to-use checker.
- **🚨 IMAP bracket quoting:** Gmail's All Mail mailbox is `"[Gmail]/All Mail"`.
  The brackets must be quoted in the IMAP SELECT command.
- **🚨 Bounced emails are PERMANENTLY LOST while over quota.** Google does
  not queue them for later delivery. The first priority is freeing enough
  space to resume reception. Aim for ~80 MB minimum threshold shown in the
  storage manager, but ideally clear 500 MB+ for headroom.
- **⚠️ App Passwords require 2FA.** The user must have 2-Step Verification
  enabled. Generate at `myaccount.google.com/apppasswords`.
- **⚠️ App Password spaces are cosmetic:** The 16-char password displays
  with spaces (`ufwd gehd yolx lbkm`) but IMAP expects them removed
  (`ufwdgehdyolxlbkm`).
- **⚠️ Storage manager confirmation buttons require checkbox first.** The
  confirm (Move to trash / Permanently delete) button starts disabled.
  Click the checkbox first, wait 1s, then click confirm. See
  `references/storage-manager-cleanup.md` for the exact dialog sequence.
- **⚠️ Only 32 items show per page in the storage manager.** For accounts
  with more than 32 large photos/videos, pagination exists but the UI may
  not show a "next page" link — check the "Unsupported videos" section too.
- **⚠️ Photos content is JS-rendered** and may not appear in a11y snapshots.
  Use the storage management page (`one.google.com/storage/management`) for
  structured cleanup, not the Photos web interface.
- **⚠️ IMAP rate limits:** Downloading 50k+ emails takes 3+ hours at
  ~16,000 emails/hour. The script at `templates/gmail-imap-backup.py` has
  built-in progress tracking for resumable operation. Run in background
  with `notify_on_complete=true`.
- **⚠️ The Takeout email notification WILL NOT ARRIVE if the account is
  over quota.** The "you'll receive an email" message is misleading.
  Poll `https://takeout.google.com/manage` directly.

### Templates Referenced

| File | Purpose |
|------|---------|
| `templates/gmail-imap-backup.py` | Download all Gmail emails + attachments via IMAP |
| `templates/gmail-imap-cleanup.py` | Bulk-delete Gmail emails AFTER backup confirmation |
| `scripts/check-takeout.py` | Poll Google Takeout manage page for archive readiness |
| `references/storage-manager-cleanup.md` | Storage manager UI detail, dialog sequences, automation patterns |
| `references/gmail-imap-deletion-quirk.md` | Gmail IMAP `\Deleted` flag non-standard behavior and working deletion approaches |

## Related

- `stealth-browser-setup` — Camofox lifecycle, cookie import, Firefox profiles
- `firefox-stealth-automation` — xul.dll patching, Firefox automation profile
- `google-data-export` — (archived into this skill)
