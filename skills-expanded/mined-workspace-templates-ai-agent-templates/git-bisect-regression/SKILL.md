---
name: git-bisect-regression
description: Finds the exact commit that introduced a regression by running git bisect with an automated test, then explains what that commit changed.
---

# Git bisect regression

Find the first bad commit with a script, not by eye.

## Steps

1. Pin down the failure and the range. Ask for a known good commit or tag if the user has not named one; if they have none, probe older tags until the check passes.
2. Write the check as a command that exits 0 when the code is good, 1 when bad, and 125 when the commit cannot be tested (does not build, missing dependency). Prefer an existing failing test: `npm test -- -t "name"`, `pytest path::test`, `go test -run Name`. Otherwise a small script in a temp file outside the repository.
3. Validate the check before starting: it must fail on the bad commit and pass on the good one. A check that is flaky gives a wrong answer, so run it three times on each end.
4. Make sure the working tree is clean (`git status`) and note the current branch.
5. Run: `git bisect start <bad> <good>`, then `git bisect run ./check.sh`. Include dependency install or build inside the script when the commits change them.
6. Read the result with `git show <sha>` and the message. Check the diff really explains the failure; if the culprit is a merge commit or a huge squash, bisect again inside it with `--first-parent` off.
7. Always finish with `git bisect reset` so the repository returns to the starting branch.

## Rules

- Never fix the bug inside the bisect session.
- Do not edit tracked files while bisecting.

## Report

Culprit commit, author, date, the lines that matter, the number of steps taken and the check command, so the user can rerun it.
