---
name: github-tool
description: >-
  GitHub integration tool. Fetches and creates issues and PRs via the gh CLI.
  Use when: Use when: you need to create or list issues and PRs, perform repository operations, or check tasks on GitHub.
tags: [development, github, external]
---


# GitHub Tool

An external tool that operates GitHub issues and PRs via the gh CLI.

## How to Invoke

**Bash**: Run with `animaworks-tool github <サブコマンド> [引数]`

## List of Actions

### list_issues — List Issues
```bash
animaworks-tool github issues [--repo OWNER/REPO] [--state open] [--limit 20]
```

### create_issue — Create Issue
```bash
animaworks-tool github create-issue --title TITLE --body BODY [--labels LABELS]
```

### list_prs — List PRs
```bash
animaworks-tool github prs [--repo OWNER/REPO] [--state open] [--limit 20]
```

### create_pr — Create PR
```bash
animaworks-tool github create-pr --title TITLE --body BODY --head BRANCH [--base main]
```
- `draft` (optional, default: false): Whether to create as a draft PR

## CLI Usage

```bash
animaworks-tool github issues [--repo OWNER/REPO] [--state open] [--limit 20]
animaworks-tool github create-issue --title TITLE --body BODY [--labels LABELS]
animaworks-tool github prs [--repo OWNER/REPO] [--state open] [--limit 20]
animaworks-tool github create-pr --title TITLE --body BODY --head BRANCH [--base main]
```

## Notes

- The gh CLI must be installed and authenticated
- If --repo is omitted, the repository in the current directory is used
