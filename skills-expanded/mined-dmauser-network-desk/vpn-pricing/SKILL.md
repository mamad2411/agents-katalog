# Skill: VPN Gateway Pricing (`price_skill_vpn_pricing`)

Compare VPN gateway pricing across Azure, AWS, and GCP. Covers per-hour costs, tunnel limits, throughput, P2S pricing, and when VPN is cheaper than dedicated circuits.

> **Source all rates from a live pricing API before calculating** — Azure via the `retail-prices-api` skill, AWS via the AWS Price List Query API, GCP via the Cloud Billing Catalog API. Do not embed static rates. Any $/hr or $/GB figures below are illustrative structure only; replace them with fetched values and cite the query, region/SKU/meter, currency, `effectiveStartDate`, and retrieval timestamp. Flag any number you could not fetch as `INDICATIVE — not fetched from a live pricing API`.

---

## Azure VPN Gateway Pricing

Azure VPN Gateway is billed per-hour for the gateway instance plus data transfer for egress:

| SKU | $/hr (approx.) | $/month (730 hrs) | S2S Tunnels | P2S Connections | Aggregate Throughput |
|---|---|---|---|---|---|
| Basic | $0.04 | $27 | 10 | 128 | 100 Mbps |
| VpnGw1 | $0.19 | $138 | 30 | 250 | 650 Mbps |
| VpnGw1AZ | $0.36 | $263 | 30 | 250 | 650 Mbps |
| VpnGw2 | $0.49 | $361 | 30 | 500 | 1 Gbps |
| VpnGw2AZ | $0.71 | $518 | 30 | 500 | 1 Gbps |
| VpnGw3 | $1.08 | $788 | 30 | 1,000 | 1.25 Gbps |
| VpnGw3AZ | $1.37 | $1,000 | 30 | 1,000 | 1.25 Gbps |
| VpnGw4 | $1.83 | $1,336 | 100 | 5,000 | 5 Gbps |
| VpnGw4AZ | $2.35 | $1,716 | 100 | 5,000 | 5 Gbps |
| VpnGw5 | $2.63 | $1,920 | 100 | 10,000 | 10 Gbps |
| VpnGw5AZ | $3.29 | $2,402 | 100 | 10,000 | 10 Gbps |

**Additional charges:**
- S2S tunnels: included up to SKU limit (additional tunnels not available beyond limit)
- P2S connections: first set included; additional at ~$0.01/hr per connection
- Data egress: standard Azure bandwidth pricing applies

```bash
# Check VPN Gateway SKU and utilization
az network vnet-gateway show --name <gw-name> -g <rg> \
  --query '{sku:sku.name, throughput:sku.tier}'

# Check tunnel status and bytes transferred
az network vpn-connection show --name <conn-name> -g <rg> \
  --query '{status:connectionStatus, bytesIn:ingressBytesTransferred, bytesOut:egressBytesTransferred}'
```

**Pricing page:** https://azure.microsoft.com/en-us/pricing/details/vpn-gateway/

---

## AWS Site-to-Site VPN Pricing

AWS VPN is simpler — per-connection-hour plus data transfer:

| Component | Cost |
|---|---|
| Site-to-Site VPN connection | $0.05/hr (~$36.50/month) |
| Data transfer out | Standard EC2 egress rates |
| Accelerated VPN (Global Accelerator) | $0.05/hr + $0.015/GB premium |

**Transit Gateway VPN attachment:**
| Component | Cost |
|---|---|
| TGW VPN attachment | $0.05/hr (~$36.50/month) |
| TGW data processing | $0.02/GB |

Each AWS VPN connection includes **two tunnels** for redundancy (same price).

**AWS Client VPN (P2S equivalent):**
| Component | Cost |
|---|---|
| Client VPN endpoint association | $0.10/hr per subnet (~$73/month) |
| Client VPN connection | $0.05/hr per active connection |

