---
name: adopt
description: Bring a repo that ion-repo did not generate to the level of ion repo new (ion repo adopt) - Claude rules, charter, pre-commit, CI, backlog, ion repo update afterwards - without overwriting a file, on a branch then merged. Use when the user asks to adopt ion-repo in an existing repo.
---

Talk to the user in their language.

1. The open repo does not follow ion-repo yet: no `.copier-answers.yml` (generated or adopted:
   skill `/repo:update`); otherwise say so and stop. A `charter.toml` without answers is a repo
   adopted before kiln 0.4.6: `ion repo adopt` completes it. The `ion-repo` command is installed
   (`ion-repo --version`); otherwise give `uv tool install ion-repo` and stop.
2. Ask for the size with the AskUserQuestion tool: `tiny` (script, personal tool), `small` (small
   app, low stakes, the default), `medium` (production, real users), `large` (several teams, high
   stakes).
3. Branch `chore/ion-repo-adopt` in a worktree (skill `/repo:worktree`), then
   `ion repo adopt --size <size>` in that worktree. It renders the template with the stack it finds
   in `backend/` and `frontend/` and lays every file the repo lacks; the files the repo has, and
   its code folders, go under `kept` in `.copier-answers.yml` and are never written by ion-repo.
4. Fill in the repo map of the new `CLAUDE.md` from the actual tree (its entry points, its
   folders), and say which kept files differ from the template the most (a README, its own CI):
   the user decides whether to bring them closer.
5. The debt the charter finds (a `Dockerfile`, a `pip install`…): show it and let the user choose,
   rule by rule, between fixing it now, removing the rule from `charter.toml`, or writing the fix
   down as a ticket (skill `/repo:backlog`). Fix nothing without agreement.
6. Commit (`chore: adopt ion-repo`), then merge (skill `/repo:merge`).

## Sum up

In the `repo` plugin's `debrief` format (`output-styles/debrief.md`): the stack found and the
debt left among its points; two frameworks at the root, one taken and the other given the
common part only, is one of them.
