---
name: pr
description: "Prepare a PR with context — summary, blast radius, review areas"
category: git
tags: [pull-request, summary, blast-radius]
depends-on: [init, branch]
input: "PR scope (current branch)"
output: ".ccs/pulls/<name>.md + PR creation"
token-estimate: 4000
parallel-safe: true
argument-hint: "[target-branch] [--draft]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-opus-4-6
context: fork
agent: general-purpose
---

# PR

Generate a complete pull request description by analyzing branch changes and calculating blast radius. Saves to `.ccs/pulls/`.

## Steps

### 1. Identify source and target
- Current branch: `git rev-parse --abbrev-ref HEAD`
- Target: user-provided or default `main`/`master`
- Read `.ccs/branches/<current>.md` if exists (regenerate if stale)

### 2. Gather change data
- `git log --oneline <target>..<current>` → commits
- `git diff --stat <target>...<current>` → files changed with line counts
- `git diff --shortstat <target>...<current>` → totals
- `git log --format="%h %s" <target>..<current>` → commit messages

### 3. Analyze impact
- Read `.ccs/file-index.md` → rank changed files
- Read `.ccs/project-map.md` → find downstream dependents
- Read `.ccs/architecture.md` → module boundaries
- Categorize changes: feature, fix, refactor, config, docs

### 4. Identify review areas
- **Must review:** S-rank files, 50+ line changes, shared utilities
- **Should review:** A-rank files, cross-module changes
- **Quick check:** B/C/D-rank files, config, docs

### 5. Generate PR document
Create `.ccs/pulls/<branch-name>.md`: title, summary (2-3 sentences), changes table (file, action, lines, rank, impact), blast radius, commits, review areas, test recommendations.

### 6. Output PR description
Also output a clean, paste-ready PR description: summary, bullet changes, test plan, blast radius.

### 7. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: branch → target, commits count, files changed, blast radius, review areas.

## Rules
- Read branch ref first — it has most context already
- Use `--stat` and `--shortstat` instead of full diffs
- Cap dependency walking at 1 level (direct dependents only)
- For large PRs (50+ files) → summarize top 20 by rank
- Does not create the actual PR on GitHub — outputs description only. Use `gh pr create` to submit.

## Refs
- Branch refs: `.ccs/branches/`
- PR docs: `.ccs/pulls/`
- File index: `.ccs/file-index.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`

---
*codebase-context-skill v2.0.0*
