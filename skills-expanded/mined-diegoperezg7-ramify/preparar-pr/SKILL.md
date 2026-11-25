---
name: preparar-pr
description: Get the current branch ready for review and open a draft pull request on GitHub, following good practice (up to date with the base, small, conventional commits, a clear description).
disable-model-invocation: true
---

# Prepare a pull request

Run this from the branch's own folder (a ramify worktree), never from the main checkout on the default branch.

1. Where are we:

   ```bash
   git branch --show-current
   BASE=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##'); BASE=${BASE:-main}; echo "$BASE"
   git status --short
   git log --oneline "$BASE"..HEAD
   git diff --shortstat "$BASE"...HEAD
   ```

   Stop and say why if the branch is the base branch, or there are no commits ahead of the base.
2. Uncommitted changes: show them and ask whether to commit them. Commit with a conventional message
   (`feat: …`, `fix: …`, `docs: …`, `refactor: …`, `test: …`, `chore: …`; imperative, under 72 characters).
3. Up to date with the base and no clash with the other finished branches:

   ```bash
   NO_COLOR=1 "${CLAUDE_PLUGIN_ROOT}"/bin/ramify ready
   ```

   It fetches and merges the base and marks the branch ready to merge. Exit 1: another branch marked ready changes
   the same files (listed): stop and tell the user which branch and files; run it again once that one is merged.
   Exit 2: the base conflicts with this branch (the merge was undone; files listed): stop and tell the user which
   files collide.
4. Size: if the diff is over ~400 changed lines, say so and suggest how to split it before going on (ask; do not split on your own).
5. Push and open the draft:

   ```bash
   git push -u origin HEAD
   gh pr create --draft --base "$BASE" --title "<conventional title>" --body "<body>"
   ```

   Body: **What** (one paragraph), **Why**, **How to test** (steps), and the list of commits. No marketing, no emojis.
6. Give the user the pull request URL. It stays a draft until they mark it ready.

Needs the `gh` CLI signed in (`gh auth status`); if it is not, say so and stop after the push.
