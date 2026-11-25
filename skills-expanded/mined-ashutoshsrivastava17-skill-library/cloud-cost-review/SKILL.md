---
name: cloud-cost-review
description: >
  Review and optimize cloud infrastructure costs — resource utilization analysis,
  right-sizing, reserved capacity, spot/preemptible usage, and savings recommendations.
  TRIGGER when: user says /cloud-cost-review, asks to reduce cloud spend, review AWS/GCP/Azure costs,
  optimize resource utilization, or find cost savings opportunities.
argument-hint: "[cloud provider, account/project, or specific service to review]"
user-invocable: true
---

# Cloud Cost Review & Optimization

You are a senior cloud architect performing a cost optimization review. Identify waste, recommend right-sizing, and produce an actionable savings plan with estimated impact.

## Process

### Step 1: Gather Cost Context

Before reviewing, determine:
- Which cloud provider(s)? (AWS, GCP, Azure, multi-cloud)
- What is the current monthly spend and trend? (growing, stable, declining)
- What are the top cost drivers? (compute, storage, data transfer, managed services)
- What is the environment breakdown? (production, staging, development, sandbox)
- Are there existing Reserved Instances, Savings Plans, or Committed Use Discounts?
- What cost management tools are in use? (Cost Explorer, Billing Console, third-party like Vantage, Kubecost)
- Are there budget alerts configured?

### Step 2: Analyze Resource Utilization

| Resource Type | Key Metrics to Review | Right-Sizing Signal | Waste Signal |
|--------------|----------------------|---------------------|-------------|
| **Compute (EC2, GCE, VMs)** | CPU utilization, memory utilization, network I/O | Avg CPU < 20% or > 80% | Avg CPU < 5% for 7+ days |
| **Kubernetes Clusters** | Pod resource requests vs. actual usage, node utilization | Requests > 2x actual usage | Nodes with < 30% allocated |
| **Databases (RDS, CloudSQL)** | CPU, connections, IOPS, storage used vs. provisioned | Provisioned IOPS > 3x actual | Multi-AZ on non-production |
| **Storage (S3, GCS, Blob)** | Access frequency, lifecycle compliance, versioning overhead | Objects not accessed in 90 days | No lifecycle policy, unlimited versioning |
| **Data Transfer** | Cross-AZ, cross-region, internet egress | Significant cross-AZ traffic | Data transfer > 10% of total bill |
| **Load Balancers** | Request count, active connections | LB with < 100 requests/day | Unused LBs (zero traffic) |
| **Managed Services** | Provisioned vs. consumed capacity | Provisioned > 3x peak usage | Services with zero utilization |

### Step 3: Identify Savings Opportunities

#### Category 1: Eliminate Waste (Immediate, Low Risk)

| Opportunity | How to Identify | Typical Savings | Action |
|------------|-----------------|----------------|--------|
| **Idle resources** | Zero or near-zero utilization for 7+ days | 100% of resource cost | Terminate or schedule auto-stop |
| **Unattached volumes** | EBS/PD volumes with no instance attachment | 100% of volume cost | Snapshot and delete |
| **Old snapshots** | Snapshots older than retention policy | Varies, often $100s-$1000s/mo | Delete per policy |
| **Unused Elastic IPs** | Allocated but not associated | $3.65/month each | Release |
| **Oversized dev/staging** | Non-production matching production size | 50-70% of non-prod compute | Downsize non-prod |
| **Unused NAT Gateways** | NAT gateways in VPCs with no active workloads | ~$32/month + data processing | Remove |

#### Category 2: Right-Size Resources (Short-Term, Low-Medium Risk)

| Resource | Analysis Method | Recommendation Logic |
|----------|----------------|---------------------|
| **Compute instances** | 14-day CPU/memory P95 | If P95 CPU < 40%, downsize by one tier. If P95 CPU < 10%, downsize by two tiers. |
| **Database instances** | 14-day CPU P95, connection count | If P95 CPU < 30% and connections < 50% max, downsize. Consider Aurora Serverless for variable workloads. |
| **Kubernetes requests** | Compare requests to actual P99 usage | Set requests = P99 actual + 20% buffer. Set limits = 2x requests. |
| **Provisioned IOPS** | Compare provisioned to actual peak IOPS | If peak < 50% provisioned, reduce. Consider gp3 over io1/io2. |
| **Redis/Memcached** | Memory utilization, connection count | If memory usage < 40%, downsize. Consider Serverless ElastiCache. |

#### Category 3: Commitment Discounts (Medium-Term, Requires Planning)

| Discount Type | Provider | Discount Range | Commitment | Best For |
|--------------|----------|---------------|------------|----------|
| **Reserved Instances** | AWS, Azure | 30-72% | 1 or 3 years | Stable baseline compute, databases |
| **Savings Plans** | AWS | 20-66% | 1 or 3 years | Flexible compute (any instance family/region) |
| **Committed Use Discounts** | GCP | 37-55% | 1 or 3 years | Stable GCE and GKE workloads |
| **Spot/Preemptible Instances** | All providers | 60-90% | None (can be interrupted) | Stateless workloads, batch processing, CI/CD |
| **Enterprise Discount Program** | AWS, GCP, Azure | 5-20% | Annual spend commitment | Large accounts ($500K+/year) |

**Commitment Coverage Target:**
- Aim for 70-80% of stable baseline covered by commitments
- Leave 20-30% as on-demand for flexibility and growth
- Never commit to more than your minimum baseline over the commitment period

#### Category 4: Architecture Optimization (Long-Term, Higher Effort)

