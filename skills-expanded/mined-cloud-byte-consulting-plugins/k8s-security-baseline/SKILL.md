---
name: k8s-security-baseline
description: >-
  Run a CIS-derived security audit of a MANAGED Kubernetes cluster (Lambda or
  similar), scoped by shared responsibility: filter out provider-owned control
  plane checks (CIS sections 1-3), execute the customer-side checklist from
  sections 4-5 — RBAC minimization, Pod Security Standards labels,
  default-deny NetworkPolicies, secrets handling, admission control — plus
  GPU-specific risks (privileged device-plugin DaemonSets, NVIDIA container
  toolkit CVEs), and output a findings table with severity and remediation.
  Use whenever the user asks for a security audit, CIS benchmark check,
  hardening review, cluster security posture, RBAC review, "who has
  cluster-admin", pod security policy/admission questions, NetworkPolicy
  coverage, admission controllers, image signing enforcement, kubelet
  hardening, or shared responsibility on managed Kubernetes. For stamping
  secure tenant namespaces use sibling researcher-tenancy-provisioner; for
  enforcing these policies as PR gates use gitops-platform-bootstrap.
---

# K8s Security Baseline (Managed Cluster)

## Purpose
Produce a defensible, evidence-backed security posture for a managed GPU research cluster: every finding tied to a CIS Kubernetes Benchmark (v1.12) check or a GPU-specific risk, every check either executed with a command or explicitly assigned to the provider's side of the line. Output is a findings table the platform team can burn down — not a generic hardening lecture.

## Core model to hold in your head

**Defense in depth**: layered controls across user data → configuration → application code → dependencies → containers → host. On a managed cluster you don't lose layers; you lose *direct access* to some (host, control plane) and gain a contract instead — so the first artifact of any audit is the responsibility split, and the second is the provider's attestation for their side.

**Shared-responsibility filter (CIS section map)**:

| CIS section | Scope | On Lambda managed K8s |
|---|---|---|
| 1. Control plane components (apiserver/scheduler/controller-manager files & flags) | Provider | Out of audit scope — request attestation |
| 2. etcd | Provider | Out of scope — ask: encryption at rest? envelope encryption for Secrets? backup policy? |
| 3. Control plane configuration (auth, audit logs) | Provider (mostly) | Ask: is API audit logging enabled and can the customer access the logs? |
| 4. Worker nodes (kubelet config/files) | **Shared — verify who owns node images** | Spot-check via API even without SSH (below) |
| 5. Policies (RBAC, PSS, NetworkPolicy, secrets, admission) | **Customer — the bulk of this audit** | Full checklist below |

Questions to put to Lambda in writing: CIS/SOC2 posture for sections 1–3; who patches node OS, kubelet, NVIDIA driver, and container toolkit, and on what cadence; audit-log access; etcd/Secrets encryption; whether customer workloads can ever be privileged-blocked at their layer. Provider answers become findings too ("unknown" = a finding).

**CIS profiles**: Level 1 = baseline, low friction — target 100%. Level 2 = defense-in-depth with operational cost — adopt deliberately. Checks are Automated (scorable by command) or Manual (require judgment); both belong in the report.

## Customer-side audit checklist (CIS section 5 + kubelet spot checks)

Run each audit command; a failed check becomes a finding row.

