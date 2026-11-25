---
name: finops-cost-optimizer
description: "Cloud FinOps cost optimization: tagging, rightsizing, autoscaling, purchase options, storage tiering, egress reduction, idle cleanup, budgets. Use when reducing cloud spend."
---

# FinOps Cost Optimizer

## Overview

Cloud bills grow silently. Engineers ship features; each one adds compute, storage, and data transfer costs that compound until Finance notices a spike. FinOps is the discipline that closes the loop: make cost visible to every engineer, assign ownership, and optimize continuously — not in a quarterly panic.

This skill covers the full stack of cloud cost levers: allocation via tagging, right-sizing compute, purchase commitments, storage tiering, egress minimization, idle resource cleanup, serverless traps, unit economics, and the cultural machinery that makes savings stick.

**Core principle:** COST IS AN ENGINEERING METRIC. Every deployment decision has a dollar consequence — engineers who can see it make better trade-offs.

## The Iron Law

```
NO RESOURCE PROVISIONED WITHOUT A COST OWNER, A TAG, AND A BUDGET ALERT
```

## When to Use

**Use this when:**
- Cloud spend is growing faster than business metrics
- Teams cannot answer "what does this service cost to run?"
- A new workload is being architected and cost must be designed in
- Purchase commitment renewals (reserved instances, savings plans) are approaching
- Storage buckets, snapshots, or EBS volumes are accumulating without lifecycle policies
- A cost anomaly alert has fired and root cause is unknown

**Use this ESPECIALLY when:**
- Someone says "we'll deal with cost optimization later" (later is always more expensive)
- A service is being moved from on-prem to cloud and the estimate is "it'll be cheaper"
- Serverless functions are being proposed for high-throughput, always-on workloads
- Engineering teams have no visibility into the costs their features generate

**Don't skip when:**
- Under time pressure to ship (cheap-by-default costs five minutes; retrofitting costs days)
- The workload seems small (small workloads multiplied across many services are the bulk of most bills)

## Cost Visibility and Allocation

### Mandatory Tagging Schema

Tags are the foundation of every downstream optimization. Without them, cost data is a blob. A minimal enforced schema:

| Tag Key | Example Value | Purpose |
|---|---|---|
| `team` | `platform-infra` | Showback / chargeback to team |
| `service` | `payments-api` | Per-service cost tracking |
| `env` | `prod` / `staging` / `dev` | Filter non-prod from commitment analysis |
| `cost-center` | `CC-1042` | Finance chargeback alignment |
| `managed-by` | `terraform` | Identifies IaC-managed vs. manual |

Enforce tagging at provisioning time via AWS Service Control Policies, GCP Organization Policies, or Azure Policy. Any resource missing required tags is flagged in the daily cost report and blocks deployment pipelines on the next PR cycle.

**Showback vs. chargeback:** Showback means teams see their cost; chargeback means it hits their budget. Start with showback to build the culture, then move to chargeback once tagging coverage exceeds 95%.

### Budget Alerts Configuration

Set three alert tiers per service and per team:

```yaml
# AWS Budgets example (Terraform)
resource "aws_budgets_budget" "payments_api" {
  name         = "payments-api-monthly"
  budget_type  = "COST"
  limit_amount = "4000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["platform-infra@example.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = ["platform-infra@example.com", "engineering-vp@example.com"]
  }
}
```

Enable anomaly detection (AWS Cost Anomaly Detection, GCP Budget anomaly alerts, Azure Cost Anomaly Detector) with a minimum threshold of $50 or 20% week-over-week change, whichever triggers first.

## Rightsizing Compute

### Decision Table

Before choosing an instance type or container resource request, answer these four questions:

| Question | Low Answer → | High Answer → |
|---|---|---|
| Is workload CPU-bound or memory-bound? | Compute-optimized (c-series) | Memory-optimized (r-series) |
| Is traffic steady or spiky? | Reserved / committed use | Autoscaling + spot/preemptible |
| Is p99 latency < 50 ms required? | Burstable (t/e-series) unsafe | Dedicated compute |
| Does workload run < 6 h/day? | Spot/preemptible + schedule | Savings plan candidate |

**Practical rightsizing process:**
1. Pull 14-day CPU and memory utilization (CloudWatch, Cloud Monitoring, Azure Monitor).
2. If average CPU < 15% and peak < 40%, downsize one instance family tier (e.g., `m5.2xlarge` → `m5.xlarge`).
3. If average memory < 30%, consider compute-optimized over general purpose.
4. For Kubernetes, use Vertical Pod Autoscaler (VPA) in recommendation mode for two weeks, then apply the p95 recommendation as the new `requests` value.

