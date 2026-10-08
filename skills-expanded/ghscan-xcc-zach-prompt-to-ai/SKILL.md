---
name: read-through-codebase
description: Create a comprehensive understanding of the codebase overview and functionality by reading through the codebase. Use when `docs/ai/*` does not exist.
---

Research the codebase comprehensively. Write to the following files under project's `.aidocs/` directory (create if not exists; If the documents below already exist, skip writing and directy output a message indicating their existence):
- `codebase-overview.md`: Refer to `instructions/codebase-overview.md` for instructions.

After creating the above files, commit with `ai-docs-commit` skill with arguments "add docs after reading through codebase".