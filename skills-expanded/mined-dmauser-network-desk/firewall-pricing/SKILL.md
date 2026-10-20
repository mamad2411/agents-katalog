# Skill: Firewall Pricing (`price_skill_firewall_pricing`)

Compare firewall pricing across cloud-native services and third-party NVAs (Network Virtual Appliances). Covers Azure Firewall, AWS Network Firewall, GCP Cloud Armor, and marketplace NVAs.

> **Source all rates from a live pricing API before calculating** — Azure via the `retail-prices-api` skill, AWS via the AWS Price List Query API, GCP via the Cloud Billing Catalog API. Do not embed static rates. Any $/hr or $/GB figures below are illustrative structure only; replace them with fetched values and cite the query, region/SKU/meter, currency, `effectiveStartDate`, and retrieval timestamp. Flag any number you could not fetch as `INDICATIVE — not fetched from a live pricing API`.

---

## Azure Firewall Pricing

| SKU | Deployment $/hr | Deployment $/month (730 hrs) | Data Processing $/GB |
|---|---|---|---|
| Basic | $0.395 | $288 | $0.065 |
| Standard | $1.25 | $912 | $0.016 |
| Premium | $1.75 | $1,278 | $0.016 |

### What Each SKU Includes

| Feature | Basic | Standard | Premium |
|---|---|---|---|
| L3/L4 filtering | ✅ | ✅ | ✅ |
| Threat intelligence | Alerts only | Alerts + deny | Alerts + deny |
| FQDN filtering | ✅ | ✅ | ✅ |
| IDPS | ❌ | ❌ | ✅ (signature-based) |
| TLS inspection | ❌ | ❌ | ✅ |
| URL filtering | ❌ | ❌ | ✅ |
| Web categories | ❌ | ✅ | ✅ |

### Azure Firewall Manager

| Component | Cost |
|---|---|
| Secured virtual hub (vWAN) | $0.25/hr ($182.50/month) per hub deployment |
| Firewall policies | Free (management plane) |

```bash
# Check Azure Firewall SKU and metrics
az network firewall show --name <fw-name> -g <rg> --query '{sku:sku, threatIntel:threatIntelMode}'

# Check data processed
az monitor metrics list --resource <firewall-resource-id> \
  --metric "DataProcessed" --interval PT1H --aggregation Total
```

**Pricing page:** https://azure.microsoft.com/en-us/pricing/details/azure-firewall/

---

## AWS Network Firewall Pricing

| Component | Cost |
|---|---|
| Firewall endpoint (per AZ) | $0.395/hr (~$288/month) |
| Data processed | $0.065/GB |

A typical multi-AZ deployment with endpoints in **3 AZs** costs:
- Endpoints: 3 × $288 = **$864/month**
- Data (1 TB): 1000 × $0.065 = **$65/month**
- **Total: ~$929/month**

```bash
# Check Network Firewall status
aws network-firewall describe-firewall --firewall-name <name> \
  --query 'Firewall.{Name:FirewallName,Status:FirewallStatus.Status}'

# Check data processed metrics
aws cloudwatch get-metric-statistics --namespace AWS/NetworkFirewall \
  --metric-name ProcessedBytes --dimensions Name=FirewallName,Value=<name> \
  --period 2592000 --statistics Sum --start-time 2024-01-01 --end-time 2024-02-01
```

**Pricing page:** https://aws.amazon.com/network-firewall/pricing/

---

## GCP Cloud Armor Pricing

Cloud Armor is a WAF/DDoS service, not a full network firewall. Pricing is per-policy and per-request:

| Component | Standard Tier | Plus Tier |
|---|---|---|
| Security policy | $5/month per policy | $5/month per policy |
| Per rule | $1/month per rule | $1/month per rule |
| Requests (first 1M) | $0.75 per million | $0.75 per million |
| Requests (1M – 10M) | $0.60 per million | $0.60 per million |
| Adaptive protection | ❌ | Included |
| Bot management | ❌ | Included |
| Plus subscription | — | $3,000/month |

### GCP Cloud Firewall (VPC Firewall Rules)

Standard VPC firewall rules are **free**. Hierarchical Firewall Policies and Cloud NGFW (powered by Palo Alto Networks) have additional costs:

