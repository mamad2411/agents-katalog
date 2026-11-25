---
name: command-equity-research-earnings-preview
description: Build a pre-earnings preview with scenarios. Use when the user wants the Codex equivalent of the upstream `/equity-research:earnings-preview` command playbook.
---

# Equity Research / Earnings Preview Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/equity-research/earnings-preview.md`.

Original argument hint: `[company ticker]`.

Load the `earnings-preview` skill and build a pre-earnings analysis with consensus estimates, key metrics to watch, and bull/base/bear scenarios.

If a ticker is provided, use it. Otherwise ask the user which company is reporting.
