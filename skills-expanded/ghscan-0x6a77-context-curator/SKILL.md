---
name: context-list
description: >
  List active sessions and saved contexts with summaries. Use /context-list
  or /context-list <task-id> to see what contexts are available for a task.
allowed-tools: Bash
---

# /context-list

**Usage:** `/context-list [task-id]`

Run the listing script and display its output:

```bash
node ~/.claude/context-curator/dist/scripts/context-list.js ${args}
```

Display the output verbatim. No reformatting or additional analysis needed — the script handles all formatting.
