# Skill: ExpressRoute / Direct Connect / Cloud Interconnect Design (hyb_expressroute-design)

Design dedicated private connectivity between on-premises networks and cloud environments using Azure ExpressRoute, AWS Direct Connect, and GCP Cloud Interconnect. This skill covers circuit provisioning, peering configuration, redundancy patterns, and advanced features.

---

## Azure ExpressRoute

### Circuit Architecture
An ExpressRoute circuit represents a logical connection between on-premises infrastructure and Microsoft cloud services through a connectivity provider at a peering location (meet-me facility). Each circuit consists of two physical cross-connections (primary and secondary) for redundancy.

**Circuit Bandwidth Options**: 50 Mbps, 100 Mbps, 200 Mbps, 500 Mbps, 1 Gbps, 2 Gbps, 5 Gbps, 10 Gbps.

**SKUs**:
- **Standard**: Connect to VNets in the same geopolitical region as the peering location.
- **Premium**: Connect to VNets in any Azure region worldwide. Increased route limits (10,000 routes for private peering vs 4,000 for Standard).

**Billing Models**:
- **Metered**: Per-GB egress charge (ingress free). Suitable for variable workloads.
- **Unlimited**: Flat monthly fee regardless of egress volume. Cost-effective above ~10 TB/month egress.

### Peering Types

**Private Peering**:
- Connects on-premises networks to Azure VNets. BGP session between on-premises edge router (customer/provider ASN) and Microsoft Enterprise Edge routers (MSEE, ASN 12076).
- Requires two /30 or /126 subnets for BGP peering (primary and secondary links).
- Advertise on-premises routes to Azure; learn VNet address spaces from Azure.
- Route limit: 4,000 prefixes (Standard) or 10,000 prefixes (Premium).

**Microsoft Peering**:
- Connects to Microsoft 365, Dynamics 365, and Azure PaaS services via public IPs.
- Requires public IP prefixes owned by the customer or provider (registered in RIR).
- Route filters control which Microsoft service communities are advertised (e.g., Exchange Online, SharePoint Online, Azure Storage in specific regions).
- NAT required — Microsoft services see traffic from the customer's public IP pool.

### Advanced Features

**ExpressRoute Global Reach**: Enables data transfer between on-premises sites through two ExpressRoute circuits via Microsoft's backbone. Useful for inter-site connectivity without MPLS or internet VPN. Available in supported peering locations.

**FastPath**: Bypasses the ExpressRoute virtual network gateway for data-path traffic, sending packets directly from the MSEE to the VNet VM. Reduces latency. Support for VNet peering and user-defined routes depends on circuit type and documented constraints; verify the current FastPath matrix before relying on peering or UDR behavior: https://learn.microsoft.com/en-us/azure/expressroute/about-fastpath.

| Circuit type | VNet peering with FastPath | UDR support with FastPath | Guidance |
|--------------|----------------------------|---------------------------|----------|
| ExpressRoute Direct | Supported under documented constraints | Supported under documented constraints | Validate gateway, route table, and NVA constraints in the current FastPath docs. |
| Provider-provisioned ExpressRoute | Verify current support before design | Verify current support before design | Do not assume ExpressRoute Direct behavior applies to partner/provisioned circuits. |

**ExpressRoute Direct**: Provides 10 Gbps or 100 Gbps physical port pairs directly into Microsoft's peering edge. Enables MACsec (802.1AE) encryption on the physical link. Supports multiple ExpressRoute circuits on the same Direct port pair with flexible bandwidth allocation. Required for circuits > 10 Gbps.

### Provisioning Commands
```bash
# Create ExpressRoute circuit
az network express-route create \
  --name MyERCircuit \
  --resource-group MyRG \
  --bandwidth 1000 \
  --peering-location "Silicon Valley" \
  --provider "Equinix" \
  --sku-family MeteredData \
  --sku-tier Premium

# Configure Private Peering
az network express-route peering create \
  --circuit-name MyERCircuit \
  --resource-group MyRG \
  --peering-type AzurePrivatePeering \
  --peer-asn 65001 \
  --primary-peer-subnet 10.0.0.0/30 \
  --secondary-peer-subnet 10.0.0.4/30 \
  --vlan-id 100
```

---

## AWS Direct Connect

### Connection Types

**Dedicated Connection**: Physical port (1 Gbps, 10 Gbps, or 100 Gbps) at an AWS Direct Connect location. Customer manages the cross-connect to their router or colocated equipment. Lead time: typically 2–4 weeks.

**Hosted Connection**: Sub-rate connection provisioned by an AWS Direct Connect Partner. Available bandwidths vary by partner and region, including higher options where supported; verify current hosted connection speeds in the AWS Direct Connect documentation before sizing: https://docs.aws.amazon.com/directconnect/latest/UserGuide/hosted_connection.html.

### Virtual Interfaces (VIFs)

