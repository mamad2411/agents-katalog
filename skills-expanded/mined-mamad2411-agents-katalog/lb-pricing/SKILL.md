# Skill: Load Balancer Pricing (`price_skill_lb_pricing`)

Compare load balancer and traffic distribution pricing across Azure, AWS, and GCP. Covers L4/L7 load balancers, CDN/Front Door, and DNS-based routing.

> **Source all rates from a live pricing API before calculating** — Azure via the `retail-prices-api` skill, AWS via the AWS Price List Query API, GCP via the Cloud Billing Catalog API. Do not embed static rates. Any figures below are illustrative structure only; replace them with fetched values and cite the query, region/SKU/meter, currency, `effectiveStartDate`, and retrieval timestamp. Flag any number you could not fetch as `INDICATIVE — not fetched from a live pricing API`.

---

## Azure Load Balancer Pricing

### Standard Load Balancer

| Component | Cost |
|---|---|
| First 5 rules | Free |
| Per additional rule | ~$0.025/hr ($18.25/month) |
| Data processed | $0.005/GB |

Basic Load Balancer is free but deprecated for production — no SLA, no AZ support.

### Application Gateway v2

| Component | Cost |
|---|---|
| Fixed cost | ~$0.246/hr ($179.58/month) |
| Capacity unit (CU) | ~$0.008/hr per CU |

Each CU provides: 2,500 persistent connections, 2.22 Mbps throughput, or 1 compute unit. You pay for whichever dimension is highest.

**WAF on App Gateway:** Application Gateway WAF v2 adds ~$0.443/hr fixed cost ($323/month) + same CU charges.

### Azure Front Door

| Component | Standard | Premium |
|---|---|---|
| Base fee | ~$35/month | ~$330/month |
| Per request (first 100M) | $0.01 per 10K | $0.012 per 10K |
| Data transfer from edge | $0.06 – $0.16/GB (by zone) | $0.06 – $0.16/GB |
| Custom domains | 5 free, then $0.01/day | 15 free, then $0.01/day |
| WAF custom rules | $5/month per policy | Included |

### Traffic Manager

| Component | Cost |
|---|---|
| DNS queries (first 1B) | $0.54 per million |
| Health checks (Azure endpoints) | Free |
| Health checks (external) | $0.36 per 1,000 checks/month |
| Real user measurements | $2 per million measurements |

```bash
# Check LB rules and data processed
az network lb show --name <lb-name> -g <rg> \
  --query '{sku:sku.name, rules:loadBalancingRules[].name}'

# Check Application Gateway metrics
az monitor metrics list --resource <appgw-id> \
  --metric "CurrentCapacityUnits" --interval PT1H

# Check Front Door usage
az afd profile show --profile-name <name> -g <rg>
```

**Pricing pages:**
- https://azure.microsoft.com/en-us/pricing/details/load-balancer/
- https://azure.microsoft.com/en-us/pricing/details/application-gateway/
- https://azure.microsoft.com/en-us/pricing/details/frontdoor/

---

## AWS Elastic Load Balancing Pricing

### Application Load Balancer (ALB)

| Component | Cost |
|---|---|
| Per hour | $0.0225/hr (~$16.43/month) |
| LCU-hour | $0.008/LCU-hr |

Each LCU provides: 25 new connections/sec, 3,000 active connections, 1 GB/hr for EC2 targets or 0.4 GB/hr for Lambda, or 1,000 rule evaluations/sec. Billed on the highest dimension.

### Network Load Balancer (NLB)

| Component | Cost |
|---|---|
| Per hour | $0.0225/hr (~$16.43/month) |
| NLCU-hour | $0.006/NLCU-hr |

Each NLCU: 800 new TCP connections/sec, 100,000 active connections, or 1 GB/hr.

### Gateway Load Balancer (GLB)

| Component | Cost |
|---|---|
| Per hour | $0.0125/hr (~$9.13/month) |
| GLCU-hour | $0.004/GLCU-hr |

### CloudFront (CDN)

| Component | US/EU | Asia Pacific | South America |
|---|---|---|---|
| HTTP requests (per 10K) | $0.0075 | $0.0090 | $0.016 |
| HTTPS requests (per 10K) | $0.01 | $0.012 | $0.022 |
| Data transfer out (first 10 TB) | $0.085/GB | $0.114/GB | $0.110/GB |

