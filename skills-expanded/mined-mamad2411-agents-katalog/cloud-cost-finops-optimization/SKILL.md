---
name: cloud-cost-finops-optimization
description: >
  Guides establishing cloud cost visibility and reducing spend across AWS,
  Azure, and GCP through tagging/labeling discipline, rightsizing,
  commitment-based discounts (Reserved Instances, Savings Plans,
  Committed Use Discounts), and FinOps showback/chargeback practices. Use
  when a user asks to "reduce our cloud bill", "set up cost allocation
  tags", "find idle/oversized resources", "decide between Reserved
  Instances and Savings Plans", "implement FinOps", "explain why cloud
  spend went up", or "build a cost dashboard per team".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# Cloud Cost & FinOps Optimization

## Purpose

Cloud spend left ungoverned grows faster than the value it produces —
not because any one decision was wrong, but because pay-as-you-go pricing
removes the natural friction that used to force capacity planning
conversations. FinOps closes that gap by making cost a first-class,
continuously reviewed signal: every resource attributable to a team and
purpose, every commitment decision (Reserved Instances, Savings Plans,
Committed Use Discounts) made deliberately rather than defaulted to
on-demand, and every anomaly caught within days, not discovered at
month-end reconciliation. This skill covers the recurring, cross-cloud
practices — tagging, rightsizing, commitment strategy, showback/
chargeback, and anomaly response — that turn cost from a lagging
indicator into an operating input.

## When to use

- Standing up cost allocation (tagging/labeling) so spend can be
  attributed to teams, products, or cost centers.
- Investigating a month-over-month cost increase or an anomaly alert.
- Deciding between commitment-based discount instruments (Reserved
  Instances vs. Savings Plans on AWS; Reserved VM Instances vs. Azure
  Savings Plans; Committed Use Discounts on GCP) for a stable workload.
- Rightsizing over-provisioned compute, storage, or database instances.
- Building a showback or chargeback dashboard so teams see (and are
  accountable for) their own spend.
- Responding to finance/leadership asking "why did the bill go up" or
  "what's our unit economics per customer/transaction."

## Prerequisites & environment

- Billing/cost data access: AWS Cost Explorer + Cost and Usage Report
  (CUR) in a dedicated S3 bucket, Azure Cost Management + Billing scoped
  to the relevant Management Group/subscription, or GCP Billing export
  to BigQuery — set these up before anything else; you cannot optimize
  what you can't see broken down by resource and tag/label.
  ("Symptom/Fix" for what happens without this is below.)
- A tagging/labeling taxonomy agreed with stakeholders (minimum viable
  set: `cost-center`, `environment`, `owner`, `service`) enforced via the
  landing-zone guardrails (AWS tag policies + SCP, Azure Policy, GCP
  Organization Policy / labels) — see the respective landing-zone
  skills.
- For commitment purchases: at least 30-90 days of historical usage data
  per instance family/region to size commitments against real, not
  guessed, baseline usage.
- Optional but recommended: a FinOps tool (CloudHealth, Cloudability,
  Kubecost for Kubernetes-specific allocation, or the open-source
  OpenCost) if spend is complex enough that native cost-explorer tools
  become unwieldy across multiple accounts/subscriptions/projects.

## Step-by-step guidance

1. **Establish cost visibility before optimizing anything.** Enable and
   confirm data is flowing to:
   - AWS: Cost and Usage Report (CUR 2.0) to S3, plus AWS Cost Anomaly
     Detection monitors per linked account or cost-allocation tag.
   - Azure: Cost Management scoped at the Management Group covering all
     subscriptions, with budgets and anomaly alerts configured per
     subscription.
   - GCP: Billing export to BigQuery (both the standard usage-cost
     export and the pricing/detailed export) so ad hoc SQL queries can
     slice spend by label, project, or SKU.

2. **Enforce and backfill cost-allocation tags/labels.** Confirm the
   landing-zone tag-policy guardrail is active for new resources, then
   run a tag-coverage report and manually (or via a script) tag
   pre-existing untagged resources — untagged spend is invisible spend
   in every downstream dashboard.

