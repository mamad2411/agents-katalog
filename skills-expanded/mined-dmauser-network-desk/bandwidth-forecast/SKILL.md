# Bandwidth Forecasting — Skill Definition

## Purpose

Provide comprehensive bandwidth forecasting capabilities for cloud networking resources. This skill covers traffic modeling methodologies, data source identification, baseline establishment, forecasting formulas, and provider-specific metrics for predicting future bandwidth requirements.

## Core Knowledge

### Traffic Modeling Methodologies

#### Linear Growth Model
- Formula: `B(t) = B₀ + (r × t)`
- Where: B₀ = baseline bandwidth, r = growth rate (Mbps/month), t = time periods
- Best for: Steady organic growth, predictable user onboarding
- Example: 500 Mbps baseline + 25 Mbps/month = 800 Mbps in 12 months

#### Exponential Growth Model
- Formula: `B(t) = B₀ × (1 + r)^t`
- Where: B₀ = baseline, r = growth rate per period, t = time periods
- Best for: Rapidly scaling applications, viral growth, IoT deployments
- Example: 500 Mbps × (1.08)^12 = 1,259 Mbps in 12 months at 8% monthly growth

#### Seasonal/Cyclical Model
- Formula: `B(t) = B₀ × (1 + r)^t × (1 + A × sin(2π × t/P))`
- Where: A = seasonal amplitude, P = period length
- Best for: Retail (holiday peaks), education (semester cycles), financial (quarter-end)
- Captures both long-term trend and periodic variations

#### Composite Model
- Combines multiple traffic sources with different growth characteristics
- Formula: `B_total(t) = Σ [B_i(t) × weight_i]`
- Best for: Enterprise environments with diverse workloads

### Baseline Establishment

#### Data Collection Period
- **Minimum:** 4 weeks for short-term planning
- **Recommended:** 3-6 months for trend identification
- **Ideal:** 12+ months to capture full seasonal cycles

#### Statistical Measures
- **Average throughput** — For sustained capacity planning
- **P95 throughput** — Industry standard for link sizing (handles 95% of observations)
- **P99 throughput** — For critical links requiring higher headroom
- **Peak (max)** — For burst capacity and failover scenarios
- **Standard deviation** — For confidence interval calculation

#### Baseline Formula
```
Effective Baseline = P95(historical_samples) × (1 + coefficient_of_variation)
Where: coefficient_of_variation = σ / μ
```

### Forecasting Formulas

#### Compound Annual Growth Rate (CAGR)
```
CAGR = (B_end / B_start)^(1/years) - 1
```

#### Time to Capacity Threshold
```
t_threshold = ln(Capacity × threshold% / B_current) / ln(1 + growth_rate)
```
Example: At 8% monthly growth, 1 Gbps link at 500 Mbps current hits 80% in:
```
t = ln(1000 × 0.8 / 500) / ln(1.08) = 6.0 months
```

#### Confidence Intervals
```
Upper bound = Forecast × (1 + 2σ/μ)
Lower bound = Forecast × (1 - 2σ/μ)
```

### Capacity Alert Thresholds

| Threshold | Action | Timeline |
|-----------|--------|----------|
| 70% sustained | Begin planning upgrade | 3-6 months |
| 80% sustained | Initiate procurement/provisioning | 1-3 months |
| 90% sustained | Emergency action, implement traffic shaping | Immediate |
| 95% peak | Risk of packet loss, connection failures | Critical |

### Headroom Planning

#### Burst vs Sustained
- **Burst headroom:** 2-3× average for microsecond/millisecond bursts (TCP window filling)
- **Short-term headroom:** 1.5× P95 for minute-scale traffic spikes
- **Sustained headroom:** 1.2-1.3× projected peak for growth buffer

#### Failover Headroom
- **Active/passive:** Each link must carry 100% of total traffic
- **Active/active (N+1):** Each link carries N/(N-1) of normal share during failover
- **ECMP (N paths):** Loss of one path increases others by 1/(N-1)

## Provider-Specific Metrics

### Azure Bandwidth Metrics

