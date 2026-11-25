---
name: commit
description: Commit, pull, and push changes using make push with a message prefixed by the work item's number
argument-hint: "<work item number>"
---

Commit the current working tree changes using this project's `make push` target.

`make push` = `make commit` + `git push`. `make commit` alone typechecks, pulls, lints, builds, tests,
stages and commits, but does NOT push — so this skill uses `make push`. The chain is the Makefile's, and this
skill never repeats it step by step: it runs the one command.

The work item's number is: $ARGUMENTS

## 1. Validate the work item's number

If `$ARGUMENTS` is empty or non-numeric, stop and ask the user for the number of the work item on the team's Brigade Board that the change belongs to (e.g., `/commit 270`). Do not proceed, and do not invent a number.

## 2. Analyze changes

Run these commands in parallel to understand what will be committed:

- `git status` (never use `-uall`)
- `git diff`
- `git diff --cached`
- `git log --oneline -5`

If the working tree is clean (no staged, unstaged, or untracked changes), there is nothing to commit. If `git status` also says the branch is ahead of origin (a merge you concluded, or commits not yet pushed), `make push` would run its whole chain and stop at "nothing to commit": run `make pull`, then `git push`, and report that. Otherwise inform the user there is nothing to commit and stop.

Remember: `make push` runs `git add --verbose :/ .` before committing, so ALL working tree changes will be included, not just staged files. It also runs `git pull` BETWEEN typecheck and lint, so lint, build and test run against the MERGED tree rather than a stale one.

## 3. Check for secrets

Scan every added line (`+` prefix) in the diff output — in ALL files, not just code files — for anything that looks like a secret: API keys, passwords, tokens, connection strings, private keys, or credentials. Non-code files (markdown, prompts, config notes) are just as likely to contain secrets. If found, warn the user and do not proceed until they confirm the files are safe.

## 4. Generate the commit message

Based on the changes, write a commit message:

- Format: `<work item>: <Message>` (e.g., `270: Let the commit skill run without asking for approval`)
- One line, under 72 characters when possible
- Imperative mood, capitalized first word after the number
- Summarize the intent (why), not a list of files changed
- Avoid shell-special characters (quotes, backticks, dollar signs) in the message

## 5. Execute

Do not ask the user to approve the commit (owner ruling, 2026-11-12). Print the command, then run exactly:

```
make push "message=<work item>: <generated message>"
```

This typechecks, pulls, lints (`make lint`), builds, tests, stages, commits and pushes, in that order. A step that fails stops the chain: none of the work is staged, committed or pushed, and the merge of origin, when there was one, stays. The only stops before it are the ones in steps 1 to 3.

## 6. Report the result

- On success, confirm the commit was pushed.
- On a build error, a test failure or a lint issue, report the error clearly. Do not retry automatically.
- A merge conflict is not a failure to report and leave: it is yours to resolve in place, by the steps of
  `docs/agent/repository/conventions.md` ("A merge conflict is the session's to resolve, in place"). The pull
  inside `make push` either stops in a merge with markers, or refuses because an uncommitted change would be
  overwritten; the rule has the steps for each. Never `git merge --abort`, never a rebase, never a force-push.
  Ask the user only when what one side meant cannot be told.
