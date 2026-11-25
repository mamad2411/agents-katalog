---
name: pr-checklist
description: Runs tests, lint and type checks, hunts leftover debug code and trims the diff before you open a pull request.
disable-model-invocation: true
---

Check this branch is ready for a pull request. Base: $ARGUMENTS (main if empty).

1. Get the change set: `git diff --stat <base>...HEAD` and the full diff. Note files changed and lines added.
2. Run the project's test, lint and type-check commands (read package.json scripts, Makefile, pyproject). Record pass or fail with the first failing message.
3. Search added lines only for: console.log, print(, debugger, FIXME or HACK notes you introduced, commented-out code, .only or .skip in tests, hardcoded URLs and keys.
4. Flag unrelated changes: whitespace-only edits, lockfile churn without a manifest change, files outside the task.
5. Check docs: does a changed public function, flag or endpoint appear in the README or docs, and is there a changelog entry if the repo keeps one?
6. Confirm commits are readable and no merge commits sit in the branch.

Output a checklist with pass, fail or n/a, each fail with file:line. Then suggest a pull request title and a three-line description. Ask before fixing anything; never push.
