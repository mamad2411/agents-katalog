---
name: monitor-deploy
description: Watch a just-shipped deploy until it proves healthy (or rolls back). Polls health/readiness, error rate, and latency against a baseline for an observation window; on threshold breach it surfaces evidence and triggers /rollback-deploy. The executor behind /deploy-stage's --watch / --no-monitor and the recovery confirmation in /rollback-deploy.
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# monitor-deploy

The first minutes after a rollout are the most likely failure window. This skill watches them.

## Premise

Declare GREEN only from observed signal, never from "the deploy command exited 0." Every verdict cites the probe that ran, the value it returned, and the threshold it was compared against — `/health → 200`, `error_rate = 0.4% (threshold 0.5%)`, `p95 = 145ms (baseline 152ms, +0% drift)`. A health-check that was never polled is not a passing health-check. The rollback decision is mechanical: a breach that persists past its `for:` debounce triggers `/rollback-deploy`, it is not a judgment call surfaced for discussion mid-incident.

## When to use

- Immediately after `/deploy-stage` (it dispatches this skill unless `--no-monitor`).
- As the recovery-confirmation step inside `/rollback-deploy` (watch the previous revision back to GREEN).
- Standalone to watch an in-flight deploy you didn't start ("monitor without deploying").
- To extend an observation window past the default (canary soak, slow-burn watch).

## Halt conditions

- Refuse to report GREEN without at least one successful health/readiness probe in the window — no probe, no pass.
- Refuse to report an error rate or latency number you didn't pull from the live signal source; don't infer "looks fine" from logs alone.
- Halt if no health endpoint / readiness signal is resolvable — ask for it rather than declaring success against nothing.
- Halt if the baseline for latency/error-rate comparison can't be established (no prior revision data) — watch absolute thresholds only and say so; don't fabricate a "+0% drift".
- A breach that clears within its debounce is a flap, NOT a pass and NOT a rollback — log it and keep watching.

## Inputs

- **health endpoint** + expected status (default `200`) — from `_extracted-codebase.md § Deploy`, the Dockerfile `HEALTHCHECK`, or the k8s readiness probe. Resolve it; don't assume `/health`.
- **observation window** — default 5 min; `--watch=<duration>` extends (max 60 min).
- **thresholds** — error-rate ceiling (default 0.5%), p95 latency drift ceiling vs baseline (default +20%), readiness target (all replicas READY).
- **baseline** — the previous healthy revision's error rate + p95, for drift comparison.
- **signal source** — k8s (`kubectl get pods` / events / `rollout status`), the metrics backend (Prometheus / Datadog / CloudWatch), and the log tail.

## Procedure

