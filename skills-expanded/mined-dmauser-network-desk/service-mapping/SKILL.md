# Service Mapping — Cross-Cloud Network Service Equivalency

## Overview

This skill provides detailed comparison tables mapping equivalent networking services across Azure, AWS, and GCP. Understanding the differences in scope, behavior, and configuration is critical when designing multi-cloud architectures. Each table highlights key distinctions that affect interoperability, migration planning, and consistent policy enforcement.

## Virtual Network

| Feature | Azure VNet | AWS VPC | GCP VPC |
|---|---|---|---|
| **Scope** | Regional (single region) | Regional (single region) | Global (spans all regions) |
| **Subnets** | Regional (span all AZs in region) | Zonal (one AZ per subnet) | Regional (span all zones in region) |
| **Secondary Ranges** | Not natively supported; use multiple address spaces | Not natively supported; use secondary CIDRs on VPC | Supported natively (alias IP ranges on subnets) |
| **Max CIDRs** | Multiple address spaces per VNet | Up to 5 CIDRs per VPC (adjustable) | Subnets define ranges; no VPC-level CIDR |
| **Peering** | VNet Peering (regional + global) | VPC Peering (intra/inter-region) | VPC Peering (global, within same org or cross-project) |
| **Transitive Routing** | Via Azure Virtual WAN, NVA, or Route Server | Via Transit Gateway (TGW) | Via HA VPN or NVA (no native transit peering) |
| **Max Subnets** | 3,000 per VNet | 200 per VPC (adjustable) | Varies by quota |

**Key Differences:** GCP's global VPC model is fundamentally different — a single VPC spans all regions, and subnets are regional. Azure and AWS VNets/VPCs are regional constructs requiring peering for cross-region connectivity. This affects multi-cloud designs: GCP workloads may live in one VPC with regional subnets while Azure/AWS require multiple VNets/VPCs connected via peering or transit hubs.

## Security Groups / Network ACLs

| Feature | Azure NSG | AWS Security Group | GCP Firewall Rule |
|---|---|---|---|
| **Statefulness** | Stateful | Stateful | Stateful (VPC firewall rules) |
| **Scope** | Attached to subnet or NIC | Attached to ENI (instance-level) | Applied to VPC (network-level) |
| **Rule Priority** | Explicit priority (100–4096) | No priority (all rules evaluated) | Explicit priority (0–65535) |
| **Default Deny** | Inbound: deny all; Outbound: allow all | Inbound: deny all; Outbound: allow all | Implied deny ingress; implied allow egress |
| **Deny Rules** | Supported | Not supported (allow-only) | Supported (allow and deny) |
| **Stateless Option** | Not available (NSGs are stateful only) | Network ACLs (stateless, subnet-level) | Hierarchical firewall policies (org-level) |
| **Tags/Targets** | ASG (Application Security Groups) | Security Group references | Network tags, service accounts |
| **Max Rules** | 1,000 per NSG | 60 inbound + 60 outbound per SG | Varies by quota |

**Key Differences:** AWS Security Groups are allow-only (no deny rules); use Network ACLs for deny rules. Azure NSGs support both allow and deny with explicit priority ordering. GCP firewall rules are VPC-wide and use target tags or service accounts for scoping — there is no per-instance firewall group attachment.

## Load Balancing

| Feature | Azure Load Balancer | AWS ALB / NLB | GCP Load Balancer |
|---|---|---|---|
| **L4 (TCP/UDP)** | Azure LB (Standard) | NLB (Network Load Balancer) | Network TCP/UDP LB (regional), TCP Proxy (global) |
| **L7 (HTTP/HTTPS)** | Application Gateway | ALB (Application Load Balancer) | HTTP(S) LB (global) |
| **Global L7** | Azure Front Door | CloudFront + ALB (not a single LB) | Global External HTTP(S) LB (single anycast VIP) |
| **Scope** | Regional (Standard LB) | Regional (ALB, NLB) | Regional or Global |
| **Cross-Region** | Azure Front Door, Traffic Manager | Global Accelerator + regional LBs | Global LB with multi-region NEGs |
| **WebSocket** | Application Gateway | ALB | HTTP(S) LB |
| **SSL Termination** | Application Gateway, Front Door | ALB | HTTP(S) LB, SSL Proxy LB |
| **Private (Internal)** | Internal LB (Standard) | Internal ALB / NLB | Internal TCP/UDP LB, Internal HTTP(S) LB |
| **Pricing Model** | Per rule + data processed | Per hour + LCU (ALB) / per hour + data (NLB) | Per rule + data processed (per-GB) |

**Key Differences:** GCP offers a truly global L7 load balancer with a single anycast VIP that routes to the nearest healthy backend worldwide — Azure and AWS require separate constructs (Front Door / CloudFront) for global distribution. AWS separates L4 (NLB) and L7 (ALB) more distinctly. Azure's Standard LB and Application Gateway serve different layers.

## Private Connectivity (Dedicated Circuits)

| Feature | Azure ExpressRoute | AWS Direct Connect | GCP Cloud Interconnect |
|---|---|---|---|
| **Port Speeds** | 1, 2, 5, 10, 100 Gbps | 1, 10, 100 Gbps (dedicated); 50 Mbps–10 Gbps (hosted) | 10, 100 Gbps (dedicated); 50 Mbps–50 Gbps (partner) |
| **SLA** | 99.95% (single circuit); 99.99% (ExpressRoute Direct, zone-redundant) | 99.99% (resiliency model with 2+ connections) | 99.99% (4-nines with redundant attachments) |
| **Pricing** | Port fee (monthly) + circuit fee (metered or unlimited) | Port-hour fee + data transfer out (per GB) | VLAN attachment fee + egress (per GB) |
| **Peering Types** | Private peering (VNets), Microsoft peering (M365, PaaS) | Private VIF (VPC), Public VIF, Transit VIF (TGW) | Private (VPC), Partner (via carrier) |
| **BGP** | Required (customer ASN + Microsoft ASN 12076) | Required (customer ASN + AWS ASN 7224/default) | Required (customer ASN + Google ASN 16550) |
| **Encryption** | MACsec (ExpressRoute Direct), IPsec over ER | MACsec (100 Gbps ports), site-to-site VPN over DX | HA VPN over Interconnect (IPsec) |
| **Global Reach** | ExpressRoute Global Reach (connect circuits across regions) | Not natively available | Not natively available |

