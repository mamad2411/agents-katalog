---
name: openfin-relay
description: Cross-chain bridging, swapping, and "bridge+call" via Relay through the OpenFinance backend. Use whenever the user wants to move tokens between chains or execute a destination-chain transaction funded from another chain. Triggers&#58; "bridge X from Y to Z", "move my USDC to Base / Arbitrum / Optimism / Polygon / Solana", "swap ETH for USDC on Base", "cross-chain swap", "bridge and call", "how do I get to Solana / back from Solana", "my USDC is stuck on Solana", EVM-to-EVM, EVM-to-Solana, Solana-to-EVM, Bitcoin bridge, gas topup on destination, native-token sentinel 0x0, relay quote/preview/execute flow, poll intent status. Covers POST /agent/relay/quote, POST /agent/relay/execute, GET /agent/relay/status. Includes the chainId cheatsheet (1/137/8453/10/42161/... and Solana 792703809 specifically), tradeType semantics (EXACT_INPUT / EXACT_OUTPUT / EXPECTED_OUTPUT), why topupGas is auto-disabled on Solana routes, the Solana wallet delegation requirement for Solana-origin execute, and bridge+call payloads (txs array). Use together with openfin-setup (API key check) and openfin-troubleshooting (Blockhash not found, Custom:101, 412 delegation).
---

# Relay Bridging

Playbook for bridging, swapping, and bridge+calling via Relay through OpenFinance.

## Three operations, one API

| Operation | What it is |
|---|---|
| **Swap** | Same-chain token swap (origin = destination chain) |
| **Bridge** | Move tokens across chains (USDC on Polygon → USDC on Base) |
| **Bridge+call** | Bridge + execute a destination-chain tx after the bridge lands — pass the tx(s) in `txs` |

Relay picks the route automatically; you just provide the inputs.

## Endpoints

All three require `x-api-key: open_…`. Relay aggregates liquidity across 40+
chains — you pass the chain IDs directly; the backend picks the route.

### `POST /agent/relay/quote` — quote only

Fetches a Relay quote for a swap, bridge, or bridge+call. Does NOT submit
any transactions. Use for preview UIs, fee estimation, or to show the user
the route before they confirm.

Request body:
```json
{
  "originChainId": 137,
  "destinationChainId": 8453,
  "originCurrency": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
  "destinationCurrency": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "amount": "10000000",
  "tradeType": "EXACT_INPUT",
  "recipient": "...",               // optional; defaults to user's dest-chain addr
  "slippageTolerance": "50",        // basis points, optional
  "topupGas": true,                 // optional; forced false for Solana routes
  "topupGasAmount": "100000",       // USD micro-units, optional
  "usePermit": false,               // EIP-3009 permit for supported tokens
  "txs": [{"to", "data", "value"}], // optional; for bridge+call
  "appFees": [{"recipient", "fee"}] // optional
}
```

`user` is server-injected from the caller's wallet based on `originChainId`
— do NOT pass it. The backend selects EVM or Solana address automatically.

Returns the full response: `{steps, fees, feeSponsorship}`. `steps` is an
array of signable/submittable actions (transactions or signatures) with
embedded `check` endpoints for status polling.

### `POST /agent/relay/execute` — quote + sign + submit + poll

End-to-end flow. Same body as `/quote`. The backend:

1. Fetches the quote
2. Walks every `step`:
   - **EVM transaction step** → sends via viem `walletClient.sendTransaction`
     on the correct chain, waits for 1 confirmation
   - **Solana transaction step** → compiles `instructions` + ALTs into a
     VersionedTransaction, has Privy sign it (`signTransaction`), broadcasts
     via our RPC with `skipPreflight: true`, confirms with the original
     blockhash/lastValidBlockHeight
   - **EIP-712 signature step** → signs with the user's EVM account and
     POSTs the signature to the step's `check.endpoint`
3. Polls `GET /intents/status/v3` with exponential backoff (1s → 10s, 5-min
   cap) until terminal status

Returns `{requestId, quote, txHashes, finalStatus}`.

Use when the user confirms the quote or directly asks to bridge / swap /
execute. Solana-origin requires the user's Solana wallet to be delegated
(see `openfin-setup` step 2).

### `GET /agent/relay/status?requestId=<id>` — manual status lookup

Get the current status of a Relay intent by its `requestId`. Use for
manual polling from the frontend when `/execute` wasn't awaited, or for
audit lookups.

**Status values:**
- `waiting` — awaiting deposit confirmation
- `depositing` — origin deposit confirmed, pending fill
- `pending` — deposit confirmed, awaiting destination submission
- `submitted` — destination transaction submitted
- `delayed` — destination fill still processing
- **`success`** — successful fill on destination (terminal)
- **`refunded`** — successfully refunded (terminal)
- **`failure`** — unsuccessful fill (terminal)

