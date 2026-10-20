---
name: cost-review
description: "Investigate a cloud bill that has grown, or reduce spend deliberately, without trading away reliability — attribute the spend before touching anything, read the top movers period over period rather than the top spenders, classify each finding as idle, overprovisioned, wrong purchase model, data transfer, retention or architectural, state what every change degrades, and report unit cost per request or tenant, not a total. Use this skill whenever someone asks why the AWS, GCP or Azure bill went up, wants a FinOps or cost-optimisation plan, is looking at rightsizing, reserved instances, savings plans, spot, NAT gateway or egress charges, untagged spend, Kubernetes cost attribution or showback, or says things like \"our bill jumped 30% last month\", \"where is all this money going\", or \"finance wants 20% off cloud\". Not for debugging slow performance, capacity planning for a launch, choosing a vendor or tool, or a live incident."
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(aws:*), Bash(gcloud:*), Bash(az:*), Bash(kubectl:*), Bash(jq:*)"
---

# Cost Review

A cost review has gone well when every recommendation names a figure, an owner, a date to verify it, and the one thing it makes worse. Anything without those four is a suggestion, and suggestions do not change a bill.

Cost work fails in two opposite directions and both are common. In the first, someone stares at a total that grew 30% and starts turning things off — a spare replica, a warm standby, a retention window — and buys a few hundred dollars a month plus an outage that costs more than the year's savings. In the second, the team runs a cost-optimisation initiative that produces a spreadsheet, three rightsizing tickets nobody owns, and a bill next month that is unchanged or higher, because the underlying growth never stopped while everyone was reading the spreadsheet. Both come from the same root: acting on a number nobody can attribute to a team, a workload or a decision. The order below exists to stop that — attribution, then the delta, then the cause, then the change with its stated cost to reliability. Skipping straight to a savings list is the failure mode this skill exists to prevent.

## Scope

Use for: explaining a bill that grew and finding the specific cause; a deliberate spend-reduction target; building cost attribution, tagging or showback where none exists; rightsizing, purchase-model and commitment decisions; data-transfer and retention investigations; Kubernetes per-namespace or per-workload cost; setting budgets and anomaly alerts; adding a cost line to architecture review.

Do not use for: debugging why something is slow, which is a performance problem that happens to have a cost; capacity planning for a launch, where the question is whether it survives rather than what it costs; choosing between vendors or tools, which is `vendor-evaluation`; a live incident, which is `incident-response`; or the migration itself when the recommendation turns out to be a replatform, which is `plan-platform-migration`.

## Two gates

**Attribution gate.** You cannot reduce what you cannot attribute. Before proposing a single change, be able to say what fraction of the bill maps to a named team, service or workload. If the untagged or unallocated share is above roughly 20%, the first deliverable is attribution, not savings — say so plainly rather than optimising the part you happen to be able to see.

**Reliability gate.** No cost change ships without a written answer to "what does this degrade". The candidates are headroom, redundancy, recovery time, and retention needed for compliance or debugging. "Nothing" is an acceptable answer for an unattached volume from 2022; it is rarely the answer for anything with traffic on it. A change whose degradation nobody wrote down gets discovered during the next incident, at which point the saving is reversed and the mechanism is distrusted.

## Workflow

### 1. Attribute before you act

Attribution is a prerequisite, not a phase-two nicety, and it is the deliverable when it is missing.

