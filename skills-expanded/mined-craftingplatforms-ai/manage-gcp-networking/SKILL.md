---
name: manage-gcp-networking
description: >
  Provision and sync GCP networking resources — Network Connectivity Center hubs and spokes,
  Shared VPC host projects and service projects, subnets, firewall rules, and Cloud DNS
  private zones — from a networking-design.md and naming-convention.md. Uses the GCP MCP
  server. Use when applying or updating GCP networking after running design-networking.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Manage GCP Networking

## Skill Type

Implementation

## System Requirements

- **GCP MCP server** configured and authenticated.
- The executing identity must have at the Organization level (or relevant projects):
  - `compute.networks.create`, `compute.subnetworks.create`
  - `compute.firewalls.create`, `compute.routes.create`
  - `networkconnectivity.hubs.create`, `networkconnectivity.spokes.create`
  - `compute.organizations.enableXpnResource` (for Shared VPC)
  - `dns.managedZones.create`, `dns.resourceRecordSets.create`
- GCP projects from the landing zone must already exist (output of `manage-gcp-landing-zone`).

## Your Goal

Apply the networking definition from `networking-design.md` to GCP. Ensure that:

1. Network Connectivity Center hub exists in the connectivity project.
2. Shared VPC is configured: connectivity project is the host project; workload projects are service projects.
3. Subnets exist per `(Sector, Tier, Region)` with correct CIDRs.
4. Firewall rules enforce the security baseline.
5. Cloud DNS private zones exist per spoke and are peered to the hub for cross-spoke resolution.
6. No VPC peering exists between spoke projects that bypasses the hub.

This skill is **idempotent**.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

- **Networking design**: Path to `networking-design.md`. Read it first.
- **Naming convention**: Path to `naming-convention.md`.
- **Project IDs**: The GCP Project IDs for the connectivity project and each spoke project (from `landing-zone-design.md`).
- **NCC vs. Shared VPC**: GCP offers two primary hub-and-spoke patterns:
  - **Shared VPC** (recommended for most deployments): One host VPC in the connectivity project; subnets shared to service projects. Simpler routing but less isolation between spokes.
  - **NCC + VPC Spokes**: Separate VPC per project, connected via NCC. Stronger per-spoke isolation, more complex routing.
  Confirm which model the networking design specifies.
- **Cloud NAT**: Centralized (in the connectivity project) or decentralized (one NAT per project)?
- **Scope of this run**: All projects, specific regions, or specific coordinates?
- **Dry-run mode**: Recommended for first-time runs.

Read all input documents before proceeding.

## Process

### Step 1 — Provision the Hub Network

**Shared VPC approach** (recommended):

In the connectivity project:
1. Create a VPC network (custom subnet mode — do not use auto-mode, which creates subnets in all regions).
2. Enable the connectivity project as a Shared VPC host project using `compute.organizations.enableXpnResource`.
3. Attach each spoke project as a Shared VPC service project.

Subnets are created in the host VPC and shared to service projects — spoke workloads run in service projects but use subnets from the host project's network.

**NCC approach**:

In the connectivity project:
1. Create a Network Connectivity Center hub.
2. For each spoke project, create a VPC network in that project.
3. Create NCC VPC spokes connecting each spoke VPC to the hub.
4. Configure routing: each spoke's traffic routes through the hub.

### Step 2 — Provision Subnets

For each `(Sector, Tier, Region)` combination, create the required subnets in the hub VPC (Shared VPC) or in each spoke VPC (NCC):

| Subnet | CIDR Offset | Purpose | Private Google Access |
|--------|------------|---------|----------------------|
| `subnet-public-*` | `.0.0/24` | Load balancers, NAT | No |
| `subnet-private-*` | `.1.0/22` | GKE nodes, compute | Yes |
| `subnet-data-*` | `.5.0/24` | Cloud SQL, Memorystore | Yes |
| `subnet-proxy-*` | `.6.0/26` | Internal load balancers (proxy-only subnet) | N/A |

**GKE secondary ranges**: GKE clusters require secondary IP ranges on the node subnet for Pod CIDRs and Service CIDRs. Define these in the networking design and add them as secondary ranges on the private subnet:
- Pod CIDR: `/17` (or larger) per cluster
- Service CIDR: `/20` per cluster

Enable Private Google Access on all private and data subnets so workloads can reach Google APIs without a public IP.

**Shared VPC subnet sharing**: For each subnet, specify which service projects are allowed to use it. Only the projects corresponding to the subnet's coordinate should have access.

### Step 3 — Provision Firewall Rules

GCP firewall rules are attached to the VPC network (not subnets). Create rules from the security baseline:

