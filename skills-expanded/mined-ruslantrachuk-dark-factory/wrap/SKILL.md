---
name: wrap
description: >
  Wrap up a built, green branch: a note on the bd task, the project documents brought in line, the phase ticked in
  tasks.md and the PR description in its three sections. Use when the code of a feature or phase is done and reviewed
  ("wrap up", "write the PR description"), and as the rules of the feature pipeline's wrap-up step. Next: CI, then
  scripts/merge-feature.sh.
---

# Skill `wrap` — the record of the work

> Part of the dark-factory plugin. The PR is the record of work (`AGENTS.md`, operating contract):
> `scripts/merge-feature.sh` refuses a PR without the three sections and writes the description into the merge commit.

## Steps

1. **bd** (a project with a bd queue; without one, skip to step 2). The phase task stays `in_progress` — `scripts/merge-feature.sh` closes it after the merge, finding it by
   the branch (tracker ID or slug). Add a note on what was done and where it stopped:
   `bd update <id> --append-notes "…"`. Done subtasks are closed; undone ones stay open with a note. No bd task at all
   (a hand-run small change) — create one with `--acceptance`, label it `change:<slug>` (and `external_ref` = the
   tracker ID) so the merge finds it. bd commands run with `timeout 60`: bd can hang on a database lock — on a timeout
   retry once, then name it under Open questions. The queue lives outside git: nothing about it is committed.
2. **Project documents** — only those the change touched (`AGENTS.md` §Finishing a feature): `ARCHITECTURE.md`
   (layers, model, endpoints), `naming.yaml` (entities and terms), `CODING_STANDARDS.md` (new rules), `README.md`
   (quickstart, settings), `docs/user-guide/` when the project has one and a screen changed, an ADR for a decision that
   shapes the architecture. Nothing touched — say so in `## Done`.
3. **`tasks.md`** of the OpenSpec change, when the work has one — tick the phase's finished items. **The pyramid bar** — when the project has
   `scripts/pyramid.py` and the branch raised the base share of its profile, write it:
   `scripts/pyramid.py --write-baseline` (the profile stays the declared one). The bar only rises with merges.
4. **The PR description**, three sections, each with text:
   - `## Done` — what the change does now: behaviour, not file names; test counters from the real run (the db lane
     named as CI's when it did not run here);
   - `## Decisions` — the choices and why, including the assumptions made along the way ("decisions the machine made
     for you") in plain language and the review remarks accepted as known consequences;
   - `## Open questions` — what is left (undone slices, review blockers), each follow-up as a bd task with its id
     (or an issue, without a queue); "none" if nothing is.
   The description goes to the PR (`gh pr edit --body-file -`, or the run returns it); it is not a file and is not
   committed.
5. **Commit** the documents, `tasks.md`, the pyramid baseline and the ADR as their own commit on the branch, with the message rules of
   `integrate`. No push from a pipeline run.

Next: push, green CI, your own review, then **`scripts/merge-feature.sh <branch>`** where the project has it (otherwise
the project's own merge path, the description becoming the merge message).
