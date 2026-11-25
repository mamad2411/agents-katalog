---
name: command-investment-banking-cim
description: Draft a Confidential Information Memorandum. Use when the user wants the Codex equivalent of the upstream `/investment-banking:cim` command playbook.
---

# Investment Banking / CIM Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/investment-banking/cim.md`.

Original argument hint: `[company name]`.

Load the `cim-builder` skill and structure a CIM for the specified company.

If a company name is provided, use it. Otherwise ask the user for the target company and available source materials.
