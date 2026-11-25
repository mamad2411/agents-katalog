# Gateway Sizing — Skill Definition

## Purpose

Provide detailed guidance for selecting and sizing network gateway services across Azure, AWS, and GCP. This skill covers SKU specifications, throughput limits, connection capacities, right-sizing criteria, upgrade paths, and cost-performance tradeoff analysis.

## Core Knowledge

### Right-Sizing Methodology

#### Sizing Formula
```
Required Capacity = Current Peak × Growth Factor × Headroom Multiplier

Where:
- Current Peak = P95 or P99 throughput (choose based on criticality)
- Growth Factor = (1 + annual_growth_rate)^planning_horizon_years
- Headroom Multiplier = 1.2 (standard) to 1.5 (critical workloads)
```

#### Example Calculation
```
Current P95: 800 Mbps
Annual growth: 40%
Planning horizon: 2 years
Criticality: High (1.3 headroom)

Required = 800 × (1.40)^2 × 1.3 = 800 × 1.96 × 1.3 = 2,038 Mbps
→ Select SKU supporting ≥ 2 Gbps sustained throughput
```

#### Selection Criteria Priority
1. **Throughput** — Must meet projected peak with headroom
2. **Connection/tunnel count** — Must support projected endpoints
3. **Features** — Zone redundancy, BGP, active-active, IKEv2
4. **Availability SLA** — Match to workload RTO/RPO requirements
5. **Cost** — Total cost including data processing charges
6. **Upgrade path** — Can SKU be upgraded in-place without downtime?

## Provider Specifics

### Azure VPN Gateway SKUs

| SKU | Aggregate Throughput | S2S Tunnels | P2S Connections | BGP | Zone Redundant | Active-Active |
|-----|---------------------|-------------|-----------------|-----|----------------|---------------|
| Basic | 100 Mbps | 10 | 128 | No | No | No |
| VpnGw1 | 650 Mbps | 30 | 250 | Yes | No | Yes |
| VpnGw1AZ | 650 Mbps | 30 | 250 | Yes | Yes | Yes |
| VpnGw2 | 1,000 Mbps | 30 | 500 | Yes | No | Yes |
| VpnGw2AZ | 1,000 Mbps | 30 | 500 | Yes | Yes | Yes |
| VpnGw3 | 1,250 Mbps | 30 | 1,000 | Yes | No | Yes |
| VpnGw3AZ | 1,250 Mbps | 30 | 1,000 | Yes | Yes | Yes |
| VpnGw4 | 5,000 Mbps | 100 | 5,000 | Yes | No | Yes |
| VpnGw4AZ | 5,000 Mbps | 100 | 5,000 | Yes | Yes | Yes |
| VpnGw5 | 10,000 Mbps | 100 | 10,000 | Yes | No | Yes |
| VpnGw5AZ | 10,000 Mbps | 100 | 10,000 | Yes | Yes | Yes |

**Key Notes:**
- Throughput is aggregate (all tunnels combined)
- Active-active doubles tunnel count but not throughput
- In-place SKU upgrade supported (VpnGw1 → VpnGw5) without downtime
- Cannot upgrade from Basic to VpnGw* (requires redeployment)
- Generation2 SKUs required for VpnGw4/VpnGw5
- Per-tunnel maximum: ~1.25 Gbps (IPsec overhead reduces effective throughput)

**Sizing Guidance:**
- < 500 Mbps, ≤ 10 tunnels, no BGP needed → Basic (dev/test only)
- < 600 Mbps, ≤ 30 tunnels, BGP needed → VpnGw1AZ
- 600 Mbps – 1 Gbps → VpnGw2AZ
- 1 – 1.25 Gbps → VpnGw3AZ
- 1.25 – 5 Gbps → VpnGw4AZ
- 5 – 10 Gbps → VpnGw5AZ

### Azure ExpressRoute SKUs

| Circuit Bandwidth | Standard Routes | Premium Routes | Monthly Cost (Metered) | Monthly Cost (Unlimited) |
|-------------------|-----------------|----------------|----------------------|------------------------|
| 50 Mbps | 4,000 | 10,000 | ~$55 | ~$150 |
| 100 Mbps | 4,000 | 10,000 | ~$110 | ~$300 |
| 200 Mbps | 4,000 | 10,000 | ~$180 | ~$510 |
| 500 Mbps | 4,000 | 10,000 | ~$360 | ~$1,025 |
| 1 Gbps | 4,000 | 10,000 | ~$575 | ~$2,050 |
| 2 Gbps | 4,000 | 10,000 | ~$1,060 | ~$3,380 |
| 5 Gbps | 4,000 | 10,000 | ~$1,800 | ~$6,650 |
| 10 Gbps | 4,000 | 10,000 | ~$2,000 | ~$8,600 |
| 100 Gbps | 4,000 | 10,000 | Contact | Contact |

