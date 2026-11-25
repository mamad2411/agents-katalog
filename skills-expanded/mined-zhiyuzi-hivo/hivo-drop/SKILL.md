---
name: hivo-drop
description: Manage files in the Hivo Drop storage service. Use this skill whenever the user asks to upload, download, delete, list, or share files via hivo-drop. Also use it when the user needs a public URL for a file, wants to make a file public or private, or asks about storage quota.
---

# Hivo Drop

> **CRITICAL — Before starting, MUST use the Read tool to read `../hivo-identity/SKILL.md`.**
> All hivo-drop operations require a valid Bearer token, obtained automatically by the `hivo` CLI. But the agent must be registered first (`.hivo/identity.json` must exist). If not registered yet, complete registration following `../hivo-identity/SKILL.md` before proceeding here.

This skill manages files in the Hivo Drop storage service via the `hivo` CLI.

---

## Workflow

### Upload a file

```bash
hivo drop upload <local_file> <remote_path> [--overwrite]
# Examples:
hivo drop upload report.html docs/report.html
hivo drop upload data.json results/data.json --overwrite
# Preview without uploading:
hivo drop upload report.html docs/report.html --dry-run
```

`<remote_path>` is the logical path inside hivo-drop (e.g. `docs/report.html`). Content-Type is detected from the file extension automatically.

Upload output includes a `file_id` (the `id` field in JSON mode, or shown in text mode). This ID is needed when sharing files with a club via `hivo club files add`.

---

### Download a file

```bash
# Save to a local file:
hivo drop download <remote_path> <local_file>
# Print to stdout:
hivo drop download <remote_path>
# Examples:
hivo drop download docs/report.html report.html
hivo drop download notes/memo.txt
```

---

### Delete a file

```bash
hivo drop delete <remote_path> --yes
# Example:
hivo drop delete docs/old-report.html --yes
# Preview without deleting:
hivo drop delete docs/old-report.html --dry-run
```

---

### List files

```bash
# List all files:
hivo drop list
# Filter by prefix:
hivo drop list docs/
```

Text output includes `OWNER_HANDLE` and `SHARE_URL` columns. Public files show their full public URL (`https://drop.hivo.ink/p/{share_id}`); private files show `-`. `OWNER_HANDLE` shows the file owner's handle (e.g. `writer@acme`), or `-` if unavailable.

JSON output (`--format json`) returns `{"files": [...]}` where each entry includes `share_id` (string for public files, `null` for private) and `owner_handle` (string or `null`). Use this to discover public URLs without an extra `hivo drop share` call.

---

### Share a file (set visibility)

```bash
# Make public — prints the public URL:
hivo drop share <remote_path> public
# Make private — revokes the share link:
hivo drop share <remote_path> private
# Preview without changing visibility:
hivo drop share <remote_path> public --dry-run
# Examples:
hivo drop share docs/report.html public
hivo drop share docs/report.html private
```

---

## Limits

| Limit | Value |
|-------|-------|
| Max file size | 1 MB |
| Max files per agent | 100 |

Exceeding either limit returns an error. Delete old files to free quota.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `no .hivo/identity.json found` | Not registered | Follow `../hivo-identity/SKILL.md` to register first |
| `invalid_token` | Token expired or wrong audience | CLI refreshes automatically; if it persists, re-check registration |
| `conflict` | File already exists | Add `--overwrite` flag |
| `file_too_large` | File exceeds 1 MB | Split or compress the file before uploading |
| `quota_exceeded` | 100-file limit reached | Run `hivo drop list` and delete unused files |
| `not_found` | File doesn't exist or is private | Check path with `hivo drop list` |

---

## When helping the user

### Exact commands — use these verbatim

```bash
# Upload
hivo drop upload <local_file> <remote_path>
hivo drop upload <local_file> <remote_path> --overwrite
hivo drop upload <local_file> <remote_path> --dry-run

# Download
hivo drop download <remote_path> <local_file>
hivo drop download <remote_path>           # stdout

# Delete
hivo drop delete <remote_path> --yes
hivo drop delete <remote_path> --dry-run

# List
hivo drop list
hivo drop list <prefix>

# Share (make public — prints URL)
hivo drop share <remote_path> public
hivo drop share <remote_path> public --dry-run
# Unshare (make private)
hivo drop share <remote_path> private
```

> **Do not invent flags or paths. The commands above are the only correct forms.**

### Decision tree

- **Prerequisite check**: Before any operation, verify `.hivo/identity.json` exists in or above the current directory. If not, stop and follow hivo-identity registration flow.
- **Upload**: ask for local file path and desired remote path. Then run `hivo drop upload`. If conflict, ask whether to overwrite.
- **Share / get public URL**: run `hivo drop upload` first if needed, then `hivo drop share <path> public`. Show the returned URL to the user.
- **List files**: run `hivo drop list` (with optional prefix) to show what files exist and their visibility.
- **Delete**: confirm the path with the user, then run `hivo drop delete <path> --yes`.
- **Download**: ask where to save, then run `hivo drop download <remote_path> <local_file>`.
- **Token**: you do not need to manage tokens — the CLI handles this automatically.
