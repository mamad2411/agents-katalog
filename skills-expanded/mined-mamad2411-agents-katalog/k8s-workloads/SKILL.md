---
name: k8s-workloads
description: "Specify a Kubernetes workload so it holds under pressure: measure the real CPU and memory profile before writing any number, then set requests and limits knowing CPU limits throttle while memory limits kill, pick the QoS class on purpose, keep liveness, readiness and startup probes distinct, size the PodDisruptionBudget, maxSurge and maxUnavailable, spread across zones, and close the race between SIGTERM and endpoint removal with a preStop hook. Use when someone asks \"what should I set for resource limits\", \"my pods get OOMKilled under load\", \"should this have a readiness probe\", \"will this PodDisruptionBudget block a node drain\", or is reviewing the numbers in a Deployment or StatefulSet spec. Not for a workload already broken (k8s-triage), how many replicas or how big the cluster (capacity-planning), generating YAML or a project (code-scaffold), or the image itself (image-hardening)."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(kubectl:*), Bash(jq:*)
---

# Kubernetes Workload Specification

A workload is specified well when you can say, from the manifest alone, what happens to it when the node fills up, when a deploy goes out at peak, when its node is drained and when the thing it depends on is down — and every number in it came from a measurement rather than from the service next door.

The job is hard because almost none of these fields fail at review time. A manifest with a CPU limit equal to its request, a liveness probe that opens a database connection, a PodDisruptionBudget over one replica and no `preStop` hook passes every linter, deploys cleanly and serves traffic for months. Each is an outage waiting for a trigger it does not control: the CPU limit throttles the p99 that nobody attributes to it, the liveness probe converts somebody else's incident into a fleet-wide restart storm, the budget blocks a cluster upgrade six weeks later, and the missing hook puts a small error spike into every rollout that everyone learns to read past. Underneath most of them is the same root cause — the numbers were guessed. Guessed high, they waste money silently; guessed low, they produce OOMKills and evictions that get investigated as application bugs.

## Scope

Use for: writing or reviewing the spec of a Deployment, StatefulSet, DaemonSet or Job — resources, probes, disruption budget, rollout strategy, placement, shutdown; deciding what a specific number should be and how to find out; hardening a workload after an incident it caused.

Do not use for:

- A workload that is broken right now — CrashLoopBackOff, pods stuck Pending, an OOMKill that just fired a page. That is `k8s-triage`, which mitigates first and captures evidence before anything is mutated. Hand over, and come back here once service is restored.
- How many replicas the service needs, how big the cluster should be, designing or reading a load test, sizing an autoscaler. That is `capacity-planning`. This skill sizes one workload's own contract; it does not size the fleet.
- Generating a project, a chart, a module or boilerplate. That is `code-scaffold`. The work here is not YAML production — it is deciding what the workload claims from the node and promises to the Service, which is the part that survives the YAML being regenerated.
- The image itself: base image, digest pinning, non-root UID, entrypoint form, scanning. That is `image-hardening`.

## Workflow

### 1. Establish the profile before writing any number

This gate is the point of the skill. Do not write a `requests` or `limits` value until you can say what the container's memory working set and CPU usage actually are under load. Numbers guessed from nothing are the shared cause of the OOMKills, the evictions and the idle spend, and every later step in this file assumes step 1 produced real figures.

```bash
set -Eeuo pipefail
NS=production
APP=checkout

# A sanity check only: metrics-server samples on an interval, so a spike between
# two samples does not appear here at all.
kubectl top pod -n "$NS" -l app="$APP" --containers

# What the scheduler currently believes, which is the number you are replacing.
kubectl get pods -n "$NS" -l app="$APP" -o json \
  | jq -r '.items[] | .metadata.name as $pod | .spec.containers[]
           | "\($pod)\t\(.name)\treq=\(.resources.requests)\tlim=\(.resources.limits)"'
```

The figures that decide the manifest come from a window, not an instant. Over at least one full business cycle that contains a weekly peak, a deploy and one cold start:

