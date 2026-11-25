---
name: permission-manager
description: 'Manage opencode permissions: review always-allow lists, suggest safe
  read-only commands, configure permission patterns'
risk: critical
license: MIT
---

## What I do
- Review and summarize currently always-allowed commands
- Suggest safe read-only commands for auto-approval
- Add or remove commands from the allow list in opencode.json
- Configure skill-level permissions (allow/deny/ask) with wildcard patterns
- Audit permission configs for security and usability

## When to use me
Use this when optimizing opencode's permission settings, reviewing allowed commands, or configuring skill access controls.

## Workflow Steps

1. **Read current config**: Load `~/.config/opencode/opencode.json` or project-level `opencode.json`
2. **Summarize permissions**: Identify currently allowed commands and skill permissions
3. **Suggest additions**: Propose safe read-only commands for auto-allow (see recommended list below)
4. **Apply changes**: Edit the config to add/remove permission entries
5. **Validate**: Ensure JSON is valid after changes

Complements opencode's built-in allow/deny/ask permissions by auditing current config and recommending adjustments through conversation.

## Key Rules
- Never allow commands that modify files, commit, push, or change system state
- Use wildcards appropriately (e.g., `git status*` not just `git status`)
- Confirm with user before modifying permission config
- Distinguish between bash command permissions and skill permissions
- Keep config organized: group related commands together

## How to trigger me

Use the Task tool with the `permission-manager` subagent type:

```
/permissions
```

Or in natural language, ask opencode to "manage opencode permissions" or "review allowed commands".
