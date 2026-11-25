---
name: ship-pr
description: Finish a Devcules module. Runs the checks, commits with a DCO sign-off on the users/kiran/ branch, pushes, and opens a PR that closes the issue. Never merges. Use when the work for the current issue is done and should go up for review.
---

# Ship the current module as a PR

1. **Branch check.** Run `git branch --show-current`. It must start with `users/kiran/`, and it must not be `main`. If you're on `main`, stop: never commit there.
2. **Checks.** Run every check in AGENTS.md ("Before opening a PR") that applies. If any fails, fix it and run it again. If a check can't run (a tool is missing), note it for the PR's Notes section; don't skip it silently.
3. **Review the change.** Run `git status` and `git diff`. Stage only the files that belong to this module, with `git add <paths>`. Then run `git diff --staged --stat` and confirm:
   - no secrets, `.env` files or local data,
   - no file over 1 MB,
   - nothing outside the module's scope.
4. **Commit.** Use `git commit -s -m "<type>(<module>): <summary>"`, in Conventional Commits format with the module as scope. Several small commits are fine.
5. **Push.** Use `git push -u origin HEAD`. Never use `--force`.
6. **Open the PR.** Use `gh pr create --base main --title "<Module>: <what it adds>" --body-file <tmpfile>`, with the body template from AGENTS.md. Fill in:
   - `Closes #<issue>`,
   - the test gate with only verified items ticked,
   - the exact Verify commands and their real output,
   - Notes for anything unverified.

   Copy the issue's labels with `--label`.
7. **Stop.** Print the PR URL and the CI status (`gh pr checks --watch` until done, if it finishes within a few minutes). Don't merge, approve or start the next issue.
