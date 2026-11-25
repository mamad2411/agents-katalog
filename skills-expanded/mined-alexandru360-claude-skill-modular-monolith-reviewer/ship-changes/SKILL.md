---
name: ship-changes
description: Stage, commit, and push local changes to remote. Refuses to operate on the default branch (auto-detected). Groups changes into logical commits based on granularity. Supports --morePR flag to split changes into multiple branches with one PR each. Triggers on phrases like "commit and push", "ship changes", "push my work", "commit everything", "ship it", "push this", "save to github", "push to remote", "let's push this up", or "commit these changes".
allowed-tools: Read, Glob, Grep, Bash
model: haiku
version: 1.0
---

# Ship Changes

Automate the stage-commit-push workflow with a safety guard against committing directly to the default branch.

## When this skill applies

Use when the user wants to:
- Commit and push local changes to the remote.
- Group uncommitted work into one or more logical commits.
- Finalize work on a feature branch.

Do **not** use when:
- The user only wants to stage without committing.
- The user explicitly wants to amend an existing commit (handle separately).
- There are no local changes (nothing to ship).

## Stop conditions

Before executing any step, check these conditions in order. If any triggers, **STOP** immediately with the corresponding message and take no further action.

| # | Condition | Check | Stop message |
|---|-----------|-------|--------------|
| 1 | Not a git repository | `git rev-parse --is-inside-work-tree` fails | "Not a git repository. Initialize with `git init` or navigate to a repo." |
| 2 | No remote configured | `git remote` returns empty | "No remote configured. Add one with `git remote add origin <url>`." |
| 3 | Git identity missing | `git config user.name` or `git config user.email` is empty | "Git identity not set. Run `git config user.name '<name>'` and `git config user.email '<email>'`." |
| 4 | On default branch | Current branch equals `<default-branch>` | "Refused: you are on the default branch (`<default-branch>`). Create or switch to a feature branch first." |
| 5 | Working tree clean | `git status --porcelain` returns empty | "Nothing to ship — working tree is clean." |
| 6 | Pre-commit hook fails | `git commit` exits non-zero due to hook | "Pre-commit hook failed. Fix the reported issues and retry. Do NOT use `--no-verify`." |
| 7a | Push rejected: non-fast-forward | stderr contains `non-fast-forward` | "Remote has new commits. Run `git pull --rebase origin <current-branch>` then retry." |
| 7b | Push rejected: branch protection | stderr contains `protected branch` or `required status check` | "Branch is protected. Direct push not allowed — create a Pull Request instead." |
| 7c | Push rejected: auth failure | stderr contains `Authentication failed` or `403` | "Authentication failed. Check your token or credentials with `git credential`." |
| 7d | Push rejected: no upstream | stderr contains `has no upstream branch` | "No upstream set. Retry with `git push -u origin <current-branch>`." |

## Execution steps

### Step 1 — Branch guard

Determine the default branch and store it as `<default-branch>`:
```
git symbolic-ref refs/remotes/origin/HEAD | sed 's|refs/remotes/origin/||'
```
If that fails, fall back to `git remote show origin | grep 'HEAD branch' | awk '{print $NF}'`.

Compare against the current branch:
```
git branch --show-current
```

If current branch IS `<default-branch>` → trigger **Stop #4**.

If user requests branch creation, sync `<default-branch>` first then create with enforced naming:
```
git fetch origin <default-branch> && git pull --ff-only origin <default-branch> && git checkout -b <type>/<issue-id>-<short-desc>
```

Branch naming format: `<type>/<issue-id>-<short-desc>`
- **Types**: `feature/`, `chore/`, `fix/`, `docs/`, `refactor/`, `test/`
- **Issue ID**: Jira key (e.g., `PBI-158`) or GitHub issue (e.g., `GH-45`). Required.
- **Short desc**: kebab-case, max 40 chars.
- Examples: `feature/PBI-158-add-login-form`, `fix/PBI-203-broken-notification`

Reject if:
- Missing type prefix
- Missing issue ID
- No short description after issue ID

