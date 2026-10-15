---
name: "@432/meta-dex-aggregator"
description: "Meta DEX Aggregator — aggregator of aggregators. Compares quotes across ParaSwap, Odos, KyberSwap, Matcha/0x, and 1inch to find the best swap price. Includes safety layer: price impact detection, gas-adjusted ranking, MEV protection flagging, slippage warnings, and outlier quote rejection. Use when the user wants to swap tokens, compare DEX prices, or find the best swap route across multiple aggregators."
version: 2.1.1
tools:
  - bash
  - oneinch_quote
  - oneinch_tokens
  - oneinch_check_allowance
  - oneinch_approve
  - oneinch_swap
  - wallet_balance
  - wallet_transfer
---

# Meta DEX Aggregator — Multi-Source Quote Comparison with Safety Layer

Aggregator of aggregators. Queries 5 DEX aggregators in parallel, ranks by
gas-adjusted net output, and runs safety checks before execution.

## Safety Features

1. **Price Impact** — Fetches fair market price from DefiLlama coins API
   (+ DexScreener fallback), compares vs quote output.
   Thresholds: 3% warning, 5% high, 10% critical (blocks swap).
2. **Gas-Adjusted Ranking** — `netOut = amountUsd - gasUsd`. Best route ≠ most tokens.
3. **MEV Protection Flags** — CowSwap and 0x Gasless are flagged `isMEVSafe`.
   Recommends MEV-safe route when within 0.5% of best price.
4. **Slippage Warnings** — Sandwich risk >1%, stablecoin pairs >0.05%, too-low revert risk.
5. **Outlier Detection** — Quotes >5% worse than best are flagged as outliers.

## Aggregators

| Adapter | API Key | Status |
|---------|---------|--------|
| ParaSwap | None needed | ✅ |
| Odos | None needed | ✅ |
| KyberSwap | None needed | ✅ |
| 1inch | Native tool (platform-proxied) | ✅ |
| Matcha/0x | `OX_API_KEY` in .env | ✅ |

## Workflow: Quote with Safety Check

**Step 1 & 2 run in PARALLEL (no dependency between them):**

```bash
# 1. Get 4 aggregator quotes (ParaSwap, Odos, KyberSwap, Matcha/0x + safety)
cd skills/meta-dex-aggregator/scripts && \
  python3 meta_dex.py quote --chain base --from ETH --to USDC --amount 0.5 --slippage 0.5
```

```
# 2. Get 1inch quote via native tool (proxied, no API key needed)
oneinch_quote(chain="base", src="<from_addr>", dst="<to_addr>", amount="<amount_in_wei>")
# Returns: { "dstAmount": "<raw_amount>" }
# Convert: dstAmount / 10^decimals = human amount
```

**Step 3 — Merge & present:**
- Script returns quotes with: `aggregator`, `amountOutHuman`, `amountUsd`, `gasUsd`, `netOut`, `vsbestPct`
- 1inch native tool returns `dstAmount` (raw wei) — convert to human amount using token decimals
- Insert 1inch into the ranked table, recalculate `vsbestPct` if 1inch is the new winner
- The script's `safety` block (priceImpact, slippageWarnings, recommendation) applies to all quotes
- If `priceImpact.severity` is "high"/"critical" — WARN and **block the swap**
- Execute via `oneinch_swap` if 1inch wins, or `wallet_transfer` with tx data for others

## Workflow: Execute Swap

```bash
# 1. Get wallet address
wallet_info()

# 2. Get swap tx data
cd skills/meta-dex-aggregator/scripts && \
  python3 meta_dex.py swap --chain base --from ETH --to USDC --amount 0.5 \
    --aggregator odos --wallet 0x... --slippage 0.5

# 3. For ERC-20 tokens: check + set approval
oneinch_check_allowance(chain, token) → oneinch_approve(chain, token) if needed

# 4. Execute via wallet_transfer using the tx data from step 2
wallet_transfer(to=tx.to, amount=tx.value, data=tx.data, chain_id=chainId)
```

## Cross-Chain Swaps

When src_chain ≠ dst_chain, use `xquote` to compare cross-chain routes:

