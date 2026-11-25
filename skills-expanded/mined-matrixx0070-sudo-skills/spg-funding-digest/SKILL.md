---
name: spg-funding-digest
version: 1.0.0
description: Compile a short-term funding and money-market digest — repo/SOFR, bill supply, central-bank facility usage, cross-currency basis, and credit/liquidity stress signals — into a structured read on funding conditions. Educational analytical workflow, not investment advice.
author: matrixx0070
tags: [spg, funding, money-markets, repo, sofr, liquidity, basis]
capabilities: []
---

# Funding Digest

## When to use
Use this to build a structured read on short-term funding and money-market conditions: where secured and unsecured rates sit versus policy, bill supply and its effect on the front end, central-bank facility usage (repo/reverse-repo, discount window, standing facilities), the cross-currency basis, and the stress signals that flag tightening liquidity. The output is a "how tight is funding, and why" digest.

**Not for:** the policy-path and macro-cycle read (lseg-macro-rates-monitor), curve-trade construction (lseg-swap-curve-strategy), or FX carry (lseg-fx-carry-trade). This is the plumbing-level funding monitor.

This is educational analysis, not investment advice.

## Method
1. **Anchor to the policy corridor.** State the policy rate and its corridor (floor = deposit/reverse-repo facility, ceiling = lending/standing facility). Every front-end rate is read *relative* to this band.
2. **Read secured rates.** SOFR (and SRF usage), tri-party and GC repo, and the SOFR-vs-IORB / SOFR-vs-RRP spread. SOFR pushing toward or above the ceiling signals reserve scarcity; sitting on the floor signals abundant liquidity.
3. **Read unsecured and the secured-unsecured gap.** Where relevant, commercial paper, and the spread of unsecured to secured — a widening gap flags counterparty/credit concern.
4. **Track bill supply and the front end.** Heavy T-bill issuance drains cash and lifts front-end yields / repo; note the trend and any debt-ceiling or quarter-end distortions.
5. **Read central-bank facility usage.** Reverse-repo (RRP) balances (a liquidity-abundance gauge), standing-repo/discount-window usage (a scarcity/stress gauge), and reserve levels. Direction matters more than level.
6. **Check the cross-currency basis.** The FX-swap-implied USD funding premium (e.g. EUR/USD, USD/JPY 3m basis). A deeply negative basis = USD funding stress, typically at quarter/year-end.
7. **Flag stress and synthesize.** Note quarter/month-end effects, and any dislocations. Conclude: are funding conditions easy, neutral, or tight, what's driving it, and the one signal to watch next.

## Example
Policy rate 4.50%, corridor floor (RRP) 4.25% / ceiling (SRF) 4.75%. SOFR printing 4.58%, ~8bp above IORB and drifting up over two weeks — reserves getting less abundant. RRP balances have fallen sharply (cash leaving the floor into bills), consistent with heavy T-bill supply lifting the front end. Standing-repo usage still near zero (no acute scarcity yet). Cross-currency basis: 3m EUR/USD at −18bp, widening into quarter-end (mild USD funding premium, seasonal). Read: funding is transitioning from abundant toward neutral — the SOFR-IORB drift and RRP drain are the tell; watch for SRF usage as the scarcity confirmation. Illustrative — NOT advice.

## Pitfalls
- **Reading rates without the corridor.** A SOFR level is meaningless without the floor/ceiling — always express front-end rates as spreads to policy and facility rates.
- **Ignoring quarter/year-end.** Regulatory (leverage-ratio) window-dressing spikes repo and widens the basis predictably at period-ends — don't confuse seasonal with structural stress.
- **Level vs direction on facilities.** RRP or reserve *levels* matter less than their trend; a falling RRP with rising SOFR is the meaningful combination.
- **Conflating secured and unsecured stress.** Repo (secured) and CP (unsecured) tell different stories; a widening secured-unsecured gap is a credit signal, a general repo spike is a liquidity/collateral signal.
- **Treating the cross-currency basis as arbitrage.** It's a persistent funding premium driven by balance-sheet costs and USD demand, not a free trade.
- **Missing the collateral angle.** Repo specials (a specific bond trading rich in repo) signal collateral scarcity distinct from cash scarcity.

## Output format
```
As of: <date> | Region/currency: <..>
Policy corridor: rate <..>, floor <..> (RRP/deposit), ceiling <..> (SRF/lending)
Secured: SOFR <..> (spread to IORB <..>bp, to RRP <..>bp), GC repo <..>, trend <..>
Unsecured / gap: CP <..>, secured-unsecured spread <..>bp
Bill supply / front end: <trend, distortions>
Facility usage: RRP <..> (Δ), SRF/discount window <..>, reserves <..>
Cross-currency basis: 3m <pair> <..>bp (trend, seasonal?)
Stress flags: quarter/year-end <..>, repo specials <..>, dislocations <..>
Read: funding <easy/neutral/tight>, driver <..>, watch next: <..>
NOT investment advice — educational analysis only.
```

## Reference

### The policy corridor
Modern central banks operate a corridor: a **floor** (deposit facility / reverse-repo rate — the risk-free place to park cash) and a **ceiling** (lending / standing-repo facility — the backstop borrowing rate). Market secured rates should trade *within* the band. In an **abundant-reserves (floor) system**, overnight rates hug the floor; as reserves drain toward scarcity, rates climb toward the ceiling. Read every front-end print as a spread to these anchors.

### Key spreads and what they signal
- **SOFR − IORB (or − RRP):** reserve abundance vs scarcity; drifting up = draining liquidity.
- **SOFR − OIS / term-SOFR term premium:** expected policy path plus a funding premium.
- **Secured − unsecured (repo vs CP/LIBOR-successor):** credit/counterparty stress when it widens.
- **Repo specials (special vs GC):** collateral scarcity for a specific issue (distinct from cash scarcity).

### Facility usage as a liquidity gauge
- **Reverse-repo (RRP) balances:** cash parked at the floor — high = excess liquidity; a sharp fall means cash is being pulled into bills/repo (front-end tightening).
- **Standing repo facility / discount window:** the borrowing backstop — non-trivial usage flags scarcity or a specific institution's stress.
- **Reserve balances:** the aggregate; the transition from "abundant" to "ample" to "scarce" is where funding volatility rises (the 2019 repo spike is the canonical scarcity event).

### Bill supply and quarter-end mechanics
- **T-bill issuance** drains cash from the system and lifts front-end yields and repo; debt-ceiling episodes (paydown then flood) whipsaw the front end.
- **Quarter/year-end:** leverage-ratio and balance-sheet reporting make dealers pull back from repo intermediation, spiking secured rates and widening the cross-currency basis — a predictable, seasonal dislocation, not structural stress.

### Cross-currency basis
The FX-swap-implied cost of borrowing USD synthetically vs directly. A **negative basis** means paying a premium for USD via FX swaps — a USD funding shortage. It widens in risk-off and at period-ends, reflecting bank balance-sheet costs and regulatory constraints; it is a persistent CIP deviation, not arbitrage. A key real-time gauge of global USD funding stress.
