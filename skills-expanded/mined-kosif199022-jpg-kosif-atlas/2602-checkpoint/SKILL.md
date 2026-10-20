---
name: checkpoint
description: Preserve conversation context across compaction and hand off work across sessions, agents, and CLI windows. Two modes. COMPACT mode (the default — "/checkpoint", "/checkpoint:compact", "checkpoint before compact", "save context before clearing", "I'm about to compact/clear", or whenever the context window is getting long) distills the high-signal context since the last checkpoint into the project's `.aai/checkpoint.md`, then tells the user to run /compact. SESSION mode ("/checkpoint:session", "session check-in", "what should I work on", "resume work", "wrap up", "session check-out") runs the multi-agent .context/ store protocol — claims a task on entry, updates the board and appends a handoff entry on exit. Use compact mode for single-conversation continuity; session mode for projects with a `.context/` directory coordinating multiple agents.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/checkpoint/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
