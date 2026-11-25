---
name: worktrees
description: Rules for working inside an ramify git worktree. Use whenever the project root has a .worktree.env file, or before starting a dev server, running xcodebuild, switching branches, merging or pushing.
---

# Working in an ramify worktree

In a repository's main checkout on its default branch, do not edit files: call the EnterWorktree tool first with a short
conventional name for the task (`feat-login`, `fix-cart-total`). ramify creates the branch (`feat/login`) and its folder,
and you continue there. Edits on the shared branch are blocked unless the user ran `git config ramify.allowMain true`.

If `.worktree.env` exists at the project root, this is an isolated git worktree, one per task, and other agents are working on other branches of the same repository at the same time.

- Work only on the branch in `WT_BRANCH`. Never check out another branch or main: it is checked out in another worktree and git will refuse.
- Read `.worktree.env` first. Dev servers must use ports `PORT` to `PORT+9`, never the main project's ports.
- For xcodebuild always pass `-derivedDataPath "$DERIVED_DATA"`. If `SIM_UDID` is set, use `-destination "id=$SIM_UDID"`.
- Never commit `.worktree.env`. Do not merge into main or push to main: the user decides that from `ramify ui` or the terminal.
- `"${CLAUDE_PLUGIN_ROOT}"/bin/ramify ls` shows every worktree of the repository, its agent and whether it is running.
- Before editing files another agent may be changing, run `"${CLAUDE_PLUGIN_ROOT}"/bin/ramify who <files>` (the `coordinar` skill): it exits 1 and names the branch when another worktree changes them.
- When the task is done, commit and run `"${CLAUDE_PLUGIN_ROOT}"/bin/ramify ready`: it brings the base in and marks the branch ready to merge. Exit 1: uncommitted changes, or a branch marked ready before changes the same files (wait or agree, then run it again); exit 2: the base conflicts with the branch (files listed): merge it, resolve, commit and run it again. When the base moves, `ramify ls` shows READY `stale` and you are told on your next prompt: run it again.

If the session did not start inside the repository (EnterWorktree then has no repository to branch from), run
`"${CLAUDE_PLUGIN_ROOT}"/bin/ramify new <feat/...> --no-launch` from the repository and call EnterWorktree with the
`path` it prints.
