---
name: k8s-audit
description: "Live, read-only audit of a running cluster on a context the user confirmed: API removals, CIS posture, runtime vs declared, utilisation."
kind: skill
pack: infrastructure
allowed-tools: [Read, Grep, Glob, Bash]
---

# k8s-audit

## Boundary — this skill audits the CLUSTER, not the YAML

Everything decidable from the repo is decided offline on the render: `k8s-render-scan` (render, Helm, Kustomize, GitOps spec), `k8s-availability-scan` (CPU request + memory request + memory limit, probes, PDBs, HPA/KEDA floors, spread, rollout, shutdown), `k8s-wiring-scan` (Services, config propagation, NetworkPolicy paths, Jobs, RBAC wiring) and `k8s-api-version-scan` (removed APIs in files, schema, admission), judged by `@k8s-reviewer`. Pod privilege, RBAC breadth and secrets in manifests are security `iac-scan` § 3's when the security pack is installed.

**Do not restate those here.** If a finding can be made from the files, hand it to its detector. What is left needs the live cluster:

| Axis | Why only the cluster can answer it |
|---|---|
| 1. API removals in what is deployed | Helm release manifests stored in the cluster and objects applied by hand are not in the repo |
| 2. CIS / node posture | kubelet flags, etcd, API-server config — none of it is in the repo |
| 3. Runtime vs declared | restarts, OOMKills, pending pods, out-of-band drift, `disruptionsAllowed`, expiring certs |
| 4. Live utilisation | requests are declared; *usage* is measured |

## Premise

Every finding cites the tool-output line it fired on: the pluto row, the failed `kube-bench` control id, the `kubectl top` figure beside the declared request, the `kubectl get` query and its output, **and the context it was read from**. No cite → no finding. "Looks over-provisioned" is a vibe; `requests.cpu: 2 / p95 usage 0.08 cores over 7d` is a finding.

## Halt conditions

