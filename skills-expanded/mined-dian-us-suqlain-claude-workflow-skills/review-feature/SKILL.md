---
name: review-feature
description: Review a finished change before it is handed over. Runs the built-in /code-review first, then checks the change against its spec and plan, a general checklist and the project's own rules (docs/review-checklist.md); verifies each finding, fixes the confirmed ones, and writes a review report. Use after test-feature passes (the review step of the spec, plan, implement, test, review workflow), or when asked to "review this" or "review the changes".
argument-hint: "[task-name] [base-ref]"
allowed-tools: Bash(git status *) Bash(git log *) Bash(git branch *) Bash(git diff *) Bash(git merge-base *)
---

# Review the feature

Invoked as `/dev-workflow:review-feature` when installed as a plugin, or `/review-feature` if the folder is copied into `~/.claude/skills/`.

Goal: what reaches the user for their live test is correct, safe, matches what was approved, and leaves the project in good shape.

## Context
- Status: !`git status --short 2>/dev/null | head -40 || true`
- Branch and recent commits: !`git branch --show-current 2>/dev/null; git log --oneline -10 2>/dev/null || true`
- Default branch candidates: !`git branch --list main master trunk develop 2>/dev/null || true`
- Project rules present: !`ls docs/review-checklist.md docs/specs docs/implementation 2>/dev/null || true`

## Steps

0. **Find the project root.** The context lines above describe the folder Claude was started in, which may not be the project the task lives in (for example a fork or a parent folder). If the argument or the task's docs are in another folder, go there and re-check `git status`, `git log --oneline -5` and the project files before going on. Treat the context lines as hints only.
1. **Scope.** The base is the second argument, else the merge base with the default branch (`git merge-base HEAD <default>`), else the uncommitted changes. Review `git diff <base>` plus untracked files (`git status --short`). List the changed files with one line each on what changed.
2. **Intent.** Read the task's spec (`docs/specs/<task>.md`) and plan (`docs/implementation/<task>/`) when they exist. The task is the first argument, else the newest folder in `docs/implementation/`.
3. **First pass:** run the built-in code review on the same scope (the `code-review` skill, at its default level). Keep its findings for step 5. If the scope is documents only (no code changed), skip it and write "not run: no code" in the report.
4. **Second pass:** open and read [checklist.md](checklist.md) now (don't work from memory), go through it, then `docs/review-checklist.md` if the project has one, item by item. Read the changed code in context: the whole function, its callers, and the tests. Mark each item ok, finding #n, or not applicable.
5. **Verify every finding** before it counts. Trace the code path, or reproduce it with a small test or command. A finding you can't confirm is dropped, or listed as "plausible" with what would confirm it.
6. **Fix the confirmed findings** in the working tree:
   - small, matching the surrounding code's naming, comments and idioms;
   - add or adjust a test when the project has tests for that area;
   - a finding that needs a design or product decision is **not** fixed: list it for the user.
7. **Report:** write `docs/implementation/<task>/review-report.md` (format below). If anything was changed, say that `test-feature` must run again, and run it if the user has asked for the whole flow.

## Severity
- **Blocker:** crash, data loss, a privacy or security breach, wrong numbers or money shown, or the spec not met.
- **Major:** wrong behaviour in a realistic case, or a missing error path on the main flow.
- **Minor:** an edge case, unclear or duplicated code, a missing test.
- **Note:** wording, naming or docs.

## Rules
- Don't commit or push.
- Never weaken, skip or delete a test to make the change pass.
- Don't widen the scope: problems in code the change didn't touch go under "Seen nearby" and aren't fixed.
- Never print secrets; redact them in quoted code.

## Report format

```markdown
# Review: <task>
<date> · <base>..<head or "working tree"> · <n> files

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| 1 | Major | `path/file.swift:120` | ... | Fixed (test added) / Left: needs your decision / Plausible |

**Verdict:** ready for testing / ready after the fixes above (re-test needed) / not ready: <why>

## Checklist
- <item>: ok / #n / n/a

## Built-in code review
<its findings, and what happened to each>

## Seen nearby (not changed)
```
