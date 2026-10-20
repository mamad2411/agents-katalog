# Transit Design — Multi-Cloud Transit Architectures

## Overview

This skill covers the design and implementation of transit architectures that connect workloads across Azure, AWS, and GCP. Transit design encompasses VPN-based connectivity, colocation-based private interconnects, cloud-native interconnect services, and third-party transit fabrics. The goal is to select and implement the right architecture pattern based on bandwidth, latency, cost, and operational requirements.

## VPN Mesh Between Clouds

VPN mesh uses cloud-native VPN gateways to establish IPsec tunnels directly between providers over the public internet. Each cloud-to-cloud pair requires separate tunnel configuration.

### Azure VPN Gateway ↔ AWS VPN Gateway

```bash
# Azure: Create VPN Gateway
az network vnet-gateway create \
  --name azure-to-aws-vpngw \
  --resource-group multicloud-rg \
  --vnet multicloud-vnet \
  --gateway-type Vpn \
  --vpn-type RouteBased \
  --sku VpnGw2 \
  --generation Generation2 \
  --asn 65010

# Azure: Create Local Network Gateway (representing AWS)
az network local-gateway create \
  --name aws-lgw \
  --resource-group multicloud-rg \
  --gateway-ip-address <AWS_VPN_ENDPOINT_IP> \
  --asn 65020 \
  --bgp-peering-address <AWS_BGP_IP> \
  --local-address-prefixes 10.64.0.0/10

# Azure: Create connection
az network vpn-connection create \
  --name azure-to-aws \
  --resource-group multicloud-rg \
  --vnet-gateway1 azure-to-aws-vpngw \
  --local-gateway2 aws-lgw \
  --shared-key <PRE_SHARED_KEY> \
  --enable-bgp true
```

```bash
# AWS: Create Customer Gateway (representing Azure)
aws ec2 create-customer-gateway \
  --type ipsec.1 \
  --public-ip <AZURE_VPN_GW_PUBLIC_IP> \
  --bgp-asn 65010

# AWS: Create VPN Gateway and attach to VPC
aws ec2 create-vpn-gateway --type ipsec.1 --amazon-side-asn 65020
aws ec2 attach-vpn-gateway --vpn-gateway-id vgw-xxxx --vpc-id vpc-xxxx

# AWS: Create Site-to-Site VPN Connection
aws ec2 create-vpn-connection \
  --type ipsec.1 \
  --customer-gateway-id cgw-xxxx \
  --vpn-gateway-id vgw-xxxx \
  --options "{\"StaticRoutesOnly\":false}"
```

### GCP Cloud VPN ↔ Azure / AWS

```bash
# GCP: Create HA VPN Gateway
gcloud compute vpn-gateways create gcp-to-azure-vpngw \
  --network=multicloud-vpc \
  --region=us-east1

# GCP: Create Cloud Router with custom ASN
gcloud compute routers create multicloud-router \
  --network=multicloud-vpc \
  --region=us-east1 \
  --asn=65030

# GCP: Create VPN Tunnel
gcloud compute vpn-tunnels create gcp-to-azure-tunnel0 \
  --peer-gcp-gateway="" \
  --peer-external-gateway=azure-ext-gw \
  --peer-external-gateway-interface=0 \
  --region=us-east1 \
  --ike-version=2 \
  --shared-secret=<PRE_SHARED_KEY> \
  --router=multicloud-router \
  --vpn-gateway=gcp-to-azure-vpngw \
  --interface=0

# GCP: Configure BGP session on Cloud Router
gcloud compute routers add-bgp-peer multicloud-router \
  --peer-name=azure-bgp-peer \
  --peer-asn=65010 \
  --interface=gcp-to-azure-if0 \
  --peer-ip-address=169.254.21.1 \
  --region=us-east1
```

## Shared Colocation Facility Model

The colocation model uses a physical facility (Equinix, Megaport, CoreSite, Digital Realty) where multiple cloud provider circuits terminate. A cloud exchange fabric or customer-managed router cross-connects the circuits at Layer 2 or Layer 3.

### Megaport MCR (Megaport Cloud Router)

Megaport MCR is a virtual router hosted on Megaport's SDN fabric that provides Layer 3 routing between cloud on-ramps without requiring customer-owned hardware:

1. Provision an MCR instance in the target metro (e.g., Ashburn, Dallas)
2. Create a VXC (Virtual Cross Connect) from MCR to Azure ExpressRoute
3. Create a VXC from MCR to AWS Direct Connect (hosted connection)
4. Create a VXC from MCR to GCP Partner Interconnect
5. Configure BGP peering on each VXC interface
6. MCR performs route exchange between all connected clouds

### Equinix Fabric (Network Edge)

Equinix Fabric provides similar virtual interconnection with the option to deploy Network Edge virtual appliances (Cisco, Palo Alto, Fortinet) for advanced routing, inspection, and policy enforcement:

1. Deploy a Network Edge device (e.g., Cisco CSR 1000v) in the Equinix metro
2. Create connections from the device to Azure ExpressRoute, AWS Direct Connect, and GCP Interconnect
3. Configure BGP and route policies on the Network Edge device
4. Equinix Fabric handles the physical cross-connects

## Cloud-Native Interconnect Options by Pair

| Cloud Pair | Native Options | Notes |
|---|---|---|
| **Azure ↔ AWS** | No native interconnect — requires colocation, VPN, or third-party | Microsoft and AWS do not offer a direct peering product |
| **Azure ↔ GCP** | No native interconnect — requires colocation, VPN, or third-party | No direct peering product available |
| **AWS ↔ GCP** | No native interconnect — requires colocation, VPN, or third-party | Carrier interconnects available via partners |
| **Azure ↔ Oracle** | Azure-Oracle Interconnect (native, select regions) | Direct private connectivity, exception to the norm |

