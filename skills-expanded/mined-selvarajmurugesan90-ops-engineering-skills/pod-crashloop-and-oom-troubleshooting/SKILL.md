---
name: pod-crashloop-and-oom-troubleshooting
description: >
  Guides diagnosing `CrashLoopBackOff` pods (using `kubectl logs
  --previous`, `kubectl describe pod`, and exit-code interpretation to
  find the real root cause) and `OOMKilled` terminations specifically
  (distinguishing an undersized memory limit from a genuine application
  memory leak using events, `kubectl top`, and limits vs. observed
  usage). Use when a user asks "why is my pod CrashLoopBackOff," "what
  does OOMKilled mean," "my pod keeps restarting," "exit code 137," "my
  pod's logs are empty after a restart," or "should I just raise the
  memory limit to stop the crashes."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Pod CrashLoopBackOff and OOMKilled Troubleshooting

## Purpose

`CrashLoopBackOff` is not itself a root cause — it's Kubernetes'
description of a symptom (a container keeps exiting, so the kubelet
keeps restarting it with exponential backoff up to a 5-minute cap). The
actual cause could be an application bug, a missing dependency, a
misconfigured probe killing an otherwise-healthy process, or the
container being killed by the kernel's OOM killer for exceeding its
memory limit — each requiring a different fix, and each easy to
misdiagnose if you only look at the crash-looping status itself rather
than the specific termination reason and exit code underneath it. This
skill covers the diagnostic sequence for both crash-loops in general and
`OOMKilled` specifically, including the most common mistake: repeatedly
raising a memory limit to make an `OOMKilled` pod "stop crashing"
without checking whether the real problem is a leak rather than sizing.

## When to use

- A pod shows `CrashLoopBackOff` in `kubectl get pods` and the restart
  count keeps climbing.
- A pod's `Last State` reason is `OOMKilled`, or its previous container
  exited with code `137`.
- `kubectl logs <pod>` shows nothing useful right after a restart.
- Deciding whether to raise a memory limit, fix a leak, or look at
  something else entirely (a probe, a missing config/secret, a
  dependency not yet ready).
- A pod restarts on a schedule that correlates suspiciously with a
  liveness probe rather than an obvious application error.

## Prerequisites & environment

- `kubectl` access to the pod's namespace with permission to read pod
  logs, events, and `describe` output.
- `metrics-server` installed (for `kubectl top pod`) or a Prometheus/
  `kube-state-metrics` + `cAdvisor` setup for historical memory usage —
  useful for distinguishing a slow leak from a sudden spike, though not
  strictly required for a first-pass diagnosis.
- A rough idea of the application's expected memory footprint under
  normal load, so an "unexpected" usage pattern is actually
  recognizable as unexpected.
- Awareness of the Deployment/StatefulSet's configured
  `resources.requests`/`resources.limits` for the container in
  question, and its liveness/readiness probe configuration.

## Step-by-step guidance

1. **Confirm the restart pattern and exit code** before assuming
   anything:
   ```bash
   kubectl get pods -n <namespace>
   kubectl describe pod <pod> -n <namespace>
   ```
   In the `describe` output, check `Last State` → `Reason` and
   `Exit Code`: `OOMKilled` + exit code `137` means the kernel's cgroup
   OOM killer terminated the container for exceeding its memory limit;
   a plain `Error` + a non-zero exit code (commonly `1`) means the
   application itself exited; exit code `143` typically indicates a
   graceful `SIGTERM` (e.g. from a failed liveness probe triggering a
   restart, or a voluntary shutdown), not a crash.

2. **Always check the previous container's logs, not just current** —
   right after a restart, the current container's logs are often empty
   or just starting up:
   ```bash
   kubectl logs <pod> -n <namespace> --previous
   kubectl logs <pod> -n <namespace> --previous -c <container>   # multi-container pod
   ```
   This is the single most-skipped step and the most common reason a
   crash-loop looks "unexplainable" — the explanation is almost always
   in the terminated container's own log tail, not the API server's
   view of it.

3. **Check events for corroborating detail** the `describe` summary may
   compress:
   ```bash
   kubectl get events -n <namespace> \
     --field-selector involvedObject.name=<pod> \
     --sort-by='.lastTimestamp'
   ```
   Look specifically for `Liveness probe failed` events (points to a
   probe, not a crash), `BackOff` events (confirms the crash-loop
   backoff timer, not new information about the cause), or an
   `OOMKilling` kernel-level message surfaced through node events.

4. **If the reason is `OOMKilled`**, determine whether it's an
   undersized limit or a real leak. Check the configured limit against
   recent usage:
   ```bash
   kubectl get pod <pod> -n <namespace> -o jsonpath='{.spec.containers[*].resources}'
   kubectl top pod <pod> -n <namespace> --containers
   ```
   A single spike to the limit under unusually high load suggests
   sizing; a memory curve that climbs steadily over hours/days
   regardless of load (visible in Prometheus'
   `container_memory_working_set_bytes` over time, if available) points
   to a leak that raising the limit will only delay, not fix.

