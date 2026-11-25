---
name: branch
description: "Create or switch branches with auto-generated context refs"
category: git
tags: [branch, switch, context-ref]
depends-on: [init]
input: "branch name or operation"
output: ".ccs/branches/<name>.md context reference"
token-estimate: 2000
parallel-safe: false
argument-hint: "[create branch-name \"purpose\"] | [branch-name] | [list] | [clean]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-sonnet-4-6
context: fork
agent: general-purpose
---

# Branch

Create or switch branches while maintaining context reference files in `.ccs/branches/`.

## Steps

### 1. Detect intent
Parse input:
- `create <name> "<purpose>"` → create new branch
- `<name>` or `switch <name>` → switch to branch
- `list` → show all branches with ref status
- `clean` → remove stale refs for deleted branches

### 2. Load context
- Read `.ccs/file-index.md` for dependency impact analysis
- Glob `.ccs/branches/*.md` for existing branch refs
- Run `git branch -a` for current branch state

### 3. Execute

**Create:**
1. Record parent branch, then `git checkout -b <name>`
2. Record merge-base: `git merge-base HEAD <parent>`
3. Create `.ccs/branches/` if needed
4. Generate `.ccs/branches/<name>.md`: parent, created date, status, purpose, empty files/commits/deps sections

**Switch:**
1. If `.ccs/branches/<name>.md` exists → read and display summary
2. If missing → generate from git state (`git log`, `git diff --stat` vs main)
3. Run `git checkout <name>`

**List:**
1. `git branch -a` + check each for `.ccs/branches/<name>.md`
2. Display: branch name, has ref (yes/no), last commit, status

**Clean:**
1. Compare active branches (`git branch`) with `.ccs/branches/*.md`
2. Delete refs where branch no longer exists

### 4. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: action, branch, parent, purpose, ref file path.

## Rules
- Read branch ref FIRST before exploring source files
- Never re-scan codebase to understand a branch — the ref has context
- Keep branch refs under 100 lines
- Does not push → use `/ccs-sync push`
- Does not create PRs → use `/ccs-pr`

## Refs
- Branch refs: `.ccs/branches/`
- File index: `.ccs/file-index.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`

---
*codebase-context-skill v2.0.0*