**Key Differences:** Azure ExpressRoute offers Global Reach to connect two ExpressRoute circuits across regions without backhauling through on-premises — unique among the three providers. AWS Direct Connect has the most flexible hosting options with both dedicated and hosted connection types. GCP Dedicated Interconnect requires minimum 10 Gbps ports (use Partner Interconnect for smaller bandwidths).

## Private Endpoints / Private Connectivity to PaaS

| Feature | Azure Private Endpoint | AWS PrivateLink | GCP Private Service Connect |
|---|---|---|---|
| **Mechanism** | NIC injected into VNet subnet with private IP | ENI injected into VPC subnet with private IP | Forwarding rule with private IP in consumer VPC |
| **Supported Services** | 60+ Azure PaaS services (Storage, SQL, Cosmos DB, etc.) | AWS services + custom (NLB-backed) | Google APIs, published services (ILB-backed) |
| **Custom Services** | Private Link Service (Standard LB-backed) | PrivateLink Endpoint Service (NLB-backed) | Published services via ILB and service attachment |
| **DNS Integration** | Private DNS Zone auto-registration | Route 53 Resolver + PHZ | Service Directory or Cloud DNS response policies |
| **Cross-Account/Subscription** | Supported (approval workflow) | Supported (acceptance model) | Supported (connection acceptance) |
| **Cross-Region** | Supported (Global VNet Peering + Private Endpoint) | Regional interface endpoints; endpoint services can opt in to cross-Region access for consumers | Supported (global access flag) |
| **Pricing** | Per hour + data processed | Per hour + data processed per AZ | Per hour + data processed |

**Key Differences:** All three providers offer similar private connectivity models, but cross-region behavior varies. Azure can reach private endpoints over global VNet peering. GCP Private Service Connect supports global access when enabled. AWS interface endpoints remain regional, while providers of endpoint services can opt in to cross-Region PrivateLink access for consumers; validate service support, added latency, inter-region data charges, and feature limitations before using it.

## DNS

| Feature | Azure Private DNS | AWS Route 53 Resolver | GCP Cloud DNS |
|---|---|---|---|
| **Private Zones** | Azure Private DNS Zones (linked to VNets) | Route 53 Private Hosted Zones (associated with VPCs) | Cloud DNS Private Zones (bound to VPC networks) |
| **Conditional Forwarding** | DNS Private Resolver (inbound/outbound endpoints) | Route 53 Resolver (inbound/outbound endpoints) | Cloud DNS forwarding zones, DNS peering |
| **Hybrid DNS** | Private Resolver endpoints in VNet | Resolver endpoints in VPC | DNS server policies with inbound forwarding |
| **Cross-Cloud DNS** | Forward to on-prem/other cloud via Private Resolver outbound | Forward via Resolver outbound endpoints | Forward via DNS forwarding zones |
| **Auto-Registration** | Supported (VM hostnames auto-registered) | Not supported (use DHCP options or scripts) | Not supported (use GCE internal DNS) |
| **Max Zones** | 1,000 private zones per subscription | 500 private zones per account | Varies by quota |

**Key Differences:** Azure supports auto-registration of VM hostnames in Private DNS Zones, which is unique. For cross-cloud DNS resolution, all three require conditional forwarding via resolver endpoints or forwarding zones — traffic flows from one cloud's resolver to the target cloud's DNS endpoint over the private interconnect or VPN.

## Cloud Firewall

| Feature | Azure Firewall | AWS Network Firewall | GCP Cloud Firewall |
|---|---|---|---|
| **Type** | Managed, stateful (L3-L7) | Managed, stateful (L3-L7) | Distributed, stateful (L3-L4), plus L7 with IPS |
| **IDPS** | Premium SKU (signature-based) | Suricata-compatible rules | Intrusion Prevention Service (IPS, L7 inspection) |
| **FQDN Filtering** | Supported (application rules) | Supported (Suricata rules, domain lists) | Supported (FQDN objects in firewall policies) |
| **TLS Inspection** | Premium SKU | Supported | Supported (with Certificate Authority integration) |
| **Deployment** | Centralized in hub VNet (dedicated subnet) | Centralized in inspection VPC (firewall subnet) | Distributed (applied at VPC level, no dedicated subnet) |
| **Pricing** | Per hour (Standard/Premium) + data processed | Per hour (endpoint) + data processed | Per endpoint + data processed; or based on policy tier |
| **Throughput** | Up to 100 Gbps (Premium) | Up to 100 Gbps | Distributed — scales with VM/network throughput |
| **Policy Scope** | Firewall Policy (can span multiple firewalls via Firewall Manager) | Firewall Policy (per firewall) | Hierarchical policies (org → folder → project) |

**Key Differences:** GCP Cloud Firewall is fundamentally distributed — rules are enforced at the VM level across the entire VPC, not at a centralized chokepoint. Azure Firewall and AWS Network Firewall are centralized appliances deployed in dedicated subnets, requiring UDR/route table configuration to steer traffic through them. GCP's hierarchical firewall policies (at org/folder level) provide top-down policy enforcement that is unique among the three providers.

**Analysis only — verify against vendor documentation before applying.**
