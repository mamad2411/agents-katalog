---
name: audit
description: Read-only cost audit of an AWS account (with or without Kubernetes) that ends in an HTML report - the bill classified into fixed categories, the biggest lines, and a four-stage cuts plan (do now / engineering / architecture / contracts) with a monthly savings forecast and the production impact of every action. Use whenever the user asks to reduce the AWS bill, where the money goes, how production is scaled at peak, savings by time of day, Savings Plans, cross-zone traffic, idle NAT, right-sizing or FinOps, even without the word "report". Never changes the account.
argument-hint: "[--profiles payer,member] [--region us-east-1] [--kube-context ctx]"
---

# AWS cost audit (read-only) → phased cuts plan

## Configuration

Take the account details from the plugin configuration, then from the arguments, then ask:

- Payer profile: `${user_config.payer_profile}`
- Member profiles: `${user_config.member_profiles}`
- Region: `${user_config.region}`
- kubectl context (EKS only): `${user_config.kube_context}`
- Timezone offset for hour-of-day tables: `${user_config.timezone_offset}`

Scripts live in `${CLAUDE_PLUGIN_ROOT}/scripts/`. Run Python with `python3 -I` (Windows: `py -3 -I`
or `python -I`) and pass paths as arguments. They only call the AWS CLI through subprocess, with
the user's own credentials, and only read.

## Premises that never change

- **Nothing in the audited account is changed.** Only `describe`, `get`, `list`, Cost Explorer,
  CloudWatch and, when there is a cluster, `kubectl get/describe` and port-forward. If a step
  seems to need a write (enable Flow Logs, create a user, change a Service), it becomes a
  **recommendation** in the plan, never an audit action. Production runs on top of this account.
- **Every recommendation states its impact on what is running.** The reader must know, per item,
  whether the action is harmless, needs a window and a rollback, or is a migration with its own
  plan. That matters more than the item's savings.
- **Numbers carry a source and a window.** Every value says where it came from (Cost Explorer,
  CloudWatch, cluster metrics, vendor console) and which period it covers. Estimates are
  labelled as estimates.
- **The output has the same shape for every company.** The bill always appears in the same
  categories with the biggest lines; the plan always has the same four stages. Content changes,
  structure does not.

## Flow

Order matters: each step changes how the next one reads.

1. **Access and scope.** Identify payer × member accounts (`aws sts get-caller-identity` per
   profile), regions, and **what the company runs**: EKS, ECS, plain EC2, Lambda, RDS, serverless.
   Run `scripts/check_requirements.sh --profiles …` (or `.ps1`) first if this is the first audit.
2. **Where the money goes.** `scripts/ce_breakdown.py --profile <payer> map` classifies the bill
   into fixed categories and prints the arrays the report template uses:

   | Category | What goes in | Varies with usage? |
   |---|---|---|
   | Compute | EC2 on-demand, Lambda, ECS/Fargate, EKS/ECS control planes, API Gateway | yes |
   | Network | data transfer, NAT, ELB, CloudFront, VPC, public IPv4 | yes |
   | Data & databases | RDS, DynamoDB, ElastiCache, OpenSearch, Redshift, managed Kafka | contract / instance |
   | Storage | S3, EBS, EFS, snapshots, ECR, Backup | yes |
   | SaaS & Marketplace | vendors billed through AWS (cache, queues, Kafka, SaaS databases) | contract |
   | Commitments | Savings Plans and Reserved Instances fees | fixed |
   | Observability, Security, Tax, Other | the rest | depends |

   Then `usage "<service>"` on the 2–3 biggest lines: `EC2 - Other` hides data transfer, EBS and
   NAT; `RDS` hides storage and backups; `S3` hides requests and transfer.
3. **Commitments before any conclusion about time of day.** `scripts/ce_breakdown.py sp` (plus
   `aws ec2 describe-reserved-instances`, `rds describe-reserved-db-instances`). If a Savings Plan
   runs at 100% utilization every day, night-time usage already equals the commitment: **shrinking
   at night saves zero** until usage grows above the plan. Only the on-demand overflow is cuttable
   by time of day. The arithmetic is in `references/method.md#savings-plan`.
4. **Hour-of-day profile of whatever dominates compute.** `scripts/cw_hod.py` with the metrics of
   that workload type (table in `references/method.md#profiles`): ASG/EC2, ECS, Lambda, RDS, ELB.
   Local timezone, weekdays and weekends apart. This is where the real peak and the slack show up.
5. **How the workload scales** — pick the branch:
   - **EKS/Kubernetes:** `scripts/k8s_scaling_snapshot.sh` + `scripts/prom_hod.py` (cores used ×
     requested × allocatable, HPAs at their cap, pending pods).
   - **ECS:** services, desired count, autoscaling policies, tasks per hour, reserved × used
     CPU/memory (`references/method.md#ecs`).
   - **Plain EC2:** ASGs and policies, instances outside ASGs, 14-day average CPU per instance,
     Compute Optimizer (`references/method.md#ec2`).
   - **Serverless:** invocations, duration and configured × used memory per function; idle
     provisioned concurrency (`references/method.md#lambda`).
