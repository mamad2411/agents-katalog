---
name: command-equity-research-model-update
description: Update a financial model with new data. Use when the user wants the Codex equivalent of the upstream `/equity-research:model-update` command playbook.
---

# Equity Research / Model Update Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/equity-research/model-update.md`.

Original argument hint: `[company ticker]`.

Load the `model-update` skill and plug in new earnings, guidance, or revised assumptions.

If a ticker is provided, use it. Otherwise ask the user which model to update and what changed.
