---
name: treasures-b2b-api
description: Use to build an AI agent on the Treasures public B2B API — discover tokenized stocks, quote/execute trades, bridge USDC across Solana and Ethereum, and read portfolio + trade history for a single end-user wallet pair. Covers endpoint selection, ownership-proof signing (incl. embedded wallets), trade/bridge execution, and error handling.
metadata:
  version: "1.0.0"
tags:
  - treasures
  - b2b-api
  - tokenized-stocks
  - solana
  - ethereum
  - trading
  - bridge
  - usdc
  - ownership-proof
---

# Treasures B2B API — Agent Skill

Guide for AI agents (and any non-human caller) using the Treasures public B2B API to discover tokenized stocks, quote + execute trades, bridge USDC across chains, and read portfolio + trade history on behalf of a single end-user wallet pair.

- **Base URL:** `https://api.treasures.io`
- **Network:** staging trades against **Ethereum mainnet + Solana mainnet-beta** (real funds, not a testnet) — point your own RPCs at mainnet; the token/contract addresses in this skill are mainnet.
- **Content type:** `application/json`
- **Wire format:** all token amounts, USDC, shares, prices, and bps-derived decimals are **strings** (avoid JS float drift). Integer fields (`expires_at`, `*_bps`, `quote_index`) are JSON numbers. Never round-trip a money value through JS `number`.

This entry doc is the map + the footguns. **It is not enough on its own to execute a trade** — full schemas, signing code, and error tables live in the references below. **Load the reference for the task before you act; you don't need to read them all.**

> **Schema-of-record:** an OpenAPI spec (`openapi.yaml`) is published alongside this skill in the same repository. This skill is self-sufficient for normal use — consult the spec only for exhaustive field-level validation or client codegen; you don't need to read it to operate.

## Reference index

| Load this                                          | When you're…                                                                                                |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [`references/auth.md`](references/auth.md)         | building the `ownership_proof` (esp. on embedded/managed Solana wallets)                                    |
| [`references/trading.md`](references/trading.md)   | quoting/submitting a buy or sell, signing trade legs, polling quote status, or setting first-time approvals |
| [`references/bridging.md`](references/bridging.md) | bridging USDC between chains (incl. the `nonce=0` EVM trap)                                                 |
| [`references/data.md`](references/data.md)         | reading `/stocks/*`, `/portfolio`, or `/trades`                                                             |
| [`references/errors.md`](references/errors.md)     | handling an error code, rate limits, or simulating a tx before broadcast                                    |

## TL;DR — happy path

```
1. GET   /stocks/tickers              → supported tickers + token addresses
2. GET   /stocks/prices?tickers=AAPL  → live price snapshot
3. ONE-TIME: set ERC-20 allowances on Ethereum (see traps below)  ← CRITICAL
4. POST  /quote/buy   (or /sell)      → quote(s) + signable payload(s)
5. Sign each signable_payload with the matching wallet key
6. POST  /trade/submit                → broadcast
7. GET   /quote/{quote_id}/status     → poll until terminal
8. GET   /portfolio                   → reconciled holdings
```

Need cross-chain USDC first? Insert a bridge between steps 2 and 4: `POST /bridge/quote` → sign + broadcast it yourself → `GET /bridge/{id}/status` until `completed` or `failed`. See [`references/bridging.md`](references/bridging.md).

## Before your first call — pre-flight traps

These cause silent or first-time-only failures. Handle them up front.

**1. Ethereum ERC-20 approvals are required before any transfer.** The API does **not** broadcast approvals for you; set them once per `(token, spender)` from the user's wallet, or your first Eth sell/bridge fails (`not_enough_balance_or_allowance` / silent forever-pending bridge). Solana has no allowances — skip on `sol` legs.

| Flow                    | Approve                                                         | Spender                                                                                 |
| ----------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Eth buy (USDC → stock)  | USDC `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`               | settlement `0x111111125421ca6dc452d289314280a0f8842a65`                                 |
| Eth sell (stock → USDC) | each protocol's stock token (per ticker — a sell may span both) | settlement (same)                                                                       |
| `eth → sol` bridge      | USDC                                                            | `signable_payload.approval_spender` from the bridge quote (non-null on the normal flow) |

