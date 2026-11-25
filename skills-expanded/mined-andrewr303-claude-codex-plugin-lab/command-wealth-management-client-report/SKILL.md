---
name: command-wealth-management-client-report
description: Generate a client performance report. Use when the user wants the Codex equivalent of the upstream `/wealth-management:client-report` command playbook.
---

# Wealth Management / Client Report Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/wealth-management/client-report.md`.

Original argument hint: `[client name] [period, e.g. Q4 2025]`.

Load the `client-report` skill to generate a professional client-facing performance report.

If a client and period are provided, use them. Otherwise ask for client details and reporting period.
