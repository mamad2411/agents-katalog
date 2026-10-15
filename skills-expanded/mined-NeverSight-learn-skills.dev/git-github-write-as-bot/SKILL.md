---
name: git-github-write-as-bot
description: MUST use before git commits, git commit rewrites, gh write commands, or GitHub MCP write actions so agent-authored git and GitHub writes use the bot identity instead of a human or machine default.
---

# Git and GitHub Write As Bot

## Overview

All agent-authored git and GitHub writes must use the bot identity.

## Trigger Requirement

This skill is mandatory before:

- `git commit`
- `git commit --amend`
- `git rebase --continue`
- `gh` write commands
- GitHub MCP write actions

## Rules

### Git commit

Use command-scoped git config:

```bash
git -c user.name="zhangyu1818-bot" -c user.email="zhangyu1818-bot@qq.com" commit -m "..."
```

For `git commit --amend`, add `--reset-author` if the current commit author is not already the bot.

### `gh` writes

Use:

```bash
GH_TOKEN="$GITHUB_BOT_TOKEN" gh <command>
```

### Plain `git push`

First set up git's GitHub credential helper with the bot token:

```bash
GH_TOKEN="$GITHUB_BOT_TOKEN" gh auth setup-git
```

Then push with the same token in the command environment:

```bash
GH_TOKEN="$GITHUB_BOT_TOKEN" git push
```

### GitHub MCP writes

Before any GitHub MCP write:

- call `get_me`
- expected login: `zhangyu1818-bot`
- if not matched, stop

## Do Not

- do not rely on machine-default git config
- do not write to GitHub as a human account
- do not change repo or global git config unless the user explicitly asks
