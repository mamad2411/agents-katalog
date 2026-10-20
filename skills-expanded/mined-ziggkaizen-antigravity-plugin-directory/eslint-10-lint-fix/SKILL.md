---
name: eslint-10-lint-fix
description: Triages ESLint 10 lint failures and applies safe, targeted fixes. Use when lint commands fail, agents propose eslint --fix, disable comments need review, or CI lint behavior needs hardening.
---

# ESLint 10 Lint Fix

Use this skill for lint failure triage and controlled fixes.

## Process

1. Reproduce lint failures with the smallest safe command.
2. Separate config/runtime failures from source-code lint findings.
3. Prefer source fixes over disable comments.
4. Use `--fix-dry-run` before broad fixes when possible.
5. Use targeted file paths for auto-fix commands.
6. Review diffs after any fix command.
7. Do not mix lint fixes with unrelated refactors.

## Helper Scripts

```powershell
node .\.agents\plugins\eslint-10\skills\eslint-10-lint-fix\scripts\eslint-disable-audit.mjs --help
node .\.agents\plugins\eslint-10\skills\eslint-10-lint-fix\scripts\eslint-command-guard.mjs --help
```

## Workflows

- `workflows/lint-failure-triage-workflow.md`
- `workflows/safe-fix-workflow.md`
- `workflows/ci-lint-hardening-workflow.md`

## Resource

- `resources/disable-comment-audit-checklist.md`
