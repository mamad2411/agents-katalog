# vwan_routing_intent — Routing Intent and Routing Policies

## Overview

Routing intent is a mechanism in Azure Virtual WAN that simplifies how traffic is steered through a security solution (Azure Firewall or a supported NVA) deployed in a secured virtual hub. Instead of manually configuring static routes, custom route tables, and UDRs on spoke VNets, routing intent uses declarative policies to automatically program the required routes across all connected resources.

Routing intent supports two independent policy types that can be enabled separately or together:

- **Internet Traffic Policy:** Routes 0.0.0.0/0 (default route) through the specified next-hop resource (Azure Firewall or NVA) for internet-bound traffic inspection.
- **Private Traffic Policy:** Routes private traffic between connected VNets, branches, VPN sites, and ExpressRoute circuits through the specified next-hop resource for east-west and hybrid inspection. Microsoft defines this by connected private destinations, not only RFC1918 aggregates; verify the current model: https://learn.microsoft.com/en-us/azure/virtual-wan/how-to-routing-policies.

## How Routing Intent Changes Effective Routes

When routing intent is enabled, the hub automatically injects routes into the effective route tables of all connected VNets, VPN connections, and ExpressRoute connections:

### Internet Traffic Policy Enabled

- All connected spoke VNets receive 0.0.0.0/0 with next hop = Azure Firewall or NVA in the hub
- Spoke VNets no longer break out to the internet directly; all internet traffic is forced through the hub security stack
- The hub advertises 0.0.0.0/0 to VPN and ExpressRoute connected branches (configurable)

### Private Traffic Policy Enabled

- Connected spoke, branch, VPN, and ExpressRoute private destinations are steered to Azure Firewall or the selected NVA
- Spoke-to-spoke traffic that previously routed directly through the hub router now transits through the firewall or NVA
- Branch-to-spoke, branch-to-branch, and hybrid private traffic are also routed through the security stack
- Effective routes are generated from the hub's connected and learned private prefixes; confirm behavior with `az network vhub get-effective-routes` before and after enabling the policy

### Both Policies Enabled

When both internet and private traffic policies are enabled simultaneously, all traffic — internet-bound, spoke-to-spoke, branch-to-spoke, and branch-to-branch — is inspected by the designated security resource. This is the recommended configuration for zero-trust network architectures.

## Inter-Hub Routing with Routing Intent

In multi-hub deployments where routing intent is enabled on both hubs:

- Traffic between spokes connected to different hubs is inspected by the firewall/NVA in **both** hubs (double inspection — source hub egress and destination hub ingress)
- The hub router exchanges connected and learned private prefixes between hubs, ensuring that inter-hub private traffic is also steered through the security stack
- Each hub independently enforces its own routing intent policies; there is no cross-hub policy inheritance

**Important:** Double firewall inspection in multi-hub scenarios can introduce latency and increase firewall processing costs. Consider this when designing multi-hub topologies with routing intent.

## Implications for Spoke-to-Spoke Traffic

Without routing intent, spoke-to-spoke traffic within the same hub routes directly through the hub router without inspection. With private traffic policy enabled:

- All spoke-to-spoke traffic is hair-pinned through the Azure Firewall or NVA
- Azure Firewall network rules and application rules apply to east-west flows
- Firewall logs capture all spoke-to-spoke traffic for auditing and compliance
- Throughput between spokes is constrained by the firewall's capacity (up to 30+ Gbps for Azure Firewall Premium)

## Default Route Injection (0.0.0.0/0)

When the internet traffic policy is enabled:

- The 0.0.0.0/0 route is automatically injected into all connected VNet route tables
- No manual UDR configuration is required on spoke subnets
- VNet connections must have the `internetSecurity` flag set to `true` (also called "Propagate Default Route") to receive the 0.0.0.0/0 route
- If `internetSecurity` is set to `false` on a VNet connection, that specific spoke will **not** receive the default route and will use its own internet path

## Private Traffic Destinations

