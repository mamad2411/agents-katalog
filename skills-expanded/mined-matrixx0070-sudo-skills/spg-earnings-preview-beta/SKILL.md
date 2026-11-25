---
name: spg-earnings-preview-beta
version: 1.0.0
description: Build a fast pre-earnings expectations map for a company — consensus, whisper, options-implied move, KPIs to watch, and the setup/skew — so you can read the print in real time. Educational analytical workflow, not investment advice.
author: matrixx0070
tags: [spg, equity, earnings, consensus, implied-move, kpi, preview]
capabilities: []
---

# Earnings Preview

## When to use
Use this to prepare for a company's earnings release: assemble consensus estimates and the buy-side "whisper," derive the options-implied move, list the KPIs and guidance lines that will move the stock, and characterize the setup (positioning, prior reaction pattern, skew) so you can interpret the print as it lands rather than scramble.

**Not for:** the full valuation and thesis build (lseg-equity-research), the standing company snapshot (spg-tear-sheet), or vol-surface analysis in its own right (lseg-option-vol-analysis). This is the focused pre-event expectations map.

This is educational analysis, not investment advice.

## Method
1. **Fix the event.** Date/time (BMO/AMC), quarter, and whether there is a call/guidance. Note comparison periods (YoY and QoQ) and any calendar quirks (extra week, FX, acquisitions).
2. **Assemble the bar.** Consensus revenue, EPS, and the key segment/KPI lines. Distinguish **published consensus** from the **whisper** (the buy-side expectation, usually above consensus into a strong quarter) — the stock reacts to the bar it's actually held to.
3. **Derive the options-implied move.** From the ATM straddle of the nearest expiry spanning the event: `implied move ≈ (ATM call + ATM put price) / spot`. This is the market's one-standard-deviation expected reaction — the "how much is priced" number.
4. **List the swing factors.** The 3–5 lines that actually move the stock: the headline beat/miss, the guidance vs consensus (usually more important than the print), the one KPI the debate hinges on (net-adds, bookings, margin, backlog), and any known controversy.
5. **Read the setup.** Positioning (crowded long/short, short interest), the stock's recent run into the print, and its **historical earnings reaction** (average absolute move, and how often it moves more/less than implied). A crowded long into a high bar is a fragile setup.
6. **Frame the reaction scenarios.** Beat-and-raise / in-line / miss-or-guide-down, each with the likely KPI pattern and a rough directional read — anchored to the implied move, not a price target.
7. **State what to watch live.** The exact metrics and their thresholds, and what would be a genuine surprise (vs already-priced). End with the setup's asymmetry.

## Example
Company reports AMC Thursday. Consensus rev $2.10B / EPS $1.34; whisper closer to $2.15B / $1.40 (buy-side bar is higher). Options-implied move (nearest weekly straddle) ≈ ±8.5% — elevated vs the 6.0% trailing average, so the market expects a big reaction. Swing factor: cloud-segment growth (debate is decel from 31%→ high-20s%); guidance for next quarter matters more than the print. Setup: stock +18% into the report, positioning crowded long, and it has moved *more* than implied in 4 of last 6 quarters — a fragile, high-bar setup. Scenarios: beat + reaffirm ≈ modest (priced); beat + raise on cloud ≈ upside > implied; in-line print with soft guide ≈ downside > implied given the run-up. Watch: cloud growth vs ~28%, operating-margin guide. Illustrative — NOT advice.

## Pitfalls
- **Reacting to the print, ignoring the guide.** Forward guidance usually drives the move more than the reported quarter — lead with it.
- **Consensus vs whisper confusion.** Beating published consensus but missing the whisper still sells off; know which bar the stock is held to.
- **Treating the implied move as a forecast of direction.** It's a magnitude (1σ), symmetric by construction — pair it with skew (put vs call IV) for the directional lean.
- **No historical reaction context.** Whether a stock typically moves more or less than implied is decisive for how to read the setup.
- **Ignoring positioning.** A great number into a crowded long and a high bar can still fall (the "good-not-good-enough" selloff).
- **Stale KPIs.** The metric that mattered last year may not be this quarter's debate — refresh the swing factors.

## Output format
```
Company: <ticker> | Report: <date, BMO/AMC>, Q<..> | Call/guidance: <y/n>
The bar: consensus rev <..> / EPS <..> / key KPI <..>; whisper: <..>
Options-implied move: ±<..>% (nearest expiry straddle) vs trailing avg <..>%; skew lean: <..>
Swing factors (3–5): <headline / guidance / key KPI / controversy>
Setup: positioning <..>, run into print <..>, historical: avg move <..>%, > implied in <x/6>
Scenarios: beat&raise <..> / in-line <..> / miss-or-guide-down <..>
Watch live: <metric: threshold> ... | Asymmetry read: <..>
NOT investment advice — educational analysis only.
```

## Reference

### Options-implied move
`Implied move ≈ (ATM straddle premium) / spot`, using the expiry that first spans the event (weekly if available). More precisely it approximates the expected 1-standard-deviation move over the option's life; for a single overnight event, strip out the non-event vol so you isolate the event premium. A rule-of-thumb refinement: implied move ≈ straddle/spot × 0.85 to adjust for the straddle overstating the 1σ move slightly.

### Consensus vs whisper vs guidance
- **Published consensus:** the mean/median of sell-side estimates — the visible bar.
- **Whisper:** the buy-side's actual expectation, often diverging from consensus into a strong or weak quarter; the stock reacts to *this* effective bar.
- **Guidance:** management's forward outlook — for growth names, the single biggest driver of the post-print move. A beat with a cut guide typically falls; a small miss with a raise can rally.

### Reaction skew and positioning
- **Skew (put vs call IV)** into the print shows the market's directional fear/greed; combine with the symmetric implied move for a lean.
- **Positioning** (short interest, crowding, fund ownership, the run into the report) sets the asymmetry: crowded longs into a high bar are fragile; hated/short names can squeeze on any relief.
- **Historical reaction:** average absolute move and hit-rate vs implied tells you whether this stock is a "sells the news" or "under-reacts then drifts" name (post-earnings-announcement drift).

### KPI taxonomy by model
- **Subscription/SaaS:** net revenue retention, net adds, billings/RPO, gross margin, FCF margin.
- **Consumer/retail:** comps (same-store sales), traffic vs ticket, inventory, gross margin.
- **Semis/hardware:** bookings/backlog, book-to-bill, utilization, ASPs, inventory.
- **Banks:** NII, NIM, credit provisions, loan growth, deposit betas.
Identify the *one* KPI the current debate hinges on — that's the number the reaction keys off, not the headline EPS.

### What is already priced
The move is only as good as the surprise. Before the print, ask: what does consensus + whisper + guidance history + the implied move already assume? A "beat" that merely meets the whisper is priced in. The tradable information is the gap between the result and the *effective* expectation, read against positioning.
