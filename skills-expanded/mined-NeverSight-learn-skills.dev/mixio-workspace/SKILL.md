---
name: mixio-workspace
description: "Manage media workspaces in Mixio Studio — upload files, get public URLs, organize projects, and manage cached media assets."
version: 0.1.0
invoke: /mixio:workspace
---

# Mixio Workspace

Upload, organize, and retrieve media files in Mixio Studio workspaces. The MCP server handles local caching so repeated uploads are instant.

## Prerequisites

- MCP server configured in your agent: `@mixio-pro/mcp` (see INSTALL.md)

## MCP Tools

These are local tools implemented directly in `@mixio-pro/mcp` (no `studio_` prefix).

### `upload_file`

Upload a local file to Mixio Studio media and cache the path → URL mapping. Re-uploads only when the file's SHA-256 has changed (unless `force: true`).

| Param | Required | Notes |
|-------|----------|-------|
| `path` | yes | absolute or `~`-expanded local path |
| `project_id` | no | scope the media to a Mixio project |
| `organization_id` | no | |
| `alt` | no | alt text/description |
| `category` | no | media category tag |
| `force` | no | re-upload even if cached |

Returns `{ ok: true, entry }` where `entry` includes `path`, `sha256`, `size`, `mediaId`, `url`, `absoluteUrl`, `filename`, `organizationId`, `projectId`, `uploadedAt`, `publicUrl` (= `absoluteUrl ?? url`), `extra`. On failure returns `{ ok: false, error, message }` with `error` one of `not_found`, `permission_denied`, `filesystem_error`, `upload_failed`.

### `get_public_url`

Get the public URL for a local file, re-hashing to detect drift. On a fresh cache hit, returns the cached URL; otherwise uploads (unless `upload: false`).

| Param | Required | Notes |
|-------|----------|-------|
| `path` | yes | |
| `upload` | no | defaults to `true`; set `false` for cache-only lookup |
| `project_id`, `organization_id`, `alt`, `category` | no | used only when uploading on a cache miss |

Returns `{ ok: true, found, source, public_url, entry }` — `source` is `"cache"`, `"cache_sha256"`, or `"uploaded"`. With `upload: false` and no cache hit, returns `{ ok: true, found: false, public_url: null, entry: null }` (not a bare null).

### `list_cached_files`

No params. Returns `{ ok: true, count, entries }` — same entry shape as `upload_file`.

### `forget_path`

Remove one path from the cache (does not delete the remote media). `{ path }` → `{ ok: true, removed: boolean }`.

### `clear_cache`

No params. Drops every cached mapping (does not delete remote media). Returns `{ ok: true, cleared: <count> }`.

## Workflows

### Upload and share

```
1. upload_file({ path: "/renders/final-cut.mp4" })
   → { ok: true, entry: { publicUrl: "https://studio.mixio.pro/api/media/file/..." } }
2. Share entry.publicUrl — it's permanent and publicly accessible
```

### Batch upload a directory

```
1. For each file in directory:
     upload_file({ path })
2. list_cached_files() to verify all uploaded
```

### Re-upload after edits

```
1. Edit the local file
2. upload_file({ path: same_path })
   → Detects content change (SHA-256), re-uploads, returns new URL
```

## Supported formats

Inferred from file extension: `png`, `jpg`/`jpeg`, `webp`, `gif`, `svg`, `mp4`, `mov`, `webm`, `mp3`, `wav`, `m4a`, `ogg`, `json`, `txt`, `pdf`. Anything else uploads as `application/octet-stream`.

## Cache Location

Local cache is stored at `~/.mixio/mcp-cache.db` (SQLite, WAL mode — safe across concurrent sessions/processes). The cache maps local file path ↔ SHA-256 hash ↔ Mixio URL.

Override the cache path with `MIXIO_FASTMCP_CACHE`, or the whole `~/.mixio` state dir with `MIXIO_HOME`.

## Limits

Not exposed by the MCP server — check your Studio plan/dashboard for current upload size and storage limits.