The private traffic policy is not limited to the three RFC1918 ranges. Treat `PrivateTraffic` as the set of connected and learned private destinations for the vWAN hub, including VNet address spaces, branch prefixes, VPN sites, and ExpressRoute-advertised prefixes. If your environment uses non-RFC1918 ranges such as CGNAT or partner-owned private space, validate the generated effective routes instead of assuming static RFC1918-only behavior.

Before and after enabling routing intent, export hub effective routes and firewall logs to confirm that each intended private prefix is steered through the security resource.

## CLI Commands

### Enable Routing Intent with Both Policies

```bash
az network vhub routing-intent create \
  --name "routing-intent-eastus" \
  --resource-group "rg-networking" \
  --vhub "hub-eastus" \
  --routing-policies "[{name:InternetTraffic,destinations:[Internet],nextHop:/subscriptions/{sub-id}/resourceGroups/rg-networking/providers/Microsoft.Network/azureFirewalls/fw-hub-eastus},{name:PrivateTrafficPolicy,destinations:[PrivateTraffic],nextHop:/subscriptions/{sub-id}/resourceGroups/rg-networking/providers/Microsoft.Network/azureFirewalls/fw-hub-eastus}]"
```

### Show Current Routing Intent Configuration

```bash
az network vhub routing-intent show \
  --name "routing-intent-eastus" \
  --resource-group "rg-networking" \
  --vhub "hub-eastus" \
  --output json
```

### Update Routing Intent (Change Next Hop to NVA)

```bash
az network vhub routing-intent update \
  --name "routing-intent-eastus" \
  --resource-group "rg-networking" \
  --vhub "hub-eastus" \
  --routing-policies "[{name:InternetTraffic,destinations:[Internet],nextHop:/subscriptions/{sub-id}/resourceGroups/rg-networking/providers/Microsoft.Network/networkVirtualAppliances/nva-hub-eastus},{name:PrivateTrafficPolicy,destinations:[PrivateTraffic],nextHop:/subscriptions/{sub-id}/resourceGroups/rg-networking/providers/Microsoft.Network/networkVirtualAppliances/nva-hub-eastus}]"
```

### Delete Routing Intent

```bash
az network vhub routing-intent delete \
  --name "routing-intent-eastus" \
  --resource-group "rg-networking" \
  --vhub "hub-eastus" \
  --yes
```

## Common Pitfalls and Best Practices

1. **Forgetting `internetSecurity` on VNet connections:** If a spoke VNet connection has `internetSecurity` set to `false`, it will not receive the 0.0.0.0/0 default route even when routing intent is enabled. Always verify this flag on all VNet connections.

2. **Non-RFC1918 address space:** Do not assume behavior from address class alone. Validate that CGNAT, partner, or public-owned private-use prefixes appear in the hub effective routes and are steered through the intended security resource.

3. **Asymmetric routing with ExpressRoute:** When private traffic policy is enabled, return traffic from on-premises may bypass the firewall if ExpressRoute routes are more specific than the policy-generated private routes. Ensure consistent route advertisement from on-premises.

4. **Firewall capacity planning:** Enabling routing intent forces all traffic through the firewall. Size Azure Firewall or NVA capacity to handle the combined throughput of all spoke-to-spoke, branch-to-spoke, and internet traffic.

5. **Migration from custom route tables:** When enabling routing intent on an existing hub with custom route tables and static routes, routing intent takes precedence and may override existing configurations. Plan a maintenance window and validate effective routes after enabling.

6. **Inter-hub double inspection:** In multi-hub deployments, traffic between hubs is inspected twice. If this is undesirable, consider using custom route tables instead of routing intent for inter-hub flows.

## Reference

- Routing intent overview: https://learn.microsoft.com/en-us/azure/virtual-wan/how-to-routing-policies
- Virtual WAN routing: https://learn.microsoft.com/en-us/azure/virtual-wan/about-virtual-hub-routing

**Analysis only — verify against vendor documentation before applying.**
