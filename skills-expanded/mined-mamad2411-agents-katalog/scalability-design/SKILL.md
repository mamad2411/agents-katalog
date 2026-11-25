# Scalability Design — Skill Definition

## Purpose

Provide comprehensive guidance on cloud networking scalability patterns, subscription/account limits, horizontal scaling strategies, and architectural decisions for when to split or consolidate network topologies. This skill enables capacity planners to design networks that scale gracefully across Azure, AWS, and GCP.

## Core Knowledge

### Scaling Philosophy

#### Vertical vs Horizontal Scaling
- **Vertical (scale-up):** Upgrade SKU/tier (e.g., VpnGw1 → VpnGw5). Simpler but hits ceilings.
- **Horizontal (scale-out):** Add parallel instances (e.g., multiple VPN gateways, ECMP paths). Higher ceiling but more complex.
- **Architectural (re-platform):** Change topology (e.g., hub-spoke → Virtual WAN). Required when horizontal hits limits.

#### When to Scale
```
Scale-up when:
- Current SKU < 70% of next SKU's cost-per-Mbps efficiency
- Need is temporary (event-driven spike)
- Operational simplicity is priority

Scale-out when:
- At maximum SKU and still growing
- Need redundancy in addition to capacity
- Different traffic classes need isolation

Re-platform when:
- Hitting subscription-level limits
- Managing > 30 peering connections manually
- Need transit routing across > 10 spokes
- Operational overhead exceeds architecture value
```

## Provider-Specific Limits

> Quota validation: Treat static limit tables as planning examples only. Before sizing or committing designs, verify current Azure limits/quotas, AWS Service Quotas, and GCP Quotas for the specific account, subscription, project, region, and resource type; request quota increases where supported.

### Azure Subscription Limits

| Resource | Default Limit | Max (with support) | Scale Strategy |
|----------|--------------|-------------------|----------------|
| VNets per subscription | 1,000 | 1,000 | Multiple subscriptions |
| Subnets per VNet | 3,000 | 3,000 | Multiple VNets |
| VNet peerings per VNet | 500 | 500 | Move to vWAN |
| Routes per route table | 400 | 400 | Summarize routes, use BGP |
| NSG rules per NSG | 1,000 | 1,000 | Multiple NSGs, ASGs |
| NSGs per subscription | 5,000 | 5,000 | Multiple subscriptions |
| VPN Gateway tunnels (VpnGw1-3) | 30 | 30 | Upgrade to VpnGw4/5 (100) |
| VPN Gateway tunnels (VpnGw4-5) | 100 | 100 | Multiple gateways |
| ExpressRoute circuits per subscription | 50 | 50 | Multiple subscriptions |
| ExpressRoute connections per VNet gateway | 4 (Standard) / 16 (High Perf/Ultra) | 16 | Multiple gateways |
| Public IPs per subscription | 1,000 | 1,000 | Multiple subscriptions |
| Network interfaces per subscription | 65,536 | 65,536 | Multiple subscriptions |
| Azure Firewall instances per subscription | 200 | 200 | vWAN secured hubs |
| Application Gateways per subscription | 1,000 | 1,000 | Sufficient for most cases |
| Load Balancer rules | 1,500 per LB | 1,500 | Multiple LBs |
| Private Endpoints per subscription | 65,000 | 65,000 | Sufficient for most cases |
| DNS Private Zones per subscription | 25,000 | 25,000 | Sufficient for most cases |

### AWS Account Limits

