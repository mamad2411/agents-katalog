# Skill: Dedicated Circuit Pricing (`price_skill_circuit_pricing`)

Pricing for dedicated private connectivity: Azure ExpressRoute, AWS Direct Connect, and GCP Cloud Interconnect. Includes port fees, data plans, partner costs, and break-even analysis against VPN.

> **Source all rates from a live pricing API before calculating** — Azure via the `retail-prices-api` skill, AWS via the AWS Price List Query API, GCP via the Cloud Billing Catalog API. Do not embed static rates. Any port-fee or $/GB figures below are illustrative structure only; replace them with fetched values and cite the query, region/SKU/meter, currency, `effectiveStartDate`, and retrieval timestamp. Flag any number you could not fetch as `INDICATIVE — not fetched from a live pricing API`.

---

## Azure ExpressRoute Pricing

### Port Fees (Monthly)

ExpressRoute circuits are billed for the port plus an optional data plan:

| Speed | Provider Port ($/month) | ExpressRoute Direct Port ($/month) |
|---|---|---|
| 50 Mbps | $55 | — |
| 100 Mbps | $110 | — |
| 200 Mbps | $220 | — |
| 500 Mbps | $550 | — |
| 1 Gbps | $1,100 | — |
| 2 Gbps | $1,700 | — |
| 5 Gbps | $3,600 | — |
| 10 Gbps | $6,000 | $5,500 |
| 40 Gbps | — | $20,000 |
| 100 Gbps | — | $50,000 |

### Data Plans

| Plan | How It Works | Best For |
|---|---|---|
| **Metered** | Port fee + $0.025/GB egress | Variable/low bandwidth |
| **Unlimited** | Port fee + flat unlimited surcharge | High/predictable bandwidth |
| **Local SKU** | Port fee only (free egress to local region) | Single-region workloads near peering location |

Unlimited surcharge varies by speed (e.g., ~$550/month for 1 Gbps unlimited on top of port fee).

### ExpressRoute Add-Ons

| Feature | Cost |
|---|---|
| Global Reach (ER-to-ER transit) | $0.05/GB |
| Premium Add-on (cross-geo peering) | +50-100% port fee |
| FastPath (bypass gateway for data plane) | Included with Ultra/ErGw3AZ |
| ExpressRoute Gateway (ErGw1Az) | ~$0.19/hr ($139/month) |
| ExpressRoute Gateway (ErGw3Az) | ~$1.07/hr ($781/month) |

```bash
# Check ExpressRoute circuit details and usage
az network express-route show --name <circuit-name> -g <rg> \
  --query '{sku:sku, bandwidth:bandwidthInMbps, peeringLocation:peeringLocation}'

# Check ExpressRoute circuit stats
az network express-route stats show --name <circuit-name> -g <rg>

# List available peering locations
az network express-route list-service-providers --query '[].{Provider:name, Locations:peeringLocations}'
```

**Pricing page:** https://azure.microsoft.com/en-us/pricing/details/expressroute/

---

## AWS Direct Connect Pricing

### Port-Hour Fees

AWS Direct Connect is billed per port-hour:

| Speed | Type | $/hr | $/month (730 hrs) |
|---|---|---|---|
| 1 Gbps | Dedicated | $0.30 | $219 |
| 10 Gbps | Dedicated | $1.50 | $1,095 |
| 100 Gbps | Dedicated | $13.70 | $10,001 |
| 50 Mbps – 500 Mbps | Hosted Connection | $0.03 – $0.14 | $22 – $102 |

### Data Transfer Out (varies by region)

| Source Region | $/GB Out |
|---|---|
| US East (N. Virginia) | $0.02 |
| US West (Oregon) | $0.02 |
| Europe (Ireland) | $0.02 |
| Asia Pacific (Tokyo) | $0.04 |
| South America (São Paulo) | $0.06 |

Data transfer **in** via Direct Connect is free.

### Transit Gateway with Direct Connect

| Component | Cost |
|---|---|
| DX Gateway | Free |
| Transit Gateway attachment | $0.05/hr (~$36.50/month) |
| TGW data processing | $0.02/GB |

```bash
# Check Direct Connect connections
aws directconnect describe-connections \
  --query 'connections[].{Id:connectionId,Bandwidth:bandwidth,State:connectionState,Location:location}'

# Check virtual interfaces
aws directconnect describe-virtual-interfaces \
  --query 'virtualInterfaces[].{Name:virtualInterfaceName,Type:virtualInterfaceType,Vlan:vlan,State:virtualInterfaceState}'

# Check data transfer costs
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-02-01 \
  --granularity MONTHLY --metrics BlendedCost \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["AWS Direct Connect"]}}'
```

