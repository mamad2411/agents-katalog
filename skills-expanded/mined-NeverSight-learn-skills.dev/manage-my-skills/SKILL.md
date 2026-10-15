---
name: manage-my-skills
description: Manage, update, and install personal agent skills from Derek-X-Wang/skills. Use when the user wants to create, edit, update, or install skills. Handles the full workflow — edit locally, commit, push, then npx skills install.
---

# Manage My Skills

You are the user's skill manager. You help create, edit, and deploy agent skills from the personal skills repo.

## Skills Repo

- **Local path:** `/Users/derekxwang/Development/projects/DXW/tools/skills`
- **Remote:** `https://github.com/Derek-X-Wang/skills`
- **Format:** Each skill is a root-level directory with a `SKILL.md` (follows [Agent Skills Spec](https://agentskills.io/specification))

If the local path does not exist, clone from remote:
```bash
git clone https://github.com/Derek-X-Wang/skills.git /Users/derekxwang/Development/projects/DXW/tools/skills
```

## Target Agents

Always install to these agents:
- `claude-code`
- `windsurf`
- `antigravity`
- `codex`
- `gemini-cli`
- `opencode`

## Commands

Determine the user's intent:

| User says | Action |
|-----------|--------|
| "update skill X", "edit skill X" | Edit an existing skill |
| "create skill X", "new skill X" | Create a new skill |
| "install skill X", "add skill X" | Install a skill locally (skip edit/push) |
| "install all", "sync skills" | Install all skills locally |
| "list skills" | List available skills in the repo |

## Workflow: Edit / Create a Skill

### Step 1: Open the skills repo

1. Check if `/Users/derekxwang/Development/projects/DXW/tools/skills` exists
2. If not, clone from `https://github.com/Derek-X-Wang/skills.git`
3. Run `git pull` to ensure we have the latest

### Step 2: Make changes

- **Edit:** Read the existing `<skill-name>/SKILL.md` (and any `references/`) files, make the requested changes
- **Create:** Create `<skill-name>/SKILL.md` with proper frontmatter:
  ```yaml
  ---
  name: skill-name
  description: What it does and when to use it.
  ---
  ```
  The `name` field must match the directory name. Lowercase, hyphens only.

### Step 3: Commit and push

```bash
cd /Users/derekxwang/Development/projects/DXW/tools/skills
git add <skill-name>/
git commit -m "feat: update <skill-name> skill\n\n<brief description of changes>"
git push
```

Always commit and push so the remote stays in sync. This ensures other devices can pull the latest.

### Step 4: Install locally

After pushing, install the updated skill to all target agents:

```bash
npx skills add Derek-X-Wang/skills --skill <skill-name> -g -y -a claude-code -a windsurf -a antigravity -a codex -a gemini-cli -a opencode
```

Confirm success by checking that the skill directory exists in `~/.claude/skills/<skill-name>/`.

### Step 5: Report

Output:
```
Skill updated: <skill-name>
  Commit: <hash>
  Pushed: github.com/Derek-X-Wang/skills
  Installed to: claude-code, windsurf, antigravity, codex, gemini-cli, opencode

Changes:
- <brief list of what changed>
```

## Workflow: Install Only (no edit)

Skip steps 2-3. Just run:

```bash
npx skills add Derek-X-Wang/skills --skill <skill-name> -g -y -a claude-code -a windsurf -a antigravity -a codex -a gemini-cli -a opencode
```

## Workflow: Install All

```bash
npx skills add Derek-X-Wang/skills -g -y --all -a claude-code -a windsurf -a antigravity -a codex -a gemini-cli -a opencode
```

## Workflow: List Skills

```bash
ls /Users/derekxwang/Development/projects/DXW/tools/skills/*/SKILL.md
```

Or if local not available:
```bash
npx skills add Derek-X-Wang/skills -l
```

## Rules

- Always `git pull` before editing to avoid conflicts
- Always commit and push after changes — the remote is the source of truth
- Use descriptive commit messages following the repo's convention
- The `name` field in SKILL.md frontmatter must exactly match the directory name
- Do not modify skills that are not owned by the user (check for attribution/license)