5. **If the reason is a plain application error (not OOM)**, read the
   `--previous` log's actual error/stack trace, then check for common
   root causes: a missing/misnamed `ConfigMap`/`Secret` key referenced
   in an env var or mounted file, a dependency (database, downstream
   service) not yet reachable at startup, a bad image tag/entrypoint, or
   a config value that's valid syntax but semantically wrong for this
   environment.

6. **Rule out a probe misconfiguration masquerading as a crash.** A
   liveness probe with too-short `initialDelaySeconds`,
   `failureThreshold`, or `timeoutSeconds` can kill a genuinely healthy,
   still-starting process, which then looks identical to a real crash
   loop from the outside:
   ```bash
   kubectl get pod <pod> -n <namespace> -o jsonpath='{.spec.containers[*].livenessProbe}'
   ```
   If events show repeated `Liveness probe failed` immediately followed
   by container restart, and the application logs (via `--previous`)
   show no actual error at the time of the kill, the probe — not the
   application — is the root cause. See
   [kubernetes-service-connectivity-troubleshooting](../kubernetes-service-connectivity-troubleshooting/SKILL.md)
   for the related readiness-probe failure mode (excluded from Service
   endpoints without a restart, the milder sibling of this issue).

7. **Check node-level memory pressure** to rule out the node's own OOM
   killer evicting the pod for a reason unrelated to *this* container's
   own limit (overcommitted node, another pod's usage crowding it out):
   ```bash
   kubectl describe node <node> | grep -A5 Conditions
   kubectl top node <node>
   ```
   A `MemoryPressure` condition on the node points to node-level
   overcommit, not necessarily this container exceeding its own limit —
   see
   [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md)
   for diagnosing node-level resource pressure directly.

8. **Debug interactively without modifying the running workload**, when
   logs alone aren't enough:
   ```bash
   kubectl debug <pod> -n <namespace> -it --image=busybox:1.36 --target=<container>
   ```
   Ephemeral containers/`kubectl debug` share the target pod's process
   namespace without requiring a redeploy or altering the crash-looping
   container itself.

9. **Apply the fix that matches the actual cause** — raise
   `resources.limits.memory` (with a deliberate, tested margin, not an
   arbitrary large bump) only if usage data supports a genuine sizing
   gap; fix and redeploy the application if it's a real leak (profile
   with the language's native tooling — heap dumps, `pprof`, etc. —
   rather than guessing); fix the referenced config/secret/dependency if
   it's a startup error; adjust probe timing/thresholds (or the health
   endpoint itself) if it's a probe misconfiguration.

