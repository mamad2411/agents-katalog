---
name: command-investment-banking-process-letter
description: Draft a process letter or bid instructions. Use when the user wants the Codex equivalent of the upstream `/investment-banking:process-letter` command playbook.
---

# Investment Banking / Process Letter Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/investment-banking/process-letter.md`.

Original argument hint: `[IOI or final bid]`.

Load the `process-letter` skill and draft process correspondence.

If a letter type is specified (IOI, final bid, management meeting invite), use it. Otherwise ask the user what stage the process is in.
