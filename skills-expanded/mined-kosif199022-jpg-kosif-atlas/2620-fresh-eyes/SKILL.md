---
name: fresh-eyes
description: Validates docs/onboarding/workflows by spawning a zero-context agent to walk through them cold, then fix-and-respawn; use for "fresh eyes", "does the onboarding work", "test the docs".
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/fresh-eyes/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
