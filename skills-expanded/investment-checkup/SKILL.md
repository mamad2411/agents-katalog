---
name: investment-checkup
description: "Use this skill when the user wants a read-out of how their investments are doing — returns against the benchmark, drift from their target mix, what their ETFs actually hold, and what fees have cost. Use it for 'how's my portfolio', 'am I too concentrated', 'how much am I paying in fees', or a periodic investment review, even if they only name one holding. Not for a single price or quote (answer directly), not for pace toward retirement (on-track), not for what to buy or sell."
---

Run a full investment checkup. Read-only: surface what is there; propose trades only if the
user asks.

## Gotchas

- TWR is the "how did the investments do" number; MWR includes the timing of the user's own
  deposits. A wide gap between them means deposit timing helped or hurt — say which.
- get_returns gives null TWR/MWR when price history is thin (data_quality.sufficient=false). Say
  so; never quote a number.
- get_portfolio_xray reports an unmapped share. State it — exposure figures exclude it.
- The benchmark is the profile's preferred_benchmark (get_profile) — pass it to get_returns as
  `benchmark`; never pick one yourself.
- Fee drag per holding is fees against current value, worked with the calculate tool.
- Amounts are in the base currency the tools report.

## Steps

1. get_portfolio — holdings and current values.
2. get_returns — 1M / 3M / YTD / 1Y / ALL, TWR and MWR, against the user's benchmark.
3. get_rebalance_plan — asset classes over or under the target mix by more than a small
   tolerance, with the drift amount.
4. get_portfolio_xray — sectors or regions that are meaningfully concentrated.
5. get_fees_summary — total fees paid, then holdings ranked by fee drag; call out the
   disproportionate ones and why (frequent small trades add up).
6. Summarize the findings, most important first, in a tight skimmable list.