```promql
# Memory: the maximum, not a percentile. Exceeding a memory limit is a kill, so a
# limit set at the 99th percentile kills the container on one percent of windows.
max_over_time(container_memory_working_set_bytes{namespace="production", container="checkout"}[7d])

# CPU: a high percentile is enough, because exceeding a CPU request costs scheduling
# position rather than the process.
quantile_over_time(0.99, rate(container_cpu_usage_seconds_total{namespace="production", container="checkout"}[5m])[7d:5m])

# Whether the current CPU limit is already throttling. Any sustained non-zero value
# here is the answer to a latency question somebody is asking elsewhere.
rate(container_cpu_cfs_throttled_periods_total{namespace="production", container="checkout"}[5m])
  / rate(container_cpu_cfs_periods_total{namespace="production", container="checkout"}[5m])
```

If a Vertical Pod Autoscaler is available, running the recommender with `updateMode: "Off"` fills in `status.recommendation.containerRecommendations` — target, lower bound and upper bound — without touching a single pod. It is the cheapest way to get a profile for a workload already in production.

What to do when the data is not there:

| What you have | What to do |
| --- | --- |
| Production metrics over a real peak | Read the numbers off, and record the query you used so the next revision is comparable. |
| A load test but no production traffic | Take the profile from the test, mark the numbers provisional, and attach a date to revisit. `capacity-planning` owns designing that test. |
| Neither, and it has to ship | Ship provisional numbers with an alert and a date, and say out loud in the pull request that they are guesses. |

There is no published-correct headroom multiplier. "Double it" and "add twenty percent" are folklore, and inventing a threshold here is how a guess acquires the authority of a measurement. What makes a provisional number safe is not its size but the alert and the review date attached to it: page on `OOMKilled` appearing in a container's last terminated reason, and put the revisit in the backlog with an owner.

On clusters at v1.33 or newer, in-place pod resize (`kubectl patch pod ... --subresource=resize`) applies a corrected CPU value without a restart; `resizePolicy[*].restartPolicy` defaults to `NotRequired`, and memory decreases are best-effort. That makes correcting a provisional CPU number cheap, which is an argument for shipping and measuring rather than deliberating.

### 2. Decide what each number is doing

The four fields do four different jobs, and most bad manifests come from treating them as one.

| Field | Enforced by | What happens when the workload wants more |
| --- | --- | --- |
| `requests.cpu` | kube-scheduler when placing the pod; cgroup CPU weight on the node | Nothing directly. It is a claim on a node and a share of contended CPU; on an idle node the container uses whatever is free. |
| `limits.cpu` | The kernel's CFS bandwidth control, on a period the kubelet defaults to 100ms | Throttled. Container runtimes do not terminate a container for CPU. |
| `requests.memory` | kube-scheduler; kubelet eviction ranking | Nothing directly, but exceeding it makes the pod an eviction candidate as soon as the node is short of memory. |
| `limits.memory` | The kernel out-of-memory killer | The container is killed, reported as `OOMKilled` with exit 137. Enforcement is reactive — it happens on memory pressure, so the kill can land well after the allocation that caused it. |

One trap before anything else: a limit with no matching request is not permissive. Kubernetes copies the limit into the request, so `limits.memory: 8Gi` with no request quietly demands 8Gi of schedulable memory.

**CPU: set the request from the measurement and usually leave the limit off.** A limit of `500m` means 50ms of CPU per 100ms window, summed across every thread. A service whose work is bursty — a garbage collection pause, a TLS handshake, a fan-out across a thread pool — can exhaust that window in the first 10ms and then sit idle for 90ms while the node has free cores. That is throttling with no contention anywhere, and it surfaces as tail latency that nobody connects back to a manifest. Accurate requests already protect the neighbours, because CPU is reclaimable and the weight mechanism hands it back under contention automatically.

A CPU limit equal to the request is right when somebody can state which of these applies:

- The node runs the `static` CPU manager policy and the workload wants exclusive cores, which requires the Guaranteed class and an integer CPU count.
- Reproducible runtime matters more than speed — a benchmark, or a batch job whose duration is a planning input.
- The ceiling is the product: a tenant boundary, or a quota someone is paying for.
- You measured throttling at the proposed limit, found it zero at peak, and want the limit as a regression guard.

"To be safe" is not on that list. A CPU limit makes only the workload carrying it slower.

**Memory: set the request and the limit, and set them equal.** Memory is not reclaimable, so the framing inverts: burst memory is memory that can only be supplied by killing something. Equal request and limit makes the failure loud, immediate and attributable to the workload that caused it, rather than arriving as an eviction of whatever else happened to be on the node. This does not by itself make the pod Guaranteed — that needs the CPU limit too, which step 3 resolves.

