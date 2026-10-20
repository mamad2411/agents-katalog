---
name: kubernetes-month-of-lunches
description: "Knowledge base from \"Learn Kubernetes in a Month of Lunches\" by Elton Stoneman. Use when applying Stoneman's frameworks for Kubernetes Pods/Deployments, Services & Ingress, ConfigMaps/Secrets, volumes/PVC, StatefulSets/Jobs, rollouts, Helm, probes/self-healing, RBAC/security, logging/monitoring, autoscaling, CRDs/Operators — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Learn Kubernetes in a Month of Lunches
**Author**: Elton Stoneman | **Pages**: ~676 | **Chapters**: 22 | **Generated**: 2026-06-19

## How to Use This Skill

- **Without arguments** — load core frameworks below for reference
- **With a topic** — ask about `services`, `probes`, `rbac`, `helm`, `autoscaling`; I find and read the relevant chapter
- **With chapter** — ask for `ch12`; I load that specific chapter file
- **Browse** — ask "what chapters do you have?" for the full index

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**Desired-state / declarative model** (the book's spine). You describe *what* you want in YAML; Kubernetes decides *how* to reach and hold that state. Always `kubectl apply -f` manifests from source control — never `create`/`edit` imperatively in prod. The control loop continuously reconciles actual → desired; this is what powers self-healing.

**The container abstraction ladder.** Container ⊂ Pod ⊂ controller. You rarely manage containers or Pods directly — you manage the controller above them:
- **Pod** — smallest deployable unit; one or more containers sharing network + storage. Pods are disposable.
- **Deployment** — manages a ReplicaSet for stateless apps; gives rolling updates, rollback, scaling.
- **StatefulSet** — stable Pod identity + per-Pod storage for data apps.
- **DaemonSet** — one Pod per node (logging, monitoring agents).
- **Job / CronJob** — run-to-completion / scheduled tasks.
- Rule: *pick the controller by the workload's identity & lifecycle needs*, then let it manage Pods.

**Loose coupling by labels & selectors.** Services, controllers, and NetworkPolicies find Pods by *label selector*, never by name/IP. Pods come and go; labels are the stable contract. This indirection is what makes scaling, rolling updates, and service discovery work.

**Services = stable networking over disposable Pods.** A Service gives a fixed virtual IP + DNS name and load-balances across matching Pods. Pick by reach:
- **ClusterIP** — internal-only (default).
- **NodePort** — exposes on every node's port; dev/on-prem.
- **LoadBalancer** — cloud external LB.
- **ExternalName** — DNS alias to an external system.
- For HTTP routing across many apps on one entry point, use **Ingress** (host/path rules + an ingress controller), not many LoadBalancers.

**Configuration lives outside the image.** Ship one image, inject config per environment via **ConfigMap** (non-secret) and **Secret** (sensitive, base64). Mount as files (volume) when the app reads config files / for live updates; use env vars for simple values. Never bake config or secrets into images.

**Storage: claims, not disks.** Apps request storage abstractly with a **PersistentVolumeClaim**; a **StorageClass** dynamically provisions the backing **PersistentVolume**. Pods mount the PVC. For per-replica storage in a StatefulSet, use `volumeClaimTemplates`. `emptyDir` = Pod-lifetime scratch; `hostPath` = node-tied (avoid in multi-node).

**Self-healing = probes + resource limits + controllers.** Three pillars:
- **Readiness probe** → gate traffic: Pod removed from Service endpoints until ready. Make it depend on the app being able to serve.
- **Liveness probe** → restart: kill+restart a hung Pod. Keep it *independent of downstream deps* or you cascade restarts.
- **resources.requests/limits** → scheduler placement + OOM protection. Repeated crashes → `CrashLoopBackOff`; K8s won't reschedule a backing-off Pod to another node, so self-healing has limits.

**Safe releases: rolling update + rollback.** Deployments default to `RollingUpdate` (tune `maxSurge` / `maxUnavailable`); `Recreate` for apps that can't run two versions. Inspect with `kubectl rollout status/history`, revert with `kubectl rollout undo`. Helm adds pre-upgrade checks and atomic rollback of a whole release.

**Packaging with Helm.** A **chart** is a templated, versioned package; **values.yaml** parameterizes it; an **install = a release** you can upgrade/rollback as a unit. Use for reusable, multi-environment app distribution.

**Security is layered (defense-in-depth).**
- **RBAC** — least-privilege: bind `Role`/`ClusterRole` to users/groups/`ServiceAccount`s via `RoleBinding`/`ClusterRoleBinding`. Never hand out `cluster-admin`. Verify with `kubectl auth can-i`.
- **securityContext** — run as non-root, read-only root FS, drop capabilities.
- **NetworkPolicy** — default-deny then allow; segment Pod-to-Pod traffic.
- **Admission control** — validate/mutate specs before they're accepted.

**Workload placement & scaling.** Steer Pods with `nodeSelector` / affinity & anti-affinity; reserve nodes with **taints + tolerations**. Scale Pods on metrics with the **HorizontalPodAutoscaler** (needs metrics-server); scale nodes with the cluster autoscaler. Pending Pod = nothing fits its resources/affinity/taints.

**Extending Kubernetes.** **CRDs** add new resource types; a **controller** running a reconcile loop watches them and drives state — that pair is the **Operator pattern**. Serverless platforms (Kubeless/Knative) build on CRDs to run functions as Pods.

**Observability.** Centralize logs with the **EFK stack** (Fluentd DaemonSet → Elasticsearch → Kibana). Metrics with **Prometheus** (pull-based scraping of `/metrics`; client libraries for your apps, exporters for third-party, kube-state-metrics for cluster objects) → Grafana dashboards.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-fast-track-setup.md) | Before You Begin (Fast-Track Setup) | desired-state model, lab setup (Docker Desktop/K3s) |
| [ch02](chapters/ch02-pods-deployments.md) | Running Containers with Pods & Deployments | Pod, Deployment, container abstraction |
| [ch03](chapters/ch03-services-networking.md) | Connecting Pods over the Network with Services | Service types, DNS, selectors |
| [ch04](chapters/ch04-configmaps-secrets.md) | Configuring Apps with ConfigMaps & Secrets | ConfigMap, Secret, env vs volume |
| [ch05](chapters/ch05-volumes-storage.md) | Storing Data with Volumes, Mounts & Claims | PV, PVC, StorageClass, access modes |
| [ch06](chapters/ch06-scaling-controllers.md) | Scaling Apps Across Pods with Controllers | ReplicaSet, DaemonSet, scaling for load/HA |
| [ch07](chapters/ch07-multicontainer-pods.md) | Extending Apps with Multicontainer Pods | init container, sidecar, adapter, ambassador |
| [ch08](chapters/ch08-statefulsets-jobs.md) | Running Data-Heavy Apps with StatefulSets & Jobs | StatefulSet, volumeClaimTemplates, Job, CronJob |
| [ch09](chapters/ch09-rollouts-rollbacks.md) | Managing App Releases with Rollouts & Rollbacks | RollingUpdate, maxSurge/maxUnavailable, rollback |
| [ch10](chapters/ch10-helm.md) | Packaging & Managing Apps with Helm | chart, release, values.yaml, upgrade/rollback |
| [ch11](chapters/ch11-dev-workflows-cicd.md) | App Development—Workflows & CI/CD | Docker vs KaaS workflow, contexts/namespaces |
| [ch12](chapters/ch12-self-healing-probes.md) | Empowering Self-Healing Apps | readiness/liveness probes, resource limits |
| [ch13](chapters/ch13-logging-fluentd-elasticsearch.md) | Centralizing Logs (EFK Stack) | Fluentd DaemonSet, Elasticsearch, Kibana |
| [ch14](chapters/ch14-monitoring-prometheus.md) | Monitoring with Prometheus | pull scraping, exporters, kube-state-metrics |
| [ch15](chapters/ch15-ingress.md) | Managing Incoming Traffic with Ingress | Ingress rules, ingress controller, TLS |
| [ch16](chapters/ch16-security-policies-admission.md) | Securing Apps: Policies, Contexts, Admission | securityContext, NetworkPolicy, admission control |
| [ch17](chapters/ch17-rbac.md) | Securing Resources with RBAC | Role/ClusterRole, bindings, ServiceAccount, least-privilege |
| [ch18](chapters/ch18-cluster-multinode.md) | Deploying K8s: Multinode & Multiarch Clusters | kubeadm init/join, control plane, HA |
| [ch19](chapters/ch19-workload-placement-autoscaling.md) | Workload Placement & Automatic Scaling | affinity, taints/tolerations, HPA |
| [ch20](chapters/ch20-custom-resources-operators.md) | Extending K8s with Custom Resources & Operators | CRD, controller/reconcile loop, Operator |
| [ch21](chapters/ch21-serverless-functions.md) | Running Serverless Functions in Kubernetes | Kubeless, triggers, Serverless framework |
| [ch22](chapters/ch22-never-the-end.md) | Never the End | QoS classes, next steps |

