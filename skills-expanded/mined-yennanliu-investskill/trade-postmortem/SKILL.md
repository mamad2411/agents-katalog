---
description: Review a closed trade or a year of trades — process vs. outcome matrix, plan adherence, the biases that showed up, what the pre-trade skills said, and the one lesson for the journal; reads closed thesis-tracker files
---

# Trade Post-Mortem

## ⚠️ Data Verification — Do This Before Any Analysis

Before running any analysis, always retrieve the latest market data for the ticker:

1. **Fetch current price** — use web search or ask the user for the live price, 52-week range, and market cap. Never assume a price from training data.
2. **Confirm key figures** — every fill (date, side, shares, price, fees) from the thesis file's decision log or the broker export; dividends received while held; the **total-return** closes of SPY and the chosen sector ETF on the exact entry and exit dates (adjusted for distributions); the stock's beta over the holding window; and the KPI values that were current on the day each decision was made. A post-mortem built on remembered fills or end-of-month benchmark prices grades the wrong trade.
3. **State your data source** — fill in the `Data & Sources` header (next section) so the origin, as-of date, retrieval path, and confidence of every figure are explicit at the top of the output.
4. **Flag stale data explicitly** — if live data is unavailable, display this warning before proceeding:

> ⚠️ **Live data unavailable.** The following analysis uses training-data estimates which may be significantly out of date. Verify all prices and metrics before making any decisions.

Never silently substitute training-data estimates for current prices. When in doubt, ask the user to paste the latest quote.

---

## 📋 Data & Sources Header — Open Every Output With It

