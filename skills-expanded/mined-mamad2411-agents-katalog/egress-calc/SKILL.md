# Skill: Egress & Data Transfer Cost Calculation (`price_skill_egress_calc`)

Calculate data transfer and egress costs across Azure, AWS, and GCP. Covers internet egress, inter-region, inter-AZ, VNet/VPC peering, and CDN offload savings.

> **Source all rates from a live pricing API before calculating** — Azure via the `retail-prices-api` skill, AWS via the AWS Price List Query API, GCP via the Cloud Billing Catalog API. Do not embed static rates. Any per-GB/per-hour figures shown below are illustrative structure only; replace them with fetched values and cite the query, region/SKU/meter, currency, `effectiveStartDate`, and retrieval timestamp. Flag any number you could not fetch as `INDICATIVE — not fetched from a live pricing API`.

---

## Azure Data Transfer Pricing

### Internet Egress (from Azure to Internet)

Data **into** Azure (ingress) is free. Outbound (egress) follows zone- and destination-specific tiered pricing.

> **Pricing assumption reviewed 2026-05-29:** Azure bandwidth pricing advertises the first 100 GB/month of internet egress free globally, then paid tiered rates. Treat any per-GB numbers in examples as illustrative only — verify current rates in the Azure Pricing Calculator or bandwidth pricing page before budgeting.

### Inter-Region Data Transfer

Traffic between Azure regions within the same continent:

| Route | Price per GB |
|---|---|
| Within same region | Free |
| Between regions (same continent) | ~$0.02 |
| Between continents | ~$0.05 – $0.08 |

### VNet Peering Data Transfer

| Peering Type | Ingress per GB | Egress per GB |
|---|---|---|
| Intra-region VNet peering | $0.01 | $0.01 |
| Global VNet peering | $0.035 – $0.075 | $0.035 – $0.075 |

```bash
# Check Azure egress metrics
az monitor metrics list --resource <nic-resource-id> \
  --metric "BytesTransmitted" --interval PT1H --aggregation Total

# Check VNet peering traffic
az network vnet peering show --name <peering-name> \
  --resource-group <rg> --vnet-name <vnet> --query '{status:peeringState}'
```

**Pricing page:** https://azure.microsoft.com/en-us/pricing/details/bandwidth/

---

## AWS Data Transfer Pricing

### Internet Egress (from AWS to Internet)

Data **into** AWS is free. Outbound pricing:

| Monthly Volume | Price per GB |
|---|---|
| First 100 GB | Free (Free Tier) |
| Up to 10 TB | $0.09 |
| 10 TB – 40 TB | $0.085 |
| 40 TB – 100 TB | $0.070 |
| 100 TB – 150 TB | $0.050 |
| 150 TB+ | Contact AWS |

### Inter-AZ Data Transfer

This is the hidden cost on AWS — traffic between Availability Zones in the same region:

| Route | Price per GB |
|---|---|
| Same AZ (using private IP) | Free |
| Cross-AZ (each direction) | $0.01 |

A typical multi-AZ deployment with 1 TB/month cross-AZ traffic costs **$20/month** ($0.01 × 1000 GB × 2 directions).

### Inter-Region Data Transfer

| Route | Price per GB |
|---|---|
| US regions to other US regions | $0.02 |
| US to Europe/Asia | $0.02 – $0.09 |

### VPC Peering Data Transfer

| Peering Type | Price per GB |
|---|---|
| Same region (each direction) | $0.01 |
| Cross-region (each direction) | $0.02 |

```bash
# Check AWS data transfer with Cost Explorer
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-02-01 \
  --granularity MONTHLY --metrics BlendedCost \
  --filter '{"Dimensions":{"Key":"USAGE_TYPE","Values":["DataTransfer-Out-Bytes"]}}'

# Check VPC Flow Logs for traffic volume
aws ec2 describe-flow-logs --filter Name=resource-id,Values=<vpc-id>

# Check NAT Gateway data processed
aws cloudwatch get-metric-statistics --namespace AWS/NATGateway \
  --metric-name BytesOutToDestination --dimensions Name=NatGatewayId,Value=<id> \
  --period 2592000 --statistics Sum --start-time 2024-01-01 --end-time 2024-02-01
```

**Pricing page:** https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer

---

## GCP Data Transfer Pricing

### Internet Egress

