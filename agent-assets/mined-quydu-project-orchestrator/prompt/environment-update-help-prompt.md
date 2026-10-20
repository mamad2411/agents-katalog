---
mode: agent
description: Explain how to inventory and update existing development tools safely.
---

# Environment Update Help

Read the full contract at `@.github/skills/environment-update/SKILL.md` before using the skill.

Run the skill with `/environment-update`. It updates existing tools only and does not install missing tools.

## Options

- `-WhatIf` inventories installed tools and lists available updates without changing anything. This is the default.
- `-All` selects every detected update after the complete list is displayed.
- A number selects one update from the displayed list.
- `-Tool "name"` narrows the inventory when supported by the host workflow.

The skill lists current version, target version, approved source, privilege requirement, restart requirement, and findings before asking what to update. It requires confirmation before applying each selected update and reports successes, skips, warnings, and errors in `reports/environment-update.json` and `reports/environment-update.md`.