### 3. Read the QoS class off, do not aim for it

| Class | Criteria |
| --- | --- |
| Guaranteed | Every container has a CPU request, CPU limit, memory request and memory limit, all above zero, with limit equal to request for both resources. |
| BestEffort | No container has any request or limit at all. |
| Burstable | Everything else. |

Under node memory pressure the kubelet ranks pods for eviction by whether usage exceeds requests, then by Pod Priority, then by how far over the request the usage is. The consequence is the part people miss: a Burstable pod using less than its requests is evicted in the same last group as a Guaranteed pod. Accurate memory requests buy nearly all the eviction protection that chasing Guaranteed buys, and they buy it without the CPU limit step 2 argues against.

So aim for Guaranteed when you want exclusive CPUs under the static policy, or when a platform policy in your cluster grants Guaranteed pods something specific. Otherwise accept Burstable and spend the effort on making the request correct. BestEffort is evicted first and is defensible only for something nobody is waiting on.

PriorityClass is the second term in that ranking, not an override of it, and is a cluster-wide decision rather than a per-workload one — agree it with whoever owns the cluster instead of setting it unilaterally.

### 4. Probes answer three different questions

| Probe | Effect of failure | The outage it causes when confused |
| --- | --- | --- |
| Readiness | The pod's IP is removed from the EndpointSlices of every matching Service | Made dependent on a downstream, it takes every replica out of the Service at once, so a partial dependency failure becomes a Service with no endpoints and a total outage. |
| Liveness | The container is killed and restarted per the pod's restart policy | Pointed at a dependency, someone else's incident becomes a restart storm here: every pod restarts, loses its warm cache and connection pool, and cannot recover even after the dependency does. |
| Startup | The container is killed once `failureThreshold * periodSeconds` has elapsed; liveness and readiness are held off until it first succeeds | Absent on a slow starter, liveness kills the container mid-boot on every attempt, producing a CrashLoop that reads as an application bug. |

The defaults are sharper than they look: `initialDelaySeconds` 0, `periodSeconds` 10, `timeoutSeconds` 1, `successThreshold` 1 (and it must be 1 for liveness and startup), `failureThreshold` 3. The one that bites is `timeoutSeconds: 1` — a handler sharing a thread pool with request handling starts timing out under exactly the load where a restart is most damaging.

Three positions worth holding:

- Default to no liveness probe. Add one only when you can name the wedged state a restart fixes — a deadlocked event loop, a connection pool the process will not rebuild. If the answer is "it crashes", the restart policy already handles that without a probe.
- The liveness endpoint must not touch a network dependency. Readiness may, and should only when the pod genuinely cannot serve any request without it.
- Put the boot budget in a startup probe rather than a large `initialDelaySeconds` on liveness. The upstream worked example is `failureThreshold: 30` with `periodSeconds: 10`, giving 300 seconds; a startup probe returns the instant the app is up, whereas `initialDelaySeconds` is a fixed tax paid on every restart.

`references/probes-and-lifecycle.md` has the full field table, a worked startup budget and the probe-level grace period.

### 5. A PodDisruptionBudget is a drain protocol, not an availability guarantee

It governs voluntary disruption through the Eviction API only. A failed node, a crashed kubelet, a `kubectl delete pod` and an OOMKill are not evictions, and no budget affects them.

The deadlock to avoid is specific and common: one replica with `minAvailable: 1` — equivalently `maxUnavailable: 0`, or `minAvailable: 100%` — permits no eviction at all, so every drain of the node hosting it blocks indefinitely. Whoever is draining eventually reaches for `--disable-eviction`, which bypasses the budget and deletes the pod directly — still a graceful delete honouring `terminationGracePeriodSeconds` and the `preStop` hook, so the cost is the stalled drain and the person's afternoon rather than an abrupt kill. The budget bought nothing and blocked maintenance. A single-replica workload with a budget is claiming availability it does not have: raise the replica count, or accept the disruption and write no budget.

Prefer `maxUnavailable` to `minAvailable`, as upstream recommends, because it keeps meaning the same thing when the replica count changes. Note also that `unhealthyPodEvictionPolicy` defaults to `IfHealthyBudget`, which refuses to evict Running-but-not-ready pods while the budget is already disrupted — so a CrashLooping deployment blocks node drains until someone sets `AlwaysAllow` or fixes the workload.

