---
name: catches
description: Show what honestly stopped this week (unbacked claims and piped test runs), by project and assistant.
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" catches), Bash(python "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" catches)
---

Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" catches
```

Where there is no `python3` (Windows often has only `python`), run the same line with `python`.

Summarise the result for the user in a few lines. If a catch looks wrong, `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" feedback` prints an issue-ready report.
