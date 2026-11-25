# vwan_design — Virtual WAN Topology Design

## Overview

This skill covers Azure Virtual WAN topology design decisions including tier selection, single-hub versus multi-hub architectures, secured hub configuration, capacity planning, and connection type provisioning. Virtual WAN provides Microsoft-managed hub infrastructure that eliminates the operational overhead of maintaining custom hub VNets, route tables, and VNet peering relationships.

## vWAN Tier Comparison

| Feature | Basic Tier | Standard Tier |
|---------|-----------|---------------|
| Site-to-site VPN | Yes | Yes |
| Point-to-site VPN | No | Yes |
| ExpressRoute | No | Yes |
| VNet-to-VNet transit | No | Yes (any-to-any) |
| Hub-to-hub transit | No | Yes (via Microsoft backbone) |
| Multi-hub deployment | No (single hub) | Yes |
| Secured Virtual Hub | No | Yes |
| Routing Intent | No | Yes |
| Branch-to-branch routing | No | Yes |
| NVA in hub | No | Yes |
| Maximum VPN scale units | 1 (500 Mbps) | 20 (10 Gbps aggregate) |
| Hub-to-hub bandwidth | N/A | Up to 50 Gbps |

**Recommendation:** Use Standard tier for all production deployments. Basic tier is suitable only for proof-of-concept scenarios with a single site-to-site VPN requirement and no transit needs.

## Single-Hub vs Multi-Hub Decision Criteria

### Single-Hub Architecture

Deploy a single hub when:

- All branch offices and spoke VNets are concentrated in one Azure region
- Total aggregate bandwidth from all branches does not exceed the capacity of a single hub (up to 20 VPN scale units = 10 Gbps)
- Latency between the hub region and all branches is acceptable (typically under 50ms RTT)
- Fewer than 500 VPN site connections are needed

### Multi-Hub Architecture

Deploy multiple hubs across regions when:

- Branch offices are distributed across geographies requiring regional affinity (e.g., US East hub for North American branches, West Europe hub for EMEA branches)
- Total VPN capacity exceeds single hub limits
- Regulatory or data sovereignty requirements mandate regional traffic containment
- ExpressRoute circuits terminate in different Azure peering locations
- Active-active disaster recovery topologies are needed

In Standard tier, hub-to-hub connectivity is automatic. Traffic between hubs traverses the Microsoft global backbone without requiring user-configured tunnels or peering. The hub router (AS 65520) automatically exchanges routes between hubs using an internal iBGP mesh.

## Secured Virtual Hubs

A secured virtual hub is a vWAN hub with Azure Firewall or a supported NVA deployed for inline traffic inspection. Secured hubs integrate with Azure Firewall Manager for centralized policy management.

Key characteristics:

- Azure Firewall in the hub inspects east-west (spoke-to-spoke, branch-to-spoke) and north-south (internet) traffic
- Firewall policies are managed via Azure Firewall Manager, enabling consistent policy across multiple secured hubs
- When Azure Firewall is deployed, routing intent can be configured to automatically steer traffic through the firewall
- Secured hubs support both Azure Firewall Standard and Premium SKUs (Premium adds TLS inspection, IDPS, URL filtering by category)

## Hub Capacity Units and Scaling

Virtual WAN hub components scale independently:

- **Hub router:** Capacity is expressed in Routing Infrastructure Units (RIUs). Azure documents the default and maximum RIU/throughput values in the hub settings table; verify the current table before sizing or quoting throughput: https://learn.microsoft.com/en-us/azure/virtual-wan/hub-settings.
- **S2S VPN gateway:** Scale units from 1 to 20. Each unit = 500 Mbps. Maximum: 20 units = 10 Gbps aggregate.
- **P2S VPN gateway:** Scale units from 1 to 20. Each unit = 500 Mbps. Maximum: 20 units = 10 Gbps aggregate. Supports up to 100,000 concurrent P2S connections.
- **ExpressRoute gateway:** Scale units from 1 to 10. Each unit = 2 Gbps. Maximum: 10 units = 20 Gbps aggregate.
- **Azure Firewall:** Standard and Premium SKUs, throughput up to 30 Gbps (Premium) or 100 Gbps (Premium with forced tunneling disabled in latest updates — verify current limits).

## Connection Types

### VNet Connections

Connect spoke VNets to the hub. Each connected VNet gets automatic route propagation from the hub route table. Supports propagation to and association with custom route tables.

### S2S VPN Connections

IPsec/IKEv2 tunnels from branch CPE devices to the hub VPN gateway. Supports BGP for dynamic route exchange. Each VPN site can have up to 4 links (active-active, dual ISP).

### P2S VPN Connections

Remote user VPN connectivity via OpenVPN, IKEv2, or SSTP protocols. Integrates with Azure AD for authentication.

### ExpressRoute Connections

Private connectivity from on-premises datacenters via ExpressRoute circuits. Supports both Standard and Premium circuits. Global Reach can be enabled for branch-to-branch routing over ExpressRoute.

## Hub IP Addressing

Each hub requires a unique address space. Use `/24` only for basic non-firewall hubs, `/23` as a general baseline, and `/22` or larger when Azure Firewall is deployed in the vWAN hub; verify current requirements in Azure hub settings before deployment. This address space is used for:

- Hub router interfaces
- VPN gateway instances
- ExpressRoute gateway instances
- NVA deployments (if applicable)
- Azure Firewall subnet (if secured hub)

**Best practice:** Assign at least a /23 to general-purpose hubs and /22 or larger to secured hubs with Azure Firewall. Ensure hub address spaces do not overlap with spoke VNets or on-premises address ranges.

## CLI Commands

### Create a Virtual WAN

```bash
az network vwan create \
  --name "contoso-vwan" \
  --resource-group "rg-networking" \
  --location "eastus" \
  --type "Standard" \
  --branch-to-branch-traffic true \
  --office365-category "Optimize"
```

### Create a Virtual Hub

```bash
az network vhub create \
  --name "hub-eastus" \
  --resource-group "rg-networking" \
  --vwan "contoso-vwan" \
  --location "eastus" \
  --address-prefix "10.100.0.0/23" \
  --sku "Standard"
```

### Create a Second Hub (Multi-Hub)

```bash
az network vhub create \
  --name "hub-westeurope" \
  --resource-group "rg-networking" \
  --vwan "contoso-vwan" \
  --location "westeurope" \
  --address-prefix "10.101.0.0/23" \
  --sku "Standard"
```

### Connect a Spoke VNet to the Hub

```bash
az network vhub connection create \
  --name "conn-spoke-web" \
  --resource-group "rg-networking" \
  --vhub-name "hub-eastus" \
  --remote-vnet "/subscriptions/{sub-id}/resourceGroups/rg-spokes/providers/Microsoft.Network/virtualNetworks/vnet-spoke-web" \
  --internet-security true
```

The `--internet-security true` flag ensures that the spoke VNet receives the 0.0.0.0/0 default route when routing intent or a static default route is configured in the hub.

### List Hub Route Tables

```bash
az network vhub route-table list \
  --resource-group "rg-networking" \
  --vhub-name "hub-eastus" \
  --output table
```

## Reference

- Virtual WAN overview: https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-about
- Virtual WAN FAQ: https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-faq
- Hub settings: https://learn.microsoft.com/en-us/azure/virtual-wan/hub-settings
- Virtual WAN limits: https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#virtual-wan-limits

**Analysis only — verify against vendor documentation before applying.**