Do the arithmetic once: with `maxUnavailable: 1` a drain moves one pod at a time, so a rolling node upgrade costs roughly the replica count multiplied by the time a pod takes to become ready, for every workload on the node. That is the whole explanation for why cluster upgrades take a weekend.

### 6. Rollout strategy is a capacity decision

| Field | Default | What accepting the default commits you to |
| --- | --- | --- |
| `maxUnavailable` | 25%, rounded down | Serving on 75% of the replicas for the length of every rollout, including one at peak. |
| `maxSurge` | 25%, rounded up | Up to 125% of the replica count must be schedulable, or the rollout stalls. |
| `minReadySeconds` | 0 | A pod counts as available the instant readiness first passes. |
| `progressDeadlineSeconds` | 600 | After ten minutes the Deployment sets `ProgressDeadlineExceeded` and keeps retrying. |
| `revisionHistoryLimit` | 10 | Ten old ReplicaSets retained, which is what a rollback reads. |

For anything latency-sensitive with room to surge, `maxUnavailable: 0` with `maxSurge: 1` keeps the served capacity at the declared replica count throughout, and costs a slower rollout plus one pod's worth of headroom.

`minReadySeconds` is the cheapest protection in the table. At 0, a pod that passes readiness and dies eight seconds later still lets the rollout advance, and it advances all the way, replacing every healthy replica with a broken one. Set it above the time it takes for the first real request to reach a new pod and fail.

No Deployment rolls itself back. `progressDeadlineSeconds` sets a condition and nothing more, so something outside the Deployment has to watch for it; if nothing does, say so rather than assuming the platform handles it. Progressive delivery and canary analysis belong to `release-strategy`. And resist setting `revisionHistoryLimit: 0` to tidy up `kubectl get rs` — it removes the rollback that `k8s-triage` reaches for first.

### 7. Placement: decide what happens when the spread cannot be satisfied

`topologySpreadConstraints` takes `maxSkew`, `topologyKey`, a label selector, and `whenUnsatisfiable`, which defaults to `DoNotSchedule`. That last field is the entire decision, and it reduces to one question: when the constraint cannot be met, is not running better than being unbalanced?

`DoNotSchedule` says yes. It is usually right across `topology.kubernetes.io/zone` for a workload that must survive losing a zone, and its cost is pods stuck Pending during a zone outage — which is exactly when you wanted to scale up. `ScheduleAnyway` says no, and degrades to a scheduler preference instead. Pairing the two across zone and host is common, but derive it from the question rather than copying the pairing.

Two things about anti-affinity. `podAntiAffinity` with `requiredDuringSchedulingIgnoredDuringExecution` on hostname is the blunt older form of the same intent: it caps the replica count at the number of eligible nodes, so a scale-up during a spike leaves pods Pending. And `IgnoredDuringExecution` is the load-bearing half of the name — nothing rebalances after scheduling, so a zone that comes back stays empty until pods are recreated. Rebalancing is a descheduler's job, not a constraint's.

Before relying on any topology key, confirm the nodes actually carry that label. A constraint whose key matches no node is not an error; it simply does nothing.

### 8. Shutdown: pod termination and endpoint removal race

The documented sequence, which matters because two of its steps are concurrent:

1. The pod is marked Terminating and the grace period clock starts.
2. The `preStop` hook runs, inside the grace period. If it overruns, the kubelet grants one 2-second extension and proceeds.
3. SIGTERM goes to PID 1 of each container — or the image's `STOPSIGNAL`, which many runtimes send instead.
4. **At the same time** as 2 and 3, the control plane begins removing the pod from the EndpointSlices of matching Services.
5. On expiry of the grace period, SIGKILL.

Step 4 being concurrent rather than sequential is the whole problem, and it is worse than concurrent: endpoint removal has to propagate to every kube-proxy, ingress controller and cloud load balancer, each on its own schedule. Until it has, traffic is still arriving at a process that has already been told to stop. This is the connection-reset spike that appears in every rollout and gets blamed on the load balancer.

The fix is a `preStop` hook that does nothing but wait, so SIGTERM is delayed until propagation has happened:

```yaml
lifecycle:
  preStop:
    exec:
      command: ["sleep", "10"]   # provisional until measured
terminationGracePeriodSeconds: 45
```