```bash
# Check ALB metrics
aws cloudwatch get-metric-statistics --namespace AWS/ApplicationELB \
  --metric-name ConsumedLCUs --dimensions Name=LoadBalancer,Value=<lb-arn-suffix> \
  --period 2592000 --statistics Average --start-time 2024-01-01 --end-time 2024-02-01

# Estimate ALB monthly cost
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-02-01 \
  --granularity MONTHLY --metrics BlendedCost \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["Elastic Load Balancing"]}}'
```

**Pricing pages:**
- https://aws.amazon.com/elasticloadbalancing/pricing/
- https://aws.amazon.com/cloudfront/pricing/

---

## GCP Load Balancing Pricing

### Forwarding Rules

| Component | Cost |
|---|---|
| First 5 forwarding rules | $0.025/hr each (~$18.25/month each) |
| Additional rules (6+) | $0.010/hr each (~$7.30/month each) |

### Data Processing

| LB Type | Data Processing $/GB |
|---|---|
| Regional internal/external (L4) | $0.008/GB |
| Global external HTTP(S) | $0.008 – $0.012/GB |
| Internal HTTP(S) | $0.008/GB |

### Cloud CDN

| Component | Cost |
|---|---|
| Cache egress (US/EU) | $0.08/GB |
| Cache fill | $0.01/GB |
| HTTP requests (per 10K) | $0.0075 |
| Cache invalidation | $0.005/invalidation |

```bash
# Check forwarding rules
gcloud compute forwarding-rules list --format='table(name,region,target,IPAddress,loadBalancingScheme)'

# Check LB utilization
gcloud monitoring time-series list \
  --filter='metric.type="loadbalancing.googleapis.com/https/request_count"'
```

**Pricing page:** https://cloud.google.com/vpc/network-pricing#lb

---

## Cost Comparison — Typical Workloads

### Small Workload (1 LB, 100 req/sec, 100 GB/month data)

| Component | Azure (Std LB) | AWS (ALB) | GCP (L7 LB) |
|---|---|---|---|
| Fixed/hourly | ~$0 (≤5 rules) | $16.43 | $18.25 |
| Data/LCU | $0.50 | ~$6 | $0.80 |
| **Total/month** | **~$1** | **~$23** | **~$19** |

### Medium Workload (L7 LB + WAF, 1K req/sec, 1 TB/month)

| Component | Azure (AppGW v2 + WAF) | AWS (ALB) | GCP (Global L7) |
|---|---|---|---|
| Fixed/hourly | $323 | $16.43 | $18.25 |
| Capacity/LCU | ~$44 | ~$60 | $10 |
| **Total/month** | **~$367** | **~$76** | **~$28** |

### Large Workload (Global LB + CDN, 10K req/sec, 10 TB/month)

| Component | Azure (Front Door Premium) | AWS (ALB + CloudFront) | GCP (Global L7 + CDN) |
|---|---|---|---|
| Fixed | $330 | $16.43 | $18.25 |
| Requests | ~$13 | ~$65 | ~$65 |
| Data transfer | ~$600 | ~$850 | ~$800 |
| **Total/month** | **~$943** | **~$931** | **~$883** |

> **Note:** Azure Standard Load Balancer is extremely cost-effective for simple L4 balancing. For L7 with WAF, AWS ALB is significantly cheaper than Azure Application Gateway. At global scale with CDN, costs converge across clouds.

---

## Key Considerations

1. **Azure Standard LB** has near-zero cost for basic L4 — hard to beat for simple TCP/UDP load balancing.
2. **AWS LCU pricing** makes cost proportional to actual usage — good for variable workloads but harder to predict.
3. **GCP forwarding rule charges** apply even to idle load balancers — clean up unused rules.
4. **WAF costs** vary dramatically: Azure WAF on App Gateway is expensive ($323/month fixed); AWS WAF is separate ($5/month + $1/rule + $0.60/M requests); GCP Cloud Armor starts at $5/policy + $1/rule.
5. **CDN + LB combined** — evaluate whether Front Door/CloudFront/Cloud CDN can replace a regional LB for globally distributed traffic.

Rates fetched live from the provider pricing API (Azure Retail Prices / AWS Price List Query / GCP Cloud Billing Catalog) — never hard-coded; cite query, region, SKU/meter, currency, and retrieval date.
**Analysis only — verify against vendor documentation before applying.**
