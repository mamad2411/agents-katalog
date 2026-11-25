---
name: manage-azure-networking
description: >
  Provision and sync Azure networking resources — Virtual WAN Hubs, Spoke VNets, subnets,
  VNet peering, NSGs, Azure Firewall rules, and Private DNS zones — from a networking-design.md
  and naming-convention.md. Uses the Azure MCP server. Use when applying or updating Azure
  networking after running design-networking.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Manage Azure Networking

## Skill Type

Implementation

## System Requirements

- **Azure MCP server** configured and authenticated.
- The executing identity must have:
  - `Network Contributor` at the Subscription scope (or Resource Group scope for spoke resources)
  - `Microsoft.Network/virtualWans/write`, `Microsoft.Network/virtualHubs/write` (if using Virtual WAN)
  - `Microsoft.Network/privateDnsZones/write`
  - `Microsoft.Network/azureFirewalls/write` (if deploying Azure Firewall)
- Subscriptions and Resource Groups from the landing zone must already exist (output of `manage-azure-landing-zone`).

## Your Goal

Apply the networking definition from `networking-design.md` to Azure. Ensure that:

1. Virtual WAN and Hub resources exist per region (or hub VNets if Virtual WAN is not in use).
2. Spoke VNets exist per `(Sector, Tier, Region)` with correct CIDRs and subnets.
3. Spokes are connected to the hub (VNet connections or peering).
4. NSGs enforce the security baseline per subnet.
5. Private DNS zones exist and are linked to the correct VNets.
6. No direct spoke-to-spoke peering exists (all traffic routes through hub).

This skill is **idempotent**.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

- **Networking design**: Path to `networking-design.md`. Read it first.
- **Naming convention**: Path to `naming-convention.md`.
- **Landing zone mapping**: Which Subscriptions hold the hub vs. each spoke (from `landing-zone-design.md`).
- **Hub type**: Virtual WAN (recommended for large deployments) or hub VNet + VPN Gateway (simpler, lower cost for small deployments)?
- **Firewall**: Is Azure Firewall to be deployed in the hub? Or a third-party NVA?
- **Scope of this run**: All spokes, specific regions, or specific coordinates?
- **Dry-run mode**: Recommended for first-time runs.

Read all input documents before proceeding.

## Process

### Step 1 — Provision Hub

For each region in scope:

**Virtual WAN approach**:
1. Check whether a Virtual WAN resource exists in the connectivity Subscription.
2. Create the Virtual WAN if missing (type: `Standard` for full routing and firewall support).
3. Check whether a Virtual Hub exists for the region.
4. Create the Virtual Hub with the hub CIDR from the IPAM table.
5. If Azure Firewall is required: deploy Azure Firewall in the hub and configure the routing intent to route all traffic through it.

**Hub VNet approach** (alternative for smaller deployments):
1. Create a hub VNet in the connectivity Subscription with the hub CIDR.
2. Deploy Azure VPN Gateway or ExpressRoute Gateway if on-premises connectivity is required.
3. Deploy Azure Firewall (optional) in its dedicated `AzureFirewallSubnet`.

### Step 2 — Provision Spoke VNets

