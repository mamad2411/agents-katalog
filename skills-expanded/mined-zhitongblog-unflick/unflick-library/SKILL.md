---
name: unflick-library
description: >-
  Build and search a personal video library with the unflick player — scan
  folders for videos, search by title or path, list and prune entries, then play
  a result. Use when the user asks to index their videos, find a movie/clip they
  have, or "what's in my library". Requires the unflick MCP server (or CLI).
license: MIT
---

# unflick: media library

Index local video folders into unflick's SQLite library and search them.

## Tools

- `library_scan(dir)` — recursively scan a directory and add video files.
- `library_search(query)` — match by title or path.
- `library_list()` — all indexed media (also the `unflick://library` resource).
- `library_remove(id)` — drop an entry by ID.

## Flows

- **"Add my Movies folder"** → `library_scan(dir="/Users/me/Movies")`, then
  report how many were added.
- **"Find my Inception file and play it"** → `library_search(query="Inception")`
  → take the top hit's `path` → `play(file=path)`.
- **"What do I have?"** → read `unflick://library` or `library_list()` and
  summarize counts / titles.

```bash
unflick library scan ~/Movies
unflick library search "inception" | jq '.[0].path'
unflick library list
```

## Guidance

- Scanning is incremental — re-scanning a folder is safe.
- When a search returns several hits, show the user the candidates (title +
  path) before auto-playing, unless they clearly meant "just play it".
- Use `library_remove(id)` only on an explicit request; confirm the title first.
