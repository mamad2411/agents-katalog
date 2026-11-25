---
name: command-private-equity-screen-deal
description: Screen an inbound deal (CIM or teaser). Use when the user wants the Codex equivalent of the upstream `/private-equity:screen-deal` command playbook.
---

# Private Equity / Screen Deal Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/private-equity/screen-deal.md`.

Original argument hint: `[path to CIM/teaser file]`.

Load the `deal-screening` skill and quickly evaluate an inbound deal against the fund's investment criteria.

If a file path is provided, use it. Otherwise ask the user for the deal materials or description.