1. Resolve the health endpoint + thresholds + baseline from inputs. If any is unresolvable, apply the matching halt condition.
2. Poll readiness until all replicas/instances report READY or the window's startup grace elapses:
   ```bash
   kubectl rollout status deploy/<name> --timeout=<startup-grace>
   ```
   (Compose: `docker compose ps` healthy; serverless/PaaS: the platform's deployment-ready API.)
3. Poll the health endpoint on an interval for the window:
   ```bash
   curl -fsS -o /dev/null -w '%{http_code}' "$HEALTH_URL"
   ```
   Expected status N consecutive times = healthy; non-2xx = breach candidate.
4. Sample error rate + latency from the metrics backend each interval; compare against threshold + baseline drift. Apply a `for:` debounce (default 60s) so a single bad scrape is a flap, not a breach.
5. Tail logs for ERROR-level entries and crash/restart signals (`CrashLoopBackOff`, OOMKilled, restart count climbing).
6. On a breach that persists past its debounce: capture evidence (last 50 log lines, breaching metric values, pod events) and trigger `/rollback-deploy`. **Hand it the breach evidence, not a target** — that command's steps 2-4 decide rollback-vs-forward-fix, resolve the target's health from the deploy ledger, and run the reversibility gate (already-applied contract migration / no retained revision / mutable tag). Passing `--to=<previous-healthy>` presumes an answer this skill has not computed: the previous revision's health is not something a health *window* observes. If the gate halts, the correct outcome is a named halt, not a revert. Then watch whatever recovery it performs back to GREEN.
7. At window end with no persistent breach: report GREEN with the observed numbers.

## Output

```
monitor-deploy — web @ abc1234 (window 5m)

Readiness:
  ✓ Rollout complete: 3/3 pods READY (47s)

Health (poll /healthz every 15s):
  ✓ 200 × 20/20 polls

Signals (vs baseline rev def5678):
  ✓ Error rate: 0.08%   (threshold 0.5%)
  ✓ p95 latency: 149ms  (baseline 152ms, -2%)
  ✓ Logs: 0 ERROR-level entries
  ✓ Restarts: 0

Result: GREEN — deploy held healthy through the window.
```

On breach + rollback:

```
monitor-deploy — web @ abc1234 (window 5m)

Readiness:
  ✓ Rollout complete: 3/3 pods READY (51s)

Signals:
  ✗ Error rate: 7.3%  (threshold 0.5%) — breached at T+1m40s, held 60s past debounce
  Log tail (last 50):
    ERROR  TypeError: cannot read property 'id' of undefined  (×412)
    ...

Breach confirmed → handing off to /rollback-deploy (evidence above; target + gate resolved there)

Rollback watch:
  ✓ /rollback-deploy resolved rev def5678 (GREEN in ai/runtime/deploys.md), gate R1-R3 PASS
  ✓ Rolled back to def5678; error rate 0.06% within 90s.

Result: RED (rolled back) — abc1234 failed the health window; previous revision restored.
Next: fix the null-deref, re-run /deploy-stage.
```

When the handoff halts instead of reverting, that is a result, not a failure to report:

```
Breach confirmed → handing off to /rollback-deploy

  ✗ HALT (R1) — rev abc1234 applied `DROP COLUMN users.legacy_phone` (contract step).
                def5678 still SELECTs it; reverting turns a 7.3% error rate into a hard outage.

Result: RED (NOT rolled back) — rollback is unavailable; forward-fix path named in the runbook.
Next: ship the null-deref fix forward. Do not revert.
```

## False positives / gotchas

- **Cold-start latency** during the startup grace is not a breach — only compare latency/error-rate after readiness, not during rollout.
- **A single non-2xx scrape** mid-window is a flap; the `for:` debounce exists precisely so one bad poll doesn't trigger a rollback.
- **No baseline (first-ever deploy)** means drift comparison is impossible — fall back to absolute thresholds and say baseline was unavailable; don't print "+0%".
- **Blue/green and canary** shift the signal source — watch the new color / canary subset, not the aggregate, or the breach gets diluted below threshold.
- **Forward DB migrations** make rollback non-trivial — if the bad deploy migrated schema, `/rollback-deploy`'s R1 gate decides whether the revert is available at all before executing anything; this skill does not auto-run destructive down-migrations and does not pre-judge the target.
- **A confirmed breach is not automatically a rollback.** This skill's decision is mechanical only up to "the breach is real, hand it off". Whether reverting *helps* depends on the migration direction and on state the new version wrote — which is why the handoff carries evidence rather than a verdict.

## Related

- `/deploy-stage` — dispatches this skill as its monitoring step (`--watch=` / `--no-monitor`).
- `/rollback-deploy` — triggered by this skill on a confirmed breach; also calls back to it to confirm recovery.
- `progressive-delivery` — tight boundary: this watches **a single deploy's** health window and triggers rollback; progressive-delivery owns the **feature-flag lifecycle** (stale/dead flags, kill-switch, cross-env parity) and the **canary's automated-analysis wiring** (the AnalysisTemplate that auto-promotes/aborts). This watches one rollout; that governs the flag's whole life and the canary's gate.
- `.claude/rules/devops-principles.md` — "monitor before declaring success" is a hard rule.
