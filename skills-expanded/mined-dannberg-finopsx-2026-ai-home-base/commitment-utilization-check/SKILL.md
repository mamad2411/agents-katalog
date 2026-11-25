---
name: commitment-utilization-check
description: Report on current utilization across all active commitments (CUDs, RIs, Savings Plans). Triggers on phrases like "commitment utilization", "are we using our CUDs", "RI report", "savings plan check", "commitment portfolio". Computes current utilization, days remaining, projected over- or under-use, and the dollar impact of any gap.
---

# Commitment Utilization Check

When invoked, produce a per-commitment report covering utilization, time remaining, projected outcome, and dollar impact. This is the report the practitioner runs before any commitment-related conversation — renewals, expansion decisions, finance variance reviews.

## Inputs to confirm before starting

- The cloud provider(s) to include (AWS, GCP, Azure, or all)
- The commitment types to include (CUDs, RIs, SPs, EDPs, dedicated capacity)
- The lookback window for utilization (default: trailing 30 days)
- Whether to include commitments that expire in the next 90 days as a separate "needs attention" section

## Steps

1. **Pull the active commitment portfolio.** For each commitment, get:
   - Provider, commitment type, scope (account / family / region)
   - Term, start date, end date, days remaining
   - Hourly or monthly commitment value
   - Coupled service or instance type

2. **Compute utilization.** For each commitment:
   - Trailing N-day utilization %
   - Trailing 7-day utilization % (recency check)
   - Whether utilization is trending up or down over the lookback window

3. **Project the outcome.** For each commitment, project to expiration based on current trend:
   - If under-utilized: projected total $ wasted by expiration (commitment value not consumed)
   - If over-utilized: projected over-the-commit $ paid at on-demand rates

4. **Categorize.** Group commitments into:
   - **Healthy**: utilization 90–100%, no action needed
   - **Under-utilized**: <85%, action needed (reduce on renewal, or find more usage to apply)
   - **Over-utilized**: >100% sustained, action needed (expand commitment to capture rate savings)
   - **Expiring soon**: ends within 90 days, regardless of utilization
   - **At-risk**: utilization volatile (>20% week-over-week swings), recommend monitoring

5. **Compute the gap dollars.** Total $ left on the table from under-utilization plus total $ overpaid from on-demand overages. This is the headline number for any leadership conversation.

## Output format

```
## Headline
[Total commitment value | Trailing utilization | $ gap (under + over) | # of commitments needing action]

## Needs action
[Per-commitment list of anything in Under-utilized, Over-utilized, or Expiring soon. Include: what, why, recommended action, dollar impact.]

## Healthy
[Brief list — name and utilization % only. The reader doesn't need detail here.]

## At-risk (volatile utilization)
[Per-commitment list with the volatility metric and what's likely causing it.]

## Recommendations for the next renewal cycle
[2–4 bullets — what should change in the next round based on this report.]
```

## House rules

- Never recommend buying more commitments based on a single month's utilization. Always look at trailing 90 days minimum for purchase recommendations.
- Always show the dollar gap, not just the percentage. "85% utilization" is abstract; "$24K wasted by year-end at this rate" is not.
- For expiring commitments, the recommendation must include both the renewal recommendation and a fallback if renewal doesn't happen in time.
- Distinguish between commitments that are under-utilized because of a workload migration (legitimate, won't recover) and those that are under-utilized because of seasonality or temporary changes (will recover, hold steady).

## Customization notes

- If your org has a commitment laddering strategy (e.g., "always 60% covered with 1-year, 30% with 3-year, 10% on-demand"), encode it here so the report flags deviations.
- Some orgs treat EDP / private pricing differently from per-commit instruments; if so, note the distinction so the AI doesn't lump them together.
- For multi-cloud orgs, run this skill once per provider rather than trying to consolidate; the commitment models are different enough that a unified report obscures more than it shows.
