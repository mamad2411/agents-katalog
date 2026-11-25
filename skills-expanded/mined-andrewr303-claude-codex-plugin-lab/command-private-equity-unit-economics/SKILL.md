---
name: command-private-equity-unit-economics
description: Analyze unit economics (ARR cohorts, LTV/CAC, retention). Use when the user wants the Codex equivalent of the upstream `/private-equity:unit-economics` command playbook.
---

# Private Equity / Unit Economics Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/private-equity/unit-economics.md`.

Original argument hint: `[company name or path to data]`.

Load the `unit-economics` skill and analyze customer economics, ARR cohorts, net retention, and revenue quality.

If a company or file is provided, use it. Otherwise ask the user for the target and available data.