```bash
python3 skills/meta-dex-aggregator/scripts/meta_dex.py xquote \
  --src-chain arbitrum --dst-chain polygon \
  --from ETH --to USDC --amount 0.5 \
  --wallet $WALLET --slippage 3
```

**Cross-chain sources:**
- **LI.FI** — aggregates 20+ bridges (Relay, Stargate, Across, Hop, etc.). Returns ready-to-sign tx data. Execute via `wallet_transfer(to, amount=value, data, chain_id, gas_limit)`. Track status with `curl -s "https://li.quest/v1/status?txHash={hash}&fromChain={src_id}&toChain={dst_id}"`.
- **1inch Fusion+** — intent-based atomic swaps (gasless, resolver handles both chains). The script returns a `needsToolCall: true` marker. Complete with `oneinch_cross_chain_quote` tool for the quote, then `oneinch_cross_chain_swap` for execution.

**Cross-chain workflow:**
1. Run `xquote` → get LI.FI routes + 1inch Fusion+ marker
2. Call `oneinch_cross_chain_quote` tool to fill in the 1inch quote
3. Compare all routes: output amount, total fees (gas + bridge + protocol), estimated time
4. Present table to user with clear winner
5. For execution: LI.FI routes → `wallet_transfer` with tx data; 1inch → `oneinch_cross_chain_swap`
6. Cross-chain is non-atomic — track status and confirm delivery on destination chain

**Safety notes for cross-chain:**
- Default slippage 3% (bridges need more than same-chain swaps)
- Always show estimated delivery time (4s to 10min depending on bridge)
- Always show fee breakdown (gas + bridge fees + protocol fees)
- After execution, track until funds arrive on destination chain
- LI.FI `DONE/PARTIAL` means bridge delivered but not the final token — may need a manual swap

## Token Resolution — Smart Confirmation

Token resolution is tiered to avoid bothering the user for obvious tokens
while protecting against picking the wrong contract for ambiguous ones.

### Confidence levels returned by `resolve_token`:

| Confidence | Meaning | Action |
|-----------|---------|--------|
| `trusted` | Hardcoded canonical address (USDC, WETH, WBTC, etc.) | ✅ Auto-use, no confirmation |
| `exact` | User provided a 0x address directly | ✅ Auto-use, no confirmation |
| `single` | Only one token matches the symbol on this chain | ✅ Auto-use, no confirmation |
| `high` | Multiple matches but top has >10x volume of runner-up | ✅ Auto-use, no confirmation |
| `ambiguous` | Multiple plausible matches, none dominant | ⚠️ **MUST confirm with user** |

### When `confidence == "ambiguous"`:

The result includes a `candidates` list. Present them to the user:

```
I found multiple tokens matching "XYZ" on Arbitrum:

1. XYZ (XYZ Protocol) — 0x1234...5678 — $2.3M 24h vol
2. XYZ (XYZ Finance) — 0xabcd...ef01 — $180K 24h vol
3. XYZ (Old XYZ) — 0x9876...5432 — $12K 24h vol

Which one did you mean? (or paste the contract address directly)
```

Once the user picks, re-call with the address directly to bypass resolution.

### Trusted token coverage:

Ethereum, Arbitrum, Base, Optimism, Polygon, BSC, Avalanche, Gnosis —
all major tokens (WETH, USDC, USDT, DAI, WBTC, LINK, UNI, AAVE, stETH,
plus chain-specific tokens like ARB, OP, AERO, GMX, etc.)

## Chain Support

ethereum, bsc, polygon, optimism, arbitrum, avalanche, gnosis, fantom,
zksync, base, linea, scroll, sonic, unichain

## Safety Response Format

The `quote` command returns a `safety` block:
```json
{
  "recommendation": "✅ All checks passed. Best route looks safe.",
  "priceImpact": {"value": 0.02, "severity": "ok"},
  "slippageWarnings": [],
  "marketPrices": {"gas_token_price": 2170, "from_token_price": 2170, "to_token_price": 1.0}
}
```

Severity levels: `ok` | `warning` (3%) | `high` (5%) | `critical` (10%)

**CRITICAL: If severity is "high" or "critical", BLOCK the swap and warn the user explicitly.**
