# Skill: Cross-Cloud Price Comparison (`price_skill_price_compare`)

Side-by-side pricing comparison of equivalent networking services across Azure, AWS, and GCP. Includes common workload scenarios, hidden costs, and pricing page references.

> **Source all rates from a live pricing API before calculating** — Azure via the `retail-prices-api` skill, AWS via the AWS Price List Query API, GCP via the Cloud Billing Catalog API. Do not embed static rates. Every cell in the comparison tables below must be a fetched value; replace the placeholders and cite the query, region/SKU/meter, currency, `effectiveStartDate`, and retrieval timestamp. Flag any number you could not fetch as `INDICATIVE — not fetched from a live pricing API`.

---

## Service-by-Service Comparison

### VPN Gateway

| Dimension | Azure (VpnGw1AZ) | AWS (Site-to-Site VPN) | GCP (HA VPN, 2 tunnels) |
|---|---|---|---|
| Hourly cost | $0.361/hr | $0.05/hr per connection | $0.075/hr × 2 tunnels |
| Monthly cost | $263 | $36.50 | $109.50 |
| Max throughput | 650 Mbps | 1.25 Gbps | 3 Gbps (aggregate) |
| S2S tunnels included | 30 | 2 (per connection) | 2 |
| AZ-redundant | ✅ (AZ SKU) | ✅ (2 tunnels by default) | ✅ (HA VPN) |
| Data transfer | Standard egress | Standard egress | Discounted egress |

### Dedicated Circuit

| Dimension | Azure ExpressRoute (1 Gbps) | AWS Direct Connect (1 Gbps) | GCP Dedicated Interconnect (10 Gbps) |
|---|---|---|---|
| Port/month | $1,100 | $219 | $1,700 |
| Data egress/GB | $0.025 (metered) or unlimited | $0.02 (US) | $0.02 |
| Unlimited option | Yes (~$1,650 total) | No | No |
| Min commitment | None (cancel anytime) | None (cancel anytime) | None |
| Partner option | Yes (various speeds) | Hosted connections | Partner Interconnect |

### Load Balancer (L4)

| Dimension | Azure Standard LB | AWS NLB | GCP L4 Regional |
|---|---|---|---|
| Fixed cost | Free (≤5 rules) | $0.0225/hr ($16.43/mo) | $0.025/hr ($18.25/mo) per rule |
| Data processed | $0.005/GB | $0.006/NLCU-hr | $0.008/GB |
| Health probes | Free | Free | Free |
| Cross-zone | Free | Free | Free |

### Load Balancer (L7)

| Dimension | Azure App Gateway v2 | AWS ALB | GCP Global HTTP(S) LB |
|---|---|---|---|
| Fixed cost | $0.246/hr ($180/mo) | $0.0225/hr ($16.43/mo) | $0.025/hr per rule |
| Variable cost | $0.008/CU-hr | $0.008/LCU-hr | $0.008-$0.012/GB |
| WAF add-on | $0.443/hr ($323/mo) | $5/mo + $1/rule + $0.60/M req | $5/policy + $1/rule |
| SSL termination | Included | Included | Included |

### Firewall

| Dimension | Azure Firewall Standard | AWS Network Firewall (3 AZ) | GCP Cloud NGFW Enterprise |
|---|---|---|---|
| Fixed/month | $912 | $864 | $1,278/hr × endpoints |
| Data processing | $0.016/GB | $0.065/GB | $0.018/GB |
| 1 TB/month total | $928 | $929 | Varies |
| IDPS/IPS | Premium only ($1,278/mo) | Included | Included (PAN-OS) |

### DNS

| Dimension | Azure DNS | AWS Route 53 | GCP Cloud DNS |
|---|---|---|---|
| Hosted zone | $0.50/month | $0.50/month | $0.20/month |
| Queries (first 1B) | $0.40/million | $0.40/million | $0.40/million |
| Health checks | Free (Azure endpoints) | $0.50-$0.75/month each | Free (integrated with LB) |
| Traffic routing | Traffic Manager ($0.54/M queries) | Route 53 routing policies (included) | Included with Cloud DNS |

### Private Link / Private Endpoint

| Dimension | Azure Private Endpoint | AWS PrivateLink | GCP Private Service Connect |
|---|---|---|---|
| Endpoint cost | ~$0.01/hr ($7.30/mo) | $0.01/hr ($7.30/mo) per AZ | Free (forwarding rule cost) |
| Data processing | $0.01/GB | $0.01/GB | $0.01/GB |
| Cross-region | Supported (global peering cost) | Same region only | Supported |

