---
name: command-equity-research-initiate
description: Create an initiating coverage report. Use when the user wants the Codex equivalent of the upstream `/equity-research:initiate` command playbook.
---

# Equity Research / Initiate Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/equity-research/initiate.md`.

Original argument hint: `[company ticker]`.

Load the `initiating-coverage` skill and begin the 5-task workflow to create an institutional-quality initiation report.

If a ticker is provided, use it. Otherwise ask the user which company to initiate on.
