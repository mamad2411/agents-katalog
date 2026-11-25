---
name: mirofish-prediction
description: >
  Qualitative scenario prediction via MiroFish swarm simulation. Builds simulated
  digital worlds from seed data (news, market signals, policy changes), runs thousands
  of agents with behavioral logic, and produces narrative prediction reports. Use as
  complement to TimesFM quantitative forecasts for trading and strategy decisions.
license: AGPL-3.0
metadata:
  author: <your-name>
  version: "1.0.0"
  depends_on:
    - aster-trading
    - timesfm-forecasting
  external_service: true
tags: [prediction, simulation, trading, strategy, research]
created: 2026-04-04
---

# MiroFish Scenario Prediction

## Overview

MiroFish is a swarm intelligence engine that builds simulated digital worlds from
real-world seed data. Thousands of agents with distinct personalities, memory, and
behavioral logic interact to produce qualitative scenario predictions.

**Complementary to TimesFM**: TimesFM gives quantitative price curves with confidence
intervals. MiroFish gives qualitative scenario narratives — what happens *if* a specific
event occurs and how it cascades through markets and public opinion.

## When to Use

- "What happens if the Fed raises rates?" — scenario simulation
- "Impact of a whale dumping 10K BTC?" — cascading effect analysis
- Public opinion modeling for token launches or policy changes
- Complementing TimesFM forecasts with narrative context
- Any council question in the trading or strategy domain
- Strategic decisions that need "what if" scenario exploration

## How to Start MiroFish

```bash
# Backend (Python 3.10, port 5001)
source ~/Projects/MiroFish/backend/.venv/bin/activate
cd ~/Projects/MiroFish && python backend/app/main.py

# Frontend (port 3002 — avoid conflict with Agent Orchestrator on 3000)
PORT=3002 npm --prefix ~/Projects/MiroFish/frontend start
```

**Prerequisites**: Real API keys in `~/Projects/MiroFish/.env`:
- `LLM_API_KEY` — OpenRouter or Claude API key
- `ZEP_API_KEY` — Zep Cloud key for agent memory

## Integration with Council

When `/council` is invoked for trading or strategy domains:

1. **Phase 0**: If MiroFish is running, seed a scenario simulation with the council question
2. Feed the simulation results as additional intelligence to the advisors
3. The **Contrarian** advisor should specifically challenge MiroFish's assumptions
4. The **Executor** should reference both TimesFM numbers and MiroFish scenarios

## Integration with /plan

When `/plan` routes a trading or strategy task:

1. Use MiroFish for "what-if" analysis before committing to a trading strategy
2. Compare MiroFish qualitative predictions against TimesFM quantitative forecasts
3. If predictions diverge significantly, escalate to council decision

## Cost Warning

Each simulation runs thousands of LLM-powered agents. A single scenario can consume
significant API tokens. Use judiciously — prefer TimesFM for routine forecasting,
reserve MiroFish for high-stakes scenario analysis.

## Combo: Full Prediction Stack

```
Aster MCP (live market data)
    → TimesFM (quantitative: price curves + confidence intervals)
    → MiroFish (qualitative: scenario narratives + cascading effects)
    → Council (multi-advisor synthesis of both)
    → autoresearch (measure prediction accuracy over time)
```
