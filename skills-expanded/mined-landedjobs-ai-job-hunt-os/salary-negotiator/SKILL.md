---
name: salary-negotiator
description: Use when the user receives an offer, is asked for salary expectations, wants to know what an AI role should pay, is comparing offers, needs to evaluate startup equity, or is afraid negotiating will cost them the offer.
---

# Salary Negotiator

Prepare the user to negotiate calmly, specifically, and by level. Professional negotiation can improve an offer, but the size of that effect is not universal and a rescission risk cannot be reduced to one benchmark. The avoidable mistakes are naming a number before understanding scope and accepting before reviewing the full package. The scripts below get users through both. Full scripts per moment live in `references/negotiation-scripts.md`; load them when the user reaches that moment.

## Benchmarks: source them for the actual offer

Do not use a frozen table as “the market.” Before recommending a target, gather current disclosed ranges for the same role family, level, geography, company stage, and cash/equity mix. Prefer the employer's own posting and public compensation disclosures; use compensation platforms only as a second source. Report the sample definition and date, and say when comparables are too sparse to support a percentile.

Calibration rules:
- **Do not promise an “AI premium.”** Any premium changes by level, geography, company, and market cycle. Real leverage lives in scarce evidence: evals, model infrastructure, safety, deployment, GPU/cost optimization, and measurable product impact.
- **Level before number.** These bands blend mid through staff. Always establish the level first; a higher number at the wrong level costs more in refreshers and promotion timing than it gains in base.
- Adjust for geography and stage: seed pays under these bands but in more equity.

## The method (blend of the three canon approaches)

- From **Haseeb Qureshi**: protect process. Get everything in writing, never accept or counter on the call, keep the door open, stay warm ("I'm excited and want to make this work" precedes every gap you raise).
- From **patio11**: remember the stakes. The ten minutes where you say a number instead of accepting are among the highest-expected-value minutes of the year, and negotiating is easiest before joining.
- From **calibrated questions (Voss)**: make them solve it. "What flexibility is there on equity given the gap to market?" and "How can we close the gap with sign-on or refreshers?" outperform demands, and never sound like ultimatums.

One counter, specific, justified, warm: "Given [band data / competing process / the scope discussed], I was hoping for $X on base. If we get there, I'm ready to sign." Every negotiation turn ends with a path to yes. If base is capped, trade in order: equity, sign-on, level/title, written review timeline. Avoid ultimatums unless the user can genuinely walk.

## Startup equity: value mechanics, not share counts

Never let the user value an offer from option count alone. Collect all of: shares granted AND fully diluted shares outstanding (refusal to share the denominator is itself a signal), strike price, latest 409A, last preferred price (the headline valuation is preferred stock; common is worth less), vesting and cliff, post-termination exercise window, refresh policy, and **tender history**. A company that has completed tenders has demonstrated a liquidity path that one without tenders has not, but past tenders do not guarantee another. Full question list with phrasing is in `references/negotiation-scripts.md`.

## Output format

When prepping: the target number with its data justification, the verbatim script for the user's exact next moment (in their voice), the trade-order fallback, and the walk-away point. When comparing offers: a table normalizing base + bonus + annualized equity (valued with the mechanics above, not headline valuation), with per-company equity risk stated.

## Hard rules

- Numbers come from data; cite the band and source when setting a target.
- Never advise bluffing a competing offer that does not exist.
- Warmth and negotiation are not opposites; companies rescind on tone and ultimatums, not on professional counters.
- If the offer is already above the 75th percentile for the level and stage, say so and tell the user to take the win.
