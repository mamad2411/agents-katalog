---
name: k8s-upgrade
description: "Upgrade a Kubernetes cluster one minor at a time — control plane, add-ons, node pools — after finding removed or deprecated APIs from live traffic, not git manifests: the apiserver_requested_deprecated_apis metric and the audit log, with kubent or pluto as a second opinion. Fix every PodDisruptionBudget that would block a drain before the window opens, canary one node pool across a full traffic peak, then roll the rest. Use when someone asks to upgrade EKS, GKE, AKS or a self-managed cluster to the next minor version, plans a maintenance window for a version bump, or asks what an upgrade breaks or whether anything still calls a removed API. Not for a workload already broken (k8s-triage), sizing a workload's resources or its PodDisruptionBudget (k8s-workloads), or building and cutting over to a replacement cluster once that is the decision (plan-platform-migration)."
allowed-tools: Bash(kubectl:*), Bash(jq:*), Bash(aws:*), Bash(gcloud:*), Bash(az:*), Bash(kubeadm:*), Bash(kubent:*), Bash(pluto:*), Read, Write, Grep, Glob
---

# Kubernetes Cluster Upgrade

The control plane, every add-on and every node pool move to the target minor version on
the planned date, with no workload discovering a removed API for the first time in
production.

The job is hard because the two mistakes that cause an upgrade window to become an
incident both look like diligence beforehand. Checking manifests in git and Helm charts
for deprecated `apiVersion` strings feels thorough, but a Helm release, an operator or a
controller creates objects the repository never shows, so a manifest-only scan
under-reports by exactly the objects that matter most — live traffic is the only source
that cannot lie about what is actually being requested. And compressing several minor
hops into one weekend "since we're already down anyway" feels efficient, but Kubernetes'
own version-skew policy forbids the control plane from skipping a minor even on a
single-instance cluster, so each hop is a separate, one-way change, and stacking them
removes the ability to attribute a regression to the hop that caused it.

## Scope

Use for: planning and sequencing a routine, scheduled Kubernetes minor-version upgrade —
control plane, add-ons and node pools — for a self-managed or managed (EKS, GKE, AKS)
cluster; finding what a target version removes before the window opens; sequencing
add-on upgrades against the new control plane; and deciding whether a routine upgrade is
still the right shape or should become a replatform.

Do not use for: a workload that is currently broken, which is `k8s-triage`; sizing a
workload's own resource requests, limits or PodDisruptionBudget, which is
`k8s-workloads` even though this skill's step 3 surfaces the budgets that would block a
drain; a database's own major-version upgrade, which has its own lock, statistics and
compatibility surface entirely separate from the cluster's; and, once this skill's own
decision table says a cluster is too far behind to sequence in place, building and
cutting over to its replacement — that is `plan-platform-migration` for the phased design
and `cutover` for the switch window itself, not a replacement for the decision made here.

## Workflow

### 1. Establish current and target versions, and refuse to skip a minor

```bash
kubectl version -o json
aws eks describe-cluster --name "$CLUSTER" --query cluster.version
gcloud container clusters describe "$CLUSTER" --format='value(currentMasterVersion)'
az aks show --name "$CLUSTER" --resource-group "$RG" --query kubernetesVersion
```

*Gate:* the control plane moves one minor at a time, even on a single-instance cluster —
Kubernetes' own version-skew policy requires this, not a house preference. A target more
than one minor away is N sequential upgrades, planned and executed one at a time, never
compressed into a single window.

### 2. Find removed and deprecated APIs from live traffic before touching anything

Query `apiserver_requested_deprecated_apis` — the `removed_release` label gives the
version that stops serving each hit — and grep the audit log for the same requests on
clusters that do not retain metrics long enough. Run `kubent` and `pluto` over the
manifest repository as a second opinion, never as the answer: both tools read what is in
git or in a running Helm release, and neither sees an object a controller or operator
created that git never shows.

*Gate:* do not schedule the control-plane step until every hit against the target
version's removed list has an owner and a merged fix, or is confirmed to be a stale
metric sample from a workload already retired. Read
`references/deprecated-api-detection.md` now for the full query, the audit-log
fallback, the two tools' invocations, and how to read a provider's per-version removal
notes against the upstream deprecation guide.

### 3. Fix every PodDisruptionBudget that would block a drain

```bash
kubectl get pdb -A -o json | jq -r '.items[] | select(.status.disruptionsAllowed == 0) | "\(.metadata.namespace)/\(.metadata.name)"'
```

Select on `.status.disruptionsAllowed == 0` rather than pattern-matching the spec —
matching only `minAvailable: "100%"` or a zero `maxUnavailable` misses an integer
`minAvailable` equal to the replica count (3 of 3 is as blocking as "100%" and neither
`==` test above catches it), and `disruptionsAllowed` is the live, resolved value
Kubernetes already computed from whichever form the spec used. A zero can also be
temporary rather than a policy choice — pods currently unhealthy push it to zero too —
but either way the drain blocks, so it belongs on this list regardless of which caused it.

Also list every single-replica workload carrying a budget at all — `k8s-workloads` step
5's deadlock arithmetic applies here, and the fix (raise replicas, or accept the
disruption and remove the budget) belongs there; this step only finds the list.

