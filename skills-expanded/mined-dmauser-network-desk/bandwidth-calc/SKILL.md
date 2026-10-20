# Skill: Bandwidth Calculation and Planning (hyb_bandwidth-calc)

Plan and size network circuits for hybrid cloud connectivity. This skill covers bandwidth measurement, capacity formulas, QoS marking, cost estimation, and upgrade decision criteria.

---

## Bandwidth Measurement Fundamentals

### Key Metrics
- **Sustained throughput**: Average bandwidth consumed over a billing period. Typically measured at the 95th percentile (discard top 5% of samples). Most providers bill on this metric for metered circuits.
- **Peak throughput**: Maximum bandwidth observed in a measurement interval. Critical for determining whether a circuit can absorb burst traffic without packet loss.
- **Burst capacity**: The ability to temporarily exceed the committed bandwidth. Some providers offer burstable circuits (e.g., 500 Mbps committed, burstable to 1 Gbps).

### Measurement Tools
```bash
# Azure ExpressRoute circuit stats
az network express-route stats show \
  --resource-group MyRG --name MyERCircuit

# Azure VPN Gateway bandwidth metrics (Azure Monitor)
az monitor metrics list \
  --resource /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworkGateways/{gw} \
  --metric TunnelBandwidth --interval PT1H

# AWS Direct Connect bandwidth (CloudWatch)
aws cloudwatch get-metric-statistics \
  --namespace AWS/DX \
  --metric-name ConnectionBpsIngress \
  --dimensions Name=ConnectionId,Value=dxcon-xxxx \
  --start-time 2024-01-01T00:00:00Z --end-time 2024-01-31T23:59:59Z \
  --period 3600 --statistics Average Maximum
```

---

## Circuit Sizing Formulas

### Basic Sizing
```
Required Circuit = (Current 95th Percentile Throughput) × (1 + Growth Factor) / (Target Utilization)
```

**Example**: Current sustained usage is 350 Mbps, expected 25% growth over 2 years, target 60% utilization:
```
Required = 350 Mbps × 1.25 / 0.60 = 729 Mbps → select 1 Gbps circuit
```

### Aggregation Planning
When multiple sites share a circuit (e.g., via SD-WAN or MPLS hub):
```
Aggregate Bandwidth = Σ(Site Bandwidth × Concurrency Factor)
```
Typical concurrency factors: 0.3–0.5 for bursty office traffic, 0.7–0.9 for sustained data transfer workloads.

### Protocol Overhead
- **Ethernet frame**: 14 bytes header + 4 bytes FCS = 18 bytes overhead per frame
- **IP header**: 20 bytes (minimum, no options)
- **TCP header**: 20 bytes (minimum, no options)
- **IPsec overhead**: ESP header (8 bytes) + IV (8–16 bytes) + padding + ESP trailer (2 bytes) + ESP auth (12–32 bytes) ≈ 50–73 bytes per packet
- **VPN effective throughput**: For 1500-byte Ethernet frames with IPsec, effective payload is approximately 1400 bytes, yielding ~93% efficiency. For small packets (64 bytes), overhead dominates — effective throughput can drop to ~50%.

---

## QoS Marking (DSCP)

When multiple traffic types share a hybrid circuit, apply Differentiated Services Code Point (DSCP) markings to prioritize critical traffic:

| Traffic Class | DSCP Value | Per-Hop Behavior | Use Case |
|--------------|------------|-------------------|----------|
| Voice (EF) | 46 | Expedited Forwarding | VoIP, real-time communication |
| Video (AF41) | 34 | Assured Forwarding 4,1 | Video conferencing |
| Business Critical (AF31) | 26 | Assured Forwarding 3,1 | ERP, database replication |
| Standard (AF21) | 18 | Assured Forwarding 2,1 | Web applications, email |
| Best Effort (BE) | 0 | Default | Internet browsing, updates |
| Scavenger (CS1) | 8 | Low priority | Backups, file sync |

**Cloud Provider DSCP Behavior**:
- **Azure ExpressRoute**: Preserves DSCP markings end-to-end on Private Peering. Microsoft peering may remark.
- **AWS Direct Connect**: Preserves DSCP markings on the Direct Connect link. Markings are stripped at the VPC boundary.
- **GCP Cloud Interconnect**: Preserves DSCP markings on the interconnect. GCP internal network does not guarantee DSCP-based QoS.

---

## Cost Estimation per Cloud

### Azure ExpressRoute
- Circuit monthly fee: varies by bandwidth and provider ($55/month for 50 Mbps to $13,000/month for 10 Gbps at Standard tier).
- Premium add-on: ~1.5× Standard price.
- Egress: Metered plan charges per GB ($0.025/GB typical); Unlimited plan includes all egress in flat fee.
- Gateway: ErGw1AZ (~$150/month), ErGw2AZ (~$550/month), ErGw3AZ (~$1,100/month).

### AWS Direct Connect
- Port hours: Dedicated connection billed per hour ($0.30/hr for 1 Gbps, $2.25/hr for 10 Gbps).
- Data transfer out: $0.02/GB (same region), varies by region and destination.
- Hosted connections: priced by partner.

### GCP Cloud Interconnect
- Port fee: $1,700/month per 10 Gbps Dedicated Interconnect link.
- VLAN attachment: $0.05/hr per attachment.
- Egress: Interconnect egress is discounted vs. internet egress ($0.02/GB for same-continent vs. $0.085/GB internet).

---

## When to Upgrade

Trigger an upgrade evaluation when:
- **95th percentile utilization exceeds 60%** sustained for 30+ days
- **Peak utilization exceeds 80%** regularly (indicates insufficient burst headroom)
- **Packet loss > 0.01%** during peak periods (indicates congestion)
- **Application latency increases** correlating with bandwidth utilization (queuing delay)
- **Growth projection** shows 60% utilization within 6 months at current trajectory

**Upgrade vs. Add Circuit**: Adding a second circuit provides both additional bandwidth and redundancy. Upgrading a single circuit improves capacity but not resilience. For production workloads, prefer adding a diverse circuit over upgrading a single circuit.

**Analysis only — verify against vendor documentation before applying.**