**Private VIF**: Connects to a VPC via a Virtual Private Gateway (VGW) or Direct Connect Gateway. BGP session with Amazon's router (ASN 7224 by default). Supports 802.1Q VLAN tagging. One private VIF per VPC (via VGW) or multiple VPCs (via Direct Connect Gateway).

**Public VIF**: Connects to AWS public services (S3, DynamoDB, EC2 public IPs) via Amazon's public IP space. BGP session advertises Amazon's public prefixes. Customer must advertise their own public prefixes (or Amazon-provided prefixes).

**Transit VIF**: Connects to one or more Transit Gateways via a Direct Connect Gateway. Enables connectivity to multiple VPCs and other Transit Gateway attachments. Supports up to 3 Transit Gateways per Direct Connect Gateway. Limited to 100 route prefixes advertised from AWS.

### Link Aggregation Groups (LAGs)
Bundle multiple dedicated connections (same bandwidth, same location) into a single logical connection using LACP (802.3ad). Minimum links threshold configurable — if active links drop below threshold, the entire LAG goes down.

### Direct Connect Gateway
A globally available resource that enables connectivity to VPCs in any AWS region (excluding China). Associates with VGWs (for private VIFs) or Transit Gateways (for transit VIFs). Supports up to 10 VGW associations and 3 Transit Gateway associations.

### Configuration Commands
```bash
# Create Direct Connect Gateway
aws directconnect create-direct-connect-gateway \
  --direct-connect-gateway-name MyDCGateway \
  --amazon-side-asn 64512

# Create Private VIF
aws directconnect create-private-virtual-interface \
  --connection-id dxcon-xxxx \
  --new-private-virtual-interface '{
    "virtualInterfaceName": "MyPrivateVIF",
    "vlan": 100,
    "asn": 65001,
    "authKey": "MyBGPKey",
    "amazonAddress": "169.254.100.1/30",
    "customerAddress": "169.254.100.2/30",
    "directConnectGatewayId": "dxgw-xxxx"
  }'
```

---

## GCP Cloud Interconnect

### Dedicated Interconnect
Physical 10 Gbps or 100 Gbps connections at GCP colocation facilities. Customer provisions cross-connects between their router and Google's peering edge. Supports up to 8 connections per interconnect for link aggregation (LACP). SLA: 99.9% with single interconnect, 99.99% with recommended topology (4 connections across 2 metro areas).

### Partner Interconnect
Connections through a Google Cloud Partner (50 Mbps to 50 Gbps). Partner handles the physical connectivity to Google. Suitable when the customer's data center is not at a GCP colocation facility or when lower bandwidth is sufficient.

### VLAN Attachments
Connect an interconnect (Dedicated or Partner) to a VPC network via Cloud Router. Each VLAN attachment is assigned a VLAN ID and creates a BGP session with the Cloud Router. Multiple VLAN attachments can share a single interconnect.

### MED-Based Routing
GCP uses Multi-Exit Discriminator (MED) for inbound traffic engineering on Cloud Interconnect:
- Cloud Router advertises VPC subnets with MED values based on the region of the VPC subnet relative to the interconnect location.
- Local region subnets: MED = 100 (preferred)
- Remote region subnets: MED = 200+ (based on inter-region distance)
- On-premises routers should honor MED to route traffic to the nearest interconnect.

### Configuration Commands
```bash
# Create VLAN attachment for Dedicated Interconnect
gcloud compute interconnects attachments dedicated create my-attachment \
  --interconnect=my-interconnect \
  --router=my-cloud-router \
  --region=us-central1 \
  --bandwidth=1g \
  --vlan=100

# Verify BGP session status
gcloud compute routers get-status my-cloud-router \
  --region=us-central1
```

---

## Circuit Sizing and Redundancy Patterns

### Sizing Guidelines
- Measure current bandwidth usage (95th percentile, peak, and average) for 30 days.
- Add 40% headroom for growth and burst absorption.
- Consider protocol overhead: Ethernet (14 bytes), IP (20 bytes), TCP (20 bytes) headers reduce usable throughput.
- Account for bidirectional traffic — most circuits are symmetric but workloads may be asymmetric.

### Redundancy Patterns

**Dual Circuits — Same Provider, Different Peering Locations**:
- Active-active or active-passive. Provides resilience against peering location failure.
- Use BGP local preference to define primary/secondary paths.

**Dual Circuits — Diverse Providers**:
- Maximum resilience against provider outages. Higher cost and complexity.
- Ensure diverse physical paths (different fiber routes, different meet-me rooms).

**ExpressRoute + VPN Backup**:
- ExpressRoute as primary (BGP LP 200), S2S VPN as backup (BGP LP 100).
- VPN provides encrypted backup over internet with automatic failover via BGP.
- Azure supports this natively — VPN Gateway and ExpressRoute Gateway can coexist in the same VNet.

**Analysis only — verify against vendor documentation before applying.**
