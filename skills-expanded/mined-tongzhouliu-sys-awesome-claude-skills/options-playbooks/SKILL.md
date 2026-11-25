---
name: options-playbooks
description: >
  Collection of 11 institutional-grade options strategy operation handbooks covering Wheel Sell Put,
  Covered Call, volatility arbitrage, event-driven strategies. Organized by ticker: comprehensive handbooks (wheel/open),
  index strategies (SPX/QQQ), tech blue-chips (AAPL/NVDA/TSLA), crypto-related (COIN/CRCL/IBIT),
  and custom client solutions (KAISHANG/MR GENG).
  Trigger this skill for: options operation handbooks, strategy manuals, client delivery documents,
  volatility strategy operations, NRA options compliance, specific operating procedures for AAPL/NVDA/TSLA/COIN/CRCL/IBIT,
  Wheel execution handbook, covered call opening handbook, three-tier circuit breaker, monthly SOP,
  performance tracking ledger, options strategy architecture (three-tier/five-tier return structure),
  EV threshold, Delta matrix operational details, market state engine operation, earnings season procedures,
  psychological discipline rules, capital allocation laws, VIX position matrix operation,
  KAISHANG strategy, MR GENG strategy, options arbitrage automation, or when creating new ticker handbooks,
  modifying existing ones, comparing strategy differences across tickers, extracting specific parameters or rules.
  Note: This skill focuses on "operational execution layer" of complete handbooks, complementing openclaw-options skill
  (which focuses on system parameters and signal engine). If user asks about opening parameters, signal format,
  Pre-screen Gate logic, prioritize openclaw-options; if asking about complete operations for specific ticker,
  client manual content, or need to generate new handbook, use this skill.
---

# Options Playbooks - Professional Trading Handbooks

## Overview

This skill provides institutional-grade strategy execution handbooks for disciplined options trading across multiple strategies and underlying assets. Each handbook includes:

- **Full operations procedures** - step-by-step execution from signal to closing
- **Risk management frameworks** - position sizing, allocation rules, margin requirements
- **Tax compliance guidance** - NRA-specific rules, withholding handling, reporting requirements
- **Performance monitoring** - key metrics, P&L tracking, rebalancing triggers

## Handbook Library Structure

### Comprehensive Strategies

- `wheel-handbook-v2.5.md` - Complete Wheel strategy system for Sell Put + Covered Call
- `covered-call-handbook.md` - Covered call operations with blue-chip focus
- `vol-arbitrage-handbook.md` - Volatility spread strategies (Calendar/Diagonal/Short Vol)
- `event-driven-handbook.md` - Earnings season and catalyst-driven positions

### Ticker-Specific Playbooks

- **Tech Blue-Chips**: AAPL, NVDA, MSFT operations (quality tier)
- **Crypto-Proxies**: COIN, MSTR, CRCL, IBIT operations (high volatility tier)
- **Diversified**: SPY, QQQ, IWM, various sector ETFs

### Custom Client Solutions

- `kaishang-strategy.md` - Three-tier capital-scaled architecture
- `mr-geng-strategy.md` - Hedge fund-style tactical allocation

## How to Use This Skill

### For New Handbook Creation

When asked to create an operations handbook for a new ticker, provide:

1. **Markets & Risk Section**
   - Market state conditions (bull/bear/neutral)
   - Volatility regime (IV percentile ranges)
   - Position tier (A/B/C/D) and capital scaling

2. **Opening Procedures**
   - Signal generation (specific Greeks targets, IV conditions)
   - Strike selection framework
   - DTE window (preferred 30-45 days)
   - Position sizing rules

3. **Management & Monitoring**
   - Profit-taking levels (target ROI %)
   - Stop-loss rules (max loss as % of capital)
   - Adjustment triggers (e.g., delta drift > 0.15)
   - Close-out timeline (e.g., close 7 days before expiration)

4. **Closing & Rebalancing**
   - Exit criteria (hit target, hit stop, DTE threshold)
   - Assignment handling (if applicable)
   - Rebalance frequency and method

5. **Tax Compliance**
   - Wash sale considerations
   - Withholding implications (NRA specific)
   - Section 1256 vs 1441 treatment
   - Reporting requirements (Form 1099-B, Schedule D)

### For Strategy Comparison

Extract operational differences across:
- Capital requirements
- Greeks targets (delta, gamma, vega)
- Risk/reward ratios
- Preferred market environments
- Tax efficiency

### For Client Delivery

Use structured handbooks to:
- Communicate strategy rationale
- Define entry/exit rules objectively
- Set performance expectations
- Establish compliance guardrails

## Key Operational Concepts

**Market State Alignment**: All operations adjust for current market regime (VIX level, IV rank, trend direction)

**Three-Factor Capital Scaling** (from OpenClaw system):
- Tier A (A+/A blue-chips): Max 8-10% of NLV per position
- Tier B (quality growth): Max 6-8% per position
- Tier C (high vol): Max 5-6% per position, concentrated positions
- Tier D (speculative): Spread-only, max 2-3% per position

**Monthly Operations Discipline**:
- Monthly review and rebalancing
- Concentration monitoring (single name < 10%, sector < 30%)
- Cash reserve management
- Tax-loss harvesting opportunities

## Tax Framework Reference

All NRA-specific rules documented in `references/01-tax-framework.md`:
- Dividend withholding (30% on US equities, ETF variations)
- Capital gains treatment (generally tax-exempt for NRA)
- Option premium taxation (usually not withheld)
- Assignment consequences (if assigned, stock holding triggers different rules)
- Form 1042-S and backup withholding recovery

## Performance Monitoring

Track per handbook:
- **Return metrics**: Annualized ROI, Sharpe ratio, max drawdown
- **Operational metrics**: Win rate, average P&L per trade, average holding period
- **Risk metrics**: Daily VAR, position concentration, margin utilization
- **Compliance metrics**: Tax-efficient closes, wash sale violations, withholding accuracy

---

**Disclaimer**: These handbooks are for educational and planning purposes. Options trading carries substantial risk and may result in total loss of capital. Not investment advice.
