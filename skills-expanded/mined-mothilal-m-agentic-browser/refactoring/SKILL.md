---
name: refactoring
description: Improve structure and readability without changing behavior.
metadata:
    triggers:
        - refactor this
        - clean up this code
        - improve maintainability
    tags:
        - coding
        - refactor
    priority: 70
---

Refactor conservatively while preserving behavior.

Checklist:
- Keep public APIs stable unless explicitly requested.
- Prefer small, testable transformations.
- Remove duplication and simplify control flow.
- Preserve performance characteristics unless improving them intentionally.
