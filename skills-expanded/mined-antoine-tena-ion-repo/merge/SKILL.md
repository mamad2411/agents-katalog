---
name: merge
description: Finishes work: fast linters on changed files, merge into develop, push, delete branch and worktree, update the repo's plugin. No CI. Use at end of work or when asked to merge.
argument-hint: "[branch]"
---

Branch: `$ARGUMENTS`, else current. Integration branch: per project `CLAUDE.md`, else `develop` if it exists, else `origin`'s default. Direct merge, no PR or approval ([NO-COMMIT-ON-MAIN]); an open PR turns "Merged" at step 4's push. Talk in the user's language.

1. `git status --porcelain` must be empty, else stop and say so. Run `/repo:review <branch>`: pushed commits are public for good. Its tidying happens before merge; what it leaves to the user: tell them, wait for their decision.
   Fast linters in the branch's worktree, only on changed files (`git diff --name-only --diff-filter=d <integration>...<branch>`): `ruff check` and `ruff format --check` on Python, `eslint` on JS/TS/Vue, the like for other languages (ion-repo: `uv run ruff check <files>`, `uv run ruff format --check <files>`). No type checker, test, `ion repo check` or `ion repo ci`: the release runs them. No such file: run nothing. Failure: fix on the branch, never merge red.
2. If moved into the worktree (`EnterWorktree`), leave it now with `ExitWorktree` (`action: "keep"`): an isolated session refuses to merge from the main tree. Then `git pull --ff-only origin <integration>`, then `git merge --no-ff <branch> -m "Merge branch '<branch>' into <integration>"`, from the main tree if on the integration branch, else `git -C` on a worktree that is. Never switch the main tree's branch under another session.
3. Conflict: stop, show files, propose a resolution.
4. `git push origin <integration>`.
5. Delete worktree and branches now, only if both hold, else delete nothing and say which failed and why:
   - `git fetch -q origin`, then `git merge-base --is-ancestor <branch> origin/<integration>` succeeds;
   - `git -C <wt> status --porcelain` empty.
   Then `git worktree remove .claude/worktrees/<name>` (never `--force`), `git branch -d <branch>` (never `-D`), and if on GitHub (`git ls-remote --heads origin <branch>`) `git push origin --delete <branch>`.
6. Repo ships a plugin (`.claude-plugin/marketplace.json` at root; ion-repo and every family tool): update the installed copy, else a just-merged skill stays `Unknown command` in new sessions. For each `<plugin>` listed, under catalog `name` `<market>` (`<tool>@<tool>` for a family tool):
   - `claude plugin list --json`: entries with `id` `<plugin>@<market>`. None: not installed, do nothing.
   - Once, after step 4's push (a GitHub marketplace reclones): `claude plugin marketplace update <market>`.
   - `claude plugin update <plugin>@<market> --scope <scope>` for each scope found, only those: `user` from anywhere; `project`, `local` from the main tree if the entry's `projectPath` is this repo (`cd <projectPath> && …`). Another repo's `projectPath`: leave it.
   - Tell the user to restart Claude Code: plugins load at launch.
   Local-folder plugin (`readFromFolder`, ion-repo here): same commands, harmless if version unchanged.
7. No CI: it runs only on the release branch (`/repo:release`). Report in the `repo` plugin's `debrief` format (`output-styles/debrief.md`). Suggest `/clear` under its **◆ Blocked**, in one line, only after a long session or before an unrelated subject; otherwise say nothing of it.
