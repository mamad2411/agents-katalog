---
name: hodlmm-rebalance-arbiter
description: "Decision gate that consumes 2 independent signals — bin drift and sBTC peg health — to produce a single REBALANCE, BLOCKED, or IN_RANGE verdict for HODLMM concentrated liquidity positions."
metadata:
  author: "cliqueengagements"
  author-agent: "Micro Basilisk (Agent 77) — SP219TWC8G12CSX5AB093127NC82KYQWEH8ADD1AY | bc1qzh2z92dlvccxq5w756qppzz8fymhgrt2dv8cf5"
  user-invocable: "true"
  arguments: "doctor | install-packs | run --wallet <address> [--pool <id>]"
  entry: "hodlmm-rebalance-arbiter/hodlmm-rebalance-arbiter.ts"
  requires: ""
  tags: "defi, read-only, mainnet-only, infrastructure"
---

# hodlmm-rebalance-arbiter

## What it does

Answers one question for HODLMM liquidity providers: **"Should I rebalance right now, or wait?"**

Running 2 monitoring skills independently gives you 2 separate signals — but no verdict. An LP still has to cross-reference bin drift and sBTC peg health manually. The arbiter encodes the operational logic into a single decision gate.

It evaluates the same dimensions as hodlmm-bin-guardian and sbtc-proof-of-reserve, then applies a priority matrix:

| Scenario | Decision |
|---|---|
| All GREEN | **REBALANCE** — safe to move |
| Reserve YELLOW | **REBALANCE** — acceptable risk |
| Any RED | **BLOCKED** — specific reason provided |
| Any ERROR | **DEGRADED** — fix data sources first |
| Bins in range | **IN_RANGE** — no rebalance needed |

The skill does NOT execute transactions. It outputs a verdict with evidence so the LP (or a future executor skill) can act with confidence.

## Why agents need it

Monitoring without a decision layer is noise. bin-guardian says REBALANCE, but is the sBTC peg healthy enough to move capital? Today, nobody answers that question. The arbiter fills the gap between monitoring and action in the HODLMM LP lifecycle.

Key insight: sometimes the most profitable move is doing nothing. During peg instability, executing a rebalance risks value loss. Earning zero fees in a safe position is better than rebalancing into instability. The arbiter enforces this discipline.

v2 note: The original submission included a third signal (Bitcoin tenure timing) which was removed after community review identified a flawed premise — L1 has no price awareness, so tenure staleness is not a valid safety signal. Rather than replacing it with something cosmetic, we stripped it out. Two rock-solid signals beat three with a weak link.

## Safety notes

- **Read-only** — never executes transactions, never moves funds
- **Fail-safe default** — missing, malformed, or stale data always pushes toward WAIT or DEGRADED, never toward REBALANCE
- **Double YELLOW = WAIT** — one caution signal is acceptable risk; two simultaneous caution signals mean the environment is degrading and action should be deferred
- **Silence locks the gate** — you need 2 positive signals to unlock REBALANCE; any gap in data blocks action
- **No API keys required** — all data from public Bitflow, Hiro, and mempool.space endpoints
- **Structured exit codes** — 0 (rebalance/in_range), 1 (blocked), 3 (degraded/error)

## Commands

### `doctor`
Verifies all 8 data sources: Bitflow Quotes, Bitflow App, Bitflow Bins, Hiro Stacks, sBTC Registry, sBTC Supply Contract, mempool.space, and bech32m self-test.

```bash
bun run skills/hodlmm-rebalance-arbiter/hodlmm-rebalance-arbiter.ts doctor
```

### `install-packs`
No additional packs required. Uses native `fetch` for all API calls.

```bash
bun run skills/hodlmm-rebalance-arbiter/hodlmm-rebalance-arbiter.ts install-packs
```

### `run`
Fetches both signals in parallel, applies the priority matrix, and outputs the decision.

```bash
# Default pool (dlmm_1)
bun run skills/hodlmm-rebalance-arbiter/hodlmm-rebalance-arbiter.ts run --wallet SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9

# Specific pool
bun run skills/hodlmm-rebalance-arbiter/hodlmm-rebalance-arbiter.ts run --wallet SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9 --pool dlmm_2
```

#### `--wallet <address>` (required)
Stacks mainnet address (SP...) to check bin positions for. The arbiter needs to know which bins the LP holds to determine if a rebalance is needed.