6. **Network.** `scripts/ce_breakdown.py regional` and `regional-trend`. The
   `DataTransfer-Regional-Bytes` line is **two problems**: `InterZone-*` (inside the VPC) and
   `PublicIP-*` (SaaS vendors in the same region reached by public IP). NAT by bytes, public
   IPv4, CloudFront vs. direct origin. Recipe in `references/method.md#regional-traffic`.
7. **Data and storage.** Database instances with low CPU or Multi-AZ outside production, gp2
   storage, orphan snapshots and volumes, S3 and ECR without lifecycle, CloudWatch log groups
   without retention (`references/method.md#data`).
8. **Proven idleness.** `scripts/nat_idle_check.py`; `available` EBS volumes; loose EIPs; ELBs
   without targets; instances under 10% CPU. Idleness only counts as proven with datapoints
   present at zero, never with missing data.
9. **Classify and size.** For each lever: front (the same categories), nominal value, value
   realizable today (net of commitments), effort, risk, stage and impact on what is running.
   Compute levers under a saturated commitment share one ceiling: their sum never exceeds the
   on-demand overflow.
10. **Report.** Follow `references/report.md`. Publish with the Artifact tool when the environment
    has it (load the artifact-design and dataviz skills first if available); otherwise write the
    HTML file and tell the user where it is. Start from `assets/plan-template.pt-BR.html` (the
    mould; its labels are in Portuguese, translate them to the user's language as you fill it).
11. **Record.** A technical note in the team's documentation with the method, numbers, limits and
    the report link, plus what is not derivable from the account (access recipes that worked,
    pitfalls), for the next audit.

## Plan stages (fixed vocabulary)

| Stage | Criterion | Typical examples |
|---|---|---|
| 0 · Do now | 1–2 weeks, no architecture change, impact nil or reversible in seconds | ECR/S3 lifecycle, loose volumes and EIPs, oversized hosts, non-production off on weekends, log retention, gp2 → gp3 on EBS, raising a saturated autoscaling cap |
| 1 · Engineering work | weeks, normal rollouts per service | right-sizing (instances, tasks, requests, Lambda memory), cache read volume, private endpoint to a vendor |
| 2 · Architecture | months, touches topology or telemetry | zone-aware routing, one collector per AZ, CloudFront in front of the origin, removing idle network |
| 3 · Contracts and platform | executive decision, data migration | renegotiate or migrate SaaS, change database class, decommission legacy systems, buy or adjust commitments |

Each stage closes with a cumulative run-rate (conservative–optimistic range), effort, risk,
prerequisite, who decides and the impact on what is running. Always include the **Safe
execution** section (windows outside the measured peaks, one change at a time through IaC/GitOps,
observe 30 minutes, export before deleting, measure before cutting, data and contracts only with a
validated replacement) and the **What not to do** section with what looks obvious but does not pay
(shutting production down at night under a saturated commitment, extra commitment for a short
overflow, consolidating NAT across VPCs through peering, sampling traces before generating metrics).

## Pitfalls that cost time (details in references/method.md)

- The AWS CLI prints timestamps in the machine's local zone; do not subtract the offset twice.
- Command-line wrappers may mangle `aws ce` JSON; call the CLI through subprocess, as the scripts do.
- `MONTHLY` over a range that crosses a month returns two rows per key; they are not duplicates.
- Hourly granularity in Cost Explorer is opt-in; without it, use CloudWatch for "by hour".
- `EC2 - Other` is not compute: it is transfer, EBS, NAT and IPv4. `map` already splits it.
- Pods with `hostNetwork` report the whole node's traffic in `container_network_*` (6 copies per
  node, ~19× inflation). Exclude them and use `node_exporter` eth*/ens*.
- A regional NAT gateway publishes metrics under an extra `AvailabilityZone` dimension; discover
  dimensions with `list-metrics` instead of assuming.
- Zone-aware replication needs 3 AZs and factor 3; with 2 AZs or factor 1 it does not apply.
- Replicating more for durability **increases** cross-zone traffic: opposite goals, decide one first.
- RDS gp2 and gp3 cost the same per GB; the switch only improves IOPS. On EBS, gp3 is 20% cheaper.

## References

- `README.md` — requirements (tools, access, read-only IAM permissions), installation, layout;
  `scripts/check_requirements.sh` / `.ps1` checks all of it before you start.
- `references/method.md` — recipes per step (categories, SP, profiles per workload type,
  EKS/ECS/EC2/Lambda, network, data, idleness, sizing) and how to read each result.
- `references/report.md` — mandatory report structure, tables, forecast chart, writing rules.
- `assets/plan-template.pt-BR.html` — report mould with example data marked as such.
