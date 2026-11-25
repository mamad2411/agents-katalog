---
name: the-kubernetes-book
description: "Knowledge base from \"The Kubernetes Book (2024)\" by Nigel Poulton. Use when applying Poulton's frameworks for Kubernetes Pods, Deployments, Services, Ingress, storage (PV/PVC/StorageClass), ConfigMaps/Secrets, StatefulSets, RBAC, the API/CRDs, and security (STRIDE, defense-in-depth) — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# The Kubernetes Book (2024)
**Author**: Nigel Poulton | **Pages**: ~308 | **Chapters**: 17 | **Generated**: 2026-06-19

## How to Use This Skill

- **Without arguments** — load core frameworks below for reference
- **With a topic** — ask about `services`, `rbac`, `storage`, `rolling updates`; I find and read the relevant chapter
- **With chapter** — ask for `ch06`; I load that specific chapter file
- **Browse** — ask "what chapters do you have?" for the full index

When you ask about a topic not in Core Frameworks below, I read the relevant
chapter file (and `glossary.md` / `patterns.md` / `cheatsheet.md`) before answering.

---

## Core Frameworks & Mental Models

**Kubernetes in one sentence** — *An orchestrator of containerized, cloud-native microservices apps.* It deploys apps, scales them on demand, self-heals them, and does zero-downtime rolling updates/rollbacks. Think of it as **the operating system of the cloud**: as Linux/Windows abstract a server's CPU/RAM/disk, Kubernetes abstracts a cloud/datacenter's nodes, networks, and volumes. (Ch1)

**The declarative model + desired state (the most important idea in the book)** — You describe *what you want* in a YAML manifest (desired state); you POST it to the API server; a **controller** runs a reconciliation loop that constantly compares *observed state* to *desired state* and makes them match. This single loop is the engine behind scaling, self-healing, and rollouts. Prefer declarative (`kubectl apply -f`) over imperative commands — manifests are versionable, repeatable, and self-documenting. (Ch2)

**Cluster anatomy** — *Control plane* nodes run the brains: **API server** (the only door in, RESTful front-end to the cluster), **cluster store** (etcd, the single source of truth), **controllers/controller manager** (reconciliation loops), **scheduler** (assigns Pods to nodes), **cloud controller manager**. *Worker nodes* run: **kubelet** (node agent), **container runtime** (containerd via CRI), **kube-proxy** (Service networking). (Ch2)

**Object nesting** — Bigger objects wrap smaller ones: **Deployment → ReplicaSet → Pod → container**. You manage the top object; Kubernetes manages the rest. (Ch2, Ch6)

**The Pod** — Smallest deployable unit and the atomic unit of scaling. A Pod is a shared execution environment (network namespace, IP, volumes) for one or more tightly-coupled containers. Pods are **immutable** — you never modify a running Pod; you replace it. You rarely deploy Pods directly — you wrap them in a controller. Patterns: **init containers** (run-to-completion setup before app containers), **sidecar** (helper container alongside the main one). (Ch4)

**Deployment** — The controller for stateless apps. Provides self-healing, scaling, and **rolling updates + rollbacks**. Update = edit the manifest's image tag and re-apply; the Deployment incrementally replaces old-version Pods with new ones (governed by `maxSurge`/`maxUnavailable`). `kubectl rollout undo` reverts to a previous ReplicaSet revision. (Ch6)

**Service** — Stable, durable networking in front of a set of ephemeral Pods. Pods come and go (new IPs each time); a Service gives a **stable name, IP, and port**, and load-balances to healthy Pods selected by **label selector** (loose coupling). Types: **ClusterIP** (in-cluster only), **NodePort** (external via node port), **LoadBalancer** (cloud LB). (Ch7)

**Ingress** — L7 HTTP/HTTPS router that exposes many Services through a single external IP using **host-based and path-based routing**. Needs two constructs: an **Ingress controller** (runs the proxy) + **Ingress** objects (the rules). Consolidates what would otherwise be many LoadBalancer Services. (Ch8)

**Service discovery** — Two halves: **registration** (every Service auto-registers a name→ClusterIP mapping in cluster DNS / **CoreDNS**) and **resolution** (Pods resolve Service names via DNS). FQDN form: `<service>.<namespace>.svc.cluster.local`. (Ch10)

**The storage trinity** — **PersistentVolume (PV)** = a piece of storage; **PersistentVolumeClaim (PVC)** = an app's request for storage; **StorageClass (SC)** = a template enabling **dynamic provisioning** (auto-create a PV to satisfy a PVC). The **CSI** (Container Storage Interface) makes storage backends pluggable. Access modes: RWO / ROX / RWX. (Ch11)

**ConfigMaps & Secrets** — Decouple configuration from the container image (same image runs in dev/test/prod). Inject three ways: **environment variables**, **container args**, or **volume mount** (volume = best for files and live updates). **Secrets are base64-encoded, NOT encrypted** — treat them as obfuscated, secure them with RBAC/encryption-at-rest. (Ch12)

**StatefulSet** — Controller for stateful apps needing **sticky identity**: stable predictable Pod names (ordinal `-0`, `-1`, `-2`), ordered startup/scaling/deletion, a **headless Service** for stable DNS, and per-Pod persistent storage via **`volumeClaimTemplates`**. Use over Deployment only when identity/order/per-Pod state matters. (Ch13)

