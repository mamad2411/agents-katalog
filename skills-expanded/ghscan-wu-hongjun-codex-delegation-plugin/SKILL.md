---
name: pi-status
description: Inspect supervised Pi delegation jobs.
---

Resolve `<plugin-root>` and run:

    node "<plugin-root>/scripts/delegate.mjs" status --provider pi

Forward supported read-only flags such as `--job`, `--all`, `--json`, `--compact`, `--limit`, and
`--stored-status`. Return output verbatim. Pi jobs are headless and do not support attach.
