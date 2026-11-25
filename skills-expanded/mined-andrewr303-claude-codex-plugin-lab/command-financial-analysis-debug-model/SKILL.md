---
name: command-financial-analysis-debug-model
description: Debug and audit a financial model for errors. Use when the user wants the Codex equivalent of the upstream `/financial-analysis:debug-model` command playbook.
---

# Financial Analysis / Debug Model Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/financial-analysis/debug-model.md`.

Original argument hint: `[path to .xlsx model file]`.

Load the `audit-xls` skill with scope **model** and audit the specified financial model for broken formulas, balance sheet imbalances, hardcoded overrides, circular references, and logic errors — including the full model-integrity checks (BS balance, cash tie-out, roll-forwards, model-type-specific bugs).

If a file path is provided, use it. Otherwise ask the user for the model to review.