| Resource | Default Limit | Max (with support) | Scale Strategy |
|----------|--------------|-------------------|----------------|
| VPCs per region | 5 | 100 | Multiple accounts |
| Subnets per VPC | 200 | 500 | Multiple VPCs |
| Route tables per VPC | 200 | 200 | Multiple VPCs |
| Routes per route table | 50 | 1,000 | Summarize, use TGW |
| Security groups per VPC | 2,500 | 2,500 | Prefix lists |
| Rules per security group | 60 inbound + 60 outbound | 1,000 total | Managed prefix lists |
| Network ACL rules | 20 per direction | 40 | Multiple ACLs |
| Elastic IPs per region | 5 | 100+ | Multiple accounts |
| Transit Gateway attachments | 5,000 | 5,000 | Multiple TGWs |
| Transit Gateway route tables | 20 | 20 | Route table optimization |
| TGW routes per route table | 10,000 | 10,000 | Summarization |
| VPN connections per VGW | 10 | 10 | Transit Gateway |
| VPN connections per TGW | 5,000 | 5,000 | Sufficient for most cases |
| NAT Gateways per AZ | 5 | 100 | Sufficient for most cases |
| Network interfaces per region | 5,000 | 15,000 | Multiple accounts |
| VPC peering connections per VPC | 125 | 125 | Transit Gateway |
| Direct Connect virtual interfaces | 50 per connection | 50 | Multiple connections |

### GCP Project Limits

| Resource | Default Limit | Max (with support) | Scale Strategy |
|----------|--------------|-------------------|----------------|
| VPC networks per project | 15 | 30 | Multiple projects |
| Subnets per network | 300 | 600 | Multiple networks |
| Subnets per region (per network) | 1 per region (recommended) | Multiple | Secondary ranges |
| Firewall rules per project | 500 | 1,000 | Hierarchical policies |
| Routes per network | 250 | 500 | Summarization |
| VPN tunnels per project | 128 | 256 | Multiple projects |
| Cloud Router BGP peers | 128 per router | 128 | Multiple routers |
| Cloud Router learned routes | 200 per region | 400 | Summarize, split routers |
| Interconnect attachments per project | 16 (per region per network) | 32 | Multiple projects |
| Internal forwarding rules per network | 75 per region | 750 | Multiple networks |
| External forwarding rules | 45 per region | 600 | Sufficient for most cases |
| Forwarding rules per LB | 5 | 15 | Multiple LBs |
| Instance groups per zone | 2,000 | 2,000 | Sufficient |
| Target pools per project | 50 | 200 | Use backend services |
| Packet Mirroring policies | 3 per project | 10 | Multiple projects |

## Horizontal Scaling Patterns

### Multiple VPN Gateways (Azure)
```
Pattern: Deploy multiple VPN gateways across different VNets/subnets
Use case: > 100 S2S tunnels or > 10 Gbps aggregate

Architecture:
┌─────────────────────────────────────┐
│           Hub VNet                   │
│  ┌─────────┐  ┌─────────┐          │
│  │ VPN GW 1│  │ VPN GW 2│          │
│  │ GwSub-1 │  │ GwSub-2 │          │
│  └────┬────┘  └────┬────┘          │
│       │             │               │
│  Sites 1-50    Sites 51-100         │
└─────────────────────────────────────┘

Limitations:
- Only 1 VPN gateway per VNet (must use separate VNets + peering)
- OR: Use Virtual WAN with multiple VPN gateway scale units
- vWAN: up to 20 Gbps per hub VPN gateway (scale units configurable)
```

### ECMP for Aggregate Throughput
```
Pattern: Multiple equal-cost paths via BGP for load distribution

Azure (ExpressRoute):
- Up to 16 ER connections per gateway (UltraPerformance/ErGw3AZ)
- ECMP across circuits for aggregate bandwidth
- 4 circuits × 10 Gbps = 40 Gbps effective (with good flow distribution)

AWS (Transit Gateway):
- Multiple VPN connections with ECMP enabled on TGW
- Up to 50 VPN connections for ECMP (practical limit ~20 for management)
- 20 tunnels × 1.25 Gbps = 25 Gbps aggregate

GCP (HA VPN):
- 4 tunnels per HA VPN gateway interface pair
- 2 interfaces × 4 tunnels = 8 tunnels per gateway pair
- Throughput is packet-rate and packet-size dependent; treat 3 Gbps/tunnel only as an upper-bound example for large packets
- Multiple gateways and ECMP can increase aggregate capacity when flow distribution and peer capacity support it
```

### Azure Firewall Scaling

#### Autoscale Behavior
```
Scale trigger: CPU > 60% or throughput > threshold
Scale-out time: 5-10 minutes (plan for initial burst handling)
Maximum scale: Not published (internally managed, dozens of instances)
Minimum instances: Cannot set minimum (always starts at base)
```