**Pricing page:** https://aws.amazon.com/directconnect/pricing/

---

## GCP Cloud Interconnect Pricing

### Dedicated Interconnect

| Speed | VLAN Attachment ($/month) | Port Fee |
|---|---|---|
| 10 Gbps | $1,700/month per attachment | Included |
| 100 Gbps | $17,000/month per attachment | Included |

Minimum of one 10 Gbps connection. Production SLA requires two connections in different edge availability domains.

### Partner Interconnect

| Speed | $/month (approx.) |
|---|---|
| 50 Mbps | $55 |
| 100 Mbps | $110 |
| 200 Mbps | $165 |
| 500 Mbps | $275 |
| 1 Gbps | $550 |
| 2 Gbps | $825 |
| 5 Gbps | $1,375 |
| 10 Gbps | $1,700 |

### Egress Discounts with Interconnect

Traffic egressing through Interconnect receives discounted pricing compared to internet egress:

| Monthly Volume | Interconnect Egress ($/GB) | Internet Egress Premium ($/GB) |
|---|---|---|
| 0 – 1 TB | $0.02 | $0.12 |
| 1 – 10 TB | $0.02 | $0.11 |
| 10 TB+ | $0.02 | $0.08 |

```bash
# Check Interconnect attachments
gcloud compute interconnects attachments list --format='table(name,region,bandwidth,state)'

# Check interconnect details
gcloud compute interconnects describe <interconnect-name> \
  --format='table(name,interconnectType,linkType,requestedLinkCount,state)'
```

**Pricing page:** https://cloud.google.com/network-connectivity/docs/interconnect/pricing

---

## Break-Even Analysis: VPN vs. Dedicated Circuit

### Azure — VPN vs. ExpressRoute

| Monthly Egress | VPN (VpnGw1AZ) | ER 50 Mbps Metered | Winner |
|---|---|---|---|
| 100 GB | $263 + $9 = $272 | $55 + $3 = $58 | **ER** |
| 500 GB | $263 + $44 = $307 | $55 + $13 = $68 | **ER** |
| 2 TB | $263 + $174 = $437 | $55 + $50 = $105 | **ER** |
| 5 TB | $263 + $419 = $682 | $55 + $125 = $180 | **ER** |

> Azure VPN gateways are more expensive per-hour than ER circuits at lower speeds. ER is often cheaper even at modest bandwidth — the break-even favors ER quickly if you need reliable bandwidth.

### AWS — VPN vs. Direct Connect

| Monthly Egress | S2S VPN | DX 1 Gbps Hosted ($22/mo) | Winner |
|---|---|---|---|
| 100 GB | $37 + $9 = $46 | $22 + $2 = $24 | **DX** |
| 1 TB | $37 + $90 = $127 | $22 + $20 = $42 | **DX** |
| 5 TB | $37 + $430 = $467 | $22 + $100 = $122 | **DX** |

> AWS VPN is cheap per-hour but egress adds up. DX hosted connections at lower speeds can be very cost-effective even at modest volumes, especially with partner pricing.

### GCP — VPN vs. Partner Interconnect

| Monthly Egress | HA VPN (2 tunnels) | Partner 100 Mbps | Winner |
|---|---|---|---|
| 100 GB | $110 + $12 = $122 | $110 + $2 = $112 | **Comparable** |
| 1 TB | $110 + $110 = $220 | $110 + $20 = $130 | **Interconnect** |
| 5 TB | $110 + $440 = $550 | $110 + $100 = $210 | **Interconnect** |

---

## TCO Template

```markdown
## 3-Year TCO: [Connection Type]

| Cost Component | Monthly | Annual | 3-Year |
|---|---|---|---|
| Port/circuit fee | $X | $X | $X |
| Data transfer (est. Y TB/mo) | $X | $X | $X |
| Gateway instance | $X | $X | $X |
| Redundancy (2nd circuit) | $X | $X | $X |
| Cross-connect / colocation | $X | $X | $X |
| Partner/provider MRC | $X | $X | $X |
| **Total** | **$X** | **$X** | **$X** |

### Assumptions
- Region: [region]
- Monthly egress: [X] TB
- Redundancy: [single/dual]
- Pricing as of: [date]
```

Rates fetched live from the provider pricing API (Azure Retail Prices / AWS Price List Query / GCP Cloud Billing Catalog) — never hard-coded; cite query, region, SKU/meter, currency, and retrieval date.
**Analysis only — verify against vendor documentation before applying.**
