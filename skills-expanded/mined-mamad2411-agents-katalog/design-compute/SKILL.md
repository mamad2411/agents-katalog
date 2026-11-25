---
name: design-compute
description: >
  Design the Kubernetes cluster topology — cluster placement per coordinate, node pool
  strategy, multi-tenancy model, and ResourceQuota tier templates — from the Platform
  Coordinate System. Produces a compute-design.md document used as input for
  manage-k8s-namespaces and cluster provisioning IaC modules. Use after design-segmentation,
  design-networking, and define-naming-convention.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Design Compute

## Skill Type

Design

## Your Goal

Produce a **compute design document** — a cloud-agnostic specification of the Kubernetes cluster topology, node pool strategy, multi-tenancy model, and quota template definitions. This document is the input for `manage-k8s-namespaces` and guides the Terraform/Pulumi IaC modules used for cluster provisioning.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Segmentation design**: The output of `design-segmentation` — Sectors, Tiers, Regions, and Tenants. Cluster placement maps to coordinates.
- **Networking design**: The output of `design-networking` — which spoke VPCs/VNets exist. Clusters live inside spokes.
- **Cloud provider(s)**: AWS (EKS), Azure (AKS), GCP (GKE). Managed Kubernetes service names differ but the design model is the same.
- **Tenant count**: How many tenants (namespaces) will share each cluster? Informs multi-tenancy model choice.
- **Workload types**: Are there GPU workloads, batch jobs, or compliance-isolated workloads that require dedicated node pools?
- **Cluster count vs. namespace count**: Does the organization prefer one cluster per region (pool model) or one cluster per tenant (silo model)? Reference the isolation spectrum from the segmentation design.
- **Autoscaling preference**: Cluster Autoscaler (provider-native) or Karpenter (AWS, or community port for other clouds)?
- **Cost sensitivity**: Spot/preemptible nodes acceptable for sandbox workloads?

## Process

### Step 1 — Determine Cluster Placement

Map clusters to coordinates. A cluster typically corresponds to one `(Sector, Tier, Region)` coordinate — it lives within that spoke's network and inherits the tier's security posture.

**One cluster per `(Sector, Tier, Region)`** (pool model — recommended baseline):
- All tenants in the same sector/tier/region share one cluster, isolated by namespace.
- Efficient: fewer clusters to maintain, lower per-cluster overhead.
- Suitable for most organizations at scale-up and enterprise stages.

**One cluster per `(Sector, Tier, Region, Tenant)`** (silo model — high isolation):
- Each tenant has a dedicated cluster.
- Maximum blast radius reduction, but extremely high operational overhead.
- Reserved for tenants with strict compliance requirements (e.g., a PCI-DSS cardholder data environment).

**Bridge model** (most common in practice):
- Most tenants share a pool cluster.
- A small number of high-compliance tenants get dedicated clusters.
- Document which tenants require dedicated clusters and why.

For each cluster, specify:
- Name (from naming convention, e.g., `k8s-ecommerce-live-eu01`)
- Coordinate: `(Sector, Tier, Region)` or `(Sector, Tier, Region, Tenant)` for silo clusters
- Cloud provider and managed service (EKS, AKS, GKE)
- Network: which spoke VPC/VNet it resides in
- Multi-tenancy model: pool, silo, or bridge

### Step 2 — Design Node Pools

Every cluster needs at least one general-purpose node pool. Define the node pool strategy:

**General-purpose pool** (required):
- Instance type: balanced CPU/memory (e.g., AWS `m5.xlarge`, Azure `Standard_D4s_v5`, GCP `e2-standard-4`)
- Minimum nodes: 3 (for HA across availability zones)
- Maximum nodes: set per cluster based on expected tenant count and workload size
- Autoscaling: enabled, using Karpenter (preferred) or Cluster Autoscaler
- Spot/preemptible: acceptable for Sandbox; not recommended for Live

