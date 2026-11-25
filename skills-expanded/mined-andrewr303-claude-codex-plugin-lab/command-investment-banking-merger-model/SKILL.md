---
name: command-investment-banking-merger-model
description: Build an accretion/dilution merger model. Use when the user wants the Codex equivalent of the upstream `/investment-banking:merger-model` command playbook.
---

# Investment Banking / Merger Model Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/investment-banking/merger-model.md`.

Original argument hint: `[acquirer] acquiring [target]`.

Load the `merger-model` skill and build a merger consequences analysis.

If acquirer and target are provided, use them. Otherwise ask the user for deal details.
