---
name: kubernetes-security-hardening
description: >-
  AKS and Kubernetes security hardening checklist. Covers cluster identity,
  workload identity, pod security, network policies, image security, secrets
  management, and runtime protection.
when-to-use: >-
  Invoke when hardening an AKS cluster, reviewing Kubernetes security posture,
  implementing pod security policies, configuring network policies, or
  setting up container image scanning.
categories:
  - security
  - kubernetes
  - aks
  - containers
---

# Kubernetes Security Hardening

Kubernetes is insecure by default. Every security control must be explicitly configured.

## Security Layers

```
Cluster Access Control
├─ Private API server (no public endpoint)
├─ Entra ID integration for kubectl access
└─ Kubernetes RBAC (namespace-scoped roles)

Workload Identity
├─ Workload identity federation (OIDC, no secrets)
├─ Key Vault CSI driver for secrets
└─ No secrets in ConfigMaps or env vars

Pod Security
├─ Pod security admission (restricted mode)
├─ Azure Policy / Gatekeeper enforcement
├─ No privileged containers, no host networking
└─ Read-only root filesystem where possible

Network Security
├─ Network policies (deny-all default)
├─ CNI choice determines policy engine
└─ Private endpoints for all backing services

Image Security
├─ Private ACR (no public registry pulls)
├─ Image scanning in CI/CD pipeline
├─ Image integrity verification (Notary v2 / Ratify)
└─ Defender for Containers runtime protection
```

---

## Cluster Access Control

### Private Cluster

- [ ] API server not publicly accessible
- [ ] Access via VPN, ExpressRoute, or private endpoint
- [ ] Authorized IP ranges as fallback if private cluster not possible

### Authentication

- [ ] Entra ID integration enabled (AKS-managed Entra ID)
- [ ] kubectl access through `az aks get-credentials` with Entra auth
- [ ] No local admin accounts — disable `--disable-local-accounts`
- [ ] Break-glass procedure documented for emergency access

### RBAC

- [ ] Kubernetes RBAC enabled (default on AKS)
- [ ] Azure RBAC for Kubernetes authorization (optional — maps Azure roles to K8s)
- [ ] Namespace-scoped roles — no cluster-admin for application teams
- [ ] Review ClusterRoleBindings — minimize cluster-wide permissions

---

## Workload Identity

### Configuration

- [ ] **Workload identity enabled** on AKS cluster
- [ ] OIDC issuer enabled
- [ ] Kubernetes service account annotated with Azure client ID
- [ ] Federated identity credential configured in Entra ID
- [ ] **No AAD Pod Identity** — deprecated, less secure, replace with workload identity

### Secrets Management

- [ ] **Key Vault CSI driver** installed and configured
- [ ] Secrets mounted as volumes, not environment variables
- [ ] Auto-rotation enabled (poll interval configured)
- [ ] No secrets in Kubernetes Secrets objects (they're base64 encoded, not encrypted)
- [ ] No secrets in ConfigMaps

---

## Pod Security

### Pod Security Admission

Enforce pod security standards at the namespace level:

| Profile | What It Allows |
|---|---|
| **Privileged** | Unrestricted — only for system namespaces |
| **Baseline** | Minimally restrictive — prevents known privilege escalations |
| **Restricted** | Heavily restricted — best practice for application pods |

- [ ] `restricted` profile enforced on all application namespaces
- [ ] `baseline` on infrastructure namespaces
- [ ] `privileged` only on `kube-system` if required

### Azure Policy / Gatekeeper

- [ ] No privileged containers (`allowPrivilegeEscalation: false`)
- [ ] No host network, host PID, or host IPC
- [ ] Required resource limits on all pods
- [ ] Required labels (team, app, environment)
- [ ] Approved container registries only (deny images from non-ACR sources)
- [ ] Read-only root filesystem where application supports it

---

## Network Policies

### Default Deny

Apply deny-all ingress and egress as baseline, then add specific allows:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: app-namespace
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### Policy Engine Selection

| Engine | Requires | Features |
|---|---|---|
| Calico | Azure CNI or kubenet (Linux) | Mature, deny-all, global policies |
| Cilium | Azure CNI with Cilium | eBPF, L7 policies, observability |
| Azure Network Policy | Azure CNI | Simpler, less feature-rich |

- [ ] Network policies deployed in every application namespace
- [ ] Default deny-all with explicit allow rules
- [ ] Pod-to-pod communication restricted to required paths only
- [ ] Egress restricted — pods cannot reach arbitrary internet endpoints

---

## Image Security

### Supply Chain

- [ ] **Private ACR only** — no pulls from Docker Hub or public registries in production
- [ ] Import approved base images to ACR
- [ ] Image scanning in CI/CD pipeline (Trivy, Defender for Containers)
- [ ] Block deployment of images with Critical/High CVEs
- [ ] Image integrity verification with Notary v2 or Ratify

### Runtime Protection

- [ ] **Microsoft Defender for Containers** enabled
- [ ] Runtime threat detection active
- [ ] Vulnerability scanning for running images
- [ ] Binary drift detection — alert when container content changes at runtime
- [ ] Admission control — block non-compliant images at deploy time

---

## Node Security

- [ ] Separate system and user node pools
- [ ] System pool tainted: `CriticalAddonsOnly=true:NoSchedule`
- [ ] Ephemeral OS disks for AKS nodes (no persistent OS state)
- [ ] Automatic node image upgrades enabled (SecurityPatch or NodeImage channel)
- [ ] Maintenance windows configured for off-hours
- [ ] Node pool autoscaling configured with appropriate bounds
- [ ] GPU/spot nodes tainted to prevent unintended scheduling

---

## Upgrade Security

- [ ] AKS on Stable or Rapid upgrade channel (not None)
- [ ] Node image auto-upgrade enabled
- [ ] Pod Disruption Budgets on all production deployments
- [ ] Blue-green node pool strategy for major version upgrades
- [ ] Surge upgrade configured (`max-surge` for speed vs cost tradeoff)

---

## Monitoring

| Tool | Purpose |
|---|---|
| Container Insights | Node/pod metrics, logs, live data |
| Managed Prometheus + Grafana | Metrics dashboards, alerting |
| Defender for Containers | Runtime threats, vulnerability scanning |
| Network Observability (Hubble/Retina) | Pod-level network flow visibility |

- [ ] Alerts on pod restarts, OOM kills, resource pressure
- [ ] Alerts on failed image pulls (may indicate registry access issues)
- [ ] Log Analytics for container logs with appropriate retention

## Related Skills

- `security-review-framework` — Full security review checklist
- `network-security-design` — Private endpoints and network hardening
- `secrets-management-audit` — Key Vault and secrets patterns
