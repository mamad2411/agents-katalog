---
name: value-check
description: Audit copy, campaigns, and UX flows across 13 ethical, trust, organic-fit, and subtlety checks before shipping. Sub-skill: load only when routed from the hook-everything entry skill, not for general writing or editing.
---
# Value, Trust & Subtlety Check (13-Point Gate)

Run this 13-point audit before delivering any copy, campaign, hook idea, market analysis, or product flow. Any **NO** requires a rewrite before shipping.

## Part 1: Ethical & Zero-Scam ("Anti-Scam") Gate

| Check | Question to Verify |
|---|---|
| **1. Payoff >= Promise** | After clicking, reading, or completing onboarding, does the user receive immediate utility equal to or greater than what the hook implied? |
| **2. Zero Fabricated Receipts** | Are all metrics, latencies, dates, quotes, and citations 100% real (or explicitly marked in brackets for the user to supply)? |
| **3. Upfront Cost Honesty** | Are pricing, renewal rules, and data permissions visible *before* the user invests non-exportable work? |
| **4. Symmetric Exit** | Can the user cancel, hibernate, export their raw data, or mute notifications in the same number of clicks it took to join (`M26 Regret Regulation`)? |
| **5. Vulnerability Guardrail** | Does the design avoid exploiting grief, addiction, financial desperation, loneliness, or minors? |

## Part 2: Market Fit, Audience Calibration, Compounding & Stylometry Gate

| Check | Question to Verify |
|---|---|
| **6. The Organic Fit Gate** | If a live market trend or statistic is included (`skills/market-intelligence`), is it 100% causally connected to the user's problem with zero forced "news-pegging"? (If it feels forced, delete the trend.) |
| **7. Audience Route Calibration** | Does the hook's construal level and proof density match the target audience's ELM processing route (`skills/audience-calibration`)? |
| **8. Visual & Choice Isolation** | Is the layout free of Choice Overload (`<= 2` competing actions per viewport) with a clear Von Restorff isolation focus (`skills/visual-ux-hooks`)? |
| **9. The Second-Look Test** | If the user read your internal design notes explaining *why* this hook chord was engineered this way, would they respect the craft and feel helped - or feel manipulated? |
| **10. The Smell Test** | Can a skeptical reader smell "marketing" or "copywriting tricks"? If yes, cut adjective intensity by 40% and add a stronger **Trust Damper** (`skills/trust-architecture`). |
| **11. Chord Orthogonality** | Did you pair high-tension hooks with trust/autonomy dampers (`skills/hook-compounding`) and rotate chords across consecutive blocks? |
| **12. 85-Rule Anti-Slop Gate** | Does the text score `<= 15/100` on `tools/slop_scan.py` and obey all 85 rules in `skills/anti-slop`? |
| **13. The Reader-Feeling Check** | For each reader segment in `skills/audience-calibration` (for example, a skimmer and a deep reader), how would it feel to read this? Name any spot that bores, confuses, or talks down to that segment, and rewrite it. |

## Decision Rule

- **Fail on 2, 3, 4, or 5** requires stopping immediately and removing the deceptive or coercive element.
- **Fail on 1, 6, 7, 8, 9, 10, 11, 12, or 13** requires rewriting the chord, stripping the forced trend, injecting a stronger trust lever, or eliminating AI/hype tells until every line passes cleanly.

Check 13 comes from gregruthenbeck's "detone" practice of asking how a piece feels to read for each user segment.