Set `allowance = max-uint256` once. Approve code + the `approval_spender` null/non-null rule: [`references/trading.md`](references/trading.md#first-time-approvals).

**2. Hold the input token on the chain you trade.** A buy spends **USDC on the chosen chain**; a sell spends the **stock token**. The server pre-checks _sell_ holdings (insufficient → `422 holdings_insufficient` at quote time) but does **NOT** pre-check _buy_ USDC — an underfunded buy passes `/quote/buy` **and** `/trade/submit`, then the on-chain swap fails at the end (`broadcast_failed` / `not_enough_balance_or_allowance`), wasting the whole flow. **Verify USDC before quoting**: read the wallet, or call `GET /portfolio` (`usdc.{sol, eth}`). Need USDC on the other chain? Bridge first.

**3. Native gas: Treasures does not subsidize it.** Any operation your key broadcasts needs native balance on that chain. Eth buys/sells are gasless (the execution venue pays), but approvals + bridge broadcasts cost ETH; all Solana txs cost SOL. Keep ≥ **0.02 SOL** and ≥ **0.01 ETH** floats. Detail: [`references/errors.md`](references/errors.md#gas).

**4. The EVM bridge tx ships with `nonce=0`.** You MUST inject the wallet's real nonce before signing or broadcast is rejected ("nonce too low"). Most common bridge footgun — see [`references/bridging.md`](references/bridging.md#evm-sign-broadcast).

**5. Solana ownership proof is base64, NOT base58.** Privy/Turnkey quickstarts show base58 (`bs58.encode`) — that's the #1 cause of `ownership_proof_sol_invalid`. See [`references/auth.md`](references/auth.md#embedded-wallets).

## Auth essentials

Three endpoints require an `ownership_proof`: `POST /quote/buy`, `POST /quote/sell`, and `POST /bridge/quote` (**both** `sol_signature` + `eth_signature` mandatory on bridge — it spans both chains). Everything else is unauthenticated; `/trade/submit` is gated by the per-leg signed payload itself.

Sign this exact UTF-8 byte string (lines joined with `\n`) with each wallet's key:

```
treasures-finance-quote-v1
{issued_at}
{sol_wallet|""}
{eth_wallet|""}
```

- `eth_wallet` **must be lowercased** in the challenge. Empty string (not `null`/omitted) for a side you didn't supply. No extra fields — schema is `.strict()`.
- `sol_signature`: **base64** raw Ed25519 over the challenge bytes. `eth_signature`: `0x` 65-byte **EIP-191 `personal_sign`** (not EIP-712).
- **Validity:** `issued_at` is unix seconds; accepted in `[now − 300s, now + 30s]`, else `401 ownership_proof_skewed`. One proof is reusable within that window (no nonce store) — a both-wallets proof works on all three endpoints; a single-wallet proof on `/quote/*` only (bridge needs both signatures).

Signing code, all-or-nothing per-proof rules, embedded-wallet troubleshooting, and deterministic test vectors: [`references/auth.md`](references/auth.md).

## Critical contracts — read before trading

- **`broadcast_unknown` → do NOT retry.** Lost upstream response; the order may have landed. Poll `/quote/{id}/status` (or `/trades`) to confirm on-chain outcome before re-quoting. Retrying risks a double-fill.
- **Slippage bounds:** `max_slippage_bps` ∈ `[10, 5000]` for `/quote/*`, `[10, 500]` for `/bridge/*`. Out of range → `400 invalid_slippage` (response echoes the cap).
- **Quote TTLs are tight** (~25–55s for trades, ~30s bridge). If sign+submit takes longer than `expires_at − 5s`, expect `410 quote_stale` — re-quote.
- **Buy = pick ONE `quote_index`; sell = submit ALL of them.** Buy with >1 leg → `400 quote_index_mismatch`; sell subset → `400 incomplete_submit`.
- **Must-handle errors** (full matrix + backoff policy in [`references/errors.md`](references/errors.md)):

| HTTP      | `error`                                                                       | Action                                                        |
| --------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------- |
| 403       | `address_blocked`                                                             | Wallet tied to a sanctioned entity — do not retry that wallet |
| 410 / 404 | `quote_stale` / `quote_not_found`                                             | Re-quote                                                      |
| 422       | `holdings_unknown` / 502 `provider_unavailable` / 503 `screening_unavailable` | Transient — backoff policy B, cap 5 attempts                  |
| 429       | `Too many requests`                                                           | Honor `Retry-After` (delta-seconds)                           |

## Endpoint index

| Endpoint                                         | Auth                                | Method |
| ------------------------------------------------ | ----------------------------------- | ------ |
| `/stocks/tickers` · `/stocks/prices?tickers=…`   | none                                | GET    |
| `/quote/buy` · `/quote/sell`                     | `ownership_proof`                   | POST   |
| `/quote/{quote_id}/status`                       | none                                | GET    |
| `/trade/submit`                                  | signed payload (per leg)            | POST   |
| `/bridge/quote`                                  | `ownership_proof` (both signatures) | POST   |
| `/bridge/{bridge_quote_id}/status`               | none                                | GET    |
| `/portfolio?sol_wallet=&eth_wallet=&source=`     | none                                | GET    |
| `/trades?sol_wallet=&eth_wallet=&limit=&offset=&source=` | none                        | GET    |
