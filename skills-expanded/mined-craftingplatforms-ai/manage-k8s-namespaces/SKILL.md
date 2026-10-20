---
name: manage-k8s-namespaces
description: >
  Provision and sync Kubernetes tenant namespaces — ResourceQuota, LimitRange, NetworkPolicy
  (default-deny), and coordinate labels — from a compute-design.md and tenant.yaml definitions.
  Uses the Kubernetes MCP server. Use when onboarding a new tenant, applying quota changes,
  or enforcing namespace guardrails after running design-compute.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Manage Kubernetes Namespaces

## Skill Type

Implementation

## System Requirements

- **Kubernetes MCP server** configured and authenticated. The agent will use Kubernetes MCP tools to call the Kubernetes API (`v1`, `networking.k8s.io`).
- The executing identity must have:
  - `v1/namespaces`: create, update, get, list
  - `v1/resourcequotas`: create, update, delete, get, list
  - `v1/limitranges`: create, update, delete, get, list
  - `networking.k8s.io/networkpolicies`: create, update, delete, get, list
- The target cluster must already be provisioned and accessible.
- RBAC for the namespace (RoleBindings) is handled by `manage-k8s-iam`, not this skill.

## Your Goal

Provision and maintain tenant namespaces in a Kubernetes cluster — each pre-configured with the platform guardrails required by the compute design. Ensure that:

1. Every declared tenant has a namespace in the cluster.
2. Each namespace has a ResourceQuota matching the tenant's declared quota template.
3. Each namespace has a LimitRange injecting default CPU/memory requests and limits.
4. Each namespace has a default-deny NetworkPolicy for both ingress and egress.
5. Each namespace carries the mandatory coordinate labels.

This skill does **not** manage RBAC (RoleBindings) — use `manage-k8s-iam` for that.

This skill is **idempotent**.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Compute design**: Path to `compute-design.md`. Read it to get the quota templates and LimitRange defaults.
- **Tenant definitions**: Path(s) to `tenants/{name}.yaml`. One namespace is created per tenant per cluster.
- **Target cluster context**: Which cluster (kubeconfig context) is in scope?
- **Namespace naming**: How are namespaces named? (e.g., `{tenant}` if the cluster is already tier-scoped, or `{tenant}-{tier}` if multi-tier.) Derive from the naming convention.
- **Quota template assignment**: Which quota template does each tenant use? (xsmall, small, medium, large, xlarge.) If not specified in the tenant definition, ask.
- **Scope of this run**: All tenants, specific tenants, or quota changes only?
- **Dry-run mode**: Recommended when applying quota reductions.

Read all input documents before proceeding.

## Process

### Step 1 — Read and Parse Input Documents

Read `compute-design.md` and the relevant `tenants/{name}.yaml` files. Extract:

- Quota template definitions (CPU/memory requests and limits, storage)
- LimitRange defaults (default CPU/memory request and limit per container)
- List of tenants and their assigned quota templates
- Mandatory label schema from the naming convention

Validate:
- Every tenant has a quota template assigned
- All quota template names referenced in tenant files exist in the compute design
- Namespace names conform to Kubernetes constraints (lowercase alphanumeric and hyphens, ≤ 63 characters)

### Step 2 — Reconcile Namespaces

For each tenant:
1. Check whether the namespace exists in the cluster.
2. Create it if missing.
3. Apply mandatory coordinate labels to existing and new namespaces:

```yaml
labels:
  mountainlab.io/tenant: payments
  mountainlab.io/sector: ecommerce
  mountainlab.io/tier: live
  mountainlab.io/region: eu01
  mountainlab.io/quota-template: medium
```

Do not delete namespaces not in the tenant list without explicit user confirmation — namespace deletion removes all resources inside it.

### Step 3 — Apply ResourceQuotas

For each tenant namespace, apply the ResourceQuota from the assigned quota template:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-quota
  namespace: payments
spec:
  hard:
    requests.cpu: "16"
    limits.cpu: "32"
    requests.memory: 32Gi
    limits.memory: 64Gi
    requests.storage: 100Gi
    persistentvolumeclaims: "20"
    pods: "100"
    services: "20"
    secrets: "50"
    configmaps: "50"
