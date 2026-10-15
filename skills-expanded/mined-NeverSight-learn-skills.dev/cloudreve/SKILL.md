---
name: cloudreve
description: >
  Manage files on a self-hosted Cloudreve v4 cloud storage instance.
  Upload local files to Cloudreve, download files from Cloudreve to local,
  list files, check storage capacity, and delete files.
  Activate when user mentions "upload to cloudreve", "cloudreve upload",
  "网盘上传", "传到网盘", "cloudreve下载", "从网盘下载", "网盘文件列表",
  "cloudreve文件", or any Cloudreve/cloud drive file operations.
license: MIT
compatibility: Requires a running Cloudreve v4 instance. Agent must have shell access (curl + python3).
metadata:
  author: zzy-cl
  version: "3.0.0"
  openclaw:
    always: true
    emoji: "☁️"
    requires:
      env:
        - CLOUDREVE_URL
        - CLOUDREVE_USER
        - CLOUDREVE_PASS
    primaryEnv: CLOUDREVE_URL
allowed-tools: exec
---

# Cloudreve File Manager

Manage files on a self-hosted [Cloudreve v4](https://cloudreve.org) instance via its RESTful API.

## When to use

- User wants to upload a local file to their cloud storage
- User wants to download a file from Cloudreve
- User wants to list or browse files on Cloudreve
- User wants to check storage usage / quota
- User wants to delete a file from Cloudreve

## When NOT to use

- User mentions a different cloud service (Google Drive, Dropbox, etc.)
- File operations on the local filesystem only

## Setup

Set environment variables in `openclaw.json`:

```json5
{
  skills: {
    entries: {
      "cloudreve": {
        enabled: true,
        env: {
          CLOUDREVE_URL: "https://cloudreve.example.com",
          CLOUDREVE_USER: "your-email@example.com",
          CLOUDREVE_PASS: "your-password"
        }
      }
    }
  }
}
```

Restart gateway after saving. **Never log or echo credentials.**

## Commands

All scripts in `scripts/` dir, relative to this skill directory.

| Command | Usage | Description |
|---------|-------|-------------|
| `upload.sh` | `upload.sh <URL> <TOKEN> <FILE> [NAME] [DIR]` | Upload local file (auto-overwrites existing) |
| `upload.py` | `python3 upload.py <URL> <TOKEN> <FILE> [NAME] [DIR]` | Upload (Python version, same logic) |
| `download.sh` | `download.sh <URL> <TOKEN> <URI> [PATH]` | Download file to local |
| `list.sh` | `list.sh <URL> <TOKEN> [DIR_URI]` | List directory contents |
| `delete.sh` | `delete.sh <URL> <TOKEN> <FILE_URI>` | Delete a file (auto-retries on lock conflict) |
| `storage.sh` | `storage.sh <URL> <TOKEN>` | Show storage usage |

## Workflow

### 1. Authenticate — get a JWT token

```bash
TOKEN=$(curl -sf -X POST "${CLOUDREVE_URL}/api/v4/session/token" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${CLOUDREVE_USER}\",\"password\":\"${CLOUDREVE_PASS}\"}" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); \
      assert d.get('code')==0, d.get('msg','login failed'); \
      print(d['data']['token']['access_token'])")
```

Tokens expire in ~1 hour. If a command returns 401, re-authenticate and retry once.

### 2. Run the command

```bash
# Example: list root directory
bash scripts/list.sh "$CLOUDREVE_URL" "$TOKEN"

# Example: upload a file
bash scripts/upload.sh "$CLOUDREVE_URL" "$TOKEN" /path/to/file.pdf

# Example: download a file
bash scripts/download.sh "$CLOUDREVE_URL" "$TOKEN" "cloudreve://my/docs/report.pdf" /tmp/

# Example: delete a file
bash scripts/delete.sh "$CLOUDREVE_URL" "$TOKEN" "cloudreve://my/old-file.txt"

# Example: check storage
bash scripts/storage.sh "$CLOUDREVE_URL" "$TOKEN"
```

### 3. Check exit code

`0` = success, non-zero = failure (error message on stderr).

## File URI Scheme

Cloudreve v4 uses `cloudreve://` URIs to locate files. Format:

```
cloudreve://[user@]host[/path][?query]
```

| Component | Description |
|-----------|-------------|
| `host` | File system type: `my` (my files), `shared_with_me`, `trash`, `share` |
| `user` | User ID (optional for `my`, defaults to current user; required for `shared_with_me`) |
| `path` | File path within the file system |
| `query` | Search/filter parameters (list only) |

**Examples:**

| URI | Meaning |
|-----|---------|
| `cloudreve://my` | Current user's root directory |
| `cloudreve://my/documents/report.pdf` | File in subdirectory |
| `cloudreve://my?category=image` | List all images |
| `cloudreve://my?name=report&type=file` | Search for files named "report" |
| `cloudreve://lUpa@my` | Another user's files (admin only) |

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | — |
| 401 | Not logged in | Re-authenticate |
| 403 | No permission | Check user/group permissions |
| 40001 | Parameter error | Check request parameters |
| 40004 | Object existed | **upload.sh auto-deletes and re-uploads** |
| 40013 | Invalid Content-Length | Ensure raw binary upload (not multipart) |
| 40016 | Path not exist | Verify URI path |
| 40020 | Invalid credentials | Check email/password |
| 40049 | File too large | Check storage policy limits |
| 40051 | Insufficient capacity | Free up storage or upgrade |
| 40073 | Lock conflict | File locked by incomplete upload session; **delete.sh auto-retries with backoff** |
| 40077 | Entity not exist | Verify file URI |

## Gotchas

- API prefix: `/api/v4/` — all endpoints use this
- Login: `POST /api/v4/session/token` with `email` + `password` (NOT `/api/v4/user/login`)
- Upload: PUT session → POST chunk(s) — local storage auto-completes, no step 3 needed
- **Upload Content-Type must be `application/octet-stream` (raw binary)** — NOT `multipart/form-data`. Using `-F` or multipart will cause `40013 Invalid Content-Length`
- Download: `POST /api/v4/file/url` returns signed URLs, then GET the URL
- File URIs must be URL-encoded when used as query parameters
- Tokens expire ~1 hour; use refresh token or re-login
- For small files (< chunk_size), single-chunk upload is sufficient
- **Overwrite**: upload.sh handles `40004 Object existed` by deleting the file first, then re-creating the session. If the file is locked (`40073`), it waits and retries
- **Lock conflicts (`40073`)**: Happen when an upload session creates a file record but never completes (crash, timeout, etc.). The lock expires when the session expires. delete.sh uses exponential backoff retry (3 attempts)
- **Official API docs**: https://docs.cloudreve.org/zh/api/overview
- **Two upload scripts**: `upload.sh` (bash, uses `dd` + pipe) and `upload.py` (python, uses `requests`). Same behavior, python version is more portable
