---
name: ag-journal
description: write_to_file technical journal entries analyzing recent changes. Use
  for session reflections, change analysis, decision documentation.
---


# Journal

Use the `journal-writer` subagent to explore the memories and recent code changes, and write some journal entries.
Journal entries should be concise and focused on the most important events, key changes, impacts, and decisions.
Keep journal entries in the `./docs/journals/` directory.

**IMPORTANT:** Invoke "/ag-project-organization" skill to organize the outputs.

## Workflow Position

**Typically follows:** `/ag-ship` (journal after shipping), `/ag-cook` (journal after implementation), `/ag-fix` (journal after bug fix)
**Terminal skill** — no typical successor.
