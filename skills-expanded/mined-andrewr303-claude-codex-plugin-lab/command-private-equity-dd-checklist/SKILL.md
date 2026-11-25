---
name: command-private-equity-dd-checklist
description: Generate a due diligence checklist. Use when the user wants the Codex equivalent of the upstream `/private-equity:dd-checklist` command playbook.
---

# Private Equity / DD Checklist Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/private-equity/dd-checklist.md`.

Original argument hint: `[company name]`.

Load the `dd-checklist` skill and generate a comprehensive, sector-tailored due diligence checklist with status tracking.

If a company name is provided, use it. Otherwise ask the user for the target company and deal details.
