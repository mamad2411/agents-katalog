---
name: command-equity-research-screen
description: Run a stock screen or generate investment ideas. Use when the user wants the Codex equivalent of the upstream `/equity-research:screen` command playbook.
---

# Equity Research / Screen Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/equity-research/screen.md`.

Original argument hint: `[screen criteria, e.g. 'undervalued midcap tech']`.

Load the `idea-generation` skill and run quantitative screens or thematic sweeps to surface new investment ideas.

If criteria are provided, use them. Otherwise ask the user what they're looking for (long/short, sector, style, theme).
