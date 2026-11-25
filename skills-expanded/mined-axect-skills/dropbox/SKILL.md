---
name: dropbox
description: Upload files to Dropbox, download from Dropbox, and create or reuse shared links. Use when the user mentions Dropbox, asks to upload/download/share a file via Dropbox, or wants a shareable link for a file already in Dropbox. Use `~/.config/dropbox-skill/credentials.json` as the only supported credentials path.
---

# Dropbox

Dropbox file operations via Dropbox HTTP API v2. Unifies upload, download, and shared-link operations.

## Trigger conditions

Invoke this skill when the user says any of:
- "upload X to Dropbox" → use `scripts/upload.sh`
- "download X from Dropbox" / "get X from Dropbox" → `scripts/download.sh`
- "share link", "shared link", "Dropbox link", "make a link for X" → `scripts/share.sh`
- "set up Dropbox", "configure Dropbox", or when `~/.config/dropbox-skill/credentials.json` does not exist → `scripts/setup.sh`

## Prerequisites (check before any operation)

Before running upload/download/share, verify the credentials file exists:

    test -f ~/.config/dropbox-skill/credentials.json

If it does not exist, tell the user:
> Dropbox is not set up yet. I can run the setup flow — it will ask for your app key, app secret, and an authorization code from a browser URL. Proceed?

Only run `setup.sh` after the user confirms.

## Path rules

- Dropbox paths MUST start with `/` (e.g. `/Papers/draft.pdf`). Reject relative paths.
- If the user gives a bare filename (e.g. "report.pdf"), ask which Dropbox folder before acting.

## Script usage

All scripts live in this skill directory's `scripts/` folder. If your client exposes the skill directory path, use it. Otherwise resolve the script path relative to this `SKILL.md` file.

### setup.sh
Interactive one-time bootstrap. Takes stdin input for app key, app secret, and authorization code.

    bash scripts/setup.sh

### upload.sh
Upload local → Dropbox. Auto-chooses single-shot vs chunked session based on file size.

    bash scripts/upload.sh <local_path> <dropbox_path>

Prints a one-line JSON summary on success: `{"path":"...","size":N,"content_hash":"..."}`

### download.sh
Download Dropbox → local. Refuses to overwrite existing local files.

    bash scripts/download.sh <dropbox_path> [<local_path>]

If `<local_path>` is omitted, uses `basename <dropbox_path>` in the current directory.
Prints the saved path on stdout.

### share.sh
Create (or retrieve existing) shared link.

    bash scripts/share.sh <dropbox_path>

Prints the URL on stdout.

## Error handling

If any script exits non-zero, show its stderr to the user verbatim. Do not retry auth errors automatically (exit codes 2 and 3) — surface them so the user can re-run setup.

Exit code reference:
- 0 — success
- 1 — bad argument or local filesystem error
- 2 — credentials.json missing (→ user should run setup.sh)
- 3 — refresh token rejected (→ user should re-run setup.sh)
- 4 — Dropbox path not found
- 5 — other API error
- 64 — usage error
- 127 — missing dependency (curl/jq)