#### `--pool <id>` (optional, default: dlmm_1)
HODLMM pool ID to evaluate.

## Output contract

```json
{
  "status": "ok | degraded | error",
  "decision": "REBALANCE | BLOCKED | IN_RANGE | DEGRADED",
  "reason": "All signals aligned. Bins out of range (active: 8388610, position: 8388600–8388605). Safe to rebalance.",
  "signals": {
    "bin_guardian": {
      "color": "GREEN | YELLOW | RED | ERROR",
      "needs_rebalance": true,
      "active_bin": 8388610,
      "user_bin_range": { "min": 8388600, "max": 8388605, "count": 6 },
      "in_range": false,
      "slippage_pct": 0.12,
      "volume_24h_usd": 515000,
      "apr_24h_pct": 47.6,
      "pool_id": "dlmm_1",
      "pair": "sBTC/USDCx"
    },
    "sbtc_reserve": {
      "color": "GREEN | YELLOW | RED | ERROR",
      "reserve_ratio": 1.002,
      "score": 100,
      "hodlmm_signal": "GREEN",
      "sbtc_circulating": 980.5,
      "btc_reserve": 982.3,
      "signer_address": "bc1p...",
      "recommendation": "sBTC fully backed. Safe for HODLMM operations."
    }
  },
  "blockers": [],
  "retry_after": null,
  "pool_id": "dlmm_1",
  "wallet": "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9",
  "timestamp": "2026-04-02T...",
  "error": null
}
```

### WAIT output example

```json
{
  "status": "ok",
  "decision": "BLOCKED",
  "reason": "Rebalance needed but blocked — sBTC peg unhealthy (ratio: 0.9820). Moving capital during de-peg risks value loss.",
  "signals": {
    "bin_guardian": { "color": "RED", "needs_rebalance": true },
    "sbtc_reserve": { "color": "RED", "reserve_ratio": 0.982, "recommendation": "sBTC under-collateralized. Do not rebalance into sBTC-paired pools." }
  },
  "blockers": ["sbtc_reserve: RED — reserve ratio 0.9820, peg unhealthy"],
  "retry_after": "2026-04-02T01:15:00.000Z"
}
```

## Data sources

| Source | Endpoint | Signal |
|--------|----------|--------|
| Bitflow Quotes API | `/api/quotes/v1/pools` | bin_guardian — pool discovery |
| Bitflow App API | `/api/app/v1/pools` | bin_guardian — TVL, volume, APR |
| Bitflow Bins API | `/api/quotes/v1/bins/{pool_id}` | bin_guardian — active bin, prices |
| Bitflow User Positions | `/api/app/v1/users/{addr}/positions/{pool}/bins` | bin_guardian — LP bin positions |
| Hiro Node Info | `/v2/info` | sbtc_reserve — block heights |
| sBTC Contract | `call-read/get-total-supply` | sbtc_reserve — circulating supply |
| sBTC Registry | `call-read/get-current-aggregate-pubkey` | sbtc_reserve — signer pubkey |
| mempool.space | `/api/address/{addr}` | sbtc_reserve — BTC reserve balance |

## HODLMM integration

This skill is the decision layer in the HODLMM LP lifecycle:

| Phase | Skill | Role |
|-------|-------|------|
| Entry | usdcx-yield-optimizer | Where to deploy capital |
| Monitor | bin-guardian, sbtc-reserve | Watch for drift and peg health |
| **Act** | **hodlmm-rebalance-arbiter** | **Should I rebalance now? GO or WAIT** |
| Optimize | smart-yield-migrator, hermetica-yield-rotator | Move between protocols |
| Exit | hodlmm-emergency-exit | Get out when things break |

The arbiter sits between monitoring and action. Without it, monitoring skills output signals that nobody synthesizes — an LP has to manually cross-reference 3 outputs every time they consider a rebalance.

## Known constraints

- Read-only — outputs a decision but cannot execute the rebalance itself. The LP or a future executor skill acts on the verdict.
- sBTC reserve check uses the full Golden Chain derivation (aggregate pubkey → P2TR address → BTC balance). If the sbtc-registry contract changes its pubkey format, the derivation will fail gracefully (ERROR → DEGRADED).
- v2 removed the tenure signal after community review (PR #125 feedback from @JakeBlockchain) identified a flawed premise. The skill is leaner and every remaining signal is defensible.
- The arbiter requires `--wallet` — it cannot make a rebalance decision without knowing which bins the LP holds.
