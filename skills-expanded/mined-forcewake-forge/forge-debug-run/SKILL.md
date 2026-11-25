---
name: forge-debug-run
description: Triage a stuck, blocked, or silently-not-processing forge run. Use when /implement or /go seems ignored, a run sits in one status too long, or a harness job failed mysteriously.
---

# forge-debug-run: triage a run

Work top-down; stop at the first layer that answers the question.

1. **Run state** (Postgres, source of truth):
   `SELECT substring(id::text,1,8), issue_iid, status, status_reason,
   commit_cycle FROM flow_runs ORDER BY created_at DESC LIMIT 10;`
   Terminal statuses: `ready_for_human`, `blocked`, `failed`, `cancelled`.
   `status_reason` is the verdict narrative — read it fully.
2. **Was the note even routed?** Bare `/implement` without a mention is
   routed since commit 4fb11b4. If the worker log shows
   "No agents matched for note event" for a run command, the app container
   predates the fix — redeploy.
3. **Queue**: `curl -s localhost:8420/metrics` → `queue_depth` (pending
   zset `forge:tasks:pending`), `dlq_depth` (exhausted tasks — cosmetic
   w.r.t. run state), `workers_active` (heartbeat lags ~30s after death).
   A task consumed but "nothing happened" usually means the app predates
   run_command routing or the worker env is stale.
4. **Worker logs**: `podman logs forge-worker --since 30m` — filter out
   `httpcore|asyncio` noise. RunService INFO lines narrate every state
   change; ERROR + retry lines indicate task failures.
5. **Harness runs** (`waiting_harness`): read the GitLab job trace
   (`GET /projects/:id/jobs/:job_id/trace`); grok/claude templates stream
   compacted events into it. Classification of failures: script_failure →
   harness_code (repairable), empty/unknown reason → harness_infrastructure,
   auth/quota patterns → harness_infrastructure. Verification adopts only
   when the real branch head equals the FORGE_RESULT head.
6. **GitLab-side**: pipeline for the candidate SHA, smoke/pytest job output,
   factory branch commits (two commits per harness cycle are expected:
   harness's own + the fallback commit).

Known-good baselines (M3): provider outage → `failed planning_failed`;
duplicate /implement → guard note, single run; worker restart → runs
continue; job cancel → `blocked harness_infrastructure`.