For each spoke in the networking design:
1. Determine the target Subscription (from the landing zone — a spoke VNet lives in the Subscription corresponding to its coordinate's Sector and Tier).
2. Check whether the VNet exists.
3. Create the VNet with the CIDR from the IPAM allocation table if missing.
4. Tag the VNet with mandatory tags.

### Step 3 — Provision Subnets

For each spoke VNet, create the required subnets from the design:

| Subnet | CIDR Offset | Delegation / Purpose |
|--------|------------|---------------------|
| `subnet-public-*` | `.0.0/24` | Load balancers, Application Gateway |
| `subnet-private-*` | `.1.0/22` | AKS node pools, compute workloads |
| `subnet-data-*` | `.5.0/24` | Managed databases, Redis Cache |
| `subnet-endpoints-*` | `.6.0/25` | Private Endpoints |
| `AzureBastionSubnet` | `.7.0/26` | Azure Bastion (if required) |

For AKS node pool subnets, ensure the subnet is large enough for the maximum node count × pod CIDR. Apply the correct subnet delegation if required (e.g., `Microsoft.ContainerService/managedClusters`).

### Step 4 — Connect Spokes to Hub

**Virtual WAN**: Create a VNet Connection from each spoke VNet to the Virtual Hub. Set the routing configuration to route all traffic through the hub (associated route table: `defaultRouteTable`; propagated route tables: `defaultRouteTable`).

**Hub VNet peering**: Create VNet peerings between the hub VNet and each spoke VNet (bidirectional). On the hub side, allow gateway transit. On the spoke side, use remote gateway. This allows on-premises routes learned by the hub gateway to propagate to spokes.

Verify: no direct spoke-to-spoke peerings exist. If any are found, report them and ask the user whether to remove them.

### Step 5 — Attach NSGs

For each subnet, attach a Network Security Group with the baseline rules from the networking design:

**Public subnet NSG**:
- Allow inbound TCP 443, 80 from Internet
- Allow inbound from hub management range (for health probes)
- Deny all other inbound

**Private subnet NSG**:
- Allow inbound from public subnet CIDR
- Allow inbound from hub management range
- Deny inbound from Internet

**Data subnet NSG**:
- Allow inbound from private subnet CIDR only
- Deny all other inbound

Create NSGs in the same Resource Group as the VNet. Associate them to subnets after creation.

### Step 6 — Provision Private DNS Zones

For each spoke, create the internal Private DNS zone:

1. Create the DNS zone (e.g., `eu01.live.internal.ecommerce.mountainlab.io`) in the connectivity Subscription.
2. Link the zone to the hub VNet (with auto-registration disabled — zones are managed by the platform).
3. Link the zone to the relevant spoke VNets.
4. For cross-spoke resolution: link all internal zones to the hub VNet so the hub DNS resolver can forward queries.

If Azure Private DNS Resolver is in use, configure inbound endpoints in the hub subnet and outbound forwarding rules for on-premises DNS zones.

### Step 7 — Report

Produce a summary of all resources created, already existing, or skipped.

## Output Format

Produce a Markdown report named `azure-networking-report.md`:

```markdown
# Azure Networking Sync Report

**Date**: [timestamp]
**Mode**: [applied / dry-run]

## Hubs

| Name | Region | Type | Status |
|------|--------|------|--------|
| vhub-eu01 | westeurope | Virtual WAN Hub | created |

## Spoke VNets

| Name | Subscription | CIDR | Status |
|------|-------------|------|--------|
| vnet-ecommerce-live-eu01 | sub-ecommerce-live | 10.32.0.0/16 | created |

## Hub Connections

| Spoke VNet | Hub | Status |
|-----------|-----|--------|
| vnet-ecommerce-live-eu01 | vhub-eu01 | created |

## NSG Associations

| Subnet | NSG | Status |
|--------|-----|--------|
| subnet-private-ecommerce-live-eu01 | nsg-private-ecommerce-live-eu01 | created |

## Private DNS Zones

| Zone | Linked VNets | Status |
|------|-------------|--------|
| eu01.live.internal.ecommerce.mountainlab.io | vnet-ecommerce-live-eu01, hub-vnet | created |

## Direct Spoke-to-Spoke Peerings Found
[List any found — should be empty]

## Open Items
[...]
```

## Principles to Apply

- **All inter-spoke traffic through the hub**: Never create direct spoke-to-spoke peering. The hub enforces network-level isolation between tiers and sectors.
- **Sandbox and Live spokes have no routing path**: The hub routing configuration must explicitly deny traffic from Sandbox spokes to Live spokes.
- **NSGs on every subnet**: Azure does not apply default-deny inbound from the internet to VNets created without NSGs. Explicit NSGs are required.
- **Private DNS zones are platform-managed**: Tenants register services; the platform manages the zones and links. Tenants do not create their own DNS zones.
- **Idempotent**: Check state before creating. Report but do not remove existing direct peerings without confirmation.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
