---
name: NSELens
description: Use this skill whenever the user asks for Indian stock picks, top N stocks to buy, rebound candidates, GTT setups, swing trade ideas, or buy recommendations for the Indian stock market. Triggers on phrases like "top 3 stocks", "top 5 Indian stocks", "top 10 stocks to buy", "best stocks for tomorrow", "NSE rebound picks", "stocks with potential", "which stocks should I look at", "stock picks", "Indian market analysis", or any request for a ranked list of Indian equity recommendations — even casually phrased. Always use this skill for any Indian stock research or ranking request. Never skip this skill when the user asks about stock picks, even if they don't say "report" or "analysis" explicitly.
---

# NSELens — Indian Stock Research Skill


Produces a data-verified, multi-dimensional Indian stock research report for the next trading day. Covers the Nifty 100 universe. Picks are based purely on potential — no sector diversification constraint. All prices must be verified from named sources before inclusion.

---

## Step 0 — Parse request and ask horizon

**Extract from the user's message:**
- **N**: Number of stocks (3, 5, or 10). Default if not stated: 5.
- **Horizon**: How long until they want the position to be profitable.

**If horizon is not stated**, ask before doing anything else — in a friendly, non-jargon way:

> "Quick one before I dive in — when are you hoping to see this trade profitable? Like within 3 months, 6 months, or are you thinking a full year or even longer?"

**Map the answer:**

| What the user says | Label | GTT or Entry Zone? |
|---|---|---|
| 3 months / quarterly / soon / short term | Q | GTT setup |
| 6 months / half yearly / mid term | H | GTT setup |
| 1 year / yearly / 12 months | Y | Entry zone + 12M target |
| 2 years / long term / 24 months | L | Entry zone + 24M target + accumulation guidance |

GTT format applies to Q and H only — NSE/BSE GTT orders have a 1-year validity, so they are only appropriate for horizons up to 1 year. For Y and L, use the Entry Zone format (no GTT language).

---

## Step 1 — Macro context scan

Before touching individual stocks, search for the current environment. Run these searches:

```
Nifty 50 index level today [current month year]
India VIX today
Brent crude oil price today
USD INR exchange rate today
RBI monetary policy stance [current year]
```

Summarise as a one-line **Market Pulse** header at the very top of the report:

> **Market Pulse** · Nifty: X,XXX (▲/▼ X%) · VIX: XX · Crude: $XX/bbl · USD/INR: XX.XX · RBI: [hawkish / neutral / accommodative]

This gives users the macro environment in which the picks are being made.

---

## Step 2 — Build a candidate longlist

Run 3–4 searches to surface Nifty 100 stocks that have declined and have rebound potential:

```
Nifty 100 stocks declined 15 percent buy opportunity [current month year]
oversold Indian large cap midcap stocks analyst buy recommendation [current month year]
Indian stocks 52 week low rebound potential [current month year]
Nifty 100 correction buying opportunity analyst target [current month year]
```