3. **Build the showback (or chargeback) view.** Minimum: a dashboard or
   scheduled report broken down by `cost-center`/`owner` tag, updated at
   least weekly, sent to the accountable team lead — not just a
   platform-team-only view. Showback (visibility without billing) is
   usually the right starting point; chargeback (actual internal billing)
   is a later maturity step once tagging coverage is reliably >95%.

4. **Rightsize compute and storage using actual utilization data**, not
   instance-family defaults:
   - AWS: Compute Optimizer recommendations for EC2/EBS/Lambda, cross-
     referenced with CloudWatch CPU/memory (via the CloudWatch agent)
     utilization over at least 2 weeks including peak periods.
   - Azure: Azure Advisor cost recommendations plus VM insights metrics.
   - GCP: Recommender's `google.compute.instance.MachineTypeRecommender`
     and `google.compute.instanceGroupManager.MachineTypeRecommender`.
   Downsize or change family only after confirming the workload's actual
   peak (not average) utilization has headroom — average-based
   rightsizing is a common cause of production incidents.

5. **Decide commitment strategy per workload class**, not organization-wide:
   - **Stable, predictable baseline usage** (e.g. a database tier that
     never scales down): AWS Reserved Instances or a Compute Savings Plan
     sized to the true floor usage over the last 90 days; Azure Reserved
     VM Instances; GCP 1-year or 3-year Committed Use Discounts (CUDs).
   - **Variable but non-zero usage across instance families/regions**:
     AWS Compute Savings Plans (flexible across family/region, unlike
     Reserved Instances) or GCP flexible CUDs — trade a small discount
     reduction for flexibility.
   - **Genuinely spiky/unpredictable workloads**: leave on-demand, or use
     Spot/preemptible capacity (AWS Spot, Azure Spot VMs, GCP Spot VMs)
     for fault-tolerant, interruptible work instead of committing.
   - Never commit to more than roughly 70-80% of observed baseline usage
     — commitments covering 100% of a fluctuating baseline routinely end
     up unused when demand dips.

6. **Set up anomaly detection and a response runbook.** When a cost
   anomaly alert fires: identify the resource/tag responsible from the
   CUR/Cost Management/BigQuery export, confirm with the owning team
   whether it's expected (a legitimate scale-up) or a mistake (an
   orphaned resource, a misconfigured autoscaler, a forgotten test
   environment), and close the loop within the same week — cost
   anomalies investigated a month later are much harder to attribute.

7. **Review and reconcile commitments quarterly.** Check utilization of
   existing Reserved Instances/Savings Plans/CUDs; if a commitment is
   consistently underutilized (workload was decommissioned, migrated, or
   downsized), plan for it to lapse rather than renewing blindly, or use
   the reserved-instance marketplace (AWS RI Marketplace) where
   applicable.

8. **Report unit economics, not just total spend**, to leadership once
   the above is in place — cost per transaction, per customer, or per
   environment tells a more actionable story than a raw month-over-month
   dollar figure.

## Best practices

- **Tag/label at resource creation time**, enforced by policy, not as a
  retroactive cleanup project — see the landing-zone skills for how to
  wire this into account/subscription/project vending.
- **Rightsize based on peak, not average, utilization** to avoid
  performance regressions; pair rightsizing changes with a rollback plan
  and a monitoring window.
- **Match commitment term to business certainty**, not just the discount
  curve — a deeper 3-year discount on a workload that might be
  decommissioned in 18 months is a false saving.
- **Separate showback (visibility) from chargeback (billing)** —
  chargeback without mature, trusted tagging data creates disputes that
  undermine the whole program.
- Treat **Kubernetes/container cost allocation as its own problem** —
  node-level cloud billing does not natively reflect per-pod or
  per-namespace cost; use a tool like OpenCost/Kubecost if container
  spend is material.
- **Automate detection of idle resources** (unattached EBS volumes/
  disks, idle load balancers, orphaned public IPs, stopped-but-not-
  deleted instances still billing for storage) as a recurring scheduled
  check, not a one-time cleanup.
