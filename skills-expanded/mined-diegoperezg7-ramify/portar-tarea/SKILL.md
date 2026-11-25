---
name: portar-tarea
description: Move uncommitted work from the repository's main checkout (the shared branch) to a branch and folder of its own, leaving the main checkout clean. Use when work was started on main by mistake.
argument-hint: "[branch name]"
disable-model-invocation: true
---

# Move work off the shared branch

Use this when changes were made directly in the main checkout (on `main` or the default branch) and should live on a branch of their own.

1. Check where you are:

   ```bash
   git rev-parse --show-toplevel; git branch --show-current; git status --short
   ```

   - If `.worktree.env` exists at the top, this is already a worktree: stop and say so, nothing to move.
   - If there are no changes, say so and offer `/ramify:nueva-rama` instead.
2. Choose the branch: `$ARGUMENTS` if given, otherwise a conventional name from what the changes do
   (`feat/…`, `fix/…`, `refactor/…`), lowercase, words joined with `-`. Show it and the list of changed files.
3. Move the work. It stashes everything (untracked files included), creates the branch and folder from the commit the
   work started on, applies the changes there and leaves the main checkout clean. A copy stays in the stash.

   ```bash
   NO_COLOR=1 "${CLAUDE_PLUGIN_ROOT}"/bin/ramify move "<branch>" -a claude
   ```

   The last line printed is the new folder.
4. Confirm with `git -C <folder> status --short` that the changes arrived, and tell the user:
   - the branch and folder, and to continue there (`cd <folder> && claude`);
   - that the main checkout is clean;
   - that a copy stays in `git stash list` ("ramify: moved to <branch>") until they drop it.

If `ramify move` reports that the changes did not apply, they are back in the main checkout: report the message and stop.
