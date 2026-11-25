---
name: google-storage-management
description: "Back up and clean Gmail, Google Photos, and Drive storage. Full lifecycle from IMAP email download with attachments to Google Takeout orchestration to browser-based bulk deletion of photos. Covers App Password generation, Gmail IMAP quirks, and storage management via Google One."
version: 1.0.0
author: Hermes Agent
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [gmail, google-photos, google-drive, google-takeout, imap, storage, backup, cleanup]
    triggers: [gmail backup, gmail cleanup, google storage, google photos delete, takeout, free up space, google account full, imap download]
    related_skills: [imap-watchdog, google-workspace, stealth-browser-setup, discord-report-format]
---

# Google Storage Management

Back up and clean Google account storage (Gmail, Photos, Drive). Covers three parallel strategies:

1. **IMAP email backup + cleanup** — download all emails with attachments via IMAP, then delete from server
2. **Google Takeout** — comprehensive export (Gmail + Photos + Drive), download archives when ready
3. **Browser-based Photos bulk deletion** — use Camofox/stealth browser to select-all and trash thousands of photos

## Prerequisites

- Gmail App Password (required for IMAP when 2FA is on). Generate at `https://myaccount.google.com/apppasswords`
- Camofox or Camoufox stealth browser running for photos deletion via web UI

## IMAP Email Backup

### Connection

```python
import imaplib
mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login("username@gmail.com", "APP_PASSWORD")
```

### Mailbox Names (Gmail)

Gmail uses the "/" separator with brackets. Quote the full name:

```python
mail.select('"[Gmail]/All Mail"', readonly=True)   # ALL messages
mail.select('INBOX')                                 # Inbox only
mail.select('"[Gmail]/Trash"')                       # Trash
mail.select('"[Gmail]/Spam"')                        # Spam
mail.select('"[Gmail]/Sent Mail"')                   # Sent
mail.select('"[Gmail]/Drafts"')                      # Drafts
```

### Download All Emails

Full backup strategy:
1. Select `"[Gmail]/All Mail"` to get ALL messages (not just inbox)
2. Use `mail.uid('search', None, 'ALL')` to get all UIDs
3. Fetch each with `mail.uid('fetch', uid, '(RFC822)')`
4. Save as .eml files, extract attachments separately
5. Track progress with a JSON state file (last_uid, total_downloaded)
6. Process in batches of 50-100 to avoid timeouts

### List Mailboxes

```python
status, mailboxes = mail.list()
for mb in mailboxes:
    print(mb.decode('utf-8', errors='replace'))
```

### Check Message Size Distribution

```python
for size_filter, label in [("5000000", ">5MB"), ...]:
    status, data = mail.uid('search', None, f'LARGER {size_filter}')
    count = len(data[0].split()) if data[0] else 0
```

### Download Attachments

Walk message parts with `msg.walk()`, check `Content-Disposition: attachment`, extract `part.get_payload(decode=True)`. Save to categorized folders (video/, image/, other/).

## Gmail IMAP Deletion (Critical Quirk)

**Gmail's IMAP does NOT permanently delete with `\Deleted` + `EXPUNGE`.** This is the most common pitfall. Standard IMAP `STORE +FLAGS \Deleted` followed by `EXPUNGE` only hides messages from the current folder view in Gmail.

### Correct Gmail Deletion Method

Use the Gmail-specific `X-GM-LABELS` extension to move messages to Trash:

```python
# Single UID
mail.uid('STORE', uid, '+X-GM-LABELS', '(\\Trash \\Deleted)')

# Batch (comma-separated UIDs, max ~200 per batch)
uid_list = ','.join(uids)
mail.uid('STORE', uid_list, '+X-GM-LABELS', '(\\Trash \\Deleted)')
```

After moving to Trash, select `"[Gmail]/Trash"` and permanently delete:

```python
mail.select('"[Gmail]/Trash"', readonly=False)
mail.uid('STORE', '1:*', '+FLAGS', '\\Deleted')
mail.expunge()
```

### `1:*` Wildcard

For non-All-Mail folders (Trash, Spam, Inbox), `'1:*'` works as a UID wildcard to select all messages:

```python
mail.select('"[Gmail]/Spam"', readonly=False)
mail.uid('STORE', '1:*', '+FLAGS', '\\Deleted')
mail.expunge()
```

### Performance

