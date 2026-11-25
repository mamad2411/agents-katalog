---
name: oxygen-sourcing
description: Find companies and people that are not in the workspace yet and land them in OXYGEN Tables: account and TAM lists, hiring companies, lookalikes, local businesses and buyers at named accounts, through free previews, typed plans, priced dry runs and approved live runs.
---

# Source new accounts and people

Read [the runtime contract](../../../docs/runtime-contract.md). Sourcing lands new companies and people in a Table with every route and cost inspectable. Enriching rows you have is [oxygen-enrichment](../oxygen-enrichment/SKILL.md); hiring, funding and tech signals are [oxygen-signals](../oxygen-signals/SKILL.md).

| Ask | Free first |
|---|---|
| Accounts by firmographics, technology, lookalikes, a TAM | `companies search preview`, then `companies search plan` |
| Who is hiring for a role | `companies search preview --source hiring` |
| People by persona, or at up to 50 named companies | `people search preview`, then `people search plan` |
| People at every company in a table | `people search plan --from-table <table>` |
| "Build leads for this ICP" | `lead-sourcing plan` |

Exact filter names come from `oxygen companies search filters --json` and `oxygen people search filters --json`; invalid enum values fail the request.

## Loop

1. Preview or plan, free: up to 50 real rows, the total that match and a priced `next_step`.
2. Dry-run the chosen route: the request, its size, its pages and its price. The dry-run request is the provider contract.
3. Show rows, route, dropped filters, size and ceiling; get approval.
4. Run live with `--approved --max-credits` at that size, wait on the ingestion and read the table.
5. Companies first, then people at the accepted accounts; enrich only the rows that survive.

## Gates

- Never invent a match count; quote one only when the provider published it.
- A dropped filter is never applied. Report each one, and never run a watch-list request whose account selector was dropped.
- A sourcing approval covers the pull only; enrichment, CRM writes and outreach are separate approvals.
- Binding a source as a recurring feed is a second approval with its own per-cycle ceiling.

In [the AP automation worked example](../../../examples/ap-automation-signal-engine/README.md), Blitz company search returned 196 accounts for 4 credits (1 credit per 50 companies) and Blitz people search costs 1 credit per 50 people.
