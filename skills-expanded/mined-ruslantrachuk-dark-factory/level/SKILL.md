---
name: level
description: Show the project's level on the dark-factory ladder (0 solo kit, 1 base template, 2 provisioned server, 3 client modules, 4 team) from evidence in the project, the signals for the next level and what would change; when the human names the change (/dark-factory:level <level>) and says yes, write FENCE_LEVEL (up or down) or name the skill that takes a structural step. Invoked by the human as /dark-factory:level.
argument-hint: "[solo|standard|team] [--fail-closed 0|1]"
disable-model-invocation: true
---

# /dark-factory:level — where the project is on the ladder

The ladder is the dark-factory repository's `docs/levels.md` (https://github.com/ruslantrachuk/dark-factory/blob/main/docs/levels.md). The mechanics are one script,
`${CLAUDE_PLUGIN_ROOT}/scripts/level.py`; this skill is the report, the proposal and the "yes".

## Rules

1. **The human decides.** Propose one step; change nothing without an explicit "yes" to that step.
2. **Fence steps are written by the script, and only on the human's own command naming the change.**
   `.claude/fences.env` is fenced at every level: deleting, moving or truncating it and lowering `FENCE_LEVEL` with
   Edit/Write run only with the human's yes in the permission dialog (denied where nobody can answer). `level.py set <level> [--fail-closed 0|1] --apply` writes it, and only after the
   human typed `/dark-factory:level <level> [--fail-closed 0|1]` with exactly that change: the plugin records that
   prompt as a grant bound to the change, valid 10 minutes, used once. A bare `/dark-factory:level` is a read-only
   report and grants nothing; a terminal grants nothing. If the script refuses, ask the human to type the command
   with the change they want; do not look for another way to write the file, and never book that command through a
   scheduled run, another session or `claude -p` (the guard denies it).
3. **A lower level binds once it is on the main branch.** The guard reads the stricter of the working tree's
   `.claude/fences.env` and the one on origin's main branch: moving down takes effect after the change is merged
   (at `team`, after a reviewer's approval). Say so when proposing a step down.
4. **Structural steps are named, never run here.** Adding base or a module and provisioning a server are
   other skills with their own dry runs and "yes": tell the human which one to run and where.

## Steps

1. Report:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/level.py" status
   ```
   Show it to the human in short: the level, the evidence behind it, gaps at this level, and for the next level what
   it adds, how it is taken and the signals seen (none seen is fine: the human may know their situation better).
2. Propose **one** step, the first that applies:
   - a gap in the fence at this level (for example base deployed but `FENCE_LEVEL=solo`, or level 2 without
     `QUOTA_FAIL_CLOSED=1`) → the fence step;
   - an argument (`solo`, `standard`, `team`, optionally `--fail-closed 0|1`) → that fence change, up or down;
   - otherwise the next level's step.
3. **Fence step** (any direction). If the human ran `/dark-factory:level` without the change, propose it and ask
   them to type `/dark-factory:level <level> [--fail-closed 0|1]`. Then the dry run, and after their "yes" (within
   10 minutes of that prompt) the same command with `--apply`:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/level.py" set <solo|standard|team> [--fail-closed 0|1]
   ```
   Moving down: say what is dropped (the dry run lists it) and that it binds once merged into the main branch. For
   `team`, also recommend GitHub branch protection on the main branch (a pull request with 1 approval, no force
   pushes, no admin bypass). The human sets it: the guard denies branch-protection and ruleset changes to the
   agent at every level. Point them at the repository's Settings → Branches (or Rules), or give them this command
   to run themselves:
   ```bash
   gh api -X PUT repos/<owner>/<repo>/branches/<main>/protection --input - <<'JSON'
   {"required_status_checks": null, "enforce_admins": true,
    "required_pull_request_reviews": {"required_approving_review_count": 1},
    "restrictions": null, "allow_force_pushes": false, "allow_deletions": false}
   JSON
   ```
   Afterwards: `.claude/fences.env` is a tracked file; it reaches the main branch like any change (a branch and
   `scripts/merge-feature.sh <branch>`, or the human pushes it).
4. **Structural step.** Tell the human what to run; do not run it:
   - **0 → 1**: `/dark-factory:add base` in the project (its conversion mode for a project that already has code). It
     asks whether the project has production (then releases by tag come with base). From level 0 it keeps the
     existing solo `.claude/fences.env` and `.githooks/pre-push`; then the human types `/dark-factory:level standard`.
   - **1 → 2**: on the server, `/dark-factory:provision-server` (`fleet.py provision`); then the human types `/dark-factory:level <current level> --fail-closed 1` (the level stays as it is) to write `QUOTA_FAIL_CLOSED=1`.
   - **2 → 3**: one module at a time, `/dark-factory:add on-call`, `/dark-factory:add monitor`,
     `/dark-factory:add observability`; the catalog with "when it is time" is `.harness/modules.md` in a base project.
   - **1, 2 or 3 → 4**: the fence step to `team` (step 3) plus branch protection, which the human sets. A server
     is not required for level 4.
   Structural steps down (removing a module, leaving the server) follow the module's manifest or the
   `provision-server` skill; this command only moves the fence down.

## Not this command

`/dark-factory:init` sets up level 0. The agent may mention a next-level signal once (the plugin prints one line at
session start when it sees one), but it never moves a project up or down by itself.
