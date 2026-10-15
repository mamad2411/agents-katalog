---
name: private-skills
description: |
  Manage all private git-backed skills in ~/.claude/skills/.
  Auto-discovers skills with .git directories — no hardcoded list.
  Supports list, status, push, pull, install, and publish commands.
  Triggers on: "private skills", "list skills", "push skills",
  "pull skills", "install skills", "publish skill", "skill status", "sync skills".
user_invocable: true
argument-hint: "<list|status|push|pull|install|publish> [skill_name]"
---

# private-skills

Manage all private git-backed skills using the script at `scripts/private-skills.sh` (relative to this skill's directory).

## Commands

### List all git-backed skills

```bash
bash "SCRIPT_PATH" list
```

Shows each git-backed skill with: name, remote URL, clean/dirty status, last commit date and message.

### Show detailed status

```bash
bash "SCRIPT_PATH" status
```

Shows `git status` output for each git-backed skill (changed files, ahead/behind remote).

### Push changes

```bash
bash "SCRIPT_PATH" push [skill_name]
```

If `skill_name` is given, push only that skill. Otherwise push all dirty skills.
Runs: `git add -A && git commit -m "Update <name>" && git push`.

### Pull latest

```bash
bash "SCRIPT_PATH" pull [skill_name]
```

If `skill_name` is given, pull only that skill. Otherwise pull all git-backed skills.
Runs: `git pull --rebase`.

### Install skill repos from GitHub

```bash
bash "SCRIPT_PATH" install [skill_name]
```

Clones skill repos from the authenticated GitHub user's account into the skills directory.
If `skill_name` is given, install just that one. Otherwise scans all user repos for ones containing `SKILL.md` and clones any not already present.

### Publish a new skill

```bash
bash "SCRIPT_PATH" publish <skill_name>
```

For a plain (non-git) skill directory: initializes git, commits all files, and creates a private GitHub repo under your GitHub account using `gh repo create`.

## Instructions

1. Resolve the script path: `SCRIPT_PATH` is `<this_skill_dir>/scripts/private-skills.sh` where `<this_skill_dir>` is the directory containing this SKILL.md.
2. Parse the user's request to determine the command and optional skill name.
3. Run the appropriate bash command above, substituting the resolved script path.
4. Present the output cleanly to the user.

## Prerequisites

- `gh` CLI authenticated (`gh auth login`)
- Git configured with push access to EFFYLYX repos