Response also includes `details` (free-form text), `inTxHashes`, `txHashes`,
`updatedAt` (ms), `originChainId`, `destinationChainId`.

## Required inputs

| Field | Type | Notes |
|---|---|---|
| `originChainId` | number | Source chain |
| `destinationChainId` | number | Destination chain |
| `originCurrency` | string | Token contract on origin (or `0x0…0` for EVM native) |
| `destinationCurrency` | string | Token contract on destination |
| `amount` | string | Smallest unit as a STRING (wei for 18-dec, `10000000` = 10 USDC) |
| `tradeType` | string | `EXACT_INPUT` \| `EXACT_OUTPUT` \| `EXPECTED_OUTPUT` |

**`user` is server-injected** based on `originChainId` — pass the right wallet
for the origin. Solana origin → Solana address; EVM origin → EVM address.
Do not pass it yourself.

**`recipient` defaults** to the user's address on the **destination chain**.
Override explicitly if bridging to a different address.

## Chain ID cheatsheet

| Chain | ID |
|---|---|
| Ethereum | `1` |
| Polygon | `137` |
| Base | `8453` |
| Optimism | `10` |
| Arbitrum | `42161` |
| BSC | `56` |
| Linea | `59144` |
| Blast | `81457` |
| Scroll | `534352` |
| zkSync Era | `324` |
| Hyperliquid | `1337` |
| **Solana** | **`792703809`** |
| Bitcoin | `8253038` |
| Tron | `728126428` |

Live list: `GET https://api.relay.link/chains`.
Treat that endpoint as source of truth for supported **origin** chains.

## Native-token sentinel

Use `0x0000000000000000000000000000000000000000` for the EVM native token
on any EVM chain (ETH / MATIC / BNB / etc.).

For Solana, use `So11111111111111111111111111111111111111112` for wrapped
SOL, or the SPL mint address for tokens (e.g.
`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` for USDC).

## Trade types

| Type | Meaning | Example |
|---|---|---|
| `EXACT_INPUT` | Send exactly `amount`, receive variable | "Bridge 10 USDC" |
| `EXACT_OUTPUT` | Send variable, receive exactly `amount` | "Get me exactly 1 ETH on Base" |
| `EXPECTED_OUTPUT` | Alternate routing | Rarely needed |

Most prompts are `EXACT_INPUT`. If user says "I want to receive X", use `EXACT_OUTPUT`.

## Gas topup defaults

Backend behavior:
- **EVM ↔ EVM**: `topupGas: true` default, `topupGasAmount: "100000"` ($0.10).
  Relay only applies it if the recipient needs gas.
- **Any route with Solana (chainId `792703809`)**: `topupGas` forced `false`.
- Ethereum L1 destination: bump `topupGasAmount` to `"500000"` ($0.50).

Override per-call via body fields `topupGas` and `topupGasAmount`.

## Solana-origin example

Bridge the user's USDC from Solana back to USDC.e on Polygon:

```json
{
  "originChainId": 792703809,
  "destinationChainId": 137,
  "originCurrency": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "destinationCurrency": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
  "amount": "1000000",
  "tradeType": "EXACT_INPUT"
}
```

`user` auto-fills as the user's Solana address; `recipient` auto-fills as
their EVM address. **Requires Solana wallet delegation** (see
`openfin-setup`). Without it, execute fails with 412.

## Bridge+call example

Bridge USDC.e Polygon → USDC Base, then call a contract on Base:

```json
{
  "originChainId": 137,
  "destinationChainId": 8453,
  "originCurrency": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
  "destinationCurrency": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "amount": "10000000",
  "tradeType": "EXACT_INPUT",
  "txs": [
    { "to": "0x…target…", "data": "0x…calldata…", "value": "0" }
  ]
}
```

## Status values

- **Terminal success:** `success`, `refunded`
- **Terminal failure:** `failure`
- **In-flight:** `waiting`, `depositing`, `pending`, `submitted`, `delayed`

If `/execute` returns non-terminal `finalStatus`, keep polling `/status`
with the `requestId`.

## Don't

- Don't use human-readable amounts. `"1000000"` = 1 USDC, not `"1"`.
- Don't pass `user` or `userId` — server injects.
- Don't retry a `failure` without checking `details` — refund may be automatic
  (`status: refunded` will follow), or the route may be unsupported.
- Don't assume Solana delegation carries over from EVM. Each chain type
  delegates separately in Privy.

## MCP note

Tool names match: `relay_get_quote`, `relay_execute`, `relay_get_status`.
