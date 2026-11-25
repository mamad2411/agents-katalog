---
name: start-issue
description: Start work on a Devcules GitHub issue or an ad-hoc task. Reads the issue (or takes free text), checks dependencies, and creates a users/kiran/<slug> branch from an updated main. Use when asked to start, pick up or work on an issue number, or to start an ad-hoc branch from a text description.
---

# Start an issue

Input: an issue number (e.g. `/start-issue 3`) or free text describing ad-hoc work (e.g. `/start-issue add agent skills`).

## Issue path (a number was given)

1. Run `gh issue view <number>`. Note the module id from the title (e.g. `M0.3`), the scope, the "Depends on" line and the test gate.
2. Check the dependency is done: the previous module's issue must be closed (`gh issue view <previous> --json state -q .state` shows `CLOSED`). If it isn't, stop and say so. Skip this when the issue says "Depends on: none".
3. Check the working tree is clean (`git status --porcelain` prints nothing). If it isn't, stop and list the changes. Never stash or discard them yourself.
4. Update main, then branch from it (see below). Make `<module>` the lowercase module id (`m0.3`) and `<slug>` two to four lowercase words from the title, joined by hyphens.
5. Check `git config user.email` is not a work address.
6. Reply with: the branch name, a three-line summary of the scope, the test gate as a checklist, and your plan in at most five steps. Then wait for the go-ahead before writing code.

## Ad-hoc path (free text, no issue number)

1. Check the working tree is clean (`git status --porcelain` prints nothing). If it isn't, stop and list the changes. Never stash or discard them yourself.
2. Update main, then branch from it (see below). Make the slug two to four lowercase words from the given text, joined by hyphens (`users/kiran/<slug>`).
3. Check `git config user.email` is not a work address.
4. Reply with: the branch name and a three-line summary of the work. Then wait for the go-ahead before writing code.

## Updating main and branching

Unless the user names a different base: run `git switch main`, then `git pull --ff-only` to update it. If the update fails (e.g. local main has diverged), stop and say so. Then run `git switch -c users/kiran/<name> main`. If the branch already exists, switch to it instead, then run `git log origin/main..HEAD --oneline` to see what's on it.
