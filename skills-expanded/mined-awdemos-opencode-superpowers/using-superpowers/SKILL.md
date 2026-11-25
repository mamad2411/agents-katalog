---
name: using-superpowers
description: MANDATORY — Read this skill FIRST at the start of EVERY conversation before any response or action
---

# Using Superpowers

If you were dispatched as a subagent to execute a specific task, skip this skill.

## Rule

Invoke the relevant Superpowers skill(s) **before any response or action**. If there is even a small chance a skill applies, use it.

User instructions always override skills.

## Workflow map

| Situation | Skill |
|-----------|-------|
| New feature / design / creative work | `brainstorming` |
| Approved design, need implementation plan | `writing-plans` |
| Plan exists, run it in this session | `subagent-driven-development` |
| Plan exists, run it in fresh parallel sessions | `executing-plans` |
| Writing or fixing code with tests first | `test-driven-development` |
| Bug, error, unexpected behavior | `systematic-debugging` |
| Between tasks / implementation complete | `requesting-code-review` |
| Ready to finish | `verification-before-completion` then `finishing-a-development-branch` |
| Isolated workspace needed | `using-git-worktrees` |
| Writing a new skill | `writing-skills` |

## How to invoke

Use the OpenCode `skill` tool: `skill({ name: "brainstorming" })` etc.

## Tool mapping

- `TodoWrite` → `todowrite`
- Subagent → `task` with `subagent_type: "general"`
- `Skill` → `skill`
- Read → `read`
- Edit → `apply_patch`
- Bash → `bash`
- Search → `grep`, `glob`
- Fetch → `webfetch`
