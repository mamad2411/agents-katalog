---
name: list-miro-boards
description: List the user's authorized Miro boards with the permanent local read-only helper. Use when the user asks to list, show, find, inventory, or check their Miro boards, or asks to run LIST_BOARDS.bat without browsing to its folder.
metadata:
  created_by: Codex
  source: self
  date_added: "2026-07-11"
---

# List Miro Boards

Run the existing secured helper and report its board list. This skill is read-only.

## Run

Execute:

```powershell
& 'C:\Users\kamil\.miro-tools\.venv\Scripts\python.exe' 'C:\Users\kamil\.miro-tools\miro_helper.py' list
```

This is the non-interactive equivalent of `C:\Users\kamil\.miro-tools\LIST_BOARDS.bat`. Prefer it because the batch file pauses for keyboard input.

## Report

- Return the board names and IDs shown by the helper.
- State that no board was created, changed, or deleted.
- If no boards are accessible, say so plainly.

## Safety Boundaries

- Keep this workflow read-only. Do not request `boards:write` or perform create, update, or delete operations.
- Never print, retrieve, copy, or expose credential values, OAuth tokens, client secrets, or Windows Credential Manager contents.
- Do not save credentials, authentication output, or private logs in Baza, Google Drive, source control, screenshots, or chat.
- Do not run `SETUP.bat` or `AUTHORIZE.bat` unless listing fails specifically because authorization is absent or expired.
- If authorization is required, tell the user that the read-only authorization needs renewal and guide them one beginner-friendly step at a time. Never ask them to paste a secret or token into chat.
- If the expected helper files are missing, report the missing path instead of recreating or moving the tool without permission.
