---
name: odos
description: Use this skill when the user asks to swap tokens, get a swap quote, provide liquidity (zap), look up DeFi token prices, or execute multi-asset swaps via the Odos DEX aggregator. Triggers on phrases like "swap X for Y", "quote", "best route", "multi-asset swap", "zap into pool", "Odos". The skill loads sub-skills under `skills/` for each operation.
version: 1.0.0
homepage: https://docs.odos.xyz
license: MIT
metadata:
  openclaw:
    emoji: "🔀"
    homepage: https://docs.odos.xyz
    requires:
      anyBins:
        - cast
        - curl
        - jq
    web3:
      networks: [1, 10, 56, 130, 137, 146, 252, 324, 5000, 8453, 34443, 42161, 43114, 59144]
      protocol: dex-aggregator
      policy:
        allowedContracts:
          1: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Ethereum
          10: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Optimism
          56: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # BNB Chain
          130: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Unichain
          137: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Polygon
          146: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Sonic
          252: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Fraxtal
          324: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # zkSync Era
          5000: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Mantle
          8453: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Base
          34443: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Mode
          42161: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Arbitrum
          43114: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Avalanche
          59144: ["0x0D05a7D3448512B78fa8A9e46c4872C88C4a0D05"] # Linea
        permit2: "0x000000000022D473030F116dDEE9F6B43aC78BA3"
        slippage:
          defaultPercent: 0.5
          maxPercent: 3.0
          requireConfirmAbovePercent: 5.0
---

# Odos DEX aggregator skill

Odos is a smart-order-routing DEX aggregator for EVM chains. It splits trades
across multiple liquidity sources to maximize output net of gas. Unique
feature: it can swap **multiple input tokens into a single output** in one
atomic transaction (multi-asset input).

## Pick the right sub-skill

| User intent | Sub-skill |
| --- | --- |
| "What's the best price for swapping X for Y?" | `skills/odos-quote.md` |
| "Swap X for Y" (signed + broadcast) | `skills/odos-swap.md` |
| "Swap A, B, and C into D in one tx" | `skills/odos-multi-asset-swap.md` |
| "Add liquidity to pool P" | `skills/odos-zap.md` |
| "Show me how Odos routed this swap" | `skills/odos-path-viz.md` |
| "What's the price of token T?" | `skills/odos-pricing.md` |

## Safety rules — apply to every sub-skill

1. **Always quote then confirm before executing.** Show the user the expected
   output amount, gas cost, price impact, and net-out value, then ask
   "shall I proceed?" before broadcasting any transaction.
2. **Always run Odos's simulation first** by calling `/sor/assemble` with
   `"simulate": true`. If `simulation.isSuccess === false`, refuse to
   broadcast and surface the simulation error.
3. **Never modify the calldata returned by `/sor/assemble`.** Pass it
   verbatim to `cast send`. Modifying it will lose funds and Odos won't
   support it.
4. **Slippage default is 0.5%.** Don't quietly raise this. If the user wants
   higher, make them say so explicitly.
5. **Token approvals.** ERC-20 swaps need an approval to the Odos router
   first. Either do an `approve()` tx via `cast` *or* use the Permit2 flow in
   `odos-swap.md` to skip the approve.

## Common environment

```bash
# Required for execution skills
export RPC_URL=https://...         # per-chain RPC

# Preferred signer: encrypted Foundry keystore
export ODOS_KEYSTORE="$HOME/.foundry/keystores/agent"
export ODOS_KEYSTORE_PASSWORD_FILE="$HOME/.foundry/keystore.pw"
SIGNER_ARGS=(--keystore "$ODOS_KEYSTORE" --password-file "$ODOS_KEYSTORE_PASSWORD_FILE")

# If you really must use a raw key, keep it out of child-process environments
# and logs. Prefer reading it from a password manager for a single command:
# SIGNER_ARGS=(--private-key "$(op read 'op://Private/agent-signer/private key')")

# Last-resort fallback only:
# export PRIVATE_KEY=0x...         # signer; inherited by child processes
# SIGNER_ARGS=(--private-key "$PRIVATE_KEY")

# Optional
export ODOS_API_KEY=...            # partner/enterprise; not needed for public quotes
```

## Common chain IDs

```
1     Ethereum
10    Optimism
56    BNB Chain
130   Unichain
137   Polygon
146   Sonic
252   Fraxtal
324   zkSync Era
5000  Mantle
8453  Base
34443 Mode
42161 Arbitrum
43114 Avalanche
59144 Linea
```

## Common chain endpoints (info that every sub-skill may need)

```bash
# Supported chains
curl -s https://api.odos.xyz/info/chains | jq

# Tradable tokens on a chain
curl -s https://api.odos.xyz/info/tokens/8453 | jq '.tokenMap | keys[:20]'

# v3 router contract address (the `to` address for Odos swaps)
curl -s https://api.odos.xyz/info/router/v3/8453 | jq

# Liquidity sources Odos can route through on a chain
curl -s https://api.odos.xyz/info/liquidity-sources/v3/8453 | jq

# Current block height as Odos sees it
curl -s https://api.odos.xyz/info/current-block/8453 | jq
```

## Errors you'll see

- `400 PATH_NOT_FOUND` — no route exists between these tokens at this size.
  Try a smaller size or different output token.
- `400 INVALID_AMOUNT` — amount is `0` or negative; remember it's in token
  base units (a string), not whole tokens.
- `429` — rate limit. Wait a few seconds and retry, or get an API key.
- `simulation.isSuccess === false` — the assembled tx would revert. Do not
  broadcast. Common causes: insufficient balance, missing approval, slippage
  too tight.
