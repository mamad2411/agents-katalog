---
name: ibkr-chokepoint-equity-scan
description: Screen demand-wave chokepoint equities through IBKR API. Use for global non-mainland-A-share industrial-chain leaders, early/smaller bottleneck suppliers, qualification-cycle moats, forward TAM, buy logic, and prompts such as 卡脖子, 龙头, 需求浪反推, 第一行只给龙头, 不能被设计掉, or material revenue.
version: 1.0.0
author: Hermes Agent + Thrill3r
license: MIT
metadata:
  hermes:
    tags: [finance, stocks, ibkr, semiconductors, aerospace, chokepoint]
    category: finance
---

# IBKR Chokepoint Equity Scan Skill

Use this when the user asks for aerospace, semiconductor, defense, AI infrastructure, or other industrial-chain equities and explicitly wants IBKR API price/contract evidence. It produces research candidates, not orders, and must not place trades.

## When to Use

Use when the request includes one or more of:
- IBKR / TWS / Gateway / port 4002 / Interactive Brokers.
- 航天产业链, 半导体产业链, 上下游个股, 卡脖子, chokepoint.
- 买点, 止损, 止盈, 长拿理由.
- Qualification cycle, TAM, monopoly, functional exclusivity, value-chain climb.
- 需求浪反推, 架构性卡脖子, 龙头和买入逻辑, 越早市值越小越好, 不能被设计掉, material revenue.
- 第一行只给龙头, 全球股, 全球产业链, 排除大陆A股, 非A股龙头.

Do not use for live order execution. If the user asks to place orders, switch to an order-entry workflow and require explicit side/size/account confirmation.

## Prerequisites

- IBKR TWS or IB Gateway running locally.
- Default API port: `127.0.0.1:4002`.
- API read access enabled in TWS/Gateway.
- `terminal` tool available.
- No Python package dependency required; use the raw IBKR socket helper if `ibapi` / `ib_insync` is absent.

## How to Run

First prove IBKR is reachable:

```bash
python3 - <<'PY'
import socket
s=socket.socket(); s.settimeout(2)
s.connect(('127.0.0.1',4002))
print('IBKR_PORT_OK 127.0.0.1:4002')
s.close()
PY
```

Then run the helper from this skill directory:

```bash
python3 ~/.hermes/skills/finance/ibkr-chokepoint-equity-scan/scripts/ibkr_chokepoint_scan.py ASTS RKLB RDW AEHR ACMR ICHR SKYT CAMT FORM VECO
```

The helper uses:
- handshake with TWS API server.
- `reqMatchingSymbols` opcode `81` for contract discovery.
- `reqMarketDataType` opcode `59`, type `3` for delayed data fallback.
- `reqMktData` opcode `1`, version `11` for quotes.

## Quick Reference

Use Feishu-safe output. Avoid wide Markdown tables for the main answer because they often render like broken text in chat.

Required fields per candidate:
- rank and ticker
- IBKR price, conId, exchange, delayed/live flag
- demand wave and architecture bottleneck
- chain position
- chokepoint reason
- why it cannot be designed away
- material revenue path and qualification-cycle evidence
- supply elasticity, market recognition, catalyst, and main risks
- buy zone
- stop
- take-profit or long-hold thesis
- thesis-break condition

First-line output contract:
- The first line of the answer must contain only the leader ticker/name list, with no explanation.
- For global-stock or global industrial-chain requests, the default leader list excludes mainland China A-shares. Include A-shares only when the user explicitly asks for A股/大陆A股/A-share coverage.
- After that first line, explain the ranking, evidence, buy logic, and rejects.

## Chokepoint Research Mandate

When the user asks for industrial-chain leaders, AI-era suppliers, 龙头, 买入逻辑, or 卡脖子, use this ranking model:

```text
excess return =
  demand shock
  × insufficient supply elasticity
  × low market recognition
  × catalyst
  - valuation / liquidity / dilution / geopolitical risk
```

Start from the demand wave and reverse-map the system architecture before naming stocks. Prefer bottlenecks that sit earlier in the value chain, are smaller in market cap, and can climb from component/material supplier into higher-value qualified modules or systems.

Hard filter:
- The chokepoint must not be easily designed away by architecture, second-source qualification, software workaround, or customer vertical integration.
- The company must be able to convert the bottleneck into material revenue, not just small proof-of-concept revenue or narrative exposure.

Do not overweight current-quarter financials when the thesis is qualification-cycle driven. Instead, look for customer qualification, platform inclusion, tool/process qualification, flight heritage, fab/tool OEM approval, design wins, long-term capacity agreements, and timing from qualification to volume revenue.

