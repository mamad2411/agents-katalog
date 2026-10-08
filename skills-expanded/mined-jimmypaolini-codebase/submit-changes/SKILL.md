---
name: submit-changes
description: Automatically submit local changes through the full branch → commit → push → pull request pipeline. Includes branch-name conformance checks and automatic branch rename when needed. Use this skill when asked to submit, ship, or push changes; when you want to move from local changes to an open PR in one step; or when orchestrating the complete git workflow automatically without manual steps.
license: MIT
---

# Submit Changes

This skill automates the full pipeline from local changes to an open pull request: **branch → commit → push → PR**. Each phase is idempotent — already-completed steps are skipped automatically.

## When to Use This Skill

- Submitting local changes as a complete workflow in one step
- Automating the branch + commit + PR process without manual intervention
- Shipping finished work without manually running each git command

## Safety Rules

These rules are non-negotiable:

- **NEVER** run destructive commands (`git reset`, `git clean`, `git checkout -- .`, `git push --force`, `git rebase`)
- **NEVER** bypass hooks with `--no-verify`
- **NEVER** disable signing with `--no-gpg-sign`
- **NEVER** auto-fix pre-commit failures — report the failure and stop
- On any failure: **report the error and stop immediately**

## Automatic Change Analysis

Before executing any phases, analyze the working tree and staged changes:

```bash
git status --porcelain
git diff HEAD
```

From the diff, automatically determine:

1. **Type** — From the allowed types (see [commit-code skill](../commit-code/SKILL.md))
2. **Scope** — From the allowed scopes (see [commit-code skill](../commit-code/SKILL.md))
3. **Gitmoji** — Best-fit emoji for the type and intent (see [commit-code skill](../commit-code/SKILL.md))
4. **Subject** — Concise imperative phrase, lowercase, no period, under 70 chars

These values drive the branch name, commit message, and PR title throughout all phases.

## Phase 1 — Branch

1. Check current branch: `git rev-parse --abbrev-ref HEAD`
2. If on `main`, create and switch to a new branch following [checkout-branch conventions](../checkout-branch/SKILL.md):

   ```bash
   git checkout -b <type>/<scope>-<description>
   ```

3. Validate branch-name conformance for the current branch:

   ```bash
   pnpm exec validate-branch-name -t "<branch>"
   ```

4. If validation fails, run the [rename-branch skill](../rename-branch/SKILL.md) to derive and apply a compliant branch name, then re-run validation.
5. Push to remote and set upstream:

   ```bash
   git push --set-upstream origin <branch>
   ```

Branch name format: `<type>/<scope>-<description>` (kebab-case, 2–4 keyword description)

## Phase 2 — Stage, Commit & Push

**Skip if:** Working tree is clean (`git status --porcelain` returns nothing).

1. Stage all changes:

   ```bash
   git add -A
   ```

2. Compose commit message: `<type>(<scope>): <gitmoji> <subject>` — single line, max 128 chars, no body/footer

3. Commit with signing enabled:

   ```bash
   export GPG_TTY="$(tty)"
   git commit -S -m "<type>(<scope>): <gitmoji> <subject>"
   ```

4. Verify the new commit signature:

   ```bash
   git verify-commit HEAD
   ```

> ✅ **Best practice:** Let Husky run signing checks automatically. The pre-commit hook runs `check-commit-signing-configuration.sh`, and the pre-push hook runs `check-push-commit-signatures.sh`.
>
> ⚠️ **Warning:** Do not invoke `scripts/git/check-push-commit-signatures.sh` directly during normal submits. It is designed for hook stdin input and can block or fail when run without ref-update data.

### If pre-commit hooks fail

**Stop immediately.** Report the hook output so the user can see what failed. Do **NOT** apply fixes or proceed to push.

### If commit succeeds

Push to remote:

```bash
git push --set-upstream origin <branch>
```

## Phase 3 — Pull Request

**Skip if:** A PR already exists for the current branch:

```bash
gh pr list --head <branch> --state open
```

1. Title: Same format as the commit message — `<type>(<scope>): <gitmoji> <subject>`
2. Body: Auto-generate from the diff using the PR template structure:
   - **🌰 Summary**: Overall purpose in 1-2 sentences
   - **📝 Details**: Bulleted list of meaningful changes
   - **🧪 Testing**: Relevant `nx run <project>:<target>` commands and manual steps
   - **🔗 Related**: Issue links discovered from branch name, commits, or `gh issue list --search`
3. Assignee and labels — Validate Conventions rejects a pull request whose metadata disagrees with its title, so set all of this at creation time rather than waiting for the reconciliation step to backfill it:
   - **Assignee**: `--assignee @me`. A pull request with no assignee fails validation.
   - **Type label**: Exactly one `type:*` label, matching the title's type. Never more than one, never a mismatch.
   - **Scope label(s)**: One `scope:*` label per scope named in the title — if the title carries more than one scope (`type(scope-one,scope-two): …`), add a `--label scope:<name>` for each of them, and no extra `scope:*` label beyond what the title names.
   - **Source label**: Exactly one `source:*` label. This skill is agent-driven, so use `source:agent` — never `source:human`, and never both.
   - **Never** apply `do-not-merge` — it blocks the pull request while present, and this workflow is opening one for immediate review, not staging a draft.
4. Create the PR:

   ```bash
   gh pr create \
     --title "<type>(<scope>): <gitmoji> <subject>" \
     --body "<generated body>" \
     --base main \
     --assignee @me \
     --label type:<type> \
     --label scope:<scope> \
     --label source:agent
   ```

   Repeat `--label scope:<name>` for each additional scope the title names.

5. Confirm the metadata actually landed — a label GitHub silently drops (typo, not-yet-created) fails CI just as surely as never adding it:

   ```bash
   gh pr view <branch> --json number,labels,assignees
   ```

   If any expected label or the assignee is missing, add it with `gh pr edit <number> --add-label <label>` / `--add-assignee @me` rather than leaving it to Validate Conventions to catch and fail on.

For complete PR conventions and description guidelines, see [create-pull-request skill](../create-pull-request/SKILL.md). For the full label vocabulary, the `opened`/`reopened` reconciliation step that creates missing labels, and how to fix each individual metadata failure, see the [triage-integration skill](../triage-integration/SKILL.md).

## Output

After completing all phases, print a summary table:

| Phase    | Result                                                    |
|----------|-----------------------------------------------------------|
| Branch   | Created `<branch>` / Already on `<branch>`                |
| Commit   | `<type>(<scope>): <gitmoji> <subject>` / Skipped (clean)  |
| PR       | Created `<url>` / Already exists `<url>`                  |
| Labels   | `type:*`, `scope:*` (one per title scope), `source:agent` |
| Assignee | `@me` — confirmed via `gh pr view`                        |

## Resources

- [checkout-branch skill](../checkout-branch/SKILL.md) — Branch naming conventions
- [rename-branch skill](../rename-branch/SKILL.md) — Rename non-conforming branches before commit/push
- [commit-code skill](../commit-code/SKILL.md) — Commit message format, types, scopes, gitmoji
- [create-pull-request skill](../create-pull-request/SKILL.md) — PR conventions and description template, full Labels section
- [triage-integration skill](../triage-integration/SKILL.md) — Label vocabulary, `opened`/`reopened` reconciliation, fixing metadata failures
- [check-commit-signing-configuration.sh](../../../scripts/git/check-commit-signing-configuration.sh) — Pre-commit hook signing prerequisite check
- [check-push-commit-signatures.sh](../../../scripts/git/check-push-commit-signatures.sh) — Pre-push hook commit signature validation
