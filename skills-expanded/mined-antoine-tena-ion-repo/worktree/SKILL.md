---
name: worktree
description: Create a work branch in a ready-to-use git worktree. The normal way to start a branch, so as not to cross another session in the main tree.
argument-hint: "<type/branch-name>"
---

Branch asked for: `$ARGUMENTS` (`feat/…`, `fix/…`, `chore/…`, like the repo's history). Without
an argument, propose one from the task.

1. Find the root of the repo (`git rev-parse --show-toplevel` of the main tree) and its
   integration branch: the one the project's `CLAUDE.md` names, otherwise `develop` if it exists
   on `origin`, otherwise the default branch (`git symbolic-ref refs/remotes/origin/HEAD`).
2. From the root, never switching the branch of the main tree: `git fetch -q origin
   <integration>`, then `git worktree add --no-track .claude/worktrees/<name> -b <branch>
   origin/<integration>` (`<name>` = the branch with `/` replaced by `-`). Without `--no-track`,
   the branch would track `origin/<integration>`: a bare `git push` refused, a `git pull` that
   pulls the integration branch. If the branch already exists, attach it without `-b`. Check
   that `.claude/worktrees/` is ignored by git; otherwise add it to `.git/info/exclude`.
3. Prepare the worktree: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/prepare-worktree.sh" <path of the
   worktree>` (copies the ignored `.env*` files of the main tree, installs the dependencies of
   each `pnpm-lock.yaml` / `package-lock.json`). If the repo also provides
   `.claude/worktree-setup.sh`, run it next with the same argument.
4. Move the session into it with Claude Code's `EnterWorktree` tool (`path` = the worktree):
   the status line, the hooks and the relative paths then describe the branch being worked on,
   not the main tree's integration branch. Without that tool, work only in the worktree
   (absolute paths). Give its path. Claude Code's isolation then refuses a command it cannot read
   (a variable even in a plain path, a heredoc, `cd`, a loop, `$(…)`, `git -C`, several commands chained around git): send git commands plain
   and one by one, and put the rest in a script.
