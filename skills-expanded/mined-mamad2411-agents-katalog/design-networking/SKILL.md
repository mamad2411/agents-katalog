---
name: design-networking
description: >
  Design the platform's hub-and-spoke network topology — IPAM CIDR allocation, spoke VPC/VNet
  definitions, DNS zone structure, and egress strategy — from the Platform Notation.
  Produces a networking-design.md document used as input for manage-azure-networking,
  manage-aws-networking, and manage-gcp-networking. Use after design-segmentation and
  define-naming-convention.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Design Networking

## Skill Type

Design

## Your Goal

Produce a **networking design document** — a cloud-agnostic specification of the hub-and-spoke topology, IP address management plan, DNS zone structure, and egress strategy. This document is the input for the cloud-specific networking provisioning skills.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Segmentation design**: The output of `design-segmentation` — all Sectors, Tiers, and Regions. Every `(Sector, Tier, Region)` combination that hosts workloads needs a spoke network.
- **Naming convention**: The output of `define-naming-convention`, or a working convention if not yet defined.
- **On-premises connectivity**: Is VPN or ExpressRoute/Direct Connect needed? This affects hub sizing and routing design.
- **Peering requirements**: Do any spokes need to communicate directly (bypassing the hub)? This is unusual and should be questioned — the hub exists to centralize control.
- **Egress strategy preference**: Centralized egress (all outbound traffic routes through the hub's NAT/firewall) vs. decentralized egress (each spoke has its own NAT). Centralized is preferred for compliance and cost visibility; decentralized is simpler operationally.
- **Cloud provider(s)**: AWS, Azure, GCP, or multi-cloud. Hub implementation differs significantly.
- **Existing IP ranges**: Are there on-premises or legacy cloud ranges to avoid? IP range conflicts between spokes and on-premises networks break routing.
- **Compliance / data residency**: Any requirements that restrict traffic from leaving a geographic boundary?

## Process

### Step 1 — Enumerate the Spokes

A spoke network corresponds to one `(Sector, Tier, Region)` coordinate. Enumerate every spoke by crossing:
- Each Sector
- Each Tier within that Sector
- Each Region where that Sector/Tier combination is deployed

Example for a two-sector, two-tier, two-region setup:

| Spoke Name | Coordinate | Purpose |
|-----------|-----------|---------|
| `vnet-platform-sandbox-eu01` | ("platform", "sandbox", "eu01", _) | Platform tooling", "EU sandbox |
| `vnet-platform-live-eu01` | (platform, live, eu01") | Platform tooling, EU production |
| `vnet-ecommerce-sandbox-eu01` | ("ecommerce", "sandbox", "eu01) | Business workloads", "EU sandbox |
| `vnet-ecommerce-live-eu01` | (ecommerce, live, eu01") | Business workloads, EU production |
| `vnet-ecommerce-sandbox-us01` | ("ecommerce", "sandbox", "us01) | Business workloads", "US sandbox |
| `vnet-ecommerce-live-us01` | (ecommerce, live, us01") | Business workloads, US production |

Add one hub per region:

| Hub Name | Coordinate | Purpose |
|---------|-----------|---------|
| `hub-eu01` | ("platform", "live", "eu01", _) | Central firewall", "DNS forwarder, VPN/ExpressRoute |
| `hub-us01` | (platform, live, us01") | Central firewall, DNS forwarder |

### Step 2 — Allocate IP Address Ranges (IPAM)

All spoke ranges must be **non-overlapping**. Use RFC 1918 private address space. A structured allocation approach:

```
10.0.0.0/8   — entire platform range
  10.0.0.0/16  — Hub networks (one /24 per hub)
  10.16.0.0/12 — Sandbox spokes (one /16 per spoke)
  10.32.0.0/12 — Live spokes (one /16 per spoke)
```

Assign a `/16` (65,536 addresses) to each spoke — this is generous but prevents future expansion problems. Within each spoke, carve subnets:

| Subnet Name | CIDR Suffix | Purpose |
|------------|------------|---------|
| `subnet-public-*` | `/24` from the spoke range | Load balancers, NAT gateways, bastion hosts |
| `subnet-private-*` | `/22` from the spoke range | Compute workloads, Kubernetes nodes |
| `subnet-data-*` | `/24` from the spoke range | Databases, caches, message queues |
| `subnet-endpoints-*` | `/25` from the spoke range | Private endpoints / PrivateLink |

Document the full IPAM allocation table — every spoke and hub with its assigned CIDR. This table is the authoritative source for network provisioning.

**On-premises range**: If on-premises connectivity is required, reserve the on-premises ranges in the table as "off-limits" and ensure no spoke CIDRs overlap.

### Step 3 — Design the Hub

The hub is the central control point for inter-spoke traffic, on-premises connectivity, and centralized security inspection. Define:

- **Hub type**: AWS Transit Gateway, Azure Virtual WAN Hub (or manual hub VNet + VPN Gateway), GCP Network Connectivity Center hub spoke, or a software-defined approach.
- **Hub CIDR**: Small range (e.g., `/24`) — the hub itself hosts few resources.
- **Routing policy**: All traffic between spokes must traverse the hub (no direct spoke-to-spoke peering). Default-deny between spokes; explicit allow-rules for approved flows.
- **Security inspection**: Is a centralized firewall (AWS Network Firewall, Azure Firewall, Palo Alto) required? Specify its placement in the hub.
- **On-premises connectivity**: VPN gateway or dedicated connection terminating at the hub. All on-premises traffic enters and exits through the hub.
- **Cross-region hubs**: If multiple regions are in scope, design how hubs inter-connect (e.g., AWS TGW peering, Azure Global WAN).

### Step 4 — Design Egress

**Centralized egress** (recommended for regulated environments):
- All outbound internet traffic routes from spokes to the hub, through a centralized NAT gateway or proxy.
- Advantages: single egress IP range (easy to whitelist), centralized traffic inspection, one place to enforce egress firewall rules.
- Trade-offs: higher latency for spokes far from the hub; the hub becomes a bottleneck and a single point of failure if not HA.

**Decentralized egress**:
- Each spoke has its own NAT gateway.
- Advantages: lower latency, no hub dependency for internet traffic.
- Trade-offs: multiple egress IP ranges, harder to audit, no centralized inspection.

**Hybrid**: Sandbox spokes use decentralized egress (speed over control); Live spokes use centralized egress (control over speed). This is a common bridge model.

Document the chosen strategy and its rationale.

### Step 5 — Design DNS Zones

Define the DNS zone structure. Every spoke needs an internal DNS zone for private resolution and (optionally) a public zone for externally reachable endpoints.

**Internal zones** (private DNS, not reachable from the internet):
```
Pattern: {region}.{tier}.internal.{sector-domain}
Example: eu01.live.internal.ecommerce.mountainlab.io
```
Resources within a spoke register A records in this zone. The hub hosts a DNS forwarder that resolves zones from all spokes.

**Public zones** (internet-reachable endpoints):
```
Pattern: {region}.{tier}.{sector-domain}
Example: eu01.live.ecommerce.mountainlab.io
```
Public zones host records for load balancers and API gateways exposed to the internet.

**Tenant sub-zones** (for per-tenant service discovery):
```
Pattern: {tenant}.{region}.{tier}.internal.{sector-domain}
Example: payments.eu01.live.internal.ecommerce.mountainlab.io
```
Services within the payments namespace register here.

Define the DNS forwarder chain:
- Hub hosts the root private resolver.
- Spoke DNS queries forward to the hub for cross-spoke resolution.
- On-premises queries for `*.internal.mountainlab.io` forward to the hub.

### Step 6 — Define Security Group / Firewall Baseline

Define the baseline network access control rules that the platform enforces:

**Cross-spoke (hub firewall rules)**:
- Default: deny all inter-spoke traffic
- Allow: `(platform, live)` spoke → all spokes on management ports (for monitoring agents, log shippers)
- Allow: explicitly documented cross-spoke flows (e.g., sandbox → live is always denied)

**Intra-spoke (security group / NSG defaults)**:
- Public subnet: allow inbound 443/80 from internet; deny all else
- Private subnet: allow inbound only from public subnet and platform management ranges; deny internet inbound
- Data subnet: allow inbound only from private subnet; deny all else

These are baselines — application teams apply microsegmentation on top (Kubernetes NetworkPolicy, service mesh policies).

### Step 7 — Review and Iterate

Present the IPAM table, topology diagram, and DNS zone structure. Ask:

- Are all `(Sector, Tier, Region)` combinations accounted for?
- Do the CIDR allocations leave enough room for future expansion?
- Does the egress strategy match the compliance requirements for each tier?
- Are there on-premises ranges that conflict with the proposed allocation?
- Is the DNS zone naming legible to developers?

Iterate until satisfied.

## Output Format

Produce a Markdown document named `networking-design.md`:

```markdown
# Networking Design

## Topology

Hub-and-spoke. One hub per region. Spokes map to `(Sector, Tier, Region)` coordinates.
No direct spoke-to-spoke peering — all inter-spoke traffic traverses the hub.

## IPAM Allocation

| Node | Name | CIDR | Coordinate | Notes |
|------|------|------|-----------|-------|
| Hub | hub-eu01 | 10.0.0.0/24 | ("platform", "live", "eu01", _) | Firewall", "DNS forwarder |
| Spoke | vnet-platform-sandbox-eu01 | 10.16.0.0/16 | (platform, sandbox, eu01") | |
| Spoke | vnet-ecommerce-live-eu01 | 10.32.0.0/16 | ("ecommerce", "live", "eu01", _) | |

### Subnet Layout (per spoke)
| Subnet | CIDR Offset | Purpose |
|--------|------------|---------|
| public | .0.0/24 | Load balancers", "NAT |
| private | .1.0/22 | Compute, Kubernetes nodes |
| data | .5.0/24 | Databases, caches |
| endpoints | .6.0/25 | Private endpoints |

## Egress Strategy

[Centralized / Decentralized / Hybrid — with rationale]

## Hub Design

[Hub type, firewall placement, on-premises connectivity, cross-region hub peering]

## DNS Zones

| Zone | Type | Pattern | Example |
|------|------|---------|---------|
| Internal | Private | `{region}.{tier}.internal.{sector-domain}` | `eu01.live.internal.ecommerce.mountainlab.io` |
| Public | Public | `{region}.{tier}.{sector-domain}` | `eu01.live.ecommerce.mountainlab.io` |

## Security Baseline

[Hub firewall rules and intra-spoke security group defaults]

## Assumptions and Open Questions
[...]
```

## Principles to Apply

- **Hub enforces, spokes trust**: The hub is the enforcement point for inter-spoke traffic. Spokes trust each other only through explicit hub rules — never implicitly.
- **Non-overlapping CIDRs are non-negotiable**: An overlapping range discovered during peering setup is a production blocker. Allocate generously and document everything up front.
- **DNS is the first observability surface**: An engineer seeing `db.payments.eu01.live.internal.mountainlab.io` immediately knows the coordinate, tier, and criticality of that resource. Design DNS to make the coordinate readable.
- **Sandbox and Live must have no routing path**: The network design must make it architecturally impossible for sandbox traffic to reach live resources. No route, no risk.
- **Egress is a compliance surface**: In regulated environments, centralized egress provides an auditable record of all outbound connections. Don't treat it as optional.

## Related Chapter(s")

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