**Specialized pools** (define only if a workload type requires them):
- **GPU pool**: For ML training or inference workloads. On-demand only. Defined with taints (`dedicated=gpu:NoSchedule`) and labels so workloads explicitly request them.
- **High-memory pool**: For in-memory databases or large caches. Defined with taints and labels.
- **Compliance-isolated pool**: For workloads that must not share kernel with other tenants (e.g., PCI-DSS cardholder data). Dedicated node pool with `dedicated={tenant}:NoSchedule` taint.
- **Batch pool**: Spot/preemptible nodes for cost-effective batch jobs. Tolerates interruption.

For each pool, specify:
- Name
- Instance type(s) (allow multiple for Karpenter NodePool specs)
- Min / max node count
- Availability zone distribution (spread across ≥ 3 AZs)
- Taints and labels
- Spot/on-demand preference
- Which tenants or workload types use it

### Step 3 — Define the Multi-Tenancy Model

For pool clusters (shared by multiple tenants), define the namespace-as-a-service model:

**Namespace per tenant**:
- One namespace per tenant in each cluster.
- Platform automation creates and configures namespaces — tenants do not create their own.
- Each namespace is pre-configured with:
  - ResourceQuota (from the quota template — see Step 4)
  - LimitRange (default CPU/memory requests and limits)
  - NetworkPolicy (default-deny all ingress and egress; platform creates explicit allow-rules)
  - RBAC (RoleBindings from the tenant IAM definition — see `manage-k8s-iam`)
  - Labels encoding the coordinate (`mountainlab.io/tenant`, `mountainlab.io/tier`, etc.)

**Virtual clusters** (`vcluster`):
- An alternative for tenants needing stronger isolation within a shared cluster (separate API server, etcd-equivalent, RBAC space).
- Higher per-tenant overhead but weaker blast radius than a full dedicated cluster.
- Recommend only if namespaces are insufficient (e.g., a tenant needs to install custom CRDs that conflict with other tenants).

Document the model chosen and which (if any) tenants use virtual clusters.

### Step 4 — Define Quota Tier Templates

ResourceQuotas prevent a single tenant from exhausting cluster resources. Define a set of templates that tenants choose from, rather than configuring quotas per tenant (which creates inconsistency).

Recommended templates (adjust numbers based on node sizes):

| Template | CPU Requests | CPU Limits | Memory Requests | Memory Limits | Persistent Storage | Use Case |
|----------|-------------|-----------|----------------|--------------|-------------------|---------|
| `xsmall` | 2 | 4 | 4 Gi | 8 Gi | 10 Gi | Single-service or very small team |
| `small` | 8 | 16 | 16 Gi | 32 Gi | 50 Gi | Small microservice team |
| `medium` | 16 | 32 | 32 Gi | 64 Gi | 100 Gi | Standard product team |
| `large` | 32 | 64 | 64 Gi | 128 Gi | 500 Gi | Large team or data-intensive service |
| `xlarge` | 64 | 128 | 128 Gi | 256 Gi | 1 Ti | Platform or specialized high-load service |

**LimitRange defaults** (injected into every namespace to prevent unbounded containers):
```yaml
defaultRequest:
  cpu: "100m"
  memory: "128Mi"
default:
  cpu: "500m"
  memory: "512Mi"
```
These defaults ensure that containers without explicit resource requests don't get scheduled with no limits.

**Quota increase process**: Define how tenants request a quota increase. Recommended: a pull request to the tenants repository changing the quota tier. The PR triggers a platform review conversation (is the team running out of capacity, or is there a scaling bug?). Friction here is intentional — it surfaces architecture conversations.

### Step 5 — Design the Platform Node Pool

The cluster itself requires resources for platform components (metrics server, logging agents, network policy controller, ingress controller, cert-manager, ExternalDNS). These should run on a dedicated platform node pool to avoid competing with tenant workloads for resources.

- **Platform pool**: 2–3 nodes, on-demand, general-purpose instance type. Taint: `dedicated=platform:NoSchedule`. Platform components tolerate this taint; tenant workloads do not.

### Step 6 — Design Edge Routing Within the Cluster

For each cluster, define how external traffic reaches workloads:

