---
name: grapim
description: Use when the user asks who or which agent changed a line or file, wants to see what each agent session changed, wants to undo or revert one agent's run (or one turn) while keeping other agents' work, wants a branch of one agent's changes, wants to restore an earlier version of a file, or when an edit was blocked because another agent holds the file.
---

# Grapim

Grapim records every edit each agent session makes in this repo. Use its commands to answer "who changed this" and to undo one agent's work without touching anyone else's.

Run the CLI as `node "${CLAUDE_PLUGIN_ROOT}/bin/grapim.js" <command>` from the repo. The MCP tools `list_runs`, `who_wrote`, `who_is_editing` and `recent_activity` give the same information without a shell.

- **What each agent changed:** `runs`
- **Who wrote each uncommitted line of a file:** `blame <file>`
- **Undo one agent's run** (or one turn with `--turn N`): run `undo <run>` first. It only prints the plan. Show the plan to the user, and run `undo <run> --yes` only after they agree. Other agents' later edits in the same files are kept. Files with overlapping edits are reported as conflicts and left alone.
- **Put one run's changes on its own git branch,** without touching the working tree: `branch <run>`
- **Approve or reject a run:** `review <run> --approve|--reject --note "..."`
- **Restore a file to a recorded version:** `restore <file> <sha-prefix>` prints the plan; add `--yes` to apply.
- **The review desk in the browser:** `serve --open`

If an edit was blocked because another agent holds the file, don't retry it. Work on other files, or tell the user who has it and what they are doing (`status` shows this).

Never run `undo --yes` or `restore --yes` without the user's explicit OK.
