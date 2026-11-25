---
name: review
description: Reviews a branch's commits and diff before public: messages, authorship, trailers, stray files, secrets, fixups; tidies history. `--repo`: whole repo. Run by /repo:merge, /repo:release; use if asked whether it is clean.
argument-hint: "[branch | --repo]"
---

Branch: `$ARGUMENTS`, else current. Integration branch: per project `CLAUDE.md`, else `develop` if it exists, else `origin`'s default. Merged and pushed commits are public forever; the branch is the last place to fix them. Talk in the user's language.

## 1. Gather
    git fetch -q --prune origin
    git log --reverse --format='%h%x09%an <%ae>%x09%s%n%b' origin/<integration>..<branch>
    git diff --stat origin/<integration>...<branch>
    git diff origin/<integration>...<branch>

Conventions: project `CLAUDE.md` (commit rules, repo map), `CONTRIBUTING.md`, `git log --no-merges --format=%s -30 origin/<integration>` (language, scopes, tone).

## 2. Commits
- **Subject**: `type(scope): summary` (`!` if breaking), history's language, under 72 chars, what changes not how; no `wip`, `test`, `oops`, `fix typo`, `update`, `.`, bare file name.
- **Body, trailers**: no `Claude-Session:`, no "Generated with"; `Co-Authored-By: Claude` only if the machine discloses (`ion repo set ai_trailers`, default `disclose`; branch guard refuses it under `never`); breaking says `BREAKING CHANGE:`.
- **Author**: user's usual identity here (`git config user.name/email`, history), never a placeholder or machine address; an outside contributor keeps theirs.
- **Shape**: atomic, task files only. Fold in: `fixup!`/`squash!`, a commit fixing or reverting one of the same branch, duplicate subjects, formatting churn after the real change.

## 3. Diff
- No secret or real personal data: `git log -p origin/<integration>..<branch> | gitleaks stdin` if installed (a worktree-moved session refuses `gitleaks git`); else read for keys, tokens, `.env`, e-mails, phones.
- No stray: debug output, `*.orig`, `*.rej`, `.DS_Store`, local `.<service>/`, large binary, lockfile without its manifest.
- No leftover: conflict markers, debug `print`/`console.log`, commented code, `TODO` without ticket, test skipped without reason.
- No change outside the task (reformatted untouched code, unrelated file).
- Present: repo map if a folder or entry point moved, backlog ticket, required docs or `CHANGELOG.md`, the change's tests.

## 4. Tidy
Report first, short list: fine, wrong, proposed fix.

Rewrite only this branch, never integration, `main` or a tag, and only if nobody builds on it: not on `origin` (`git ls-remote --heads origin <branch>` empty), or the user's own with no open PR from someone else. Pushed branch: only with the user's yes, then `git push --force-with-lease origin <branch>`. Otherwise report without rewriting.

Note the tip (`git rev-parse <branch>`), then from the branch's worktree, never interactive (`GIT_EDITOR=true` before each rebase):
- fold: `git commit --fixup=<sha>` (or existing `fixup!`), then `git rebase --autosquash origin/<integration>`;
- reword: `git commit --allow-empty -m "amend! <current subject>" -m "<new message>"`, same rebase (`--fixup=reword:` refuses `-m`, opens an editor);
- stray file: `git rm --cached <file>` in a fixup of the commit adding it, pattern in `.gitignore` if it can return;
- secret already pushed: stop, user revokes first; rewriting does not unpublish it.

After: `git diff <old tip> <branch>` empty unless a file was meant to go; history meets section 2. Published commits are not rewritten: say what is wrong and what prevents it next time (rule, hook, `/repo:report`).

## 5. `--repo`: before a release
- **Published commits** (`git log <previous tag>..<candidate>`): section 2; not rewritable, `CHANGELOG.md` says what a poor subject hides.
- **Remote branches**: `git branch -r --merged origin/<integration>`, others via `git for-each-ref --sort=-committerdate refs/remotes/origin --format='%(refname:short) %(committerdate:relative) %(subject)'`: abandoned, open PR, in progress. Propose deleting merged, closing or finishing abandoned; delete nothing on GitHub without yes.
- **Merged local branches, worktrees**: `/repo:cleanup`.
- **Unmerged worktrees, local branches**: list with last commit age and uncommitted changes; flag untouched over two weeks or uncommitted as likely forgotten. Ask for each (finish, keep, delete with yes). Warning only: never blocks the release.
- **Tags**: well formed (`vX.Y.Z`, `-rc.N`), none on a commit outside `main` or a release branch.

## 6. Summary
In the `repo` plugin's `debrief` format (`output-styles/debrief.md`), its result sentence the verdict: clean, tidied, or to fix by the user. Inside `/repo:merge` or `/repo:release`: the verdict in one line, the debrief at their end.
