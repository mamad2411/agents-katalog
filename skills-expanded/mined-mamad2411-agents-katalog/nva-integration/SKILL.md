# vwan_nva_integration — NVA and SD-WAN Integration in Virtual WAN

## Overview

Azure Virtual WAN supports deploying Network Virtual Appliances (NVAs) directly inside the virtual hub, enabling inline traffic inspection, SD-WAN termination, and advanced network services without requiring separate spoke VNets for appliance hosting. NVAs in the hub integrate with the hub router via BGP peering and participate in the vWAN routing fabric as first-class next hops.

## Deployment Models

### Managed NVA (Marketplace Deployment)

Managed NVAs are deployed from the Azure Marketplace directly into the vWAN hub. The NVA vendor provides the VM images, and Azure manages the underlying infrastructure (placement, networking, high availability). The user configures the appliance through the vendor's management plane.

Key characteristics:

- Deployed as a managed resource within the hub — no user-managed VNet or subnet required
- Automatic integration with the hub router for route exchange
- Infrastructure units control appliance scaling (CPU, memory, throughput)
- Vendor-managed software updates and patching through the vendor's orchestrator
- Azure manages compute placement and high availability across availability zones

### Bring-Your-Own NVA (Spoke-Based)

For vendors or appliance versions not yet supported as managed NVAs in the hub, deploy the NVA in a dedicated spoke VNet and establish BGP peering with the hub router through the VNet connection.

Key characteristics:

- NVA runs in a standard spoke VNet with user-managed NICs and subnets
- BGP peering is configured between the NVA and the hub router over the VNet connection
- User manages VM sizing, availability sets/zones, and software lifecycle
- Requires UDRs or routing intent to steer traffic to the NVA spoke
- More operational overhead but supports any BGP-capable appliance

## BGP Peering with the Hub Router

The vWAN hub router operates under **AS 65520** (reserved, non-configurable). NVAs establish eBGP peering with the hub router to exchange routes dynamically.

BGP peering details:

- **Hub router ASN:** 65520 (fixed for all vWAN hubs)
- **Hub router peering IPs:** Two IPs from the hub address space, exposed via the hub's BGP peer configuration
- **NVA ASN:** Any valid private ASN (64512–65534, 4200000000–4294967294) except 65520
- **Peering type:** eBGP multihop (TTL typically set to 2–3 hops for managed NVA)
- **Route exchange:** The NVA advertises branch/on-premises prefixes to the hub; the hub advertises spoke VNet and other branch prefixes to the NVA

```bash
# Retrieve hub router BGP peer information
az network vhub show \
  --name "hub-eastus" \
  --resource-group "rg-networking" \
  --query "virtualRouterAsn,virtualRouterIps" \
  --output json
```

Expected output:
```json
{
  "virtualRouterAsn": 65520,
  "virtualRouterIps": ["10.100.0.68", "10.100.0.69"]
}
```

## Supported Managed NVA Vendors

| Vendor | Product | Use Case |
|--------|---------|----------|
| **Barracuda Networks** | CloudGen WAN | SD-WAN + NGFW unified appliance in hub |
| **Cisco Systems** | Catalyst 8000v (Viptela) | Enterprise SD-WAN with vManage orchestration |
| **Fortinet** | FortiGate Next-Gen Firewall | SD-WAN + NGFW with FortiManager integration |
| **VMware (Broadcom)** | SD-WAN (VeloCloud) | SD-WAN with VMware Orchestrator |
| **Versa Networks** | Versa SD-WAN | Multi-tenant SD-WAN with Versa Director |
| **Citrix** | Citrix SD-WAN | Application-aware SD-WAN with Citrix Orchestrator |

Vendor documentation and integration guides:

- Barracuda: https://campus.barracuda.com/product/cloudgenwan/
- Cisco Catalyst SD-WAN: https://www.cisco.com/c/en/us/solutions/enterprise-networks/sd-wan/index.html
- Fortinet SD-WAN: https://docs.fortinet.com/product/sd-wan/
- VMware SD-WAN: https://docs.vmware.com/en/VMware-SD-WAN/
- Versa Networks: https://docs.versa-networks.com/
- Citrix SD-WAN: https://docs.citrix.com/en-us/citrix-sd-wan/

