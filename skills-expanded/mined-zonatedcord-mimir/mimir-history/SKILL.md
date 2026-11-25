---
name: mimir-history
description: Show recent Mimir estimate history. Use when asked to "show mimir history" or "view past estimates". Supports optional count (e.g. "last 5") and --csv flag.
---

Run this command and print the output verbatim:

    node ~/.codex/mimir/scripts/history-show.js [N] [--csv] [--stats]

- Replace `[N]` with a number if the user specified a count (e.g. 5). Omit for default (10).
- Add `--csv` if the user asked for CSV output.
- Add `--stats` if the user asked for statistics or a summary of estimates.

Do not add commentary or interpretation. Output only what the script prints.
