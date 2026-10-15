---
name: spec-driven-cancel
description: Cancel and permanently delete an in-progress spec-driven change. Warns before deleting. Use this to abandon a change that will not be implemented.
version: 0.1.0
---

You are helping the user cancel and remove an in-progress spec-driven change.

## Steps

1. **Select the change** — run `node {{SKILL_DIR}}/scripts/spec-driven.js modify` to list active changes. Ask which change to cancel. If already specified, use it.

2. **Warn the user** — this is permanent and cannot be undone. Show:
   > "Cancelling will permanently delete `.spec-driven/changes/<name>/` and all its contents (proposal.md, specs/, design.md, tasks.md). This cannot be undone. Proceed?"
   Wait for explicit confirmation before continuing.

3. **Cancel the change** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js cancel <name>
   ```

4. **Confirm** — report that the change was deleted.

## Rules
- Always warn and require explicit confirmation — deletion is irreversible
- Only cancel active changes (not archived ones)
- If the user wants to abandon a fully implemented change, suggest `/spec-driven-archive` instead — archive preserves history, cancel deletes it
