---
name: report
description: Check whether Foreman worked as intended in this project's runs, from its gate log, and print a report the user can share in an issue. Use when the user invokes /foreman:report, asks whether Foreman worked during a run, or wants to report a problem with Foreman.
---

# Foreman report

Run from the project root, passing on any `--since` the user gave (for example `--since 2026-10-28T21:00`):

    uv run --no-project --python 3.12 "${CLAUDE_PLUGIN_ROOT}/hooks/report.py"

Show the output as it is, in a code block. Then, in two or three sentences:

- Name each `FAIL` line and what it means for the run. Do not guess at causes the report does not show.
- Say that the report holds only the structure of the gate log (steps, decisions, durations, versions), no files, commands, branches or plans, and that the user should still read it before posting it.
- If they want to report a problem, it goes to https://github.com/michalzan/foreman/issues with this report and a sentence on what they expected and what happened.

Do not read transcripts, the plan or the code for this skill, and do not post anything yourself.
