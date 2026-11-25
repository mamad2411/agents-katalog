---
name: k8s-availability-scan
description: "Availability of rendered Kubernetes workloads: requests, probes, PDB drain over the HPA/KEDA floor, spread, rollout, shutdown timing, platform SPOFs."
kind: skill
pack: infrastructure
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: k8s-availability-scan

## Premise

A workload is available when the disruptions a cluster performs every week — a node drain, a rollout, a scale event, a SIGTERM — cost no requests. None of that shows in the file that sets it. A PodDisruptionBudget with `minAvailable: 1` is correct on a worker whose KEDA floor is 2, and it blocks every drain on a Deployment with one replica. An HPA on CPU never scales a container with no CPU request. A `preStop` of 10 s plus a drain of 30 s fits a 45 s grace period exactly, and the same numbers kill in-flight work at 40 s. Scanners get this wrong in both directions: they demand a CPU limit (precedents § 1), read an HPA-managed Deployment as one replica (§ 6), and have no idea what KEDA is.

This skill reads **the render** — what `k8s-render-scan` § 0 wrote per environment — never the source YAML. `scripts/availability.sh` (beside this file, installed as `.claude/skills/k8s-availability-scan/scripts/availability.sh`; jq only, offline, bash 3.2 and zsh, `--self-test`) joins every object in `render-<env>.json` and prints one candidate row per class site. Its floor is the corrected one: KEDA `ScaledObject.minReplicaCount` (default 0) and HPA `minReplicas` before `spec.replicas` (precedents § 42). The research join it replaces read only HPA + `spec.replicas`, and on a real repo its one PDB row was a false positive from a KEDA floor of 2.

**Every finding cites the source `<file:line>` (from `__src`) + the environment whose render shows it + the CD target or runbook line that deploys it + the floor and where it came from + the oracle that proved it + the fix in the source.** A jq row is a candidate. "Workloads are available" is never printed without the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/infrastructure.md`](../../../../snippets/precedents/infrastructure.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Infrastructure V267 (Pod-template classes, StatefulSet merged in), V268 (PDB drain), V269 (Scaling), V270 (Spread), V271 (Rollout shape), V272 (Shutdown timing) and V273 (Platform SPOF).

## The rule

A candidate is a finding when all four hold (the seven gates as `precedents/infrastructure.md` reads them for infrastructure):

1. **The environment is deployed** (gate 1). `cd-targets.tsv`, the deploy job or a runbook line applies the env that shows it. A dev overlay or a local stack is Hardening (precedent 7); documented temporary sizing is `accepted-risk` (precedent 47).
2. **The disruption occurs** (gate 2): a drain, a rollout, a scale event, a SIGTERM, a zone or node loss on a cluster that has more than one.
3. **No control already handles it** (gate 4): a LimitRange default, a KEDA or HPA floor, leader election in code, a mesh drain, a platform-level PDB, a cluster scheduler profile.
4. **The arithmetic or the oracle uses numbers the files name** (gates 3 and 6): the floor from the render, the grace period from the pod spec, the drain from the code, the chart default from the pinned chart. Never a remembered default for a version nobody read.

## Boundaries

- **Liveness that checks a shared dependency** (`/health/db`, `pg_isready` as liveness) → performance `request-path-scan` § 15 when the performance pack is installed; this skill prints a `route:` row and never grades it. Without the pack, the row reads `N/A (owner pack performance not installed)` and is listed.
- **Probe handler semantics** (a readiness endpoint that always answers 200, HC-01) → observability `metric-hygiene-scan` § 7 when that pack is installed. This skill owns probe **presence, shape and timings** in the manifest; without the pack, handler truth is `N/A (owner pack observability not installed)`.
- **Privilege** (`securityContext`, host namespaces, capabilities, RBAC breadth, mutable image tags as a supply-chain risk) → security `iac-scan` § 3 (grep 4j for tags) when the security pack is installed. Without it the row is tagged `security-class (owner pack not installed)`, listed, never graded.
- **The shutdown code chain** (SIGTERM handling, PID 1, the drain constant itself) → devops `deploy-safety-scan` § 5 and `container-build-scan` § 2 when the devops pack ships them. **The arithmetic is owned here** (`THR-SHUTDOWN-GRACE`); without a devops number, read the constant (grep 7).
- **`replicas` rendered beside an autoscaler in a Helm chart, a Kustomize env or under Argo selfHeal** → `k8s-render-scan` § 2, § 3f, § 4a (this pack). § 4 here grades only the plain-manifest (`raw`) form, so one root cause is one finding.
- **Config rollout, Service and port wiring, NetworkPolicy paths, Job and CronJob run controls, RBAC wiring** → `k8s-wiring-scan` (this pack). **Removed APIs, schema, admission rejection, retired controllers** (K-INGRESS-RETIRED) → `k8s-api-version-scan` § 1–§ 4. **Unpinned charts** (PIN-HELM) → `iac-state-scan` § 3. **`maxReplicas × requests` as a cost** → `iac-cost-scan`.
- **Capacity headroom** → performance `@capacity-planner`; **pool × replicas vs `max_connections`** → database `connection-config-scan` § 2, which reads the HPA/KEDA ceiling this skill's § 4 prints.

## Version gate (gate 3), read from files

| Version | Where to read it | Why it changes the verdict |
|---|---|---|
| Target Kubernetes minor | the runbook's cluster-create `--version`, Argo destination + cluster docs, `kubeVersion` in `Chart.yaml`, a kind node image, CI `--kube-version` (the same read `k8s-render-scan` § Version gate makes) | Native `preStop.sleep` is GA in 1.34 and validated against the grace period; `exec sleep` never is (precedent 61). PDB `unhealthyPodEvictionPolicy` is stable in 1.31. Native sidecars are stable in 1.33. `matchLabelKeys` on spread constraints is beta. Supported minors on 2026-10-10 are 1.34–1.37, with 1.34 EOL on 2026-10-27 (precedent 62) |
| KEDA, metrics-server, ingress controller | the chart pin in `inventory-platform.tsv`, an Argo `targetRevision`, an image tag | `minReplicaCount` defaults to 0 and `maxReplicaCount` to 100 (KEDA ScaledObject spec, keda.sh 2.18, fetched 2026-10-10); a chart's replica and PDB defaults are its config (precedent 45). Unpinned → the default is unknowable → Unconfirmed |
| Helm major | CI and the runbook (as `k8s-render-scan` reads it) | Helm 4 server-side apply turns `replicas` on an HPA target into a failed upgrade, not a silent reset (precedent 60) |
| Node and zone count | the cluster-create line (`--node-pool … count=`, `min-nodes`, `node_count`, `desired_size`), the provider module | Single-node: zone spread is meaningless (precedent 8) and required anti-affinity strands a rollout |

No version found → the version-gated rows are Unconfirmed, with the probe written out (the minor from the provider console; `helm show values <chart> --version <v>`).

## Pre-flight

Run as **one** script from the repo root (shell state does not survive between tool calls). Render first; this skill never re-renders.

```bash
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/k8s.XXXXXX")}"
RS=.claude/skills/k8s-render-scan/scripts   # render.sh ships with k8s-render-scan
[ -f "$SCAN/render-ledger.tsv" ] || bash "$RS"/render.sh . --out="$SCAN" --kube-version=<target minor>
bash .claude/skills/k8s-availability-scan/scripts/availability.sh "$SCAN" --repo=. > "$SCAN/availability.tsv"   # §1–§9 candidate rows
awk -F'\t' 'NR > 1 { print $1, $2 }' "$SCAN/availability.tsv" | sort | uniq -c                                # counts per § and class

