---
name: right-sizing-recommendations
description: Generate ticket-ready right-sizing actions for a service, workload, or team. Triggers on phrases like "right-size", "rightsizing", "are we over-provisioned", "what can we shrink", "utilization opportunities". Pulls utilization data, generates concrete recommendations with dollar impact estimates, formatted so the practitioner can paste each one into a ticket and assign it.
---

# Right-Sizing Recommendations

When invoked, turn utilization data into a list of concrete actions an engineering team can act on. The output is not "your fleet is over-provisioned" — it's "shrink this specific instance from N1 to N2, save $X/month, here's the ticket text."

## Inputs to confirm before starting

- Scope: service, workload, team, project, or specific resource list
- Utilization window (default: trailing 30 days)
- Resource types in scope (default: VMs, managed databases, persistent disks; expand on request)
- Constraints: anything that must NOT be touched (production-critical workloads, customer-impacting services, anything inside a change freeze)

## Steps

1. **Pull utilization.** For each in-scope resource, get CPU, memory, network, and (where relevant) disk IOPS over the window. Also pull the current size/tier/SKU and its monthly cost.

2. **Apply right-sizing logic.** A resource is a candidate for right-sizing if:
   - **Down-size**: P95 utilization on the binding dimension is below 40%, sustained across the window
   - **Up-size**: P95 utilization on any dimension is above 85%, with throttling or evictions observed
   - **Schedule**: utilization shows clear daily/weekly patterns (e.g., near-zero on weekends) and the resource isn't required 24/7
   - **Eliminate**: <5% utilization across the window, no recent connections or queries

3. **Skip the ones you shouldn't touch.** Filter out anything matching the user's constraints. Also auto-skip:
   - Resources with creation time within the last 14 days (too new to judge)
   - Resources tagged with `do-not-rightsize` or equivalent
   - Resources whose owning team is in a change freeze

4. **Estimate dollar impact.** For each recommendation:
   - Current monthly cost
   - Projected cost after the change
   - Monthly savings ($)
   - Annualized savings ($)
   - Confidence: high / medium / low (based on how stable the utilization pattern is)

5. **Generate the ticket text.** One ticket per recommendation. See template below.

## Ticket template

Each ticket follows this format so the receiving engineer has everything they need without having to ask:

```
**Right-size [resource_id] from [current size] to [recommended size]**

**Why:** Trailing 30-day P95 utilization is [X]% on [CPU/memory/etc.],
well below the [threshold]% we use as the rightsize trigger.

**Action:** Change the instance type / tier / SKU.

**Impact:**
- Current monthly cost: $[A]
- Projected monthly cost: $[B]
- Monthly savings: $[A-B]
- Annualized: $[12*(A-B)]

**Risk:** [low / medium / high — name the specific risk if not low]

**Validation:** After deploying, monitor [metric] for [N] days. If
utilization climbs above [threshold]%, revert.

**Confidence:** [high / medium / low]
```

## House rules

- Never recommend a change without an estimated dollar impact. A right-sizing recommendation without numbers is a chore, not an action.
- Round dollar figures to the nearest dollar for monthly, nearest hundred for annualized. False precision (`$47.32/month`) makes the recommendation feel computed by a script and ignored.
- If confidence is low, say so — don't bury it. Engineering teams will tune you out fast if they get burned by a confident-sounding bad recommendation.
- For each batch of recommendations, include a one-line "if you do all of these" total at the top. That's the number leadership cares about.

## Output format

```
## Headline
[Total recommendations: N | Total monthly savings if all applied: $X | Annualized: $Y]

## Recommendations (sorted by impact)
[One ticket per recommendation, in the format above]

## Skipped (and why)
[Any resources that would have been candidates but were excluded by constraints — useful for the practitioner to verify the skip reasons are still valid]
```

## Customization notes

- The 40% / 85% / 5% thresholds are starting defaults. Tune them to your org's risk tolerance — production-heavy fleets might use 50% as the down-size trigger.
- If your org uses commitment-based discounts, factor that in: a right-size that drops a resource below a committed tier may not save what the on-demand math suggests.
- Add your specific change-management process to the ticket template (e.g., "this needs SRE review before merging") so the recommendations match how work actually gets done.