## Output Format

Default to compact candidate cards, not Markdown tables:

```text
#1 SKYT | SkyWater
IBKR: 37.76 delayed | conId 482880559 | ISLAND
位置: 半导体上游 / trusted foundry / 特殊工艺
卡点: 国防+特殊工艺资格认证；替换成本高
买点: 34.7 / 32.1
止损: 29.5
止盈: 47.2 / 58.5
长拿: 若国防/先进封装订单持续兑现，可留核心仓
破局: 资格丢失、订单不转收入、持续稀释
```

If a dense overview is needed, use a monospace aligned code block:

```text
Ticker  Px      Buy1   Buy2   Stop   TP1    TP2    Grade
SKYT    37.76   34.7   32.1   29.5   47.2   58.5   A
AEHR    110.95  102.1  94.3   86.5   138.7  172.0  A
RDW     26.43   24.3   22.5   20.6   33.0   41.0   A-
```

Only use Markdown tables when the target channel is known to render them correctly.

## Procedure

1. Parse scope.
   - If market is unspecified, default to IBKR-accessible US/global listings outside mainland China A-shares.
   - If the user says global stocks or 全球股, exclude mainland China A-shares unless A-shares are explicitly requested.
   - If user names A/H/US, constrain candidates to that market.

2. Build candidate universe from demand waves, not from popularity lists.
   - First write the demand wave in one line, then list the architecture bottlenecks it creates.
   - Aerospace examples: LEO communications, satellite buses, launch, space components, ISR/geospatial data, rugged defense electronics.
   - Semiconductor examples: HBM/advanced packaging, probe cards, wafer-level burn-in, wet clean, metrology/inspection, laser anneal, MOCVD, test handlers.
   - AI infrastructure examples: liquid cooling CDUs, cold plates, quick disconnects, rack manifolds, power shelves, busbars, high-current connectors, FFKM/EPDM seals, high-purity elastomers, optics/interconnect test.

3. Apply the chokepoint filter.
   - Pass only if the function cannot be easily designed away.
   - Pass only if the company can turn the bottleneck into material revenue.
   - Prefer qualification-cycle moats: defense, foundry, tool qualification, aerospace flight heritage, customer requalification cost.
   - Prefer smaller/earlier companies only after the bottleneck passes.
   - Reject popular leaders if the bottleneck is already fully understood, commoditizing, or too small inside a conglomerate to move revenue.

4. Query IBKR.
   - Use `reqMatchingSymbols` to prove the ticker maps to a real IBKR contract.
   - Pick exact `STK` + requested currency/market.
   - Use delayed quotes if live market data is not subscribed.
   - Label delayed data explicitly when IBKR returns code `10167`.

5. Derive buy points mechanically unless user gives a chart model.
   - Starter pullback: current price * `0.92`.
   - Add zone: current price * `0.85`.
   - Invalidation stop: current price * `0.78`.
   - First take-profit: current price * `1.25`.
   - Second take-profit: current price * `1.55`.
   - For very volatile pre-profit names, widen stop only if position size shrinks.

6. Long-hold exception.
   - Only allow no-stop / long-hold framing when the thesis is qualification-cycle driven and the user accepts drawdown.
   - Name the break condition anyway: loss of qualification, design-out evidence, canceled platform, dilution spiral, or material revenue not appearing after stated cycle window.

7. Output compactly.
   - First line: only the leader ticker/name list.
   - Rank candidates.
   - Use candidate cards as the default user-facing shape.
   - Use one monospace aligned overview block only when comparing many tickers.
   - Avoid wide Markdown tables in Feishu/chat surfaces unless the user explicitly asks.
   - Include IBKR price/evidence block.
   - Include rejects/observations.
   - State no order was placed.

## Pitfalls

- Do not answer from memory when IBKR was required; at minimum prove port, contract, and price source.
- Do not treat market-data subscription errors as fatal if delayed data is available.
- Do not confuse a good product with a chokepoint; alternatives matter.
- Do not call something material revenue unless revenue path can plausibly scale with the bottleneck.
- Do not overfit to current financials when user asks for qualification cycle / forward TAM.
- Do not recommend no-stop long holds for binary execution names without naming thesis-break conditions.

## Verification

Before finalizing:
- IBKR port check passed or blocker stated.
- Each recommended ticker has IBKR contract evidence.
- Each price is labeled live or delayed.
- Each buy plan has entry + stop + take-profit, or a no-stop long-hold thesis and break conditions.
- Candidate output uses Feishu-safe cards or monospace aligned code blocks, not wide Markdown tables.
- Rejected candidates are separated from buy candidates.
- No trades/orders were placed.
