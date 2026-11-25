---
name: incident
description: >-
  Production incident triage for Fly-hosted apps: site down, 500s, empty
  data, broken predictions. Trigger on "prod is down", "site is down", "500 on
  prod", "users are complaining", or any urgent production report.
---

# Incident triage

Order: restore service first, root-cause second.

## 1. Assess

```bash
fly status -a <app>                        # machines started? recent deploy?
curl -s https://<domain>/health | head     # is it actually down or partial?
fly logs -a <app> --no-tail | grep -iE 'error|traceback' | tail -50
```

Classify: full outage / one route broken / stale-empty data / slow.

## 2. Known failure modes (check before inventing new ones)

- **Recent deploy broke it**: `fly releases -a <app>`; if the incident
  started at a release, roll back first, debug after.
- **Machines stuck `created`**: release_command gotcha; redeploy via local
  flyctl without release_command.
- **Prediction routes 500 (shape mismatch)**: FEATURE_COLS drift between
  repos; sync + redeploy in the right order.
- **Empty tables for a completed race**: data pipeline gap; cached data
  should serve (cache-resilience policy); check R2 artefacts and the
  backfill cron rather than the API code first.
- **Upstream data lag** (FastF1/Jolpica): predictions look like nonsense;
  wait/fallback logic, not code rollback.

## 3. Restore

Prefer the smallest action that restores service: rollback release, restart
a crash-looping machine (`fly machine restart`), or republish a missing
artifact. Destructive actions (destroying apps/volumes) are never part of
triage.

## 4. Afterwards

Root-cause with the `debugger` subagent, fix properly, and note the failure
mode in project memory if it's new.
