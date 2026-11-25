---
name: local-file-memory
description: Use a Markdown file in the repo as persisted agent memory across chats. Use when the user wants session-spanning context, a decision log, or to resume work without re-pasting history.
---

# Local file memory

Teach and apply the **local file** pattern for agent memory: read before work, update after.

## Steps

1. **Resolve path** — Default: `.cursor/agent-memory/MEMORY.md`. If missing, copy the starter from [examples/agent-frameworks/local-file-memory-template/MEMORY.md](../../../examples/agent-frameworks/local-file-memory-template/MEMORY.md) and create the directory.

2. **Read first** — Open the memory file and summarize **Current focus**, **Decisions**, and **Open questions** in chat (or use them silently if the user only asked for edits).

3. **Do the task** — Follow the user’s request; align with **Do not forget** and past **Decisions**.

4. **Update memory** — After substantive work, edit the file: refresh **Current focus**, append dated lines under **Decisions**, check off or add **Open questions**, extend **Do not forget** if new constraints appeared. Optionally add a line under **Session log**.

5. **Stay safe** — Do not store secrets (keys, tokens) in memory files. See [local-file-memory.md](../../../examples/agent-frameworks/local-file-memory.md).

## Reference

- Full write-up: [examples/agent-frameworks/local-file-memory.md](../../../examples/agent-frameworks/local-file-memory.md)
- Heavyweight variant (split state + workflow): [project-vibe-master-workflow.md](../../../examples/agent-frameworks/project-vibe-master-workflow.md); template [initial-state/](../project-vibe-master-workflow/initial-state/), generated practice files [data/](../project-vibe-master-workflow/data/)
