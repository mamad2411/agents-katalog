---
name: "source-command-hunch-fragile"
description: "Report the most fragile parts of this codebase, with evidence"
---

# source-command-hunch-fragile

Use this skill when the user asks to run the migrated source command `hunch-fragile`.

## Command Template

Ask Hunch for the fragility ranking (run `hunch fragile` or query Hunch),
then produce a **fragility report with evidence**: the specific files/functions,
the bug history behind them, their churn and fan-in, and any missing guards.
Avoid generic advice — every claim must cite a Hunch record or metric.