**API security pipeline & RBAC** — Every request flows **AuthN → AuthZ → Admission control**. **RBAC** answers authorization: **Role/ClusterRole** define *what* (verbs on resources); **RoleBinding/ClusterRoleBinding** bind them to *who* (users, groups, **ServiceAccounts**). Apply **least privilege** — no wildcards, no cluster-admin by default. (Ch14)

**The API & CRDs** — Everything is an object exposed by one RESTful API. Resources live in **API groups** with **versioning** (alpha → beta → stable/GA). Extend Kubernetes with **Custom Resource Definitions (CRDs)** — your own object types served by the same API. (Ch15)

**Security: STRIDE + defense-in-depth** — Threat-model with **STRIDE** (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege). Defend in layers across the lifecycle: **build** (signed/scanned images, SBOM), **deploy** (RBAC, Pod Security Standards/admission, policy engines), **runtime** (NetworkPolicy isolation, runtime monitoring, secrets management). (Ch16, Ch17)

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-kubernetes-primer.md) | Kubernetes primer | orchestration, cloud-native, OS-of-the-cloud, CRI/containerd, CNCF |
| [ch02](chapters/ch02-principles-of-operation.md) | Principles of operation | declarative model, desired state, control plane/worker, object nesting |
| [ch03](chapters/ch03-getting-kubernetes.md) | Getting Kubernetes | Docker Desktop, GKE, kubectl, kubeconfig/contexts |
| [ch04](chapters/ch04-working-with-pods.md) | Working with Pods | Pod abstraction, init containers, sidecar, restart policy, lifecycle |
| [ch05](chapters/ch05-namespaces.md) | Virtual clusters with Namespaces | virtual cluster, soft isolation, resource quotas, namespaced vs cluster-scoped |
| [ch06](chapters/ch06-deployments.md) | Kubernetes Deployments | Deployment→ReplicaSet→Pod, rolling update, rollback, maxSurge/maxUnavailable |
| [ch07](chapters/ch07-services.md) | Kubernetes Services | ClusterIP/NodePort/LoadBalancer, label selector, EndpointSlices |
| [ch08](chapters/ch08-ingress.md) | Ingress | Ingress controller, IngressClass, host/path routing, TLS |
| [ch09](chapters/ch09-webassembly.md) | WebAssembly on Kubernetes | Wasm, WASI, runwasi/containerd shim, RuntimeClass, Spin |
| [ch10](chapters/ch10-service-discovery.md) | Service discovery deep dive | registration vs resolution, CoreDNS, FQDN, ndots |
| [ch11](chapters/ch11-storage.md) | Kubernetes storage | PV, PVC, StorageClass, CSI, dynamic provisioning, access modes |
| [ch12](chapters/ch12-configmaps-secrets.md) | ConfigMaps and Secrets | config decoupling, env/args/volume injection, base64≠encryption |
| [ch13](chapters/ch13-statefulsets.md) | StatefulSets | sticky identity, ordinals, headless Service, volumeClaimTemplates |
| [ch14](chapters/ch14-api-security-rbac.md) | API security and RBAC | AuthN→AuthZ→Admission, Role/RoleBinding, ServiceAccount, least privilege |
| [ch15](chapters/ch15-kubernetes-api.md) | The Kubernetes API | RESTful API, API groups, versioning, CRDs, api-resources |
| [ch16](chapters/ch16-threat-modeling.md) | Threat modeling Kubernetes | STRIDE, attack surface, per-category mitigations |
| [ch17](chapters/ch17-real-world-security.md) | Real-world Kubernetes security | supply chain, defense-in-depth, Pod Security, NetworkPolicy |

## Topic Index

- **Admission control** → ch14, ch16, ch17
- **API groups / versioning** → ch15
- **API server** → ch02, ch15
- **ClusterIP / NodePort / LoadBalancer** → ch07
- **CoreDNS / DNS** → ch10
- **CRD / extending the API** → ch15
- **CRI / containerd** → ch01
- **ConfigMaps** → ch12
- **Control plane / etcd / scheduler** → ch02
- **Declarative model / desired state** → ch02, ch06
- **Deployments** → ch06
- **Ingress** → ch08
- **Init containers / sidecar** → ch04
- **kubectl / kubeconfig / contexts** → ch03
- **Labels / selectors** → ch06, ch07
- **Least privilege** → ch14, ch17
- **Namespaces** → ch05
- **NetworkPolicy** → ch17
- **Pods / lifecycle / restart policy** → ch04
- **PV / PVC / StorageClass / CSI** → ch11
- **RBAC (Role / RoleBinding / ServiceAccount)** → ch14
- **Rolling updates / rollback** → ch06
- **Secrets** → ch12
- **Service discovery** → ch10
- **Services** → ch07
- **StatefulSets / volumeClaimTemplates** → ch13
- **STRIDE / threat modeling** → ch16
- **Supply chain / image signing / scanning** → ch17
- **WebAssembly / Wasm / RuntimeClass** → ch09

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — decision rules, trade-off matrices, kubectl quick-reference

---

## Scope & Limits

Covers The Kubernetes Book (2024) content only — Kubernetes ~v1.29 era. For hands-on
work in your cluster, combine with live `kubectl`, the official docs, and your platform's
specifics. For a complementary task-oriented treatment, see the `kubernetes-month-of-lunches` skill.