```bash
# Check VPN connection status
aws ec2 describe-vpn-connections --vpn-connection-ids <vpn-id> \
  --query 'VpnConnections[].{State:State,Tunnels:VgwTelemetry[].{Status:Status,BytesIn:AcceptedRouteCount}}'

# Estimate VPN costs via Cost Explorer
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-02-01 \
  --granularity MONTHLY --metrics BlendedCost \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["AWS VPN"]}}'
```

**Pricing page:** https://aws.amazon.com/vpn/pricing/

---

## GCP Cloud VPN Pricing

GCP offers Classic VPN and HA VPN:

| Component | Cost |
|---|---|
| Cloud VPN gateway (Classic) | $0.075/hr (~$54.75/month) |
| Cloud VPN gateway (HA) | $0.075/hr per tunnel (~$54.75/month/tunnel) |
| Data egress via VPN | Standard GCP egress rates (discounted vs. internet egress) |

HA VPN requires a minimum of **two tunnels** for 99.99% SLA ($109.50/month minimum).

**VPN egress discount:** Traffic over VPN uses inter-region or inter-connect pricing tiers rather than full internet egress rates.

```bash
# Check VPN tunnel status
gcloud compute vpn-tunnels describe <tunnel-name> --region <region> \
  --format='table(name,status,detailedStatus)'

# Check VPN gateway
gcloud compute vpn-gateways describe <gw-name> --region <region>
```

**Pricing page:** https://cloud.google.com/network-connectivity/docs/vpn/pricing

---

## Cross-Cloud Comparison (Equivalent Capacity)

For a typical single-site S2S VPN with ~500 Mbps throughput and 500 GB/month egress:

| Dimension | Azure (VpnGw1AZ) | AWS (S2S VPN) | GCP (HA VPN, 2 tunnels) |
|---|---|---|---|
| Gateway/hr | $0.36/hr | $0.05/hr | $0.075/hr × 2 |
| Gateway/month | $263 | $36.50 | $109.50 |
| Egress 500 GB | $43.50 | $45.00 | $10–20 (VPN discount) |
| **Total/month** | **~$307** | **~$82** | **~$125** |

> **Note:** Azure VPN Gateway pricing includes more tunnel capacity (30 tunnels on VpnGw1) and higher throughput. AWS pricing is per-connection, so multi-site deployments (10+ sites) shift the comparison. Always normalize to your specific tunnel count and bandwidth.

---

## When VPN Is Cheaper Than Dedicated Circuits

VPN is generally more cost-effective when:

| Scenario | VPN | Dedicated Circuit |
|---|---|---|
| Bandwidth < 200 Mbps | ✅ Preferred | Over-provisioned |
| Predictable high bandwidth (1+ Gbps) | Expensive SKU needed | ✅ Preferred |
| Latency-sensitive (< 10ms) | Best-effort ISP path | ✅ Private backbone |
| Multiple branch offices (50+) | Complex to manage | ✅ With SD-WAN |
| Backup/DR only | ✅ Preferred | Expensive for standby |

**Break-even rule of thumb:**
- Azure: VPN becomes more expensive than ExpressRoute 50 Mbps Metered at ~$400/month of data transfer
- AWS: Direct Connect 1 Gbps hosted (~$220/month port) breaks even at ~2 TB/month egress vs. VPN
- GCP: Partner Interconnect breaks even at ~1–2 TB/month vs. HA VPN

---

## Quick Cost Formula

```
Monthly VPN Cost = (gateway_hourly_rate × 730) + (egress_GB × egress_rate)
```

Example — Azure VpnGw2AZ with 1 TB egress:
```
= ($0.71 × 730) + (1000 × $0.087)
= $518 + $87
= $605/month
```

Rates fetched live from the provider pricing API (Azure Retail Prices / AWS Price List Query / GCP Cloud Billing Catalog) — never hard-coded; cite query, region, SKU/meter, currency, and retrieval date.
**Analysis only — verify against vendor documentation before applying.**