```

For each quota:
1. Check whether a `ResourceQuota` named `tenant-quota` exists in the namespace.
2. Create it if missing.
3. Update it if the template has changed — report the delta (old values vs. new values) before applying.

**Quota reductions are breaking changes**: If a quota is being reduced below the namespace's current resource usage, the existing workloads are not affected immediately, but new resource requests will fail. Warn the user before applying a reduction and recommend checking current usage first.

### Step 4 — Apply LimitRanges

For each tenant namespace, apply the LimitRange that injects default resource requests and limits into containers that don't specify them:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: tenant-limits
  namespace: payments
spec:
  limits:
    - type: Container
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
      default:
        cpu: "500m"
        memory: "512Mi"
      max:
        cpu: "4"
        memory: "8Gi"
```

The `max` values prevent a single container from claiming more than a reasonable fraction of the quota, providing basic protection against runaway resource consumption.

For each LimitRange:
1. Check whether it exists.
2. Create or update per the compute design's defaults.

### Step 5 — Apply Default NetworkPolicies

For each tenant namespace, apply a default-deny policy for both ingress and egress. This forces application teams to explicitly define which traffic their services allow.

**Default deny all ingress**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: payments
spec:
  podSelector: {}
  policyTypes:
    - Ingress
```

**Default deny all egress**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: payments
spec:
  podSelector: {}
  policyTypes:
    - Egress
```

**Platform allow-list** (add these in addition to the deny rules):
- Allow egress to the cluster's DNS service (`kube-dns` in `kube-system`, UDP 53):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-egress
  namespace: payments
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

Application teams are responsible for adding further NetworkPolicy rules to allow their service-to-service traffic. The platform provides the default-deny floor and the DNS allow-list.

For each NetworkPolicy:
1. Check whether it exists.
2. Create it if missing.
3. Do not modify or delete NetworkPolicies not managed by this skill (custom policies added by application teams).

### Step 6 — Validate and Report Namespace State

After applying, verify each namespace's state:

- Labels present and correct
- ResourceQuota exists and matches the assigned template
- LimitRange exists
- Default-deny NetworkPolicies exist
- No namespace is over-quota (check current usage vs. quota hard limits)

Report any namespace where current usage exceeds 80% of the quota limit — these are candidates for a quota increase request.

### Step 7 — Report

Produce a summary.

## Output Format

Produce a Markdown report named `k8s-namespaces-report.md`:

```markdown
# Kubernetes Namespace Sync Report

**Date**: [timestamp]
**Cluster**: [cluster context name]
**Mode**: [applied / dry-run]

## Namespaces

| Namespace | Tenant | Quota Template | Status |
|-----------|--------|---------------|--------|
| payments | payments | medium | created |
| recommendations | recommendations | small | exists (labels updated) |

## ResourceQuotas

| Namespace | Template | CPU Req | Mem Req | Status |
|-----------|----------|---------|---------|--------|
| payments | medium | 16 | 32Gi | created |
| recommendations | small | 8 | 16Gi | exists (no change) |

## LimitRanges

| Namespace | Status |
|-----------|--------|
| payments | created |
| recommendations | exists |

## NetworkPolicies

| Namespace | Policy | Status |
|-----------|--------|--------|
| payments | default-deny-ingress | created |
| payments | default-deny-egress | created |
| payments | allow-dns-egress | created |

## Quota Usage Warnings

| Namespace | Resource | Current Usage | Limit | % Used |
|-----------|---------|--------------|-------|--------|
| recommendations | memory requests | 13Gi | 16Gi | 81% |

## Namespaces Not in Tenant List (Orphans)

| Namespace | Action |
|-----------|--------|
| legacy-payments | Not managed — confirm before deletion |

## Open Items
[Quota reduction warnings, network policy CNI compatibility notes, etc.]
```

## Principles to Apply

- **Namespaces are platform-vended**: Tenants do not create their own namespaces. The platform creates them pre-configured. This is the vending machine model — developers request, the platform delivers.
- **Default-deny is the floor**: Application teams must explicitly allow the traffic their services need. The platform does not open any application-level traffic — only DNS is allowed by default.
- **LimitRange prevents unbounded containers**: Without defaults, a container with no resource request may get scheduled with no limits and starve its node. LimitRange makes the safe behavior automatic.
- **Quota reductions require care**: Reducing a quota below current usage does not evict existing workloads but will cause all new resource requests to fail. Always check current usage before reducing.
- **RBAC is separate**: This skill provisions resource boundaries (quota, networking) only. Role bindings are managed by `manage-k8s-iam`.
- **Idempotent**: Check before creating. Report orphan namespaces but do not delete without explicit confirmation.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
