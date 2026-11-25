---
name: hades-learn
description: Run the HADES learning loop for a team - lessons, CONTEXT.md digest, decisions, team skills, role notes, team.json, promotion to org and company - then commit the vault. --migrate finishes a team migrated from HADES v1.
when_to_use: The owner asks HADES to learn from a task, from notes, to re-learn a project, or to finish the v1 migration of a team (/hades-learn <team> --migrate).
argument-hint: "<team> [task-id | relearn | --migrate | notes]"
---

# /hades-learn - learning loop

`hades` = `node {{HADES_HOME}}/bin/hades.mjs`; vault = `{{HADES_VAULT}}`. Never ask the owner.

1. Team: `hades team resolve <first token>`, else `hades team resolve <cwd>`. Mode, from `$ARGUMENTS`:
   - `--migrate` -> migrate mode (the team was converted by `hades migrate`; no task, strip the flag);
   - a `<team>-NNN` -> that task; `relearn` -> relearn mode; else the most recent task in
     `hades task list <team>`; none -> relearn mode.
2. Remaining text = owner notes: append them verbatim to that task's README.md Lessons section
   (`owner: ...`); no task -> put them in the Assignment line. `--migrate` and `relearn` are never notes.
3. Migrate mode only, before the spawn: `git -C {{HADES_VAULT}} status --porcelain -- <team_dir>`.
   Every listed file without a `hades-migrate` marker that is not a `.v1.md` has uncommitted changes
   that predate the migration: name them in the Assignment as "do not touch: <paths>".
4. Spawn `hades-knowledge-curator`:
   ```
   HADES task <task-id | none> | team <team> (org <org>) | stage close
   Task folder: <task folder, or none>
   Team folder: {{HADES_VAULT}}/<team_dir>/
   Project: <abs project_path>
   CLI: node {{HADES_HOME}}/bin/hades.mjs
   Read: README.md, state.json, defects.json, stage Summaries (when a task is given); migrate: TEAM.md, agents/*.v1.md
   Assignment: learning loop per {{HADES_HOME}}/playbooks/knowledge-capture.md [+ relearn mode | + migrate mode; do not touch: <paths>]
   Done when: OUTPUT lists every vault file changed or deleted (absolute paths); migrate: no `hades-migrate` marker and no .v1.md left
   ```
5. Verify: the OUTPUT files exist (deleted ones do not); migrate mode also
   `Grep -rln "hades-migrate" <team_dir>` finds only the do-not-touch files, and `hades team resolve <team>` exits 0.
6. `git -C {{HADES_VAULT}} add -A -- <OUTPUT files> <task README.md, if a task>` (`-A` stages
   deletions; a deleted file that was never committed makes git refuse: drop it from the list);
   commit `learn(<team>): <one line>` (migrate: `learn(<team>): finish v1 migration`) per
   `{{HADES_HOME}}/company/commit-policy.md`. Never push.
7. Report: one line per file changed or deleted, what was learned; migrate: files left untouched.
