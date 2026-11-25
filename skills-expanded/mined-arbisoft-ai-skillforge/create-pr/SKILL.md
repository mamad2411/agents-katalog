---
name: create-pr
description: >-
  Create a GitHub pull request from the current branch using the gh CLI.
  Use when the user asks to create a PR, open a pull request, submit changes
  for review, or push and create a PR.
---

# Create PR

Create a GitHub pull request from the current branch using `gh`.

## Prerequisites

- **`gh` CLI** must be installed and authenticated (`gh auth status` to verify).
- The repository must have a GitHub remote.

## Workflow

### Step 1: Assess the current state

Run these in parallel to understand what we're working with:

```bash
git status
git branch --show-current
git log --oneline -10
git remote -v
```

**Guard rails:**
- If on `main` or `master`, ask the user if they want to create a branch first.
- If there are uncommitted changes, ask the user if they should be committed before creating the PR.

### Step 2: Determine the base branch

Default to the repository's default branch:

```bash
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
```

If the user specifies a different base, use that instead.

### Step 3: Gather commit history for the PR body

Get all commits on this branch since it diverged from the base (replace `<base>` with the branch name from Step 2):

```bash
git log --oneline <base>..HEAD
git diff <base>...HEAD --stat
```

### Step 4: Draft the PR title and body

**Title:** Infer from the branch name and commits. Use conventional style when appropriate (e.g., `feat: ...`, `fix: ...`, `docs: ...`). Keep it concise (<72 chars).

**Body:** Use this template:

```markdown
## Summary
<1-3 bullet points describing what changed and why>

## Changes
<file-level summary of key changes>

## Test plan
<checklist of how to verify the changes>
```

Show the draft to the user before submitting if there's any ambiguity. For straightforward changes, proceed directly.

### Step 5: Push the branch

Check whether you have push access to `origin`. If `origin` points to a repo you don't own (common in open-source), fork first:

```bash
gh repo fork --remote=true
```

This sets `origin` to your fork and `upstream` to the original repo. Then push:

```bash
git push -u origin HEAD
```

### Step 6: Create the PR

**Same-repo workflow** (you have push access to origin):

```bash
gh pr create --title "TITLE" --body "BODY" --base <base>
```

**Fork workflow** (origin is your fork, upstream is the target repo):

```bash
gh pr create \
  --repo UPSTREAM_OWNER/REPO \
  --head YOUR_USERNAME:BRANCH \
  --base <base> \
  --title "TITLE" \
  --body "BODY"
```

Use a HEREDOC for the body to preserve formatting:

```bash
gh pr create --title "the title" --body "$(cat <<'EOF'
## Summary
- bullet points

## Changes
- file changes

## Test plan
- [ ] verification steps
EOF
)"
```

### Step 7: Confirm

After creation, output the PR URL so the user can access it directly.

## Options the user may request

| Request | How to handle |
|---------|--------------|
| Draft PR | Add `--draft` flag |
| Specific reviewers | Add `--reviewer user1,user2` |
| Labels | Add `--label label1,label2` |
| Milestone | Add `--milestone "v1.0"` |
| Assign to self | Add `--assignee @me` |

## Error handling

- If `gh auth status` fails, tell the user to run `gh auth login`.
- If no remote exists, tell the user to add one with `git remote add origin <url>`.
- If the push fails with a 403 or permission denied, the user likely doesn't have write access — fork the repo with `gh repo fork --remote=true` and retry.
- If the branch is already up-to-date with base (no commits), warn that the PR will be empty.
- If a PR already exists for this branch, show the existing PR URL instead of creating a duplicate.
