---
name: skill-evals
description: Runs one skill's existing evals/evals.json — triggering cases against a fresh subagent, quality cases judged against prose pass criteria — and reports a PASS/FAIL table, no scores; use for "run the evals for X", "test this skill's evals", "does X still trigger right".
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/skill-evals/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