*Gate:* every budget on the list is resolved before step 6, or the node-pool drain
stalls indefinitely mid-window. Discovering a blocking budget during the drain converts
a scheduled maintenance window into an incident running `k8s-triage`'s procedure instead
of this one's.

### 4. Upgrade the control plane

```bash
aws eks update-cluster-version --name "$CLUSTER" --kubernetes-version "$TARGET"
gcloud container clusters upgrade "$CLUSTER" --master --cluster-version "$TARGET"
az aks upgrade --name "$CLUSTER" --resource-group "$RG" --kubernetes-version "$TARGET" --control-plane-only
kubeadm upgrade apply "$TARGET"   # self-managed
```

*Gate:* there is no rollback for this step. Say so in the plan document before the
window opens, not during it, and do not compress it into the same maintenance action as
an add-on or node-pool step that still has one.

### 5. Upgrade add-ons in this fixed order: CNI, CoreDNS, kube-proxy, CSI driver, ingress controller

Each add-on moves to a version compatible with the new control plane before the next one
is touched. Nothing schedules without the CNI, and DNS and kube-proxy are load-bearing
for everything that follows — an ad hoc order turns "which add-on broke this" into a
guess.

*Gate:* confirm each add-on's own compatibility statement against the new control-plane
version before upgrading it. Read `references/upgrade-sequence-and-skew.md` now for the
version-skew table condensed to what decides ordering, the no-skip rule's source, why
each add-on in the fixed order is a prerequisite for the next, and the decision table
for when "more than one minor behind" means a new cluster rather than N hops.

### 6. Canary one node pool, then bake across a full traffic peak

```bash
kubectl cordon "$NODE"
kubectl drain "$NODE" --ignore-daemonsets --delete-emptydir-data --timeout="$COMPUTED_TIMEOUT"
```

Compute the timeout from step 3's surviving PodDisruptionBudgets times the time a pod
takes to become ready — the same arithmetic `k8s-workloads` step 5 states for sizing a
drain.

*Gate:* do not roll the remaining node pools until the canary has served one full
traffic peak with the SLI unchanged. "No errors in an hour" and "no errors across a full
peak" are different claims, and the failure modes an upgrade introduces — a subtly
incompatible CNI version, a CoreDNS config drift — often surface only under peak
concurrency.

### 7. Re-run step 2 at the new version

Zero hits are expected. Any remaining hit is a workload that needs fixing before the
*next* upgrade, not before this one closes out.

## Hard gates

1. Never skip a minor on the control plane, including on a single-instance cluster.
2. Deprecated-API usage is checked against live traffic, never against manifests in git
   alone.
3. Every PodDisruptionBudget that would block the drain is resolved before the node-pool
   step, not discovered during it.
4. The control plane has no rollback. Treat it as one-way and isolate it from any step
   that still has one.
5. When the target is more than one minor away and the downtime budget cannot absorb N
   sequential control-plane hops, hand the cluster to `plan-platform-migration` for the
   phased design and `cutover` for the switch window — never compress N in-place hops
   into one weekend.

## Output format

```markdown
## Current state
[control-plane version, add-on versions, node-pool versions, target version, minors of gap]

## Deprecated and removed API findings
| API | Requests in window | Source object | Owner | Status |

## Blocking PodDisruptionBudgets
| Namespace/name | Current setting | Fix applied |

## Sequence
| # | Component | From | To | Rollback | Bake |

## Canary and bake plan
[pool, traffic peak covered, SLI watched, bake duration]

## Abort criteria
[per step, what stops the window and what state it leaves the cluster in]
```

## Anti-patterns

**Trusting kubent or pluto as the whole picture.** kubent recovers an object's original
`apiVersion` from the `kubectl.kubernetes.io/last-applied-configuration` annotation that
`kubectl apply` sets, and pluto covers git manifests and Helm releases; an object an
operator or controller created directly, through neither path, carries none of that and
is invisible to both. Read live traffic first, and treat both tools as confirmation of
what you already found, not as the search itself.

**Compressing more than one minor hop into a single weekend "since we're already
down."** Each hop is a separate, one-way control-plane change. Stacking them does not
reduce the number of failure points; it removes the ability to attribute a regression to
the hop that caused it.

**Calling the bake done at "no errors in an hour."** An hour with no errors and a full
traffic peak with no errors are different claims, and the failure modes an upgrade
introduces often surface only under peak concurrency.

**Fixing a blocking PodDisruptionBudget the day of the upgrade.** Discovering it during
the drain converts a scheduled maintenance window into an incident.

**Upgrading add-ons in whatever order the changelogs arrived.** The fixed order exists
because nothing schedules without the CNI, and an ad hoc order turns "which add-on broke
this" into a guess.

## Reference files

- `references/deprecated-api-detection.md` — read at step 2: the full
  `apiserver_requested_deprecated_apis` query with the `removed_release` label, the
  audit-log fallback, the `kubent` and `pluto` invocations and their shared blind spot,
  and how to read a provider's per-version removal notes against the upstream
  deprecation guide.
- `references/upgrade-sequence-and-skew.md` — read at steps 1, 4 and 5: the
  version-skew table condensed to what decides ordering, the no-skip rule with its
  source, the fixed add-on order and why each one is a prerequisite for the next, and
  the decision table for when "more than one minor behind" means a new cluster rather
  than N hops.
