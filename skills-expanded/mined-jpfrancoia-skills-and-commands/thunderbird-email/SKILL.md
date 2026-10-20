---
name: thunderbird-email
description: Read-only access to Thunderbird/Betterbird email via the local Gloda SQLite database and mbox files. Search emails, read message content, look up contacts, check unread counts. Use when the user asks about their email, messages, inbox, or contacts.
---

# Thunderbird Email Skill

Read-only access to the user's email via Thunderbird/Betterbird's local Gloda search database and mbox mail files. No API keys, no network access -- everything is read from local files.

## When to Use This Skill

Invoke this skill when the user:

- Asks about their **inbox**: "check my email", "any new messages", "what's in my inbox"
- **Searches** for messages: "find that email about X", "what did Y send me", "emails with attachments"
- Asks about **contacts**: "what's X's email address", "who emails me most"
- Needs **email content**: "show me that receipt", "what was the tracking number from Amazon"
- Asks about **email stats**: "how many unread emails", "messages this week"

## Safety Rules

- **NEVER write to any Thunderbird file** -- not the SQLite databases, not the mbox files, nothing.
- **NEVER cat or read entire mbox files** -- they can be multi-GB. Use targeted access only.
- This is a **read-only** skill. To compose or send email, the user should use Thunderbird directly.

## Discovery (Run Once Per Conversation)

On first use in a conversation, run these steps to locate the user's Thunderbird data. Cache the results mentally for the rest of the conversation.

### Step 1: Find the profile directory

```bash
ls -d ~/.thunderbird/*default*/global-messages-db.sqlite
```

The profile directory is the parent of whichever path(s) this returns. Thunderbird profiles almost always contain the word "default" in the directory name (e.g. `abc123.default-release`, `xyz789.betterbird-default`).

If multiple profiles are found, ask the user which one to use. If none are found, Thunderbird may not be installed or the profile path is non-standard.

### Step 2: Map accounts to IMAP directories

```bash
grep -E "mail\.server\.server[0-9]+\.(userName|directory-rel)" <PROFILE>/prefs.js | sort
```

This produces pairs like:

```
user_pref("mail.server.server2.directory-rel", "[ProfD]ImapMail/imap.gmail.com");
user_pref("mail.server.server2.userName", "user@gmail.com");
```

Match server numbers to pair each email address with its IMAP directory under the profile. Ignore entries with `userName=nobody` (that's Local Folders).

### Step 3: Open the Gloda database (read-only)

```bash
sqlite3 "file:<PROFILE>/global-messages-db.sqlite?immutable=1"
```

The `?immutable=1` flag allows safe read-only access even while Thunderbird is running (avoids WAL lock conflicts). Alternatively, copy the file to `/tmp/` first if you need to run many queries.

### Step 4: Build folder map

```sql
SELECT id, folderURI, name, indexingPriority FROM folderLocations ORDER BY id;
```

This maps folder IDs (used throughout the `messages` table) to folder URIs which contain the account email and folder path. The `indexingPriority` values mean:

| Priority | Meaning |
|----------|---------|
| 50 | INBOX |
| 60 | Sent Mail |
| 20 | Normal folder |
| -1 | Trash / Spam / Bin (excluded from search by default) |

## Database Schema Reference

### `messages` -- Individual email messages

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    folderID INTEGER,              -- FK to folderLocations.id
    messageKey INTEGER,            -- IMAP UID (NOT a sequential mbox index)
    conversationID INTEGER NOT NULL, -- FK to conversations.id
    date INTEGER,                  -- Microseconds since Unix epoch
    headerMessageID TEXT,          -- RFC 2822 Message-ID header value
    deleted INTEGER NOT NULL DEFAULT 0,  -- 0=active, 1=deleted
    jsonAttributes TEXT,           -- JSON blob (see key map below)
    notability INTEGER NOT NULL DEFAULT 0
);
```

**Timestamps** are microseconds since Unix epoch. To convert in SQL:

```sql
datetime(date/1000000, 'unixepoch')           -- UTC
datetime(date/1000000, 'unixepoch', '+1 hour') -- UTC+1
```

### `conversations` -- Email threads

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    oldestMessageDate INTEGER,     -- Microseconds (may be NULL)
    newestMessageDate INTEGER      -- Microseconds (may be NULL)
);
```

