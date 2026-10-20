---
name: ctf-xpoc
description: Use when pi needs the xpoc executable for Chaitin cloud/local POC listing, pulling, and target scanning. Trigger on mentions of xpoc, quick POC sweep, Chaitin POC manager, or cloud POC scanning.
---

# Local Assets

- Tool root: wherever `xpoc` is installed (put it on PATH, or `cd` into its directory).
- Binary: `xpoc` (Linux build) / `xpoc.exe` (Windows).
- Read the bundled `doc.md` for pull/list behavior and batch input modes.

# Workflow

- Use `list` first when the user wants to inspect available POCs.
- Use `pull` when the local plugin cache is stale or missing.
- Prefer targeted groups or IDs instead of broad scans when the target scope is narrow.

# Common Commands

```bash
# xpoc should be on PATH or run from its install dir (Linux build)
xpoc list -a
xpoc pull
xpoc -t https://example.com -o result.html
xpoc -g web.list -t https://example.com
xpoc -i targets.txt
```

# Notes

- xpoc is a command-line binary; do not assume GUI behavior.
- Batch mode accepts redirected stdin or `-i targets.txt`.
- Favor narrow POC groups on fragile targets.