#### Multiple Public IPs for SNAT
```
SNAT ports per PIP: 2,496 (per backend destination)
Maximum PIPs: 250
Total SNAT capacity: 250 × 2,496 = 624,000 ports

Scaling formula:
Required PIPs = peak_concurrent_outbound_connections / 2,496
Add 20% headroom: PIPs = (connections / 2,496) × 1.2
```

#### Azure Firewall Premium Throughput
```
Without IDPS: up to 100 Gbps (TCP)
With IDPS (alert mode): ~10 Gbps
With IDPS (deny mode): ~10 Gbps
With TLS inspection: ~40% reduction from IDPS throughput

Scaling strategy for > 100 Gbps:
→ Multiple firewall instances in different VNets
→ UDR-based traffic steering to distribute load
→ Azure Firewall Manager for central policy
```

### Application Gateway Autoscaling

```
Autoscale Configuration:
- Minimum instances: 2 (for HA, recommended)
- Maximum instances: 125
- Scale based on: CU consumption (connections + throughput + compute)

Scaling speed:
- Scale-out: 6-7 minutes per new instance
- Scale-in: Graceful drain + 10-minute cooldown

Capacity planning:
- Pre-warm for known events (set min instances higher)
- Azure support can pre-warm for very large events
- Each instance: ~10 CU = 25,000 connections + 22.2 Mbps + 10 compute units
```

### Transit Gateway Scaling (AWS)

```
Route Tables:
- Default: 20 route tables per TGW
- Use for: segment isolation (prod/dev/shared-services)
- Strategy: consolidate where possible, split for security boundaries

Attachments:
- Maximum: 5,000 per TGW
- Types: VPC, VPN, Direct Connect, Peering, Connect
- VPC attachments: current official quota is up to 100 Gbps per attachment per AZ each direction and up to 7.5M pps; realized throughput depends on AZ placement, flow distribution, and architecture

Multi-TGW strategy:
- Regional TGWs peered together
- Per-segment TGWs (security isolation)
- Maximum 50 peered TGWs per TGW

Bandwidth planning:
- TGW data processing: $0.02/GB (significant at scale)
- 1 TB/day = $0.02 × 1,000 = $20/day = $600/month per direction
- Consider VPC peering for heavy traffic pairs (no data processing fee)
```

## Architectural Splitting Decisions

### When to Split into Multiple Subscriptions/Accounts

#### Azure — Multiple Subscriptions
```
Split when:
- VNet count approaching 800+ (80% of 1,000 limit)
- NSG count approaching 4,000+ (80% of 5,000 limit)
- Need separate billing/governance boundaries
- RBAC blast radius reduction required
- Resource group count > 800 (limit 980)

Pattern: Management Group hierarchy
├── Root Management Group
│   ├── Platform (networking, identity, management)
│   ├── Production (one sub per workload or BU)
│   ├── Non-Production (dev, test, staging)
│   └── Sandbox (experimentation)
```

#### AWS — Multiple Accounts
```
Split when:
- VPC count at 4+ per region (limit 5 default)
- Security group count > 2,000
- Need AWS Organizations SCPs for governance
- Blast radius / security boundary requirements
- Service quotas becoming constraint

Pattern: AWS Control Tower / Organizations
├── Management Account
│   ├── Security OU (log archive, audit)
│   ├── Infrastructure OU (networking, shared services)
│   ├── Production OU (workload accounts)
│   └── Non-Production OU (dev/test accounts)
```

#### GCP — Multiple Projects
```
Split when:
- VPC network count approaching 12+ (limit 15)
- Firewall rules > 400 (limit 500)
- Need folder-level policies (hierarchical firewall rules)
- Separate billing boundaries required

Pattern: GCP Organization hierarchy
├── Organization
│   ├── Folders (per BU or environment)
│   │   ├── Shared VPC host projects
│   │   └── Service projects
```

### Hub-Spoke Scale Limits → Virtual WAN Migration

