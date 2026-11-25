---
name: openclaw-mimi-alpaca-trading-skill
description: Execute trades, analyze markets, and manage portfolios using apcacli command-line tool for Alpaca's Trading API. Use this skill when the user wants to trade stocks, ETFs, options, crypto, check market data, view positions, manage orders, or analyze their portfolio. Also use when they mention "buy," "sell," "trade," "market data," "stock price," "portfolio," "account balance," or "alpaca trading." When the user requests a trade, present 3 good options with reasoning behind each and execute their chosen option after confirmation.
---

# Alpaca Trading Skill — Mimi's Autonomous Agent

Execute trades and manage portfolios through `apcacli` for Alpaca's Paper Trading API.

## Credentials

```bash
export APCA_API_KEY_ID="PKLBTOOFHMVLVOU2X7WHKNPH55"
export APCA_API_SECRET_KEY="AiJZpe2HdnzSKY2dc8Hx1P2wYK5Y7dyi6kjBeVYRbSAP"
```

Always prefix apcacli commands with these env vars inline, e.g.:
```bash
APCA_API_KEY_ID="PKLBTOOFHMVLVOU2X7WHKNPH55" APCA_API_SECRET_KEY="AiJZpe2HdnzSKY2dc8Hx1P2wYK5Y7dyi6kjBeVYRbSAP" apcacli account get
```

---

## Autonomous Trading Strategy

**Goal:** Maximize portfolio value over 30 days (paper trading — high risk tolerance encouraged).
**Style:** Dollar-cost averaging + momentum/technical analysis hybrid.
**Risk tolerance:** HIGH. Be aggressive. This is not real money.

### Each Autonomous Run — Decision Flow

1. **Check market status** — `apcacli market` — if closed, stop immediately.
2. **Check account** — `apcacli account get` — note buying power and equity.
3. **Check positions** — `apcacli position list` — see what's held.
4. **Scan for opportunities** — use `web_search` to find:
   - Trending/momentum stocks today
   - Earnings beats or upcoming catalysts
   - Sector momentum (AI, energy, defense, consumer)
5. **Decide and act** — based on the framework below.

### Trading Framework

**Dollar-Cost Averaging (DCA):**
- For core holdings (SPY, QQQ, NVDA), add to positions on dips. Deploy 5–10% of available buying power per run.
- Don't wait for the "perfect" entry — regular buying builds position over time.

**Momentum / Technical Signals:**
- Look for stocks up >2% today with volume — momentum plays.
- Look for recent earnings beats — stocks often run for 1–3 days post-beat.
- Avoid stocks already up >10% today (chasing is risky even at high risk tolerance).

**Position Sizing:**
- No single position > 25% of total equity (guardrail).
- Prefer spreading across 3–6 positions rather than concentrating.
- Reserve at least 10% of equity as cash buffer.

**Selling Rules:**
- Take profit if any position is up >15% — sell half.
- Cut losses if any position is down >12% — close it.
- On each run, check existing positions against these thresholds before buying anything new.

**Preferred Tickers (rotate through):**
- Core anchor (~50% of portfolio): SPY, QQQ, NVDA, META, MSFT, AAPL
- Small/Mid cap opportunistic (~40% of portfolio): Actively hunt these each run via web_search. Look for:
  - Small caps with recent catalysts (earnings beat, FDA approval, contract win, analyst upgrade)
  - Sector momentum plays: biotech, defense, AI infrastructure, clean energy, semiconductors
  - Companies showing unusual volume or price action today
  - Undervalued names with near-term news expected
- Avoid: True penny stocks under $2, crypto (unreliable fills), volume under 500k/day

### Example Run Script

```bash
# 1. Check market
APCA_API_KEY_ID="..." APCA_API_SECRET_KEY="..." apcacli market

# 2. Account state
APCA_API_KEY_ID="..." APCA_API_SECRET_KEY="..." apcacli account get

# 3. Positions
APCA_API_KEY_ID="..." APCA_API_SECRET_KEY="..." apcacli position list

# 4. After analysis, place a trade
APCA_API_KEY_ID="..." APCA_API_SECRET_KEY="..." apcacli order submit buy NVDA --value 2000

# 5. Confirm
APCA_API_KEY_ID="..." APCA_API_SECRET_KEY="..." apcacli order list
```

### Reporting

After each autonomous run, send a brief summary to the user via Telegram:
- What you bought/sold and why
- Current portfolio value
- Any positions that hit profit/loss thresholds

---

## Manual Trade Commands

**Buy:**
```bash
apcacli order submit buy SYMBOL --value AMOUNT
apcacli order submit buy SYMBOL --quantity N
```

**Sell:**
```bash
apcacli order submit sell SYMBOL --quantity N
apcacli position close SYMBOL
```

**Check:**
```bash
apcacli position list
apcacli account get
apcacli order list
```
