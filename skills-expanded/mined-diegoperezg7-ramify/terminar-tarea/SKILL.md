---
name: terminar-tarea
description: Close a finished task once its branch is merged: check nothing is lost, remove its ramify worktree and branch, and return to the main checkout.
argument-hint: "[branch or worktree name]"
disable-model-invocation: true
---

# Finish a task

1. Which task: `$ARGUMENTS`, or the current worktree if `.worktree.env` exists here (`WT_BRANCH`, `WT_MAIN`).
   Otherwise list the worktrees and ask:

   ```bash
   NO_COLOR=1 "${CLAUDE_PLUGIN_ROOT}"/bin/ramify ls
   ```

2. Check it is really done, from the main checkout (`WT_MAIN`):

   ```bash
   git -C "<main>" fetch --quiet origin 2>/dev/null
   git -C "<worktree>" status --short
   git -C "<main>" log --oneline "<base>".."<branch>"
   gh pr view "<branch>" --json state,url 2>/dev/null
   ```

   - Uncommitted changes, or commits not in the base and no merged pull request: stop and say what is pending.
     If the work is finished, mark it ready to merge from its worktree, so the user sees it in the queue
     (`ramify ls`, READY) and it stays checked against the base and the other ready branches:

     ```bash
     cd "<worktree>" && NO_COLOR=1 "${CLAUDE_PLUGIN_ROOT}"/bin/ramify ready
     ```

     Exit 1: another branch marked ready changes the same files; exit 2: the base conflicts (files listed). Say
     which, and suggest `/ramify:preparar-pr` to open a pull request.
3. Remove it. `ramify rm` refuses when anything would be lost, and deletes the branch only when it is merged:

   ```bash
   cd "<main>" && NO_COLOR=1 "${CLAUDE_PLUGIN_ROOT}"/bin/ramify rm "<branch>"
   ```

4. Tell the user it is gone and remind them that their next task should start on its own branch
   (`/ramify:nueva-rama`). Never use `--force` unless the user asks for it explicitly.
