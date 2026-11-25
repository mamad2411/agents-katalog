---
name: pe-earnings-review
description: Review a company's latest quarter — results vs expectations, guidance, the market's reaction, and what changed in the thesis. Use when the user asks about earnings, "how was the quarter", or post-print catch-ups.
---

# Earnings Review

Structured read of a company's latest reported quarter.

## Data access

- Alpha Vantage app (`apps_execute_tool`, app=alpha_vantage): earnings
  history and surprise, fundamentals, price series around the print.
- The X plugin (when installed and connected) for the market conversation
  and reaction; otherwise skip commentary rather than inventing it.
- Vault (`analyst_vault_query`) only when private-market context matters
  (recent acquisitions closing into the quarter, ownership changes).

## Workflow

1. **The print.** Reported revenue and EPS vs consensus where the data
   exposes it (label beats/misses only from actual surprise fields, never
   inferred). Sequential and YoY growth.
2. **The drivers.** What moved: segments, margin bridge, one-offs — to the
   extent the data shows it. Keep to 3-4 bullets.
3. **Guidance.** Raised, held, cut, or not given (say which).
4. **The reaction.** Price move from the pre-print close to now; notable
   commentary from X when available, summarized with links.
5. **Thesis delta.** 2-3 bullets: what this quarter confirmed, what it
   challenged, what to verify next quarter.

## Rules

- Consensus numbers only from tool output; if unavailable, frame as
  "vs prior quarter/year" instead.
- Reaction commentary is attributed and linked, never paraphrased into
  fact.
- Research support, not advice — no buy/sell/hold conclusions.