There is no correct sleep value to copy, and anyone quoting one is quoting their own dataplane. It is the propagation delay of yours, and it differs between iptables kube-proxy, IPVS, an eBPF CNI, an ingress controller, and a cloud load balancer with its own health-check interval and deregistration delay. Measure it: roll the deployment repeatedly under steady load and read the edge error count against the sleep value, raising it until the errors stop.

Then set `terminationGracePeriodSeconds` — default 30 — above the sleep plus the longest in-flight request plus connection drain, because the grace period is the budget all of those share rather than an addition to them.

Two things that make the hook useless anyway:

- PID 1 has to handle SIGTERM. When it is a shell, the signal reaches the shell and the application never sees it; every pod then burns the full grace period and exits 137, which reads as an OOMKill on the dashboards. Entrypoint form belongs to `image-hardening`; the symptom belongs here.
- A sidecar proxy that exits first fails the requests still in flight. Native sidecar containers — init containers with `restartPolicy: Always`, on by default since v1.29 — are terminated only after the last main container has stopped, in reverse order of definition, which is the ordering you want. A proxy declared as an ordinary container gets SIGTERM at an arbitrary time in an arbitrary order.

### 9. Rehearse the two failures a review cannot see

```bash
set -Eeuo pipefail
NS=production
APP=checkout
NODE=node-7

# 1. The drain deadlock. Blocking here on "Cannot evict pod as it would violate the
#    pod's disruption budget" is the step 5 failure, found now rather than during a
#    cluster upgrade window.
kubectl drain "$NODE" --ignore-daemonsets --delete-emptydir-data --timeout=300s

# 2. The endpoint race. Roll twice under steady load and count errors at the edge;
#    a spike bounded by the rollout is the step 8 failure.
kubectl rollout restart deploy/"$APP" -n "$NS"
kubectl rollout status deploy/"$APP" -n "$NS" --timeout=300s
```

Before merging, answer each of these without opening the manifest again: what happens when the node fills up, when this node is drained, when the main dependency is down, and when a deploy goes out at peak. Any answer of "I would have to look" names a field that has not actually been decided.

## Reference files

- `references/resource-profiling.md` — measuring the profile: which statistic to use for each resource and why, the full queries, the VPA recommender in `Off` mode, in-place resize, and what a provisional number needs attached to it. Read it at step 1, before writing any number.
- `references/probes-and-lifecycle.md` — every probe field with its default, the three probes' distinct questions, a worked startup budget, the full termination sequence, how to measure the `preStop` sleep, and sidecar ordering. Read it at steps 4 and 8.
- `references/disruption-and-rollout.md` — budget shapes with the drain arithmetic, `unhealthyPodEvictionPolicy`, rollout parameters worked through real replica counts, and topology spread against anti-affinity. Read it at steps 5 to 7.

## Anti-patterns

**Copying resource numbers from the service next door.** The neighbour's numbers were also copied, and the chain usually terminates in a tutorial. It is invisible because it works: the pod schedules and serves, and the cost shows up as either a monthly bill nobody attributes or an OOMKill under a load profile the original service never had.

**Setting the CPU limit equal to the request to be safe.** It protects nobody. The limit constrains only the workload carrying it, throttling it inside a 100ms window while the node sits idle, and the neighbours were already protected by accurate requests. The exceptions in step 2 are real but each has to be named.

**Raising the memory limit whenever the pod is OOMKilled.** Correct exactly once, when the original number was too low. Against a leak it buys time proportional to the headroom and converts a loud failure into a slower one that now happens overnight. The limit is not the fix; the profile from step 1 is what says which case this is.

**A liveness probe that checks a dependency.** The most expensive line in a manifest. It guarantees that a downstream outage is amplified into a self-inflicted restart storm across every replica, at the precise moment when keeping warm caches and open connections is what would have let you ride it out.

**A PodDisruptionBudget over a single replica.** It reads as care and functions as a permanent block on node drains. Whoever is draining eventually bypasses it, so the disruption happens anyway — the budget only delayed it, and claimed an availability guarantee one replica cannot honour.

**Trusting the Deployment to roll itself back.** It does not. `progressDeadlineSeconds` expiring sets a condition on an object; the bad ReplicaSet stays up and keeps being retried. Either something watches for that condition or the rollback is a human noticing.