- **Cost allocation tags.** Pick a small mandatory set — owner or team, service, environment, cost-centre — and activate them as cost allocation tags in the billing console, which is a separate step from applying them to resources and only takes effect going forward. Enforce them at creation time in the IaC module and with a policy check, because a tag applied by a quarterly sweep documents history rather than changing behaviour.
- **Account and project structure.** The strongest attribution boundary is not a tag, it is an account, subscription or project. Untaggable spend — support charges, some data transfer, marketplace subscriptions — still lands in an account, so a per-team account with consolidated billing attributes things a tag never will.
- **Cost categories or grouping rules.** Map accounts and tags into the reporting dimensions the organisation actually thinks in (product line, team, tenant). Do this once in the billing tool rather than in a spreadsheet each month.
- **Kubernetes.** A cluster is one line on the bill and dozens of workloads underneath. Split it with OpenCost or Kubecost, which apportion node cost by each pod's requests and usage over time, then aggregate by namespace, label or controller. Requests, not limits, are what the scheduler reserved and therefore what the workload cost.
- **Shared cost.** A shared cluster, a shared database, a NAT gateway, a platform team's observability bill. Any split is a convention, not a measurement — even usage-proportional splits pick a usage metric arbitrarily. Choose one (even split, proportional to requests, proportional to revenue, or left in a platform bucket nobody is charged for), write it down where the report is read, and keep it stable. Re-litigating the convention every quarter costs more attention than the accuracy is worth.

`references/attribution.md` has the concrete setup: the mandatory tag set, the queries against Cost Explorer and the BigQuery billing export, the OpenCost aggregation, and worked examples of each shared-cost convention. Read it when the attribution gate fails.

### 2. Find the delta, not the total

A billing export is too large to read inline, so hand it to the `cost-analyst` subagent rather than opening it here. It returns the top movers period over period with the cause of each, and the export itself never enters this conversation.

A bill that grew has a specific cause, and it is almost never the biggest line. Compare period over period at the resource and usage-type level, then sort by change rather than by size.

```bash
# Month over month, by service and usage type, unblended.
aws ce get-cost-and-usage \
  --time-period Start=2026-07-01,End=2026-09-01 \
  --granularity MONTHLY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE Type=DIMENSION,Key=USAGE_TYPE \
  | jq -r '...'   # diff the two periods and sort by absolute change
```

The top spenders and the top movers are different lists, and only the second one answers the question. Compute costs are usually the largest line and usually flat; the thing that grew is frequently a usage type nobody has ever read out loud, such as `DataTransfer-Regional-Bytes` or `NatGateway-Bytes`.

Then read the movers against a calendar of what changed. Typical causes, in the order they turn up:

| Delta shape | Usual cause |
| --- | --- |
| A step change on one date | A deploy, a new service, an instance-family change, a feature launch, a config flip such as a retention or log-level change |
| A steady linear ramp | Accumulating storage, snapshots, log or metric retention, a slow leak of orphaned resources |
| Growth proportional to traffic | Working as intended — check unit cost before calling it a problem |
| A short spike that never came back down | A load test, a backfill, a migration that left resources behind |
| Growth in requests or transfer with flat traffic | A retry loop, a chatty client, an N+1 against a metered API, a misconfigured cache |

Two accounting traps to clear before believing any delta: amortised versus unblended cost, where an upfront commitment lands as a spike in one month unless you read amortised; and credits or free-tier expiry, which make a bill grow with no change in usage at all.

### 3. Classify each mover against the taxonomy

| Cause | How it looks | Action | Typical risk |
| --- | --- | --- | --- |
| **Idle and orphaned** | Unattached volumes, unassociated addresses, load balancers with no healthy targets, snapshots of instances that are gone, dev and staging running overnight and at weekends | Delete after an ownership check; schedule non-production environments off out of hours | Low, but confirm the volume is not somebody's uncollected forensic evidence |
| **Overprovisioned** | Utilisation percentiles far below the size, memory footprint a fraction of the instance, an over-replicated stateless tier | Rightsize from percentiles with stated headroom (step 4) | Real. This is where the outage comes from |
| **Wrong purchase model** | Steady baseline on on-demand; interruption-tolerant batch on on-demand; a commitment covering a workload being re-architected | Cover the trough with committed spend, run tolerant work on spot, leave the peak on-demand | The commitment trap: a one or three-year discount on a workload you plan to change |
| **Data transfer** | Cross-AZ chatter between a service and its database or cache, cross-region replication, NAT gateway processing on traffic that could use a VPC endpoint, egress to the internet or to a peer | Colocate the chatty pair in an AZ, add gateway or interface endpoints, front egress with a CDN, compress | Availability: colocating in one AZ trades transfer cost for a zonal failure mode. Say so |
| **Storage class and retention** | Logs and metrics at full fidelity forever, snapshots with no expiry, hot storage for cold objects, high-cardinality metrics | Lifecycle rules, tiering, downsampling, a retention policy with a stated reason per class | Debugging and compliance both need history. Check the legal floor before cutting |
| **Architectural** | Per-request cost of a chatty design, an N+1 against a metered API, a serverless function invoked per row, a queue polled at high frequency for a quiet topic | A code or design change, sized as engineering work | Highest effort, and usually the only lever that fixes unit cost rather than total |

