---
name: safe-commit
description: Standardized safe git commit workflow. Use when the user asks to commit code,提交代码, git commit, 提交到仓库, or when preparing a commit after implementation. Enforces branch baseline check, Chinese-only commit messages, and exclusion of non-business planning files.
---

# Safe Commit

This skill standardizes git commit behavior for everyday implementation work.

## Purpose

Prevent unsafe or low-quality commits by enforcing:

1. Branch baseline check
2. Chinese-only commit messages
3. Exclusion of plan/process files unrelated to business implementation

## Workflow

### Step 1: Check branch baseline

Before committing:

- If the project has a release baseline rule (for example `release/1.0.X`), verify the current working branch is based on the latest release branch.
- Do not rely only on local branch refs. If matching `release/1.0.X` refs are not visible locally or in already-fetched remote refs, explicitly check remote heads first (for example `git ls-remote --heads origin "release/1.0.*"`) or fetch the release refs before deciding that no baseline exists.
- If it is behind, stop and tell the user that the branch must be updated before committing.
- Do not guess the release branch name. Use project rules such as `AGENTS.md`.
- Generate a short branch-diff summary against the target release baseline (for example: ahead/behind commit count, or a concise list of unique commits/files) and show it to the user before committing.
- If the remote check still cannot identify a unique baseline branch, stop and ask the user instead of proceeding with a guessed baseline.

### Step 2: Check commit scope

Run git status and separate files into:

- Business implementation files
- Test/config files required by the implementation
- Pre-existing unrelated changes
- Plan/process artifacts

Default exclusions:

- `task_plan.md`
- `findings.md`
- `progress.md`
- `*.plan.md`
- other planning or temporary process files

Only include excluded files if the user explicitly requests it.

### Step 3: Draft commit message

Rules:

- Commit message must be Chinese only
- Describe only the current change content
- Do not mix unrelated topics in one commit message

Use this 3-part template when helpful:

```text
<中文动词><对象>

<为什么这次修改有必要>
```

### Step 4: Final confirmation behavior

Before actually committing, present:

- current branch
- branch baseline result
- branch diff summary against `release/1.0.X`
- file list to be committed
- excluded plan/process files
- proposed Chinese commit message

If anything is ambiguous, ask before committing.

## Output Template

```markdown
## 提交检查

- 当前分支: ...
- 基线检查: 通过 / 未通过
- 相对 release 基线差异摘要: ...
- 纳入提交: [...]
- 默认排除: [...]
- commit 信息: ...
```

## Hard Rules

- Never commit on the wrong branch without user approval
- Never include planning/process files by default
- Never write the commit message in English unless explicitly requested
- Never hide pre-existing unrelated changes
