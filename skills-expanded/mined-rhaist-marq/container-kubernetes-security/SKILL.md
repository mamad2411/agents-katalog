---
name: container-kubernetes-security
description: "Covers securing container images and Kubernetes clusters: minimal/signed images and trivy scanning, Pod Security Admission, RBAC least privilege, NetworkPolicy, secrets, runtime detection (Falco/Tetragon), managed-K8s shared responsibility, CIS/NSA benchmarks and the Kubernetes support cadence. Use when the user is hardening or reviewing a container platform, EKS/AKS/GKE cluster, Kubernetes RBAC or Pod Security settings, or asks about image signing or runtime detection."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Container & Kubernetes security

Two layers: the **image** (what you ship) and the **cluster** (where it runs). Real cluster compromises are rarely kernel 0-days. They come from an exposed API/kubelet/dashboard, an over-privileged service account, a privileged pod, a leaked kubeconfig or cloud key, or an unpatched add-on.

Related skills: CNAPP/KSPM categories in `load_skill cloud-security`; CI gates, SBOM and cosign in `load_skill devsecops`; responding to one in `load_skill cloud-incident-response`.

## Version currency (an EOL cluster is a finding)

- **Upstream cadence.** About 3 minors a year, each patched for about 14 months (12, then 2 in maintenance mode).
- **As of Nov 2026** the supported minors are **1.37** (26 Aug 2026), **1.36** (Apr 2026) and **1.35** (maintenance mode 28 Dec 2026, EOL 28 Feb 2027). **1.34 went EOL on 27 Oct 2026.** verify: https://kubernetes.io/releases/
- **EKS:** 14 months standard plus 12 months extended support, which is paid and on by default. After 26 months EKS auto-upgrades the control plane only; nodes stay behind. verify: https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html
- **AKS:** 1 year community support plus 1 year LTS on the Premium tier, covering the last two patches only.
- **GKE:** about 14 months, plus about 10 more on the paid Extended channel.
- **Extended support covers the control plane only.** Add-ons (ingress, CNI, operators) reach end of life on their own schedules.
- **ingress-nginx was retired on 24 Mar 2026.** No more releases or security fixes; the repo is archived. Migrate to Gateway API or a maintained controller. It was the controller behind IngressNightmare (CVE-2025-1974, unauthenticated RCE via its admission webhook). verify: https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/

## Images

