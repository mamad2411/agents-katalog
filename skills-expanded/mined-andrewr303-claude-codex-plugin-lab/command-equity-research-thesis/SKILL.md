---
name: command-equity-research-thesis
description: Create or update an investment thesis. Use when the user wants the Codex equivalent of the upstream `/equity-research:thesis` command playbook.
---

# Equity Research / Thesis Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/equity-research/thesis.md`.

Original argument hint: `[company ticker]`.

Load the `thesis-tracker` skill to create a new thesis or update an existing one with new data points.

If a ticker is provided, use it. Otherwise ask the user which position to review.