## Custom NVA IP Ranges in the Hub

When a managed NVA is deployed, it consumes IP addresses from a dedicated NVA subnet within the hub address space. This range is automatically carved from the hub's address prefix. Ensure the hub address space is large enough (recommended /23 or larger) to accommodate:

- Hub router infrastructure IPs
- VPN gateway IPs
- ExpressRoute gateway IPs
- NVA instance IPs (varies by infrastructure units — more units = more IPs)
- Azure Firewall subnet (if co-deployed — note: co-deployment of Azure Firewall and NVA has specific constraints)

## NVA Infrastructure Units and Scaling

Managed NVAs scale using infrastructure units. Each infrastructure unit provides a defined amount of compute (vCPUs, memory) and network throughput:

- **Minimum deployment:** 2 infrastructure units (for high availability — active-active across two instances)
- **Maximum deployment:** Vendor-dependent, typically up to 80 infrastructure units
- **Scaling:** Infrastructure units can be adjusted post-deployment to increase throughput
- **Throughput per unit:** Varies by vendor — typically 500 Mbps to 1 Gbps per unit (consult vendor datasheets)

## CLI Commands

### Deploy a Managed NVA in the Hub

```bash
az network virtual-appliance create \
  --name "nva-fortinet-eastus" \
  --resource-group "rg-networking" \
  --vhub "/subscriptions/{sub-id}/resourceGroups/rg-networking/providers/Microsoft.Network/virtualHubs/hub-eastus" \
  --vendor "fortinet" \
  --bundled-scale-unit "4" \
  --market-place-version "7.2.0" \
  --boot-strap-configuration-blobs "https://storageaccount.blob.core.windows.net/config/bootstrap.conf" \
  --cloud-init-configuration-blobs "https://storageaccount.blob.core.windows.net/config/cloud-init.txt"
```

### List NVAs in a Hub

```bash
az network virtual-appliance list \
  --resource-group "rg-networking" \
  --output table
```

### Show NVA Details

```bash
az network virtual-appliance show \
  --name "nva-fortinet-eastus" \
  --resource-group "rg-networking" \
  --output json
```

### Update NVA Scale Units

```bash
az network virtual-appliance update \
  --name "nva-fortinet-eastus" \
  --resource-group "rg-networking" \
  --bundled-scale-unit "8"
```

### Create BGP Connection for Spoke-Based NVA

```bash
az network vhub bgpconnection create \
  --name "bgp-to-spoke-nva" \
  --resource-group "rg-networking" \
  --vhub-name "hub-eastus" \
  --peer-asn 65001 \
  --peer-ip "10.50.1.4" \
  --vhub-conn "/subscriptions/{sub-id}/resourceGroups/rg-networking/providers/Microsoft.Network/virtualHubs/hub-eastus/hubVirtualNetworkConnections/conn-spoke-nva"
```

### List BGP Connections

```bash
az network vhub bgpconnection list \
  --resource-group "rg-networking" \
  --vhub-name "hub-eastus" \
  --output table
```

## Routing Traffic Through the NVA

To steer traffic through a managed NVA, use one of these approaches:

1. **Routing Intent (recommended):** Configure routing intent with the NVA as the next hop for internet and/or private traffic policies. This automatically programs routes in all connected VNets and branches.

2. **Static routes in hub route table:** Add static routes in the hub's default route table pointing to the NVA's IP as the next hop for specific prefixes.

3. **BGP route advertisement:** The NVA advertises more-specific routes to the hub router via BGP, attracting traffic from spokes and branches.

## Reference

- NVA in vWAN hub: https://learn.microsoft.com/en-us/azure/virtual-wan/about-nva-hub
- Deploy NVA in hub: https://learn.microsoft.com/en-us/azure/virtual-wan/how-to-nva-hub
- BGP peering with hub: https://learn.microsoft.com/en-us/azure/virtual-wan/create-bgp-peering-hub-portal

**Analysis only — verify against vendor documentation before applying.**