Build a longlist of **12–15 candidates**. Apply these initial filters:
- Declined ≥10% from recent 52-week high or ATH
- Part of Nifty 100 (large or mid-cap)
- Not a penny stock
- No ongoing SEBI investigation or fraud allegation (check in news)
- Promoter pledging <70% (above this, flag but don't auto-reject — explain the risk)

---

## Step 3 — Deep research per candidate (run for every stock)

Do this for each of the 12–15 candidates. Be thorough — the quality of the final picks depends entirely on the quality of this step.

### 3a. Live price — HARD RULE ⚠️

Search: `[STOCK NAME] NSE share price [today's date] [month] [year]`

**You MUST find the CMP confirmed by a named source. Acceptable sources:**
Dhan · Tickertape · Investing.com India · Kotak Neo · Groww · INDmoney · Screener.in · Bajaj Broking · Moneycontrol · NSE India · Business Standard · Economic Times Markets

**If you cannot find a price from a named source: skip this stock entirely and move to the next candidate. Never estimate, assume, or carry forward a price from memory.**

Collect:
- CMP (state source name + date, e.g. "₹826.85 via Dhan, Apr 2")
- 52-week high and 52-week low
- % decline from 52-week high
- 50 DMA and 200 DMA (if findable)
- Whether stock is above or below both DMAs

### 3b. Fundamentals

Search: `[STOCK NAME] fundamentals PE ratio revenue profit margin promoter pledging 2026`

Collect:
- Revenue trend: growing / flat / declining (last 2–3 quarters)
- Net profit trend (last 2–3 quarters, % YoY)
- PE ratio and PB ratio
- EBITDA margin
- ROE (return on equity)
- Debt status: debt-free / low debt (D/E <0.5) / moderate / high
- **Promoter pledging %** — flag with ⚠️ if >30%, flag with 🚨 if >50%
- Dividend yield (if any)

### 3c. Upcoming earnings date

Search: `[STOCK NAME] Q4 results date 2026` or `[STOCK NAME] board meeting earnings April May 2026`

This is a **mandatory field** in every card. Write "Not yet confirmed" if not found. An earnings date within 30 days = strong near-term catalyst — note it clearly.

### 3d. Analyst opinions and targets

Search: `[STOCK NAME] analyst target price brokerage recommendation 2026`

Collect:
- Consensus rating: Strong Buy / Buy / Hold / Sell
- Average 12-month price target (₹)
- How many analysts cover this stock
- Specific brokerage calls — name the firm and target (e.g. "Kotak: Buy, ₹1,050 | Axis Securities: Buy, ₹1,150")
- Never state a target price without naming the source brokerage

### 3e. Relative strength vs Nifty

Search: `[STOCK NAME] vs Nifty performance YTD 2026` or `[STOCK NAME] 1 year return vs Nifty`

Compare:
- If Nifty is down X% YTD and the stock is down Y%:
  - Y < X → ✅ Outperforming index (bullish divergence — stock is holding up better)
  - Y ≈ X → ➡️ In line with market
  - Y > X → ⚠️ Underperforming index (falling harder than market — needs strong fundamental justification to include)

### 3f. News and institutional activity

Search: `[STOCK NAME] news FII DII buying April 2026` and `[STOCK NAME] latest news [current month] 2026`

Collect:
- Key news in last 30 days (positive or negative)
- Any FII or DII buying / selling data mentioned
- Corporate events: buyback, dividend announcement, merger, acquisition, regulatory action
- Any analyst upgrades or downgrades in last 60 days

### 3g. Retail sentiment

Search: `[STOCK NAME] stock outlook community investor sentiment 2026`

Assign one tag: **Bullish / Mixed / Bearish / Neutral**

Always state what the tag is based on:
- "based on analyst consensus and recent news flow" (institutional signal)
- "based on community and forum discussion" (retail signal — lower weight)
- "mixed — institutional positive, retail cautious" (split signal)

Be transparent about the source quality. Never label retail sentiment as "Bullish" based on a single news article.

### 3h. Technical levels

From the price data and any technical reports found:

Collect:
- Key support levels (1–2 price levels)
- Key resistance levels (1–2 price levels)
- RSI reading — search if needed: `[STOCK NAME] RSI technical analysis [current month] 2026`
  - <30 = oversold (strong buy signal)
  - 30–45 = weak but recovering
  - 45–55 = neutral
  - >60 = getting overbought
- Whether price is above or below 50 DMA and 200 DMA

---

## Step 4 — Confidence scoring

Score each candidate on exactly 4 dimensions. One point per dimension. No partial points.

| Dimension | Award 1 point if... |
|---|---|
| **Fundamentals** | Revenue growing YoY, PE reasonable for sector, margins stable or improving, promoter pledging <30%, low/no debt |
| **Technicals** | Price near key support, RSI <45, trading near or below 200 DMA |
| **Sentiment** | Analyst consensus is Buy or Strong Buy, no major negative news in last 30 days, FII/DII not net sellers |
| **Catalyst** | Upcoming earnings within 60 days, or known sector tailwind, or positive corporate event (buyback / acquisition / new order) |

**Score → Confidence label:**
- 4/4 → **HIGH**
- 3/4 → **MEDIUM-HIGH**
- 2/4 → **MEDIUM**
- 1/4 → **LOW** → discard this candidate, replace with next on longlist
- 0/4 → **REJECT**

Show the breakdown on every card:
> `Fundamentals ✓ | Technicals ✓ | Sentiment ✗ | Catalyst ✓ → 3/4 = MEDIUM-HIGH`

---

## Step 5 — Risk/Reward calculation

After setting the GTT or Entry Zone prices, compute:

```
Risk %   = (Trigger − Stop Loss) / Trigger × 100
Reward % = (Target − Trigger) / Trigger × 100
R:R      = Reward % / Risk %
```

- R:R ≥ 2.0 → Strong setup ✅
- R:R 1.5–2.0 → Acceptable setup
- R:R < 1.5 → Weak setup ⚠️ — flag on the card, include with caution

---

## Step 6 — Rank and select top N

After scoring all candidates, rank them by:
1. Confidence score (4 first, then 3, etc.)
2. Risk/reward ratio (higher is better, as tiebreaker)
3. Catalyst proximity (upcoming earnings sooner = higher priority)

Select the top N. Note in the report header if multiple picks happen to be from the same sector — it's allowed but worth flagging so users can decide how to size positions.

**Minimum upside rule:** Every pick must have a credible path to ≥8% upside from trigger price. If not achievable, drop and replace.

---

## Step 7 — Build GTT or Entry Zone

### For Q and H horizons — GTT Setup

- **Buy Trigger**: At or just below CMP, at a confirmed technical support level. Never set above CMP. Aim for the strongest nearby support.
- **Target**: ≥8% above trigger for Q horizon. 12–18% for H horizon. Anchored to next resistance level and/or analyst target.
- **Stop Loss**: 5–8% below trigger. Use tighter stops (5%) for large-caps with strong fundamentals. Wider (8%) for volatile stocks or those with high beta.
- **GTT note**: "GTT orders on Zerodha Kite / Upstox / Angel One have 1-year validity — no need to reset daily."

### For Y and L horizons — Entry Zone

- **Accumulation Zone**: A price range (not a single price) where the user should build their position gradually over weeks. Set the lower bound at strong support and upper bound at current CMP.
- **12M Target** (Y) or **24M Target** (L): Based on analyst consensus + DCF/fundamental fair value found in research.
- **Key Support to Watch**: The level where, if broken on a weekly close, the thesis is broken. User should reassess or exit if this breaks.
- **Position guidance**: "Buy in 3 tranches — ⅓ now, ⅓ on a 5% dip, ⅓ on further weakness or after quarterly results confirm the thesis."
- No GTT language for these horizons.

---

## Step 8 — Render the report

### Always include:
1. Market Pulse header (from Step 1)
2. Horizon and date context line (e.g. "3-month swing picks · Next trading day · Nifty 100 universe")
3. Individual stock sections (format depends on N — see below)
4. Standard disclaimer at the end

---

### Format for top 3 and top 5 — Full Cards

Each card, in this order:

```
[RANK]. [COMPANY NAME] · NSE: [TICKER] · [SECTOR] · [LARGE/MID-CAP]

CMP: ₹XXX (source: [NAME], [DATE]) | 52W: ₹XXX – ₹XXX | Down X% from high
Confidence: Fundamentals ✓/✗ | Technicals ✓/✗ | Sentiment ✓/✗ | Catalyst ✓/✗ → X/4 = [LABEL]

WHY IT DIPPED
2–3 sentences. Company-specific or macro cause. Be specific, not generic.

FUNDAMENTALS
Revenue: [trend] | Net Profit: [trend] | PE: X | PB: X | Margins: X% | Debt: [level]
Promoter pledging: X% [flag if needed] | Dividend yield: X% | Earnings date: [DATE or "Not confirmed"]

RELATIVE STRENGTH vs NIFTY
[Stock] down X% YTD vs Nifty down Y% → [Outperforming / In line / Underperforming]
Retail sentiment: [Bullish / Mixed / Bearish] (based on [source type])

TECHNICAL OUTLOOK
Support: ₹XXX / ₹XXX | Resistance: ₹XXX / ₹XXX
50 DMA: ₹XXX ([above/below]) | 200 DMA: ₹XXX ([above/below]) | RSI: ~XX ([condition])

CATALYSTS
[Tag 1] · [Tag 2] · [Tag 3]

[GTT SETUP or ENTRY ZONE — based on horizon]
Trigger: ₹XXX | Target: ₹XXX (+X%) | Stop Loss: ₹XXX (-X%)
Risk/Reward: X.Xx | GTT validity: 1 year on NSE/BSE platforms
[OR for Y/L: Accumulation zone: ₹XXX–₹XXX | 12M/24M target: ₹XXX | Key support: ₹XXX]

RISKS
⚠️ [Risk 1] · ⚠️ [Risk 2] · ⚠️ [Risk 3]
```

---

### Format for top 10 — Table + Compact Cards

**First: Summary table** with all 10 stocks:

| # | Ticker | CMP (verified) | Down from High | Trigger | Target | SL | R:R | Confidence |
|---|---|---|---|---|---|---|---|---|
| 1 | XXXX | ₹XXX | ▼ X% | ₹XXX | ₹XXX | ₹XXX | X.X | HIGH |
... (all 10 rows)

**Then: Compact card per stock** (shorter than full cards — drop "Why it dipped", condense fundamentals to 2 lines):

```
[RANK]. [NAME] · [TICKER] · Confidence: X/4 = [LABEL]
CMP: ₹XXX (source, date) | 52W: ₹XXX–₹XXX | Down X% | Earnings: [DATE]
Fundamentals: PE X | Margins X% | Pledging X% | Revenue [trend]
RS vs Nifty: [tag] | Retail sentiment: [tag]
Technical: Support ₹XXX | RSI ~XX | [above/below] 200 DMA
GTT: Trigger ₹XXX → Target ₹XXX (+X%) → SL ₹XXX | R:R X.Xx
Risks: [Risk 1] · [Risk 2]
```

---

## Step 9 — Dark mode rendering rules (HTML widget output)

When rendering the report as an HTML widget (via the visualize tool), **never hardcode hex colors for any text, background, or border inside the GTT box or any card section**. Hardcoded colors break in dark mode — text becomes invisible because it matches the dark background.

### Mandatory CSS variable rules

**Always use these CSS variables — never hardcode hex values like `#185FA5`, `#FAEEDA`, `#1D9E75`, etc.:**

| Element | Correct CSS variable |
|---|---|
| Text (primary) | `var(--color-text-primary)` |
| Text (muted/labels) | `var(--color-text-secondary)` |
| Text (info/blue) | `var(--color-text-info)` |
| Text (success/green) | `var(--color-text-success)` |
| Text (warning/amber) | `var(--color-text-warning)` |
| Text (danger/red) | `var(--color-text-danger)` |
| Background (info) | `var(--color-background-info)` |
| Background (success) | `var(--color-background-success)` |
| Background (warning) | `var(--color-background-warning)` |
| Background (danger) | `var(--color-background-danger)` |
| Background (card) | `var(--color-background-primary)` |
| Background (row/pill) | `var(--color-background-secondary)` |
| Border (default) | `var(--color-border-tertiary)` |
| Border (info) | `var(--color-border-info)` |
| Border (warning) | `var(--color-border-warning)` |

### GTT box pattern (copy this exactly)

```html
<!-- Blue GTT box (standard) -->
<div style="border-radius: var(--border-radius-md); padding: 10px 14px; margin-top: 10px; border: 0.5px solid var(--color-border-info); background: var(--color-background-info);">
  <div style="font-size: 11px; font-weight: 500; text-transform: uppercase; color: var(--color-text-info); margin: 0 0 8px;">GTT Setup — 6-month horizon</div>
  <div style="display: flex; flex-wrap: wrap; gap: 8px 20px; font-size: 13px;">
    <div style="display: flex; flex-direction: column; gap: 2px;">
      <span style="font-size: 11px; color: var(--color-text-secondary);">Trigger</span>
      <span style="font-weight: 500; color: var(--color-text-primary); font-size: 14px;">₹X,XXX</span>
    </div>
    <div style="display: flex; flex-direction: column; gap: 2px;">
      <span style="font-size: 11px; color: var(--color-text-secondary);">Target</span>
      <span style="font-weight: 500; color: var(--color-text-primary); font-size: 14px;">₹X,XXX (+X%)</span>
    </div>
    <div style="display: flex; flex-direction: column; gap: 2px;">
      <span style="font-size: 11px; color: var(--color-text-secondary);">Stop Loss</span>
      <span style="font-weight: 500; color: var(--color-text-primary); font-size: 14px;">₹X,XXX (-X%)</span>
    </div>
    <div style="display: flex; flex-direction: column; gap: 2px;">
      <span style="font-size: 11px; color: var(--color-text-secondary);">R:R</span>
      <span style="font-weight: 500; background: var(--color-background-success); color: var(--color-text-success); padding: 2px 8px; border-radius: var(--border-radius-md); font-size: 12px;">X.Xx ✓</span>
    </div>
  </div>
  <div style="font-size: 11px; color: var(--color-text-secondary); margin-top: 8px;">GTT orders on Zerodha Kite / Upstox / Angel One have 1-year validity — no need to reset daily.</div>
</div>

<!-- Warning GTT box (governance/risk overhang) — swap info → warning -->
<div style="border: 0.5px solid var(--color-border-warning); background: var(--color-background-warning);">
  <div style="color: var(--color-text-warning);">GTT Setup — ⚠️ Risk overhang</div>
  <!-- Same inner structure, R:R badge uses rr-ok class -->
</div>
```

### Key rule summary
- GTT trigger, target, stop loss values → always `color: var(--color-text-primary)` — **never a hardcoded color**
- GTT box section title → `color: var(--color-text-info)` (blue box) or `color: var(--color-text-warning)` (warning box)
- Labels above values (Trigger, Target, Stop Loss) → `color: var(--color-text-secondary)`
- R:R badge (good) → `background: var(--color-background-success); color: var(--color-text-success)`
- R:R badge (weak) → `background: var(--color-background-warning); color: var(--color-text-warning)`
- Catalyst tags → `background: var(--color-background-success); color: var(--color-text-success)`
- Risk text → `color: var(--color-text-danger)`

---

## Hard rules — never break any of these

1. **No unverified prices.** Every CMP must come from a named source with a date. Estimated or recalled prices are forbidden.
2. **No hallucinated analyst targets.** Only state targets found in search results, attributed to a specific brokerage by name.
3. **Promoter pledging must be checked and shown** on every card. If >50%, add 🚨 prominently.
4. **No GTT format for Y or L horizons.** Only entry zones and price targets for 1-year and 2-year holds.
5. **Always ask horizon** if not stated. Do not assume or default silently.
6. **Nifty 100 only.** Do not go outside this universe unless the user explicitly requests it.
7. **Minimum 8% upside from trigger.** Any pick that can't credibly reach 8% above trigger gets dropped.
8. **Minimum confidence 2/4.** Discard any stock scoring 1/4 or 0/4.
9. **No more than N stocks in the output.** Never pad with weak picks just to hit the count.

---

## Standard disclaimer

> ⚠️ This report is for informational and educational purposes only and does not constitute financial advice. All investments in securities markets are subject to market risk. Stock prices are volatile and past performance does not guarantee future returns. Nifty 100 stocks mentioned are for research purposes only — not a solicitation to buy or sell. GTT orders do not guarantee execution at exact prices. Please consult a SEBI-registered investment adviser before making any investment decisions.

---

## Quick reference

| Setting | Value |
|---|---|
| Universe | Nifty 100 (large + mid-cap) |
| Minimum decline to qualify | 10% from recent high |
| Minimum upside target | 8% from trigger |
| Horizon options | 3M (Q) · 6M (H) · 1Y (Y) · 2Y (L) |
| GTT format | Q and H only |
| Entry zone format | Y and L only |
| Confidence model | 4 dimensions, 1 pt each, min 2/4 to include |
| Price verification | Mandatory — named source + date required |
| Promoter pledging | Always check — flag >30%, warn >50% |
| Output for top 3/5 | Full individual cards |
| Output for top 10 | Summary table + compact cards |
