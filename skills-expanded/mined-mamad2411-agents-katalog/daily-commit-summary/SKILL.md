---
name: daily-commit-summary
description: Generate daily task summaries by analyzing git commits. MUST include analyzed Tasks section.
---

# Daily Commit Summary Skill

Generate a daily task summary by analyzing git commits and rewriting them into clear, human-readable task descriptions.

## When to Use This Skill

- "What did I do today?"
- "Summarize my commits"
- "Daily commit summary"
- "/daily-commit-summary"

## Configuration

`~/.daily-commit-summary.yaml`:

```yaml
repositories:
  - ~/projects/portal-api
  - ~/projects/portal-frontend
work_hours:
  start: "08:00"
  end: "18:00"
author: "your.email@example.com"
```

---

## 🚨 CRITICAL: EXECUTION STEPS (MUST FOLLOW IN ORDER)

**STEP 1: Collect commits** → Run git log commands for each repository

**STEP 2: TRANSFORM commits to tasks** → This is MANDATORY, not optional!
- Take each commit message
- Rewrite it as a human-readable task sentence
- Use action verbs: Fixed, Implemented, Updated, etc.

**STEP 3: Output with Tasks FIRST** → Tasks section must appear before commit details

---

## ⚠️ MANDATORY OUTPUT REQUIREMENTS

**YOU MUST ALWAYS INCLUDE THE "Summary Task Daily" SECTION.**

This section analyzes raw commits and rewrites them as clear task sentences. This is the PRIMARY purpose of this skill - not just listing commits.

**DO NOT just dump raw commits. TRANSFORM them into task sentences.**

---

## Required Output Format

```
📋 Daily Commit Summary
Date: [Day], [Month] [Date], [Year] (08:00 - now)

---

Summary Task Daily

- [Transformed task sentence 1]
- [Transformed task sentence 2]

---

[Rest of commit details...]
```

---

## Example

**Input (raw commits):**
```
b0b0352 fix(notification-template): update mock Thai name to include month
551c5ef chore: update gitignore and mock data
f344b80 []
```

**Required Output:**

```
📋 Daily Commit Summary
Date: Saturday, March 21, 2026 (08:00 - now)

---

Summary Task Daily

- Fixed notification template to correctly display Thai month names in mock data
- Updated project configuration files (gitignore) and mock data for testing

---

📊 Commits Detail

backoffice-portal-next (3 commits)

🔧 fix
- b0b0352 fix(notification-template): update mock Thai name to include month

🔨 chore
- 551c5ef chore: update gitignore and mock data

❓ other
- f344b80 []

Other Repositories

| Repository | Commits |
|------------|---------|
| portal-uam | 0 |
| portal-cube | 0 |
| portal-backend | 0 |
| portal-backend-cms | 0 |

Total: 3 commits today 🎉
```

---

## 🔄 TRANSFORMATION RULES (STEP 2)

Parse commits using Conventional Commits format: `<type>(<scope>): <description>`

Reference: #[[file:commit/SKILL.md]]

For EACH commit, you MUST transform it like this:

| Raw Commit | → | Transformed Task |
|------------|---|------------------|
| `feat(auth): add login with Google` | → | Implemented Google login authentication |
| `fix(cart): resolve quantity update issue` | → | Fixed cart quantity update issue |
| `fix(notification-template): update mock Thai name to include month` | → | Fixed notification template to correctly display Thai month names in mock data |
| `chore: update gitignore and mock data` | → | Updated project configuration files (gitignore) and mock data for testing |
| `refactor(api): simplify error handling` | → | Refactored API error handling for better maintainability |
| `perf(query): optimize database lookup` | → | Optimized database query lookup performance |
| `test(auth): add login unit tests` | → | Added unit tests for login authentication |
| `docs(readme): update installation steps` | → | Updated README installation documentation |
| `build(deps): upgrade react to v19` | → | Upgraded React dependency to version 19 |
| `ci(github): add deploy workflow` | → | Configured GitHub Actions deploy workflow |

### Task Writing Rules

1. **Start with action verb**: Fixed, Implemented, Updated, Refactored, Added
2. **Be descriptive**: Expand abbreviations, add context
3. **Human-readable**: Write for standup reports
4. **Group related**: Combine multiple commits about same feature
5. **Skip empty**: Don't include WIP/empty commits like `[]` as tasks

### Grouping Example

**Multiple related commits:**
```
feat(auth): add login page
feat(auth): add password validation  
fix(auth): resolve token issue
```

**→ ONE analyzed task:**
```
- Implemented user authentication system with login page and password validation
```

---

## Commit Type → Task Language

Reference: Uses Conventional Commits format from #[[file:commit/SKILL.md]]

| Type       | Description                                          | Task Action Words                    |
| ---------- | ---------------------------------------------------- | ------------------------------------ |
| `feat`     | New feature or functionality                         | Implemented, Added, Created          |
| `fix`      | Bug fix                                              | Fixed, Resolved, Corrected           |
| `docs`     | Documentation changes only                           | Updated documentation, Documented    |
| `style`    | Code style (formatting, semicolons, no logic change) | Fixed styling, Improved formatting   |
| `refactor` | Code change that neither fixes bug nor adds feature  | Refactored, Restructured, Improved   |
| `perf`     | Performance improvement                              | Optimized, Improved performance      |
| `test`     | Adding or updating tests                             | Added tests for, Improved test coverage |
| `build`    | Build system or external dependencies                | Updated build, Upgraded dependencies |
| `ci`       | CI/CD configuration changes                          | Updated CI/CD, Configured pipeline   |
| `chore`    | Other changes (tooling, configs)                     | Updated, Maintained, Cleaned up      |
| `revert`   | Revert a previous commit                             | Reverted, Rolled back                |

---

## Checklist Before Responding

Before showing output, verify:

- [ ] "Summary Task Daily" section is present at the TOP (after date)
- [ ] Tasks are TRANSFORMED (not raw commit messages)
- [ ] Tasks use clear action verbs (Fixed, Implemented, Updated, etc.)
- [ ] Related commits are grouped into single tasks
- [ ] Empty/WIP commits like `[]` are excluded from tasks

**🚫 WRONG OUTPUT (just dumping commits):**
```
📊 Daily Commit Summary
b0b0352 fix(notification-template): update mock Thai name to include month
```

**✅ CORRECT OUTPUT (transformed to tasks):**
```
📋 Daily Commit Summary
Date: Saturday, March 21, 2026

Summary Task Daily
- Fixed notification template to correctly display Thai month names in mock data
```

**If the "Summary Task Daily" section is missing or contains raw commits, the output is WRONG.**
