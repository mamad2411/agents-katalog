---
name: ship
description: Commit, push and open the pull request for a change in this repo, after the local gate passes. Use when the user says "abre o PR", "ship", "commita e sobe", "open the PR" or the work on a branch is done and approved.
---

# Ship a change

Opens one PR for one change. Stop and tell the user when a step fails; do not
skip it.

1. **Branch.** Never commit on `main`. If on `main`, create
   `<type>/<short-topic>` (`docs/`, `feat/`, `fix/`, `ci/`, `chore/`) first.
2. **Look before staging.** `git status --short`: stage only this change's
   files by name, never `git add -A`. A `.env*` or other file with a real
   secret → stop and say so.
3. **Hooks on.** `git config core.hooksPath` must print `.githooks`; if not,
   set it (CONTRIBUTING, "Commit, push and PR").
4. **Gate.** `sh scripts/check.sh` must pass. It is the same gate as the
   required `validate` check.
5. **Behavior check.** A change to what a skill, agent or reference makes the
   agent do needs a run of `.claude/skills/verify/` (or the user's `/verify`)
   first; say in the PR what was run and what it showed.
6. **Commit.** Conventional Commits with the plugin as scope, as in
   `git log`: `docs(frontend-stack): …`, `fix(taste): …`, `ci: …`. Body: why,
   then what, as short lines or bullets.
7. **Push and PR.** `git push -u origin <branch>`, then
   `gh pr create --base main` with this body:

   ```markdown
   ## Why
   ## What
   ## Evidence   (research sources, verify runs; omit when none)
   ## Checks     (scripts/check.sh output, one line per check)
   ```

8. **After.** Bind the PR to the session when the app offers it, and report
   the link. Merge is the user's.

Upstream content under `plugins/<vendored>/` changes only through
`stack.json` and `scripts/sync.py` (CONTRIBUTING); a hand edit there is a
stop.
