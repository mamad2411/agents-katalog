---
name: resolve-todos
description: Gathers to-do and fix-me comments, ranks them by risk and age, and fixes only the small, safe ones once you approve.
disable-model-invocation: true
---

Resolve the to-do and fix-me comments in: $ARGUMENTS (whole repository if empty).

1. Run `git grep -n -E "T[O]DO|FIXME|HACK|XXX"`, skipping vendored and generated folders.
2. For each hit, run `git blame -L <line>,<line> <file>` to get its age and author, and read ten lines around it.
3. Classify every item: **quick** (under 15 minutes, one file, no behavior change to callers), **ticket** (needs design, a decision or several files), **stale** (the code it mentions no longer exists or the issue is already fixed).
4. Rank by risk: FIXME in error paths, security or data handling first, then age.

Print a table: file:line, age, class, one-line plan. Do not edit anything yet.

Ask which quick items to fix and which stale comments to delete. Fix only those, one small commit-ready change at a time, and run the tests after each. Remove the comment when its work is done. Never invent a ticket number.
