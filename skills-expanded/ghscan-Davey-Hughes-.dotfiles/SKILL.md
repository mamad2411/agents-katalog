---
name: prep-pr
description: Use when a working branch needs to become a pull request in an open source repo, or when asked to prep, tidy, or clean up a branch before opening a PR - symptoms are WIP and fixup commits, commits out of logical order, leftover explanatory comments the repo would not have written, and commit messages written for yourself rather than for a maintainer.
disable-model-invocation: true
---

# prep-pr

A branch that works is not a branch a maintainer wants to read. This turns a working branch into one a stranger can review: comments that match the repo, commits in a logical order, messages that scan.

**Nothing is pushed.** No `git push`, no force-push, no PR opened. The branch is left clean and local; the human takes it from there.

## Order of operations

Backup → ask about the review → comments → commits → messages → review (if approved) → report.

The review question is asked once, up front. The review itself runs last, on the finished branch.

## Step 0: backup and base

Refuse to start on a dirty tree. `git status --porcelain` must be empty; tell the user to commit or stash.

Establish the base commit and confirm it with the user if it is not obvious:

```bash
git symbolic-ref -q --short refs/remotes/upstream/HEAD \
  || git symbolic-ref -q --short refs/remotes/origin/HEAD
git merge-base HEAD "$BASE"
```

Then, before changing anything:

```bash
git branch "prep-pr-backup/$(git branch --show-current)-$(date +%Y%m%d-%H%M%S)"
```

Report the backup branch name to the user immediately. Any step goes wrong: `git reset --hard <backup>`.

## Step 1: ask about the review

Ask once, now, before any edits:

> Run a subagent code review over the full branch diff once cleanup is done?

Record the answer and move on. Do not ask again mid-flow.

## Step 2: comments

Read the repo before touching your own diff. Sample neighbouring files in the directories you changed and answer: how many comments per function does this repo actually carry, and what do they explain?

Delete from the branch diff:
- Narration of what the next line plainly does
- Change history ("was X, now Y", "renamed from Z")
- Commented-out code
- TODOs with no issue number
- Comments addressed to the reviewer or to the user rather than to a future reader
- Docstrings on things the repo does not document

Keep: why a non-obvious choice was made, workarounds with a link, invariants a caller must respect, license and lint headers.

The test: if a regular contributor to this repo would not have written that line, it goes.

## Step 3: commits

Plan first, rewrite second. Read `git log --oneline <base>..HEAD` and `git diff --stat <base>..HEAD`, then show the user the before/after commit list and get approval before rewriting.

Target shape:
- Each commit builds and passes tests on its own
- Each commit does one thing and could be reverted alone
- Fixups are squashed into the commit they fix
- Prep and refactors first, then the feature, then tests and docs - unless the repo's own history does it differently
- Dropped: unrelated drive-by edits, debug scaffolding, work that was later reverted, local-only config

Then rebase. `git rebase -i` cannot be driven interactively here, so write the todo list to a file and feed it in:

```bash
# write the pick/squash/drop list to a file, then hand it to the rebase
GIT_SEQUENCE_EDITOR="cp $TODO" git rebase -i "$BASE"
```

Conflicts you cannot resolve with confidence: stop, `git rebase --abort`, report.

## Step 4: messages

Match the repo, not your habits. `git log --oneline -50 <base>` shows whether it uses conventional-commit prefixes, sentence case, ticket refs. Copy that. Read CONTRIBUTING.md for message rules and for a DCO sign-off requirement.

- Subject: imperative, around 50 characters, no trailing period
- Body: only when the *why* is not obvious from the diff; wrap at 72
- Cut: "as requested", session narration, "part 2 of 3", any assistant or tool attribution or trailer

## Step 5: review, if approved

Only if the user said yes in Step 1. Dispatch one subagent with the full `<base>..HEAD` diff and the repo's conventions, asking for correctness bugs, leftover scaffolding, and style mismatches.

Report findings; do not act on them. Fixing a finding means rewriting history again, which needs a fresh confirmation.

## Step 6: report

- Backup branch name
- Commit count before and after, with the final `git log --oneline` list
- What was dropped, and why
- Review findings, if any
- That nothing was pushed

## Common mistakes

| Mistake | Fix |
|---|---|
| Rewriting history before showing the plan | Show before/after commit list, get approval |
| Trimming comments to your taste | Sample the repo's files first; match its density |
| Reviewing before cleanup | The review runs on what actually ships |
| Pushing "to check CI" | Out of scope. Hand the branch back |
| Skipping the backup because the change is small | The backup is Step 0 for every run |