Idle and retention findings are where the safe money is. Data transfer is where the surprise usually is, because it is invisible on every dashboard the team looks at and often turns out to be the largest single mover.

### 4. Size from percentiles, with the headroom written down

Rightsizing from an average is how a cost saving becomes a page. Pull at least two weeks of data, covering a weekend and any weekly or monthly peak, and size against the high percentile rather than the mean.

- Use p95 or p99 of CPU and memory over the window, not the average and not the last hour.
- State the headroom explicitly: "sized so p99 utilisation lands at 60%, leaving room for a 1.6x traffic increase and one instance failing".
- Check what the smaller instance changes besides vCPU and memory: network and EBS bandwidth, burst credits, and NUMA or cache behaviour all move with instance size, and a memory-bound service on a smaller instance can lose more throughput than the size suggests.
- For Kubernetes, rightsize requests against usage percentiles; limits are a different decision, and setting a CPU limit equal to the request introduces throttling that looks like a latency regression with no cost saving.
- Verify after the change with the same percentile, at the same window length, before counting the money.

### 5. Check the purchase model against the workload's remaining life

Committed spend is the largest single lever on most bills and the easiest to regret. Before committing, answer one question: will this workload exist, in this shape, for the length of the term? A three-year commitment on a fleet you are about to move to a different instance family, a managed service, or another region converts a discount into a floor you keep paying.

- Commit to the **trough**, not the average and not the peak. The trough is what runs at 04:00 on a public holiday.
- Prefer the flexible instruments (compute savings plans over per-instance reservations) unless the inflexible discount is materially larger, because flexibility is what survives a re-architecture.
- Ladder the terms rather than committing everything at once on the same date, so a change of plan does not have to wait for a single cliff.
- Spot is for work that tolerates interruption: batch, CI, stateless replicas behind capacity that can absorb the loss. Requiring a specific instance type in a single AZ removes most of spot's safety, so diversify across families and zones.

### 6. Name what each change degrades, then write the finding

Every finding gets the same block, and the degradation field is the one that makes it reviewable. Confidence matters as much as the figure: a Cost Explorer figure for a resource you can name is high confidence, an estimate of a rightsizing outcome is medium, and a modelled architectural saving is low until it ships.

### 7. Convert to unit economics

Total spend is not a goal. A business that doubled its customers should have a bill that grew, and cutting it may be the wrong thing to do.

Pick the denominator the business actually runs on — cost per thousand requests, per active tenant, per build minute, per GB served, per order — and report the trend of that alongside the total. A bill that grows while unit cost falls is a company working; a unit cost that grows is the alarm, and it is the only number that tells you whether an architectural change is worth funding. Publish one or two units, not a suite: a unit metric nobody can recite is not steering anything.

### 8. Make it stick

A one-off cleanup regresses within about two quarters, reliably, because the mechanism that created the spend is untouched.

- **Budgets and anomaly detection**, routed to the team that can act on them rather than to a finance alias. The routing discipline is the same as any other alert — an owner, a threshold that means something, and a response that is not "acknowledge and move on"; `alert-design` covers why an unactioned cost alert decays exactly like an unactioned page.
- **A cost line in architecture review and in the pull-request template** for infrastructure changes: what does this cost at expected load, and at ten times it.
- **Showback per team**, monthly, from the attribution built in step 1. Chargeback is a bigger organisational commitment; showback gets most of the behaviour change for a fraction of the argument.
- **An owner per finding and a verification date.** Both, or it does not count as shipped.