### Step 2 — Inventory changes

Classify all changes into categories:

```
git diff --cached --name-status          # Staged (ready to commit)
git diff --name-status                   # Unstaged (modified, not added)
git ls-files --others --exclude-standard # Untracked (new files)
git diff --cached --diff-filter=R        # Renamed (detect moves)
git diff --cached --diff-filter=D        # Deleted (confirm intent)
```

Present inventory to user as a summary table:

> | Category | Count | Files |
> |----------|-------|-------|
> | Staged | 3 | src/features/auth/Login.tsx, ... |
> | Unstaged | 1 | src/utils/format.ts |
> | Untracked | 2 | src/features/auth/Login.test.tsx, ... |
> | Renamed | 1 | OldName.tsx → NewName.tsx |
> | Deleted | 0 | — |

Rules:
- **Renamed files** stay together in the same commit group (not split as delete + add).
- **Untracked files**: list separately and ask "Include these new files? (y/all/n)" before staging.
- **Deleted files**: highlight explicitly so user confirms intent.

If all categories are empty → trigger **Stop #5**.

### Step 3 — Deterministic grouping

Group changes using this priority hierarchy:
1. **Per feature folder** — files in the same `src/features/<name>/` form one group.
2. **Per type** — files outside feature folders group by nature: config, docs, test, shared types.
3. **Per topic** — remaining files that share a common purpose (e.g., a rename across multiple locations).

Always present the proposed grouping to the user with options:

> "Proposed: N commit(s).
>
> | # | Type | Scope | Files |
> |---|------|-------|-------|
> | 1 | feat | notifications | src/features/notifications/... |
> | 2 | chore | config | tsconfig.json, vite.config.ts |
>
> Options:
> **(a)** Accept split as proposed
> **(b)** Squash all into a single commit
> **(c)** Adjust — tell me how to regroup"

Wait for user response before proceeding.

### Step 4 — Commit

For each commit group:
1. Stage the relevant files by name (never `git add -A` or `git add .`).
2. Determine the commit message:
   - **If user provided a message** → use it directly.
   - **If no message provided** → analyze `git diff --cached` and generate a Conventional Commit.

**Commit message format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Subject line (required):**
- Format: `type(scope): description`
- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `style`, `build`, `ci`, `revert`
- Scope: the feature or area affected (e.g., `notifications`, `counter`, `config`)
- Max 50 characters, lowercase first letter, no period at end
- Imperative mood: "add" not "added" or "adds"

