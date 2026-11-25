---
name: resize
description: Move a repo up or down ion-repo's sizes (tiny, small, medium, large) - what the new size brings or removes shown before the merge, the settings that go with it, ion repo set on a branch, merged. Use when the user asks to change a project's size, or it outgrew its size or is heavier than it needs.
argument-hint: "[tiny|small|medium|large]"
---

Size asked for: `$ARGUMENTS`; without one, propose it from what the project has become. Talk to
the user in their language.

## 1. Where the repo stands

1. Read the size in `.copier-answers.yml` (`size`). An old name is the same notch: `spark` =
   tiny, `ember` = small, `flame` = medium, `blaze` = large (renamed in 0.4.10; `ion repo set`
   converts it).
2. Weigh the notch against what the project is, from its README and backlog:
   - **tiny**: a script, a personal tool, a one-off analysis;
   - **small**: a small app or site, one or two people, low stakes;
   - **medium**: in production with real users, personal data stored, several contributors;
   - **large**: several teams or services, high stakes.
   Storing other people's data or going to production is the usual reason to go up; a project
   that stayed a personal tool, the usual reason to go down. Say which notch fits and why, in two
   lines; the user decides.

## 2. What changes, before anything merges

Branch `chore/ion-repo-resize` in a worktree (skill `/repo:worktree`), clean tree. Run there
`ion repo set size=<new>` together with the settings that go with it, each one asked to the user
first:
- going to **medium** or **large**: `podman=true` (its default there), and for a Django backend
  in production `deploy=vps vps_host=… api_domain=… site_url=… deploy_branch=…`; on a server
  that already runs another project, free ports `vps_port=… vps_db_port=…` (read what listens
  with `ssh <host> ss -ltnp`) and the server's Caddyfile importing `/etc/caddy/sites/*.caddy`;
  look for the host and the domain in the user's other repos (their `.vps/`, `.cloudflare/`
  folders, their docs) before asking;
- going **down**: nothing is switched off without saying so: containers, deployment and the
  rules of the upper notch go, list them.

Then show the user what the notch did, from the diff (`git diff --stat`, then
`git diff .claude/rules/ion-repo/ charter.toml .github/`): the rules added or removed (for medium,
for instance, personal data covered by export and anonymisation in the same change, the frozen
API contract, request correlation, antivirus on uploads), the CI jobs, the containers and the
production files. Ask before going on; on a no, remove the worktree and the branch: nothing
reached `develop`.

## 3. Finish

1. Conflicts (`<<<<<<< before updating`): keep the project's own version of what it built
   (pages, config, README sections), take ion-repo's additions around it, and never a demo the
   template brings to a new project (a health badge, an `/api` proxy that would shadow the
   front's own server routes). A binary file the project replaced (an icon) is kept as it was:
   `git checkout <integration> -- <file>` if the update put ion-repo's back.
2. Commit in batches of 10 files at most, grouped by theme (ion-repo's rules and settings, CI,
   backend, containers, production, docs), then run the same `ion repo set` again: it locks,
   installs and runs every check. Commit the lock files it writes.
3. Update the repo map of the project's `CLAUDE.md` for every folder the notch added or removed
   (`backend/`, `config/vps/`, `scripts/ops/`…).
4. Merge into `develop` (skill `/repo:merge`). Deploying is a separate step, through the
   project's `docs/operations/production.md`.
