---
name: command-private-equity-ic-memo
description: Draft an investment committee memo. Use when the user wants the Codex equivalent of the upstream `/private-equity:ic-memo` command playbook.
---

# Private Equity / IC Memo Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/private-equity/ic-memo.md`.

Original argument hint: `[company name]`.

Load the `ic-memo` skill and draft a structured IC memo synthesizing due diligence findings, financial analysis, and deal terms.

If a company name is provided, use it. Otherwise ask the user for the target and available materials.
