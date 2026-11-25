---
name: command-private-equity-dd-prep
description: Prep for a diligence meeting or expert call. Use when the user wants the Codex equivalent of the upstream `/private-equity:dd-prep` command playbook.
---

# Private Equity / DD Prep Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/private-equity/dd-prep.md`.

Original argument hint: `[company name] [meeting type]`.

Load the `dd-meeting-prep` skill and generate targeted questions, benchmarks, and red flags to probe.

If details are provided, use them. Otherwise ask for the company, meeting type (management presentation, expert call, customer reference), and topic focus.