**Body (optional — include when the "why" isn't obvious):**
- Separated from subject by blank line
- Explain what and why, not how
- Wrap at 72 characters

**Footer (optional):**
- Issue reference (as Jira link): `Fixes [PBI-158](https://legogroup.atlassian.net/browse/PBI-158)` or `Closes #45`
- Breaking changes: `BREAKING CHANGE: <description>`

3. Create the commit using heredoc format:
   ```
   git commit -m "$(cat <<'EOF'
   type(scope): subject

   Body explaining why this change was made.

   Fixes [PBI-XXX](https://legogroup.atlassian.net/browse/PBI-XXX)
   EOF
   )"
   ```
   Omit body and footer if the subject is self-explanatory.

### Step 5 — Pre-push checks

Run these checks in order before pushing:

**5a — Secrets scan** (see Step 5.6 below for details)

**5b — Test check**
Inspect the diff for behavior/logic changes (new functions, modified conditionals, changed return values).
If behavior changed and no test files (`*.test.*`, `*.spec.*`) were added or modified in the same diff → **pause** and ask:
> "Logic changed but no tests were updated. Continue without tests? (y/n)"

**5c — Quality gate marker**
The Claude `block-unverified-push` hook requires `.claude/tmp/quality-gates.ok` to exist before allowing push.

If Step 4 (commit) succeeded, Husky pre-commit already validated lint + format on staged files.
Husky pre-push will validate `tsc --noEmit && vitest run` at push time.

Create the marker after successful commit to unlock the Claude push hook.
Use the **Write tool** (not Bash) to avoid the circular block:
```
Write file: .claude/tmp/quality-gates.ok
Content: "ok"
```
Do NOT use Bash to create this file — the hook blocks Bash commands when the marker doesn't exist yet.

This avoids duplication:
- Lint + format → covered by Husky pre-commit (Step 4)
- Typecheck + tests → covered by Husky pre-push (Step 6)
- Marker → created here to satisfy Claude hook

If Husky pre-push fails (tsc or vitest error) → push is blocked anyway. No quality is bypassed.

### Step 6 — Push

Push the current branch to origin with tracking:
```
git push -u origin <current-branch>
```

Only fast-forward pushes allowed. If rejected, parse stderr and trigger the matching stop:
- `non-fast-forward` → **Stop #7a**
- `protected branch` / `required status check` → **Stop #7b**
- `Authentication failed` / `403` → **Stop #7c**
- `has no upstream branch` → **Stop #7d**

### Step 7 — Draft PR

**7a — Check for existing PR:**

Before offering to create a PR, check if one already exists for this branch:
```
gh pr list --head <current-branch> --state open --json number,title,url
```

If a PR already exists → output:
> "Existing PR found: #<number> — <title>
> <url>
> Pushed new commits to the existing PR.
>
> Update PR title/description to reflect new commits? (y/n)"

If yes, regenerate title and body from the full commit log on the branch (`git log <default-branch>..HEAD --oneline`) and update:
```
gh pr edit <number> --title "<type>(<scope>): <subject>" --body "$(cat <<'EOF'
## Summary
- <bullet points from all branch commits>

## Test plan
- [ ] Verify <main behavior>
- [ ] Check for regressions

Fixes [<issue-id>](https://legogroup.atlassian.net/browse/<issue-id>)
EOF
)"
```

If user declines → skip update, keep existing PR as-is.

**7b — Create new PR (only if none exists):**

If no existing PR, ask:
> "Create a Draft Pull Request? (y/n)"

If yes, create a draft PR and open it in the browser:
```
gh pr create --draft --title "<type>(<scope>): <subject>" --body "$(cat <<'EOF'
## Summary
- <bullet points from commit messages>

## Test plan
- [ ] Verify <main behavior>
- [ ] Check for regressions

Fixes [<issue-id>](https://legogroup.atlassian.net/browse/<issue-id>)
EOF
)"
```

The `--draft` flag ensures no reviewers are notified until the PR is ready.

If user declines → skip, output the manual command for later use.

### Step 8 — Summary

Output a final summary:
```
Shipped:
- N commit(s) on branch `<branch>`
- Remote: origin/<branch>
- Commit(s): <short-hash> <message> (for each)
- PR: <url> (draft) — or "skipped"
```

### Step 5a detail — Secrets scan

Before committing, scan staged changes for secrets using two layers:

**Layer 1 — File denylist (by name/extension):**
Block any file matching:
`.env`, `.env.*`, `credentials.*`, `*.key`, `*.pem`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `*.secret`, `*-secret.yaml`, `*.tfvars`

**Layer 2 — Content pattern scan (in diff):**
Run `git diff --cached` and scan for patterns:

| Pattern | What it catches |
|---------|-----------------|
| `AKIA[0-9A-Z]{16}` | AWS Access Key ID |
| `ghp_[a-zA-Z0-9]{36}` | GitHub Personal Access Token |
| `sk-[a-zA-Z0-9]{48}` | OpenAI / Anthropic API Key |
| `-----BEGIN (RSA\|EC\|OPENSSH) PRIVATE KEY-----` | Private keys inline |
| `password\s*[:=]\s*['"][^'"]+['"]` | Hardcoded passwords |
| `(secret\|token\|api_key)\s*[:=]\s*['"][^'"]+['"]` | Generic secrets assignment |
| `mongodb(\+srv)?://[^:]+:[^@]+@` | Connection strings with credentials |
| `postgres://[^:]+:[^@]+@` | PostgreSQL connection strings |

If any match is found → **STOP** with:
> "Secrets detected in staged changes:
> - `<file>:<line>` — `<pattern matched>`
>
> Remove the secret, use environment variables, and retry."

Do NOT offer to proceed — secrets are a hard block, not a confirmation prompt.

## `--morePR` mode

When invoked with `--morePR`, the skill splits changes into multiple branches and creates one PR per group.

### Prerequisites

- Must be on a **working branch** (not the default branch) — same guard as normal mode.
- All changes must be **uncommitted** (staged, unstaged, or untracked). Already-committed changes are not split.

### Flow

**M1 — Inventory & grouping (reuses Step 2 + Step 3)**

Present the same inventory table and deterministic grouping proposal. Then ask the user:

> "Proposed N group(s):
>
> | # | Scope | Files |
> |---|-------|-------|
> | 1 | notifications | src/features/notifications/... |
> | 2 | auth | src/features/auth/... |
> | 3 | config | tsconfig.json, vite.config.ts |
>
> Each group becomes a separate branch + PR.
> Options:
> **(a)** Accept split as proposed
> **(b)** Merge groups — tell me which numbers to combine
> **(c)** Move files between groups — tell me which files go where
> **(d)** Cancel — ship everything as a single PR (normal mode)"

Wait for user response. Iterate until the user accepts with **(a)**.

**M2 — Stash working changes**

Save all current changes (staged + unstaged + untracked) to a temporary stash:
```
git stash push --include-untracked -m "ship-morePR-working-stash"
```

**M3 — For each group, sequentially:**

For group `i` (1..N):

1. **Start from default branch:**
   ```
   git checkout <default-branch>
   git pull --ff-only origin <default-branch>
   ```

2. **Create a branch:**
   ```
   git checkout -b <type>/<issue-id>-<short-desc>
   ```
   Branch naming follows the same rules as Step 1. If user didn't provide issue IDs per group, ask once per group:
   > "Group <i> (<scope>): branch name? (e.g., `feature/PBI-200-add-notifications`)"

3. **Restore only this group's files from stash:**
   ```
   git checkout stash@{0} -- <file1> <file2> ...
   ```
   For untracked files that don't exist on `<default-branch>`:
   ```
   git show stash@{0}^3:<file> > <file>
   git add <file>
   ```

4. **Commit** — same rules as Step 4 (conventional commit, secrets scan, no `--no-verify`).

5. **Push:**
   ```
   git push -u origin <branch-name>
   ```

6. **Create Draft PR** — same format as Step 7b. No confirmation prompt per PR in `--morePR` mode (user already approved the split).

7. **Record** the PR URL and branch name for the final summary.

**M4 — Cleanup**

After all groups are processed:

1. Return to the original working branch:
   ```
   git checkout <original-working-branch>
   ```

2. Drop the stash:
   ```
   git stash drop stash@{0}
   ```

3. The original working branch remains intact with all original changes still present (uncommitted). The user decides what to do with it.

**M5 — Summary**

Output a combined summary:
```
Shipped (--morePR):
- N branch(es) created, N Draft PR(s) opened.

| # | Branch | PR | Title |
|---|--------|----|-------|
| 1 | feature/PBI-200-notifications | #42 | feat(notifications): add toast system |
| 2 | feature/PBI-201-auth | #43 | feat(auth): add login form |

Original working branch: `<branch>` (unchanged)
```

### Error handling in `--morePR`

- If any group fails (commit hook, push rejection, secrets detected): **stop processing**, report the error, and restore state:
  ```
  git checkout <original-working-branch>
  ```
  Already-created PRs remain open. User can fix the issue and re-run for remaining groups.

- If stash application fails for a file (conflict with default branch): report the file, skip the group, continue with the next group. List skipped groups in the summary.

## Constraints

- **Never force-push** unless the user explicitly says "force push".
- **Never skip hooks** (no `--no-verify`).
- **Untracked files**: include only if they are clearly part of the current work. If ambiguous, ask.
