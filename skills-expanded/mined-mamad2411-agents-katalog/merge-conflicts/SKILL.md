---
name: merge-conflicts
description: "Resolve merge conflicts on a pull request by merging the target branch into the source branch and fixing conflicts. Use when a PR has merge conflicts, a branch needs to be updated, or when asked to fix conflicts. Triggers on: fix merge conflicts, resolve conflicts, merge conflicts on PR, update branch, rebase PR."
---

# Merge Conflict Resolver

> ⛔ **CRITICAL: Check `git.autoCommit` before completing merge commit**
>
> **Trigger:** Before running `git commit --no-edit` in Step 5.
>
> **Check:** Read `project.json` → `git.autoCommit`
> - If `true` (default): Proceed with commit normally
> - If `false`: **NEVER run `git commit`** — failure to comply violates project constraint
>
> **When autoCommit is disabled:**
> 1. Stage resolved files: `git add <resolved-files>`
> 2. Report: "Conflicts resolved and staged. Run `git commit --no-edit` to complete merge."
> 3. Wait for user confirmation before pushing

Resolve merge conflicts on a pull request by merging the target branch into the source branch and fixing all conflicts.

---

## Input

The user provides a PR number or URL. If not provided, ask for it.

---

## The Job

1. Get the PR details
2. Fetch and checkout the source branch
3. Merge the target branch in
4. Resolve every conflict
5. Complete the merge commit
6. Push

---

## Step 1: Get PR Details

Use `gh pr view <PR> --json headRefName,baseRefName,title,body` to get:

- **headRefName** — the source branch (the one with your changes)
- **baseRefName** — the target branch (the one you're merging into, e.g. `main`)

---

## Step 2: Fetch and Checkout

```bash
git fetch origin <baseRefName> <headRefName>
git checkout <headRefName>
```

Make sure the local branch is up to date with the remote:

```bash
git pull origin <headRefName>
```

---

## Step 3: Start the Merge

```bash
git merge origin/<baseRefName> --no-edit
```

If there are no conflicts, you're done — skip to Step 6.

If there are conflicts, `git merge` will exit non-zero and list the conflicted files. Continue to Step 4.

---

## Step 4: Resolve Conflicts

For each conflicted file:

1. **Read the file** to see the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
2. **Understand both sides:**
   - The `HEAD` side is the source branch (your PR's changes)
   - The incoming side is the target branch (e.g. `main`)
3. **Decide the correct resolution.** In most cases:
   - If both sides changed different things, keep both changes
   - If both sides changed the same thing differently, prefer the source branch's intent while incorporating any necessary updates from the target branch
   - For lock files, dependency manifests, or generated files — regenerate rather than manually merge
4. **Edit the file** to remove all conflict markers and produce the correct merged result
5. **Stage the resolved file:** `git add <file>`

### Special cases

- **Lock files** (`package-lock.json`, `bun.lock`, `go.sum`, etc.): Delete the file, regenerate it by running the appropriate install command (`npm install`, `bun install`, `go mod tidy`, etc.), then stage it.
- **Generated code** (protobuf outputs, compiled assets): Regenerate using the project's build tooling rather than manually resolving.
- **Moved or renamed files**: Check `git status` for rename detection. If a file was renamed on one side and modified on the other, apply the modifications to the renamed path.

### Verification

After resolving all files, confirm no conflict markers remain:

```bash
grep -rn '<<<<<<< ' . --include='*' | grep -v node_modules | grep -v .git
```

If any markers are found, go back and fix them.

---

## Step 5: Complete the Merge

Once all conflicts are resolved and staged:

```bash
git commit --no-edit
```

This uses the default merge commit message that git prepared.

---

## Step 6: Push

```bash
git push origin <headRefName>
```

---

## Guidelines

- **Do not rebase.** Always merge. Rebasing rewrites history on a shared branch and can cause problems for other contributors.
- **Do not force push.** If a regular push fails, something is wrong — investigate before proceeding.
- **Preserve intent.** When resolving conflicts, the goal is to keep the PR's changes working correctly with the latest target branch. Don't drop changes from either side unless there's a clear reason.
- **Regenerate, don't merge** lock files and generated artifacts.
- **Run a quick sanity check** after resolving if the project has a fast build or typecheck command (check AGENTS.md for available commands). Don't run full test suites unless the user asks.
- **If a conflict is ambiguous** and you cannot determine the correct resolution with confidence, stop and ask the user before proceeding. Describe both sides of the conflict and your proposed resolution.