- **Use minimal bases.** Distroless, Wolfi/Chainguard, or Docker Hardened Images (free under Apache-2.0 since Dec 2025; verify current terms at https://docs.docker.com/dhi/). Build multi-stage, run as a non-root `USER`, and ship no shell or package manager.
- **Pin by digest** (`@sha256:`). Tags are mutable, so `latest` in a manifest is a finding.
- **Scan with trivy** (in your CI; marq does not run it): `trivy image` for a registry ref and `trivy fs` for a build context or manifest directory, covering vuln + secret + misconfig (`DS-*` Dockerfile checks).
  - Re-scan running images on a schedule; new CVEs land on images already deployed.
- **Sign, then verify at admission** (cosign + Kyverno/policy-controller; `load_skill devsecops`). A signature that nothing checks protects nothing.
- **Your scanner is supply chain too.** On 19 Mar 2026 attackers published a malicious Trivy **v0.69.4** binary and images and force-pushed 76 of 77 `trivy-action` tags. Malicious v0.69.5 to v0.69.6 images followed on Docker Hub. Tracked as GHSA-69fq-xp46-6x23 / CVE-2026-33634.
  - Pin CI actions to a commit SHA and scanner images by digest, and verify their signatures. The scanner runs with your CI secrets in reach.
  - Current release is v0.76.2 (5 Nov 2026). Use a release outside the compromised range. verify: https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23

## Admission & pod security

- **Pod Security Admission** replaced PodSecurityPolicy, which was removed in 1.25.
  - Three levels (`privileged` / `baseline` / `restricted`), set per namespace with labels like `pod-security.kubernetes.io/enforce=restricted`.
  - **An unlabeled namespace is effectively privileged.**
- **Roll out in stages:** `warn` + `audit` labels first, fix what fires, then `enforce`.
- **What restricted requires:** `runAsNonRoot`, all capabilities dropped, `allowPrivilegeEscalation: false`, seccomp `RuntimeDefault`, and no hostPath, hostNetwork or hostPID.
- **Custom rules** (registry allowlist, labels, signatures):
  - ValidatingAdmissionPolicy (CEL, GA in 1.30) or MutatingAdmissionPolicy (stable in 1.36).
  - Kyverno or Gatekeeper for more.
- **Pitfalls:**
  - Blanket exemptions for `kube-system` or CI namespaces become the hole.
  - Webhooks with `failurePolicy: Ignore` fail open.
  - Admission webhooks are network services too, so keep them off the pod network.

## RBAC least privilege

- **Treat these as cluster-admin:**
  - `*` on `*`, or the verbs `escalate`, `bind` and `impersonate`.
  - `create pods`: lets the holder run as any service account in the namespace and mount hostPath.
  - `get`/`list secrets`: `list` returns the values.
  - `pods/exec`, `nodes/proxy`, `serviceaccounts/token`.
  - Writing webhook configurations or approving CSRs.
- **Binding hygiene:** bind roles to IdP groups, not individual users. Never bind to `system:anonymous`, `system:unauthenticated` or `system:authenticated`.
- **Service accounts:** default `automountServiceAccountToken: false`, one SA per workload, and projected time-bound tokens. Long-lived token Secrets are a legacy smell.
- **Map cloud identity on purpose.**
  - EKS: use **access entries**; the `aws-auth` ConfigMap is deprecated.
  - Pods get their own identity (EKS Pod Identity/IRSA, Entra Workload ID, GKE Workload Identity), not the node role.
  - Block pod access to IMDS (IMDSv2 with hop limit 1, or an egress policy), or every pod inherits the node's cloud role.

## Network policy

- **Pod networking is flat and allow-all by default.** A NetworkPolicy object is only enforced if the CNI enforces it (Calico, Cilium and similar).
- **Default-deny per namespace,** for both ingress and egress. Then allow DNS and each app's real flows.
- **Deny egress to metadata and the API server.** Block `169.254.169.254`, and the API server for workloads that don't need it.
- **Never internet-facing:** the kubelet (10250), etcd (2379-2380), controller-manager/scheduler (10257/10259) and dashboards. Keep the API endpoint private or behind authorized networks. verify: https://kubernetes.io/docs/reference/networking/ports-and-protocols/

## Secrets

- **Secrets are only base64-encoded.** Enable **encryption at rest with KMS v2** (GA in 1.29), and check each managed provider's default.
- **Prefer an external store** (Vault or a cloud secret manager), synced in via External Secrets Operator or the Secrets Store CSI driver. Restrict `get`/`list secrets` with RBAC.
- **Keep secrets out of image layers, Helm values and env vars.** They leak into logs, crash dumps and `docker history`. Scan for them with gitleaks, trufflehog and trivy.

## Runtime detection & audit

- **Sensors:**
  - **Falco** (CNCF graduated): syscall/eBPF rules plus a K8s audit plugin.
  - **Tetragon** (a Cilium project): eBPF observability that can also enforce in-kernel, e.g. kill a process.
- **High-signal detections:**
  - A shell in a container, or an exec into a pod.
  - Writes to binary directories.
  - A pod reading its SA token, then calling the API.
  - New egress destinations; miner patterns.
- **The K8s audit log is off by default.**
  - Self-managed clusters need an audit policy file. EKS needs control-plane logging turned on; AKS needs a diagnostic setting.
  - Enable it before you need it and ship it to the SIEM (`load_skill detection-engineering`).

## Managed-K8s shared responsibility

- **The provider owns** the control-plane components (API server, etcd, scheduler): their patching, availability and etcd encryption.
- **You own:**
  - When upgrades happen.
  - Node images, unless you run GKE Autopilot, EKS Auto Mode or Fargate.
  - Add-ons, RBAC, admission, NetworkPolicy and secrets.
  - Workload identity and audit-log export.
  - API-endpoint exposure. It is often public by default, so restrict it.

## Benchmarks

- **CIS Kubernetes Benchmark v2.1.0** (late Sep 2026) covers about 1.35 to 1.37; v2.0.x covers 1.34 to 1.35.
  - On managed clusters use the CIS EKS/AKS/GKE benchmarks; many self-managed checks don't apply.
  - Tooling: kube-bench or `trivy k8s --compliance`.
  - verify: https://www.cisecurity.org/benchmark/kubernetes
- **NSA/CISA Kubernetes Hardening Guidance v1.2** (Aug 2022) is still the latest edition found.
  - Good for the reasoning, but it predates ValidatingAdmissionPolicy/MutatingAdmissionPolicy, KMS v2 and the ingress-nginx retirement. Take the current control list from CIS.
  - verify: https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF

## Rules

- Fix exposure and identity first (API endpoint, kubelet, RBAC, IMDS), then pod hardening, then runtime detection.
- Enforce Pod Security Admission per namespace; unlabeled means privileged.
- Default-deny NetworkPolicy, on a CNI that actually enforces it.
- Stay on a supported minor, and track add-on end of life separately.
- Pin by digest and verify signatures, including for your own security tooling.