Never rightsize on less than seven days of data. Never rightsize during a known traffic spike window.

## Autoscaling and Scale-to-Zero

### Design for Zero When Idle

| Workload Type | Scale-to-Zero Strategy |
|---|---|
| HTTP API (low SLA) | AWS Lambda / Cloud Run — scale to zero natively |
| HTTP API (SLA < 100 ms cold start budget) | ECS/GKE min=1 with scheduled scale-down nights/weekends |
| Batch jobs | Spot fleet + event-driven trigger; zero when no queue depth |
| Dev/staging environments | Scheduled shutdown 20:00–07:00 weekdays, full weekend off |
| CI build agents | Ephemeral runners (GitHub Actions hosted / Buildkite elastic) |

Autoscaling target CPU utilization should be set at 60–70% for steady workloads, not the default 80%, to leave headroom before the next scale-out event. Scale-in cooldown must be at least 5 minutes to prevent thrash.

## Purchase Options

Commitment instruments produce the largest single-line savings (20–60%) but carry risk if utilization assumptions are wrong. Sequence:

1. **Baseline first:** run on-demand for 60–90 days on new workloads to establish a stable baseline.
2. **Spot/preemptible for interruptible work:** batch, ML training, CI, canary environments. Size spot fleets with a diversity of 3+ instance types to reduce interruption impact.
3. **Savings Plans or Committed Use Discounts for the baseline:** cover only the floor — the minimum compute you will always need. Use the "Coverage" report in Cost Explorer to identify that floor.
4. **Reserved Instances for predictable, single-instance-type workloads** (RDS, ElastiSearch, Redshift) where flexibility is not required.
5. **Never commit more than 70% of current spend** in the first commitment cycle — usage can drop with optimization work.

Review commitments quarterly. Unused reserved capacity is pure waste; sell unused RIs on the AWS Marketplace or let them expire without renewal.

## Storage Tiering and Lifecycle Policies

### S3 / GCS / Azure Blob Lifecycle Example

```json
{
  "Rules": [
    {
      "ID": "log-archive-tiering",
      "Filter": { "Prefix": "logs/" },
      "Status": "Enabled",
      "Transitions": [
        { "Days": 30,  "StorageClass": "STANDARD_IA" },
        { "Days": 90,  "StorageClass": "GLACIER_IR" },
        { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
      ],
      "Expiration": { "Days": 2555 }
    }
  ]
}
```

**Rules of thumb:**
- Objects not accessed in 30 days → Infrequent Access (40–45% savings).
- Objects not accessed in 90 days → Glacier Instant Retrieval (68% savings).
- Audit logs not needed for < 7 years → expire at retention boundary.
- Enable S3 Intelligent-Tiering for buckets where access patterns are unknown and object size > 128 KB.
- Delete unattached EBS volumes weekly via Lambda or AWS Config rule `ec2-volume-inuse-check`.
- Delete orphaned snapshots older than 90 days unless tagged `retain=true`.

## Data Egress and Transfer Cost Reduction

Egress charges are the most invisible cost driver. Cross-region and internet egress can exceed compute spend for data-heavy workloads.

**Reduction checklist:**
- **Same-region placement:** co-locate services that exchange large payloads in the same region and availability zone. AZ-to-AZ transfer within a region costs $0.01/GB on AWS — significant at scale.
- **CDN for static assets:** assets served via CloudFront, Cloud CDN, or Azure Front Door avoid origin egress for repeat requests.
- **VPC endpoints / Private Google Access:** S3, DynamoDB, and GCS access via VPC endpoint avoids NAT Gateway charges ($0.045/GB on AWS NAT vs. $0.00/GB via endpoint).
- **Compression before transfer:** GZIP or Zstandard on API responses and inter-service payloads; measure payload size reduction with `Content-Encoding` metrics in your APM.
- **Avoid multi-region replication for non-DR data:** replicate only what your RTO/RPO requires.

## Serverless Cost Traps

Serverless is not always cheaper. It becomes expensive when:

