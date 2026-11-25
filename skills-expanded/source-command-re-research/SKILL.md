---
name: "source-command-re-research"
description: "Refresh one Stinger's research archive on the six-month window by re-running the forge pipeline's Research and Distillation stages, then flag which guides now rest on claims the refreshed research contradicts or no longer supports. Trigger with \"re-research the payments stinger\", \"refresh research for X-stinger\", \"is Y-stinger's research stale\", \"update the research archive for Z\", \"the six-month window is up on this stinger\"."
license: "AGPL-3.0-or-later"
disable-model-invocation: true
---

# source-command-re-research

Use this skill when the user asks to run the migrated source command `re-research`.

Read [the command procedure](../../commands/re-research.md) in full before acting. Resolve paths in that procedure relative to its `commands/` directory. Codex invokes this as a skill, not a slash command.

This command maintains The Wasp Nest itself. Require a writable source checkout and read its live `src/commands/re-research.md` before making changes; never edit the installed plugin cache.
