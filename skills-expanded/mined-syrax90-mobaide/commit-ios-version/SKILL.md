---
name: commit-ios-version
description: Commit, push, open a PR for, and immediately merge an iOS app version bump (MARKETING_VERSION / CURRENT_PROJECT_VERSION in ios/Config/Version.xcconfig), then return to an up-to-date main. Use when the user asks to commit the current iOS version, commit the iOS version bump, or ship/merge the bumped iOS version.
---

# Commit the iOS version bump

The user has already edited the version in `ios/Config/Version.xcconfig` (`MARKETING_VERSION` and/or `CURRENT_PROJECT_VERSION`). Ship that change end to end without pausing for confirmation, reviewers or CI.

Normally release-please bumps both values in its release PR (see `docs/versioning-and-updates.md`). A manual `MARKETING_VERSION` bump must also set `"ios"` in `.release-please-manifest.json` to the same version, or release-please computes the next version from a stale base.

## 1. Check the change

```bash
git status --short
git diff -- ios/Config/Version.xcconfig .release-please-manifest.json
```

- Read the new `MARKETING_VERSION` (e.g. `1.0.10`) and `CURRENT_PROJECT_VERSION` (build number) from the diff — call them `<version>` and `<build>`.
- The diff must contain only version lines. If it touches anything else, or there is no version change at all, stop and tell the user.
- Commit only the version bump. Leave unrelated modified files (e.g. `.claude/settings.local.json`) unstaged.

## 2. Branch, commit, push

If the current branch is `main`, first create a branch: `git checkout -b bump-ios-to-<version>` (dots replaced with dashes). Otherwise stay on the current branch.

```bash
git add ios/Config/Version.xcconfig .release-please-manifest.json
git commit -m "Bump up iOS version to <version>"   # plus the attribution trailer
git push -u origin HEAD
```

## 3. Create the PR and merge it immediately

```bash
gh pr create --base main --title "chore(ios): bump version to <version>" --body "Bump the iOS app to <version> (build <build>)."   # plus the PR attribution line
gh pr merge --squash
```

- Use `--squash` (the repo allows squash merges only; the PR title becomes the commit subject on `main`).
- Do not wait for reviews or GitHub Actions, and do not use `--auto`. If the merge is refused because required checks or reviews are pending, retry with `gh pr merge --squash --admin` — the user explicitly asked for an immediate merge.
- Do not pass `--delete-branch` (it tries to check out `main` locally, which fails in a worktree).
- Confirm with `gh pr view --json state,mergedAt` that the PR is `MERGED`.

## 4. Return to main

```bash
git checkout main
git pull origin main --rebase
```

If `git checkout main` fails because `main` is already checked out in another worktree, do not force it and do not touch that other worktree — report it to the user instead.

## 5. Report

Tell the user the version/build, the PR URL, that it was merged, and the result of the final pull.
