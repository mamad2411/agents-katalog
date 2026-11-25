---
name: cost-optimization-checklist
description: >-
  Azure cost optimization checklist covering waste elimination, right-sizing,
  commitment discounts, and governance. Actionable steps for reducing Azure
  spend without architecture changes.
when-to-use: >-
  Invoke when reviewing Azure spend, right-sizing resources, evaluating
  reservations or savings plans, eliminating waste, or establishing cost
  governance practices for a team or subscription.
categories:
  - cost
  - finops
  - governance
  - azure
---

# Cost Optimization Checklist

Right-size first. Eliminate waste second. Buy commitments third. In that order.

---

## Waste Elimination (Fastest Savings)

### Common Waste Patterns

| Waste Type | Detection | Typical Savings |
|---|---|---|
| Unattached managed disks | Azure Advisor, Resource Graph | 100% of disk cost |
| Idle public IP addresses | No associated NIC or LB | ~$3.65/month each (adds up) |
| Non-production running 24/7 | No auto-shutdown configured | 65%+ with 10h/day schedule |
| Orphaned resources | No traffic/connections 30+ days | 100% of resource cost |
| Unused App Service plans | No apps deployed | 100% of plan cost |
| Old snapshots | Created > 30 days, no retention policy | Storage costs |
| Stopped VMs with Premium disks | VM deallocated, disk still billed | Full disk cost |
| Unused Application Gateways | No backend pools, zero traffic | ~$250/month WAF v2 |
| ExpressRoute circuits not in use | Provider status != Provisioned | $200–$10,000/month |
| Log Analytics over-ingestion | Noisy diagnostics, verbose logging | 20–50% of monitoring cost |

### Detection

- [ ] Review Azure Advisor cost recommendations weekly
- [ ] Run Resource Graph queries for unattached disks, orphaned IPs, orphaned NICs
- [ ] Schedule Azure Automation reports for weekly orphaned resource detection
- [ ] Apply Azure Policy to audit unattached disks and idle public IPs

### Log Analytics Optimization

- [ ] Check top tables by ingestion volume — AzureDiagnostics, ContainerLog are common offenders
- [ ] Disable verbose diagnostic settings on non-critical resources
- [ ] Use resource-specific diagnostic settings instead of legacy AzureDiagnostics
- [ ] Enable Application Insights adaptive sampling
- [ ] Use Basic Logs tier for high-volume, low-query tables (90% cost reduction)
- [ ] Compare ingestion against commitment tier thresholds

---

## Right-Sizing (Highest Impact)

### VM Right-Sizing

- [ ] Monitor CPU, memory, disk IOPS, network for 2+ weeks
- [ ] Flag VMs consistently below 30% utilization across all metrics
- [ ] Downsize to next smaller SKU in same family
- [ ] Validate application performance after resize

**SKU Selection:**

| Series | Best For |
|---|---|
| B-series | Variable workloads, low average CPU (web, dev) |
| D-series | Balanced general purpose (default choice) |
| E-series | Memory-intensive (databases, caching) |
| F-series | Compute-intensive (batch, gaming) |
| L-series | Storage-intensive (big data) |

### App Service Right-Sizing

- [ ] Monitor CPU and memory percentage — below 40% means overprovisioned
- [ ] Reduce instance count if autoscale rarely triggers
- [ ] Use Free/Basic tiers for dev/test
- [ ] Consolidate low-traffic apps onto shared plans
- [ ] Schedule reduced instance count for nights/weekends

### Database Right-Sizing

- [ ] SQL: Review DTU vs vCore — many databases overpay on wrong model
- [ ] SQL: Use elastic pools for databases with variable usage
- [ ] SQL: Evaluate serverless compute tier for intermittent workloads
- [ ] SQL: Challenge Premium tier — General Purpose often suffices
- [ ] Cosmos DB: Enable autoscale throughput, consider serverless for dev/test
- [ ] Cosmos DB: Review partition key design — poor keys force over-provisioning

### Container Right-Sizing

- [ ] Set CPU and memory requests based on actual observed usage, not defaults
- [ ] Use VPA recommendations to right-size pod resource requests
- [ ] Right-size AKS node SKU to match pod resource profiles
- [ ] Enable cluster autoscaler with appropriate min/max bounds

---

## Automation — Start/Stop Schedules

Non-production running 24/7 is the easiest savings:

| Schedule | Running Hours | Savings |
|---|---|---|
| 10h/day × 5 days/week | 50/168 hours | ~70% |
| 12h/day × 7 days/week | 84/168 hours | ~50% |

- [ ] Configure auto-shutdown on all non-production VMs
- [ ] Use tags (`AutoShutdown=true`) to identify scheduled resources
- [ ] Apply to AKS node pools, App Service plans, and VMs
- [ ] Use DevTest Labs for built-in auto-shutdown/start policies

---

## Commitment Discounts (Buy After Right-Sizing)

### Decision Tree

1. **Interruptible workload?** → Spot VMs (up to 90% savings)
2. **Dev/test workload?** → Dev/Test pricing subscription (~55% off Windows/SQL)
3. **Stable SKU/region for 1-3 years?** → Reservation (30-72% savings)
4. **Stable but size/region may change?** → Savings Plan (15-65% savings)
5. **Short-lived or unpredictable?** → Pay-as-you-go

### Stacking Strategy

1. Buy **reservations first** for stable base — highest discount rate
2. Buy **savings plans** for variable portion — flexibility for shifting workloads
3. Apply **Azure Hybrid Benefit** on top for Windows/SQL workloads
4. Target **80%+ utilization** across all commitments
5. Set utilization alerts — notify if below 80%

### When to Buy Reservations

- [ ] Workload has run stable for 30+ days at consistent utilization
- [ ] No planned migration or decommission within commitment term
- [ ] Azure Advisor shows recommendation with high confidence

---

## Governance Cadence

| Frequency | Action |
|---|---|
| Weekly | Review Azure Advisor cost recommendations |
| Weekly | Check for new orphaned/idle resources |
| Monthly | Full orphaned resource sweep across subscriptions |
| Monthly | Review resources with zero traffic for 30+ days |
| Quarterly | Review with application owners — validate all resources needed |
| Quarterly | Audit commitment utilization — exchange underperforming reservations |
| Quarterly | Review Log Analytics ingestion trends and commitment tier fit |

---

## Tagging for Cost Allocation

Every taggable resource gets these minimum tags:

| Tag | Purpose | Example |
|---|---|---|
| `Environment` | Deployment stage | `dev`, `staging`, `prod` |
| `Project` | Business project | `contoso-api` |
| `Owner` | Responsible team | `platform-engineering` |
| `CostCenter` | Billing allocation | `CC-12345` |
| `ManagedBy` | IaC tool | `terraform`, `Bicep` |

- [ ] Enforce mandatory tags via Azure Policy (deny deployment without required tags)
- [ ] Use tag inheritance policies for resource groups → resources
- [ ] Build cost allocation views in Cost Management using tags

## Related Skills

- `naming-conventions` — Azure resource naming and tagging standards
- `iac-review` — Infrastructure code review including cost considerations
