---
name: command-financial-analysis-3-statement-model
description: Fill out a 3-statement financial model template. Use when the user wants the Codex equivalent of the upstream `/financial-analysis:3-statement-model` command playbook.
---

# Financial Analysis / 3 Statement Model Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/financial-analysis/3-statement-model.md`.

Original argument hint: `[path to template file]`.

Load the `3-statement-model` skill and populate a 3-statement financial model (Income Statement, Balance Sheet, Cash Flow Statement).

If a file path is provided, use it as the template. Otherwise ask the user for their model template.
