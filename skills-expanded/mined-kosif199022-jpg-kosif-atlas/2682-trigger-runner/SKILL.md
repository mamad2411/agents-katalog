---
name: trigger-runner
description: Runs a folder's declared .aai/triggers.md standing intentions — compares each to last-run stamps in .aai/memory/, runs what's due, and can offer promotion to native hooks/cron on a capable harness; use for "check triggers", "run due triggers", "session-start due-check".
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/trigger-runner/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
