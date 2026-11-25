---
name: env-promotion
description: Design env-promotion (dev → staging → prod) — one artifact promoted, env-specific config injected, gates between stages, rollback path.
---

# env-promotion

> Promote the same artifact through environments rather than rebuilding per env. Pin the gates between stages.

## When to use

- A team is moving from "build per env" to "build once, promote".
- Releases keep regressing because dev/staging differ from prod in ways that aren't tracked.
- A workflow needs a deploy path before opening prod traffic.

## Procedure

1. **One artifact, many envs.** The same container image / package goes through every stage. Config differs; the binary does not.
2. **Three default stages**:
   - **dev** — fast feedback. Auto-deploy on merge to main.
   - **staging** — production-shaped. Production traffic shape (or shadow), production-grade data (sanitized).
   - **prod** — canary first, then full.
3. **Gate per transition**:
   - dev → staging: tests + smoke against deployed dev.
   - staging → prod: error budget healthy, change freeze respected, on-call ack, change record opened (no PII in record).
   - prod canary → prod full: SLO burn rate stays below threshold for canary window; automatic abort otherwise.
4. **Config injection**:
   - Per-env config in a single source of truth (a YAML per env in the repo, or a parameter store).
   - No secrets in repo. Secrets injected from a secret manager via env-specific names.
5. **Rollback path** named per stage. Usually "redeploy the previous version's image tag". Faster than git revert.
6. **Observability per stage** — same dashboard template, dashboard filterable by env. Alerts route differently per env.

## Output

```text
Env promotion: refund-service

Artifact: container image `refund:${git_sha}` pushed once from main.

Stages:
  dev      → auto-deploy on merge to main
              gate: nothing (fast feedback)
  staging  → auto-deploy when dev has been running ≥ 10m with no error
              gate: integration suite pass, traffic-replay smoke pass
  prod     → manual trigger from staging
              gate (canary): 10% traffic for 30m;
                              abort if burn rate > 14× over 1h window
              gate (full):   error rate within 1% of canary baseline
                              for 30m; manual ack required

Config:
  envs/dev.yaml, envs/staging.yaml, envs/prod.yaml in repo.
  Secrets injected at deploy time from AWS Secrets Manager by name.

Rollback:
  deploy prior image tag (we keep last 10). Documented at runbook X.

Observability:
  Single Grafana dashboard with `env` filter. Alerts: dev → silenced,
  staging → #staging-alerts, prod → PagerDuty.
```

## Anti-patterns to avoid

- Building per env. The binary changes, so the test signal is meaningless.
- Manual `kubectl apply` to prod with the local config that "shouldn't differ".
- Gates that everyone manually skips. If a gate doesn't fire, remove it.
- No rollback path documented.