**Key Notes:**
- Metered circuits include outbound data charges ($0.025/GB typically)
- Unlimited circuits have no data charges (predictable cost)
- Burst up to 2× provisioned bandwidth (metered charges apply at burst rate)
- ExpressRoute Direct required for 40 Gbps and 100 Gbps
- ExpressRoute Direct supports MACsec encryption (line-rate)
- Circuit upgrade is non-disruptive (within same peering location)
- Cross-region via Global Reach (Premium add-on required)

**Sizing Decision Matrix:**
```
Monthly data transfer < 1 TB   → Metered (lower base cost)
Monthly data transfer > 5 TB   → Unlimited (break-even ~4-6 TB depending on SKU)
Need > 10 Gbps                 → ExpressRoute Direct (dedicated ports)
Need encryption at line rate   → ExpressRoute Direct with MACsec
Need multi-region              → Premium add-on + Global Reach
```

### Azure Application Gateway v2

| Metric | Standard_v2 | WAF_v2 |
|--------|-------------|---------|
| Max instances (autoscale) | 125 | 125 |
| Throughput per instance | ~500 Mbps | ~250 Mbps (WAF processing) |
| Max aggregate throughput | ~62.5 Gbps | ~31.25 Gbps |
| Connections per instance | 2,500 concurrent | 2,500 concurrent |
| Capacity Units (CU) per instance | 10 CU | 10 CU |

**Capacity Unit Components:**
- 1 CU = 2,500 concurrent connections + 2.22 Mbps throughput + 1 compute unit
- The dimension that reaches its limit first determines CU consumption
- Min instances (always-on) + autoscale max = cost-performance control

**Sizing Formula:**
```
Required CUs = MAX(
  concurrent_connections / 2500,
  throughput_mbps / 2.22,
  compute_units_needed
)
Min instances = Required CUs at baseline / 10
Max instances = Required CUs at peak / 10
```

### Azure Firewall Throughput

| SKU | Max Throughput | IDPS Throughput | Notes |
|-----|---------------|-----------------|-------|
| Standard | 30 Gbps | N/A | TCP traffic; 3 Gbps for non-TCP |
| Premium | 100 Gbps | 10 Gbps (with IDPS alert/deny) | TLS inspection reduces by ~40% |

**Scaling Characteristics:**
- Auto-scales based on throughput and CPU
- Scale-out in ~5-10 minutes (not instant)
- Multiple public IPs (up to 250) for SNAT port scaling
- Each PIP provides 2,496 SNAT ports per backend
- Forced tunneling mode impacts throughput

### AWS VPN Gateway

| Configuration | Throughput | Tunnels |
|--------------|-----------|---------|
| Site-to-site VPN (VGW) | 1.25 Gbps per tunnel | 2 per connection, 10 connections |
| Site-to-site VPN (TGW) | 1.25 Gbps per tunnel | 2 per connection, 5,000 connections |
| Accelerated VPN | 1.25 Gbps per tunnel | Leverages Global Accelerator |
| ECMP (TGW, multiple connections) | N × 1.25 Gbps | Max aggregate ~50 Gbps |

**Key Notes:**
- VPN throughput depends on packet size (smaller packets = lower throughput)
- 1,400-byte packets: ~1.2 Gbps effective
- 200-byte packets: ~400 Mbps effective
- ECMP across multiple VPN connections for aggregate throughput > 1.25 Gbps
- Transit Gateway required for ECMP support

### AWS Transit Gateway Bandwidth

| Metric | Current planning frame |
|--------|------------------------|
| VPC attachment bandwidth | Up to 100 Gbps per VPC attachment per AZ, each direction |
| VPC attachment packet rate | Up to 7.5 million packets per second per VPC attachment per AZ |
| Per-flow behavior | Depends on AZ path, flow hashing, and workload architecture; avoid sizing on stale single-flow constants |
| Aggregate per TGW | AWS managed; realized throughput depends on attachment design |
| Maximum attachments | 5,000 |
| Maximum peered TGWs | 50 |

**Sizing Considerations:**
- Use per-VPC-attachment-per-AZ quotas for capacity modeling; place workloads and attachments deliberately across AZs.
- Multi-flow workloads benefit from flow hashing, but elephant flows can still bottleneck on a single path.
- Validate route-table, attachment, packet-rate, and bandwidth quotas in AWS Service Quotas before sizing.
- Data processing charges apply to TGW traffic; verify current pricing.

### GCP Cloud VPN

