---
name: command-private-equity-source
description: Source deals — discover companies and draft founder outreach. Use when the user wants the Codex equivalent of the upstream `/private-equity:source` command playbook.
---

# Private Equity / Source Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/private-equity/source.md`.

Original argument hint: `[sector or criteria, e.g. 'industrial services in Texas $10-50M']`.

Load the `deal-sourcing` skill and run the sourcing pipeline: discover target companies, check CRM for existing relationships, and draft personalized founder outreach emails.

If criteria are provided, use them. Otherwise ask the user for sector, size, geography, and deal parameters.
