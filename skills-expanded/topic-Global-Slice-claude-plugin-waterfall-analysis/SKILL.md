---
name: waterfall-analysis
version: "1.0"
description: Guides exit waterfall analysis using Slice MCP cap-table, share-class, securities, rounds, and ownership tools. Use when answering questions about exit proceeds, liquidation preferences, participating preferred, conversion thresholds, proceeds allocation, MOIC, investor returns, or ordinary/common shareholder payouts.
---

# Waterfall Analysis

## Scope

Use when the user asks how exit proceeds would be distributed in a sale, merger, IPO, liquidation, or other liquidity event. For current cap-table ownership without an exit scenario, use cap-table-analysis. For round history and total raised, use funding-rounds-analysis.

Waterfall analysis is term-sensitive; do not present exact legal allocation unless share-class terms and seniority are available from Slice data or supplied by the user.

## Input Workflow

1. Ask for exit proceeds if the user did not provide an amount.
2. Use `cap_table_get_summary` and `ownership_get_company_breakdown` for company-level share counts.
3. Use `share_classes_list` and `share_classes_get_one` to inspect share-class rights, liquidation preference, participation, conversion ratios, and seniority where available.
4. Use `rounds_list` and `rounds_get_total_raised` to understand invested capital by round/share class.
5. Use `cap_table_search_entries` and securities tools to identify stakeholder holdings by share class.
6. Include options/warrants only according to the scenario: exercised-only, fully diluted, treasury-stock method, or as instructed by the user.

## Waterfall Mechanics

Typical seniority is most recent preferred first, then earlier preferred, then ordinary/common, unless governing documents specify pari passu or another order. Non-participating preferred receives the greater of its liquidation preference or as-converted participation. Participating preferred receives preference first and then participates in residual proceeds, sometimes subject to a cap.

At low exit values, junior classes may receive nothing after senior preferences. At high values, preferred classes may convert if as-converted proceeds exceed the preference.

## Output

Show assumptions and calculation mode first. Then summarize by share class and stakeholder where data supports it: invested capital, preference multiple, preference amount, residual/as-converted proceeds, total proceeds, and percentage of total. Include breakeven or conversion-threshold notes when useful.

If required terms are missing, provide a scenario model with clearly labeled assumptions rather than implying a definitive legal waterfall.
