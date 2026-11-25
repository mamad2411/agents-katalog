# Skill: Hub-Spoke Topology Design

## Purpose

This skill provides expert guidance on designing hub-spoke network topologies across Azure, AWS, and GCP. It covers topology selection, shared service placement in the hub, spoke-to-spoke communication patterns, transit routing, and decision criteria for choosing between hub-spoke, mesh, and managed transit services.

## Core Knowledge

### Hub-Spoke Architecture Fundamentals

The hub-spoke model centralizes shared network services (firewall, DNS, bastion, monitoring) in a "hub" network while workloads reside in isolated "spoke" networks. All inter-spoke and egress traffic routes through the hub, enabling centralized security inspection and policy enforcement.

**When to use hub-spoke:**
- Centralized egress/ingress control is required (compliance, cost optimization)
- Multiple workload teams need network isolation from each other
- Shared services (firewall, DNS forwarder, jump boxes) serve all workloads
- Route summarization at the hub simplifies on-premises route advertisements

**When NOT to use hub-spoke:**
- Fewer than 3 VNets/VPCs (overhead exceeds benefit)
- Ultra-low latency spoke-to-spoke traffic where the hub hop is unacceptable
- Workloads that are entirely independent with no shared services

### Cloud-Specific Implementations

#### Azure: Hub-Spoke with VNet Peering

```
Hub VNet (10.0.0.0/16)
├── AzureFirewallSubnet (10.0.1.0/26)         ← Azure Firewall or NVA
├── GatewaySubnet (10.0.255.0/27)              ← VPN/ExpressRoute Gateway
├── AzureBastionSubnet (10.0.2.0/26)           ← Bastion host
├── DnsResolverInbound (10.0.3.0/28)           ← Private DNS Resolver
└── SharedServices (10.0.10.0/24)              ← Domain controllers, monitoring

Spoke-Prod VNet (10.1.0.0/16) ←── peered ──→ Hub
Spoke-Dev VNet (10.2.0.0/16)  ←── peered ──→ Hub
```

**Key settings for Azure peering in hub-spoke:**
```bash
# Spoke-to-Hub peering (on the spoke side)
az network vnet peering create \
  --name spoke-to-hub \
  --resource-group spoke-rg \
  --vnet-name spoke-vnet \
  --remote-vnet /subscriptions/.../hub-vnet \
  --allow-forwarded-traffic true \
  --use-remote-gateways true          # Use hub's VPN/ER gateway

# Hub-to-Spoke peering (on the hub side)
az network vnet peering create \
  --name hub-to-spoke \
  --resource-group hub-rg \
  --vnet-name hub-vnet \
  --remote-vnet /subscriptions/.../spoke-vnet \
  --allow-forwarded-traffic true \
  --allow-gateway-transit true         # Share gateway with spokes
```