| Configuration | Throughput planning frame | Max Tunnels | Aggregate framing |
|--------------|---------------------------|-------------|-------------------|
| Classic VPN | Packet-rate based; 3 Gbps is an upper-bound example for large packets | 8 per gateway | Packet-size and ECMP dependent |
| HA VPN (2 interfaces) | Packet-rate based; 250k pps per tunnel system limit | 4 per interface (8 total) | Sum only with effective ECMP and sufficient peer capacity |
| HA VPN + ECMP | Packet-size dependent per tunnel | 8 tunnels | Validate with current GCP quotas and tests |

**Key Notes:**
- Cloud VPN limits are packet-rate based (250k pps per tunnel), so throughput varies with packet size.
- Treat 3 Gbps as an upper-bound example for large packets, not a deterministic sizing guarantee.
- Ingress is limited by peer device and path.
- HA VPN provides 99.99% SLA (vs 99.9% for Classic).
- Verify current GCP Quotas before sizing or promising aggregate throughput.

### GCP Cloud Interconnect

| Type | Capacity Options | SLA |
|------|-----------------|-----|
| Dedicated (10G) | 10 Gbps per link, up to 8 links (80 Gbps) | 99.9% (single) / 99.99% (redundant) |
| Dedicated (100G) | 100 Gbps per link, up to 8 links (800 Gbps) | 99.9% (single) / 99.99% (redundant) |
| Partner | 50 Mbps to 50 Gbps per attachment | Varies by partner |

**VLAN Attachment Capacities:**
- 50 Mbps, 100 Mbps, 200 Mbps, 300 Mbps, 400 Mbps, 500 Mbps
- 1 Gbps, 2 Gbps, 5 Gbps, 10 Gbps, 20 Gbps, 50 Gbps

**Sizing Decision:**
```
< 1 Gbps needed    → Partner Interconnect (lower commitment)
1-10 Gbps          → Dedicated 10G link
10-80 Gbps         → Multiple Dedicated 10G links (LAG)
> 80 Gbps          → Dedicated 100G links
```

## Cost vs Performance Tradeoffs

### Azure VPN Gateway Cost Optimization
```
VpnGw1AZ hourly: ~$0.50/hr ($365/month)
VpnGw2AZ hourly: ~$0.75/hr ($548/month)
VpnGw3AZ hourly: ~$1.12/hr ($818/month)
VpnGw4AZ hourly: ~$1.87/hr ($1,365/month)
VpnGw5AZ hourly: ~$3.50/hr ($2,555/month)

Cost per Mbps (monthly):
VpnGw1AZ: $0.56/Mbps
VpnGw2AZ: $0.55/Mbps
VpnGw3AZ: $0.65/Mbps
VpnGw4AZ: $0.27/Mbps  ← Best value for high throughput
VpnGw5AZ: $0.26/Mbps  ← Best value at scale
```

### Decision Framework
```
IF current_peak < 50% SKU_capacity AND no_growth_expected:
    → Consider downgrade (save cost)
    
IF current_peak > 70% SKU_capacity:
    → Plan upgrade within 3-6 months
    
IF current_peak > 80% SKU_capacity:
    → Upgrade within 1-3 months
    
IF tunnel_count > 80% SKU_limit:
    → Upgrade for connection capacity regardless of throughput
```

### ExpressRoute vs VPN Break-Even Analysis
```
VPN (VpnGw3AZ): ~$818/month, 1.25 Gbps, encrypted, internet path
ExpressRoute (1 Gbps metered): ~$575/month + data charges, private path

Break-even (data charges):
If monthly transfer < 10 TB: ExpressRoute metered may be cheaper
If monthly transfer > 10 TB: ExpressRoute unlimited ($2,050/month) wins
If latency-sensitive: ExpressRoute always (predictable latency)
If compliance requires private path: ExpressRoute required
```

## Upgrade Path Planning

### Non-Disruptive Upgrades
- Azure VPN Gateway: VpnGw1-5 (in-place, minutes of brief interruption)
- Azure ExpressRoute: Circuit bandwidth upgrade (non-disruptive)
- AWS Transit Gateway: No sizing changes needed (managed)
- GCP Interconnect: Add VLAN attachments or links to LAG

### Disruptive Upgrades (Require Redeployment)
- Azure VPN Basic → VpnGw* (full redeployment)
- Azure VPN Gen1 → Gen2 (redeployment for some regions)
- Changing from VPN to ExpressRoute (parallel deployment + migration)
- GCP Classic VPN → HA VPN (new gateway required)

### Upgrade Timeline Template
```
Month 0: Alert triggered (80% utilization)
Week 1: Validate growth trend (not temporary spike)
Week 2: Select target SKU, estimate cost impact
Week 3: Get budget/change approval
Week 4: Execute upgrade (maintenance window if disruptive)
Week 5: Validate performance, update monitoring thresholds
```

---

**Analysis only — verify against vendor documentation before applying.**