X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/.git/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.terraform/**'
   -g '!**/{test,tests,testdata,__tests__,spec,e2e,fixtures,__mocks__,mocks,examples}/**' -g '!**/*.{spec,test,e2e-spec}.*'
   -g '!**/*_test.go' -g '!**/{jest,vitest}.setup.*' -g '!**/setupTests.*' -g '!*.{lock,snap,map,svg}' -g '!**/{locales,i18n,translations}/**')
CODE=(-g '!*.{md,mdx,yml,yaml,json,txt}')                       # app code only: the drain and the lock live there
RB=(-g '*.{md,sh,bash,mk,tf,yml,yaml}' -g 'Makefile' -g 'Justfile')   # runbooks and IaC ARE read here: the cluster shape lives there

# 5. Leader election or a lock in code (precedent 5: a 1-replica Recreate singleton is intended).
rg -n --pcre2 '(?i)\bleader[-_]?elect\w*|\bleaderelection\b|\bLeaseLock\b|\bpg_try_advisory_lock\b|\bredlock\b|\bShedLock\b|@SchedulerLock\b' "${X[@]}" "${CODE[@]}" .
# 7. The app's drain: a shutdown constant, a server-close timer, a framework grace setting (precedent 46). Comment lines dropped.
rg -n --pcre2 '(?i)\b(?:shutdown|drain|grace(?:ful)?|terminat\w*)_?(?:drain_)?(?:timeout|delay|period|seconds|ms)\w*\s*[:=]\s*[\d_.]+|\bforceCloseConnections\b|\bcloseGraceDelay\b|\benableShutdownHooks\s*\(|\bserver\.close\s*\(|timeout-per-shutdown-phase|\bgraceful[-_]timeout\b|\bGracefulStop\s*\(|\.Shutdown\s*\(\s*ctx|\bshutdown_timeout\b' "${X[@]}" "${CODE[@]}" . \
  | rg -v --pcre2 '^[^:]+:\d+:\s*(?:\*|//|#|/\*)'