| Component | Cost |
|---|---|
| VPC firewall rules | Free |
| Cloud NGFW Standard (FQDN, geo-filtering) | $0.018/GB |
| Cloud NGFW Enterprise (IPS/IDS by PAN-OS) | $0.018/GB + $1.75/hr per endpoint |

```bash
# List Cloud Armor policies and rules
gcloud compute security-policies list --format='table(name,type)'
gcloud compute security-policies describe <policy-name> --format='table(rules[].priority,rules[].action)'
```

**Pricing page:** https://cloud.google.com/armor/pricing

---

## NVA (Network Virtual Appliance) Pricing

Third-party firewalls on cloud marketplaces combine VM compute costs with software licensing:

### Palo Alto Networks VM-Series

| Component | Cost (approx.) |
|---|---|
| VM-300 equivalent (4 vCPU) | $0.50 – $1.00/hr compute |
| PAYG license (Bundle 1) | ~$1.05/hr |
| PAYG license (Bundle 2 - NGFW) | ~$1.76/hr |
| BYOL | $0 runtime (annual license ~$5K–$50K) |
| **Total PAYG (Bundle 2)** | **~$2.76/hr ($2,015/month)** |

### Fortinet FortiGate

| Component | Cost (approx.) |
|---|---|
| FortiGate-VM04 (4 vCPU) | $0.40 – $0.80/hr compute |
| PAYG license (NGFW) | ~$0.84/hr |
| BYOL | $0 runtime (annual license ~$3K–$20K) |
| **Total PAYG** | **~$1.64/hr ($1,197/month)** |

### Check Point CloudGuard

| Component | Cost (approx.) |
|---|---|
| vSEC (4 vCPU) | $0.40 – $0.80/hr compute |
| PAYG license (NGTP) | ~$1.25/hr |
| BYOL | $0 runtime (annual license varies) |
| **Total PAYG** | **~$2.05/hr ($1,497/month)** |

> **BYOL vs PAYG:** For sustained use (24×7), BYOL is typically 30-50% cheaper over 3 years. PAYG is better for dev/test, burst capacity, or proof-of-concept.

---

## Cost at Different Throughput Levels

| Monthly Data | Azure FW Standard | Azure FW Premium | AWS NFW (3 AZ) | NVA (FortiGate PAYG) |
|---|---|---|---|---|
| 100 GB | $912 + $2 = $914 | $1,278 + $2 = $1,280 | $864 + $7 = $871 | $1,197 + $0 = $1,197 |
| 500 GB | $912 + $8 = $920 | $1,278 + $8 = $1,286 | $864 + $33 = $897 | $1,197 |
| 1 TB | $912 + $16 = $928 | $1,278 + $16 = $1,294 | $864 + $65 = $929 | $1,197 |
| 5 TB | $912 + $80 = $992 | $1,278 + $80 = $1,358 | $864 + $325 = $1,189 | $1,197 |
| 10 TB | $912 + $160 = $1,072 | $1,278 + $160 = $1,438 | $864 + $650 = $1,514 | $1,197 |

> **Key insight:** Cloud-native firewalls have lower fixed costs but per-GB charges add up. NVAs have higher fixed costs but no per-GB charges — making them cheaper at high throughput (typically 5+ TB/month). Azure Firewall Basic ($288/month) is compelling for small workloads with light traffic.

---

## Decision Framework

| Factor | Cloud-Native FW | NVA (3rd party) |
|---|---|---|
| Low traffic (< 1 TB/month) | ✅ Cheaper | Over-provisioned |
| High traffic (> 5 TB/month) | Per-GB costs grow | ✅ Flat cost |
| Advanced L7 features (IPS/IDS) | Azure FW Premium / AWS NFW | ✅ More mature |
| Operational complexity | Low (PaaS managed) | Higher (patching, HA) |
| Multi-cloud consistency | ❌ Different per cloud | ✅ Same vendor everywhere |
| HA requirements | Built-in | Must design (active/passive, GWLB) |

Rates fetched live from the provider pricing API (Azure Retail Prices / AWS Price List Query / GCP Cloud Billing Catalog) — never hard-coded; cite query, region, SKU/meter, currency, and retrieval date.
**Analysis only — verify against vendor documentation before applying.**