| # | Check (CIS ref) | Audit | Remediation | Sev |
|---|---|---|---|---|
| 1 | cluster-admin only where required (5.1.1) | `kubectl get clusterrolebindings -o=custom-columns=NAME:.metadata.name,ROLE:.roleRef.name,SUBJECT:.subjects[*].name` — review every cluster-admin subject | Rebind to lesser roles, then `kubectl delete clusterrolebinding <name>`; never touch `system:`-prefixed bindings | High |
| 2 | Minimize secrets access (5.1.2) | `kubectl auth can-i get secrets --as=<subject> -A` per principal; review roles granting get/list/watch on secrets | Strip get/list/watch on secrets from non-platform roles | High |
| 3 | No wildcards in Roles (5.1.3) | `kubectl get roles,clusterroles -A -o yaml \| grep -B5 '"\*"'` | Replace `*` with explicit verbs/resources | Med |
| 4 | Minimize pod-create rights (5.1.4) | Enumerate who can create pods (`kubectl auth can-i create pods --as=...`) | Pod creation implies node-level reach; restrict to workload namespaces | Med |
| 5 | Default SAs inactive, tokens unmounted (5.1.5/5.1.6) | `kubectl get sa default -A -o yaml \| grep -c automountServiceAccountToken` — expect per-ns false | Set `automountServiceAccountToken: false` on default SAs and pods that don't call the API | Med |
| 6 | No system:masters use; limit bind/impersonate/escalate (5.1.7/5.1.8) | Review group memberships and role verbs | Reserve for break-glass with audit trail | High |
| 7 | No privileged containers admitted (5.2.2) | `kubectl get pods -A -o jsonpath=$'{range .items[*]}{@.metadata.name}: {@..securityContext}\n{end}' \| grep -i privileged` | PSS enforce label ≥ baseline on all tenant namespaces (below) | High |
| 8 | No hostPID/hostIPC/hostNetwork, no allowPrivilegeEscalation, no root, drop capabilities (5.2.3–5.2.9) | `kubectl get pods -A -o json \| jq '.items[] \| select(.spec.hostPID or .spec.hostIPC or .spec.hostNetwork) \| .metadata.name'`; securityContext review | `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`; restricted PSS where images allow | High |
| 9 | Active policy control mechanism exists (5.2.1, 5.5.1) | List PSA labels + admission controllers: `kubectl get ns -o custom-columns=NAME:.metadata.name,ENFORCE:.metadata.labels.pod-security\.kubernetes\.io/enforce`; check for Gatekeeper/Kyverno deployments | Enforce PSA labels every namespace; OPA Gatekeeper or Kyverno for image provenance (signed images via Cosign) — modern equivalent of ImagePolicyWebhook | High |
| 10 | NetworkPolicies in every namespace (5.3.1/5.3.2) | `kubectl get networkpolicy -A` — every tenant ns needs default-deny plus explicit allows; verify CNI supports NetworkPolicy | Default-deny ingress and egress stamped per tenant, with narrow DNS/object-store/registry/telemetry allows from `researcher-tenancy-provisioner` | High |
| 11 | Secrets as files, external storage considered (5.4.1/5.4.2) | Grep manifests for `secretKeyRef` env usage; inventory secret sprawl | Prefer volume mounts over env vars (env leaks via logs/inspect); Sealed Secrets/ESO strategy per gitops-platform-bootstrap | Med |
| 12 | Namespace boundaries, no default ns, seccomp, securityContext (5.6.1–5.6.4) | `kubectl get all -n default` — expect empty; check `seccompProfile: RuntimeDefault` in pod specs | Tenancy bundles; `kubectl label ns <ns> pod-security.kubernetes.io/enforce=baseline` | Med |
| 13 | Kubelet spot checks (4.2.1/4.2.2/4.2.4) — even without node SSH | `kubectl get --raw /api/v1/nodes/<node>/proxy/configz \| jq` — verify `authentication.anonymous.enabled: false`, `authorization.mode` ≠ AlwaysAllow, `readOnlyPort: 0` | If provider-managed and non-compliant → escalate to Lambda with the evidence | High |
| 14 | RBAC self-check tooling | `kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa>` per workload SA | Trim to least privilege | Med |

PSS rollout without breakage: label `warn`/`audit` first, watch violations for a week, then flip `enforce`. Three levels: privileged / baseline / restricted.

## GPU-specific risks (not in CIS — audit them anyway)