# 8. Cluster shape: node pools, node counts (precedent 8; required anti-affinity needs the nodes).
rg -n --pcre2 '(?:\bclusters?\s+create\b|\bcreate\s+cluster\b|\baks\s+create\b)|--node-pool\b[^\n]*\bcount=\d|\b(?:min|max)-nodes[= ]\d|^\s*(?:node_count|min_node_count|max_node_count|min_nodes|max_nodes|desired_size|min_size|initial_node_count)\s*=' "${RB[@]}" "${X[@]}" .
# 9. Request-path charts deployed by an Argo Application or Flux HelmRelease (the runbook lines are in inventory-platform.tsv).
rg -n --pcre2 '^\s*(?:chart|repoURL):\s*\S*(?:ingress-nginx|nginx-ingress|traefik|contour|envoy-gateway|gateway-helm|kong|haproxy|istio|cert-manager|keda|metrics-server|prometheus-adapter|coredns)\b' -g '*.{yml,yaml}' "${X[@]}" .
```

`availability.sh` row shape: `§ · class · env · origin · Kind/ns/name · detail · source file[:line]`. Class prefixes: `route:` (another owner; listed, not graded), `ctx:` (arithmetic inputs for the read step, never a finding), `info:` (state-the-intent, coverage only). `__src.line` is empty for Kustomize objects: cite the source file plus the `name:` line you read. Missing jq → § 1–§ 8 are `blocked (jq not installed)`. A failed or blocked render (`render-ledger.tsv`) makes every row for that env `blocked (render failed: <env>)`.

**Measured 2026-10-10** (render.sh, jq 1.7.1; `--self-test`: 32 rows, every seed hit, every decoy quiet, under bash 3.2, bash 5 and zsh):

| Target | Rows (no `ctx:`) | What they were |
|---|---|---|
| Research fixture (the 29-object bake-off render: raw + Kustomize prod/dev + chart) | 34 | Every seeded availability class the research jq caught (PDB ×2 incl. the 1-replica PDB, HPA-NOREQ ×2, HPA-REPLICAS ×3, MINMAX, RWO-ROLLING, ROLLOUT-SHAPE, SELECTOR-TEMPLATE, PROBE-SAME, EXEC-TIMEOUT, STS-SVC, the 60 s drain over a 30 s grace) and the deep-liveness seed as a `route:` row. Decoys quiet: no CPU limit (×14 workloads), the DaemonSet, the Job without probes, the leader-elected `Recreate` singleton, the HPA-managed Deployment with `replicas` omitted, `maxUnavailable: 1` + `AlwaysAllow`, the zone spread `ScheduleAnyway` |
| Real monorepo (Kustomize base + a managed-cloud overlay + 2 raw envs; not named) | base 16 · overlay 15 · local 7 · platform 6 | after reading: 1 Finding (2 sites), 4 Unconfirmed, 6 Hardening groups, 1 Refuted (§ Output). The research join's PDB row on the KEDA-floored worker is **gone**; its spread row on that worker now appears (the floor of 2 was invisible before) and is Hardening by precedent 44 |
| `benchmarks/fixtures/*` (15) | 2 of 15 render objects: 11 and 5 | none keyed (those fixtures seed database and security classes); rows are memory-overcommit, spread, PDB-missing, preStop on raw manifests. Greps: 7 → 3 / 0 hits (gunicorn `graceful_timeout`, two `enableShutdownHooks()`), 5 → 1 (an advisory-lock poller), 8 and 9 → 0 |
| Real repo greps | 7 → 1 (the drain constant `…_DRAIN_TIMEOUT_MS = 30_000`) · 5 → 0 · 8 → 6 (one node pool `count=1;min-nodes=1;max-nodes=2`) · 9 → 0 | |

## The 3,000-hit path

1. **Group** by (class, field path, root-cause file). Memory limit = 2–4 × request on every workload is **one finding with N sites**, fixed at the base or the chart helper. A class firing in every env from one base file is one group.
2. **Rank** prod CD-target envs first, then whatever a runbook applies by hand, then the rest. Within an env: § 3 BLOCK, § 6 rejected shapes, § 4 NOREQ, § 9, § 7, then the rest.
3. **Read** the top 20 groups fully and 3 samples from each remaining group.
4. **Dismiss** a whole env (a local stack, `examples/`) only with **one** read that shows nothing deploys it, and name it in the coverage block.
5. **Ledger the rest** as `Live, unreviewed (k groups / n rows — <the continuing command>)`. Never `checked`.

## Scans for

| § | Classes | Default severity |
|---|---|---|
| 1 | K-RES-MISSING, K-MEM-OVERCOMMIT, K-QUOTA-SHAPE, K-PRIORITY | RES-MISSING medium; QUOTA-SHAPE medium; MEM-OVERCOMMIT low (fleet group); PRIORITY low |
| 2 | K-PROBE-SAME, K-READINESS-MISSING, K-PROBE-STARTUP, K-PROBE-EXEC-TIMEOUT, K-PROBE-GRPC, K-PROBE-JOB; `route:` K-PROBE-DEEP | READINESS-MISSING and STARTUP medium; SAME low when both shallow (precedent 11), else medium; EXEC-TIMEOUT, GRPC, JOB low–medium |
| 3 | K-PDB-BLOCK, K-HPA-PDB, K-PDB-MISSING, K-PDB-ORPHAN, K-PDB-UNHEALTHY, K-PDB-API | BLOCK / HPA-PDB **blocker** on a prod workload; MISSING and ORPHAN medium; UNHEALTHY low |
| 4 | K-HPA-REPLICAS, K-HPA-NOREQ, K-HPA-MINMAX, K-KEDA-ZERO, K-HPA-VPA, K-HPA-BEHAVIOR | NOREQ and REPLICAS high; KEDA-ZERO and VPA medium; MINMAX low–medium; BEHAVIOR low |
| 5 | K-SPREAD, K-SPREAD-HARD, K-SPREAD-ROLLOUT | SPREAD low (precedent 44), medium when a PDB or a zone-loss requirement needs the guarantee on a multi-node cluster; HARD medium; ROLLOUT low |
| 6 | K-ROLLOUT-SHAPE, K-ROLLOUT-DEADLINE, K-HISTORY, K-RWO-ROLLING, K-STATEFUL-RECREATE, K-DS-UPDATE, K-STS-PODMGMT, K-SELECTOR-TEMPLATE; `route:` K-PULLPOLICY | a shape the API server rejects is a **blocker** (the prod render does not apply); RWO-ROLLING high; downtime shape and STATEFUL-RECREATE medium; DEADLINE, HISTORY, DS-UPDATE, PODMGMT low |
| 7 | K-SHUTDOWN-PRESTOP, K-SHUTDOWN-GRACE, K-SIDECAR-ORDER | medium; GRACE high when the killed work is a payment, an email or another side effect; SIDECAR-ORDER high on a Job that never completes |
| 8 | K-STS-SVC, K-STS-VCT, K-STS-PVC-RETENTION | medium; PVC-RETENTION `Delete` on a system-of-record store high; unset is `info` |
| 9 | K-PLATFORM-SPOF | high on a request-path controller (ingress or Gateway); medium for a cert-manager webhook, the KEDA operator or metrics-server under an HPA |

Severity drops one step on a deployed non-prod env (precedent 7) and to Hardening on one nothing deploys. No Kubernetes class has a CWE; the ids are the pack's.

### 1. Resources and QoS

```
BAD:   resources: {limits: {memory: 512Mi}}                         # no CPU request → BestEffort CPU, an HPA on CPU is inert
       resources: {requests: {memory: 128Mi}, limits: {memory: 2Gi}}   # 16× overcommit: the node's memory is promised twice
GOOD:  resources: {requests: {cpu: 250m, memory: 512Mi}, limits: {memory: 512Mi}}   # no CPU limit (precedent 1)
```
Every container is read — init containers and native sidecars included, never only `[0]`. The API defaults a missing request to its limit, so a limits-only container is not missing a request (a decoy the research join reported). **There is no CPU-limit row**: a missing CPU limit is not a defect (precedent 1, `rules/infra-principles.md`).

**Read the code:** Does a LimitRange in the namespace fill the default (gate 4; the row names it when it is in the render, but a platform-installed one is not)? Is a K-MEM-OVERCOMMIT ratio one convention across the fleet? Does a ResourceQuota on CPU or memory meet a namespace with no LimitRange (K-QUOTA-SHAPE: admission rejects the pod)? Is the K-PRIORITY workload one the cluster must keep under pressure?

**Finding when** a deployed served workload runs without a CPU or memory request, or without a memory limit where nothing defaults it (precedent 2), or a quota will reject it. **Proof:** V267 (Pod-template classes): the row prints for every env's render before the fix and not after; `kubectl apply --dry-run=server` on a scratch kind cluster with the namespace's quota rejects it ("must specify requests").

### 2. Probes: presence, shape, timings

```
BAD:   livenessProbe: {httpGet: {path: /ready}} = readinessProbe        # one dependency blip restarts every replica
       livenessProbe: {initialDelaySeconds: 90}, no startupProbe        # a slow boot loops; a hung process waits 90 s to die
       readinessProbe: {exec: {command: [pg_isready]}}                  # timeoutSeconds unset = 1 s; flaps under load
GOOD:  startupProbe for the boot budget · liveness = the process answers · readiness = it can serve now · exec timeout ≥ 3 s
```
**Read the code:** Is the handler both probes call shallow (it answers if the process serves)? Then identical probes are low (precedent 11); if it checks a dependency, the liveness half is `route → performance request-path-scan §15`. Is the container without readiness the one the Service's `targetPort` reaches? How long does the slowest boot take at the prod CPU request? Is the K-PROBE-JOB container a long-running worker disguised as a Job (precedent 3 flip)? Probes on ordinary Jobs and CronJobs are not applicable (precedent 3).

**Finding when** a served container takes traffic before it can serve, gets killed while it is still booting, or is restarted by a check that fails under load or a dependency blip. **Proof:** V267 rows plus the class oracle: a rollout under load gives 5xx while new pods start (K-READINESS-MISSING); a cold start on kind at the prod CPU request restarts in a loop (K-PROBE-STARTUP). The deep-liveness oracle is performance's.

### 3. PDB drain over the real floor

```
BAD:   PDB minAvailable: 1 · Deployment replicas: 1                       # disruptionsAllowed 0: every drain gets 429
       PDB minAvailable: 1 · KEDA minReplicaCount: 0 (unset)              # scaled up to 1 pod, the same deadlock (precedent 42)
       PDB maxUnavailable: 0                                             # nothing is ever evicted
GOOD:  ≥ 2 replicas + maxUnavailable: 1 + unhealthyPodEvictionPolicy: AlwaysAllow · or one replica and no PDB (accept the disruption)
```
The floor is KEDA `minReplicaCount` (default 0), else HPA `minReplicas` (default 1), else Rollout/Deployment/StatefulSet `spec.replicas` (default 1), and the PDB arithmetic uses `max(floor, 1)`: an activated KEDA target runs at least one pod. Percentages round up for both fields (kubernetes.io, *Specifying a Disruption Budget*, fetched 2026-10-10). A PDB on a DaemonSet is meaningless and never a row (precedent 4). `THR-K8S-PROD-FLOOR`: a served prod workload has a floor ≥ 2, a PDB that is `maxUnavailable: 1` or `minAvailable` below the floor, and **never a PDB on a single replica**.

**Read the code:** Which env is prod, and is its floor the trial overlay's (precedent 47)? Is the BLOCK target a deliberate undrainable singleton with a manual failover runbook (still a row, low)? Does the K-PDB-ORPHAN selector target pods an operator creates outside the render? For K-PDB-MISSING: is the workload leader-elected (precedent 5) or a dev overlay (precedent 7)? K-PDB-API: a `policy/v1beta1` PDB is one finding credited to `k8s-api-version-scan` § 1; a v1 PDB with `selector: {}` selects every pod in the namespace.

**Finding when** a deployed PDB leaves `disruptionsAllowed` at 0 with every pod healthy at the floor, or a served prod workload at ≥ 2 replicas can be fully evicted. **Proof:** V268 (PDB drain): on a scratch kind cluster (explicit `--kubeconfig`), `kubectl drain <node> --dry-run=server --ignore-daemonsets` or an Eviction with `dryRun: ["All"]` returns 429 before the fix and allows ≥ 1 eviction after. Fix by raising the floor (a capacity decision the user takes, with the arithmetic) or loosening the PDB — never by adding a PDB to one replica.

### 4. Autoscaling: HPA and KEDA

```
BAD:   HPA cpu Utilization 70 · container requests no cpu                 # ScalingActive=False: it never scales
       HPA owns the count · manifest still renders replicas: 3            # every client-side apply resets it; Helm 4 SSA fails the upgrade
       ScaledObject minReplicaCount: 0 · a Service selects the Deployment  # the first request after idle meets zero endpoints
       ScaledObject with no maxReplicaCount                               # KEDA default 100: an unbounded bill and downstream
GOOD:  requests on every container the metric reads · replicas omitted (precedent 6) · served floor ≥ 2 · max written
```
An HPA with no `metrics` defaults to CPU at 80 % (HPA v2 API reference, fetched 2026-10-10), so it needs CPU requests too. A KEDA `cpu`/`memory` trigger needs a request or limit on the containers whatever its `metricType` (KEDA cpu scaler prerequisites, keda.sh 2.18, fetched 2026-10-10). `THR-SCALE-CEILING`: every autoscaler has a written max; the `max × unit` arithmetic is `iac-cost-scan`'s, and the replica ceiling feeds database `connection-config-scan` § 2.

**Read the code:** For K-HPA-REPLICAS, which applier runs the env: `kubectl apply` (a fight on every apply), `--server-side` (a field-manager conflict) or Helm 4 (a failed upgrade, precedent 60)? Only the `raw` origin is graded here (§ Boundaries). Is `min == max` an incident pin with a ticket? Is the `minReplicaCount: 0` workload really served, or does the Service select it only for metrics? Does a VPA in `Auto` act on the resource the HPA scales on?

**Finding when** the autoscaler cannot scale, is undone by the deploy path, scales a served workload to zero, or has no ceiling. **Proof:** V269 (Scaling): on kind with metrics-server, `kubectl get hpa -o jsonpath='{.status.conditions[?(@.type=="ScalingActive")].status}'` is `False` with "missing request for cpu" before the fix and `True` after; an apply leaves `.spec.replicas` to the autoscaler; the floor read from the render meets `THR-K8S-PROD-FLOOR`.

### 5. Topology spread

```
BAD:   replicas: 3 · PDB maxUnavailable: 1 · no spread on a 3-zone pool   # the PDB assumes a spread nothing guarantees
       topologySpreadConstraints: {topologyKey: zone, whenUnsatisfiable: DoNotSchedule}   # no minDomains: zone loss → Pending
GOOD:  {topologyKey: kubernetes.io/hostname, maxSkew: 1, whenUnsatisfiable: ScheduleAnyway, matchLabelKeys: [pod-template-hash]}
```
"No spread" is a placement-guarantee gap, not "every replica on one node": with no cluster default, the scheduler applies soft constraints of hostname `maxSkew: 3` and zone `maxSkew: 5`, both `ScheduleAnyway` (precedents § 44, kubernetes.io, fetched 2026-10-10). A zone constraint on a single-zone cluster is meaningless (precedent 8).

**Read the code:** How many nodes and zones does the target cluster have (grep 8)? Does a PDB, an SLO or a zone-loss requirement need the guarantee? Does the cluster's scheduler profile disable the defaults (`defaultingType: List` with empty `defaultConstraints` — the precedent 44 flip)? With required hostname anti-affinity, do floor + surge pods fit the node count?

**Finding when** a multi-node or multi-zone prod cluster runs a workload whose availability requirement needs a placement guarantee that only soft defaults give, or a hard constraint can strand pods or a rollout. **Proof:** V270 (Spread): on a 3-node kind cluster, the replicas place as declared and a rollout completes under the constraint.

### 6. Rollout shape

```
BAD:   strategy: {rollingUpdate: {maxSurge: 0, maxUnavailable: 0}}        # the API server rejects it: the prod render does not apply
       replicas: 1 · maxUnavailable: 1                                     # every rollout takes the service to 0 ready pods
       RollingUpdate + an RWO PVC                                          # the surge pod cannot attach on another node
       revisionHistoryLimit: 0                                             # `kubectl rollout undo` has nothing to go back to
GOOD:  maxSurge ≥ 1, maxUnavailable 0 on small services · Recreate (or RWX) for an RWO volume · history ≥ 2
```
Deployment `maxUnavailable` percentages round down and `maxSurge` rounds up, against the floor. K-SELECTOR-TEMPLATE (a selector the template labels do not satisfy) is rejected at apply. K-DS-UPDATE covers `OnDelete`, a wide `maxUnavailable` on a node agent, and a DaemonSet surge with a `hostPort` [K?: whether the surge pod can bind; prove on kind]. `route:` K-PULLPOLICY fires only on `:latest` (or no tag) with an explicit `IfNotPresent`/`Never`; a SHA tag is never a row (precedent 50), and the mutable tag itself is security `iac-scan` 4j (precedent 9).

**Read the code:** Does the K-STATEFUL-RECREATE singleton write (a scheduler, a migrator, a primary) with no leader election (grep 5; precedent 5)? Is the RWO claim's storage class RWX in prod? Does a slow but healthy start exceed `progressDeadlineSeconds`? Is rollback done by git (GitOps), which makes K-HISTORY low?

**Finding when** the prod render is rejected, a rollout takes the service to zero, stalls on a volume, or two writers overlap. **Proof:** V271 (Rollout shape): `kubectl apply --dry-run=server` on kind (explicit `--kubeconfig`) rejects the shape before the fix; a two-node rollout with an RWO volume sits at `Multi-Attach` until the deadline, and completes with `Recreate` or RWX.

### 7. Shutdown timing — `THR-SHUTDOWN-GRACE`

```
BAD:   preStop exec [sleep, 10] · SHUTDOWN_DRAIN_SECONDS=60 · grace unset (30)   # 10 + 60 + 5 = 75 > 30: SIGKILL mid-drain
       preStop exec [sleep, 40] · grace 30                                       # unvalidated: the kill lands inside the sleep
       served pod, no preStop                                                    # endpoint removal races SIGTERM: 5xx per rollout
       istio-proxy / cloud-sql-proxy in containers                               # dies with the app on SIGTERM; a Job never completes
GOOD:  preStop {sleep: {seconds: 10}} (native, validated, GA 1.34) · drain 30 · grace 45 · the proxy as a native sidecar
```
The rule is `preStop_s + app_drain_s + 5 ≤ terminationGracePeriodSeconds` (default 30). The API server rejects a native `sleep` ≥ grace and never validates `exec: [sleep, N]` (precedent 61), so only this arithmetic catches the exec form. The drain often lives in code, not in env (precedent 46): `availability.sh` reads an env value whose name says shutdown/drain + timeout (a `…_MS` name or an `ms` suffix is divided by 1000) and prints a `ctx:SHUTDOWN` row with every input; when the drain is not in the manifest, take devops `deploy-safety-scan` § 5's number or grep 7's constant. Non-served workers are judged on checkpointing within the grace period, never on `preStop`.

**Read the code:** What does the app do on SIGTERM: stop accepting, finish in-flight, close pools, exit? Is the drain constant the one the entrypoint uses? Does a mesh or the load balancer drain the endpoint before SIGTERM (a DaemonSet behind a `LoadBalancer` Service: does the LB health check drain the node first)? Is the sidecar a native sidecar (`initContainers` with `restartPolicy: Always`)?

**Finding when** the arithmetic fails with every number read from a file, or a served workload has no endpoint-removal delay and the oracle shows errors. **Proof:** V272 (Shutdown timing): load through the Service during `rollout restart` on kind gives non-zero 5xx before the fix and 0 after (3 runs, within the noise band); a pod deleted mid-request ends with exit 137 before and 0/143 after. No load generator → `[report-flagged]` with the arithmetic as the static trace.

### 8. StatefulSet

```
BAD:   serviceName: pg-headless · no headless Service rendered          # no stable per-pod DNS; peers cannot find each other
       persistentVolumeClaimRetentionPolicy: {whenDeleted: Delete}       # deleting the set deletes the data
GOOD:  a Service with clusterIP: None of that name · Retain on a system-of-record store · VCT changes shipped as a migration
```
K-STS-VCT compares `volumeClaimTemplates` between the base-branch render (`k8s-render-scan` § 5 writes `$SCAN/base/`) and head; a template change does not resize existing claims [K?: partial mutability on 1.35+ — prove on kind before asserting]. An unset retention policy is `info` (Retain/Retain: state the intent).

**Read the code:** Is the headless Service owned by another chart or an operator? Is the `Delete` store a cache with a rebuild path (precedent 29)? **Finding when** a deployed set loses its identity DNS, its data on delete or scale-down, or a size change silently does nothing. **Proof:** V267 (StatefulSet variant): `nslookup <pod>-0.<svc>` fails on kind; scale 3 → 1 deletes the claims under `whenScaled: Delete`.

### 9. Platform single points of failure

```
BAD:   helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx   # no replicaCount, no PDB: the chart default
GOOD:  --version <pin> -f platform/ingress-values.yaml   # controller.replicaCount: 2, a PDB, spread — read at the pinned version
```
A component the request path needs, installed by a runbook, a Makefile, CI or an Argo `Application`, is in scope: its chart defaults are its config (precedent 45). `availability.sh` reads `inventory-platform.tsv` (`k8s-render-scan` § 0) and the install line's own `--set` keys and values files for `replicaCount`, `replicas`, autoscaling or a PDB, for ingress and Gateway controllers, cert-manager, KEDA, metrics-server, prometheus-adapter and CoreDNS. Grep 9 adds Argo and Flux installs. A runbook line that sets none prints K-PLATFORM-SPOF; one that sets them prints `ctx:PLATFORM`.

**Read the code:** Is the component on every request's path (ingress, Gateway) or on a control path (cert issuance, scaling metrics, admission webhooks)? What does the chart set by default at the **pinned** version (`helm show values <chart> --version <v>`: network, no cluster)? Unpinned → the default is unknowable → Unconfirmed, and PIN-HELM goes to `iac-state-scan` § 3 (V245). Does the repo's own runbook or diagram state the replica count (a static two-ended trace)? Is the controller retired (K-INGRESS-RETIRED → `k8s-api-version-scan` § 4; one finding per site, corroborating)?

**Finding when** a request-path component runs one replica (chart default or explicit) with no PDB in a deployed environment. **Proof:** V273 (Platform SPOF): with the chart's values at its pinned version on kind, killing the controller pod during load gives 5xx before the fix and 0 after; or the S-tier trace: the install line sets nothing **and** the chart default (or the repo's own runbook) says one replica.

## Tool lane

| Tool (measured version) | Command, on `$SCAN` | Reads | Trap |
|---|---|---|---|
| `render.sh` (`k8s-render-scan` § 0) | as § Pre-flight | every root, per env | Kustomize objects carry no source line; raw manifests do |
| jq 1.7.1 via `availability.sh` | `availability.sh "$SCAN" --repo=.` | every `render-*.json`, `inventory-platform.tsv`, `base/` | an env that failed to render has no JSON: read the ledger, never count it as clean |
| kube-score 1.20.0 (optional, cross-check only) | `kube-score score --kubernetes-version v<minor> --ignore-container-cpu-limit render-<env>.yaml` | objects + 2 canaries | without `--ignore-container-cpu-limit` it fires on precedent 1 (5 rows on the real repo); `pod-probes-identical` is precedent 11 |
| kube-linter 0.8.3 (optional) | `kube-linter lint --format json render-<env>.yaml canary.yaml` | fewer than rendered: drops removed APIs and YAML-1.1 objects (precedent 53) | reads an HPA-managed Deployment as 1 replica (precedent 6); `pdb-unhealthy-pod-eviction-policy` = K-PDB-UNHEALTHY |
| kind (scratch) | V267–V273, `KUBECONFIG="$SCAN/kind.kubeconfig"` on every call | — | never the user's context. No docker → the K-tier rows are `[report-flagged]` with the command written out |

A scanner's silence is not a pass (precedent 51); every class's coverage comes from `availability.sh` and the read step.

**Stacks real repos use:** plain manifests (raw envs) · Kustomize bases and overlays · Helm charts in the repo, per values file · charts installed from a remote repo by a runbook or CI (inventory rows; § 9 reads their defaults at the pin) · Argo CD Applications and Rollouts (a Rollout's `spec.replicas` is a floor; a `workloadRef` Rollout's template is the referenced Deployment) · Flux Kustomizations and HelmReleases (grep 9) · KEDA `ScaledObject` · Helmfile, cdk8s, Tanka and Timoni render through the project's own command into the same ledger, or the row reads `blocked (no renderer for <tool>)`.

## Output

```
k8s-availability-scan — target k8s 1.36 (runbook) · KEDA (chart UNPINNED) · nodes: 1 pool, count 1–2 (runbook) · Helm 4.2.4
Render: 4 envs · 60 objects · 0 failed (k8s-render-scan § 0) · availability.sh: 44 rows (38 + 6 platform) · 10 ctx

Findings: 1 · Unconfirmed: 4

1. ai/runbooks/<deploy runbook>.md:301 (+ :569)                         [report-with-fix]   high
   §9 K-PLATFORM-SPOF — ingress-nginx is installed with no replicaCount or PDB; every request goes edge → ingress → app.
   Static trace: the install line sets 2 unrelated --set keys; the operations runbook draws "ingress-nginx (1 pod)".
   Fix: a values file with controller.replicaCount: 2 + a PDB, pinned with --version. Corroborates: K-INGRESS-RETIRED (k8s-api-version-scan §4).

2. ai/runbooks/<deploy runbook>.md:305                                   [report-flagged]    medium
   §9 K-PLATFORM-SPOF — KEDA installed UNPINNED with no replica setting: the chart default is unknowable.
   Unproven link: the default at the deployed version. Settling run: `helm show values kedacore/keda --version <deployed>`.
3–5. cert-manager (UNPINNED) · metrics-server 3.14.0 (chart default unread; both CPU HPAs depend on it) · edge DaemonSet behind
   the LoadBalancer with no preStop (does the LB drain the node first?) — [report-flagged], each with its settling run.

Verification: 44 rows + 10 ctx → 12 groups → 1 finding · 4 unconfirmed · 6 hardening · 0 pre-existing · 1 refuted
  Refuted: §7 api — preStop 10 (exec) + SHUTDOWN_DRAIN constant 30 (code) + 5 = 45 ≤ grace 45 (precedent 46).
  Hardening: memory limit 2–4 × request, 14 rows → 1 group · PDB unhealthy-eviction ×6 · identical shallow probes ×2 (§ 11)
             · spread ×4 on a 1–2 node pool (§ 8, § 44) · served floor 1 on the trial overlay, accepted-risk (§ 47) · local env ×7 (§ 7)

Class coverage:
  §1  resources / QoS        checked (17 rows → hardening: 1 fleet group + the local env; 0 CPU-limit rows by design)
  §2  probes                 checked (6 → hardening: 4 identical shallow, 2 local exec; route: 0)
  §3  PDB drain              checked (6 → hardening; BLOCK 0 — the KEDA floor of 2 read, precedent 42)
  §4  autoscaling            checked (1 → accepted-risk) · KEDA max written: yes
  §5  spread                 checked (4 → hardening)
  §6  rollout shape          checked (0 rows)
  §7  shutdown timing        checked (4 prestop + 10 ctx → 1 refuted, 1 unconfirmed: edge DaemonSet behind the LB; local ×2)
  §8  StatefulSet            N/A (no StatefulSet rendered)
  §9  platform components    checked (6 inventory rows → 1 finding, 3 unconfirmed)
Tool ledger: render.sh RAN (60/60) · jq 1.7.1 RAN · kube-score NOT-RUN (optional) · kind NOT-RUN (no consent) → V268–V273 static only
```

`[report-with-fix]` means the deployed env, the arithmetic or oracle and the source fix are all in hand. `[report-flagged]` means one link is unproven — a chart default at an unread version, a drain constant not found, no scratch cluster for a K-tier oracle — and the row names that link and the run that settles it. The coverage block lists **§ 1–§ 9 on every run**: `checked (k rows → m)` only when the step ran; `N/A (<reason>)` when the render has no such object; `blocked (<reason>)` when the render failed or jq is missing; `Live, unreviewed (…)` for a partial review. Object names from a real repo stay in the user's report; the measured tables in this file describe the repo, never name it.

## False positives / precedents

The verifier reads [`precedents/infrastructure.md`](../../../../snippets/precedents/infrastructure.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **No CPU limit** is not a finding (§ 1). **Memory limit absent** is low–medium only with no LimitRange default (§ 2).
- **Probes on Jobs** are not applicable (§ 3). **Identical shallow probes** are low (§ 11).
- **A PDB on a DaemonSet** is meaningless (§ 4). **`replicas: 1` + `Recreate` on a leader-elected singleton** is intended (§ 5).
- **An HPA-managed Deployment with `replicas` omitted** is correct (§ 6). **The KEDA and Rollout floors** come first (§ 42).
- **Single-replica dev overlays** follow their env (§ 7); **documented trial sizing** is `accepted-risk` until launch (§ 47).
- **Zone spread on one zone** is meaningless (§ 8); **no spread** is a guarantee gap, not one-node placement (§ 44).
- **`imagePullPolicy` demands on digest or SHA tags** are noise (§ 9, § 50).
- **The drain may be a code constant** (§ 46); **a chart installed by a runbook is in scope** (§ 45).

## When to run

- In every `/infra-audit` that touches Kubernetes, after `k8s-render-scan` § 0, on every env's render.
- On a diff that changes a workload, PDB, HPA, `ScaledObject`, VPA, probe, `preStop`, grace period, strategy, spread, StatefulSet, or a runbook or CI line that installs a platform chart. Diff the **render**, not the source.
- Before a node-pool upgrade or a cluster minor upgrade (§ 3 decides whether the drain can finish), and before launch (`THR-K8S-PROD-FLOOR` on every served prod workload).

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/infra-audit` that is `@k8s-reviewer` in refute mode. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- **Never touch a real cluster.** The user's default kube context may be a real managed cluster. Every K-tier oracle runs on a scratch kind cluster with `KUBECONFIG="$SCAN/kind.kubeconfig"` (or `--kubeconfig`) on the same command line, created and deleted by the run; refuse when `KUBECONFIG` is unset or resolves to `~/.kube/config`. `kubectl drain`, `apply --dry-run=server` and Eviction calls contact whatever context they are given (precedent 56). A live read of the real cluster belongs to `k8s-audit`, behind its own context halt. Starting docker or a VM for kind is reported, and stopped by the run that started it.
- **Never write in the repo**, and never `helm install/upgrade`, `kubectl apply/patch/delete` outside the scratch cluster.
- Do not emit or accept a CPU-limit row, and do not recommend a PDB for a single replica.
- Do not judge a PDB, spread or HPA row without the floor and its source (KEDA, HPA, Rollout, `spec.replicas`).
- Do not judge `THR-SHUTDOWN-GRACE` without the drain number: read it, or the row stays Unconfirmed with the grep 7 hit to read.
- Do not grade a § 9 chart default from memory: read it at the pinned version, or the row is Unconfirmed.
- Halt on any finding without the source `<file:line>`, the env, the deploying CD target or runbook line, and the fix in the source.
- Do not print "workloads are available" without the coverage block, and do not report an env as checked when its render failed.
- Do not grade a class another skill or pack owns (§ Boundaries); cross-link it.

## Related

- `/infra-audit` (this pack) dispatches this skill after `k8s-render-scan`; `/infra-fix` closes its findings failing-first, at the base, chart or values file the prod CD target reads, and asks before any change that raises replicas, `minReplicas` or a node pool (capacity costs money).
- `@k8s-reviewer` judges the rows in refute mode. `/k8s-generate` should run § 1–§ 7 on its own output before it claims PRODUCTION-GRADE.
- `k8s-render-scan` (§ 0 render, § 2–§ 4 replicas forms, § 5 base render), `k8s-wiring-scan`, `k8s-api-version-scan` and `iac-state-scan` (this pack) own the neighbouring classes; `k8s-audit` owns the live cluster.
- Performance `request-path-scan` § 15, observability `metric-hygiene-scan` § 7, security `iac-scan` § 3, devops `deploy-safety-scan` § 5 and database `connection-config-scan` § 2 own the routed halves (§ Boundaries).
- `THR-K8S-PROD-FLOOR`, `THR-SCALE-CEILING` and `THR-SHUTDOWN-GRACE` live in `templates/governance/thresholds.json`.