- **Context halt (2026-10-10 rule).** Never read the default or current context. Before any live command, name the cluster context (and kubeconfig file) and run only after the user confirms that exact context **in this session**. Every command passes it explicitly: `kubectl --context=<ctx>`, `pluto … --kube-context=<ctx>`, `helm --kube-context <ctx>`. A command that takes no context flag runs with `KUBECONFIG=<the file the user named>`. No confirmed context → every axis prints `NO-DATA(<context>)`, never a pass.
- **Read-only verbs only:** `get`, `describe`, `top`, `events`, `auth can-i`, `version`. Never `apply`, `delete`, `patch`, `edit`, `drain`, `cordon`, `scale`, `rollout restart`, `exec`, `port-forward`, `helm install/upgrade/rollback`, or any `--dry-run=server` against the user's cluster (a dry-run belongs on a scratch kind cluster, precedents § 56).
- **Never run `kubent`.** It is stale (0.7.3, 2024-08), contacts the ambient context when run bare, and exits 0 with findings (precedents § 55). pluto replaces it.
- **Never loop over binaries with `version`**: some ignore their arguments and list the ambient cluster.
- Halt on any finding that cannot name the tool line or parsed field it fired on, or the context it came from.
- Halt on a utilisation claim without BOTH numbers — the declared request AND the measured usage, with the window.
- Halt on a deprecation finding without the cluster's current minor AND the removal minor from the deprecation guide.
- Halt on anything a static detector owns (see Boundary) — hand it over instead of restating it.
- Do not propose auto-fix against a running cluster. Report; humans decide.
- High or critical rows pass through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/infrastructure.md`](../../../../snippets/precedents/infrastructure.md) before they are reported as confirmed; under `/infra-audit --live=<context>` the judge is `@k8s-reviewer`.

## Tools

| Axis | Tool (always with the confirmed context) | The citation it produces |
|---|---|---|
| API removals | `pluto detect-helm --kube-context=<ctx> -o json --target-versions k8s=v<next minor>`; `pluto detect-api-resources --kube-context=<ctx> …` | release or resource + apiVersion + removal minor |
| CIS posture | `kube-bench` (a Job the platform team runs on worker nodes; the skill reads its output, it never schedules it) | the failed control id + its remediation text |
| Runtime | `kubectl --context=<ctx> get`/`describe`/`get events`, the GitOps controller's sync status | the field or event line |
| Utilisation + cost | `kubectl --context=<ctx> top` (metrics-server), OpenCost / Kubecost | the measured series beside the declared request |

pluto's default target minor is stale: always pass `--target-versions` with the minor read from the cluster (precedents § 54). If a tool is not installed, say so and mark that axis **UNVERIFIED**. Never infer an axis you did not measure.

## Checks

### 1. API versions the cluster is about to stop serving

- Record the control-plane minor first (`kubectl --context=<ctx> version -o json`) — every finding is relative to it.
- Kubernetes maintains **only the three most recent minors** (https://kubernetes.io/releases/). A cluster outside that window is a finding on its own, at the top of the report. Dated support facts are re-read at audit time (precedents § 62).
- Run pluto on the Helm releases and live API resources. Report each hit as: `<resource> · <apiVersion> · removed in <minor> · your next upgrade target is <minor>`, citing the deprecation guide (https://kubernetes.io/docs/reference/using-api/deprecation-guide/), never memory.
- What the repo renders is `k8s-api-version-scan`'s; report only what is deployed and absent from the render (a Helm release from a runbook, an object applied by hand).
- Include CRDs and third-party controllers, each against its own supported-minor matrix.

### 2. Node + control-plane posture (CIS)

- `kube-bench` output for the node roles the cluster runs (managed control planes are the provider's — scope to worker nodes and say so).
- Report failed control ids with their remediation text; suppress the provider-owned ones, naming which.

### 3. Runtime reality vs declared intent

- **Crash/restart pressure** — non-zero restart counts and the last termination reason (`OOMKilled` is a memory-limit or request problem; `Error` is the app's).
- **Unschedulable work** — `Pending` pods and the scheduler's reason from the event line. A `Pending` pod is an HA claim that is not true.
- **Out-of-band drift** — a live spec that differs from git, or an object no GitOps `Application`/`Kustomization` owns. HPA- or KEDA-driven `replicas` drift is expected; a changed image or resource block is not. Reconciliation drift is devops `gitops-audit`'s when that pack is installed.
- **Drain blockers** — PDBs with `status.disruptionsAllowed: 0` now. The static PDB arithmetic is `k8s-availability-scan` § 3; this is the cluster's answer today.
- **Certificate expiry** — cert-manager `Certificate` objects whose last renewal failed or that are near expiry. The inventory and signal are `dns-tls-lifecycle-scan`'s.
- **Node conditions** — `MemoryPressure` / `DiskPressure` / `PIDPressure` on any node, and the workloads evicted next.

### 4. Live utilisation

- **Over-provisioned requests** — requests vs p95 usage. The audit's default threshold: usage below one quarter of request, sustained over at least seven days; state it in the report.
- **Under-provisioned requests** — usage at or above request. A missing CPU **limit** is not a finding (precedents § 1); a CPU limit that throttles a served workload is.
- **Unattached PVCs** — bound to no pod, with size; a price only from a bill line or a dated pricing page (`/cost-audit`).
- **Idle Deployments** — zero request rate over the window, from the metrics backend.

## Output

```
K8s audit — context <ctx> (confirmed in session) · control plane v<minor> (<in / OUT of> the supported window)

HIGH:
  ✗ helm release <name>: <kind> <apiVersion> removed in v<minor> (pluto detect-helm, target v<next>) — the upgrade fails on it
  ✗ kube-bench control <id> FAIL on worker nodes — <remediation summary>
  ✗ Deployment <name>: <n> restarts, last reason OOMKilled, memory limit <x> vs peak <y>
MEDIUM:
  ⚠ PDB <name>: status.disruptionsAllowed=0 — no node holding these pods can be drained today
  ⚠ Deployment <name>: requests.cpu <r>, p95 usage <u> over 7d (below the 1/4 threshold)
Handed to the static detectors (not audited here): k8s-availability-scan · k8s-wiring-scan · k8s-api-version-scan
UNVERIFIED (tool absent): <axis> — <tool> not installed · NO-DATA(<ctx>) when no context was confirmed
```

## Rules

- Audit production separately from staging; one confirmed context per run.
- Every axis is measured-and-cited, UNVERIFIED or NO-DATA. There is no fourth state.
- Blocking findings become a ticket with an owner and a deadline; API-removal rows get the upgrade window as their deadline.

## Related

- `k8s-render-scan`, `k8s-availability-scan`, `k8s-wiring-scan`, `k8s-api-version-scan` (this pack) — everything decidable from the render; `@k8s-reviewer` judges them.
- `@kubernetes-architect` — upgrade cadence and addon-matrix policy that axis 1 measures.
- `network-exposure-audit` (this pack) — network correctness and the live exposure reads; exposure classes are security's.
- `dr-audit` — backup and restore posture, including PV snapshots and operator backups.