10. **Confirm the fix** by watching the restart count stabilize, not
    just disappear once:
    ```bash
    kubectl get pod <pod> -n <namespace> -w
    ```
    A restart count that stays flat for a full deploy cycle (and ideally
    a full traffic-pattern cycle, e.g. a day's peak-load window) is a
    real confirmation; one that hasn't incremented in the last five
    minutes is not.

## Best practices

- Always run `kubectl logs --previous` before concluding "no useful
  logs" — the current container's logs are frequently empty
  immediately after a restart while the previous container's final
  output holds the actual error.
- Set `resources.requests`/`resources.limits` deliberately from real
  observed usage under load, not a copy-pasted default — see
  [capacity-planning-and-load-testing](../../../site-reliability-engineering/skills/capacity-planning-and-load-testing/SKILL.md)
  for load-testing methodology to establish real sizing rather than
  guessing.
- Treat repeated `OOMKilled` after a limit increase as a strong leak
  signal, not something to "fix" with a second, larger increase — track
  memory usage over time and profile the application rather than
  scaling the limit indefinitely.
- Configure liveness and readiness probes distinctly and deliberately:
  liveness failures restart the container (should only fire for
  genuinely unrecoverable states), readiness failures just pull it from
  Service endpoints (should fire for temporary unavailability) — sharing
  one probe for both purposes is a common source of unnecessary
  restarts during normal startup or brief slowness.
- Correlate a suspected OOM with node-level memory pressure, not just
  the container's own limit — a node running hotter than expected can
  produce OOM-adjacent symptoms across multiple pods simultaneously,
  which is a capacity/bin-packing problem, not a single application's
  bug.
- When a crash loop appears right after a chaos-engineering experiment
  or game day, cross-check whether it's the intended fault injection
  working as designed rather than a new bug — see
  [chaos-engineering-and-resilience-testing](../../../site-reliability-engineering/skills/chaos-engineering-and-resilience-testing/SKILL.md).

## Common pitfalls

- **Symptom:** `kubectl logs <pod>` shows nothing useful, or just a
  fresh startup banner with no error.
  **Fix:** Use `--previous` to read the terminated container's own final
  output, not the newly restarted container's just-starting logs — this
  is the most common reason a crash loop looks unexplainable at first
  glance.

- **Symptom:** Exit code `137` is assumed to be an application bug and
  "fixed" by repeatedly restarting the deployment, but the crash
  recurs.
  **Fix:** `137` = terminated by `SIGKILL`, commonly (not always) the
  cgroup OOM killer. Confirm via `describe pod`'s `Last State.Reason` —
  if it says `OOMKilled`, the fix is about memory (limit sizing or a
  leak), not the restart itself.

- **Symptom:** Raising the memory limit makes the crash loop stop
  temporarily, but the same pod gets `OOMKilled` again hours or days
  later after climbing back up to the new, higher limit.
  **Fix:** This pattern is a strong signal of a genuine memory leak, not
  an undersized limit. Repeatedly raising the limit only delays the
  next OOM and burns more node capacity per pod in the meantime — profile
  the application (heap dump, language-native memory profiler) and fix
  the leak instead of treating the limit as the dial to turn.

- **Symptom:** A pod restarts on a suspiciously regular interval, and
  application logs (via `--previous`) show no actual error at the
  moment of each restart.
  **Fix:** Check events for `Liveness probe failed` — a probe configured
  with too-short `initialDelaySeconds`/`timeoutSeconds` relative to the
  app's real startup or response time will kill an otherwise-healthy
  process on a schedule that mimics a crash loop. Fix the probe
  configuration (or the health endpoint's actual behavior) rather than
  debugging the application for a bug that isn't there.

- **Symptom:** `kubectl delete pod <pod>` is used repeatedly to "fix" a
  crash-looping pod whenever someone notices it.
  **Fix:** The controller (Deployment/StatefulSet/ReplicaSet) just
  recreates the pod, and it crash-loops again for the same underlying
  reason — this masks the root cause instead of fixing it, and burns
  time on every recurrence. If it's done with
  `kubectl delete pod --force --grace-period=0` to speed things up,
  > **Warning:** this skips graceful termination entirely and can leave
  a stateful workload's on-disk or external state inconsistent; use it
  only when a pod is genuinely stuck (e.g. its node is gone), and
  diagnose the actual crash cause (steps 1–6 above) instead of deleting
  reflexively.

## Worked example

**Scenario:** `payments-worker-6f9d4b5-2xk9p` shows `CrashLoopBackOff`
with a restart count climbing every few minutes.

```bash
kubectl describe pod payments-worker-6f9d4b5-2xk9p -n payments
# Last State:     Terminated
#   Reason:       OOMKilled
#   Exit Code:    137
#   Started:      ...
#   Finished:     ...
```

```bash
kubectl get pod payments-worker-6f9d4b5-2xk9p -n payments \
  -o jsonpath='{.spec.containers[0].resources}'
# {"limits":{"memory":"256Mi"},"requests":{"memory":"128Mi"}}

kubectl top pod payments-worker-6f9d4b5-2xk9p -n payments --containers
# (prior to the last OOM, memory climbed from ~90Mi at startup to 256Mi
#  over roughly 40 minutes of otherwise-steady request volume)
```

The steady climb regardless of load — not a sudden spike under a
traffic burst — points to a leak rather than an undersized limit.
Checking `--previous` logs confirms no application-level error at the
moment of the kill (consistent with OOM, not a code-path crash).
Investigation of the worker's in-memory cache finds it has no eviction
policy, growing unbounded with every processed job. The fix: add a
bounded, TTL'd eviction policy to the cache (the real fix), plus a more
conservative, evidence-based limit increase to `384Mi` as headroom — not
a blind large jump — and a Prometheus alert on
`container_memory_working_set_bytes` trending toward the limit so the
next leak is caught before it OOMs in production again.

```bash
kubectl get pod payments-worker-6f9d4b5-2xk9p -n payments -w
# restart count stays flat through a full day's peak-traffic window
```

## Cross-references

- [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md) — diagnosing node-level `MemoryPressure` when an OOM looks correlated with overall node capacity rather than one container's limit.
- [kubernetes-service-connectivity-troubleshooting](../kubernetes-service-connectivity-troubleshooting/SKILL.md) — the related readiness-probe failure mode (excluded from Service endpoints without a restart) versus the liveness-probe-triggered restarts covered here.
- [capacity-planning-and-load-testing](../../../site-reliability-engineering/skills/capacity-planning-and-load-testing/SKILL.md) — load-testing methodology for setting real, evidence-based memory requests/limits instead of guessing.
- [chaos-engineering-and-resilience-testing](../../../site-reliability-engineering/skills/chaos-engineering-and-resilience-testing/SKILL.md) — distinguishing an intentional fault-injection kill from a genuine new crash-loop bug.
