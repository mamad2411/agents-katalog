---
name: cloud-cost-optimization
description: Finds and reduces cloud spend on AWS, Azure, GCP and Kubernetes - cost visibility and tagging, rightsizing, autoscaling and scheduling, idle and orphaned resources, storage tiers, commitment discounts, spot capacity, data transfer and logging costs, and unit economics. Use when the cloud bill is too high or rising, when asked to cut costs, review spend, set budgets or tagging, estimate the cost of a design, or before buying reserved capacity or savings plans.
license: MIT
---

# Cloud Cost Optimization

Make cost visible before cutting it, then work the biggest line items first. Most savings come from a few levers: things that are idle, things that are oversized, things that run when nobody uses them, and data that moves or is kept when it doesn't need to be. **Never delete, resize or stop resources, or purchase commitments, without the user's explicit confirmation.** Recommend; let the owner decide.

## When to use

- The bill is high, rising, or surprising; someone asks "where is the money going?"
- Setting up budgets, alerts, tagging or cost allocation.
- Estimating the running cost of a new design or a pull request.
- Deciding whether to buy reserved instances, savings plans or committed-use discounts.

## Workflow

1. **Get the breakdown.** Pull the last 3-6 months by service, account/subscription/project, region and tag from the provider's cost tool (AWS Cost Explorer / Data Exports, Azure Cost Management, GCP Billing reports or billing export to BigQuery). Note the trend, not just the total.
2. **Pareto it.** List the top 5-10 line items; they usually hold most of the spend. Ignore the long tail for now.
3. **Attribute.** For each top item, find the owning team/service. If you can't, fix tagging first (see Visibility).
4. **Find waste** in each top item using the levers below, in order: idle and orphaned, off-hours, oversized, wrong pricing model, data transfer, storage, observability volume.
5. **Estimate savings** for each finding from current usage and the provider's pricing pages or calculator. Show assumptions. Don't quote prices from memory; they change.
6. **Propose changes** as a ranked list: saving, effort, risk, owner. Mark anything with data-loss or availability risk.
7. **Make approved changes through code** (IaC or config), not console clicks, so they stick (see `infrastructure-as-code`).
8. **Measure** the effect after a full billing cycle and add guardrails so the waste doesn't return.

## Visibility first

- **Tag/label everything** with at least: `owner` (team), `service`, `environment`, `cost-center`. Enforce with policy (AWS tag policies / SCPs, Azure Policy, GCP organization policies) and in IaC modules.
- On AWS, user-defined tags only appear in billing once activated as **cost allocation tags**.
- Shared costs (networking, shared clusters, support plans) need an explicit allocation rule.
- Kubernetes: cluster cost is shared; use a cost allocation tool such as OpenCost or Kubecost to split by namespace/label.
- **Budgets and anomaly alerts** per account/team (AWS Budgets and Cost Anomaly Detection, Azure budgets and cost alerts, GCP budgets and alerts). Route alerts to the owning team, not a shared inbox nobody reads.
- **Unit economics**: track cost per request, per customer, per order or per GB processed. Total spend rising with growth is fine; cost per unit rising is the real problem.

## Levers

### 1. Idle and orphaned resources

| Resource | How to find |
| --- | --- |
| Unattached disks / volumes | AWS `aws ec2 describe-volumes --filters Name=status,Values=available`; Azure `az disk list --query "[?diskState=='Unattached']"`; GCP `gcloud compute disks list --filter="-users:*"` |
| Unused static/public IPs | AWS `aws ec2 describe-addresses --query "Addresses[?AssociationId==null]"` (AWS also charges for in-use public IPv4); GCP `gcloud compute addresses list --filter="status=RESERVED"` |
| Old snapshots and images | Snapshots older than the retention policy with no linked AMI/image or restore plan |
| Idle load balancers, NAT gateways | No or near-zero traffic in metrics over weeks |
| Stopped VMs with attached premium disks | Compute is free while stopped; disks and IPs are not |
| Forgotten environments | Dev/test/demo stacks with no deploys or traffic for weeks |
| Idle databases and caches | Near-zero connections or CPU over weeks |

Before deleting: confirm the owner, snapshot or back up if there's any doubt, and get explicit approval.

### 2. Run only when needed

- Schedule non-production compute off outside working hours and weekends (instance schedulers, scale node pools or deployments to zero, stop dev databases where supported).
- Autoscale production on load; set sensible minimums and maximums.
- Prefer scale-to-zero or serverless for spiky or low, intermittent traffic; prefer always-on instances for steady high utilization (per-request pricing gets expensive at sustained load).