GCP offers **Premium** and **Standard** network service tiers with different pricing:

| Monthly Volume | Premium Tier (per GB) | Standard Tier (per GB) |
|---|---|---|
| 0 – 1 TB | $0.12 | $0.085 |
| 1 – 10 TB | $0.11 | $0.065 |
| 10 TB+ | $0.08 | $0.045 |

Standard tier routes through ISP networks (higher latency, lower cost). Premium tier uses Google's backbone (lower latency, higher cost).

### Inter-Region Data Transfer

| Route | Price per GB |
|---|---|
| Same zone | Free |
| Same region, different zone | $0.01 |
| Between regions (same continent) | $0.01 – $0.02 |
| Between continents | $0.05 – $0.08 |

### VPC Peering

Traffic within the same region over VPC peering is charged at the same rates as intra-VPC cross-zone traffic. Cross-region peering follows inter-region pricing.

```bash
# Check GCP egress metrics
gcloud monitoring time-series list \
  --filter='metric.type="compute.googleapis.com/instance/network/sent_bytes_count"' \
  --interval-start-time="2024-01-01T00:00:00Z"

# Check billing export for network costs
bq query --use_legacy_sql=false \
  'SELECT service.description, SUM(cost) as total_cost
   FROM `project.dataset.gcp_billing_export_v1_*`
   WHERE service.description LIKE "%Network%"
   GROUP BY 1 ORDER BY 2 DESC'
```

**Pricing page:** https://cloud.google.com/vpc/network-pricing

---

## CDN Offload Savings

Serving static content through a CDN is typically 40-60% cheaper than direct egress and reduces origin load:

| Service | Per-GB Egress (approx.) |
|---|---|
| Azure direct egress | $0.087 |
| Azure CDN (Standard) | $0.065 |
| Azure Front Door | $0.060 |
| AWS direct egress | $0.09 |
| CloudFront | $0.085 (US/EU) |
| GCP direct egress (Premium) | $0.12 |
| Cloud CDN | $0.08 |

**CDN savings example:** 5 TB/month of static content:
- Direct Azure egress: 5000 GB × $0.087 = **$435/month**
- Via Azure CDN: 5000 GB × $0.065 = **$325/month**
- Savings: **$110/month ($1,320/year)**

---

## Output Template

Use this template for egress cost estimates:

```markdown
## Data Transfer Cost Estimate

**Region:** [e.g., East US / us-east-1 / us-central1]
**Period:** Monthly

| # | Source | Destination | Monthly GB | $/GB | Monthly Cost |
|---|--------|-------------|-----------|------|-------------|
| 1 | Azure East US | Internet | 500 | $0.087 | $43.50 |
| 2 | Azure East US | Azure West US | 200 | $0.02 | $4.00 |
| 3 | AWS us-east-1 AZ-a | AWS us-east-1 AZ-b | 1000 | $0.01 × 2 | $20.00 |
| 4 | GCP us-central1 | Internet (Premium) | 300 | $0.12 | $36.00 |
| 5 | VNet Peering (intra-region) | — | 100 | $0.01 × 2 | $2.00 |
| | **Total** | | **2100** | | **$105.50** |

### Optimization Opportunities
- Move static content to CDN → est. savings: $XX/month
- Consolidate cross-region traffic → est. savings: $XX/month
- Compress API responses (est. 60% reduction) → est. savings: $XX/month
```

---

## Key Tips

1. **Ingress is free** on all three clouds — cost is always on the sending side for internet egress.
2. **Inter-AZ on AWS** is the silent killer — multi-AZ architectures with chatty services can generate significant costs at $0.01/GB each way.
3. **GCP Premium vs Standard tier** — if latency tolerance allows, Standard tier saves 25-50%.
4. **VNet/VPC peering** is charged bidirectionally on Azure and AWS — both sides pay.
5. **NAT Gateway data processing** adds on top of egress — on AWS it is $0.045/GB processed, often overlooked.
6. **Private endpoints / Private Link** — data processing charges apply (~$0.01/GB on Azure) but avoid internet egress pricing.

Rates fetched live from the provider pricing API (Azure Retail Prices / AWS Price List Query / GCP Cloud Billing Catalog) — never hard-coded; cite query, region, SKU/meter, currency, and retrieval date.
**Analysis only — verify against vendor documentation before applying.**
