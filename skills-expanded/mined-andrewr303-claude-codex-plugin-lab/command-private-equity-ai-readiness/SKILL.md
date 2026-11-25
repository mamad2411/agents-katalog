---
name: command-private-equity-ai-readiness
description: Scan the portfolio for the highest-leverage AI opportunities. Use when the user wants the Codex equivalent of the upstream `/private-equity:ai-readiness` command playbook.
---

# Private Equity / AI Readiness Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/private-equity/ai-readiness.md`.

Original argument hint: `[path to quarterly materials folder, or company names]`.

Load the `ai-readiness` skill and scan portfolio companies for AI leverage — per-company go / no-go gate, quick wins ranked by EBITDA impact across the portfolio, and replays that hit multiple companies at once.

If a folder or company list is provided, use it. Otherwise ask which companies to include and for their latest quarterly materials.