**Spoke-to-spoke via hub firewall** — Requires UDR on each spoke subnet pointing 0.0.0.0/0 (or the other spoke's CIDR) to the Azure Firewall's private IP:
```bash
az network route-table route create \
  --resource-group spoke-rg \
  --route-table-name spoke-rt \
  --name to-other-spokes \
  --address-prefix 10.0.0.0/8 \
  --next-hop-type VirtualAppliance \
  --next-hop-ip-address 10.0.1.4      # Azure Firewall private IP
```

#### AWS: Hub-Spoke with Transit Gateway

AWS VPC peering is non-transitive, making Transit Gateway (TGW) the standard hub-spoke building block:

```
Transit Gateway (TGW)
├── Attachment: Hub VPC (10.0.0.0/16) — shared services, NAT, firewall
├── Attachment: Prod VPC (10.1.0.0/16)
├── Attachment: Dev VPC (10.2.0.0/16)
└── Attachment: VPN/Direct Connect
```

```bash
# Create Transit Gateway
aws ec2 create-transit-gateway \
  --description "Hub TGW" \
  --options DefaultRouteTableAssociation=enable,DefaultRouteTablePropagation=enable

# Attach a VPC
aws ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id tgw-abc123 \
  --vpc-id vpc-spoke1 \
  --subnet-ids subnet-az1 subnet-az2
```

**Spoke isolation with TGW route tables:** Create separate route tables for prod vs dev to prevent cross-environment traffic:
```bash
aws ec2 create-transit-gateway-route-table \
  --transit-gateway-id tgw-abc123 \
  --tags Key=Name,Value=prod-rt

# Associate prod VPC attachment to prod route table
aws ec2 associate-transit-gateway-route-table \
  --transit-gateway-route-table-id tgw-rtb-prod \
  --transit-gateway-attachment-id tgw-attach-prod
```

#### GCP: Hub-Spoke with Shared VPC or VPC Peering

GCP offers two hub-spoke models:

**Shared VPC (recommended for organizations):** A host project owns the VPC; service projects attach workloads to subnets in the shared VPC. No peering needed — it's a single network.

```bash
# Enable Shared VPC on host project
gcloud compute shared-vpc enable host-project-id

# Associate service project
gcloud compute shared-vpc associated-projects add service-project-id \
  --host-project host-project-id
```

**VPC Network Peering:** For independent VPCs that need connectivity. Subnet routes exchange automatically; custom/dynamic routes require explicit import/export.

```bash
gcloud compute networks peerings create hub-to-spoke \
  --network hub-vpc \
  --peer-network spoke-vpc \
  --peer-project spoke-project \
  --export-custom-routes \
  --import-custom-routes
```

### Shared Services Placement in the Hub

| Service | Hub Subnet | Sizing | Notes |
|---------|-----------|--------|-------|
| Firewall / NVA | Dedicated (e.g., AzureFirewallSubnet) | /26 minimum (Azure Firewall requirement) | All spoke traffic routes through firewall via UDR |
| VPN/ER Gateway | GatewaySubnet (Azure) or dedicated VPC (AWS) | /27 minimum (Azure) | Enables on-prem connectivity shared with spokes |
| Bastion / Jump Box | Dedicated subnet | /26 (Azure Bastion) or /28 | Secure RDP/SSH without public IPs on spokes |
| DNS Resolver | Dedicated subnet | /28 | Private DNS resolution for on-prem ↔ cloud |
| Monitoring agents | SharedServices subnet | /24 | Prometheus, Grafana, Log Analytics forwarders |
| DevOps agents | SharedServices subnet | /24 | Self-hosted build agents, runners |

### Spoke-to-Spoke Communication Patterns

| Pattern | How It Works | Latency | Security | Use When |
|---------|-------------|---------|----------|----------|
| Via hub firewall/NVA | UDRs route spoke traffic to hub firewall → firewall forwards to destination spoke | +2–5ms (hub hop) | Full L3/L7 inspection | Default — security inspection required |
| Direct VNet peering | Additional peering between spokes (bypasses hub) | Minimal | No centralized inspection | Low-latency, trusted spoke pairs |
| Azure Virtual WAN | Managed hub with automatic spoke-to-spoke routing | ~same as peering | Depends on secured hub config | 50+ VNets, global scale |
| AWS TGW | All spokes attached to TGW; route tables control paths | +0.5–1ms per hop | TGW + firewall appliance VPC | AWS standard pattern |

### Transit Routing Considerations

1. **Azure:** VNet peering is non-transitive. Spoke A cannot reach Spoke B through the hub unless a firewall/NVA in the hub forwards traffic AND UDRs on both spokes point to the NVA. Enable "Allow Forwarded Traffic" on all peerings.

2. **AWS:** VPC peering is non-transitive. Transit Gateway provides transitive routing natively. For inspection, route TGW traffic through a centralized firewall VPC (inspection VPC pattern).

3. **GCP:** VPC peering is non-transitive. For transitive routing, use a Network Virtual Appliance (NVA) in the hub VPC with custom route import/export enabled on peerings, or use Network Connectivity Center for managed transit.

## Decision Matrix: Topology Selection

| Criteria | Hub-Spoke | Mesh | Virtual WAN / TGW | Isolated |
|----------|-----------|------|-------------------|----------|
| Number of VNets/VPCs | 3–50 | 2–10 | 50+ | 1–3 |
| Centralized security | ✅ Required | ❌ Not enforced | ✅ Configurable | ✅ Per-network |
| Spoke-to-spoke latency | Medium (hub hop) | Low (direct) | Low–Medium | N/A |
| Operational complexity | Medium | High (N×N peerings) | Low (managed) | Low |
| Cost | Firewall + Gateway | Peering fees only | Managed service fee | Minimal |
| On-prem connectivity | Shared via hub gateway | Per-network gateways | Integrated | Per-network |
| Best for | Enterprise standard | Small tightly-coupled clusters | Large-scale / global | Compliance isolation |

## Anti-Patterns to Avoid

1. **Hub without firewall** — A hub that only routes traffic without inspection defeats the purpose. Use at minimum NSG/security group rules if a full firewall isn't justified.
2. **Oversized hub** — Don't place workloads in the hub. It should contain only shared network services. Workloads belong in spokes.
3. **Missing UDRs** — Peering alone doesn't route spoke-to-spoke traffic through the hub. Without UDRs, spoke traffic goes directly to the internet or is dropped.
4. **Single point of failure** — Deploy firewalls and gateways in zone-redundant SKUs. Use Active/Active VPN gateways. In AWS, attach TGW to subnets in multiple AZs.

## References

- Azure hub-spoke topology: https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke
- Azure Virtual WAN: https://learn.microsoft.com/azure/virtual-wan/virtual-wan-about
- AWS Transit Gateway: https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html
- GCP Shared VPC: https://cloud.google.com/vpc/docs/shared-vpc
- GCP Network Connectivity Center: https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/overview

**Analysis only — verify against vendor documentation before applying.**