## Where to be sceptical

Vendor and native cost tools optimise for what they can see, and what they can see is resource metadata rather than intent.

- A "97% waste" or "you are overspending by 60%" headline usually counts reserved headroom, failover capacity, warm standbys and burst allowance as waste. Reprice the claim against the workload's actual requirements before repeating it to anyone.
- Recommendation engines size from short lookback windows and miss weekly and monthly peaks entirely.
- A savings percentage quoted against on-demand list price is not a saving against what you currently pay if you already hold commitments.
- Savings claimed at the moment of a recommendation, rather than verified in a later bill, are the most common form of fictional money. Count a saving when it appears in an invoice.

## Output format

Report a cost review in this shape, one block per finding, ranked by annualised figure over effort.

```markdown
## Attribution status
[Share of spend attributed, the untagged remainder, the shared-cost convention in use.]

## The delta
[Period over period, top movers by change with figures, and what changed on each date.]

## Findings
### F1 — [what it is]
Monthly figure:  [amount, and whether it is amortised or unblended]
Confidence:      [high / medium / low, and why — measured, estimated, or modelled]
Degrades:        [headroom, redundancy, recovery time, retention — or "nothing, and why"]
Effort:          [config change / ticket / engineering work]
Owner:           [name]
Verify on:       [date, and the number that has to move]

## Unit economics
[The chosen unit, its current value, its trend, and what it says the total does not.]

## Not recommended
[What was considered and rejected, with the reliability reason. This is the section that
stops the same suggestion arriving again next quarter.]

## Controls
[Budgets, anomaly alerts and their routing; the review gate; showback cadence.]
```

## Anti-patterns

**Turning things off before attributing them.** The unattributed resource is the one nobody can vouch for, which is exactly why it looks safe to delete and exactly why it is not. The cost is an outage that erases a year of the savings and, worse, ends the organisation's tolerance for cost work at all.

**Rightsizing from averages.** An average hides the peak that sizing exists to survive. The instance runs fine for three weeks and falls over on the monthly close, the marketing send, or the Monday morning ramp — and the incident is attributed to load rather than to the change that caused it. Size from p95 or p99 over a window that contains a real peak, and write the headroom down.

**Committing to a workload you are about to change.** A three-year commitment on a fleet that is mid-replatform buys a discount and a floor. You keep paying for the old shape while running the new one, and the migration's business case quietly gets worse. Commit to the trough, prefer flexible instruments, and ladder the end dates.

**A cost initiative with no owner and no unit metric.** Produces a spreadsheet, a kickoff, and a bill that is unchanged. Without a named owner per finding nothing ships, and without a unit metric nobody can tell growth from waste, so the initiative argues about the total until attention runs out.

**Optimising the third-largest line while data transfer sits unexamined.** Cross-AZ, NAT gateway and egress charges are invisible on every dashboard the team keeps and are frequently the single largest mover. Spending a week rightsizing instances while an unexamined transfer line grows is negative work.

**Counting savings that were never realised.** A saving exists when a later invoice is smaller, not when a recommendation is written or a ticket is closed. Recommendation-time totals accumulate into a claimed number several times larger than any observed reduction, and once leadership has noticed that gap, every future figure from the team is discounted.

## Reference files

- `references/attribution.md` — read when the attribution gate fails or spend cannot be mapped to teams: the mandatory tag set and how to enforce it at creation, activating cost allocation tags, account and project structure, Cost Explorer and BigQuery billing-export queries, Kubernetes attribution with OpenCost, and the shared-cost conventions with a worked example of each.
- `references/cost-levers.md` — read when sizing a specific finding: the rightsizing procedure and the metrics that actually bound an instance, commitment and spot arithmetic including break-even coverage, the data-transfer decision table by path, storage class and retention policy, and the verification step that turns a projection into a counted saving.