#### Azure Hub-Spoke Limits
```
Symptoms requiring migration to vWAN:
- > 500 VNet peerings on hub (hard limit)
- > 30 site-to-site VPN tunnels (VpnGw1-3 limit)
- Need any-to-any spoke connectivity (requires NVA/Azure Firewall in hub)
- Managing hundreds of UDRs manually
- Multiple regions requiring full mesh
- Need branch-to-branch connectivity (S2S transit)

Virtual WAN advantages:
- Up to 500 VNet connections per hub (same as peering, but managed)
- Automatic any-to-any routing (no UDRs needed for spoke-to-spoke)
- 20 Gbps aggregate VPN (per hub, with scale units)
- Built-in hub-to-hub transit (inter-region)
- Routing intent for simplified security policy
- Integrated ExpressRoute, VPN, SD-WAN
```

#### Migration Decision Matrix
| Criteria | Hub-Spoke | Virtual WAN |
|----------|-----------|-------------|
| Spokes | < 50 | 50-500 |
| Regions | 1-2 | 3+ |
| S2S tunnels | < 30 | 30-1,000 |
| Transit routing | NVA/Firewall in hub | Built-in |
| Routing complexity | Low-medium | High (delegated to vWAN) |
| Customization | Full control of routes | Less control, managed service |
| Cost | Lower (no vWAN fees) | Higher (vWAN + hub fees) |
| Branch connectivity | Manual (VPN + UDRs) | Automatic branch-to-branch |
| SD-WAN integration | Manual NVA | Native partner integration |

#### Hybrid Approach: Staged Migration
```
Phase 1: Deploy Virtual WAN hub alongside existing hub-spoke
Phase 2: Connect new spokes to vWAN hub
Phase 3: Migrate existing spokes in batches (re-peer to vWAN hub)
Phase 4: Decommission legacy hub
Phase 5: Enable routing intent for security integration

Timeline: 3-6 months for enterprise migration
Risk: Dual-homed period requires careful route preference management
```

## Scaling Patterns by Use Case

### High Bandwidth (> 10 Gbps)
```
Azure:
- ExpressRoute Direct (40/100 Gbps ports)
- Multiple VNet gateways with ECMP
- Virtual WAN with multiple ER connections per hub

AWS:
- Direct Connect 100 Gbps
- LAG (up to 4 connections)
- Transit Gateway with multiple VPC attachments sized against current per-attachment-per-AZ quotas; verify AWS Service Quotas before committing

GCP:
- Dedicated Interconnect 100 Gbps
- 8-link LAG (800 Gbps)
- Multiple VLAN attachments
```

### High Connection Count (> 1,000 sites)
```
Azure:
- Virtual WAN (1,000 VPN branches per hub)
- Multiple hubs for > 1,000 branches
- SD-WAN partner integration

AWS:
- Transit Gateway (5,000 VPN connections)
- AWS SD-WAN partners via TGW Connect

GCP:
- HA VPN at scale (multiple gateways)
- Network Connectivity Center for hub model
- Partner SD-WAN via Cloud Router
```

### High Route Count (> 1,000 routes)
```
Azure:
- ExpressRoute Premium: 10,000 routes per peering
- Route summarization at on-premises
- Azure Route Server: 1,000 routes per peer (8,000 total)
- BGP communities for selective route propagation

AWS:
- TGW route table: 10,000 routes
- Summarization at on-premises routers
- Prefix lists for route filtering

GCP:
- Cloud Router: 200 learned routes per region (400 with support)
- Custom route advertisements
- Summarization mandatory at scale
```

## Monitoring for Scale

### Key Metrics to Track for Scaling Decisions
```
1. Resource count vs limits (alert at 80%):
   - VNets, subnets, peerings, NSGs, routes, PIPs

2. Throughput vs capacity (alert at 70%/80%/90%):
   - Gateway bandwidth, circuit utilization, firewall throughput

3. Connection/session counts vs limits:
   - VPN tunnels, SNAT ports, concurrent connections, BGP peers

4. Error rates indicating exhaustion:
   - SNAT port exhaustion events
   - Route table overflow (packets dropped)
   - Connection timeouts (overloaded gateway)
   - BGP route withdrawal (route limit exceeded)
```

---

**Analysis only — verify against vendor documentation before applying.**