All major cloud-to-cloud paths (Azure-AWS, Azure-GCP, AWS-GCP) currently require either VPN, colocation cross-connect, or third-party fabric. No native direct peering product exists between any of the three major providers (except the Azure-Oracle interconnect).

## Third-Party Transit Fabrics

### Aviatrix Multi-Cloud Transit

Aviatrix deploys transit gateways (Aviatrix Controller + Gateways) in each cloud using native compute (Azure VM, EC2, GCE). The Controller orchestrates BGP, IPsec, and route propagation. High-Performance Encryption (HPE) achieves line-rate throughput by using multiple tunnels in parallel. Deployment uses Terraform:

```hcl
resource "aviatrix_transit_gateway" "azure_transit" {
  cloud_type   = 8    # Azure
  account_name = "azure-account"
  gw_name      = "azure-transit-gw"
  vpc_id       = "<vnet-name>:<rg-name>:<subscription-id>"
  vpc_reg      = "East US"
  gw_size      = "Standard_D3_v2"
  subnet       = "10.0.0.0/24"
  enable_active_mesh = true
}

resource "aviatrix_transit_gateway_peering" "azure_aws" {
  transit_gateway_name1 = aviatrix_transit_gateway.azure_transit.gw_name
  transit_gateway_name2 = aviatrix_transit_gateway.aws_transit.gw_name
}
```

### Alkira Cloud Exchange Platform (CXP)

Alkira provides a SaaS-based network infrastructure with virtual CXPs deployed in major metros. Connectivity is established by pointing cloud VNets/VPCs to Alkira CXPs via native VPN or dedicated connections. Alkira handles segmentation, firewall insertion, and multi-cloud routing through a policy-driven intent model.

### Prosimo Application Transit

Prosimo focuses on application-layer transit with App Transit Edges deployed in each cloud. It provides path optimization, WAN acceleration, and application-aware routing. Prosimo integrates with cloud-native constructs (Azure VNet peering, AWS Transit Gateway, GCP VPC peering) and adds an intelligent overlay for cross-cloud traffic.

## BGP Routing Across Clouds

### AS Number Planning

Assign unique private AS numbers (64512–65534 for 16-bit, or 4200000000–4294967294 for 32-bit) to each cloud environment:

| Environment | ASN | Purpose |
|---|---|---|
| Azure hub | 65010 | Azure transit/hub VNet |
| AWS hub | 65020 | AWS Transit Gateway |
| GCP hub | 65030 | GCP Cloud Router |
| On-premises | 65001 | Data center core |
| Colocation router | 65050 | Megaport MCR / Equinix NE |

### Route Filtering and Summarization

- Advertise summarized prefixes at cloud boundaries (e.g., 10.0.0.0/10 for all Azure, 10.64.0.0/10 for all AWS)
- Filter specific /24 and /28 prefixes to prevent route table bloat
- Use AS-path prepending to influence path selection for failover scenarios
- Implement prefix limits on BGP sessions to protect against route leaks

## Transit Architecture Patterns

**Hub-Spoke per Cloud with Cross-Cloud Backbone:** Each cloud has a hub VNet/VPC with spokes peered to it. Hubs connect cross-cloud via interconnect or VPN. This is the most common enterprise pattern — it mirrors each cloud's native hub-spoke model and adds cross-cloud links at the hub tier.

**Flat Mesh:** Every VNet/VPC connects directly to every other via peering or tunnels. Simple for small deployments (3–5 networks) but scales poorly — connection count grows as N×(N-1)/2.

**Hierarchical (Regional + Global):** Regional hubs aggregate traffic within a geographic area; global transit hubs connect regions. Suited for large multinational deployments with 10+ regions across clouds.

## Bandwidth and SLA Considerations

| Method | Bandwidth model | SLA | Typical Latency |
|---|---|---|---|
| Azure VPN Gateway | Throughput depends on gateway SKU, active-active design, and tunnel count; check current SKU limits before sizing | Gateway/SKU dependent | Variable (internet path) |
| AWS Site-to-Site VPN (standard tunnels) | Per-tunnel throughput is limited and workload-dependent; use ECMP across tunnels where supported | VPN SLA depends on endpoint redundancy | Variable (internet path) |
| AWS Site-to-Site VPN (Large Bandwidth Tunnel) | Higher per-tunnel bandwidth option where available; validate region, device, and feature support | VPN SLA depends on endpoint redundancy | Variable (internet path) |
| GCP HA VPN | Per-tunnel and aggregate throughput depend on HA VPN interfaces, Cloud Router, and ECMP | HA VPN SLA requires redundant tunnels/interfaces | Variable (internet path) |
| ExpressRoute (Standard) | Circuit bandwidth by provisioned SKU/port | 99.95%+ with proper redundancy | <2ms same metro |
| Direct Connect (dedicated) | 1–100 Gbps dedicated connections, with LAG for scale | Resiliency model dependent | <2ms same metro |
| GCP Dedicated Interconnect | 10/100 Gbps circuits; multiple VLAN attachments/circuits for scale | Up to 99.99% with redundant design | <2ms same metro |
| Megaport MCR | Bandwidth by selected virtual cross-connect/service size | Provider SLA | <1ms within metro |

When designing for production workloads, always provision redundant paths. Single-circuit designs do not meet the SLA thresholds published by any major cloud provider.

**Analysis only — verify against vendor documentation before applying.**
