---
name: data-skill
description: Read, search, and write raw local data (files, CSV, JSON, PDF, HTML, XLSX, images) across the workspace and operator-mounted folders. Use when the user asks about local files, documents, spreadsheets, logs, or data on disk.
allowed-tools: data
metadata:
  author: opencompany
  version: "1.0"
  category: data
  icon: "🗂️"
  color: "#50fa7b"

---

# Data Access Skill

Work with raw local data through the `data` tool. Check the tool in your
tool list for the full schema; this skill covers strategy, not parameters.

## The two path namespaces

- `reports/q3.csv` — workspace-relative (the workflow's own scratch space,
  always readable and writable)
- `mnt/<mount_name>/file.csv` — an external folder the operator approved;
  read-only unless its writable flag is on

You MUST start with `list` on an empty path: it returns the workspace root
AND the mounts enabled on this node (with their writable flags). Never guess
mount names.

## Reading — pick the honest tier, page deliberately

`read` auto-detects text / csv / json / pdf / html / xlsx / image / binary
from the extension; `as_type` forces a tier when the extension lies.

- Everything is paged with `offset` / `limit`. Check `truncated` and
  `rows_total` / `lines_total` / `pages_total` before summarizing — a
  truncated read is a sample, not the file.
- Skim first, then zoom: read with the default limit to see the shape, then
  page into the region that matters. Do not crank `limit` to the max on the
  first read of an unknown file.
- CSV/XLSX return `columns` + `rows`; JSON deep structures are pruned at
  depth 8 (`pruned_paths` tells you where — read a subpath as text if you
  need what was pruned).
- Images return metadata plus a file reference — if the host model supports
  vision the image itself becomes visible; otherwise use the `vision` tool.
- Binary files return a reference and checksum, never content. Pass the
  reference's path to a tool that can handle the format.

## Writing — bounded and non-destructive

- `write` replaces, `append` extends; both are UTF-8 text, workspace or
  writable mounts only.
- There is NO delete. Do not try to empty files as a substitute; tell the
  user deletion is a manual action in the gallery panel.
- `copy_to_workspace` imports a mount file into the workspace (never
  overwrites — it suffixes). Use it before operations that need a workspace
  reference: previews, drags, vision on mount images.

## Anti-patterns

- Guessing paths instead of `list`/`search` first.
- Re-reading a whole file when you already have the page you need — results
  persist in your context; reread only new offsets.
- Reading a huge JSON as `json` when you need one field — read as text and
  page, or search first.
- Asking for a mount that is not in your `list` result: mounts are
  operator-controlled; you cannot add them.