### 3. Rightsize

- Use p95/p99 CPU and memory over 2-4 weeks, not averages, and include peak periods. Memory metrics on VMs often need an agent.
- Use provider recommendations as a starting point (AWS Compute Optimizer, Azure Advisor, GCP Recommender), then check against the workload's real peaks.
- Kubernetes: rightsize **requests** (they drive node count), then let the cluster autoscaler shrink nodes.
- Move to current-generation instance families and, where the software supports it, ARM-based instances, after testing.
- Databases: check whether size is driven by CPU, memory, IOPS or storage before changing tiers.

### 4. Pricing model

| Workload | Model |
| --- | --- |
| Steady 24/7 baseline after rightsizing | Commitment discounts: AWS Savings Plans / Reserved Instances, Azure Reservations / savings plan for compute, GCP committed use discounts |
| Interruptible, stateless, batch, CI runners, fault-tolerant workers | Spot / Spot VMs (preemptible), with interruption handling |
| Spiky or unknown | On-demand until the pattern is known |

- Rightsize and remove waste **before** committing; otherwise you lock in the waste.
- Commit only to the stable floor of usage, not the peak. Check current coverage and utilization of existing commitments first.
- Purchasing commitments is a financial commitment for 1-3 years. Present the analysis; the user or finance makes the purchase.
- Check licensing benefits you already own (for example Azure Hybrid Benefit for Windows Server and SQL Server).
- GCP applies sustained use discounts automatically to eligible VMs; factor them into comparisons.

### 5. Data transfer

- Internet egress, cross-region and often cross-zone traffic are billed; ingress is usually free.
- **NAT gateways** charge per GB processed. Route traffic to cloud storage and other provider services through private/VPC endpoints where available (AWS gateway endpoints for S3 and DynamoDB carry no hourly or data processing charge).
- Keep chatty services and their databases in the same region (and zone where availability allows).
- Serve static and cacheable content through a CDN; compress responses.
- Watch replication, backups and logs shipped across regions or to third-party tools.

### 6. Storage

- Lifecycle policies to move old objects to cheaper tiers and expire what you don't need: S3 lifecycle rules / Intelligent-Tiering, Azure Blob access tiers (Hot, Cool, Cold, Archive) with lifecycle management, GCP Cloud Storage classes (Standard, Nearline, Coldline, Archive) with Object Lifecycle Management.
- Check retrieval fees and minimum storage durations before moving data to cold tiers.
- On AWS, gp3 volumes are usually cheaper than gp2 for the same baseline performance; verify against your IOPS needs.
- Delete incomplete multipart uploads and old object versions per a retention policy.
- Set retention on snapshots and backups to what policy requires, not forever.

### 7. Observability and logging

- Log volume and retention are often a top-10 line item. Drop debug logs in production, sample high-volume info logs, and set retention per log type.
- High-cardinality metric labels (user IDs, request IDs) multiply time series and cost (see `observability`).
- Sample traces instead of keeping 100%.

### 8. Architecture and managed services

- Compare managed vs self-hosted including people time, on-call and upgrades, not just the infrastructure line.
- Caching (see `caching-strategies`) and fixing N+1 queries (see `sql-optimization`) cut database size more than tier changes.
- Add cost to design reviews: estimate monthly cost at expected and 10x load.

## Guardrails so it stays fixed

- Cost diff in pull requests for IaC changes (for example Infracost).
- Policies that require tags and block oversized or unapproved resource types in non-production.
- TTLs or auto-cleanup for ephemeral environments.
- Monthly review of top movers per team; anomaly alerts routed to owners.

## Anti-patterns

- **Buying commitments first**, before removing idle and oversized resources.
- **Rightsizing from averages**, then falling over at peak.
- **Deleting "unused" resources without an owner check or backup.**
- **Optimizing the long tail** while the top three line items go unexamined.
- **Console changes** that IaC reverts on the next apply.
- **Cutting redundancy** (single zone, no replicas) to save money without an explicit, owned availability decision.
- **Quoting prices from memory** instead of current pricing pages or calculators.

## Done when

- Top line items are attributed to owners via tags/allocation, with budgets and anomaly alerts in place.
- A ranked list of findings exists with estimated savings, risk and owner; approved changes are made in code.
- No resources were deleted, resized or commitments bought without explicit confirmation.
- Savings are measured after a billing cycle and guardrails prevent regression.
