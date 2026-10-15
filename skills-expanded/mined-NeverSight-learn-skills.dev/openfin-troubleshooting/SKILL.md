---
name: openfin-troubleshooting
description: >-
  Error-to-fix playbook for every known failure mode on the OpenFinance backend
  — Polymarket, Relay, Hyperliquid, Privy delegation, and Solana RPC issues.
  Use this the moment a call fails, returns an unexpected status, or behaves
  inconsistently with on-chain state. Triggers on ANY of these error signatures
  verbatim or in paraphrase. Polymarket&#58; "allowance: 0 but on-chain shows
  max", "CLOB reports allowance 0", "approvals confirmed but order rejected",
  "404 upstream" on market orders, "tick size" rejection, "order size below
  minimum", USDC.e vs pUSD vs native USDC confusion, V1 vs V2 exchange
  confusion. Relay&#58; "InstructionFallbackNotFound", "Custom:101",
  "Custom:6000", "AnchorError", "Blockhash not found", "TransactionExpired",
  "No valid authorization signatures were provided", "Solana wallet is not
  delegated to the app", 412 delegation errors, quote succeeded but execute
  failed, stuck funds on Solana, stuck funds cross-chain, topupGas forced off.
  Hyperliquid&#58; "Insufficient perp account value", "price out of bounds",
  WebSocket stale data, spot vs perp balance confusion. General&#58; any "why is X
  failing", "why does on-chain and API state disagree", "what does this error
  mean". Read this BEFORE assuming a bug in the MCP or backend — most of these
  errors are already catalogued with known fixes.
---

# OpenFinance Troubleshooting

Error → diagnosis → fix. Check here before assuming an issue is a server-side
bug: most failures are known and have been hit before.

## Polymarket

### `POST /agent/polymarket/approvals` shows max but CLOB returns `allowance: 0`

**Root cause:** approval targeted the wrong USDC contract or wrong exchange spender.

Polymarket on Polygon enforces allowance against **USDC.e**
(`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`), not pUSD or native USDC. And
orders settle on the **V1 exchange** (`0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`),
not V2 — even though the SDK is `clob-client-v2`. The CLOB's `GET /version`
returns `1`.

**Fix:** Call `POST /agent/polymarket/approvals` with `{negRisk: true}` if the
market is neg-risk. The server approves USDC.e on V1 spenders. If you
previously approved a different token manually, those allowances are stuck
against the wrong token.

### `POST /agent/polymarket/order/market` returns `404 upstream` (limit orders work)

**Root cause:** SDK's `createMarketOrder` calls `ensureBuilderFeeRateCached`
which does unauthenticated `GET /fees/builder-fees/<code>`. That endpoint
404s until Polymarket's fee service has the builder code onboarded.

**Fix:** Already patched — the backend catches the 404 and caches a zero-rate
entry. If you still see this, the deployment is behind. Retry passes through
after the patch is live.

### `Order failed: tick size` on a price that looks right

**Root cause:** Market's minimum tick size is smaller than `0.01` (the default).
Passing `0.01` when the market needs `0.001` or `0.0001` rejects.

**Fix:** Pass `tickSize: "0.001"` or `"0.0001"` explicitly in the request body.
Read the market's min tick from `GET /agent/polymarket/markets/cid/:conditionId`.

### `Order size below minimum`

Polymarket requires ~$1 USDC minimum notional. `price=0.05, size=10` = $0.50
notional → rejected.

**Fix:** Increase size so `price * size >= 1`.

## Relay

### `InstructionFallbackNotFound (Custom:101)` on Solana-origin execute

**Root cause:** Instruction data decoded with wrong encoding. Relay returns
Solana instruction `data` as **hex** (no `0x` prefix), not base64. Early
backend versions decoded as base64 → garbage bytes → depository rejected.

**Fix:** Already patched. First 8 bytes of a correctly-decoded instruction
should match Relay's discriminator (e.g. `0b9c60da27a3b413`).

### `Blockhash not found` repeatedly on Solana execute

**Root cause:** Privy's `signAndSendTransaction` uses a different RPC than
the one that issued the blockhash. Cross-RPC divergence — no retry fixes it.

**Fix:** Already patched — backend now uses Privy's `signTransaction` (sign
only) and broadcasts via our own RPC with `skipPreflight: true`. If you still
see it, set `SOLANA_RPC_URL` to a dedicated provider (Helius/Triton/QuickNode)
— the public `api.mainnet-beta.solana.com` is heavily throttled.

### `401 No valid authorization signatures were provided` on Solana execute

**Root cause:** User's Solana wallet isn't delegated to the app. EVM
delegation doesn't transfer.

**Fix:** See `openfin-setup` step 2 — frontend must call
`useDelegatedActions().delegateWallet({ address: solanaAddress, chainType: 'solana' })`.
Server catches this now and returns 412 with a clearer message.

### `POST /agent/relay/execute` says "User has no Solana wallet provisioned"

**Root cause:** Privy app isn't configured to create Solana embedded wallets,
or the specific user logged in before Solana was enabled.

**Fix:** Enable Solana in Privy dashboard; existing users may need to trigger
wallet creation.

### Gas topup forced off unexpectedly

**Expected behavior, not a bug.** When either origin or destination chain ID
is Solana (`792703809`), `topupGas` is forced to `false` server-side. Topup
doesn't work cleanly for EVM↔SVM routes.

## Hyperliquid

### `Insufficient perp account value`

**Root cause:** Perp trading requires margin. USDC on Hyperliquid isn't
automatically available for perp trading.

**Fix:** `POST /agent/trading/transfer` to move USDC between spot and perp
accounts, or deposit first via `GET /agent/trading/deposit-address`.

### WebSocket data is stale

**Root cause:** The backend maintains one shared connection to
`wss://api.hyperliquid.xyz/ws` and caches per-channel. If the connection dropped
and reconnected, the first few messages after reconnect may be missing.

**Fix:** The backend auto-reconnects after 3s. Retry the read; cache fills
within a few seconds. If persistent, something is wrong with outbound WS from
the server host.

### `Order rejected: price out of bounds`

**Root cause:** Hyperliquid rejects prices too far from the current mid (price
bands). Typically ±5-10% depending on asset.

**Fix:** Read mid via `GET /agent/trading/market/mids` and set price within
bounds. For aggressive fills, use limit orders crossing the book but within
the band.

## General principles

1. **Check `GET /agent/wallets` first** when anything auth-related fails. It
   tells you if delegation is in place and which chains are provisioned.
2. **On-chain state != CLOB/Relay state.** Approvals can show on-chain but
   still report 0 upstream because of token/contract mismatches. Don't trust
   "on-chain says X" without also checking the service's view.
3. **When in doubt, read the error string verbatim** — don't paraphrase. Many
   errors have specific signatures (`Custom:101` vs `Custom:6000`) that map to
   exactly one fix.
