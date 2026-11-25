---
name: command-wealth-management-proposal
description: Create an investment proposal for a prospect. Use when the user wants the Codex equivalent of the upstream `/wealth-management:proposal` command playbook.
---

# Wealth Management / Proposal Command Playbook

This installable skill wraps the exported command playbook from `codex/commands/wealth-management/proposal.md`.

Original argument hint: `[prospect name]`.

Load the `investment-proposal` skill to create a personalized investment proposal for a prospective client.

If a prospect name is provided, use it. Otherwise ask for prospect details.
