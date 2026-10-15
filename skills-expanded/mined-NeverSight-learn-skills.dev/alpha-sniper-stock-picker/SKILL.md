---
name: alpha-sniper-stock-picker
description: This skill should be used when the user asks to "选股", "帮我选股", "pick stocks", "what to buy tomorrow", "AlphaSniper", "A股推荐", "今天买什么股票", "screen stocks", "sector hotspots", "明天买什么", or "板块热点". Implements the AlphaSniper 6-phase quantitative funnel for A-share T+1 next-day stock selection.
disable-model-invocation: true
allowed-tools: WebSearch, WebFetch, Read
context: fork
---

# AlphaSniper A-Share Stock Picker

A professional A-share (China) stock selection skill implementing the AlphaSniper 6-phase funnel methodology. Designed for T+1 trading — emphasis on next-day entry advantage, not same-day chasing.

**Core philosophy:** Rather miss than chase wrong. Select "about to launch" stocks, not "already launched" ones.

## Scope and Limitations

- **Covers:** A-share (Shanghai + Shenzhen) main board, ChiNext, STAR Market stocks for T+1 next-day trading
- **Does NOT cover:** Hong Kong H-shares, US-listed Chinese ADRs, B-shares, intraday T+0 strategies, futures, options, or ETF selection
- **Market hours:** Optimized for after-hours analysis (post 15:00 CST). During trading hours, data is real-time but recommendations are still for next-day entry

## Anti-Fabrication Rules (MANDATORY)

All data (stock codes, names, prices, volumes, sector rankings, financials, technicals) MUST originate from WebSearch/WebFetch results executed during this session. Zero exceptions.

1. **No fabrication.** Never invent stock names, codes, prices, or metrics. Never use "placeholder" or "representative" data. Never substitute training data for live search results.
2. **Fail transparently.** If a search fails: report it, try backup queries (see `references/data-sources.md`), and if all fail, halt with "Unable to complete analysis — real-time data unavailable."
3. **Cite sources.** For each phase, note the search query that produced the data (e.g., "Source: WebSearch '东方财富 概念板块排行 今日涨幅排名'").
4. **Final verification.** Before Phase 6 output, confirm all stock codes and names trace to a web search result from this session. If not, remove the stock.

**A recommendation based on fake data is worse than no recommendation.**

## Prerequisites

Execution requires WebSearch and WebFetch tools to gather real-time data from financial websites. Do NOT proceed without executing actual web searches. Primary data sources:

| Data Type | Recommended Sources | Search Keywords |
|-----------|-------------------|-----------------|
| Market overview | East Money (eastmoney.com), Sina Finance | `A股大盘行情 涨跌家数 今日` |
| Sector rankings | East Money sector page | `东方财富 板块排行 概念板块 今日涨幅` |
| Sector fund flow | East Money fund flow | `东方财富 板块资金流向 主力净流入` |
| Individual stock quotes | East Money, Sina, Xueqiu | `{stock_code} 实时行情 东方财富` |
| Stock financials | East Money F10 | `{stock_code} 财务指标 ROE 负债率` |
| Stock technical data | East Money K-line, indicators | `{stock_code} 技术指标 MACD RSI KDJ` |
| Fund flow (stock-level) | East Money individual fund flow | `{stock_code} 资金流向 主力净流入` |

Read `references/data-sources.md` for detailed search query templates, backup sources, data quality rules, and trading hours awareness.

## Graceful Degradation

When data collection is incomplete, degrade gracefully rather than halting entirely:

| Data Gap | Degradation Strategy |
|----------|---------------------|
| Market overview unavailable | Skip Phase 1; add "⚠️ Market health unverified" warning to output |
| Sector rankings partial | Proceed with available sectors; note "Only N sectors analyzed" |
| Individual stock financials missing | Exclude stock from fundamental scoring; redistribute weights per scoring-model.md |
| Fund flow data unavailable | Use volume analysis as proxy; reduce Momentum confidence by -10 |
| All WebSearch fails | Halt with clear message; suggest user retry or provide data manually |

**Rule:** Degradation must be explicitly reported in Phase 6 output. Never silently fill gaps.

## Execution Pipeline

Execute the 6 phases sequentially. If any phase fails, report clearly and stop. Do NOT skip phases.

Read `references/execution-phases.md` for the complete phase-by-phase execution guide with data collection steps, scoring rules, and verification checkpoints.

### Phase Summary

| Phase | Purpose | Key Output |
|-------|---------|------------|
| 1. Market Health Gate | Assess market-wide panic signals | GO/NO-GO decision |
| 2. Sector Hotspot Screening | Identify top 8 institutional-flow sectors | Ranked sector list with scores |
| 3. Candidate Pool Construction | Extract ~50-60 stocks from hot sectors | Candidate list with basic data |
| 4. Quantitative Scoring | Hard filters + 4-dimensional scoring | Top 10 ranked candidates |
| 5. AI Adversarial Verification | Risk manager challenge on each candidate | APPROVE/RISKY/REJECT verdicts |
| 6. Final Output | Present ≤3 recommendations | Formatted stock cards with disclaimer |

Detailed scoring formulas → `references/scoring-model.md`
Hard filter rules → `references/hard-filters.md`
AI verification framework → `references/ai-verification.md`
Data collection strategy → `references/data-sources.md`
Outcome tracking framework → `references/outcome-tracking.md`
Sample output → `examples/sample-output.md`
Output verification → `scripts/verify-output.sh`

### Phase 6: Final Output

Present ≤3 final recommendations using the format in `templates/output-template.md`. Run the final verification checklist from that template before outputting. If no stocks pass all 6 phases: "No stocks meet all criteria today. Better to stay in cash than chase marginal opportunities."

## User Customization

Override defaults when the user specifies preferences:

| User Says | Override |
|-----------|---------|
| "我偏好成长股" / "growth stocks" | Relax PE upper bound to 60; increase Profit Growth weight to 35% |
| "只看大盘股" / "large-cap only" | Add filter: market cap >= 100亿 |
| "激进一点" / "more aggressive" | Relax today's gain cap to 9%; reduce chase penalty by 50% |
| "保守一些" / "more conservative" | Tighten today's gain cap to 5%; increase Risk weight to 30% |
| "排除某行业" / "exclude [sector]" | Add sector to exclusion list in Phase 2 |
| "我有3万块" / position size hint | Adjust turnover filter proportionally (smaller capital = lower turnover OK) |

Confirm overrides with the user before executing.

## Key Principles

- **T+1 Mindset**: Recommendations are for TOMORROW's open. Penalize same-day gains aggressively.
- **Capital Flow > Price**: Institutional fund flow is the strongest single factor. Price rising without fund support is dangerous.
- **Conservative Bias**: When uncertain, reject. Missing is cheaper than chasing wrong.
- **Track and Learn**: After each session, if the user reports outcomes (e.g., "yesterday's pick went up/down"), record in conversation memory: stock code, recommendation date, outcome direction, and which phase's signal was most/least accurate. This informs future calibration.