**Baseline rules (applied to all spokes)**:
- `deny-all-ingress` (priority 65534): Deny all ingress. This is the implicit default in GCP, but making it explicit with a named rule makes auditing clearer.
- `allow-internal-ingress` (priority 1000): Allow ingress from the VPC's own CIDR (intra-spoke communication). Apply only to private and data subnets via target tags.
- `allow-hub-management` (priority 900): Allow ingress from the hub/platform management CIDR on management ports (SSH, metrics scraping, health checks). Apply via target tags.
- `allow-lb-health-checks` (priority 800): Allow ingress from Google's health check IP ranges (`35.191.0.0/16`, `130.211.0.0/22`) on health check ports.

**`Tier("live")` additional rules**:
- No `allow-public-ingress` — external traffic must enter through a load balancer, not directly to VMs.

**`Tier("sandbox")`**:
- Optionally allow developer SSH via IAP (`allow-iap-ssh`, allowing `35.235.240.0/20` on port 22) — use Identity-Aware Proxy instead of public SSH.

For each rule:
1. Check whether it exists in the target VPC.
2. Create it if missing.

### Step 4 — Provision Cloud NAT

**Centralized**: Deploy Cloud NAT in the connectivity project, attached to the hub VPC's router. Route all egress traffic from spoke subnets through the hub's Cloud NAT via NCC routing.

**Decentralized**: Deploy Cloud NAT in each spoke project (for Shared VPC: in the service project's region, attached to the host VPC's Cloud Router for that region). Configure each subnet to use manual IP allocation for auditable egress IPs.

### Step 5 — Provision Cloud DNS Private Zones

For each spoke `(Sector, Tier, Region)`:
1. Create a Cloud DNS private managed zone (e.g., `eu01.live.internal.ecommerce.mountainlab.io`).
2. Set the zone's visibility to `private` and restrict it to the hub VPC (for Shared VPC) or the spoke VPC (for NCC).
3. Configure DNS peering or DNS forwarding from the hub to resolve spoke zones:
   - In the hub VPC, create a DNS forwarding zone pointing to each spoke's internal zone.
   - Alternatively, use Cloud DNS peering between the hub and spoke zones.
4. For on-premises DNS: create a DNS policy with an inbound server policy in the hub VPC, exposing a fixed inbound IP that on-premises resolvers can forward to.

### Step 6 — Report

Produce a summary of all resources created, already existing, or skipped.

## Output Format

Produce a Markdown report named `gcp-networking-report.md`:

```markdown
# GCP Networking Sync Report

**Date**: [timestamp]
**Mode**: [applied / dry-run]
**Model**: [Shared VPC / NCC]

## Hub Network

| Resource | Project | Status |
|---------|---------|--------|
| VPC: hub-network | connectivity | created |
| Shared VPC host enabled | connectivity | applied |

## Service Project Attachments

| Service Project | Status |
|----------------|--------|
| ecommerce-live | attached |
| ecommerce-sandbox | attached |

## Subnets

| Name | VPC | CIDR | Region | Status |
|------|-----|------|--------|--------|
| subnet-private-ecommerce-live-eu01 | hub-network | 10.32.1.0/22 | europe-west1 | created |

## Firewall Rules

| Name | Network | Direction | Source | Ports | Status |
|------|---------|-----------|--------|-------|--------|
| allow-hub-management | hub-network | Ingress | 10.0.0.0/24 | 22, 9100 | created |

## Cloud DNS Private Zones

| Zone | Visibility | VPCs Authorized | Status |
|------|-----------|----------------|--------|
| eu01.live.internal.ecommerce.mountainlab.io | Private | hub-network | created |

## Direct VPC Peerings Between Spokes Found
[List any found — should be empty]

## Open Items
[GKE secondary range sizing, Shared VPC subnet sharing confirmations, etc.]
```

## Principles to Apply

- **Shared VPC keeps subnets in one place**: The connectivity project owns all subnets. Service projects borrow them. This gives the platform team full control over IP allocation and routing without touching workload projects.
- **Private Google Access on all workload subnets**: GKE nodes and Cloud SQL instances must reach Google APIs without public IPs. Enable Private Google Access — it is not enabled by default.
- **Firewall rules are VPC-wide**: Unlike AWS Security Groups (per-resource), GCP firewall rules apply to the entire VPC and are scoped by target tags. Use consistent tags on all compute resources to ensure correct rule application.
- **GKE secondary ranges must be pre-allocated**: GKE clusters fail to create if the node subnet lacks secondary IP ranges. Define and provision secondary ranges before cluster provisioning.
- **No spoke-to-spoke VPC peering**: All inter-spoke traffic must traverse the hub. Report any direct peerings found between spoke VPCs as a policy violation.
- **Idempotent**: Check state before creating. Never delete VPCs or subnets without confirmation.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
