---
name: investorclaw
description: Deterministic-first portfolio analyzer — holdings, performance, Sharpe + Sortino, FRED yield curves, bond duration, sector breakdowns, scenario rebalancing. Free by default (Yahoo Finance), no API key required; optional Massive key for futures/premium data.
homepage: https://github.com/argonautsystems/InvestorClaw
user-invocable: true
metadata: {"license":"MIT-0","version":"4.10.0","upstream-runtime":"https://github.com/mnemos-os/mnemos-ic-runtime","upstream-engine":"https://github.com/argonautsystems/ic-engine"}
---

## Authoritative operating contract

These rules govern any agent using this skill. Examples elsewhere in this file
are reference only and never override them.

### Data integrity — InvestorClaw is the only source of truth
- Every price, percent, dollar figure, or market fact an agent states MUST come
  from an InvestorClaw tool result returned in the SAME turn. InvestorClaw
  returns HMAC-signed envelopes; that signed data is the only source of truth.
- Never invent, estimate, guess, or use the model's own training knowledge for
  any number. If a tool did not return it this turn, do not state it — say
  "InvestorClaw returned no data for that".
- Tool prose with no concrete numbers = no data; never convert it into a figure.

### Current tool surface (underscore namespace)
- `investorclaw__portfolio_market_snapshot(symbols?, benchmarks?)` — real-time
  prices + day-change% for holdings and benchmarks (SPX/NDX/DJI/VIX, BTC/ETH).
  `symbols` is a COMMA-SEPARATED STRING (e.g. "NVDA,AAPL"), not a list. No args =
  holdings + benchmarks. Use this (not portfolio_ask) for any "price of X" and to
  read the portfolio against the market.
- `investorclaw__portfolio_performance_window(period=...)` — return / P&L /
  movers over a window. period: 1d, 1w, 1mo, 1y, 5y, 10y, 20y, max, or natural
  phrases ("today", "last week", "last year", "entire history").
- `investorclaw__portfolio_ask(question=...)` — analysis / explanation.

Older `investorclaw.*` dot-namespace examples below are stale; the underscore
forms above are the current tool names.

## Autonomous / always-on monitoring agents

For unattended agents (scheduled monitors and alerters — e.g. a MarketWatch
agent), in addition to the contract above:
- Drive each run from a tool call first; never answer a market question from
  memory. A scheduled "poll" means call `portfolio_market_snapshot`.
- Threshold scan: call `portfolio_market_snapshot`, then emit ONE terse line
  only when a holding or benchmark breaches the configured move (e.g. ±3% a
  holding, ±10% VIX); otherwise emit a single `NO_ALERT` token and stop.
- If the required tool errors or returns no data, emit a fixed marker such as
  `OPS_FAIL market_snapshot unavailable` and stop — never fabricate a reassuring
  number to fill the gap.
- No clarifying questions in unattended mode; map intent and act.
- Periodic / EOD reports: pull `portfolio_performance_window` for the window,
  then `portfolio_market_snapshot` for index closes; report numbers verbatim.
- Always read holdings in the context of the benchmarks in the same snapshot.
- Delivery is push, terse, numbers-first. Educational, not personalized advice.


<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors
-->

# InvestorClaw

This repository is the **umbrella project** for InvestorClaw — README,
license, regression harness, and the public face. The agent-readable
SKILL.md that ClawHub publishes lives in the runtime repo:

- **Dockerized v4.x runtime + ClawHub-published SKILL.md**:
  [`mnemos-os/mnemos-ic-runtime`](https://github.com/mnemos-os/mnemos-ic-runtime)
- **Claude Code / Claude Desktop plugin** (container-first, this repo):
  `/plugin marketplace add argonautsystems/InvestorClaw` — same skill + container
  as every other runtime. See [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).
- **Engine source** (Python analyzers): [`argonautsystems/ic-engine`](https://github.com/argonautsystems/ic-engine)

## Install (v4.x dockerized runtime)

```bash
git clone https://github.com/mnemos-os/mnemos-ic-runtime.git ~/.investorclaw
cd ~/.investorclaw
mkdir -p portfolios
docker compose up -d
```

The compose pulls
\`ghcr.io/argonautsystems/ic-engine:4.7.7-cpu\` (publicly hosted, no
auth) and runs it on \`localhost:18090\` (MCP + REST) and
\`localhost:18092\` (dashboard).

For the full agent-readable spec (12-tool catalog, first-run timeline,
per-runtime config blocks, troubleshooting), see the published
[SKILL.md in the runtime repo](https://github.com/mnemos-os/mnemos-ic-runtime/blob/main/SKILL.md).

## Documentation

This umbrella repo carries the comprehensive doc set:

- [README.md](README.md) — features, quick start, model + API key
  recommendations
- [STONKMODE.md](STONKMODE.md) — narrated commentary mode
- [CAPABILITIES.md](CAPABILITIES.md) — full feature catalog
- [PRIVACY.md](PRIVACY.md) — data-handling policy
- [DISCLAIMER.md](DISCLAIMER.md) — educational-use disclaimer
- [SECURITY.md](SECURITY.md) — vulnerability disclosure
- [CHANGELOG.md](CHANGELOG.md) — release history
- [docs/](docs/) — EOD report, glossary, philosophy, install models,
  COBOL testing, MCP tools reference, Stonkmode architecture +
  avatar legend, Windows setup guide
- [docs/references/](docs/references/) — input / output / schema /
  consultative-LLM contracts

## License

- This umbrella repo: Apache 2.0 (substantive code) + MIT-0 (SKILL.md,
  agent-skills artifacts).
- Per-file SPDX-License-Identifier headers indicate the applicable
  license.

InvestorClaw is educational only. Not financial advice.
