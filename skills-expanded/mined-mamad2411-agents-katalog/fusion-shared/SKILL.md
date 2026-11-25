---
name: fusion-shared
description: Internal shared-reference support package for installed fusion-* skills (fusion-writing, fusion-polishing, fusion-reader, fusion-data-analysis, fusion-diagnostics, fusion-machine-ops, etc.). Do not invoke it as a standalone user workflow. Load only the specific core or journal-format file requested by another fusion skill.
---

# Fusion Shared References

Use this package only as a dependency of another installed fusion skill.

- Load the exact referenced file; do not preload the whole package.
- Treat `core/` and `journal-formats/` as shared definitions, not standalone workflows.
- `core/terminology-ledger.md` is the single source of truth for fusion bilingual terminology and symbol conventions.
- `core/machine-database.md` is the single source of truth for machine parameters (EAST, DIII-D, NSTX, KSTAR, W7-X, JET, ITER, CFETR).
- Use a specific `journal-formats/<journal>.md` only when the target journal's formatting requirements matter for the current task.
- Return to the requesting skill for task logic, output format, and final QA.