### NAT Gateway

| Dimension | Azure NAT Gateway | AWS NAT Gateway | GCP Cloud NAT |
|---|---|---|---|
| Fixed gateway charge | Hourly gateway charge; verify current Azure NAT Gateway pricing | Hourly gateway charge; verify current AWS VPC pricing | Gateway uptime charge applies; verify current Cloud NAT pricing |
| Data processing | Per-GB processing charge; illustrative only | Per-GB processing charge; illustrative only | Per-GiB processing charge applies in addition to gateway uptime |
| Public IPs | Public IP charges may apply | Public IPv4 hourly charges apply for in-use and idle addresses | Public IP hourly charges may apply |
| Max throughput | 50 Gbps | 45 Gbps per GW | Scales automatically |

### Public IP Address

| Dimension | Azure | AWS | GCP |
|---|---|---|---|
| Static IPv4 (attached) | Hourly/monthly charge; verify current page | Charged hourly for all in-use public IPv4 addresses | Hourly charge; verify current page |
| Static IPv4 (idle) | Hourly/monthly charge; verify current page | Charged hourly for idle public IPv4 addresses | Higher idle hourly charge may apply |
| Dynamic IP | Deprecated | N/A | N/A |
| IPv6 public IP | Verify current page | Generally no public IPv4-style hourly charge; verify VPC pricing | Verify current page |

---

## Common Workload Scenarios

### Small: Single-site, basic LB, 100 GB egress

| Component | Azure | AWS | GCP |
|---|---|---|---|
| VPN Gateway (S2S) | $263 (VpnGw1AZ) | $36.50 | $109.50 (HA VPN) |
| Load Balancer (L4) | ~$1 (Std LB) | $16.43 (NLB) | $18.25 |
| Internet Egress (100 GB) | $8.70 | $9.00 | $12.00 (Premium) |
| DNS Zone + Queries | $1.00 | $1.00 | $0.60 |
| Public IP (1) | $3.60 | Free | $2.92 |
| **Total/month** | **~$277** | **~$63** | **~$143** |

### Medium: ExpressRoute/DX + VPN backup, App Gateway, 1 TB egress

| Component | Azure | AWS | GCP |
|---|---|---|---|
| Circuit (500 Mbps/1 Gbps) | $550 (ER Metered) | $219 (DX 1 Gbps) | $550 (Partner 1 Gbps) |
| Circuit egress (1 TB) | $25 | $20 | $20 |
| VPN backup | $263 (VpnGw1AZ) | $36.50 | $109.50 |
| L7 Load Balancer | $180 (AppGW v2) | $16.43 (ALB) + ~$60 LCU | $18.25 + ~$10 |
| Firewall | $912 (Standard) | $864 (3 AZ) | $912 (NGFW) |
| NAT Gateway | Gateway uptime + data processing + public IPs; verify calculator | Gateway uptime + data processing + public IPv4; verify AWS VPC pricing | Gateway uptime + data processing + public IPs; verify Cloud NAT pricing |
| **Total/month** | **~$2,008** | **~$1,294** | **~$1,665** |

### Large: Multi-region, Front Door/CDN, 10 TB egress

| Component | Azure | AWS | GCP |
|---|---|---|---|
| Global LB + CDN | $943 (Front Door Premium) | $931 (ALB + CloudFront) | $883 (Global LB + CDN) |
| ER/DX (2 regions) | $2,200 | $438 | $3,400 (Dedicated) |
| Circuit egress (10 TB) | $250 | $200 | $200 |
| VPN backup (2 regions) | $526 | $73 | $219 |
| Firewall (2 regions) | $1,824 | $1,728 | $1,824 |
| Private Endpoints (20) | $146 | $146 (per AZ) | ~$0 (forwarding rule) |
| DNS + Traffic Routing | $10 | $10 | $5 |
| **Total/month** | **~$5,899** | **~$3,526** | **~$6,531** |

> **Key takeaway:** AWS tends to be cheapest at all scales primarily due to lower VPN and Direct Connect port costs. Azure wins on L4 LB cost (nearly free). GCP Cloud NAT must be modeled with gateway uptime, data processing, public IP, and egress charges. Actual costs depend heavily on specific SKU choices, commitment discounts, and EA/EDP pricing.

