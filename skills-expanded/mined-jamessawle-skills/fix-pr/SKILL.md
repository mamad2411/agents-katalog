---
name: fix-pr
description: Use this skill whenever someone mentions a PR that needs fixing, is broken, blocked, or unmergeable. Handles merge conflicts, failed CI, broken builds, and rebasing — diagnoses the problem, clones the repo, resolves conflicts, fixes tests, and force-pushes the result. Trigger for any mention of "PR conflicts", "CI failing", "checks failing", "can't merge", "rebase my PR", "fix PR", "unblock PR", "build is red", "PR is stuck", or any reference to a specific PR number that has problems. This skill follows a safe, structured workflow with force-with-lease pushes and PR comments documenting every change.
license: MIT
compatibility: Requires GitHub CLI (gh) authenticated with push access to the target repo
allowed-tools: Bash, Read, Edit, Write, Agent
argument-hint: <owner/repo> <pr-number>
metadata:
  author: jamessawle
  version: "1.0"
---

# Fix PR

Fix a single GitHub PR that has merge conflicts or failed CI checks.

For Claude Code-specific guidance (permissions, delegation, command patterns), see `references/claude.md`.

## Arguments

- `$0` — GitHub repository in `owner/repo` format
- `$1` — PR number

If arguments are missing, ask the user to provide them: `/fix-pr owner/repo 123`

## Workflow

### Step 1: Diagnose the PR

Run these checks in parallel:

```bash
gh pr view $1 --repo $0 --json title,baseRefName,headRefName,mergeable,state,statusCheckRollup,mergeStateStatus
```

```bash
gh pr checks $1 --repo $0
```

Analyze the results:

- **mergeable**: Is the PR mergeable or does it have conflicts?
- **statusCheckRollup**: Are CI checks passing, failing, or pending?
- **state**: Is the PR still open?

If the PR is clean (mergeable, all checks passing), report that and stop — no work needed.

### Step 2: Clone and fix

Clone the repo into a temporary working directory. Delegate the clone-and-fix work to a subagent if your platform supports it — pass it the diagnostic info, WORKDIR path, repo, PR number, base branch, and head branch. The subagent should work autonomously and return a summary.

> **Platform note:** `mktemp -d` returns `/var/folders/*` on macOS and `/tmp/*` on Linux.

```bash
WORKDIR=$(mktemp -d)
gh repo clone $0 $WORKDIR -- --depth=50
git -C $WORKDIR fetch origin pull/$1/head:pr-branch
git -C $WORKDIR checkout pr-branch
```

**Command patterns:**

- Use `git -C $WORKDIR` for all git operations to avoid affecting the user's current working directory
- Use `GIT_EDITOR=true` before rebase commands to avoid interactive editors
- For non-git commands: `cd $WORKDIR && <command>`
- Read files using absolute paths (`$WORKDIR/<file>`)

Do NOT use worktree isolation — this skill may be invoked from a directory that is not the target repo.

#### For merge conflicts

1. Rebase onto the base branch:

   ```bash
   git -C $WORKDIR fetch origin <baseRefName>
   git -C $WORKDIR rebase origin/<baseRefName>
   ```

2. When conflicts occur, for each conflicting file:
   - Read the file to understand both sides of the conflict
   - Read surrounding context and related files to understand intent
   - Resolve the conflict preserving the intent of both changes
   - Stage the resolved file and continue the rebase:

     ```bash
     git -C $WORKDIR add <file>
     GIT_EDITOR=true git -C $WORKDIR rebase --continue
     ```

3. If a conflict is ambiguous and you cannot confidently resolve it, abort the rebase and report which files and why.

#### For failed CI checks

1. Get failure logs:
   - For GitHub Actions: `gh run view <run-id> --repo $0 --log-failed`
   - For other CI: read the CI config to understand what commands are run, then run linters/tests locally to reproduce failures
2. Diagnose and fix the failure.
3. Re-run tests/linters to verify the fix passes.
4. **Roll fixes into the appropriate existing commit** rather than adding a separate "fix" commit at the end. Use `git commit --fixup=<sha>` followed by `git rebase --autosquash` to fold the fix into the commit that introduced the problem. Each commit in the PR should pass all checks on its own — this keeps the history clean and bisectable.
5. If the failure isn't attributable to a specific commit (e.g. a flaky config issue), amend it into the most relevant commit rather than appending a new one.

#### For both issues

Handle conflicts first (rebase), then address CI failures on the rebased branch. When fixing CI after a rebase, still prefer rolling fixes into existing commits over adding new ones.

### Step 3: Present changes, push, and comment

Present a summary to the user **before** asking for approval, including:

- What conflicts were found and how each was resolved
- The rebased commit list (`git log --oneline`)
- The diff stat (`git diff --stat`)
- Any caveats (e.g. lock files needing regeneration, tests that couldn't run locally)

Only **after** presenting the summary, ask for **one single confirmation** to push and comment. This is the **only point where user interaction is required**.

On approval, push with `--force-with-lease` (explicit ref for shallow clone compatibility):

```bash
git -C $WORKDIR fetch origin <headRefName>:refs/remotes/origin/<headRefName>
git -C $WORKDIR push origin pr-branch:<headRefName> --force-with-lease=<headRefName>:origin/<headRefName>
```

Then comment on the PR. Tailor the content to exactly what happened — these are templates, not copy-paste:

```bash
# On success:
gh pr comment $1 --repo $0 --body "$(cat <<'EOF'
**Automated PR maintenance** (via `fix-pr` skill)

**Actions taken:**
- Rebased onto `<baseRefName>` — resolved conflicts in `<files>`
- <any other actions, e.g. CI fixes>

**Conflict resolutions:**
- `<file>`: <brief description of how it was resolved>

All checks should re-run automatically.
EOF
)"

# On failure / partial success:
gh pr comment $1 --repo $0 --body "$(cat <<'EOF'
**Automated PR maintenance** (via `fix-pr` skill)

**Status: Needs manual attention**

**What was attempted:** <actions taken>
**What couldn't be resolved:** <files and why>
**Suggested next steps:** <specific guidance>
EOF
)"
```

Always comment, even on failure — this creates an audit trail.

### Step 4: Verify and clean up

Check the PR state after pushing:

```bash
gh pr view $1 --repo $0 --json mergeable,mergeStateStatus
```

Report the final status to the user, then clean up regardless of outcome:

```bash
rm -rf "$WORKDIR"
```

## Important guidelines

- **Minimize user interaction** — only ask for approval once, at the push + comment step
- If conflicts are ambiguous, report them rather than guessing — preserve intent of both sides
- Never use `--force` — always `--force-with-lease`
- Always comment on the PR with what was done, even on failure