The first thing in the output is this provenance block, filled in — never left as placeholders. It is the standard documented on the [Data & Accuracy](https://yennanliu.github.io/InvestSkill/data-and-accuracy.html) page and the first thing `result-validator` looks for:

```
Data & Sources
  As of:      <date the figures represent, e.g. 2026-06-30>
  Source:     <primary docs — SEC EDGAR 10-K/10-Q, company IR, FRED, exchange data …>
  Retrieval:  <pasted by user | web/tool retrieval | model memory>
  Confidence: <HIGH | MEDIUM | LOW>
```

- `Retrieval: model memory` must be paired with `Confidence: LOW` — memory is a placeholder until confirmed against a primary source.
- Mixed sources: list each with its own as-of date rather than blending them.
- Sources disagree on the same figure (a closing price, a deal term): prefer the primary source (SEC filing, company release, exchange data) over an aggregator, then the most recent dated one. Show both values with their sources and dates, say which you used and why, and never average them.
- Data the user pasted is reported as `pasted by user`; do not upgrade its confidence beyond what the user's own source supports.

---

## 🌐 Output Language — `--lang zh-TW`

English is the default. With `--lang zh-TW` — or when the user writes in Traditional Chinese and asks for a Chinese answer — write the whole analysis in Traditional Chinese (繁體中文, Taiwan usage), keeping it machine-checkable:

- **Translate** every heading, narrative paragraph, table header and bullet. Give each metric's English name in brackets the first time it appears — 自由現金流（Free Cash Flow, FCF） — so the reader can match it to the glossary and to English analyses.
- **Keep in English** tickers, figures and units, SEC form and item names (10-K Item 7, Form 4), the four `Data & Sources` field labels (`As of`, `Source`, `Retrieval`, `Confidence` — the Retrieval value may be written in Chinese, e.g. 使用者提供), and the Investment Signal box and JSON footer exactly as specified — field names and the BULLISH / NEUTRAL / BEARISH, HIGH / MEDIUM / LOW, BUY / HOLD / SELL, STRONG / MODERATE / WEAK values. Tools parse them.
- Title the invalidation section **論點失效條件（Thesis Invalidation）**, and close with the disclaimer in Chinese: **免責聲明：** 僅供教育用途，非投資建議。
- Use Taiwan financial terms: 殖利率、本益比、營業利益率、自由現金流、聯準會、選擇權、買權／賣權、除息日、預扣稅.

---

## Overview

Every other skill in the catalog looks forward. `thesis-tracker` writes the contract before the trade and re-checks it while the position is open; `position-ladder` plans the entries and trims; `tax-lens` prices the exit. Once the position is closed, nothing looks back — and looking back is the only way an investor learns whether their *process* works, as distinct from whether they were lucky this time.

**This skill grades the decision separately from the result.** It takes a closed trade (or a year of them), reconstructs what the investor knew and planned at each decision point, and answers five questions in order: *Which quadrant of the process-vs-outcome matrix is this? Did I do what my plan said? Which biases showed up, and where is the evidence? Were the pre-trade analyses right, and for the right reasons? Where did the return actually come from?* It ends with one sentence for the journal — the lesson — and a **Process Score 0–10**.

It reuses the vocabulary of Learning lesson 13, *Psychology & Process* (`site/content/LEARNING-PSYCHOLOGY.md`): the four quadrants (*deserved success*, *bad luck*, *dumb luck*, *deserved loss*), the eight biases and their antidotes, the journal template, and the sell discipline of rules vs. reasons.

**What it is not.** It is not a re-analysis of the stock with hindsight, and it is not a tax calculation (`tax-lens` does that). The signal block at the end is the only forward-looking part: the view on *re-entering the ticker today*, informed by what the post-mortem learned. Pairs with `thesis-tracker` (its closed files are this skill's primary input), `position-ladder` (the plan the sizing is graded against), `tax-lens` (after-tax result and wash-sale check on any re-entry), and `learning-coach` (to turn the lesson into a drill).

---

## 1. Modes and Inputs

| Mode | Invocation | What it does |
|------|------------|--------------|
| **Single trade** | `trade-postmortem ZEPH` | Reads `output/thesis/ZEPH.md` (status CLOSED) or a pasted trade log, grades one round trip |
| **Year** | `trade-postmortem --year 2026` | Reads every CLOSED file in `output/thesis/` (and/or a broker CSV) with a close date in the year; per-trade grades plus aggregate statistics |

| Input | Required | Default if unstated |
|-------|----------|---------------------|
| Ticker (single mode) or year (year mode) | ✅ | — |
| Closed thesis file `output/thesis/<TICKER>.md` **or** a pasted trade log / broker CSV | ✅ one of the two | — |
| Benchmarks | optional | SPY plus the SPDR sector ETF matching the stock's GICS sector (XLK, XLV, XLF, …); state the choice |
| Prior analysis outputs (`stock-eval`, `bear-case`, `stock-valuation`, `earnings-preview`, …) dated before the decisions | recommended | use the "Informed by" column of the decision log; if none survive, say the pre-trade comparison is limited |
| `position-ladder` plan (rungs, ceiling) | optional | the `Ceiling:` field in the thesis file |
| Account type and tax bracket | optional | pre-tax only, with a one-line pointer to `tax-lens` |
| Ticker to evaluate for re-entry (year mode) | optional | the largest-loss trade of the year — the most likely candidate for a revenge trade |

### Reading a closed `thesis-tracker` file

The file follows the `thesis-tracker` saved-file contract exactly; read it section by section:

| File section | What the post-mortem takes from it |
|--------------|------------------------------------|
| `# Thesis · <TICKER> · opened YYYY-MM-DD · status CLOSED` | Open date; confirm status is CLOSED (if not, stop — run `thesis-tracker <TICKER> --close` first, or treat as a pasted log and say so) |
| `Data & Sources` line | The as-of date of the original analysis — the information set the entry decision is graded against |
| `## Thesis` paragraph and `Horizon / Entry / Size / Ceiling` line | The mechanism, the planned horizon, the planned entry, size, and share-count ceiling |
| `## KPIs` table | The thresholds and the last recorded values — did a KPI breach precede the exit? |
| `## Triggers` table | Which triggers fired and when (`FIRED YYYY-MM-DD`), and what action each obliged (review / trim / exit) |
| `## Catalysts` | Which expected events happened, and what evidence they produced |
| `## Pre-mortem` | Did the actual failure (or success) path match the one written in advance? |
| `## Decision log` | Every action, price, reason, and the skill that informed it — the raw material for plan adherence and bias detection. The final `closed` row carries the exit reason and P&L written by `--close` |

### Reading a pasted trade log or broker CSV

Accept any export with at least `date, side (buy/sell), ticker, quantity, price`; use `fees`, `dividends`, and `lot id` when present. Match sells to buys by **specific lot ID if given, else FIFO**, and say which. Without a written plan there is nothing to adhere to: reconstruct the *implied* plan from the user's own words (ask: "what were you expecting, and what would have made you sell?"), label it **reconstructed**, and cap the plan-adherence component at 5 / 10 — a plan written after the fact is shaped by the outcome.

---

## 2. Framework

### Phase 1 — Reconstruct the timeline (the hindsight firewall)

Build one table of every decision, with only the information available **on that date**:

| Date | Action | Shares · price | Position after | Thesis status then | KPI / trigger state then | Reason given then | Informed by |
|------|--------|----------------|----------------|--------------------|--------------------------|-------------------|-------------|
| YYYY-MM-DD | open / add / trim / close / review | | shares · % of portfolio | INTACT / WEAKENED / BROKEN | e.g. GM 58.2% vs ≥ 55% ✓ | from the decision log | skill + run date |

**The hindsight rule:** a decision is graded on what was knowable when it was made. "The CEO resigned three months later" is not evidence the entry was bad; "the 10-Q that showed the margin breach was out a week before the add" is evidence the add was bad. Mark any fact the user only learned later as `(later)` and keep it out of the process grade.

### Phase 2 — The outcome, honestly measured

| Measure | How | Value |
|---------|-----|-------|
| Gross P&L ($) | proceeds − cost basis, all lots | |
| Dividends received ($) | sum while held (ex-dates inside the window) | |
| Costs ($) | commissions + fees + estimated spread (½ bid-ask × shares per fill) + FX if any | |
| **Total return after costs** | (gross P&L + dividends − costs) ÷ total capital deployed | % |
| Money-weighted return (IRR) | when there were multiple entries/exits; it charges the adds and trims for their timing | % annualized |
| Holding period | first buy → last sell; and the weighted average by lot | days |
| SPY total return, same window | first-entry date → exit date, distributions reinvested | % |
| Sector ETF total return, same window | as above | % |
| **Excess vs. benchmark** | total return − benchmark return (use the sector ETF when the thesis was about the company within its industry, SPY when it was a market or macro call; state which) | pp |
| Tax note | short- vs. long-term (> 1 year), wash-sale risk if re-bought within 30 days — the numbers go to `tax-lens` | one line |

**Outcome grade (column of the matrix):** *good outcome* = excess total return after costs vs. the chosen benchmark ≥ 0; *bad outcome* = < 0. Report the absolute return beside it, and when the two disagree say so in one line ("made 6%, but the sector ETF made 14% — the capital would have done better in the index").

### Phase 3 — Return attribution: where the money came from

Decompose the stock's own price-plus-dividend return over the window (first entry → final exit, as if one lot) into three additive layers:

| Layer | Formula | Reads as |
|-------|---------|----------|
| Market | R_SPY | What simply being in stocks earned |
| Sector | R_sector − R_SPY | What being in this industry added or cost |
| Stock-specific | R_stock − R_sector | What this company did on its own — the only layer the thesis claimed to know |
| *(check)* | the three sum to R_stock | |

When the stock's beta over the window is far from 1 (below 0.7 or above 1.3), add the beta-adjusted view: expected = β × R_SPY; **alpha = R_stock − β × R_SPY**. A high-beta winner in a rising market may have zero alpha.

Then a fourth, separate number — **timing and execution**:

```
Plan return     = return had every fill followed the written plan (planned rungs, ceiling,
                  and an exit on the day the first exit-trigger FIRED)
Timing effect   = actual total return − plan return
```

A positive timing effect means the deviations helped *this time* (that is still a process question — see Phase 5); a negative one is the dollar cost of not following the plan. If no written plan exists, report timing against the simplest alternative — the whole position bought on the first-entry date and sold on the exit date — and label it.

### Phase 4 — Plan adherence

Grade each element against what the thesis file (or reconstructed plan) said **before** the trade:

| Element | Plan said | What happened | Adhered? | Cost of the deviation |
|---------|-----------|---------------|----------|----------------------|
| Entry | price / rung / condition | | ✓ / partial / ✗ | $ or pp vs. plan |
| Sizing | initial size, % of portfolio, cap | | | |
| Adds | rungs, and "no add while WEAKENED / BROKEN" | | | |
| Ceiling | share-count ceiling from `position-ladder` | max shares actually held | | |
| Stop / exit trigger | which trigger, action obliged | date it fired → date acted on (the **lag**) | | |
| Profit exit / trim | target or valuation range | | | |
| Reviews | next-check dates in the file | done on time / late / skipped | | |

Score each row 10 (followed), 5 (partially, or followed late), 0 (ignored); the **adherence sub-score** is their average over the rows the plan actually covered. Two rules: an **exit-trigger lag** of more than 10 trading days counts as *partial*, more than 30 as *ignored*. And a deviation that made money is still a deviation — score it as one, and record its sign in the cost column so year mode can test whether the investor's overrides add value on average.

### Phase 5 — Biases detected

For each bias from lesson 13, look for its **evidence pattern** in the decision log. A bias is *confirmed* only when the log shows the pattern; it is *suspected* when the pattern is partly there or the user's own words suggest it; otherwise *not seen*. Never diagnose a bias from the outcome alone.

| Bias | Evidence pattern in the log | Verdict |
|------|-----------------------------|---------|
| **Anchoring** on purchase price | Reasons that reference cost basis: "sell when back to even", "waiting for $X" where $X is the entry; exit dates cluster near the cost basis | confirmed / suspected / not seen |
| **Disposition effect** | Winner sold on a gain with thesis still INTACT and no rule fired; loser held past a fired exit trigger; holding period of losers ≫ winners (year mode test, Phase 7) | |
| **FOMO / herding** | Entry after a > 20% run in the prior 20 sessions; thesis paragraph dated the same day as (or after) the entry; reasons citing social media, "everyone", or the chart alone; the 24-hour cooling-off skipped | |
| **Confirmation bias** | No `bear-case` run before the entry or at reviews; KPIs re-defined or thresholds loosened after a breach; reviews that cite only bullish sources | |
| **Sunk cost** | Adds made while the thesis was WEAKENED or BROKEN, or above the ceiling, with reasons like "lower my average" | |
| **Overconfidence** | Size above the stated cap; cap raised mid-trade; "high conviction" used to justify size; no pre-mortem written | |
| **Loss aversion** | Exit trigger fired and the position was held to "avoid locking in the loss"; stop moved down | |
| **Recency / extrapolation** | Entry or add justified by the last few quarters' trend alone; target derived by extending recent growth without a base rate | |

Quote the decision-log line that is the evidence. A bias without a quoted line is a guess — mark it *suspected* at most.

### Phase 6 — What the pre-trade skills said vs. what happened

For every analysis listed in the "Informed by" column (and any others the user pastes, dated before the decision):

| Skill · run date | What it said (signal, score, key claim) | What happened | Verdict |
|------------------|------------------------------------------|---------------|---------|
| e.g. `stock-eval` · 2025-02-28 | BULLISH 7.1 — margin expansion to 60% | GM peaked at 58%, then fell to 52% | wrong on the mechanism |
| e.g. `bear-case` · 2025-02-28 | Thesis-killer #2: competitor pricing | Competitor cut prices in Q3 | right — and the user ignored it |

Verdicts: **right for the right reason**, **right for the wrong reason** (the call worked but the stated mechanism did not happen — treat as luck), **wrong**, **not testable** (the window was too short). Then answer: *did the user follow the analysis, override it, or not run it?* An override that was right is still worth recording; three overrides in a row that were right is evidence of edge, one is not.

### Phase 7 — Year mode: aggregate statistics

Run Phases 1–6 per trade (abbreviated: one line each), then compute across the closed trades of the year:

| Statistic | Formula | Healthy reading |
|-----------|---------|-----------------|
| Trades closed | count (a round trip = one ticker from first buy to flat) | — |
| **Hit rate** | winners ÷ trades (winner = total return after costs > 0) | Means little alone — read with payoff |
| Average win / average loss | mean % (and $) of winners; of losers | |
| **Payoff ratio** | average win ÷ \|average loss\| | > 1.5 makes a 45% hit rate profitable |
| **Expectancy per trade** | hit rate × avg win − (1 − hit rate) × \|avg loss\| | > 0, and stated in % and $ |
| Profit factor | gross gains ÷ gross losses | > 1.5 |
| Largest loss vs. plan | the worst trade's actual loss ÷ its planned maximum loss (stop distance × planned size) | ≤ 1.2×; > 2× means the stop or the ceiling did not hold |
| **Holding period: winners vs. losers** | median days held, winners and losers separately | Losers held ≥ 1.5× as long as winners, *and* average win < average loss → **disposition effect flagged** |
| Excess vs. SPY, whole year | money-weighted return of the closed trades − SPY over the same capital-weighted windows | ≥ 0 |
| Quadrant counts | number of trades in each of the four cells | Most trades in the top row |
| Bias frequency | confirmed count per bias | The most frequent bias is next year's rule |
| Override value | sum of the "cost of deviation" column across all trades | Negative → follow the plan; positive over 10+ overrides → the plan needs rewriting, not ignoring |
| Average Process Score | mean, and its correlation with excess return | |

**Sample-size warning:** fewer than 20 closed trades makes every rate above an anecdote. Say so, report the numbers anyway, and lean on the per-trade process grades, which do not need a sample.

### Phase 8 — Process Score (0–10) and the quadrant

The headline number of the post-mortem. It grades **the decisions, on the information available at the time** — not the P&L.

| Component | Weight | 10 looks like | 0 looks like |
|-----------|--------|---------------|--------------|
| Pre-trade plan quality | 25% | Falsifiable thesis, 3–5 KPIs with thresholds, exit triggers, pre-mortem, size inside cap, `bear-case` read — all dated before the first buy | No written plan; or written after the entry |
| Plan adherence (Phase 4) | 35% | Every row followed; exit acted on within 10 trading days of the trigger | Ceiling breached, adds into a WEAKENED thesis, fired exit trigger ignored |
| Bias exposure (Phase 5) | 25% | Start at 10; −2 per *confirmed* bias, −1 per *suspected*; floor 0 | Three or more confirmed biases |
| Review discipline | 15% | Every next-check done on time, decision log written at the time of each action, `--update` run after each catalyst | Reviews skipped; log reconstructed afterwards |

```
Process Score = 0.25 × Plan + 0.35 × Adherence + 0.25 × Bias + 0.15 × Review
```

**Quadrant:** Process Score ≥ 6.0 → *good decision* row; < 6.0 → *bad decision* row (5.0–5.9 is reported as "borderline", but it still goes in a row). Column from Phase 2. Name the quadrant with lesson 13's label and its instruction:

| | **Good outcome** | **Bad outcome** |
|---|---|---|
| **Good decision** | *Deserved success* — repeat the process; do not raise size because it worked | *Bad luck* — do not "fix" a process that was right; confirm the thesis actually broke rather than the price just moving |
| **Bad decision** | *Dumb luck* — the most dangerous cell; write down exactly what was skipped | *Deserved loss* — fix the process, not the stock |

### Phase 9 — The journal lesson

One sentence, in the first person, that names **the behaviour** (not the stock), **the evidence**, and **the rule** that would have prevented or repeated it:

> *"When the file says WEAKENED, the ladder is closed — I added 150 shares into a margin miss and it cost me $1,620 against my own plan."*

Rules: no lesson about the market ("tech was weak"), no lesson that needs hindsight ("I should have known the CEO would leave"), and no more than one. If the quadrant is *deserved success* or *bad luck*, the lesson is what to **keep** doing. In year mode, the lesson comes from the most frequent confirmed bias or the largest override cost. Format it as a journal entry row so it can be pasted into the decision log.

### Phase 10 — Re-entry view (the only forward-looking part)

The signal block answers one question: **knowing what this post-mortem found, would I buy this ticker today, at today's price?** It is lesson 13's anchoring antidote applied after the fact — the old cost basis and the old P&L are irrelevant.

| Component | Weight | 10 looks like | 0 looks like |
|-----------|--------|---------------|--------------|
| Thesis today | 40% | The original mechanism is still alive *and* the exit was a process error or a valuation trim; or a fresh `stock-eval` / `thesis-tracker` reading is INTACT-grade | The mechanism was falsified structurally (Phase 6: "wrong on the mechanism") |
| Price vs. value today | 30% | Current price inside or below a recent `stock-valuation` range | Above the range; or no valuation available (score 5 and cap Confidence at LOW) |
| Fit with the lesson | 30% | The lesson is about execution that a rule now fixes; the user has shown edge in this kind of setup | The lesson says the user has no edge here (repeated *dumb luck* / *deserved loss* on the same setup, or the name sits outside their circle of competence) |

If the user supplies no current data on the ticker, report the re-entry Score as **5.0** (NEUTRAL, Confidence LOW, Action HOLD — "no view without fresh work"). A re-entry is never a re-opening of the old file: it requires a new `thesis-tracker` Open with a new thesis, and a `tax-lens` wash-sale check when the exit was at a loss within the last 30 days.

---

## 3. Output Format

**Single-trade mode**
1. **Data & Sources** header (fills, benchmark prices, dividends; the thesis file path and its as-of date)
2. **Verdict line first:** `ZEPH · Deserved loss · Process 5.6 / 10 · −20.0% after costs vs. sector ETF +4.0% · lesson below`
3. **Executive summary** — three sentences: what happened, which quadrant and why, what changes
4. **Timeline** with the hindsight firewall (Phase 1)
5. **Outcome table** (Phase 2) and **attribution** — three layers, beta note if needed, timing effect (Phase 3)
6. **Plan adherence** table with the cost of each deviation (Phase 4)
7. **Biases detected** with quoted evidence (Phase 5)
8. **Pre-trade skills vs. what happened** (Phase 6)
9. **Process Score** breakdown and the **2×2 matrix** with the trade placed in its cell (Phase 8)
10. **The journal lesson** as a paste-ready decision-log row (Phase 9)
11. **Re-entry view** (Phase 10), **Thesis Invalidation**, and the **Investment Signal block**

**Year mode** — Data & Sources; a one-line-per-trade table (ticker · dates · return · excess · Process Score · quadrant · top bias); the aggregate statistics table (Phase 7) with the disposition-effect test spelled out; the quadrant counts in the 2×2; the year's one lesson; then the re-entry view, Thesis Invalidation and signal block for the named (or largest-loss) ticker.

---

## Example

```
User: trade-postmortem ZEPH   (reads output/thesis/ZEPH.md, status CLOSED)

[ZEPH is a fictional ticker; all figures are hypothetical.]

The file's plan: thesis opened 2025-03-03 — gross margin expands past 60% as the new
product line scales. KPI gross margin ≥ 55%; exit trigger "GM < 55% for one quarter →
exit". Ladder: 100 sh at $40, 100 at $37, 100 at $34; ceiling 300 sh.

The decision log shows: bought 100 @ $40.00 and 100 @ $37.00 per plan; 2025-08-12 the
10-Q showed GM 53.9% and the status went WEAKENED, yet on 2025-08-14 the user bought
150 @ $33.00 ("great chance to lower my average"); the exit trigger FIRED 2025-11-06
(GM 52.1%) with the stock at $34; the user held ("I'll sell when it's back to $36") and
sold all 350 sh @ $29.00 on 2026-02-10. Fees $15, no dividends.

Outcome: cost $12,650, proceeds $10,150 → −$2,515 gross, −$2,530 after fees,
−20.0% on capital deployed. Over the window, SPY +9.0%, sector ETF +4.0% (hypothetical):
excess vs. sector −24.0 pp → bad outcome. Attribution (first entry $40 → exit $29,
−27.5%): market +9.0, sector −5.0, stock-specific −31.5 pp. Plan return: 100 @ $40 +
100 @ $37, no add while WEAKENED, exit 200 sh @ $34 when the trigger fired → −$910
(−11.8%). Timing effect: −$1,620 — the cost of the two deviations.

Plan adherence: entry 10, sizing 10, adds 0 (added while WEAKENED), ceiling 0 (350 > 300),
exit 0 (trigger lag ~65 trading days), reviews 5 (the August check ran 3 weeks late)
→ adherence 25 / 6 = 4.2. Biases: sunk cost confirmed (quote: "lower my average"), anchoring
confirmed ("back to $36" is near the $36.14 average cost), disposition suspected.
Pre-trade skills: stock-eval was wrong on the mechanism; bear-case thesis-killer #2
(competitor pricing) was right and was not wired into a trigger.

Process Score = 0.25×8 + 0.35×4.2 + 0.25×5 + 0.15×6 = 5.6 → bad-decision row (borderline)
→ Deserved loss. Lesson: "When the file says WEAKENED, the ladder is closed — I added
150 shares into a margin miss and it cost me $1,620 against my own plan."

Re-entry view at today's price: the margin mechanism was falsified, no fresh valuation
supplied → re-entry Score 3.5 / 10, BEARISH, Action SELL (stay out; no re-entry without
a new thesis). Then Thesis Invalidation and the signal block.
```

---

## Notes

- **Grade the decision, not the price chart.** The hindsight firewall (Phase 1) is the whole point of the skill; a post-mortem that uses later facts to grade earlier decisions teaches the outcome, which is exactly the lesson the 2×2 exists to prevent.
- **A good outcome never raises the Process Score, and a bad one never lowers it.** If the user pushes back ("but it made money"), the answer is the *dumb luck* cell.
- **Benchmarks are total-return and window-matched.** Price-only SPY understates the market by its dividend yield; a calendar-year benchmark against a seven-month trade is meaningless.
- **One lesson.** Five lessons are a list nobody re-reads. Pick the one with the largest dollar cost or the most frequent bias.
- **Tax figures are pointers, not calculations.** Short- vs. long-term status and wash-sale exposure on a re-entry go to `tax-lens`; this skill is educational only.
- **Before:** `thesis-tracker <TICKER> --close` (so the file is CLOSED with its final log row). **After:** paste the lesson into the next thesis file's decision log; run `learning-coach --quiz` on lesson 13 if a bias was confirmed; and, if re-entering, `thesis-tracker` Open with a new thesis, `position-ladder` for the size, and `tax-lens` for the wash-sale window.
- Keep closed files; year mode reads them. Where the environment cannot read `output/thesis/`, ask the user to paste the file.

## Thesis Invalidation

After delivering the analysis signal, specify what would reverse it:

**If signal is BULLISH (re-entry justified) — the view breaks if:**
- The KPI that the original thesis depended on (named in the old file) prints below its threshold again at the next filing — the post-mortem judged the exit a process error; a second breach says it was the thesis
- The price rises above the top of the current `stock-valuation` range before a new thesis file is written — the re-entry becomes a chase, which is the FOMO pattern from Phase 5
- The bias the post-mortem confirmed shows up in the new trade's first decision-log row (e.g. a size above the cap "because I know this one now")

**If signal is BEARISH (stay out) — the view breaks if:**
- The mechanism the post-mortem judged falsified is restored by new evidence (e.g. two consecutive quarters back above the old KPI threshold, from the filings, not from guidance)
- The price falls well below a freshly computed valuation range with the business stable — the "no" was about price, and the price has changed
- The user writes a new, narrower thesis that does not depend on the falsified mechanism, and it survives `bear-case`

**Re-run this analysis when:**
- [ ] Next earnings release of the ticker (for the re-entry view)
- [ ] The user is about to re-enter the ticker — run it before the order, not after
- [ ] Price moves ±15% from current level
- [ ] Year end (year mode), or after every 10 closed trades
- [ ] Material news event (acquisition, leadership change, regulatory decision)

## Standard Signal Output

This skill grades a **closed** trade, so the signal block cannot describe it. State the mapping explicitly: the box expresses the **re-entry view on the ticker today** (Phase 10) — `Signal: BULLISH` means that, knowing what the post-mortem found, buying it again at today's price is justified under a new written thesis; `NEUTRAL` means no edge either way, or no fresh data (Score 5.0, Confidence LOW, Action HOLD); `BEARISH` means stay out. `Action: BUY` means "open a new `thesis-tracker` file and size with `position-ladder`" — never "re-open the old trade"; `Action: SELL` means "do not re-enter" (and close any residual shares). In year mode the box covers the ticker the user named, or the year's largest-loss trade.

All analysis concludes with this standardized block:

In the output, the box below is followed immediately by this machine-readable footer — the same values as the box, filled in (no placeholders, no comments), so tools can read the result without parsing the box:

```json
{"investskill": "1", "skill": "trade-postmortem", "ticker": "<TICKER, or null for a portfolio / market-wide view>", "as_of": "<YYYY-MM-DD from Data & Sources>", "signal": "<BULLISH | NEUTRAL | BEARISH>", "confidence": "<HIGH | MEDIUM | LOW>", "horizon": "<SHORT-TERM | MEDIUM-TERM | LONG-TERM>", "score": 0.0, "action": "<BUY | HOLD | SELL>", "conviction": "<STRONG | MODERATE | WEAK>", "retrieval": "<pasted by user | web/tool retrieval | model memory>", "sources": ["<each primary source, dated>"]}
```

```
╔══════════════════════════════════════════════╗
║              INVESTMENT SIGNAL               ║
╠══════════════════════════════════════════════╣
║ Signal:      BULLISH / NEUTRAL / BEARISH     ║
║ Confidence:  HIGH / MEDIUM / LOW             ║
║ Horizon:     SHORT / MEDIUM / LONG-TERM      ║
║ Score:       X.X / 10                        ║
╠══════════════════════════════════════════════╣
║ Action:      BUY / HOLD / SELL               ║
║ Conviction:  STRONG / MODERATE / WEAK        ║
╚══════════════════════════════════════════════╝
```

Score Guide: 8.0–10.0 Strongly Bullish | 6.0–7.9 Moderately Bullish | 4.0–5.9 Neutral | 2.0–3.9 Moderately Bearish | 0.0–1.9 Strongly Bearish
Confidence: HIGH (strong data, clear signals) | MEDIUM (mixed signals) | LOW (limited data, conflicting signals)
Horizon: SHORT-TERM (1 week–3 months) | MEDIUM-TERM (3 months–1 year) | LONG-TERM (1+ years)

**Note:** The Score in the box is the Re-entry Score from Phase 10, mapped onto the standard scale. **The Process Score is not the box Score** — it grades past decisions and is reported in the body (Phase 8 and the verdict line); a high Process Score on a closed trade says nothing about whether to buy the stock again.

**Disclaimer:** Educational analysis only. Not financial advice.
