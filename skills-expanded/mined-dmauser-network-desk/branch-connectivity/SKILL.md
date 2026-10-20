# vwan_branch_connectivity — Branch Connectivity (S2S VPN, P2S VPN, ExpressRoute)

## Overview

Azure Virtual WAN provides three primary mechanisms for connecting branch offices, remote users, and datacenters to the virtual hub: Site-to-Site (S2S) VPN for branch office IPsec connectivity, Point-to-Site (P2S) VPN for remote user access, and ExpressRoute for dedicated private circuits from co-locations and datacenters. Each mechanism is deployed as a gateway within the hub and scales independently using scale units.

## Site-to-Site VPN

### Protocol and Configuration

S2S VPN in vWAN uses IKEv2 for tunnel establishment with IPsec for data encryption. Each VPN site represents a branch location and can have up to 4 links (for multi-ISP or active-active configurations).

Key capabilities:

- **IKEv2 protocol:** Main mode negotiation with support for DPD (Dead Peer Detection)
- **BGP support:** Dynamic route exchange between branch CPE and hub VPN gateway. The hub VPN gateway uses AS 65515 for BGP peering with VPN sites (distinct from the hub router's AS 65520)
- **Scale units:** 1 to 20+ scale units per hub. Each scale unit provides 500 Mbps aggregate throughput. At 20 units, the gateway supports 10 Gbps aggregate across all tunnels
- **Custom IPsec/IKE policies:** Override default proposals with specific algorithms per connection

Default IPsec/IKE parameters:

| Parameter | Phase 1 (IKE) | Phase 2 (IPsec) |
|-----------|---------------|-----------------|
| Encryption | AES256 | AES256 |
| Integrity | SHA256 | SHA256 |
| DH Group | DHGroup14 | DHGroup14 |
| SA Lifetime | 28800 seconds | 3600 seconds |

### Auto-Connect for VPN Sites

vWAN supports auto-connect functionality where VPN sites created through an SD-WAN partner orchestrator (Cisco vManage, VMware Orchestrator, Fortinet FortiManager) are automatically connected to the nearest hub based on geographic proximity. The partner API handles:

- VPN site creation with branch IP and link information
- IPsec tunnel establishment to the hub VPN gateway
- BGP session activation for dynamic routing
- Hub assignment based on branch location metadata

### CLI Commands — S2S VPN

```bash
# Create a VPN gateway in the hub
az network vpn-gateway create \
  --name "vpn-gw-eastus" \
  --resource-group "rg-networking" \
  --vhub "hub-eastus" \
  --location "eastus" \
  --scale-unit 2

# Create a VPN site representing a branch
az network vpn-site create \
  --name "branch-newyork" \
  --resource-group "rg-networking" \
  --location "eastus" \
  --virtual-wan "contoso-vwan" \
  --ip-address "203.0.113.10" \
  --address-prefixes "10.200.0.0/24" \
  --device-vendor "Cisco" \
  --device-model "ISR4451" \
  --link-speed 100 \
  --bgp-peering-address "10.200.0.1" \
  --asn 65010

# Connect the VPN site to the hub gateway
az network vpn-gateway connection create \
  --name "conn-branch-newyork" \
  --resource-group "rg-networking" \
  --gateway-name "vpn-gw-eastus" \
  --remote-vpn-site "/subscriptions/{sub-id}/resourceGroups/rg-networking/providers/Microsoft.Network/vpnSites/branch-newyork" \
  --enable-bgp true \
  --protocol-type IKEv2

# Apply custom IPsec policy to a connection
az network vpn-gateway connection ipsec-policy add \
  --resource-group "rg-networking" \
  --gateway-name "vpn-gw-eastus" \
  --connection-name "conn-branch-newyork" \
  --ike-encryption AES256 \
  --ike-integrity SHA384 \
  --dh-group DHGroup14 \
  --ipsec-encryption GCMAES256 \
  --ipsec-integrity GCMAES256 \
  --pfs-group PFS14 \
  --sa-lifetime 3600 \
  --sa-data-size 102400000
```

## Point-to-Site VPN

### Protocols and Authentication

P2S VPN in vWAN provides remote user connectivity with support for multiple tunnel protocols and authentication methods:

**Supported protocols:**

- **OpenVPN (TCP/UDP 443):** Recommended for most deployments. Supports all OS platforms, traverses most firewalls.
- **IKEv2:** Native support on Windows 10+, macOS, iOS. Better performance than OpenVPN but may be blocked by corporate firewalls.
- **SSTP (TCP 443):** Windows-only, legacy support. Use OpenVPN for new deployments.

**Authentication methods:**

- **Azure AD (Entra ID):** Recommended for enterprise deployments. Supports MFA, Conditional Access, and user/group-based authorization. Requires OpenVPN protocol.
- **Certificate-based:** Mutual TLS authentication with client certificates. Supports all protocols. Suitable for device authentication scenarios.
- **RADIUS:** Delegates authentication to an external RADIUS server (e.g., NPS, FreeRADIUS). Supports EAP-MSCHAPv2, EAP-TLS. Useful for integrating with existing identity infrastructure.

### CLI Commands — P2S VPN

```bash
# Create a P2S VPN server configuration
az network p2s-vpn-gateway create \
  --name "p2s-gw-eastus" \
  --resource-group "rg-networking" \
  --vhub "hub-eastus" \
  --location "eastus" \
  --scale-unit 2 \
  --vpn-server-config "p2s-config-aad" \
  --address-space "172.30.0.0/16"

# Download the P2S VPN client profile
az network p2s-vpn-gateway vpn-client generate \
  --name "p2s-gw-eastus" \
  --resource-group "rg-networking" \
  --authentication-method EAPTLS
```

## ExpressRoute

### Circuit Association and Route Propagation

ExpressRoute provides private, dedicated connectivity from on-premises networks to Azure through an ExpressRoute circuit provisioned via a connectivity provider. In vWAN, ExpressRoute circuits are associated with the hub's ExpressRoute gateway.

Key integration points:

- **Circuit association:** ExpressRoute circuits are linked to the hub via an authorization key (cross-subscription) or directly (same subscription)
- **Route propagation:** On-premises routes learned via ExpressRoute BGP peering are propagated to the hub route table and further to all connected VNets and VPN branches
- **Peering configuration:** Private peering is required; Microsoft peering is used for Office 365/Dynamics 365 traffic
- **ExpressRoute Global Reach:** Enables branch-to-branch routing directly over ExpressRoute circuits without traversing the hub VPN gateway. Traffic stays on the Microsoft backbone.

### CLI Commands — ExpressRoute

```bash
# Create an ExpressRoute gateway in the hub
az network express-route gateway create \
  --name "er-gw-eastus" \
  --resource-group "rg-networking" \
  --vhub "hub-eastus" \
  --location "eastus" \
  --min-val 2

# Connect an ExpressRoute circuit to the hub
az network express-route gateway connection create \
  --name "conn-er-datacenter" \
  --resource-group "rg-networking" \
  --gateway-name "er-gw-eastus" \
  --peering "/subscriptions/{sub-id}/resourceGroups/rg-er/providers/Microsoft.Network/expressRouteCircuits/er-circuit-datacenter/peerings/AzurePrivatePeering" \
  --authorization-key "{auth-key}"
```

## Branch-to-Branch Routing

In Standard tier, branch-to-branch routing is enabled by default. Traffic between VPN-connected branches routes through the hub. Traffic between ExpressRoute-connected sites can use Global Reach for direct paths or transit through the hub.

When routing intent private traffic policy is active, branch-to-branch traffic also transits through the Azure Firewall or NVA for inspection.

## Scale and Performance Considerations

| Component | Scale Unit Range | Throughput per Unit | Maximum Aggregate |
|-----------|-----------------|--------------------|--------------------|
| S2S VPN Gateway | 1–20 | 500 Mbps | 10 Gbps |
| P2S VPN Gateway | 1–20 | 500 Mbps | 10 Gbps (100K users) |
| ExpressRoute Gateway | 1–10 | 2 Gbps | 20 Gbps |

Size gateways based on peak aggregate throughput across all connections, not individual tunnel bandwidth. Plan for 20–30% headroom above expected peak traffic to accommodate bursts and growth.

## Reference

- S2S VPN in vWAN: https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-site-to-site-portal
- P2S VPN in vWAN: https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-point-to-site-portal
- ExpressRoute in vWAN: https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-expressroute-portal

**Analysis only — verify against vendor documentation before applying.**
