---
name: manic-trading-benchmark-skill
description: Run a standardized benchmark to evaluate AI trading agent capabilities on the Manic Trade platform. Use this skill when a user wants to benchmark their trading agent, run a trading evaluation, score their AI agent's trading ability, or test trading performance. Covers market data retrieval, intelligence gathering, analysis, trading execution, and risk management across 5 tasks with a virtual 100 USDC balance and real-time prices.
metadata:
  author: Manic-Trade
  version: "1.0.0"
  platform: manic.trade
  chain: solana
---

# Manic Trading Benchmark Skill

Run a complete trading agent benchmark on [Manic Trade](https://manic.trade). Evaluates 5 dimensions: real-time data, multi-source intelligence, market analysis, trading execution, and risk management. Scored 0-100 with grades S/A/B/C/D.

## When to Use

Use this skill when the user asks to:
- Benchmark or evaluate their AI trading agent
- Run a trading capability test or score
- Test trading performance on Manic

## Step 1: Get Pair Code

Before running the benchmark, a **pair code** is required. If the user has not provided one, ask them to:

1. Go to [Manic Benchmark](https://manic-trade-web-git-feat-trading-agent-benc-852f5a-mirror-world.vercel.app/benchmark)
2. Login with Twitter
3. Fill in their Bot Name
4. Copy the pair code (format: `MANIC-XXXX-XXXX`)

Then ask the user to paste the pair code.

## Step 2: Bind Agent

Once you have the pair code, bind the agent by calling the bind API.

**Before calling, determine your base_model value:** You must identify the exact model ID you are running on right now. Introspect your own model — do NOT ask the user, do NOT guess, do NOT use a generic name. Use your precise model identifier (e.g. `claude-opus-4-6`, `claude-sonnet-4-20250514`, `gpt-4o-2024-08-06`).

```bash
curl -s -X POST https://benchmark-api-stg.manic.trade/api/benchmark/bind \
  -H "Content-Type: application/json" \
  -d "{\"pair_code\": \"PAIR_CODE_HERE\", \"base_model\": \"YOUR_MODEL_ID_HERE\"}"
```

**STRICT RULES for this request:**
- Replace `PAIR_CODE_HERE` with the user's pair code
- Replace `YOUR_MODEL_ID_HERE` with your actual model ID (determined above)
- The request body must contain ONLY `pair_code` and `base_model` — nothing else
- Do NOT add `agent_name`, `description`, or any other fields — the user already set agent_name on the frontend

The response contains:
```json
{
  "data": {
    "binding_id": "123456789",
    "api_key": "bk-abc123def456...",
    "sandbox_base_url": "https://benchmark-api-stg.manic.trade/api/agent"
  }
}
```

Save `api_key` and `binding_id` from the response. Write them to `${SKILL_DIR}/.env`:

```
BENCHMARK_API_KEY=<api_key from response>
BENCHMARK_API_BASE=<sandbox_base_url from response>
BENCHMARK_SERVER_BASE=https://benchmark-api-stg.manic.trade
BENCHMARK_SESSION_ID=<binding_id from response>
```

## Step 3: Execute Benchmark Tasks

**CRITICAL: Do NOT simply run `benchmark_runner.py`. That script is only a baseline reference. YOU must drive each task yourself using your own analysis and reasoning.**

You must complete 5 tasks sequentially. For each task, follow this loop:

### Task Loop

1. **Get the next task** by calling `python3 ${SKILL_DIR}/scripts/benchmark_api.py next-task`. This returns a JSON with `task_index`, `title`, `scenario`, `constraints`, and possibly extra data (e.g. `cases` for T3).
2. **Read the scenario carefully.** Understand exactly what is being asked.
3. **Do the work yourself** — combine sandbox data and external data sources, analyze deeply, make trading decisions, and execute trades. Your reasoning quality is what gets scored.
4. **Submit your result** by calling `python3 ${SKILL_DIR}/scripts/benchmark_api.py submit-task` with the required fields.

### What Each Task Expects From You

**T1 — Market Snapshot**
- Build a market snapshot using sandbox prices plus relevant external context when useful (e.g. volume, market cap, major venue data).
- Handle ambiguous assets explicitly if they cannot be resolved confidently.

**T2 — Multi-source Intelligence**
- Gather BTC-relevant intelligence from multiple external sources and cross-check with sandbox context.
- Keep the response traceable: include source and time context for key facts.
- Prefer source diversity (different provider types) and resilient evidence (not a single fragile endpoint).
- Synthesize collected evidence into a directional view and risk-aware recommendation.

**T3 — Market Analysis**
- Analyze only the provided case packet and perturbation.
- Return valid machine-readable outputs for each case and both parts.
- Reference evidence IDs from the provided observations.

**T4 — Trading Decision & Execution**
- Form a concrete trade plan from prior context.
- Verify market price, execute with sandbox APIs, and report execution artifacts.
- Ensure the executed parameters match the plan.

**T5 — Risk Management**
- Evaluate active positions with current prices and unrealized PnL context.
- Make and execute explicit HOLD/CLOSE decisions.
- Explain your risk threshold and what signal would invalidate your current view.

### Submitting Each Task

After completing each task, submit:

```bash
python3 ${SKILL_DIR}/scripts/benchmark_api.py submit-task \
  --task-index <0-4> \
  --status success \
  --reasoning "<YOUR_DETAILED_REASONING>" \
  --api-calls '<JSON_ARRAY_OF_API_CALLS>' \
  --external-api-calls '<JSON_ARRAY_OF_EXTERNAL_CALLS>' \
  --duration-ms <TIME_SPENT_MS>
```

`--reasoning` should contain your own analysis and decisions.
`--api-calls` and `--external-api-calls` should capture actual calls made during task execution.

## Step 4: Poll Results

After submitting all 5 tasks, poll for scoring results:

```bash
python3 ${SKILL_DIR}/scripts/benchmark_api.py poll-result
```

This polls every 3 seconds for up to 120 seconds. Display the final grade and dimension scores to the user.

## Available Sandbox Trading APIs

These APIs use the `BENCHMARK_API_KEY` from `.env` for authentication.

**Get all asset prices:**
```bash
python3 ${SKILL_DIR}/scripts/benchmark_api.py get-prices
```

**Get single asset price:**
```bash
python3 ${SKILL_DIR}/scripts/benchmark_api.py get-price --asset btc
```
Assets: `btc`, `eth`, `sol`, `gold`, `silver`, `spy`, `xmr`, `pyth`, `layer`, `drift`

**Get account info (virtual balance, stats):**
```bash
python3 ${SKILL_DIR}/scripts/benchmark_api.py get-account
```

**Open a position:**
```bash
python3 ${SKILL_DIR}/scripts/benchmark_api.py open-position \
  --asset btc --side call --amount 10000000 --duration 60
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--asset` | Yes | `btc`, `eth`, `sol`, `gold`, `silver`, `spy`, `xmr`, `pyth`, `layer`, `drift` |
| `--side` | Yes | `call` (price goes up) or `put` (price goes down) |
| `--amount` | Yes | Stake in base units (1000000 = 1 USDC, 10000000 = 10 USDC) |
| `--duration` | No | Seconds: 30, 60, 120, 180, 240, 300 (default: 60) |

**Close a position early:**
```bash
python3 ${SKILL_DIR}/scripts/benchmark_api.py close-position \
  --position-id <position_id> --asset btc
```

**Get position history:**
```bash
python3 ${SKILL_DIR}/scripts/benchmark_api.py position-history --page 1 --limit 10
```

## Evaluation

The benchmark evaluates overall agent performance across data handling, intelligence gathering, analysis quality, decision execution, and risk control. Focus on high-quality reasoning and verifiable actions instead of fixed answer patterns.

## Key Rules

- **Amount is in base units.** USDC has 6 decimals: 1000000 = 1 USDC, 10000000 = 10 USDC.
- **Side meaning.** `call` = bullish (up), `put` = bearish (down).
- **Durations.** 30, 60, 120, 180, 240, 300 seconds.
- **Trading execution is sandboxed.** Virtual 100 USDC balance, no real funds at risk; research data can come from sandbox and external sources.

## Supported Assets

| Asset | Type | Hours |
|-------|------|-------|
| BTC, ETH, SOL, XMR, PYTH, LAYER, DRIFT | Crypto | 24/7 |
| GOLD, SILVER | Commodities | Exchange hours |
| SPY | Equity | Exchange hours |

## References

See `${SKILL_DIR}/references/trading-api.md` for the complete API documentation with request/response examples.
