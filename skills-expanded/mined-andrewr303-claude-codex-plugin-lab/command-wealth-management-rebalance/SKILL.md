---
name: command-wealth-management-rebalance
description: Analyze drift and generate rebalancing trades. Use when the user wants the Codex equivalent of the upstream `/wealth-management:rebalance` command playbook.
---

# Wealth Management / Rebalance Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/wealth-management/rebalance.md`.

Original argument hint: `[client name or account]`.

Load the `portfolio-rebalance` skill to analyze allocation drift and recommend tax-aware rebalancing trades.

If a client or account is provided, use it. Otherwise ask for the portfolio to analyze.