| Risk | Why it matters | Check / control |
|---|---|---|
| Privileged NVIDIA DaemonSets | Device plugin, GPU Operator, DCGM-Exporter run privileged with hostPath device access — by design. They are the exception that must not become the rule | Confine to dedicated namespaces (`gpu-operator`, `nvidia-device-plugin`) labeled PSS `privileged`, while all tenant namespaces enforce baseline/restricted. Alert on any *other* namespace admitting privileged pods |
| NVIDIA Container Toolkit CVEs | Container-escape class bugs (e.g., CVE-2024-0132 TOCTOU in the toolkit) let a malicious image reach the host from a GPU container — catastrophic on multi-tenant research nodes | Inventory toolkit/driver versions (`kubectl get nodes -o custom-columns=NAME:.metadata.name,DRIVER:.metadata.labels.nvidia\.com/cuda\.driver\.major` when GPU feature discovery labels exist); confirm in writing who patches (Lambda node image vs customer GPU Operator) and the SLA; subscribe to NVIDIA security bulletins |
| Untrusted images on shared GPU nodes | Researchers pull arbitrary community ML images; sharing (time-slicing/MPS) has no fault isolation between co-tenants | Image scanning (Trivy) in CI; require signed images (Cosign + Gatekeeper/Kyverno verify) for shared pools; strict-isolation tenants → MIG or whole GPU (gpu-sharing-advisor) |
| hostPath dataset mounts | Researchers mount node paths for speed; breaks container isolation | PSS baseline blocks hostPath (5.2.11); provide PVC/object-store paths instead |
| Notebook servers as attack surface | JupyterHub pods execute arbitrary user code by definition | Non-root singleuser images, restricted PSS where feasible, default-deny egress with explicit allows, per-user namespaces with quota (researcher-tenancy-provisioner) |
| Runtime detection gap | Long-lived GPU nodes running third-party code | Falco (or equivalent eBPF-based) DaemonSet watching shell-in-container, /etc/passwd writes, SA-token misuse — Level 2 control |

## Output specification

Findings table, most severe first:

| ID | Finding (CIS ref / GPU-risk) | Severity | Evidence (command + output excerpt) | Remediation | Owner (customer / Lambda) | Due |
|---|---|---|---|---|---|---|

Plus: responsibility-split summary with provider answers received/outstanding; score (checks passed / applicable, Level 1 and Level 2 separately, sections 1–3 marked N/A-provider — never scored as passes); and a top-5 burn-down list. Codify recurring checks as CI policy gates and admission policies via gitops-platform-bootstrap so the audit converges to continuously-enforced instead of annual.

## Workflow
1. Establish the split: send the provider question list; mark sections 1–3 (and section 4 items on provider-managed node images) accordingly.
2. Run the section-5 checklist top to bottom; capture command output as evidence per row.
3. Run the GPU-risk table; version-inventory the NVIDIA stack.
4. Grade findings (High = exploitable path to cross-tenant or node compromise; Med = weakens a layer; Low = hygiene).
5. Deliver the findings table; convert accepted remediations into Git PRs (policies, PSS labels, netpol) rather than ad hoc kubectl.
6. Re-run quarterly or on provider/platform version changes; diff against the last table.

## Guardrails
- Never delete or modify `system:`-prefixed RBAC bindings; cluster components need them.
- Never flip PSS `enforce` cluster-wide in one step — warn/audit first or you'll evict the GPU operator itself.
- The GPU stack legitimately needs privilege; the control is *containment* (dedicated privileged namespaces), not denial — an audit that flags the device plugin as "critical: privileged pod" without that nuance destroys credibility.
- Default-deny NetworkPolicies without allow rules for DNS, ingress controller, and Prometheus scrape break everything — ship deny + allows as one change.
- Provider-owned check ≠ ignorable check: unanswered attestation requests stay open findings.
- Evidence or it didn't happen: every scored row carries the command and output, in line with the benchmark's audit/remediation pairing.

## Suggested effort
Standard audit: 1–2 days (checklist + GPU risks + report). Provider Q&A adds calendar time — send the questions on day one. Continuous enforcement conversion: +1–2 days with gitops-platform-bootstrap.
