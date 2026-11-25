---
name: split-task
description: Split a large Claude Code task into safer sub-tasks to avoid context limit failures. Use when /mimir shows HIGH or CRITICAL risk.
argument-hint: "<task description> [--files file1 file2 ...]"
allowed-tools: [Bash]
---

Run the Mimir task splitter and display the suggested breakdown:

```bash
node ~/.claude/mimir/scripts/split.js --stdin <<'MIMIR_EOF'
$ARGUMENTS
MIMIR_EOF
```

## Examples

```
/split-task refactor entire authentication system
/split-task migrate all API endpoints to new schema --files src/api/users.ts src/api/posts.ts
```
