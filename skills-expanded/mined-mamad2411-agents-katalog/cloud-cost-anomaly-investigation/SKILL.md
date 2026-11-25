---
name: cloud-cost-anomaly-investigation
description: >
  Walks through investigating an unexpected cost spike on this month's
  cloud bill right now — querying AWS Cost Explorer/CUR, Azure Cost
  Management, or GCP BigQuery billing export to isolate the specific
  resource, tag, and team responsible before it becomes a formal FinOps
  review. Use when a user asks "why did our AWS/Azure/GCP bill jump this
  week/month," "what's driving this cost anomaly alert," "find what
  resource caused this spike," or "who do I ask about this spend before
  the finance review." Distinct from cloud-cost-finops-optimization,
  which covers the ongoing tagging/rightsizing/commitment program this
  investigation is a single incident inside of.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# Cloud Cost Anomaly Investigation

## Purpose

A cost anomaly alert or a finance Slack message ("why is spend up 30%
this week?") starts a clock: the sooner the specific resource, tag, and
owning team are identified, the cheaper and less politically charged the
fix is. Left uninvestigated for a month, the same question turns into a
formal FinOps review with executives in the room, and the trail (which
engineer changed what, on which day) is much colder. This skill is the
tactical, hours-not-weeks workflow for tracing a specific spike back to
its cause — a runaway resource, a misconfigured autoscaler, a forgotten
non-prod environment, a data-transfer surprise — using each provider's
cost-explorer/billing-query tooling, so the on-call or platform engineer
can hand finance an answer (and, ideally, a fix) inside the same week the
alert fired. It assumes cost visibility (CUR, Cost Management, BigQuery
export) is already enabled; if it isn't, that's the actual blocker — see
[cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
step 1 for standing that up first.

## When to use

- A cost anomaly detection alert (AWS Cost Anomaly Detection, Azure Cost
  Management anomaly alert, a GCP budget/BigQuery-based alert) just
  fired and needs triage before it's dismissed or escalated.
- Someone asks "why did the bill jump" for a specific day/week/month and
  wants an answer faster than the next scheduled FinOps review.
- A budget alert threshold was crossed and the specific driver needs to
  be identified before deciding whether it's expected (legitimate scale-
  up) or a mistake.
- Preparing the input for a formal FinOps review so it starts from "here
  is what happened and why" instead of "we're still looking into it."
- Confirming whether a suspected cause (a deploy, a config change, a new
  feature launch) actually correlates with the cost increase, with data,
  not guesswork.

## Prerequisites & environment

- Billing export already flowing with resource- and tag-level
  granularity: AWS Cost and Usage Report (CUR 2.0) in an S3 bucket (or
  Cost Explorer API access as a lighter-weight alternative for
  day/service-level slicing), Azure Cost Management scoped to the
  relevant subscription(s)/Management Group, or GCP Billing export to
  BigQuery (both the standard and detailed/pricing export tables). If
  this isn't enabled yet, that gap is the finding — escalate it as the
  first step rather than trying to reconstruct spend from the console UI.
- Read access to the query tooling for at least the provider(s) actually
  in use: AWS CLI `ce` (Cost Explorer) commands or Athena over CUR
  parquet files, `az costmanagement` CLI or the Cost Management portal,
  `bq query` against the billing export dataset.
- A tagging baseline (`cost-center`/`owner`/`environment`/`service`) —
  even partial — to attribute spend to a team; without it, the
  investigation can identify the *resource* but not the *owner*, which is
  usually the actually-needed answer. See
  [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
  for closing tagging gaps.
- Knowledge of (or access to) a change log/deploy history (CI/CD deploy
  events, Terraform apply history, autoscaling group activity history)
  to correlate a cost change with a specific engineering event, not just
  a calendar date.

## Step-by-step guidance

1. **Establish the exact window and magnitude before looking for a
   cause.** Don't start from "this month is high" — pin down the day the
   trend changed. AWS Cost Explorer via CLI, grouped by day and service,
   over the trailing 14 days:
   ```bash
   aws ce get-cost-and-usage \
     --time-period Start=2026-07-14,End=2026-07-28 \
     --granularity DAILY \
     --metrics "UnblendedCost" \
     --group-by Type=DIMENSION,Key=SERVICE
   ```
   Azure equivalent — daily actual cost by service name over the same
   window:
   ```bash
   az costmanagement query \
     --type ActualCost \
     --timeframe Custom \
     --time-period from=2026-07-14 to=2026-07-28 \
     --dataset-granularity Daily \
     --dataset-aggregation '{"totalCost":{"name":"Cost","function":"Sum"}}' \
     --dataset-grouping name=ServiceName type=Dimension \
     --scope "/subscriptions/<SUBSCRIPTION_ID>"
   ```
   GCP equivalent — daily cost by service from the BigQuery billing
   export:
   ```sql
   SELECT
     DATE(usage_start_time) AS usage_day,
     service.description AS service,
     SUM(cost) AS daily_cost
   FROM `<PROJECT_ID>.<BILLING_DATASET>.gcp_billing_export_v1_<BILLING_ACCOUNT_ID>`
   WHERE usage_start_time BETWEEN TIMESTAMP("2026-07-14") AND TIMESTAMP("2026-07-28")
   GROUP BY usage_day, service
   ORDER BY usage_day, daily_cost DESC
   ```
   Identify the specific day the daily run-rate stepped up (a step
   change, not a gradual ramp, points to a discrete event like a deploy
   or a misconfiguration; a gradual ramp points to organic growth or a
   slow leak like an unbounded log/storage accumulation).

2. **Narrow from service to specific resource and tag.** Re-run the same
   query grouped by `USAGE_TYPE`/resource ID (AWS), by `ResourceId`
   (Azure), or by `sku.description`/`resource.name` (GCP), filtered to
   just the service and date range identified in step 1:
   ```bash
   aws ce get-cost-and-usage \
     --time-period Start=2026-07-20,End=2026-07-28 \
     --granularity DAILY \
     --metrics "UnblendedCost" \
     --filter '{"Dimensions":{"Key":"SERVICE","Values":["Amazon Elastic Compute Cloud - Compute"]}}' \
     --group-by Type=DIMENSION,Key=USAGE_TYPE
   ```
   For AWS, if Cost Explorer's dimension granularity isn't enough to name
   an individual resource, query CUR directly via Athena for
   `line_item_resource_id`:
   ```sql
   SELECT line_item_resource_id, line_item_usage_start_date, SUM(line_item_unblended_cost) AS cost
   FROM cur_database.cur_table
   WHERE line_item_usage_start_date BETWEEN TIMESTAMP '2026-07-20' AND TIMESTAMP '2026-07-28'
     AND product_product_name = 'Amazon Elastic Compute Cloud'
   GROUP BY line_item_resource_id, line_item_usage_start_date
   ORDER BY cost DESC
   LIMIT 20
   ```
   For GCP, the BigQuery export includes `resource.name` and per-label
   fields directly, so this step and step 1 can often be a single query
   with tighter `GROUP BY`.

3. **Attribute the resource to a tag/label and owning team.** Group the
   same query by cost-allocation tag (`cost-center`, `team`, `owner`,
   `environment`):
   ```bash
   aws ce get-cost-and-usage \
     --time-period Start=2026-07-20,End=2026-07-28 \
     --granularity DAILY \
     --metrics "UnblendedCost" \
     --group-by Type=TAG,Key=team
   ```
   ```sql
   -- GCP: group by a resource label present in the billing export
   SELECT
     (SELECT value FROM UNNEST(labels) WHERE key = 'team') AS team,
     SUM(cost) AS cost
   FROM `<PROJECT_ID>.<BILLING_DATASET>.gcp_billing_export_v1_<BILLING_ACCOUNT_ID>`
   WHERE usage_start_time BETWEEN TIMESTAMP("2026-07-20") AND TIMESTAMP("2026-07-28")
   GROUP BY team
   ORDER BY cost DESC
   ```
   If the resource has no tag/label at all, that absence *is* a finding —
   flag it for backfill per
   [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
   step 2 even while the immediate investigation continues by other means
   (resource-creation timestamp, VPC/subnet/resource-group ownership
   convention, CloudTrail/Activity Log `CreatedBy` metadata).

4. **Correlate the cost step-change with an actual event**, not just a
   date. Cross-reference the day/hour identified in step 1 against:
   - AWS CloudTrail (`aws cloudtrail lookup-events --lookup-attributes
     AttributeKey=ResourceName,AttributeValue=<resource-id>`) for who/what
     created or resized the resource.
   - Azure Activity Log (`az monitor activity-log list --resource-group
     <RESOURCE_GROUP> --start-time 2026-07-19T00:00:00Z`).
   - GCP Cloud Audit Logs (`gcloud logging read` filtered to the resource
     and time window).
   - The CI/CD deploy history or Terraform state history for the same
     window — a cost step-change that lines up with a deploy timestamp is
     almost always attributable to that change (a new autoscaling max, a
     larger instance type, a new always-on resource, a misconfigured
     retry loop generating excess API calls/data transfer).

5. **Distinguish "expected" from "mistake" before escalating**, and say
   which explicitly in the write-up:
   - **Expected**: a legitimate traffic/scale-up, a planned feature
     launch, an intentional environment stood up for a defined purpose.
     Action: confirm with the owning team, note it, move on — this is a
     FinOps/showback data point, not an incident.
   - **Mistake**: a misconfigured autoscaler with no upper bound, a
     forgotten non-prod environment left running at production scale, a
     runaway retry loop driving data-transfer or API-call costs, a
     resource provisioned in the wrong region/instance family. Action:
     confirm with the owning team, then fix (see step 6) and document
     root cause.
   Never guess; ask the owning team identified in step 3 to confirm
   which case it is before taking any action on the resource itself.

6. **Act only after confirming true responsibility and intent**, and
   prefer the least destructive fix that resolves the anomaly:
   - Rightsize or scale down rather than delete, if the resource is still
     needed at a smaller footprint.
   - If the resource genuinely looks orphaned/unused, do not delete it as
     part of this investigation — hand off to
     [orphaned-cloud-resource-cleanup](../orphaned-cloud-resource-cleanup/SKILL.md),
     which has the explicit non-use confirmation steps required before
     any deletion.
   > **Warning:** Do not delete or terminate a resource identified during
   > a cost investigation without confirming with its owning team first,
   > even if it looks clearly like a mistake (an idle non-prod instance,
   > a forgotten test cluster) — the same symptom can also be a
   > deliberately retained warm-standby DR resource (see
   > [disaster-recovery-and-backup-strategy](../disaster-recovery-and-backup-strategy/SKILL.md))
   > or an active but low-utilization workload with a non-obvious
   > dependency. Cost urgency is not a reason to skip the confirmation
   > step.

7. **Close the loop with a short written finding**, even for an internal
   Slack/ticket update: window, resource(s), tag/team, root cause
   (expected vs. mistake), and either the fix applied or the fix planned
   with an owner and date — this is what turns a one-off investigation
   into input the next formal FinOps review can build on instead of
   re-deriving.

8. **If this is the second or third time the same team/service causes an
   anomaly**, escalate beyond a one-off fix: recommend a budget
   alert/Cost Anomaly Detection monitor scoped to that team's
   cost-allocation tag (per
   [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
   step 6) so the next occurrence is caught by monitoring, not by finance
   noticing the bill.

## Best practices

- **Always pin the exact day the trend changed before hypothesizing a
  cause** — grouping by week or month hides the step-change signal that
  makes correlation with a specific deploy/config change possible.
- **Query at the finest granularity the export supports** (resource ID,
  not just service) — service-level totals answer "what category" but
  rarely "which specific resource," and "which specific resource" is
  what an owning team needs to actually act on.
- **Treat an untagged resource driving a spike as two findings, not
  one**: the cost anomaly itself, and the tagging gap that made
  attribution slower than it should have been.
- **Cross-reference cost data with change history (CloudTrail/Activity
  Log/deploy logs), not just billing data alone** — billing data tells
  you *what* cost more; audit/deploy logs tell you *why*, and only the
  combination lets you say "this is caused by X change."
- **Never conflate "investigated" with "fixed"** — identifying the
  resource and team is the deliverable of this skill; the actual
  rightsizing/decommissioning/tagging fix may belong to
  [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
  or [orphaned-cloud-resource-cleanup](../orphaned-cloud-resource-cleanup/SKILL.md)
  depending on what's found.
- **Write the finding down even when the answer is "expected, no
  action"** — a documented, confirmed-expected spike is exactly the
  evidence a future formal FinOps review needs to avoid re-investigating
  the same non-issue.

## Common pitfalls

- **Symptom:** The cost anomaly alert names a service (e.g. "Amazon EC2")
  but nobody can say which team or workload is responsible, and the
  investigation stalls waiting for someone to "look into it."
  **Fix:** Group the Cost Explorer/Cost Management/BigQuery query by
  cost-allocation tag, not just service, immediately (step 3) — if the
  resource has no tag, that's the actual finding to report (a tagging
  gap), and the resource-creation audit log (CloudTrail/Activity
  Log/Cloud Audit Logs) becomes the fallback attribution path rather than
  waiting on tags that don't exist.

- **Symptom:** An engineer, under pressure to "fix the spike fast,"
  terminates an EC2 instance/VM that looked idle, and it turns out to
  have been a pinned warm-standby DR replica or a batch job that only
  runs weekly.
  **Fix:** **Never delete or stop a resource as part of a cost
  investigation without confirming its actual purpose with the owning
  team first** — a low-recent-utilization resource is not the same as an
  unused one; hand off to
  [orphaned-cloud-resource-cleanup](../orphaned-cloud-resource-cleanup/SKILL.md)'s
  explicit non-use confirmation process instead of acting unilaterally
  during triage.

- **Symptom:** The investigation concludes "spend went up because of
  EC2/Compute Engine/VMs" but a week later the same category spikes
  again for an unrelated reason.
  **Fix:** The finding stopped at the service level instead of the
  specific resource/tag/root-cause level, so nothing specific could be
  monitored going forward. Push every investigation down to a named
  resource and a named root cause (a specific autoscaling group's max
  size, a specific misconfigured retry loop), and set a scoped anomaly
  monitor on that dimension afterward.

- **Symptom:** A spike traced to a runaway process turns out to be
  driven by unexpectedly high **data transfer/egress** costs, not compute
  or storage, and the investigation initially misses it because it only
  looked at the top-line service breakdown.
  **Fix:** Data transfer/network egress often appears as its own line
  item or `USAGE_TYPE` (`DataTransfer-Out-Bytes` on AWS, `Bandwidth` on
  Azure, `Network` SKUs on GCP) separate from the compute resource
  generating it. Explicitly check network/data-transfer usage types in
  step 2's group-by, not just compute/storage, especially when the
  triggering service's own on-demand cost looks unremarkable but total
  spend still jumped.

- **Symptom:** By the time finance raises the question in a monthly
  review, the CloudTrail/Activity Log retention window has already
  rolled past the date of the actual change, and correlation in step 4
  becomes guesswork.
  **Fix:** This is why the investigation needs to happen within days of
  the anomaly alert, not at month-end — extend default audit-log
  retention (CloudTrail to a long-retention S3 bucket, Activity Log to a
  Log Analytics workspace, Cloud Audit Logs export to BigQuery) so a
  slower-to-notice anomaly still has a change-history trail to
  correlate against.

## Worked example

**Scenario:** An AWS Cost Anomaly Detection alert fires: overall spend is
tracking roughly 18% above the trailing-week baseline, three days into
the current billing cycle.

1. Run the daily/service-grouped Cost Explorer query (step 1) over the
   trailing 10 days — the daily run-rate shows a clean step-change
   starting exactly two days ago, concentrated in "Amazon Elastic
   Compute Cloud - Compute," not a gradual ramp across multiple services.
2. Narrow by `USAGE_TYPE` (step 2): the increase is almost entirely
   `BoxUsage:m5.4xlarge` in `eu-west-1`, not spread across instance
   types — pointing at a specific autoscaling group or fleet, not
   general traffic growth.
3. Group by the `team` cost-allocation tag (step 3): 95% of the new
   `m5.4xlarge` spend carries `team=search-indexing`.
4. Cross-reference CloudTrail for the same window and instance type
   (step 4): an Auto Scaling Group `search-indexing-workers` had its
   `MaxSize` changed from 10 to 60 two days ago via a Terraform apply,
   timestamped an hour before the cost step-change began.
5. Confirm with the `search-indexing` team lead (step 5): the change was
   an accidental copy-paste in a Terraform PR meant to raise a *different*
   ASG's max size for an unrelated load test; the `search-indexing` ASG's
   actual autoscaling demand never required more than ~12 instances, so
   the fleet scaled up to near the new (wrong) ceiling under normal load
   and stayed there.
6. Fix: revert the `MaxSize` to 10 via the same Terraform-managed
   pipeline (not a manual console click, to keep it in version control),
   confirm the ASG scales back down within the hour, and post a written
   finding in the team's channel: resource = `search-indexing-workers`
   ASG, root cause = accidental `MaxSize` change in `PR #482`, fix =
   reverted in `PR #491`, cost impact = roughly the 18% spike over the
   two days it ran.
7. Because this is the team's second ASG-sizing-related cost incident
   this quarter, recommend a Cost Anomaly Detection monitor scoped
   specifically to `team=search-indexing` so the next runaway autoscaler
   change is caught within hours instead of at the next billing-cycle
   review.

## Cross-references

- [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md) —
  the ongoing tagging, rightsizing, and anomaly-monitoring program this
  investigation is a single incident inside of; escalate tagging gaps
  and recurring-cause fixes there.
- [orphaned-cloud-resource-cleanup](../orphaned-cloud-resource-cleanup/SKILL.md) —
  hand off here, rather than deleting anything directly, when the
  investigation finds a resource that appears genuinely unused.
- [cloud-access-request-and-iam-lifecycle-management](../cloud-access-request-and-iam-lifecycle-management/SKILL.md) —
  when a spike traces back to a resource created under a stale or
  over-broad temporary access grant, that grant's lifecycle is handled
  there.
- [disaster-recovery-and-backup-strategy](../disaster-recovery-and-backup-strategy/SKILL.md) —
  check before treating a low-utilization resource as wasteful spend; it
  may be a deliberately retained warm-standby/backup asset.
