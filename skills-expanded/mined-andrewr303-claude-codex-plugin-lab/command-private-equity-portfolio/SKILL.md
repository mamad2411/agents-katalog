---
name: command-private-equity-portfolio
description: Review portfolio company performance. Use when the user wants the Codex equivalent of the upstream `/private-equity:portfolio` command playbook.
---

# Private Equity / Portfolio Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/private-equity/portfolio.md`.

Original argument hint: `[company name or path to financial package]`.

Load the `portfolio-monitoring` skill and analyze a portfolio company's performance against plan — KPIs, variances, and red flags.

If a company name or file is provided, use it. Otherwise ask the user for the portfolio company and financial data.