- Involve **engineering, not just finance**, in every optimization
  decision — a rightsizing or commitment change that isn't understood by
  the team running the workload will get silently reverted or cause an
  incident.

## Common pitfalls

- **Symptom:** Finance asks "why did the AWS/Azure/GCP bill jump 30%
  last month" and nobody can answer without a multi-day manual dig
  through the console.
  **Fix:** No Cost and Usage Report / Cost Management export / BigQuery
  billing export was enabled with sufficient granularity, or tagging
  coverage was too low to attribute the increase. Set up the export and
  a minimum tagging bar (see step 1-2) before treating any specific
  optimization as urgent — visibility is the actual bottleneck, not the
  optimization technique.

- **Symptom:** A team purchased Reserved Instances/CUDs for peak-season
  capacity, and six months later most of the commitment sits unused,
  still billing.
  **Fix:** Commitment was sized against a temporary peak instead of
  sustained baseline usage. Size commitments to the trailing 90-day p10
  (near-floor) usage, and cover the variable portion above that with
  on-demand or Savings Plans/flexible CUDs instead of Reserved Instances.

- **Symptom:** A rightsizing recommendation is applied automatically and
  causes a latency-sensitive service to start throttling under load.
  **Fix:** The recommendation was based on average CPU utilization,
  which hid short bursts to near 100%. Cross-check peak utilization and
  application-level SLOs (latency, error rate) before applying automated
  rightsizing recommendations, and roll out during a low-traffic window
  with fast rollback available.

- **Symptom:** Kubernetes cluster shows a flat, high cloud compute bill
  regardless of which team scales its workloads up or down.
  **Fix:** Cost is being measured at the node level, not attributed
  per-namespace/pod. Deploy a cost-allocation tool (OpenCost/Kubecost) to
  break the node-level bill down by namespace/label so showback data
  reflects actual team usage instead of an even split.

- **Symptom:** A "cost optimization" cleanup script deletes what looks
  like an unattached EBS volume/disk, and it turns out to be a manually
  detached backup snapshot source someone needed.
  **Fix:** **Never auto-delete storage resources flagged as "idle"
  without a tagged grace period and human confirmation** — idle-resource
  detection should open a ticket or require explicit approval before any
  deletion, especially for anything holding data (see
  `cloud-native-storage-strategy` and
  `disaster-recovery-and-backup-strategy` for what's safe to actually
  remove versus what must be retained under a backup/retention policy).

## Worked example

**Scenario:** A SaaS company's AWS bill grew 40% quarter-over-quarter with
no corresponding customer growth, and finance wants an explanation within
the week.

1. Confirm CUR is enabled and tag coverage; find ~15% of EC2/RDS spend is
   on resources missing the `cost-center` tag — backfill those tags
   first so the breakdown is complete.
2. Query CUR by `cost-center` and `environment` tags: the `data-platform`
   team's `non-prod` environment spend tripled.
3. Cross-reference with Compute Optimizer: several `db.r5.4xlarge` RDS
   instances in `non-prod` show under 10% average CPU utilization over
   the trailing 30 days, with no meaningful peaks — they were sized to
   match production "just in case" during a migration and never resized
   down.
4. Rightsize the non-prod RDS instances to `db.r5.large` after confirming
   with the data-platform team that non-prod doesn't need production-
   scale capacity, monitored over a one-week rollout window.
5. Identify that the same team's stable production baseline usage
   qualifies for a 1-year Compute Savings Plan sized to the trailing
   90-day p10 usage, covering roughly 70% of baseline while leaving burst
   capacity on-demand.
6. Set an AWS Cost Anomaly Detection monitor scoped to the
   `data-platform` cost-allocation tag so a similar unmonitored ramp is
   caught within days next time, not a quarter later.

## Cross-references

- [aws-landing-zone-setup](../aws-landing-zone-setup/SKILL.md)
- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)
- [cloud-native-storage-strategy](../cloud-native-storage-strategy/SKILL.md)
