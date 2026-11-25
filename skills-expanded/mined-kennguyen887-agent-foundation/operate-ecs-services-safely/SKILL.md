---
name: operate-ecs-services-safely
description: Use before ANY change to a deployed container service behind a load balancer (AWS ECS/Fargate, or equivalent) — changing an env var / task-def, scaling, deploying, terminating an instance — AND when such a service is down (502/503, deploy stuck below desired, tasks failing the LB health check) or a scheduled/cron worker isn't running. A verify-before-mutate discipline + an observe→diagnose→recover playbook. Principle-first; AWS ECS commands shown, but the failure modes apply to any orchestrated container service.
metadata:
  last-updated: 2026-06-22
  author: Ken Nguyễn <ntnpro@gmail.com>
---

## When to use

- About to **change** a deployed service: edit an env var / task-def field, scale replicas, deploy, recycle an instance.
- A service is **down**: load balancer returns 502/503, a deploy is stuck below desired replicas, tasks cycle on the LB health check.
- A **scheduled/cron worker** isn't doing its job (jobs not running, nothing processed).

## The one principle

**Changing an env var, the replica count, or the image is a full deploy — it rolling-restarts tasks.** The *value* you set is rarely what breaks; the **restart** is, because each fresh task must pass the load-balancer health check before it receives traffic. So "just flip an env" or "just scale to 1" has the blast radius of a production deploy. Treat it as one.

## Before you change anything (checklist)

1. **Read the LIVE value first — never assume a default.** The current replica count, image tag, the actual deployed env/secret value, the LB health-check path. Diagnosing or changing from an assumed value is how "small" changes become outages.
2. **Will the health check survive a fresh restart?** If the health endpoint **hard-fails or blocks on a flaky / non-critical dependency**, fix that *first*. A health probe that gates the load balancer must depend only on what's truly required to serve traffic (e.g. the database) — never on a best-effort dependency (a third-party API, a push provider). Otherwise any restart during that dependency's blip kills every task at once.
3. **Check capacity and co-tenancy.** How many hosts, how much free CPU/MEM, are their agents healthy? On small clusters with bin-packing, an added workload co-locates with the live service and can starve it. Verify headroom *before* adding load; watch host-level metrics after, not just your task's own health.
4. **One deliberate change, then watch it converge.** **Never churn** repeated deploy / force-redeploy / rollback commands — orchestrators back off scheduling after repeated failures and the service can stop launching tasks entirely (a self-inflicted, prolonged outage). Make one change, observe to steady state, then decide.
5. **Know where the value lives.** Env/config often lives only on the live task/deployment spec, not in the repo (CI may swap only the image and preserve env). So a change is an out-of-band edit to the running spec — there's no PR review; you are the review.
6. **After: verify and keep watching.** Replicas `running == desired`, LB target healthy, health endpoint 200 — and keep an eye out, because resource-starvation degradation can surface slowly (tens of minutes later), not immediately.

## When a service is down — observe (AWS ECS shown; adapt to your orchestrator)

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://my-app.example.com/health         # 200 / 502 / 503
aws ecs describe-services --cluster <cluster> --services <service> \
  --query 'services[0].{running:runningCount,pending:pendingCount,desired:desiredCount,deps:length(deployments),events:events[:6].message}'
TG=$(aws ecs describe-services --cluster <cluster> --services <service> --query 'services[0].loadBalancers[0].targetGroupArn' --output text)
aws elbv2 describe-target-health --target-group-arn $TG --query 'TargetHealthDescriptions[].{state:TargetHealth.State,reason:TargetHealth.Reason}'
aws logs get-log-events --log-group-name <log-group> --log-stream-name <stream/taskId> --start-from-head --limit 100 --query 'events[].message' --output text
aws ecs describe-container-instances --cluster <cluster> --container-instances <ci-arn> \
  --query 'containerInstances[].{agent:agentConnected,running:runningTasksCount,remMem:remainingResources[?name==`MEMORY`].integerValue|[0]}'
