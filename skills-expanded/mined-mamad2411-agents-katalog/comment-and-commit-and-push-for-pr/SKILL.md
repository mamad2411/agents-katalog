---
name: comment-and-commit-and-push-for-pr
description: >-
  Stages all uncommitted changes, commits with a descriptive message, pushes the
  branch (setting upstream tracking if needed), and opens a GitHub pull request
  via the gh CLI with a well-structured description. Use whenever the user wants
  to ship their current work as a PR.
---

# comment-and-commit-and-push-for-pr skill

Stage every uncommitted change, commit, push the branch to origin (wiring up tracking if it has none), and open a GitHub pull request with a thorough description.

## Prerequisites check

Before doing anything else, verify the environment is ready:

```bash
which gh && gh auth status
```

- If `gh` is not found: stop and tell the user to install it (`brew install gh`) and authenticate (`gh auth login`).
- If `gh` is not authenticated: stop and tell the user to run `gh auth login`.
- Confirm the required token scope includes `repo`. If not, the user must re-authenticate with `gh auth refresh -s repo`.

## Step-by-step

### 1. Sync with remote before touching anything

Before staging a single file, make sure the working branch is up to date. Run these in parallel:

```bash
git rev-parse --abbrev-ref HEAD
git fetch --all --prune
git status --short
```

Use the results to determine the sync strategy:

#### 1a. Pull the current branch's remote counterpart (if it exists)

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

- **Tracking branch exists and working tree is clean**: pull normally.

  ```bash
  git pull
  ```

- **Tracking branch exists but there are uncommitted changes**: do **not** stash automatically. Tell the user that local changes are present and ask whether to stash-pull-unstash or skip the pull. Default recommendation: stash, pull, unstash.

  ```bash
  # Only run these three commands if user agrees:
  git stash push -m "pre-sync stash"
  git pull
  git stash pop
  ```

  If `git stash pop` produces conflicts, stop and ask the user to resolve them before continuing.

- **No tracking branch**: skip the pull; the branch is local-only and there is nothing to pull from yet.

- **Pull rejected (non-fast-forward / diverged)**: stop immediately. Report the divergence and ask the user how to proceed. Do **not** rebase or reset without explicit instruction.

#### 1b. Merge the integration branch if behind it

After pulling the current branch, check whether it is behind `develop` (or `main` if `develop` doesn't exist):

```bash
# determine integration branch (prefer develop, fall back to main/master)
git rev-parse --verify origin/develop 2>/dev/null && echo "develop" || \
  git rev-parse --verify origin/main 2>/dev/null && echo "main" || echo "master"
```

Then count how many commits the integration branch has that the current branch does not:

```bash
git rev-list --count HEAD..origin/<integration-branch>
```

- **Count > 0 (current branch is behind)**: merge the integration branch in.

  ```bash
  git merge origin/<integration-branch> --no-edit
  ```

  - If the merge succeeds cleanly, report the number of commits pulled in and continue.
  - If the merge produces **conflicts**: stop immediately. List the conflicting files and ask the user to resolve them, then re-run the skill.

- **Count = 0 (current branch is up to date or ahead)**: no action needed; continue.

- **Current branch IS the integration branch** (e.g., you are on `develop`): skip this sub-step entirely.

#### 1c. Confirm the working tree is ready

After syncing, verify the tree is in a state suitable for staging:

```bash
git status --short
```

If merge conflict markers (`<<<<<<<`) appear in any tracked file, stop and ask the user to resolve them.

---

### 2. Snapshot current state

Run these four commands **in parallel**:

```bash
git status
git diff HEAD
git log --oneline -10
git remote -v
```

- `git status` — shows untracked and modified files.
- `git diff HEAD` — full diff of staged + unstaged changes relative to HEAD.
- `git log --oneline -10` — reveals commit-message style and conventions in this repo.
- `git remote -v` — confirms a remote named `origin` exists.

If no `origin` remote exists, stop and ask the user to add one:

```
git remote add origin <url>
```

### 3. Analyse the diff

Read the diff carefully. For each changed file identify:

- **What** changed (new feature, bug fix, refactor, test, docs, config, dependency).
- **Why** it changed — infer from context, variable names, surrounding code, and file paths.
- Whether any file should **not** be committed (`.env`, secrets, large binaries, untracked lock files). If spotted, pause and ask.

### 4. Stage the files

Prefer explicit file names over `git add -A` so accidental inclusions are visible:

```bash
git add <file1> <file2> ...
```

Use `git add -A` only when the entire working tree is safe to stage.

Do **not** stage:
- `.env`, `.env.*`, or any file likely to contain secrets
- Large binary files unless explicitly requested

### 5. Draft and create the commit

Follow conventions from `git log`. Default structure when no convention is evident:

```
<imperative-mood summary, ≤72 chars>

- Bullet for each logical change group
- Focus on WHY, not WHAT

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

Create the commit via heredoc:

```bash
git commit -m "$(cat <<'EOF'
<subject line>

<body>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

If the pre-commit hook fails: fix the issue, re-stage, and create a **new** commit. Never use `--no-verify`.

### 6. Determine upstream tracking and push

Check whether the current branch already has a remote tracking branch:

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

- **Tracking branch exists**: push normally.

  ```bash
  git push
  ```

- **No tracking branch**: push and set upstream in one command.

  ```bash
  git push -u origin <current-branch>
  ```

  Where `<current-branch>` comes from:

  ```bash
  git rev-parse --abbrev-ref HEAD
  ```

Never force-push. If the push is rejected because the remote has diverged, stop and tell the user — do not rebase or reset without explicit instruction.

### 7. Check for an existing PR

Before creating a new PR, check whether one already exists for this branch:

```bash
gh pr view --json number,url,state 2>/dev/null
```

- **PR already exists**: report its URL and state. Ask the user if they want to update the PR description or just leave it. Do not create a duplicate.
- **No PR exists**: proceed to step 7.

### 8. Draft the PR description

Use the full diff and commit history to write a thorough PR body. Structure it as:

```markdown
## Summary

<2–4 sentences describing the overall change and motivation>

## Changes

- <file or area>: <what changed and why>
- <file or area>: <what changed and why>
(one bullet per logical change group — not one per file)

## Test plan

- [ ] <manually verify X>
- [ ] <check that Y still works>
- [ ] <any migration or env-var steps the reviewer needs to run>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Derive the base branch:
- Use `main` if it exists on the remote, otherwise `master`, otherwise ask the user.

```bash
gh pr create \
  --base <base-branch> \
  --title "<same subject as the commit, ≤72 chars>" \
  --body "$(cat <<'EOF'
<PR body>
EOF
)"
```

### 9. Confirm and report

After the PR is created, report back:

- Commit hash and subject.
- Push result (new branch or existing tracking branch).
- PR URL.
- If anything was skipped (e.g., nothing to commit, PR already existed), explain why.

### 10. Trigger test agents in parallel

Immediately after reporting the PR, spawn the `e2e-testing` and `unit-testing` agents **in parallel** using the Agent tool. Pass each agent the same context block so they can independently determine what's in their purview and write tests.

Construct a shared context string containing:
- The PR number and URL
- The list of changed files (from `git diff --name-only origin/main..HEAD`)
- The full diff stat summary
- The test plan checklist items generated in step 7

Prompt for the **e2e-testing** agent:

```
A pull request was just created: <PR_URL>

