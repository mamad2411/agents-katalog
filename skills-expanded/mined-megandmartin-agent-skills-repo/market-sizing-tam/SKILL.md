---
name: market-sizing-tam
description: Build a TAM/SAM/SOM estimate with sourced assumptions, bottom-up math preferred over top-down, and a pessimistic/base/optimistic sensitivity table. Use when the user asks "how big is this market", "TAM for my pitch deck", "size the opportunity", "is this market big enough", or needs SAM/SOM numbers investors will probe. Don't use for dissecting a single rival's product — that's competitor-teardown — or for weekly market monitoring — that's trend-radar.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Research & Analysis, Market Sizing, Strategy, Fundraising]
    related_skills: [competitor-teardown, trend-radar, csv-data-analyst]
---

# Market Sizing (TAM / SAM / SOM)

Builds a market size a founder can defend under questioning: bottom-up first (count of buyers × price they'd pay), top-down only as a cross-check, and every single number carrying a receipt — a source URL, a user-provided figure marked as such, or an explicitly labeled assumption. The standard: no naked numbers. A TAM slide with unsourced figures is the fastest way to lose an investor's trust.

## When to Use

- User needs TAM/SAM/SOM for a pitch deck, accelerator application, or go/no-go decision.
- User asks "is this market big enough to bother?"
- Stress-testing a market claim someone else made ("the report says $40B — is that real?").
- **Not for:** analyzing one competitor (`competitor-teardown`); tracking market signals over time (`trend-radar`); crunching a CSV of your own sales data (`csv-data-analyst`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Bottom-up TAM | (# of potential buying units) × (realistic annual price) — both sourced |
| SAM | TAM × reachable fraction (geography, segment, channel) — each filter sourced |
| SOM | SAM × attainable share in 3 yrs — anchored to a comparable's actual trajectory |
| Buyer counts | census/labor stats, industry bodies, app-store counts, LinkedIn filters — record URL + date |
| Cross-check | independent top-down (analyst report) — flag if it diverges >3x from bottom-up |
| Sensitivity table | python heredoc, step 6 — pessimistic / base / optimistic per assumption |

## Procedure

1. **Precheck** — get from the user: the specific buyer definition ("who writes the check"), the price point (their actual or intended pricing), and geography/segment limits. If web tools are available, sources get fetched live; if not, every external number must come from the user with its origin named — otherwise it goes in as `assumption` with low confidence.
2. **Define the unit** — one sentence: "A buyer is <who>, paying <price> per <period> for <what>." Every later number hangs off this. Vague unit = fictional TAM.
3. **Count buyers (bottom-up)** — find the number of buying units from a primary-ish source: government stats, industry association counts, platform self-reporting, LinkedIn/job-board filter counts. Record the figure, URL, publication date, and what it actually counts (which is rarely exactly your buyer — state the mismatch).
4. **Price the unit** — use the user's real pricing, or comparable products' actual prices (source them). Annualize. TAM = buyers × annual price. Show the multiplication explicitly.
5. **Filter to SAM and SOM** — SAM: apply each reachability filter (geography, language, segment, channel) as a separate sourced or labeled percentage — no single mystery "×20%". SOM: anchor to evidence, e.g. a comparable company's year-3 revenue or share (sourced), or channel math (audience × conversion). "1% of the market" with no mechanism is banned.
6. **Sensitivity table** — vary the 2–3 weakest assumptions:
   ```bash
   python3 <<'PY'
   buyers = {"pess": 60_000, "base": 120_000, "opt": 200_000}   # source each in the report
   price  = {"pess": 240, "base": 480, "opt": 720}               # annual $, sourced
   reach  = {"pess": 0.05, "base": 0.12, "opt": 0.20}            # SAM filters combined
   for k in ("pess", "base", "opt"):
       tam = buyers[k] * price[k]
       print(f"{k:>4}: TAM ${tam:,.0f} | SAM ${tam*reach[k]:,.0f}")
   PY
   ```
7. **Cross-check top-down** — find one independent analyst/industry figure for the market. If it's within ~3x of bottom-up TAM, note agreement. If not, investigate which definition differs and say which you trust and why. Then deliver via the template.

## Output Template

```
# Market Size — <product/market> — <date>
Buyer unit: <who> paying $<X>/yr for <what>

## Bottom-up
TAM = <N buyers> [source: <url>, <date>, counts: <what it actually counts>]
      × $<price>/yr [source: <url or "user's live pricing">]
      = $<TAM>
SAM = TAM × <filter 1: X% — source/label> × <filter 2: ...> = $<SAM>
SOM = SAM × <mechanism-based share — anchor: <comparable + source>> = $<SOM>

## Sensitivity
| Scenario | Buyers | Price | Reach | TAM | SAM |
|---|---|---|---|---|---|
| Pessimistic / Base / Optimistic rows |

## Cross-check
Top-down: $<X> [source] — <agrees / diverges because <definition difference>>

## Assumption register
| # | Assumption | Value | Receipt (url/user/assumption) | Confidence |

## Verdict
<Big enough for the goal? One paragraph, referencing the pessimistic case.>
```

## Pitfalls

- **Top-down laundering** — "$50B market, we take 1%" survives zero investor questions. Recovery: bottom-up is the spine; top-down only cross-checks. If only top-down data exists, say so and mark the whole estimate low-confidence.
- **A number without a receipt slips in** — one unsourced "80M SMBs" poisons the whole model. Recovery: the assumption register is mandatory; before delivering, scan every numeral in the doc and confirm it appears in the register or derives from ones that do.
- **Source counts the wrong thing** — "number of US restaurants" used for "restaurants that would buy scheduling software". Recovery: for each source, write one line on the mismatch between what's counted and your buyer, and haircut accordingly with the haircut labeled as an assumption.
- **SOM by wishful percentage** — "we'll capture 5%" with no mechanism. Recovery: SOM must come from channel math or a named comparable's actual trajectory; otherwise report SOM as "not estimable yet" — that's more credible than fiction.
- **Stale or circular sources** — a 2019 blog citing a 2016 report citing a press release. Recovery: record publication dates; prefer primary sources; if the chain ends in a vendor press release, label it `vendor-claimed` and lower confidence.

## Verification

- [ ] Every number appears in the assumption register with a receipt and confidence label
- [ ] TAM math shown explicitly (buyers × price), reproducible by hand
- [ ] Sensitivity table has all three scenarios with stated assumption ranges
- [ ] SOM anchored to a mechanism or comparable, not a naked percentage
- [ ] Top-down cross-check present, divergence explained if >3x