| Trap | Symptom | Fix |
|---|---|---|
| High-frequency invocations | Lambda costs more than equivalent ECS task at >10M req/month | Move to always-on container with autoscaling |
| Large payload per invocation | 128 KB+ event bodies inflate duration × memory billing | Offload payload to S3, pass reference |
| Cold start mitigation via Provisioned Concurrency | Provisioned concurrency costs same as EC2 reserved | Reconsider if latency SLA allows warm instance |
| DynamoDB on-demand at sustained throughput | On-demand 6–7× more expensive than provisioned at stable load | Switch to provisioned capacity + auto-scaling |
| Step Functions Express vs. Standard | Standard Workflows billed per state transition ($0.025/1K) | Use Express for high-freq, short-duration flows |

## Unit Economics and Cost-per-Feature

Track cost as a rate per business unit, not just total spend:

- **Cost per API request** = monthly compute cost ÷ monthly request count
- **Cost per active user** = monthly total cloud cost ÷ monthly active users
- **Cost per transaction** = (compute + storage + egress) ÷ transactions processed

Publish these metrics to an engineering dashboard alongside latency and error rate. When a new feature ships, compare cost-per-request before and after. A feature that increases cost-per-request by 15% must either justify the value or be optimized within two sprints.

## Red Flags — STOP and Follow Process

If you observe any of the following, halt provisioning or deployment and resolve first:

- A resource has no `team` or `service` tag
- Compute instances are sized at more than 2× the observed peak utilization
- An S3 bucket older than 30 days has no lifecycle policy and no `retain=true` tag
- Dev or staging resources are running 24/7 without a scheduled shutdown
- A commitment purchase is being proposed before 60 days of on-demand usage history exists
- Monthly egress costs exceed 20% of total monthly bill without a documented CDN or endpoint strategy
- A Lambda function is flagged as running > 1 million invocations/day without a cost comparison to containers

**ALL of these mean: STOP. Add the tag, policy, or analysis before proceeding.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We'll optimize cost after we launch" | By launch, the architecture is set; retrofitting autoscaling and tagging costs three sprints. |
| "Spot instances are too risky for production" | Stateless services behind a load balancer tolerate spot interruption gracefully with a two-instance-type fleet and graceful shutdown handling. |
| "Reserved instances are too hard to manage" | Compute Savings Plans require zero instance-type choices and cover all EC2/Fargate usage; an hour to purchase, immediate savings. |
| "The bill is high but the business is growing" | Cost-per-unit should stay flat or fall as volume grows; a rising cost-per-unit signals an architecture problem, not a growth tax. |
| "Engineers shouldn't worry about cost, that's Finance's job" | Engineers make every provisioning decision; Finance can only see the outcome. Cost awareness at the point of decision is the only scalable control. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Which team owns this?" — resources lack cost tags; allocation is impossible
- "Why did the bill jump last Tuesday?" — no anomaly detection or cost-tagged deployment events
- "We're paying for things we don't use" — no idle resource cleanup or scheduled shutdown
- "The savings plan is underutilized" — over-committed relative to actual baseline
- "Our egress bill is huge" — data architecture places services in wrong regions or lacks CDN/endpoints

**When you see these:** STOP. Run the relevant diagnostic from this skill before continuing any feature work.

## Related Skills

- **cloud-security-auditor** — security guardrails on the same IAM, network, and storage resources targeted by cost optimization; run in parallel, not sequentially
- **devops-release-engineer** — deployment pipelines are the enforcement point for tagging policies and scheduled scaling; coordinate tag-enforcement gates here
- **observability-pro** — cost anomaly investigation requires the same telemetry (metrics, logs, traces) as reliability investigation; shared instrumentation reduces duplication
- **terraform-pro** — infrastructure-as-code is the authoritative location for resource tagging, lifecycle policies, and autoscaling configuration; all cost controls must live in IaC, not the console

## Verification

- [ ] All resources in scope have `team`, `service`, `env`, and `cost-center` tags
- [ ] Budget alerts configured at 80% actual and 100% forecasted for each service
- [ ] Cost anomaly detection enabled with a $50 or 20% WoW threshold
- [ ] Compute utilization reviewed against 14-day baseline before any sizing decision
- [ ] S3/GCS/Blob buckets have lifecycle policies or are tagged `retain=true` with justification
- [ ] No orphaned EBS volumes, unattached IPs, or idle NAT Gateways remain
- [ ] Dev/staging environments have scheduled shutdown outside business hours
- [ ] Purchase commitments cover no more than the confirmed 60-day on-demand floor
- [ ] Egress architecture reviewed; VPC endpoints or CDN in place where applicable
- [ ] Unit economics (cost-per-request or cost-per-user) are measurable and baselined
- [ ] All cost controls are codified in IaC (Terraform/Pulumi), not console-only changes
