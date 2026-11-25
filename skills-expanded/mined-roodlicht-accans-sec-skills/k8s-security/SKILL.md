---
name: k8s-security
description: Kubernetes security review — RBAC discipline, Pod Security Standards (baseline/restricted), NetworkPolicy default-deny, admission controllers (Kyverno/Gatekeeper/VAP), External Secrets Operator, and runtime monitoring via Falco and audit logs.
---

# Kubernetes Security

## When to use

This skill covers the cluster and workload layer on top of `container-hardening`. Image content and build live there; what K8s does with those images (scheduling, RBAC, networking, secrets, runtime policy) lives here.

Activates on:

- A request like "review our K8s manifests", "our RBAC is sprawling", "turn on Pod Security Standards", "write a NetworkPolicy", "which admission controller should we use", "cosign verification in the cluster".
- New or modified manifests: `Deployment`, `StatefulSet`, `DaemonSet`, `Job`, `ServiceAccount`, `Role(Binding)`, `ClusterRole(Binding)`, `NetworkPolicy`, `ValidatingAdmissionPolicy`, Helm charts, Kustomize overlays.
- A cluster audit driven by compliance (CIS Kubernetes Benchmark, NSA/CISA guide, PCI-DSS cloud scope).
- A handoff from `security-review` when K8s is in scope.
- An incident where lateral movement in a cluster is suspected (see `ir-runbook` for response).

### When NOT to use (handoff)

- Container image content (base image, USER, caps) → `container-hardening`. This skill takes the image as given.
- Cluster-provisioning IaC (EKS/GKE/AKS module, node groups, VPC) → `iac-security`. Manifest level here, infrastructure level there.
- CI pipeline that applies manifests → `cicd-hardening`. GitOps controllers (Argo CD, Flux) we mention only as context here.
- Secret backend (Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault) → `secrets-scanner`. External Secrets Operator bridges both.
- Per-CVE on K8s components or sidecars → `cve-triage`.
- Service-mesh config (Istio AuthorizationPolicy, mTLS, Linkerd) sits partly in scope (auth/runtime), partly out (traffic management is ops).
- Pentest against a cluster → `recon-agent` + `web-exploit-triage`.

## Approach

Six phases. Phases 1–3 form the cluster baseline, phase 4 bridges to external secrets, phase 5 covers runtime.

### 1. Cluster baseline: RBAC, Pod Security Standards, admission

The three controls that should be in place from day one in a new cluster.

**RBAC discipline**:

- **Default deny for service accounts.** `automountServiceAccountToken: false` on the namespace-default service account and on every Pod that doesn't need API access. The default SA mounted into every pod is the most-abused attack trampoline.
- **Least-privilege roles.** Wildcards (`verbs: ["*"]`, `resources: ["*"]`) are red flags. Split read and write, scope to specific resources, prefer `Role` (namespace-scoped) over `ClusterRole` where possible.
- **No cluster-admin for applications.** The `cluster-admin` ClusterRole is for human operators only, and even then preferably via just-in-time escalation.
- **Kyverno/Gatekeeper policy that blocks high-risk RBAC**: no wildcards in prod namespaces, no bindings to `system:anonymous`, no escalation to `cluster-admin`.
- **Audit what permissions exist**: `kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa>`. Or tools like `rbac-lookup`, `krane`, `permission-manager`.

**Pod Security Standards (PSS)** have replaced PodSecurityPolicy since Kubernetes 1.25. Three levels, enforced per namespace via labels:

- **privileged** — anything goes. Only for system workloads that need it.
- **baseline** — prevents known privilege-escalation (no hostNetwork, no privileged containers, restricted hostPath, no Linux capabilities beyond defaults).
- **restricted** — harden-by-default: runAsNonRoot, readOnlyRootFilesystem, seccomp RuntimeDefault, all caps dropped plus NET_BIND_SERVICE-style explicit adds, no privilege escalation, restricted volume types.

Labels per namespace:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: payments
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: v1.29
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

`enforce` blocks, `audit` logs, `warn` warns at `kubectl apply`. Start with `warn` + `audit`, migrate to `enforce` once findings are cleaned up.

**Admission controllers** for rules PSS doesn't cover:

- **Kyverno** — YAML policies, no-code, stronger on mutation (e.g. auto-injecting `readOnlyRootFilesystem: true`). Default choice for teams without Rego experience.
- **OPA Gatekeeper** — Rego policies, deeper logic possible, same engine as `iac-security` phase 4. Default if you already use OPA.
- **ValidatingAdmissionPolicy (VAP)** — built-in in Kubernetes 1.30+, CEL expressions instead of Rego. No external controller needed, lighter than Gatekeeper, less feature-rich. Use for simple policies.

One of these is enough. All three together is maintenance burden without added value.

### 2. Workload hardening: securityContext in the Pod spec

This is the bridge between `container-hardening` (what's in the image) and what K8s actually does with it. Every Deployment/StatefulSet/Job needs this block:

```yaml
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: app
          image: <registry>/<image>@sha256:<digest>
          imagePullPolicy: IfNotPresent
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
              # only add what's strictly needed:
              # add: ["NET_BIND_SERVICE"]
          resources:
            limits:
              cpu: "500m"
              memory: "512Mi"
            requests:
              cpu: "100m"
              memory: "128Mi"
```

Per field, briefly:

- **runAsNonRoot + runAsUser** — backup when the image has no USER directive. Explicitly set a non-root UID.
- **readOnlyRootFilesystem** — writable paths via `emptyDir` or persistent-volume mounts; the rest is read-only. Malware persistence inside the container becomes harder.
- **seccompProfile RuntimeDefault** — Docker/containerd default seccomp filter on. Required in restricted PSS.
- **capabilities drop ALL** — no Linux caps unless explicitly added.
- **allowPrivilegeEscalation false** — blocks setuid escalation.
- **resource limits** — prevents one pod from exhausting the node (DoS amplification). Limits and requests, not just one.
- **imagePullPolicy** — IfNotPresent with a digest pin; `Always` only with mutable tags (which you don't want in production).

### 3. Network isolation: NetworkPolicy default-deny

Without NetworkPolicy, intra-cluster traffic is wide open. Install default-deny, then allow per Pod/namespace what's needed.

Default-deny per namespace:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: payments
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

Then explicit allow policies:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-web
  namespace: payments
spec:
  podSelector:
    matchLabels: { app: payment-api }
  policyTypes: [Ingress]
  ingress:
    - from:
        - namespaceSelector:
            matchLabels: { role: web }
          podSelector:
            matchLabels: { app: web-frontend }
      ports:
        - protocol: TCP
          port: 8080
```

Egress to the internet: an allowlist of DNS-resolvable hostnames is not possible with vanilla NetworkPolicy (which works on pod/namespace selectors and IP CIDRs). For FQDN egress use a CNI with FQDN support (Cilium, Calico Enterprise) or an egress proxy (Istio egress gateway, Squid).

Cilium and Calico also offer `ClusterwideNetworkPolicy` for policies that hover above namespaces — useful for baseline defaults.

### 4. Secrets: why K8s Secrets aren't enough, and what is

`kind: Secret` is base64, not encryption. Anyone with RBAC access to `secrets.get` in the namespace reads everything. Encrypted-at-rest in etcd is possible if you set `--encryption-provider-config` on the kube-apiserver — but that's opt-in and often skipped.

Three approaches, increasing in maturity:

- **SealedSecrets** (Bitnami). Encrypt the secret offline with a cluster public key, commit the encrypted object in git. Useful for GitOps; one cluster = one key pair.
- **External Secrets Operator (ESO)**. Pull model: ESO syncs external secret stores (Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, Doppler, Infisical) to K8s Secret objects. The object in the Pod is still base64, but the source of truth is outside the cluster. Default in enterprise contexts.
- **Secrets Store CSI Driver**. Mount secrets as files via a CSI volume; no K8s Secret object as an intermediate. Secrets never in etcd. Heavier to set up, cleaner threat model.

For all three: secret rotation remains an external responsibility (see `secrets-scanner` phase 4). K8s ESO only handles sync.

IRSA (IAM Roles for Service Accounts) on EKS, Workload Identity on GKE, Managed Identity on AKS: bind the SA directly to a cloud IAM role, no static API key needed. Default recommendation for cloud workloads.

### 5. Runtime monitoring

What's actually happening in the cluster, and do you notice it in time?

- **Kubernetes audit log**. `--audit-policy-file` on kube-apiserver. At minimum: every RBAC change, every secret read by non-system accounts, every `exec`/`attach` action, every `escalate`/`bind` verb. Stream to a SIEM (see `siem-query` and `log-triage`).
- **Falco** (CNCF OSS). eBPF/kernel-based syscall monitoring with rule sets for anomalies: shell-in-container, `cat /etc/shadow`, `chmod 777` in prod namespaces, network connections to known C2. Default for runtime threat detection in open source.
- **Tetragon** (Cilium) — eBPF-based observability plus enforcement. Comparable to Falco, more kernel-level.
- **KubeArmor** — runtime enforcement with AppArmor/BPF.
- **Service-mesh auth** — Istio `AuthorizationPolicy` or Linkerd policy for mTLS enforcement between services. Doesn't replace NetworkPolicy; complements it at L7.

Alerts from Falco etc. go to `detection-engineer` for rule tuning and `ir-runbook` for response.

### 6. Verification-loop

Layer 1: scope (every namespace has a PSS label? every Pod has a securityContext? every namespace has a default-deny NetworkPolicy?), assumptions ("we use Workload Identity" only when you've actually seen the SA annotations), gaps (audit log enabled, Falco alerts routed, runtime monitoring also covers kube-system), consistency (PSS level matches actual securityContext settings).

Layer 2: K8s API versions and field names correct (PSS syntax changed at 1.25, VAP is 1.30+), CVE references for K8s components verified against NVD, no fabricated Kyverno policy snippets that don't run against real CRDs.

## Output

```
K8s security review — <cluster/namespace/app>
Scope: <manifests, Helm charts, namespaces>

Cluster baseline:
  RBAC:             <audit findings, wildcards, over-permissive>
  PSS per namespace:<table: namespace → enforce/audit/warn>
  Admission:        <Kyverno | Gatekeeper | VAP | none>

Workload hardening:
  Pods without securityContext: <N>
  runAsNonRoot false:           <N>
  readOnlyRootFilesystem false: <N>
  capabilities not dropped:     <N>
  No resource limits:           <N>

Network:
  Namespaces without default-deny: <list>
  Egress policies present:         <yes/no per namespace>
  FQDN egress via:                 <CNI | proxy | none>

Secrets:
  Native K8s Secrets in use: <N, source-of-truth or ESO-synced?>
  Encryption at rest etcd:   <on/off>
  Workload Identity:         <yes/no per service>

Runtime:
  Audit log on:    <yes/no>
  Falco/Tetragon:  <deployed, alerts routed>
  Service mesh:    <Istio/Linkerd/none, mTLS scope>

Findings (severity-sorted)

Verification-loop: ...
```

Per finding: location (manifest or resource), CIS-benchmark ID where relevant, CWE-ID where applicable, severity, fix (YAML snippet rather than prose).

## References

- Kubernetes Pod Security Standards — [https://kubernetes.io/docs/concepts/security/pod-security-standards/](https://kubernetes.io/docs/concepts/security/pod-security-standards/). Official definition of privileged/baseline/restricted.
- Kubernetes RBAC — [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/).
- Kubernetes NetworkPolicy — [https://kubernetes.io/docs/concepts/services-networking/network-policies/](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
- ValidatingAdmissionPolicy — [https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/). Built-in alternative to OPA/Kyverno from 1.30.
- CIS Kubernetes Benchmark — [https://www.cisecurity.org/benchmark/kubernetes](https://www.cisecurity.org/benchmark/kubernetes). Audit checklist.
- NSA/CISA Kubernetes Hardening Guide — [https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF). Semi-governmental baseline.
- OWASP Kubernetes Top 10 — [https://owasp.org/www-project-kubernetes-top-ten/](https://owasp.org/www-project-kubernetes-top-ten/).
- NIST SP 800-204B — [https://csrc.nist.gov/pubs/sp/800/204/b/final](https://csrc.nist.gov/pubs/sp/800/204/b/final). Microservices + service-mesh security.
- Kyverno — [https://kyverno.io/](https://kyverno.io/). YAML policy engine.
- OPA Gatekeeper — [https://open-policy-agent.github.io/gatekeeper/website/](https://open-policy-agent.github.io/gatekeeper/website/).
- External Secrets Operator — [https://external-secrets.io/](https://external-secrets.io/).
- Secrets Store CSI Driver — [https://secrets-store-csi-driver.sigs.k8s.io/](https://secrets-store-csi-driver.sigs.k8s.io/).
- Falco — [https://falco.org/](https://falco.org/). Runtime threat detection.
- Cilium — [https://docs.cilium.io/](https://docs.cilium.io/). CNI with FQDN egress and Tetragon integration.

## Categories

- appsec
