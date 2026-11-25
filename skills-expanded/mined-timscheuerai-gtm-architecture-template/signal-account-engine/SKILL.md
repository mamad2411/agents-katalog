---
name: signal-account-engine
description: Build a signal-scored outbound engine in OXYGEN: source the TAM, enrich and fit-score companies, layer hiring and leadership signals into a free score and tier, then find, fit-score and enrich buyers only at Tier A and B accounts and write short researched copy and route them into 1 draft Sequence behind an approval.
---

# Build the signal-scored account engine

Read [the AP automation worked example](../../../examples/ap-automation-signal-engine/README.md) first. It is the same engine built end to end, with every column, workflow, cost and lesson.

Score every account on cheap account-level signals first, pay for contacts only at the top tier, and open each message with the trigger that put the account there. One weak signal alone never starts outreach.

## The engine

1. **Knowledge.** Write the ICP, the buyers and the signal weights as pages ([oxygen-knowledge](../oxygen-knowledge/SKILL.md)). Every score reads them.
2. **Source the TAM** ([oxygen-sourcing](../oxygen-sourcing/SKILL.md)). One Accounts table keyed on the company LinkedIn URL, so every source dedupes into one row.
3. **Enrich the company** only where the source left gaps ([oxygen-enrichment](../oxygen-enrichment/SKILL.md)).
4. **Score company fit** with a Classify column against the ICP page. Fit C stops spend.
5. **Layer signals** ([oxygen-signals](../oxygen-signals/SKILL.md)): hiring tables with an AI filter, a free formula that names the ERP from each job ad, a free ContactOut count of new finance leaders, past champions. Free lookups count them per account; free formulas turn them into points with freshness decay and a stacking bonus, then a tier.
6. **Find the buyer** at Tier A and B accounts only: a cheap people search first, ContactOut where it finds nobody.
7. **Score persona fit** with a Classify column against the buyers page; a misfit sends the search to the next role.
8. **Contact waterfall.** Work email Blitz first, ContactOut on a miss (billed on a hit), verification, then LinkedIn steps only when no email is verified.
9. **Research and copy:** an AI research agent reads each Tier A/B account (cited); an AI column writes short copy per ready buyer: the why-now fact, the pain it brings in 1 line, and 1 offer, ideally a free resource, as a question (25 to 45 words).
10. **Route** ([oxygen-workflow-authoring](../oxygen-workflow-authoring/SKILL.md), [oxygen-sequencer](../oxygen-sequencer/SKILL.md)): ready buyers go into 1 draft Sequence that reads the copy columns, behind a human approval. The Sequence stays a draft until someone starts it with a send ceiling.

Run both paths: this signal path puts fresh-signal accounts first, and a coverage path gives every fit account 1 touch every 90 days within sending capacity. Both refresh themselves. To rebuild the worked example in a new folder in one go, use `examples/ap-automation-signal-engine/build_engine.py` (`--plan` first).

## Rules

- Columns for work inside one table; Workflows only where work crosses tables or runs on a schedule. OXYGEN Workflows replace the glue scripts that usually connect these steps.
- Store formula and lookup values with a free forced run before lookups, AI columns or run conditions read them.
- Every paid step previews, pilots one row and runs under an approved ceiling.
- Prove the score: backtest the signals behind recent meetings, then compare meetings per 100 accounts by tier after 30 days.
