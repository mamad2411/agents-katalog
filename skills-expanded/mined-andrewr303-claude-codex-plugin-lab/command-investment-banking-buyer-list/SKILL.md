---
name: command-investment-banking-buyer-list
description: Build a buyer universe for a sell-side process. Use when the user wants the Codex equivalent of the upstream `/investment-banking:buyer-list` command playbook.
---

# Investment Banking / Buyer List Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/investment-banking/buyer-list.md`.

Original argument hint: `[company or sector]`.

Load the `buyer-list` skill and build a universe of potential strategic and financial acquirers.

If a company or sector is provided, use it. Otherwise ask the user for the target company details.
