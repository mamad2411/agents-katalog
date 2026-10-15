---
name: email-tool
description: 'Interact with Gmail from the terminal using email_tool.py. Use for listing, searching, filtering, reading, or sending Gmail messages. Triggers: list emails, search emails, filter inbox, read email, send email, check inbox, show attachment, email by subject, email by date, email by sender, unread emails, read emails.'
argument-hint: 'list [count] [--subject TEXT] [--from ADDRESS] [--on DATE] [--since DATE] [--before DATE] [--read|--unread] | read <uid> | attachment <uid> <filename> | send --to <addr> --subject <subj> (--body <text>|--body-file <file>) [--attach file ...] [--compress]'
---

# email-tool

A command-line Gmail client (`email_tool.py`) that connects via IMAP (read/search) and SMTP (send) using a Gmail App Password stored in `.env`.

## Prerequisites

- Python 3.12 virtual environment activated: `source .venv/bin/activate`
- `.env` file with `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD` set
- Gmail IMAP enabled in account settings (Settings → Forwarding and POP/IMAP → Enable IMAP)

---

## Commands

### `list` — List and search inbox messages

```
python email_tool.py list [count]
                          [--subject TEXT]
                          [--from ADDRESS]
                          [--on DATE | --since DATE] [--before DATE]
                          [--read | --unread]
```

Shows the most recent `count` messages (default: `10`) matching all supplied filters.

**Output columns**

| Column | Description |
|--------|-------------|
| `ID`   | IMAP UID — use in `read` / `attachment` commands |
| `From` | Full sender name and address |
| `Subject` | Full subject line |
| `Date` | Received date/time (`YYYY-MM-DD HH:MM:SS`) |
| `R`    | Read status: `Y` = read, `N` = unread |
| `Att`  | `Y` = message likely has attachments |

**Filters**

| Option | Description | Example |
|--------|-------------|---------|
| `--subject TEXT` | Subject contains TEXT (server-side, case-insensitive) | `--subject "invoice"` |
| `--from ADDRESS` | Sender name or address contains ADDRESS (partial match) | `--from "alice"` or `--from "alice@example.com"` |
| `--on YYYY-MM-DD` | Received on this calendar day | `--on 2026-05-01` |
| `--on "YYYY-MM-DD HH:MM"` | Received within this exact minute | `--on "2026-05-01 09:30"` |
| `--since YYYY-MM-DD` | Received on or after this date | `--since 2026-04-01` |
| `--since "YYYY-MM-DD HH:MM"` | Received at or after this date+time | `--since "2026-04-01 08:00"` |
| `--before YYYY-MM-DD` | Received before this date | `--before 2026-05-01` |
| `--before "YYYY-MM-DD HH:MM"` | Received before this date+time | `--before "2026-05-01 18:00"` |
| `--read` | Only read (seen) messages | `--read` |
| `--unread` | Only unread (unseen) messages | `--unread` |

**Mutual exclusivity rules**
- `--on` and `--since` are mutually exclusive
- `--read` and `--unread` are mutually exclusive
- `--since` and `--before` can be combined to form a date/time range

**Examples**

```bash
# 10 most recent messages
python email_tool.py list

# 25 most recent messages
python email_tool.py list 25

# Search by subject keyword
python email_tool.py list --subject "invoice"

# Search by partial sender address
python email_tool.py list --from "alice@"

# Messages received on a specific day
python email_tool.py list --on 2026-05-01

# Messages received at a specific minute
python email_tool.py list --on "2026-05-01 09:30"

# Messages received on or after a date
python email_tool.py list --since 2026-04-01

# Date range
python email_tool.py list --since 2026-04-01 --before 2026-05-01

# Date+time range
python email_tool.py list --since "2026-04-28 08:00" --before "2026-04-28 18:00"

# Only unread messages
python email_tool.py list --unread

# Only unread messages from a specific sender this month
python email_tool.py list --from "boss@" --since 2026-05-01 --unread

# 50 read messages with "report" in subject
python email_tool.py list 50 --subject "report" --read
```

---

### `read` — Read a full message

```
python email_tool.py read <uid>
```

Prints `From`, `To`, `Date`, `Subject`, attachment filenames, and the message body.

```bash
python email_tool.py read 12345
```

---

### `attachment` — Display an attachment

```
python email_tool.py attachment <uid> <filename>
```

Reads and displays an attachment as text. Use the exact filename shown by `read`.

**Supported formats**

| Extension | Output |
|-----------|--------|
| `.txt` `.md` `.csv` `.log` `.rst` `.yaml` `.yml` `.json` `.xml` `.html` `.htm` `.ini` `.toml` `.sh` | Raw text |
| `.docx` | Paragraph text extracted |
| `.pdf` | Text extracted page by page with page-break markers |
| `.zip` | Table of contents: filename, size, modified date |
| Anything else | Error message: unsupported file type |

```bash
python email_tool.py attachment 12345 report.pdf
python email_tool.py attachment 12345 archive.zip
python email_tool.py attachment 12345 notes.docx
```

---

### `send` — Send an email

```
python email_tool.py send --to <addr> --subject <subj>
                          (--body <text> | --body-file <file>)
                          [--attach file1 file2 ...]
                          [--compress]
```

**Options**

| Option | Required | Description |
|--------|----------|-------------|
| `--to` | Yes | Recipient email address |
| `--subject` | Yes | Email subject line |
| `--body` | One of | Inline body text |
| `--body-file` | One of | Path to a plain-text file used as the body |
| `--attach` | No | One or more file paths to attach |
| `--compress` | No | Zip all attachments into `attachments.zip` before sending |

**Examples**

```bash
# Simple message
python email_tool.py send \
  --to colleague@example.com \
  --subject "Quick note" \
  --body "Please see the attached files."

# Body from file with attachments
python email_tool.py send \
  --to colleague@example.com \
  --subject "Monthly report" \
  --body-file message.txt \
  --attach report.pdf data.csv

# Compressed attachments
python email_tool.py send \
  --to colleague@example.com \
  --subject "Project files" \
  --body "Files are compressed in the zip." \
  --attach design.docx notes.md screenshot.png \
  --compress
```

---

## Procedure

1. Confirm `.env` exists with valid credentials (`GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`).
2. Activate the virtual environment: `source .venv/bin/activate`
3. Run the appropriate command.
4. Use `list` to find UIDs, then `read` or `attachment` with those UIDs.

## Troubleshooting

| Error | Fix |
|-------|-----|
| `Error: .env not found` | `cp .env.example .env` and fill in credentials |
| `IMAP LOGIN failed` | Verify App Password; confirm IMAP is enabled in Gmail settings |
| `Attachment not found` | Run `read <uid>` to see exact attachment filenames |
| `Invalid date/datetime` | Use `YYYY-MM-DD` or `'YYYY-MM-DD HH:MM'` (quote when using time) |
| `No messages found` | Filters may be too narrow; try relaxing one filter at a time |