You are being called as part of the PR workflow to identify and write Playwright E2E tests.

## Changed files
<paste git diff --name-only output>

## Diff summary
<paste git diff --stat output>

## PR test plan (from the PR description)
<paste the ## Test plan section verbatim>

Your job:
1. Review the changed files and test plan items.
2. Identify which items are user-visible flows that belong in Playwright E2E specs (UI interactions, page navigation, form submissions, modal flows, etc.).
3. For each applicable item, write or extend a spec under tests/e2e/ following the e2e-testing skill at .claude/skills/e2e-testing/SKILL.md.
4. Run npm run test:e2e and fix failures until green (or report any blockers such as missing seed data or auth).
5. Report: which test plan items you covered, which spec files were written/modified, and the test run result.

Skip anything that is purely a logic/unit concern (lib/ pure functions, validators) — the unit-testing agent handles those.
```

Prompt for the **unit-testing** agent:

```
A pull request was just created: <PR_URL>

You are being called as part of the PR workflow to identify and write Vitest unit tests.

## Changed files
<paste git diff --name-only output>

## Diff summary
<paste git diff --stat output>

## PR test plan (from the PR description)
<paste the ## Test plan section verbatim>

Your job:
1. Review the changed files and test plan items.
2. Identify which items involve pure logic, lib/ utilities, validators, parsers, or data-transformation functions that belong in Vitest unit tests.
3. For each applicable item, write or extend *.test.ts files colocated with the changed modules, following the unit-testing skill at .claude/skills/unit-testing/SKILL.md.
4. Run npm run test and fix failures until green (or report exact failure output).
5. Report: which test plan items you covered, which test files were written/modified, and the npm run test result.

Skip UI flows and browser interactions — the e2e-testing agent handles those.
```

After both agents finish, summarize their findings: which test plan items each covered, any gaps neither agent could address, and whether both test suites pass.

## Safety rules

| Rule | Reason |
|------|--------|
| Always sync before staging | Staging on a stale branch produces PRs that will conflict on merge |
| Never stash automatically without asking | Stash pops can conflict; the user must decide |
| Never rebase or reset to resolve divergence | Data loss risk; always stop and ask |
| Never use `--no-verify` | Pre-commit hooks exist for a reason — fix failures, don't skip them |
| Never force-push | Rewrites shared history; ask the user explicitly if they need it |
| Never amend a published commit | Creates divergence with remote; create a new commit instead |
| Never commit secrets | `.env` and credential files must stay out of git |
| Confirm before committing if diff is >500 lines or touches CI/CD, migrations, or security-sensitive files | Big or risky changes deserve a human checkpoint |
| Never create a duplicate PR | Always check `gh pr view` before `gh pr create` |

## Error handling

- **`gh` not installed or not authenticated**: stop immediately and give setup instructions.
- **Pull rejected (non-fast-forward / remote diverged)**: stop, report the divergence, and ask the user how to proceed. Do not rebase or reset without explicit instruction.
- **Uncommitted changes block the pull**: ask the user before stashing. Default recommendation is stash → pull → unstash, but always confirm first.
- **`git stash pop` conflicts after pull**: stop and ask the user to resolve the stash conflicts before continuing.
- **Merge of integration branch (develop/main) produces conflicts**: stop, list all conflicting files, and ask the user to resolve them before re-running the skill.
- **Push rejected (non-fast-forward)**: stop, report the divergence, and ask the user how to proceed.
- **No `origin` remote**: stop and ask the user to add one.
- **Pre-commit hook fails**: fix the issue, re-stage, create a new commit.
- **Nothing to commit**: skip commit step, proceed to push + PR if there are unpushed commits.
- **Merge conflict markers in files**: stop and ask the user to resolve conflicts first.
- **PR already open for this branch**: report the existing PR URL and ask the user what they want to do.