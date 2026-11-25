---
name: proton-mail
description: "Read and search Proton Mail through the local Proton Bridge (IMAP over STARTTLS on 127.0.0.1). Use when the user mentions Proton Mail, proton-bridge, asks to check/list/search their Proton inbox, read a specific Proton email, or list unread mail. Read-only: it does not send, delete, or move mail. Credentials live at `~/.proton-imap`."
---

# Proton Mail (via Proton Bridge)

Read and search Proton Mail from the command line through the locally running
Proton Bridge app, which exposes a standard IMAP server (`127.0.0.1:1143`) over
STARTTLS. All work goes through one helper: `scripts/proton_mail.py`.

This skill is **read-only** by design: it lists, searches, and reads messages.
It does not send, delete, move, or flag mail.

## Prerequisites (check before any operation)

1. Proton Bridge must be running. Quick check:

       pgrep -af protonmail-bridge

   If nothing prints, tell the user to start it (it is a desktop/tray app):

       protonmail-bridge --no-window &

2. Credentials file `~/.proton-imap` must exist with KEY=VALUE lines:

       PROTON_IMAP_USER=you@proton.me
       PROTON_IMAP_PASS=<bridge-generated password>
       PROTON_IMAP_HOST=127.0.0.1
       PROTON_IMAP_PORT=1143

   The password is the **bridge-specific** password shown in the Proton Bridge
   app under "Mailbox details", NOT the Proton account password. The file
   should be `chmod 600`. If it is missing, ask the user for the bridge
   username and password (or have them run `protonmail-bridge --cli` then
   `info`), then write the file yourself with `umask 077`.

## Usage

Run the helper with `python3` (stdlib only, no deps):

    python3 scripts/proton_mail.py <subcommand> [options]

Resolve the script path relative to this SKILL.md if the client exposes the
skill directory; otherwise use the absolute path
`~/Documents/Project/AI_Project/skills/proton-mail/scripts/proton_mail.py`.

### folders
List every mailbox with message and unread counts. Good first call to discover
folder names (Proton labels appear as IMAP folders, e.g. `Folders/...`,
`Labels/...`).

    python3 scripts/proton_mail.py folders

### list
Recent messages, newest first. Default 15 from INBOX.

    python3 scripts/proton_mail.py list -n 20 -f INBOX

Each block shows a `● ` marker for unread, the date, From, Subject, and a
`[uid N]` token. Pass that UID to `read`.

### unread
Only unseen messages (default 30).

    python3 scripts/proton_mail.py unread -n 50

### search
IMAP server-side search. Combine filters freely; with no filter it lists all.

    python3 scripts/proton_mail.py search --from kaist.ac.kr
    python3 scripts/proton_mail.py search --subject invoice --since 01-Jun-2026
    python3 scripts/proton_mail.py search --text "poster" --unread -n 10

- `--from` / `--subject` / `--text` are substring matches.
- `--since DD-Mon-YYYY` (e.g. `01-Jun-2026`) means on/after that date.
- `--unread` restricts to unseen.
- `-f` selects a folder (default INBOX); use `-f "All Mail"` to search everything.

### read
Full content of one message by UID. Prefers the `text/plain` part, falls back
to HTML. Reading is non-destructive (does NOT mark the message as seen).

    python3 scripts/proton_mail.py read 9253
    python3 scripts/proton_mail.py read 9253 --headers   # headers only
    python3 scripts/proton_mail.py read 9253 -f Sent
    python3 scripts/proton_mail.py read 9253 --raw > msg.eml   # raw RFC822

UIDs are stable within a folder, but differ across folders. Always pair a UID
with the folder it came from.

## Notes & gotchas

- The bridge cert is self-signed for localhost; the helper disables cert
  verification deliberately (connection never leaves `127.0.0.1`).
- INBOX can hold thousands of messages; always bound listings with `-n`.
- "Connection refused" / "cannot reach IMAP" means the bridge is not running.
- "IMAP login failed" means the bridge password in `~/.proton-imap` is stale.
  Bridge rotates it if the user re-adds the account; refresh from the app.
- This skill is read/search only; it does not send, delete, move, or flag mail.
