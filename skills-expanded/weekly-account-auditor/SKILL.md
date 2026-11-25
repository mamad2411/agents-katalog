---
name: weekly-account-auditor
description: 'Compare two complete Google Ads periods, explain the few changes that matter, and rank the next checks without changing the account. Use for a weekly review or when performance suddenly feels off.'
---

# Weekly Account Auditor

## Doctrine

A useful account review explains movement, not just totals. Compare equal, complete periods in the account timezone, find the campaigns or ad groups driving the change, and put tracking gaps ahead of confident conclusions. Recent conversions may still arrive, so a bad-looking week is not final until conversion delay is accounted for.

## When to use

- Run once a week with a current period and an equal comparison period.
- Use a connected Google Ads MCP, or paste exports with campaign metrics and date ranges.
- Bring the business target, primary conversion definition, currency, timezone, and known conversion delay when you have them.

## Run it

```
Run a READ-ONLY weekly Google Ads audit. Use live account data if connected; otherwise use the exports I paste. Change nothing.

1. Confirm the account, currency, timezone, primary conversion, target CPA or ROAS, and two equal complete date ranges. If any are missing, mark the gap before interpreting performance.
2. Compare spend, impressions, clicks, conversions, conversion value, CPA, and ROAS only where the required inputs exist. Show the formula behind every calculated metric.
3. Find the campaign or ad-group drivers behind the largest useful changes. Use entity names and IDs, current value, comparison value, and absolute change.
4. Check conversion delay, tracking interruptions, partial days, and major account changes before calling a trend real. Never estimate missing conversions from the length of an outage.
5. Return at most 5 findings, ranked by business impact and confidence. Separate observed facts, likely explanations, and next checks.

End with a short action list labeled: investigate, keep watching, or ready for approval. Do not pause, scale, or edit anything. Say "No changes were made."
```

## Guardrails

- Equal complete periods only. Do not compare a partial day with a finished day.
- A tracking outage or unresolved conversion delay lowers confidence. It does not justify pausing campaigns or scaling winners.
- Do not turn hours of missing tracking into an estimated conversion count or "corrected" CPA. The missing number is unknown until it is reconciled.
- Do not invent revenue, profit, attribution, or a target the user did not provide.
- Never recommend a fixed percentage budget move from summary metrics alone.
- A low CPA does not prove a campaign has room to scale. Ask for impression share, budget limits, query coverage, and marginal performance before proposing more spend.
- Search-term reports can omit low-activity queries. State the coverage limit when search-term evidence is used.

## Good output looks like

A five-minute review with the real movement, the entities driving it, the caveats that could change the verdict, and a short next-check list. No dashboard dump and no account changes.
