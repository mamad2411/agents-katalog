---
name: git-autopilot
description: Automatically manages git for all project work. Triggers whenever you create files, edit code, finish a task, work in a project directory, or when git should be initialized. This skill ensures every project has git enabled and commits are made at natural stopping points — the user should never have to think about git. Also triggers when the user mentions commits, version control, saving progress, or git in any way.
---

# Git Autopilot

The user prefers not to manage git manually. Handle all git operations proactively so they never have to think about version control.

## Core Behaviors

### 1. Always ensure git is initialized

When working in any directory under `/home/sabro/projects/`, check if git is set up:

```bash
git -C <project-dir> rev-parse --is-inside-work-tree 2>/dev/null
```

If not initialized:
```bash
cd <project-dir>
git init
git checkout -b main
```

Set the identity if not configured (use the repo-local config, not global):
```bash
git config user.name "brownho"
git config user.email "brownho@users.noreply.github.com"
```

Create a sensible `.gitignore` if one doesn't exist. Include at minimum:
```
node_modules/
.env
*.log
.DS_Store
dist/
```

Make an initial commit with everything that should be tracked:
```bash
git add -A
git commit -m "Initial commit"
```

### 2. Commit at natural stopping points

Make a commit whenever:
- A logical piece of work is finished (feature added, bug fixed, config changed)
- The user is about to move on to something different
- Files have been created or substantially edited
- A task is marked as completed
- The session is wrapping up

Don't batch unrelated changes into one commit. If you did work on two separate things, make two commits.

### 3. Write good commit messages

Follow this format:
- Start with a verb: Add, Fix, Update, Remove, Refactor, Configure
- Keep the first line under 72 characters
- Describe **what changed and why**, not just "updated files"
- Add a blank line and a body paragraph if the change is non-obvious

Examples:
```
Add powerbi-knowledge MCP server configuration

Configure the stdio MCP server to serve the Power BI knowledge
base via Docker with native Node.js fallback.
```

```
Fix wrong MCP script path in install-mcp skill
```

### 4. Stage files thoughtfully

- Use `git add <specific-files>` rather than `git add -A` when possible
- Never commit `.env` files, secrets, credentials, or API keys
- Never commit `node_modules/`, build artifacts, or cache directories
- If in doubt about a file, check `.gitignore` first
- Run `git status --short` before committing to review what's staged

### 5. Push and keep GitHub in sync

After committing, if the repo has a remote configured, push automatically:
```bash
git remote -v 2>/dev/null | grep -q origin && git push origin $(git branch --show-current) 2>/dev/null || true
```

If there's no remote, that's fine — local git history is still valuable.

### 6. Maintain a README.md

Every project under `/home/sabro/projects/` should have a `README.md` at its root. If one doesn't exist, create it after the initial commit.

**When to update the README:**
- After adding a new feature, skill, hook, agent, or MCP server
- After changing the project structure (new directories, renamed files)
- After a significant config change (new slash commands, new plugins)
- At the end of a session if the project changed substantially

**What the README should contain:**
- Project name and one-line description
- What the project does (features, capabilities)
- Directory structure overview (if non-obvious)
- How to install / set up / run
- Available commands, skills, or API endpoints (if applicable)
- Dependencies or prerequisites

**How to update:**
- Read the current README first
- Only update sections that are stale or missing — don't rewrite the whole file
- Keep it concise — the README is a quick reference, not a novel
- Match the existing style and tone

### 7. Handle existing dirty state

If you start a session and find uncommitted changes from a previous session:
1. Run `git status --short` and `git diff --stat` to understand what changed
2. If the changes look intentional, commit them with a descriptive message
3. If they look like leftover junk (temp files, test outputs), ask the user before committing

### 8. Use branches for risky work

If you're about to make a big change that might not work out (refactoring, experimental features), create a branch first:
```bash
git checkout -b <descriptive-branch-name>
```

This way the user can always get back to a known-good state. Merge back to main when the work is confirmed good.

## What NOT to do

- Don't amend commits unless the user asks — amending rewrites history and can lose work
- Don't force push — ever
- Don't rebase without asking
- Don't delete branches without asking
- Don't run `git reset --hard` — if something needs undoing, use `git revert`
- Don't spam `pm2 restart` or other service commands while doing git work
