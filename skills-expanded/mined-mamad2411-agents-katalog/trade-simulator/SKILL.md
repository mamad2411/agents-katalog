---
name: "@1247/trade-simulator"
version: 1.0.0
description: "Multi-agent scenario analysis for traders using MiroFish swarm intelligence architecture. LLM-powered market participant simulation with behavioral reasoning, cascade analysis, and post-sim interviews."
author: starchild
tags: [trading, simulation, mirofish, scenario-analysis, risk, multi-agent, stress-test]
---

# 🐟 Trade Simulator (MiroFish Architecture)

> Multi-agent scenario analysis for traders. Not a spreadsheet — a behavioral simulation.
> Built on MiroFish's swarm intelligence architecture, adapted from social simulation to market simulation.

## MiroFish Integration

This skill implements MiroFish's 5-stage prediction pipeline, replacing social media environments with financial markets:

| MiroFish Stage | Original (Social) | Our Adaptation (Markets) |
|---|---|---|
| 1. Graph Construction | Zep knowledge graph from news/docs | Market State Graph from live Coinglass/HL data |
| 2. Environment Setup | Twitter/Reddit agent profiles | Market participant profiles (Whale, MM, Retail, etc.) |
| 3. Simulation | OASIS dual-platform social interaction | Round-based market interaction with LLM reasoning |
| 4. Report Generation | ReACT report with Zep tools | ReACT report with market data tools |
| 5. Deep Interaction | Interview any social agent | Interview any market participant |

### Key MiroFish Patterns Used

1. **LLM-driven agent reasoning** (from `oasis_profile_generator.py`) — agents don't use if/else rules. Each agent has a persona prompt and "thinks" each round via LLM call
2. **Simulation config auto-generation** (from `simulation_config_generator.py`) — describe scenario in natural language, LLM generates agent roster, parameters, event timeline, activity patterns
3. **ReACT report generation** (from `report_agent.py`) — multi-step reasoning with tool use: plan outline → generate sections → cite evidence → synthesize predictions
4. **Post-simulation interviews** (from `zep_tools.py` Interview system) — chat with any agent after simulation to understand their reasoning
5. **Knowledge graph backbone** — entities, relationships, and facts structured for agent retrieval (we use in-memory graph instead of Zep Cloud)

### What We Don't Use

- ❌ OASIS / camel-ai (social media simulation runtime — irrelevant to markets)
- ❌ Zep Cloud (replaced with local in-memory knowledge graph)
- ❌ Flask frontend (we output to agent conversation)
- ❌ Twitter/Reddit environments (replaced with market environment)

## Architecture

```
skills/trade-simulator/
├── SKILL.md                          # This file
└── scripts/
    ├── mirofish_engine.py            # Core engine — 5-stage pipeline
    ├── market_graph.py               # Stage 1: Market state graph builder
    ├── profile_generator.py          # Stage 2: LLM agent profile generation
    ├── simulation_runner.py          # Stage 3: Round-based market simulation
    ├── report_agent.py               # Stage 4: ReACT report generation
    └── interview.py                  # Stage 5: Post-sim agent interviews
```

## Usage

### Quick Scenario Analysis
```
Agent: "Run a trade simulation: What happens to my BTC short if ETF inflows spike 500%?"
```

The engine will:
1. Build market state graph from live data (OI, funding, liquidations, whale positions)
2. Auto-generate 5-8 market participant agents calibrated to current conditions
3. Run 6-round simulation where each agent LLM-reasons about their actions
4. Generate ReACT analysis report with turning points, cascade analysis, recommendations
5. Offer interactive interviews with any simulated agent

### Supported Scenarios
- **Directional shocks**: "What if BTC pumps/dumps 10-20%?"
- **Catalyst events**: "What if ETF inflows spike?" / "What if Tether depegs?"
- **Market structure**: "What if funding goes extreme?" / "What if OI doubles?"
- **Portfolio stress**: "How does my portfolio react to a black swan?"

### Interview Mode
After any simulation:
```
Agent: "Interview the whale agent — why did they cover at round 4?"
Agent: "Ask the market maker about their liquidity decision"
```

## Data Sources (Live)

| Data | Tool | What It Feeds |
|---|---|---|
| Open Interest | `cg_open_interest()` | Market leverage state |
| Funding Rates | `funding_rate()` | Positioning sentiment |
| Liquidation Levels | `cg_liquidations()` | Cascade trigger points |
| Whale Positions | `cg_hyperliquid_whale_positions()` | Whale agent calibration |
| Long/Short Ratios | `long_short_ratio()` | Crowd positioning |
| Orderbook Depth | `hl_orderbook()` | MM agent calibration |
| ETF Flows | `cg_btc_etf_flows()` | Institutional flow context |
| Price/OHLC | `cg_ohlc_history()` | Price context |
| Social Sentiment | `lunar_coin()` | Retail agent behavior |

## Workflow

1. **Collect live market data** using tools above
2. **Run simulation**: `python3 skills/trade-simulator/scripts/mirofish_engine.py`
   - Pass market data + scenario + user positions as JSON
   - Engine runs all 5 MiroFish stages
   - Returns structured results (agent actions, report, interview-ready state)
3. **Present results** with key insights, PnL impact, risk warnings
4. **Offer interviews** — user can interrogate any agent
