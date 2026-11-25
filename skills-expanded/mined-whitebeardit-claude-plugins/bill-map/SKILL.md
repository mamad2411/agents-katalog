---
name: bill-map
description: Where the AWS money goes, in two minutes and in the same shape for every company - the bill of the last 30 days classified into fixed categories (Compute, Network, Data & databases, Storage, SaaS & Marketplace, Commitments, Observability, Security, Tax, Other) with the biggest lines, read from Cost Explorer in the payer account. Use when the user asks "where does our AWS money go", "what is the biggest line", "how much is data transfer / NAT / marketplace", or wants the bill breakdown before deciding whether to run the full audit. Read-only.
argument-hint: "[--profile payer] [--start YYYY-MM-DD --end YYYY-MM-DD]"
---

# Bill map

Payer profile from the configuration (`${user_config.payer_profile}`) unless given as argument.
Cost Explorer from the payer sees every linked account; from a member account only that one,
so if the user gives a member profile, say that the map is partial.

```bash
python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/ce_breakdown.py" --profile <payer> [--start … --end …] map
python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/ce_breakdown.py" --profile <payer> accounts
```

Then open the two or three biggest lines with `usage "<service>"` (always `EC2 - Other` when it
is in the top: it hides data transfer, EBS, NAT and public IPv4) and, if "Commitments" shows up,
run `sp` to know whether the Savings Plan is saturated.

Answer with:

1. The total and the window.
2. The category table as printed (category, USD, %, varies with usage?).
3. The top lines table, and for each of the three largest, one sentence on what it is and whether
   it responds to volume cuts, to contracts, or to right-sizing/shutdown.
4. Which category should be the first front of a cuts plan, and whether the Savings Plan (if
   any) is saturated, because that decides if anything "by time of day" can be cut.
5. One line offering `/aws-cost-audit:audit` for the full plan.

Keep the category names exactly as the script prints them, translated to the user's language if
they are not reading English; the fixed vocabulary is what lets two companies compare their maps.
Do not estimate savings here: this skill maps, the audit sizes.
