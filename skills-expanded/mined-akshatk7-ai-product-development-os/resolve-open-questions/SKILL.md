---
name: resolve-open-questions
description: Use when asking "what's still TBD?", "any open questions?", "clean up open items", or auditing unresolved decisions.
---

Scan all projects for unresolved items and check if they've been answered.

**Before starting:** Read `gotchas.md` and `runs.log` in this skill folder.

## Instructions

1. Grep all files under `projects/` for: "TBD", "open question", "pending", "awaiting", "to be determined", "needs decision", "unclear".
2. For each hit, extract: file path, surrounding context, approximate age.
3. For items >1 week old, search for resolution evidence in Slack and meeting notes.
4. Output grouped by project:

```
## Open Questions Audit

### [Project Name] ([count] items)

**Resolved** (evidence found):
- [file:line]: [question] → **Answer:** [what was decided, source]

**Still Open:**
- [file:line]: [question] — [age]

**Stale** (>2 weeks, no evidence):
- [file:line]: [question] — [age] — suggest asking [person from README.md team]
```

5. For "Resolved" items, propose the specific file edit.
6. Present to user for approval before making any edits.

## Post-Run
Append to `runs.log`. If new failure patterns discovered, add to `gotchas.md`.
