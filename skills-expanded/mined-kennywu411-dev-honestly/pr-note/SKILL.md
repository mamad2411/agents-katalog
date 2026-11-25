---
name: pr-note
description: Put this branch's real test evidence into its pull request (last code edit, each test/build after it and the line it printed, claims with nothing behind them). Use after opening or updating a PR, or when the user asks what was actually verified.
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" pr-note --gh), Bash(python3 "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" pr-note), Bash(python "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" pr-note --gh), Bash(python "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" pr-note)
---

Run, from the repository:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" pr-note --gh
```

Where there is no `python3` (Windows often has only `python`), run the same line with `python`.

It needs the GitHub CLI (`gh`) and an open PR for the current branch. Without a PR, run it without `--gh` to print the block, and show it to the user.

Report what the block says in one or two sentences: whether a test ran after the last code edit and passed. Do not restate it as "all tests pass" unless the block shows a passing run after the last edit.