#### VNet Gateway Throughput
| SKU | Aggregate Throughput | Metric Name |
|-----|---------------------|-------------|
| VpnGw1 | 650 Mbps | `TunnelBandwidth` |
| VpnGw2 | 1.0 Gbps | `TunnelBandwidth` |
| VpnGw3 | 1.25 Gbps | `TunnelBandwidth` |
| VpnGw4 | 5.0 Gbps | `TunnelBandwidth` |
| VpnGw5 | 10.0 Gbps | `TunnelBandwidth` |

**Key Metrics (Azure Monitor):**
- `TunnelBandwidth` — Bytes/sec per tunnel
- `TunnelIngressBytes` / `TunnelEgressBytes` — Directional traffic
- `TunnelIngressPackets` / `TunnelEgressPackets` — Packet counts
- `P2SBandwidth` — Point-to-site aggregate bandwidth
- `P2SConnectionCount` — Active P2S connections

#### ExpressRoute Circuit Utilization
| Circuit SKU | Bandwidth | Metric |
|-------------|-----------|--------|
| 50 Mbps | 50 Mbps | `BitsInPerSecond` / `BitsOutPerSecond` |
| 100 Mbps | 100 Mbps | `BitsInPerSecond` / `BitsOutPerSecond` |
| 200 Mbps | 200 Mbps | `BitsInPerSecond` / `BitsOutPerSecond` |
| 500 Mbps | 500 Mbps | `BitsInPerSecond` / `BitsOutPerSecond` |
| 1 Gbps | 1,000 Mbps | `BitsInPerSecond` / `BitsOutPerSecond` |
| 2 Gbps | 2,000 Mbps | `BitsInPerSecond` / `BitsOutPerSecond` |
| 5 Gbps | 5,000 Mbps | `BitsInPerSecond` / `BitsOutPerSecond` |
| 10 Gbps | 10,000 Mbps | `BitsInPerSecond` / `BitsOutPerSecond` |
| 100 Gbps | 100,000 Mbps | `BitsInPerSecond` / `BitsOutPerSecond` |

**ExpressRoute Metrics:**
- `BitsInPerSecond` / `BitsOutPerSecond` — Circuit utilization
- `ArpAvailability` — ARP table availability (health indicator)
- `BgpAvailability` — BGP session state
- `GlobalReachBitsInPerSecond` / `GlobalReachBitsOutPerSecond` — Global Reach traffic

**Burst Behavior:**
- ExpressRoute circuits allow bursting up to 2× provisioned bandwidth (metered circuits)
- Premium add-on enables Global Reach and increased route limits (10,000 routes)

#### Azure NAT Gateway
- Bandwidth is a **per NAT gateway resource** limit, not multiplied by public IP count: Standard supports up to 50 Gbps per resource; StandardV2 supports up to 100 Gbps per resource where available.
- Public IP count scales SNAT port inventory, not bandwidth. Use 64,512 SNAT ports per public IP for port-capacity planning only.
- Monitor: `ByteCount`, `PacketCount`, `SNATConnectionCount`.
- Verify current limits and regional availability via Azure limits/quotas before sizing.

### AWS Metrics

#### Transit Gateway
- VPC attachment throughput is documented per attachment per Availability Zone and direction; current official quota is up to 100 Gbps per VPC attachment per AZ with up to 7.5 million packets per second.
- Realized throughput depends on AZ placement, traffic symmetry, flow distribution, and attachment architecture.
- Verify current quotas in AWS Service Quotas before sizing.

**CloudWatch Metrics:**
- `BytesIn` / `BytesOut` — Per attachment
- `PacketsIn` / `PacketsOut` — Per attachment
- `PacketDropCountBlackhole` — Routing issues
- `BytesDropCountNoRoute` — Missing routes

#### VPN Gateway (AWS)
- Per-tunnel throughput: 1.25 Gbps
- Per-VPN connection (2 tunnels): 1.25 Gbps (active/passive) or 2.5 Gbps (ECMP)
- Accelerated VPN: up to 1.25 Gbps per tunnel via Global Accelerator
- Maximum VPN connections per TGW: 5,000

