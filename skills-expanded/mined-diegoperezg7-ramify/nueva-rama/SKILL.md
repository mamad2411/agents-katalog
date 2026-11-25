---
name: nueva-rama
description: Start the current task on a branch and folder of its own (a ramify worktree) instead of the shared branch. Use when the user asks to start a task, a feature or a fix on its own branch.
argument-hint: "[what the task is]"
disable-model-invocation: true
---

# Start a task on its own branch

One task, one branch, one folder: the agent never works on the shared branch, so parallel agents never overwrite each other.

1. Pick a conventional branch name from the task in `$ARGUMENTS` (ask in one line if it is empty):
   - `feat/<short-topic>` for something new, `fix/<short-topic>` for a bug, `docs/`, `refactor/`, `test/`, `chore/` otherwise.
   - lowercase ASCII, words joined with `-`, at most 5 words: `feat/magic-link-login`.
2. Create it from the current repository (it copies `.worktreeinclude` files, reserves ports and runs the project setup):

   ```bash
   NO_COLOR=1 "${CLAUDE_PLUGIN_ROOT}"/bin/ramify new "<branch>" --no-launch
   ```

   The last line printed is the new folder.
3. Tell the user, in two lines: the branch, the folder, and how to continue there
   (`cd <folder> && claude`, or reopen this session in that folder). Read its `.worktree.env`: dev servers must use
   `PORT` to `PORT+9`.

If the command says the branch or folder already exists, offer `ramify open <branch>` instead of creating another one.
Never switch the main checkout to the new branch with `git checkout`: that folder belongs to the shared branch.
