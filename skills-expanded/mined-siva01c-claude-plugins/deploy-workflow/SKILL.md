---
name: deploy-workflow
description: >
  Safe deployment workflow for Drupal 10/11 sites: pre-flight checks,
  backup, the correct update sequence (composer install, database updates,
  config import, cache rebuild), verification, and rollback plan. Use when
  deploying to any environment, releasing to production, or when the user
  asks to "push changes live", "update the server", or run a release. Also
  use for multisite releases where each site needs its own database update
  pass.
---

# Deploy Workflow

Deployment of a Drupal site has a fixed order of operations. Skipping a step
or reordering it produces failures that only surface at runtime. This skill
enforces the sequence and its preconditions.

## When this activates

- Deploying a Drupal codebase to staging or production
- Running a release on a multisite platform
- Applying core or contrib updates on a server
- The user asks to push changes live or update an environment

## Phase 0 — Pre-flight (before touching the target)

1. Confirm the target: which environment, which drush alias or SSH host. **Never assume production.**
2. Verify the working tree being deployed is clean and on the intended tag/branch.
3. Check config status on the target: `drush config:status`. Unexpected overrides on the target mean someone changed config in the UI — resolve before deploying, or the import will silently destroy their changes.
4. Maintenance window: for schema-changing releases, ask whether maintenance mode is required (`drush state:set system.maintenance_mode 1`).

**Exit condition:** target confirmed by the user, config status reviewed.

## Phase 1 — Backup

```bash
drush @TARGET sql:dump --result-file=auto --gzip
```

Also snapshot the current codebase reference (deployed tag/commit) so rollback is a known state, not a guess.

**Exit condition:** a restorable database dump exists and its location is recorded.

## Phase 2 — Deploy sequence

The canonical order:

```bash
git fetch && git checkout TAG            # or the platform's deploy mechanism
composer install --no-dev --optimize-autoloader
drush deploy                             # = updb + cim + cr + deploy:hook (Drush 10.3+)
```

If `drush deploy` is not available or the project needs explicit control:

```bash
drush updb -y        # database updates first — update hooks may rely on old config
drush cim -y         # import configuration
drush cr             # rebuild caches
drush deploy:hook -y # post-deploy hooks, if used
```

Notes:

- If an update hook depends on **new** config being present, that is a design smell — prefer `hook_post_update` or `hook_deploy_NAME()`; do not hand-reorder cim before updb as a workaround without understanding why.
- **Multisite:** run the update sequence per site: `drush -l SITE updb -y && drush -l SITE cim -y && drush -l SITE cr` for every site sharing the codebase. A release is not done until every site has been updated.

**Exit condition:** every command exited 0. A non-zero exit stops the workflow — do not continue past a failed `updb` or `cim`.

## Phase 3 — Verify

1. `drush config:status` — must report no differences.
2. `drush core:requirements --severity=2` — no new errors.
3. `drush watchdog:show --severity=Error --count=20` — no new runtime errors.
4. Load the front page and one or two critical paths (login, key form) — HTTP 200 and visually sane.
5. Disable maintenance mode if it was enabled.

**Exit condition:** all checks pass. If any fails, go to Phase 4 instead of debugging live under pressure — unless the fix is obvious and low-risk.

## Phase 4 — Rollback (only when verification fails)

1. Restore the codebase to the previous tag/commit.
2. Restore the Phase 1 database dump.
3. `drush cr`, re-verify, and communicate the failed release.

## Hard rules

- No deployment without a Phase 1 backup. No exceptions, including "small" releases.
- Never run `drush sql:drop`, `sql:sync` toward production, or destructive commands against the production alias as part of a deploy.
- Never mark a multisite release complete while any site is un-updated.
- If the DDEV-based local flow is what the user needs (local update, not a server deploy), prefer the `drupal-ddev-operations` skill (ddev-tools plugin) when available.
