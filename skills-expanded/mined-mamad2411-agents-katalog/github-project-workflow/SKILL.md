---
name: github-project-workflow
description: Use when the user assigns a task, requests a feature, reports a bug, or plans work that should be tracked before implementation begins
---

# GitHub Project Workflow

## Overview

Issue-first workflow: create a GitHub Issue and link it to the user's Project board before writing any code.

**Status note:** Each Project has its own workflow for setting status when items are added. The default may be "TODO", "In progress", or no status depending on the Project configuration. Closing an Issue (via commit or manually) typically moves it to "Done" if the Project workflow is configured. No manual status updates needed in most cases.

**Core principle:** No Issue, no code.

## When to Use

- User assigns a task, feature, bugfix, or TODO
- Any non-trivial work (> 2 minutes)

**Skip when:**
- One-line fixes (typo, formatting)
- Pure questions with no implementation
- No remote repository
- User declined Project integration

## Setup (First Time Only)

```bash
gh --version          # verify installed
gh auth status        # verify logged in
gh project list --owner @me
```

Ask: "Which Project for task tracking?" Save choice:

```bash
mkdir -p ~/.claude/skills/github-project-workflow
cat > ~/.claude/skills/github-project-workflow/config <<'EOF'
PROJECT_NUMBER=2
PROJECT_OWNER=@me
PROJECT_ENABLED=true
EOF
```

On subsequent runs, read config. If `PROJECT_ENABLED=false`, skip Project linking.

## Workflow

### 1. Create Issue (BEFORE code)

```bash
# Try creating with label. If label does not exist, create it first.
gh issue create \
  --title "[Feature] Brief description" \
  --body "$(cat <<'EOF'
## 实现目标
一句话说明要做什么
## 实现内容
- [ ] 子任务1
- [ ] 子任务2
## 验收标准
- [ ] 标准1
- [ ] 标准2
EOF
)" \
  --label "enhancement" 2>/dev/null || (
    gh label create enhancement --color a2eeef 2>/dev/null || true
    gh issue create \
      --title "[Feature] Brief description" \
      --body "$(cat <<'EOF'
## 实现目标
一句话说明要做什么
## 实现内容
- [ ] 子任务1
- [ ] 子任务2
## 验收标准
- [ ] 标准1
- [ ] 标准2
EOF
      )" \
      --label "enhancement"
  )
```

**Title format:** `[Phase X] Name` / `[Feature] Name` / `[Bug] Description`
**Required body sections:** `## 实现目标`, `## 实现内容`, `## 验收标准`
**Labels:** `enhancement` (features), `bug` (fixes), `question`, `documentation`

### 2. Link to Project (If enabled)

```bash
gh project item-add {PROJECT_NUMBER} --owner {PROJECT_OWNER} --url "{issue_url}"
```

Status is set according to the Project's configured workflow (commonly "TODO" or "In progress").

### 3. Implement and Commit

```bash
git commit -m "Add feature Closes #12"
```

Use `Closes #N` / `Fixes #N` to auto-close on merge. Use `Refs #N` to reference without closing.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Coding before Issue | Stop. Create Issue first. Delete code written without one. |
| Missing checklists | Always include `## 验收标准` with `- [ ]` |
| Commit without Issue ref | Amend or ensure next commit references it |
| Wrong label | `enhancement` for features, `bug` for fixes |
| Manual status updates | Let Project auto-workflow handle it. See @status-control.md if override is needed. |
| `gh issue edit -f` for Status | **Does not exist.** Status is a Project field. |
