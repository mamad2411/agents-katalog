---
name: openfin-troubleshooting
author: OpenFinance
homepage: https://openfinance.tech
license: Proprietary
version: 1.0.1
description: Error → fix lookup for the OpenFinance backend (Polymarket, Relay, Hyperliquid, Solana RPC, account-setup). Use the moment a call fails or returns an unexpected status. Triggers on the error signatures verbatim or paraphrased — Polymarket — "maker address not allowed", post-migration balance/allowance both reading 0, "allowance max but CLOB returns 0", "tick size", "order size below minimum"; Relay — "InstructionFallbackNotFound / Custom:101", "Blockhash not found", "401 No valid authorization signatures" or 412 on Solana execute, "User has no Solana wallet provisioned", "topupGas forced off"; Hyperliquid — "Insufficient margin / account value too low", "withdrawal not arriving on Arbitrum", WebSocket stale data, "price out of bounds". Read this BEFORE assuming a bug.
---

# OpenFinance Troubleshooting

> **Publisher.** Part of the OpenFinance skill bundle (openfin-setup, openfin-troubleshooting, openfin-hyperliquid, openfin-relay, openfin-onramp, openfin-polymarket, openfin-onchain) — all maintained by OpenFinance (https://openfinance.tech). Install as a set, not individually.

Error → fix lookup. Most errors map to exactly one fix.

## Polymarket

### `maker address not allowed, please use the deposit wallet flow`

Polymarket's CLOB rejects raw EOAs. Orders must name the **deposit
wallet** as `funder`/`signer` with `signatureType=POLY_1271`. The
backend handles this automatically; if you still see the error, confirm
the user's deposit wallet via `GET /agent/polymarket/deposit-wallet`
and verify the deployment has the deposit-wallet path enabled.

### `not enough balance / allowance: balance: 0`

pUSD is on the EOA, not the deposit wallet. Orders settle from the
deposit wallet — pUSD on the EOA is stranded for trading.

**Fix:** `GET /agent/polymarket/deposit-wallet`. If `pUSD.eoa > 0` and
`pUSD.depositWallet == 0`, transfer pUSD from EOA → deposit wallet
(plain ERC-20 `transfer`, EOA pays MATIC). Going forward, route
Polymarket-bound deposits to the deposit wallet, not the EOA.

### `allowance: 0` / `not enough balance / allowance` after the wallet has pUSD

V2 settles against **pUSD** (`0xC011a7E12a19f7B1f670d46F03B03f3342E82DFB`),
not USDC.e.

**Fix:** Retry the order — the order endpoints recover from this. If
the wallet still holds USDC.e (no longer the settlement token), convert
/ bridge it to pUSD first.

### `Order failed: tick size`

Default `tickSize` is `0.01`; some markets need `0.001` or `0.0001`.

**Fix:** Read `min_tick_size` from the market metadata
(`GET /agent/polymarket/markets/cid/:conditionId`) and pass it
explicitly.

### `Order size below minimum`

Polymarket requires ~$1 USDC notional. Bump `size` so
`price * size >= 1`.

## Relay

### `InstructionFallbackNotFound (Custom:101)` on Solana execute

Already patched (instruction data is hex, not base64). If it returns,
the deployment is behind.

### `Blockhash not found` repeatedly on Solana execute

Cross-RPC divergence. Already patched (backend signs and broadcasts
via its own RPC). If persistent, set `SOLANA_RPC_URL` to a dedicated
provider (Helius / Triton / QuickNode) — the public RPC is throttled.

### `401 No valid authorization signatures` / `412` on Solana execute

The user's openfinance.tech account is missing the Solana side of the
setup.

**Fix:** Send the user to [openfinance.tech](https://openfinance.tech)
to complete setup, then retry. Quotes were unaffected — no state spent.

### `User has no Solana wallet provisioned`

The user's account predates Solana support, or Solana isn't enabled.

**Fix:** Send the user to openfinance.tech to enable Solana, then
retry.

### Gas topup forced off

**Expected, not a bug.** When either origin or destination chain is
Solana (`792703809`), `topupGas` is forced `false` (EVM↔SVM topup
doesn't route cleanly).

## Hyperliquid

### `Insufficient margin` / `account value too low`

Three causes:
- The unified balance is genuinely below the required notional.
- The wallet isn't in `unifiedAccount` mode yet (so spot USDC isn't
  perp margin).
- The agent only read `account.withdrawable` and missed the spot slice.

**Fix:** Run the auto-unify rule (one call now — `/account/spot` was
removed; the spot slice ships in the same envelope):

```
snap     = GET /agent/trading/account
perpUSDC = snap.clearinghouseState.withdrawable
spotUSDC = snap.spotClearinghouseState.balances.find(b => b.coin === 'USDC')?.total ?? 0
mode     = snap.userAbstraction

if perpUSDC > 0 and mode in ("default", "disabled"):
  POST /agent/trading/abstraction { abstraction: "u" }   # one-shot

unifiedFreeUSDC = perpUSDC + spotUSDC
```

Skip the abstraction call when `perpUSDC === 0` and `spotUSDC > 0` —
the wallet is already unified. If `unifiedFreeUSDC >= required`, just
place the order. If short, walk the funding ladder in
`openfin-hyperliquid` (bridge → onramp).

**Counter-examples seen:**

- Agent reads `withdrawable = $0`, ignores spot ($18.98 USDC sitting
  there), tells the user to onramp. Wrong — sum both first.
- Agent sees `"default"` abstraction with USDC on both sides, treats
  them as one balance, order fails. Wrong — upgrade to `unifiedAccount`
  first.

### Withdrawal not arriving on Arbitrum

Expected. `POST /withdraw` → `withdraw3` finalizes in ~5 minutes once
L1 validators co-sign; flat $1 fee deducted. After ~10 minutes,
delays are Hyperliquid-side — direct user to Hyperliquid's Discord,
not OpenFinance.

### `Order rejected: price out of bounds`

Price bands ~5–10% from mid. Read mid via `GET /market/mids` and stay
in-band; cross the book aggressively but inside the band.

### WebSocket data stale

Backend maintains a shared connection and auto-reconnects after 3s.
The first few messages post-reconnect can be missing — retry the read.
Persistent issue = outbound WS broken on the server host.

## General

1. **Check `GET /agent/wallets` first** when anything auth-related
   fails — tells you which chains are provisioned. Missing chain →
   openfinance.tech to complete setup.
2. **On-chain state != CLOB / Relay state.** Approvals can show
   on-chain but report 0 upstream from token/spender mismatches.
   Don't trust "on-chain says X" without checking the service.
3. **Read errors verbatim** — `Custom:101` vs `Custom:6000` map to
   exactly one fix each. Don't paraphrase before looking up.