| Optimization | Potential Savings | Implementation Effort | Example |
|-------------|------------------|----------------------|---------|
| **Graviton/ARM migration** | 20-40% on compute | Medium | Migrate compatible workloads to ARM instances |
| **Serverless migration** | 40-80% for variable workloads | High | Move low-traffic APIs from containers to Lambda/Cloud Functions |
| **Storage tiering** | 30-70% on storage | Low-Medium | Move infrequent data to S3 IA/Glacier, GCS Nearline/Coldline |
| **Data transfer optimization** | 20-50% on transfer | Medium | Use VPC endpoints, consolidate cross-AZ traffic, use CDN |
| **Database engine optimization** | 20-50% on database | High | Migrate from licensed DB to open-source, use Aurora Serverless |
| **Container packing** | 20-40% on cluster cost | Medium | Improve bin-packing, use Karpenter/Cluster Autoscaler effectively |

### Step 4: Build a Savings Plan

Prioritize recommendations by savings impact and implementation effort:

| Priority | Criteria | Timeline |
|----------|----------|----------|
| **P0 — Quick Wins** | > $100/month savings, < 1 hour effort, no risk | This week |
| **P1 — Low Hanging Fruit** | > $500/month savings, < 1 day effort, low risk | This sprint |
| **P2 — Right-Sizing** | > $1000/month savings, requires testing | Next 2-4 weeks |
| **P3 — Commitments** | Significant savings, requires approval and planning | Next 1-2 months |
| **P4 — Architecture** | Large savings, significant engineering effort | Next quarter |

### Step 5: Implement Cost Governance

| Control | Purpose | Implementation |
|---------|---------|---------------|
| **Budget Alerts** | Detect unexpected spend increases | Set alerts at 50%, 80%, 100% of monthly budget |
| **Tagging Policy** | Attribute costs to teams/services | Require tags: `team`, `service`, `environment`, `cost-center` |
| **Quota/Limits** | Prevent accidental large resource creation | Set account-level quotas for expensive resource types |
| **Scheduled Scaling** | Reduce non-production costs outside business hours | Auto-stop dev/staging instances evenings and weekends |
| **FinOps Reviews** | Regular cost review cadence | Weekly anomaly review, monthly optimization review |
| **Cost Anomaly Detection** | Automated detection of spend spikes | Enable AWS Cost Anomaly Detection or equivalent |

### Step 6: Measure and Report

**Key FinOps Metrics:**

| Metric | Formula | Target |
|--------|---------|--------|
| **Unit Cost** | Total cost / business unit (per user, per request, per GB) | Decreasing over time |
| **Commitment Coverage** | Committed spend / total eligible spend | 70-80% |
| **Waste Ratio** | Identified waste / total spend | < 5% |
| **Cost per Environment** | Spend breakdown by environment | Non-prod < 30% of total |
| **Cost Trend** | Month-over-month spend change | Aligned with business growth |

## Output Format

```
## Cloud Cost Review: [Account/Project Name]

### Current Spend Summary
[Monthly spend, trend, top 5 cost drivers]

### Waste Identified
[Table of idle/unused resources with monthly cost]

### Right-Sizing Recommendations
[Table of resources to resize with current vs. recommended and savings]

### Commitment Opportunities
[RI/SP/CUD recommendations with discount and payback period]

### Architecture Optimizations
[Longer-term optimization opportunities]

### Savings Summary
| Category | Monthly Savings | Annual Savings | Effort |
|----------|----------------|---------------|--------|
| Waste elimination | $X | $X | Low |
| Right-sizing | $X | $X | Medium |
| Commitments | $X | $X | Low |
| Architecture | $X | $X | High |
| **Total** | **$X** | **$X** | |

### Implementation Roadmap
[Prioritized action items with owners and timelines]

### Governance Recommendations
[Tagging, budgets, alerts, review cadence]
```

## Quality Checklist

- [ ] All major resource types reviewed (compute, storage, database, network, managed services)
- [ ] Utilization data covers at least 14 days (longer for commitment decisions)
- [ ] Non-production environments reviewed separately from production
- [ ] Savings estimates are conservative (use lower bound)
- [ ] Right-sizing recommendations include a rollback plan
- [ ] Commitment recommendations do not exceed minimum baseline usage
- [ ] Tagging policy covers cost attribution to teams and services
- [ ] Budget alerts are configured with appropriate thresholds
- [ ] Recommendations include effort estimate and risk level
- [ ] Unit economics (cost per user/request) are tracked alongside absolute costs

## Edge Cases

- **Multi-Account / Organization:** Review consolidated billing for cross-account RI/SP sharing. Ensure discount benefits are attributed to the correct team. Check for orphaned accounts with active resources.
- **Kubernetes Cost Attribution:** Use Kubecost, OpenCost, or provider-native tools to attribute cluster costs to namespaces/teams. Container right-sizing requires pod-level metrics, not just node-level.
- **Data Transfer Costs:** Often hidden and significant. Map data flows between services, regions, and to the internet. Use VPC endpoints for AWS service traffic. Consider CDN for egress-heavy workloads.
- **Spot Instance Management:** Use mixed instance policies with multiple instance types. Implement graceful shutdown handling. Never run stateful or single-instance workloads on spot. Use spot for CI/CD runners, batch jobs, and horizontal scale-out tiers.
- **Licensing Costs:** Windows and commercial database licenses add significant cost. Consider BYOL (Bring Your Own License) or migration to open-source alternatives. Factor license costs into right-sizing decisions.
- **Growth Planning:** Do not optimize for today's usage if a launch or traffic increase is planned within the commitment window. Use Savings Plans (flexible) over Reserved Instances (rigid) when growth is uncertain.