# WHICH container is eating the host? Host CPUUtilization (AWS/EC2) says the box is saturated, NOT by what.
# Per-task/service consumer (emitted only while the agent is connected — see blind-spot note):
aws cloudwatch get-metric-statistics --namespace ECS/ContainerInsights --metric-name CpuUtilized \
  --dimensions Name=ClusterName,Value=<cluster> Name=ServiceName,Value=<service> \
  --start-time <ISO> --end-time <ISO> --period 300 --statistics Average Maximum \
  --query 'sort_by(Datapoints,&Timestamp)[].{t:Timestamp,avg:Average,max:Maximum}' --output text
# swap MetricName=MemoryUtilized for the memory-leak / GC-spiral signature (growing vs flat)
```

Interpret:
- **502/503** = the LB has no healthy target.
- `running < desired` with `pending = 0` = the orchestrator isn't launching (often scheduler back-off after repeated failures).
- Many deployment records / `deps > 1` = prior churn.
- In boot logs: an app-ready line (e.g. `listening on port`) **plus** health-check dependency errors = the app is up but the health probe 503s on a dependency (the most common killer). Only a boot banner with no ready line = it hung before serving.
- `agentConnected = false` on a host = it can't place tasks (restart the agent or replace the host).
- **100% host CPU / OOM → isolate the consumer by measurement, never guess.** Host `CPUUtilization` (AWS/EC2) only says the box is saturated; pull per-task/service `ECS/ContainerInsights` `CpuUtilized`/`MemoryUtilized` to see WHICH container ate it and whether memory grew (leak / GC-spiral) or stayed flat. A worker that merely logged errors near the outage is a *suspect* — confirm with the per-task metric before attributing the cause or shipping a fix.
- **Blind spot:** when the host saturates, the agent disconnects and per-task Container Insights metrics **stop at that instant**. The pre-disconnect window is your evidence; treat the post-disconnect 100%-CPU window as **undetermined** (consumer not observable), not as confirmation of whatever you suspected. Precedent (2026-06-30): a scheduler was confidently blamed for a CPU outage; per-task metrics showed it idle (~2–5 CPU units, flat mem), and the sustained-CPU window was unobservable — so "undetermined" was the honest call, not the scheduler.

## Recovery — match the cause (one action, observe, never churn)

| Cause | Fix |
|---|---|
| Health probe 503s on a **non-critical dependency** (it's slow/down and its check exceeds the LB timeout) | Make the health endpoint gate on **critical deps only** (e.g. `CRITICAL_CHECKS = ["database"]`); report the rest for observability but never fail the LB probe on them. Add a short per-check timeout so the probe always answers under the LB timeout. |
| Need to restore serving **without a deploy** | Point the LB health check at a **dependency-free liveness path** (e.g. `/version` that returns 200 unconditionally); revert to the real health path after fixing it. |
| **Stuck at 0 tasks / `pending 0`** (scheduler back-off after failed tasks) | Force-redeploy does **not** reliably reset back-off; **scale to 0 then back to N** to reset scheduling. |
| **Disconnected agent / unhealthy host** | Restart the agent or replace the host (in an autoscaling group: terminate → it's auto-replaced); the healthy host serves meanwhile. |
| A **scheduled/cron worker** isn't running | Confirm the worker/scheduler service is actually **running** (`desired/running`), not scaled to 0 or crash-looping on boot; run **exactly one** replica (more double-fires jobs); confirm it has cluster headroom before scaling it up. |

## The anti-pattern that causes most of this

Treating an env/scale change as a harmless config tweak (so the health-check-survives-a-restart check is skipped), then — when the restart fails — **churning recovery deploys**, which trips scheduler back-off and turns a recoverable blip into a prolonged outage. Read live state, change one thing, verify the health check tolerates a restart, and observe to convergence.
