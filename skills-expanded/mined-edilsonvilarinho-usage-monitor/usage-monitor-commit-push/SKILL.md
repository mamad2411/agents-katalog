---
name: usage-monitor-commit-push
description: Safely stage, commit, and push intended changes in the usage-monitor repository with the repo's required temporary git identity, narrow verification, never touching the original author config. Use when Codex needs to commit or push local changes for this project, especially when unrelated files may exist or the user explicitly asks to publish work.
---

# Usage Monitor Commit Push

Commit only the intended files with a temporary agent git identity, passed per command and never written to the git config.

## Workflow

1. Read [AGENTS.md](../../../AGENTS.md) and [README.md](../../../README.md) first.
2. Continue only after the user explicitly asks to commit, push, or publish changes.
3. Inspect repository state with:
   - `git status --short --branch`
   - `git branch --show-current`
   - `git remote -v`
   - `git diff --stat`
   - `git diff --cached --stat`
4. Stage only explicit file paths. Never use broad staging such as `git add .` when unrelated changes may exist.
5. Choose the narrowest relevant verification before the commit:
   - Docs-only changes: inspect the diff for coherence.
   - Kotlin, UI, history, lifecycle, or repository changes: run `gradlew.bat allTests` or a narrower relevant test target.
   - Installer or packaging changes: run `gradlew.bat packageInstaller` when the installer behavior is part of the change.
6. Prefer the bundled script `scripts/commit_and_push.ps1` for the actual commit and push.
7. Report the branch, commit hash, push result, and final `git status --short --branch`.

## Script

Use the bundled PowerShell helper to stage only the requested files, commit with the temporary git identity, and optionally skip the push. It works in the main checkout and in a worktree.

Example:

```powershell
powershell -ExecutionPolicy Bypass -File `
  .codex\skills\usage-monitor-commit-push\scripts\commit_and_push.ps1 `
  -RepoPath C:\Users\edils\workspace\usage-monitor `
  -Message "docs: sync README with current architecture and workflows" `
  -Files README.md `
  -TempUserName codex `
  -TempUserEmail codex@openai.com
```

Use `-SkipPush` when the user asked only for a local commit. Use `-DryRun` to preview the staging plan without touching the index.

The identity goes as `git -c user.name=… -c user.email=… commit` (#498): nothing is written to the config, so nothing is left behind if the commit, the push or the process fails, and a worktree (where `.git` is a file) works the same. Tests: `pwsh -NoProfile -Command "Invoke-Pester -Path .claude/skills/usage-monitor-commit-push/scripts -Output Detailed"`.

## Guardrails

- Do not commit or push without explicit user approval in the current conversation.
- Do not stage unrelated changes.
- Do not force-push unless the user explicitly asks for it.
- Keep commit messages focused on the actual change scope.
- Do not modify another agent's uncommitted work in order to make a verification pass. Stop and report instead.