- **Ingress controller**: One ingress controller per cluster (e.g., ingress-nginx, Traefik, or cloud-native). Managed by the platform team; deployed on the platform node pool.
- **ExternalDNS**: Watches Ingress/Service resources and automatically creates DNS records in the spoke's public DNS zone. Tenants create an Ingress with an annotation; ExternalDNS handles the rest.
- **cert-manager**: Issues and renews TLS certificates (Let's Encrypt or internal CA). Tenants annotate Ingress resources with the certificate issuer; cert-manager handles the rest.
- **Gateway API** (optional): If the organization is moving from Ingress to the Kubernetes Gateway API, note the migration path. The platform team manages the `Gateway` resource; tenants manage `HTTPRoute`.

### Step 7 — Review and Iterate

Present the cluster topology, node pool design, and quota templates. Ask:

- Is the pool vs. silo decision correct for all tenants?
- Are the quota templates sized appropriately for the expected workload mix?
- Are there workload types not covered by the defined node pools?
- Is the edge routing model (Ingress vs. Gateway API) aligned with the team's current tooling?

Iterate until satisfied.

## Output Format

Produce a Markdown document named `compute-design.md`:

```markdown
# Compute Design

## Cluster Topology

| Cluster Name | Coordinate | Provider | Network Spoke | Multi-Tenancy Model |
|-------------|-----------|----------|--------------|---------------------|
| k8s-ecommerce-live-eu01 | ("ecommerce", "live", "eu01", _) | AKS | vnet-ecommerce-live-eu01 | Pool (all tenants) |
| k8s-payments-live-eu01 | ("ecommerce", "live", "eu01", "payments") | AKS | vnet-ecommerce-live-eu01 | Silo (PCI scope) |

## Node Pools

### Cluster: k8s-ecommerce-live-eu01

| Pool Name | Purpose | Instance Type | Min/Max | Spot? | Taints |
|-----------|---------|--------------|---------|-------|--------|
| general | Default tenant workloads | Standard_D4s_v5 | 3/20 | No | — |
| platform | Platform components | Standard_D2s_v5 | 2/3 | No | dedicated=platform:NoSchedule |

## Multi-Tenancy Model

[Pool / Silo / Bridge description with which tenants get dedicated clusters]

## Namespace Configuration

[Pre-configured components: ResourceQuota, LimitRange, NetworkPolicy, RBAC, Labels]

## Quota Templates

| Template | CPU Req | CPU Limit | Mem Req | Mem Limit | Storage |
|----------|---------|-----------|---------|-----------|---------|
| xsmall | 2 | 4 | 4 Gi | 8 Gi | 10 Gi |
| small | 8 | 16 | 16 Gi | 32 Gi | 50 Gi |
| medium | 16 | 32 | 32 Gi | 64 Gi | 100 Gi |
| large | 32 | 64 | 64 Gi | 128 Gi | 500 Gi |
| xlarge | 64 | 128 | 128 Gi | 256 Gi | 1 Ti |

### LimitRange Defaults
[Default CPU/memory requests and limits injected into every namespace]

### Quota Increase Process
[PR-based process and review policy]

## Edge Routing

[Ingress controller, ExternalDNS, cert-manager, Gateway API note]

## Assumptions and Open Questions
[...]
```

## Principles to Apply

- **Platform as a namespace vending machine**: Tenants request namespaces; the platform delivers them pre-configured with quota, network policy, RBAC, and labels. Tenants never create namespaces themselves.
- **Quota friction is a feature**: The ResourceQuota system forces a conversation when teams run out of capacity. This is intentional circuit-breaker behavior that surfaces bad architecture before it becomes a production incident.
- **Platform components on their own pool**: Metrics collection, log shipping, and ingress routing must not compete with tenant workloads for node resources.
- **LimitRange protects the cluster from runaway containers**: A container with no resource request can starve the node. LimitRange defaults prevent this without requiring every developer to set explicit limits.
- **Ingress is a platform concern, routing is a tenant concern**: The platform provides the ingress controller and edge gateway; tenants configure their own `Ingress` or `HTTPRoute` resources.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