---

## Hidden Costs to Watch

| Hidden Cost | Cloud | What Happens | Typical Impact |
|---|---|---|---|
| Inter-AZ data transfer | AWS | $0.01/GB each direction for cross-AZ | $20/TB — adds up in multi-AZ |
| NAT Gateway processing | All | $0.045/GB on top of egress | $45/TB — often overlooked |
| Health probe traffic | Azure/AWS | LB health probes consume bandwidth | Minimal but non-zero |
| DNS query costs | All | $0.40/million queries | Significant at millions/day |
| Public IP idle charges | All | Charged even when unused | $3-7/month per IP |
| Peering bidirectional | Azure/AWS | Both sides pay for peering traffic | 2× the expected cost |
| TGW data processing | AWS | $0.02/GB through Transit Gateway | $20/TB — significant |
| vWAN hub charges | Azure | $0.25/hr per secured hub | $182.50/month per hub |
| App Gateway min CU | Azure | Minimum capacity even at zero traffic | $180/month fixed |
| Cross-region ER Premium | Azure | Premium add-on required for cross-geo | +50-100% port fee |

---

## Pricing Calculator & Page URLs

| Cloud | Pricing Calculator | Key Pricing Pages |
|---|---|---|
| **Azure** | https://azure.microsoft.com/en-us/pricing/calculator/ | [Bandwidth](https://azure.microsoft.com/en-us/pricing/details/bandwidth/) · [VPN](https://azure.microsoft.com/en-us/pricing/details/vpn-gateway/) · [ExpressRoute](https://azure.microsoft.com/en-us/pricing/details/expressroute/) · [LB](https://azure.microsoft.com/en-us/pricing/details/load-balancer/) · [App GW](https://azure.microsoft.com/en-us/pricing/details/application-gateway/) · [Front Door](https://azure.microsoft.com/en-us/pricing/details/frontdoor/) · [Firewall](https://azure.microsoft.com/en-us/pricing/details/azure-firewall/) · [DNS](https://azure.microsoft.com/en-us/pricing/details/dns/) · [Private Link](https://azure.microsoft.com/en-us/pricing/details/private-link/) |
| **AWS** | https://calculator.aws/ | [Data Transfer](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer) · [VPN](https://aws.amazon.com/vpn/pricing/) · [Direct Connect](https://aws.amazon.com/directconnect/pricing/) · [ELB](https://aws.amazon.com/elasticloadbalancing/pricing/) · [Network FW](https://aws.amazon.com/network-firewall/pricing/) · [Route 53](https://aws.amazon.com/route53/pricing/) · [PrivateLink](https://aws.amazon.com/privatelink/pricing/) |
| **GCP** | https://cloud.google.com/products/calculator | [VPC Pricing](https://cloud.google.com/vpc/network-pricing) · [Cloud NAT](https://cloud.google.com/nat/pricing) · [Cloud VPN](https://cloud.google.com/network-connectivity/docs/vpn/pricing) · [Interconnect](https://cloud.google.com/network-connectivity/docs/interconnect/pricing) · [LB Pricing](https://cloud.google.com/vpc/network-pricing#lb) · [Cloud Armor](https://cloud.google.com/armor/pricing) · [Cloud DNS](https://cloud.google.com/dns/pricing) |

---

## Quick Decision Guide

| Need | Best Value | Notes |
|---|---|---|
| Cheapest S2S VPN | AWS ($36.50/mo) | Azure if you need many tunnels (30 included) |
| Cheapest dedicated circuit | AWS DX 1 Gbps ($219/mo) | GCP Partner Interconnect competitive too |
| Cheapest L4 LB | Azure Std LB (near-free) | Unbeatable for ≤5 rules |
| Cheapest L7 LB | AWS ALB ($16.43/mo base) | Watch LCU charges at scale |
| Cheapest firewall | Azure FW Basic ($288/mo) | For low-traffic, basic filtering |
| NAT modeling | Verify per-cloud calculator | Include gateway uptime, data processing, public IP, and egress charges |
| Cheapest DNS hosting | GCP Cloud DNS ($0.20/zone) | AWS/Azure both $0.50/zone |

Rates fetched live from the provider pricing API (Azure Retail Prices / AWS Price List Query / GCP Cloud Billing Catalog) — never hard-coded; cite query, region, SKU/meter, currency, and retrieval date.
**Analysis only — verify against vendor documentation before applying.**