**CloudWatch Metrics:**
- `TunnelDataIn` / `TunnelDataOut` — Bytes per tunnel
- `TunnelState` — Tunnel up/down status

#### Direct Connect
- Dedicated: 1 Gbps, 10 Gbps, 100 Gbps
- Hosted: 50 Mbps to 10 Gbps
- LAG: Up to 4 connections in Link Aggregation Group

**CloudWatch Metrics:**
- `ConnectionBpsIngress` / `ConnectionBpsEgress`
- `VirtualInterfaceBpsIngress` / `VirtualInterfaceBpsEgress`

### GCP Metrics

#### Cloud Interconnect
- VLAN attachment: 50 Mbps to 50 Gbps
- Dedicated Interconnect: 10 Gbps or 100 Gbps per link
- Partner Interconnect: 50 Mbps to 50 Gbps
- Maximum 8 links in a LAG = 800 Gbps (8 × 100 Gbps)

**Cloud Monitoring Metrics:**
- `interconnect.googleapis.com/network/attachment/received_bytes_count`
- `interconnect.googleapis.com/network/attachment/sent_bytes_count`
- `interconnect.googleapis.com/link/circuit/receiving_light_level/value`

#### Cloud VPN
- Size Cloud VPN by packet rate and packet size. The system limit is packet-rate based (250k packets per second per tunnel); throughput is packet-size dependent.
- Treat 3 Gbps per tunnel as an upper-bound planning example for large packets, not a deterministic guarantee; aggregate estimates depend on ECMP, tunnel count, packet size, and peer device capacity.
- Verify current GCP quotas before sizing.

**Cloud Monitoring Metrics:**
- `vpn.googleapis.com/tunnel_traffic/received_bytes_count`
- `vpn.googleapis.com/tunnel_traffic/sent_bytes_count`
- `vpn.googleapis.com/tunnel_traffic/dropped_packets_count`

#### Cloud NAT
- Per-VM: 7 Gbps egress (with sufficient NAT IPs)
- Auto-scaling NAT IP allocation available
- Monitor: `nat/sent_bytes_count`, `nat/port_usage`

## Data Sources

### Primary Data Sources
1. **Flow Logs** — VNet flow logs (Azure default), VPC Flow Logs (AWS/GCP); use Azure NSG flow logs only as legacy/migration input where already deployed (new creation blocked after 2025-06-30; retire 2027-09-30)
2. **Connection Monitors** — Azure Network Watcher, AWS Reachability Analyzer
3. **Metrics APIs** — Azure Monitor, CloudWatch, Cloud Monitoring
4. **SNMP/Streaming Telemetry** — On-premises equipment feeding into cloud

### Aggregation Periods
- **Real-time dashboards:** 1-minute granularity
- **Trending analysis:** 5-minute or 1-hour aggregation
- **Capacity reports:** Daily P95/average aggregation
- **Long-term forecasts:** Weekly or monthly trend data

### Data Retention for Forecasting
- Azure Monitor: 93 days standard, up to 2 years with diagnostic settings to Log Analytics
- CloudWatch: 15 months at reduced granularity (1-hour after 15 days, 5-hour after 63 days)
- Cloud Monitoring: 6 weeks at full resolution, 2 years at reduced

## Practical Forecasting Example

### Scenario: ExpressRoute Circuit Sizing
```
Current: 1 Gbps circuit, 6-month average utilization = 55%, P95 = 72%
Growth: 12% per quarter (CAGR = 58%)

6-month forecast:  720 Mbps × (1.12)^2 = 903 Mbps (90.3% of circuit)
12-month forecast: 720 Mbps × (1.12)^4 = 1,133 Mbps (exceeds circuit!)

Recommendation: 
- Upgrade to 2 Gbps circuit within 3 months
- At current growth, 2 Gbps hits 80% in ~18 months
- Consider 5 Gbps for 3-year horizon
```

---

**Analysis only — verify against vendor documentation before applying.**