## Topic Index

- **Admission control** → ch16
- **Affinity / anti-affinity** → ch19
- **Autoscaling (HPA / cluster)** → ch19
- **ConfigMaps** → ch04
- **Contexts / namespaces** → ch11
- **Control plane / kubeadm** → ch18
- **CronJobs** → ch08
- **CRDs / custom resources** → ch20
- **DaemonSets** → ch06, ch13
- **Deployments** → ch02, ch09
- **DNS / service discovery** → ch03
- **EFK / logging** → ch13
- **Helm (charts, releases, values)** → ch10
- **Ingress** → ch15
- **Jobs** → ch08
- **Liveness / readiness probes** → ch12
- **LoadBalancer / NodePort / ClusterIP** → ch03
- **Multiarchitecture / Windows nodes** → ch18
- **NetworkPolicy** → ch16
- **Operators / reconcile loop** → ch20
- **Pods** → ch02, ch07
- **Multicontainer Pods (sidecar/init/adapter/ambassador)** → ch07
- **PersistentVolumes / PVC / StorageClass** → ch05
- **Prometheus / metrics** → ch14
- **QoS classes (BestEffort/Burstable/Guaranteed)** → ch22, ch12
- **RBAC (Role/ClusterRole/bindings/ServiceAccount)** → ch17
- **Resource requests / limits** → ch12, ch19
- **Rollouts / rollbacks** → ch09, ch10
- **Scaling (load vs HA)** → ch06, ch19
- **Secrets** → ch04
- **securityContext** → ch16
- **Serverless functions (Kubeless/Knative)** → ch21
- **Services** → ch03
- **StatefulSets** → ch08
- **Taints / tolerations** → ch19
- **Volumes (emptyDir/hostPath)** → ch05
- **CI/CD developer workflows** → ch11

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — decision rules, trade-off matrices, kubectl quick-reference

---

## Scope & Limits

This skill covers the book content only (Kubernetes ~1.18–1.20 era APIs as taught by Stoneman; verify current `apiVersion`s against your cluster). For hands-on work in your codebase, combine with project-specific manifests and `kubectl`. For topics beyond the book, check related skills or ask directly.