- Batch `STORE` with comma-separated UIDs (~200/batch) is faster than individual
- `1:*` wildcard only works on smaller folders
- For All Mail with 50k+ messages, X-GM-LABELS per-UID is slow (~5-10s per 100 UIDs)
- The web UI (Google One Storage Manager) is faster for bulk deletion

### PITFALL -- Gmail IMAP EXPUNGE Timeout / System Error

**Symptom:** Calling `mail.expunge()` on the Trash folder (or any folder with 10k+ messages marked `\Deleted`) raises `imaplib.IMAP4.abort: System Error` or `socket error: EOF`.

**Root cause:** Gmail's IMAP server closes the connection on large EXPUNGE operations (~8k+ messages). The `\Deleted` flag is stored on each UID, but the server can't atomically expunge that many in one command.

**Fix -- small batches with fresh connections:**

```python
BATCH_SIZE = 500
all_uids = data[0].split()
for i in range(0, len(all_uids), BATCH_SIZE):
    batch = all_uids[i:i+BATCH_SIZE]
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(USERNAME, PASSWORD)
    mail.select('"[Gmail]/Trash"', readonly=False)
    batch_str = ','.join(uid.decode() for uid in batch)
    mail.uid('store', batch_str, '+FLAGS', '\\Deleted')
    try: mail.expunge()
    except: pass  # Connection reset after successful STORE is normal
    mail.logout()
```

Each batch gets a fresh connection. The `STORE` flag-setting succeeds even if the subsequent `EXPUNGE` or `LOGOUT` raises -- the server processes the flag change immediately.

**Verification:** Reconnect and check Trash count drops to 0.

## Google Takeout

1. Navigate to `https://takeout.google.com`
2. Select products: Mail, Drive, Photos (the storage-heavy ones)
3. Choose file type (ZIP), size (2 GB), frequency (Export once)
4. Export can take hours to days
5. Download link is emailed, OR check `https://takeout.google.com/manage`
6. **Caveat:** if Gmail storage is full, the email notification may bounce. Always check the Manage Exports page directly.

## Google Photos Bulk Deletion (Browser)

Phased approach through Google One Storage Manager:
1. Go to `https://one.google.com/storage/management`
2. Click "Large photos and videos" → select all → Move to trash
3. Click "Show more items" repeatedly to load additional batches
4. Click "Unsupported videos" → same process
5. Empty Photos trash at `https://photos.google.com/trash`

For the main Photos grid (`photos.google.com`):
1. Navigate to All Photos view
2. Use JavaScript to select all visible checkboxes:
   ```javascript
   var cbs = document.querySelectorAll('[role="checkbox"]');
   for (var i = 0; i < cbs.length; i++) {
       if (cbs[i].getAttribute("aria-checked") !== "true" && cbs[i].offsetParent !== null) {
           cbs[i].click();
       }
   }
   ```
3. Click "Move to trash" in the toolbar
4. Confirm
5. Empty trash

Repeat scroll + select + trash cycles until all photos are cleared. Each cycle handles ~49-127 items.

## Storage Progress Tracking

Use Google One storage page (`https://one.google.com/storage`) to track progress:

| State | Meaning |
|-------|---------|
| "You're out of storage" | 100% — email bouncing |
| "You've used 99% of storage" | 14.9 GB/15 GB — email working |
| "You've used 95% of storage" | 14.3 GB/15 GB |
| Photos: X GB | Deleted items remain in Trash for 60 days |
| Gmail: X GB | Trash must be emptied separately |

Trashed items still count against quota until the Trash is emptied or the 60-day auto-delete runs.

## References

- `references/gmail-imap-deletion.md` — Full transcript of the X-GM-LABELS deletion technique

## Pitfalls

- **🚨 `\Deleted` + `EXPUNGE` does NOT delete in Gmail.** It only hides from current folder. Use `X-GM-LABELS \Trash \Deleted`.
- **App Password required** when 2FA is enabled. Generate from Google Account security settings.
- **Trash counts against quota.** Deleting via IMAP moves to Trash; must empty Trash separately for space to free.
- **Google One storage numbers are cached.** May not update for several minutes after deletion.
- **Camoufox browser may crash** under heavy automation. Restart the server process.
- **Takeout can take hours-days.** Set up a cron checker. Check Manage Exports page directly (email may bounce if Gmail is full).
- **Rate limits:** Gmail IMAP ~2000 connections/day. Keep watchdog/batch scripts under this limit.
- **Takeout notification emails may bounce** when Gmail is full. Always check the Manage Exports page directly.