### `folderLocations` -- Folder registry

```sql
CREATE TABLE folderLocations (
    id INTEGER PRIMARY KEY,
    folderURI TEXT NOT NULL,        -- e.g. "imap://user%40gmail.com@imap.gmail.com/INBOX"
    name TEXT NOT NULL,             -- e.g. "INBOX", "Sent Mail", "Bills"
    indexingPriority INTEGER NOT NULL,
    dirtyStatus INTEGER NOT NULL
);
```

The `folderURI` encodes the account email (URL-encoded `@` as `%40`) and the IMAP server hostname.

### `contacts` -- Known contacts (auto-collected from email headers)

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    directoryUUID TEXT,
    contactUUID TEXT,
    popularity INTEGER,            -- How often this contact appears
    frecency INTEGER,              -- Frequency + recency score
    name TEXT,                     -- Display name
    jsonAttributes TEXT
);
```

### `identities` -- Email addresses linked to contacts

```sql
CREATE TABLE identities (
    id INTEGER PRIMARY KEY,
    contactID INTEGER NOT NULL,    -- FK to contacts.id
    kind TEXT NOT NULL,            -- Always "email"
    value TEXT NOT NULL,           -- The email address
    description NOT NULL,
    relay INTEGER NOT NULL
);
```

### `messagesText_content` -- Full-text content (backing table for FTS)

```sql
-- This is the backing store for the messagesText FTS3 virtual table.
-- The FTS3 MATCH syntax does NOT work with standard sqlite3 (requires
-- Thunderbird's custom "mozporter" tokenizer). Use LIKE instead.
CREATE TABLE messagesText_content (
    docid INTEGER PRIMARY KEY,     -- Same as messages.id
    c0body TEXT,                   -- Plaintext message body
    c1subject TEXT,                -- Subject line
    c2attachmentNames TEXT,        -- Attachment filenames
    c3author TEXT,                 -- From header (name + email)
    c4recipients TEXT              -- To/CC recipients
);
```

**Important**: `LIKE` queries on this table run in ~60ms across 100K+ messages. This is the primary search mechanism.

### `attributeDefinitions` -- Defines jsonAttributes keys

```sql
CREATE TABLE attributeDefinitions (
    id INTEGER PRIMARY KEY,
    attributeType INTEGER NOT NULL,
    extensionName TEXT NOT NULL,
    name TEXT NOT NULL,
    parameter BLOB
);
```

## jsonAttributes Key Map

The `jsonAttributes` column in `messages` is a JSON object with numeric string keys. Here is the complete mapping:

| Key | Name | Type | Description |
|-----|------|------|-------------|
| 43 | from | integer | Contact ID of sender |
| 44 | to | array of int | Contact IDs of To recipients |
| 45 | cc | array of int | Contact IDs of CC recipients |
| 46 | bcc | array of int | Contact IDs of BCC recipients |
| 50 | isEncrypted | boolean | Whether message is encrypted |
| 52 | involves | array of int | All contact IDs involved |
| 53 | recipients | array of int | All recipient contact IDs |
| 55 | toMe | array | Pairs indicating "to me" status |
| 58 | star | boolean | Starred/flagged |
| 59 | read | boolean | Read status |
| 60 | repliedTo | boolean | Whether user replied |
| 61 | forwarded | boolean | Whether user forwarded |

Example `jsonAttributes` value:
```json
{
    "43": 2,
    "44": [1],
    "45": [],
    "46": [],
    "50": false,
    "52": [2, 1],
    "53": [1],
    "55": [[1, 2]],
    "58": false,
    "59": true,
    "60": false,
    "61": false
}
```

To query by attribute (e.g. unread messages), use `json_extract()`:

```sql
-- Unread messages
WHERE json_extract(jsonAttributes, '$."59"') = 0
   OR json_extract(jsonAttributes, '$."59"') IS NULL

-- Starred messages
WHERE json_extract(jsonAttributes, '$."58"') = 1
```

## SQL Recipes

All recipes assume you've opened the database with `?immutable=1` as described in Discovery Step 3.

### Search by keyword (subject + body)

```sql
SELECT m.id, datetime(m.date/1000000, 'unixepoch') as dt,
       t.c1subject, t.c3author, f.name as folder
FROM messages m
JOIN messagesText_content t ON m.id = t.docid
JOIN folderLocations f ON m.folderID = f.id
WHERE m.deleted = 0
  AND (t.c1subject LIKE '%KEYWORD%' OR t.c0body LIKE '%KEYWORD%')
ORDER BY m.date DESC
LIMIT 20;
```

### Recent messages in INBOX

```sql
SELECT m.id, datetime(m.date/1000000, 'unixepoch') as dt,
       t.c1subject, t.c3author
FROM messages m
JOIN messagesText_content t ON m.id = t.docid
JOIN folderLocations f ON m.folderID = f.id
WHERE f.name = 'INBOX'
  AND m.deleted = 0
  AND f.folderURI LIKE '%ACCOUNT_EMAIL%'
ORDER BY m.date DESC
LIMIT 20;
```

Replace `ACCOUNT_EMAIL` with the URL-encoded email (e.g. `user%40gmail.com`). To get messages for all accounts' inboxes, remove the `folderURI LIKE` filter.

### Unread messages

```sql
SELECT m.id, datetime(m.date/1000000, 'unixepoch') as dt,
       t.c1subject, t.c3author, f.name as folder
FROM messages m
JOIN messagesText_content t ON m.id = t.docid
JOIN folderLocations f ON m.folderID = f.id
WHERE m.deleted = 0
  AND f.indexingPriority >= 0
  AND (json_extract(m.jsonAttributes, '$."59"') = 0
       OR json_extract(m.jsonAttributes, '$."59"') IS NULL)
ORDER BY m.date DESC
LIMIT 30;
```

### Messages from a specific person

```sql
-- First find the contact
SELECT c.id, c.name, i.value as email
FROM contacts c
JOIN identities i ON c.id = i.contactID
WHERE c.name LIKE '%NAME%' OR i.value LIKE '%NAME%';

-- Then get their messages (using the contact ID from above)
SELECT m.id, datetime(m.date/1000000, 'unixepoch') as dt,
       t.c1subject, f.name as folder
FROM messages m
JOIN messagesText_content t ON m.id = t.docid
JOIN folderLocations f ON m.folderID = f.id
WHERE m.deleted = 0
  AND json_extract(m.jsonAttributes, '$."43"') = CONTACT_ID
ORDER BY m.date DESC
LIMIT 20;
```

Or search by author string directly (no contact lookup needed):

```sql
SELECT m.id, datetime(m.date/1000000, 'unixepoch') as dt,
       t.c1subject, t.c3author, f.name as folder
FROM messages m
JOIN messagesText_content t ON m.id = t.docid
JOIN folderLocations f ON m.folderID = f.id
WHERE m.deleted = 0
  AND t.c3author LIKE '%NAME_OR_EMAIL%'
ORDER BY m.date DESC
LIMIT 20;
```

### Starred messages

```sql
SELECT m.id, datetime(m.date/1000000, 'unixepoch') as dt,
       t.c1subject, t.c3author, f.name as folder
FROM messages m
JOIN messagesText_content t ON m.id = t.docid
JOIN folderLocations f ON m.folderID = f.id
WHERE m.deleted = 0
  AND json_extract(m.jsonAttributes, '$."58"') = 1
ORDER BY m.date DESC
LIMIT 20;
```

### Messages with attachments

```sql
SELECT m.id, datetime(m.date/1000000, 'unixepoch') as dt,
       t.c1subject, t.c3author, t.c2attachmentNames, f.name as folder
FROM messages m
JOIN messagesText_content t ON m.id = t.docid
JOIN folderLocations f ON m.folderID = f.id
WHERE m.deleted = 0
  AND t.c2attachmentNames IS NOT NULL
  AND t.c2attachmentNames != ''
ORDER BY m.date DESC
LIMIT 20;
```

### Messages in a date range

```sql
-- Timestamps are microseconds since epoch.
-- To convert a date string to microseconds:
--   strftime('%s', 'YYYY-MM-DD') * 1000000

SELECT m.id, datetime(m.date/1000000, 'unixepoch') as dt,
       t.c1subject, t.c3author, f.name as folder
FROM messages m
JOIN messagesText_content t ON m.id = t.docid
JOIN folderLocations f ON m.folderID = f.id
WHERE m.deleted = 0
  AND m.date >= strftime('%s', '2026-01-01') * 1000000
  AND m.date <  strftime('%s', '2026-02-01') * 1000000
ORDER BY m.date DESC
LIMIT 50;
```

### Read full message body (from Gloda)

For most messages, the plaintext body is already in the Gloda database:

```sql
SELECT t.c1subject, t.c3author, t.c4recipients, t.c0body
FROM messagesText_content t
WHERE t.docid = MESSAGE_ID;
```

This returns the plaintext body. For ~95% of queries, this is sufficient. Only resort to reading the mbox file if you need the full MIME content (HTML rendering, raw headers, or actual attachment files).

### Contact lookup

```sql
-- Search by name or email
SELECT c.id, c.name, c.popularity, c.frecency, i.value as email
FROM contacts c
JOIN identities i ON c.id = i.contactID
WHERE c.name LIKE '%QUERY%' OR i.value LIKE '%QUERY%'
ORDER BY c.popularity DESC
LIMIT 10;

-- Most frequent contacts
SELECT c.id, c.name, c.popularity, c.frecency, i.value as email
FROM contacts c
JOIN identities i ON c.id = i.contactID
ORDER BY c.popularity DESC
LIMIT 20;
```

### Conversation thread (all messages in a thread)

```sql
SELECT m.id, datetime(m.date/1000000, 'unixepoch') as dt,
       t.c1subject, t.c3author, f.name as folder
FROM messages m
JOIN messagesText_content t ON m.id = t.docid
JOIN folderLocations f ON m.folderID = f.id
WHERE m.conversationID = CONVERSATION_ID
  AND m.deleted = 0
ORDER BY m.date ASC;
```

### Count messages per folder

```sql
SELECT f.name, f.folderURI, COUNT(m.id) as msg_count
FROM messages m
JOIN folderLocations f ON m.folderID = f.id
WHERE m.deleted = 0
GROUP BY f.id
ORDER BY msg_count DESC;
```

## Reading Full MIME Content from mbox Files

The `messagesText_content.c0body` column has the plaintext body for most messages. Only use mbox access when you need:
- Full HTML email content
- Raw email headers
- Actual attachment file data

### Mapping a message to its mbox file

1. From the `messages` table, get `headerMessageID` and `folderID`.
2. From `folderLocations`, get the `folderURI` for that `folderID`.
3. The `folderURI` encodes the path. For example:
   - `imap://user%40gmail.com@imap.gmail.com/INBOX` -> `<PROFILE>/ImapMail/imap.gmail.com/INBOX`
   - `imap://user%40gmail.com@imap.gmail.com/[Gmail]/Sent Mail` -> `<PROFILE>/ImapMail/imap.gmail.com/[Gmail].sbd/Sent Mail`
   - `imap://user%40gmail.com@imap.gmail.com/Bills/Food` -> `<PROFILE>/ImapMail/imap.gmail.com/Bills.sbd/Food`

The pattern: in the folderURI path after the server, each `/` boundary that has children uses the `.sbd` (sub-directory) convention. The parent becomes an mbox file and `<parent>.sbd/` contains child mbox files.

### Extracting a single message by Message-ID

Use `grep` to find the byte offset, then `python3` to extract:

```bash
# Find which line the Message-ID appears on (fast, even in multi-GB files)
grep -n -m 1 'Message-ID: <HEADER_MESSAGE_ID>' <MBOX_FILE>
```

Then use Python to extract the full MIME message:

```python
import mailbox
import email

# Open mbox (does NOT load everything into memory)
mbox = mailbox.mbox('<MBOX_FILE>')

target_msgid = '<HEADER_MESSAGE_ID>'

for key in mbox.iterkeys():
    msg = mbox.get_message(key)
    if msg.get('Message-ID', '').strip('<> ') == target_msgid.strip('<> '):
        # msg is an email.message.EmailMessage object
        # Get plaintext body:
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                print(part.get_content())
                break
        break

mbox.close()
```

**Warning**: `mailbox.mbox()` iterates sequentially. For a 4.9 GB All Mail file this can be very slow. Prefer the Gloda `c0body` column when possible. If you must use mbox, try the INBOX or specific label folders (which are much smaller) rather than All Mail.

For faster targeted extraction, use `grep -b` to get byte offset and `dd`/`tail` to seek directly:

```bash
# Get byte offset of the Message-ID line
grep -b -m 1 'Message-ID: <HEADER_MESSAGE_ID>' <MBOX_FILE>

# Then read backwards to find the "From - " separator, and forward to the next one
# This is best done with a small Python script using file.seek()
```

## Gmail IMAP Folder Layout

Gmail labels map to IMAP folders in Thunderbird as follows:

```
<PROFILE>/ImapMail/<SERVER_DIR>/
    INBOX                          # Inbox (mbox file)
    INBOX.msf                      # Index for INBOX
    Bills                          # Custom label (mbox)
    Bills.sbd/                     # Subfolder directory for Bills
        Food                       # Nested label: Bills/Food
        Orders                     # Bills/Orders
        Transport                  # Bills/Transport
    Development                    # Custom label
    Deliveries                     # Custom label
    [Gmail].sbd/                   # Gmail system folders
        All Mail                   # All messages (can be very large)
        Sent Mail                  # Sent messages
        Bin                        # Trash
        Drafts                     # May be .msf only (no offline mbox)
        Spam                       # May be .msf only (no offline mbox)
    msgFilterRules.dat             # Message filter rules
```

Key points:
- `.sbd` suffix = "sub-directory", contains child folder mbox files
- `.msf` files are Mork-format indexes -- do NOT try to parse these, use Gloda instead
- Some folders (Drafts, Spam, Templates) may exist only as `.msf` files with no offline mbox copy
- Each IMAP account gets its own directory (e.g. `imap.gmail.com`, `imap.gmail-1.com`, `imap.gmail-2.com`)

## Gotchas

- **Timestamps**: Always microseconds since Unix epoch. Divide by 1,000,000 for seconds.
- **FTS3 MATCH broken**: The `messagesText` virtual table uses Thunderbird's custom `mozporter` tokenizer. Standard `sqlite3` cannot use `MATCH` on it. Always use `LIKE` on the `messagesText_content` backing table instead.
- **messageKey is IMAP UID**: Not a sequential index into the mbox file. Do not try to use it to seek into mbox files.
- **Large mbox files**: `[Gmail]/All Mail` can be 5+ GB. Never read it entirely. Use Gloda's `c0body` for content, or `grep` for targeted mbox access.
- **Database locking**: Always use `?immutable=1` in the SQLite URI, or copy the DB to `/tmp/` first.
- **Deleted messages**: Filter with `WHERE m.deleted = 0` to exclude deleted messages.
- **Folder indexing priority**: -1 means Trash/Spam/Bin. Exclude these from general searches with `WHERE f.indexingPriority >= 0`.
- **NULL dates in conversations**: `oldestMessageDate` and `newestMessageDate` in `conversations` may be NULL. Use `messages.date` for reliable date filtering.
- **Contact ID 1**: Typically the user themselves (the primary account owner).
