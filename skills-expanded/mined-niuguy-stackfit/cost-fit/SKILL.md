---
name: cost-fit
description: Estimate the monthly launch cost of a project's chosen or recommended production stack, judge whether free tiers can safely carry the release, identify exactly which actions or thresholds trigger the first bill, and specify the spending alerts and limits to configure before launch. Use for "how much will this cost to run", free-tier fitness checks, budget planning before a release, or protecting a public launch from runaway usage bills.
---

# Cost Fit

Turn the assembled production stack into a launch cost picture: a defensible
monthly range, the free-tier verdict for each service, the first-bill
triggers, and the guardrails that keep a public launch from producing a
surprise invoice. Estimate from stated assumptions and current official
pricing, never from remembered prices.

## Rules

- Optimize for the first months of production, not a mature-business cost
  model.
- Estimate from the actual stack: the services chosen by the user or by other
  StackFit skills (`prod-db`, `deploy-plan`, `auth-plan`, `storage-plan`).
  Identify unresolved service choices as estimation gaps rather than picking
  services in this skill.
- Never invent traffic. Use user-supplied expectations when given; otherwise
  state explicit low, expected, and spike scenarios and label them as
  assumptions.
- Compare pricing dimensions, not copied headline prices. Retrieve current
  official pricing at execution time and record checked dates.
- Judge a free tier by its worst behavior at the limit — suspension, data
  loss, hard caps, or automatic billing — not by its allowance.
- Present ranges with stated drivers, never false-precision totals.
- Include operational cost drivers the project controls: retention settings,
  regions, instance counts, and always-on versus scale-to-zero behavior.
- Never read secret values or connect to provider billing accounts without
  explicit permission.
- Recommend only by default. Do not change plans, set billing limits, or
  create alerts unless the user explicitly requests implementation.

## Workflow

### 1. Establish the stack and workload

List every service the release will run, from prior StackFit recommendations,
repository evidence, and user statements. Mark unresolved choices as gaps.

Establish workload assumptions: expected visitors or requests, registered
users, data size and growth, file storage and serving volume, background job
frequency, and external metered APIs such as LLM, email, or payment calls.
Ask at most three concise questions when an answer could change the verdict;
otherwise state assumptions and mark the estimate provisional.

### 2. Map billable dimensions

Read [cost-readiness.md](references/cost-readiness.md). For each service,
identify the dimensions it bills on and connect each to the workload
assumption that drives it. Flag application behaviors that multiply metered
usage, such as chatty polling, unbounded LLM calls, uncached public
endpoints, or verbose log retention.

### 3. Judge free-tier fitness

For each service on a free or hobby tier, retrieve current terms and classify
the tier as **safe**, **usable with named risks**, or **unsafe** for this
release using the fitness gates in the reference. Commercial-use restrictions,
suspension-at-limit behavior, and data-retention limits decide this more often
than the usage allowance does.

### 4. Estimate

Produce a monthly cost range for the low, expected, and spike scenarios using
current official pricing. Attribute the range to its drivers: which service
dominates, which dimension moves first, and where the next pricing cliff sits
(the first paid plan, an overage threshold, or a scale step). Record sources
and checked dates; mark unpriceable items unknown rather than guessing.

### 5. Specify guardrails

Specify, per service: spending alerts at actionable thresholds, hard caps or
budget limits where the provider supports them and the outage trade-off is
acceptable, and application-level protections for the usage the stack cannot
cap — rate limiting on expensive endpoints, budgets on metered API calls, and
caching in front of hot paths. Distinguish alerts that inform from limits
that stop spend by stopping service.

### 6. Present

Return:

1. **Cost verdict** — the expected monthly range and whether the release fits
   the stated or assumed budget.
2. **Assumptions** — the workload scenarios and every value assumed.
3. **Per-service breakdown** — tier, billable dimensions, driving workload,
   free-tier verdict, and estimated range.
4. **First-bill triggers** — the specific actions or thresholds that end the
   free ride, in likely order.
5. **Guardrails checklist** — alerts, caps, and application protections to
   configure before launch.
6. **Cost cliffs and growth path** — what growth forces the next spend step
   and roughly when.
7. **Sources** — official pricing links with checked dates.

State which assumption, if wrong, most changes the estimate.

## Implementation handoff

If the user asks to implement guardrails, configure alerts and limits through
each provider's supported billing surface, confirm before enabling any hard
cap that can interrupt service, and verify each alert fires by checking the
provider's test or preview mechanism where one exists. Re-estimate after the
first weeks of real usage data and reconcile against actual invoices.
