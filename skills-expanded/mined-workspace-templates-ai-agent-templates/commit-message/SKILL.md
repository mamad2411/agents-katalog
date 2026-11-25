---
name: commit-message
description: Writes a Conventional Commits message from your staged changes, shows it to you and commits only after you say yes.
disable-model-invocation: true
---

Write a commit message for the staged changes. Extra context from the user: $ARGUMENTS

1. Run `git diff --staged --stat` and then `git diff --staged`. If nothing is staged, stop and say so. Do not stage anything yourself.
2. Run `git log -n 10 --oneline` and copy the project's habits for scope names and tense.
3. Pick one type: feat, fix, refactor, perf, docs, test, build, ci, chore. If two types fit, the diff is probably two commits: say so and propose the split by file.
4. Write the subject as `type(scope): summary`, imperative mood, lower case, no period, at most 72 characters. Use the scope or ticket id from the user's text when given.
5. Add a body only when the reason is not obvious from the subject. Explain why the change was needed and any trade-off, wrapped at 72 columns. Add `BREAKING CHANGE:` in the footer if a public interface changed.

Show the message in a code block, then ask: "Commit with this message?" Run `git commit` only after a clear yes. Never use --no-verify and never amend an existing commit.
