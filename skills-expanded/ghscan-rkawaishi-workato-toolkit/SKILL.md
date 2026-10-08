---
description: Start, stop, or restart Workato recipes and view their run state, independently of push. Dev-only for mutations; on test/prod profiles it switches to guidance instead of executing. Japanese prompts are also supported.
allowed-tools: Bash, Read, Glob, Grep
disable-model-invocation: true
---

# /run-recipes

Recipe run control as a first-class operation (spec S6-1〜S6-4): see what is running,
start/stop/restart without a push, and hand start failures to the diagnose loop.

## Usage

- `/run-recipes` — run-state overview of the current project (= `status`, read-only)
- `/run-recipes status [--project <name>]` — same, for a specific project
- `/run-recipes start|stop|restart --id <id>` — one recipe
- `/run-recipes start|stop|restart --all [--project <name>]` — every recipe in the project

## 0. Environment guard (mandatory before any start/stop/restart)

Resolve the active profile first:

```bash
python3 scripts/workato-api.py profile show
```

- **`status` is read-only and allowed against any environment.**
- **start / stop / restart are dev-only.** If the resolved profile name does not end
  with `-dev`, do **not** attempt the operation — switch to the prod-boundary guidance
  below. The plugin's PreToolUse hook and the helper's built-in dev guard would refuse
  anyway; they are the last line of defense, not the UX. This skill hands over *before*
  they fire.

### Prod boundary guidance (S6-3 — when asked to start/stop on test/prod)

Recipe control in test/prod is **always a human action in the Workato UI**
(the agent's test/prod API keys are read-only by design). Print, in one message:

1. **Why**: per-environment capability design — the agent can only mutate dev;
   test/prod changes go through the Deploy feature.
2. **What to operate**: the exact recipe name(s) and ID(s) (from `status`, which
   still works read-only).
3. **Where**: the direct recipe URL(s) built from the ID — e.g.
   `https://app.workato.com/recipes/<id>` (adjust the host for the org's region and
   pick the target environment in the UI's environment switcher) — plus the
   navigation fallback: target environment → project → recipe → *Stop recipe* /
   *Start recipe*.
4. **What comes next**: if this is incident containment, the fix itself follows the
   hotfix path — fix in dev (`/diagnose-jobs`), then re-promote via `/deploy-project`
   (dev→test→prod, checklists included). There is no shortcut that edits prod directly.

## 1. status (default)

```bash
# folder_id comes from .workatoenv (with --project: `workato projects use "<name>"` first)
python3 scripts/workato-api.py recipes list --folder-id <folder_id>
```

Present a table: `ID / name / running|stopped / last job outcome`. For the last-job
column, query per recipe (`jobs list --recipe-id <id> --limit 1`) — on a large project
this is one call per recipe, so fetch it for the recipes the user cares about (or when
the list is small) and say when the column was skipped. Then flag anything suspicious:

- **Stopped but should be running** (e.g. it was pushed and started earlier, or other
  recipes in the same project run): call it out as a possible start failure and offer
  `/diagnose-jobs` (start-error entrance).
- Filter with `--status running` / `--status stopped` when the list is long.

## 2. start / stop

Always via the helper — it carries the dev guard and `--dry-run`:

```bash
python3 scripts/workato-api.py recipes start <id>
python3 scripts/workato-api.py recipes stop <id>
```

- `--all`: run `recipes list --folder-id <folder_id>` first, then loop over the
  returned IDs one by one (the helper takes a single recipe per call).
- Never wrap the raw CLI for this; the helper is the guarded path.

## 3. restart

Order is guaranteed: **stop → start**, per recipe, completing the stop before the
start. Use restart to roll out changes to running recipes when a push did not already
do it (`workato push --restart-recipes` covers the push case — do not duplicate it here).

## 4. After any operation

Re-run `status` and show the resulting state, so the report reflects reality rather
than the request ("started 3, running 3" / "started 3, 1 failed to start — see below").

## 5. Start failures (S6-4)

A recipe can fail to **start** even though push and validation succeeded (broken or
incomplete recipe definition, unassigned connection, trigger misconfiguration). A
recipe that never starts produces **no jobs**, so job-based checks stay silent.

On a start error:

1. Show the helper's error output verbatim.
2. Do not retry blindly — hand over to `/diagnose-jobs` (start-error entrance), which
   runs the fix → re-push → restart loop until the start succeeds.
3. If the cause is an unauthenticated connection, ask the user to authenticate in the
   Workato UI first, then start again.

## Notes

- Mutations are dev-only; `status` works everywhere the key can read.
- The helper supports `--dry-run` on start/stop — use it when the user wants a preview.
- This skill does not push. Pair with `/push-project` for deploys and `/deploy-project`
  for promotion.
