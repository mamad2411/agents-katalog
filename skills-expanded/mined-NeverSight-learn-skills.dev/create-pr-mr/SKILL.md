---
name: create-pr-mr
description: Prepare and create pull requests or merge requests with clear change summaries, affected files, and correct target branches. Use when the user asks to create, open, draft, update, or prepare a PR, pull request, MR, or merge request.
---

# Create PR or MR

## Flow

1. Inspect: `git status --short`, `git branch --show-current`, `git remote -v`, recent commits.
2. Detect host CLI:
   - GitHub: `gh pr create`
   - GitLab: `glab mr create`
   - Missing/unknown: draft title/body and say what could not run.
3. Check existing PR/MR first.
4. Push branch when appropriate.
5. Create concise PR/MR; report URL and any caveats.

## Checks

- Existing review request: `gh pr view --json number,title,url,state` or `glab mr view`.
- If one exists, update or report it. Do not duplicate.
- Ready commits: `git status --short`, `git log --oneline origin/HEAD..HEAD`.
- If `origin/HEAD` missing, infer default branch from remotes/conventions: `main`, `master`, `develop`.

## Branch

- Use current branch unless user named another.
- Avoid PRs/MRs from protected default branches.
- Push: `git push -u origin HEAD`.
- If network/auth fails, stop with exact blocker. Never invent a URL.

## Body

Default:

```md
## Summary
Briefly state what this PR/MR is for in 1-2 sentences.

## Changes
- ...
- ...

## Files affected
- `path/to/file`: ...
- `path/to/other`: ...
```

Add screenshots/links only when real.

Content:

- Title fits change; Conventional Commit style is fine.
- Summary = short purpose/context before the change list.
- Changes = behavior changed.
- Files affected = concise list of touched files or directories and why they changed.
- Do not add `Tests`, `Verification`, or test-run notes to the PR/MR body.
- Bug fix: problem and corrected behavior.
- UI: screenshots only when captured.
- Migration/ops: rollout and rollback notes only if directly part of the change.
- Risks/follow-ups only when useful and directly tied to affected files.

## GitHub

- Create: `gh pr create --base main --head current-branch --title "..." --body "..."`
- Draft: add `--draft` when user asks or work is not review-ready.
- Useful: `gh pr checks`, `gh pr edit --title "..." --body "..."`, `gh pr view --web`.

## GitLab

- Create: `glab mr create --target-branch main --source-branch current-branch --title "..." --description "..."`
- Draft/WIP when user asks or work is not review-ready.
- Useful: `glab mr view`, `glab mr update --title "..." --description "..."`.

## Hygiene

- State URL after creation.
- Say if unrelated local changes remain.
- No force-push, public-branch rebase, or retarget unless user asked.
- Factual title/body. No marketing gloss.
