---
name: openfin-setup
author: OpenFinance
homepage: https://openfinance.tech
license: Proprietary
version: 1.0.1
description: Auth check for the OpenFinance backend — confirms an API key is available before any other OpenFinance skill runs. Use FIRST whenever the user is about to call any /agent/* route (Polymarket, Hyperliquid, Relay), is hitting 401/412, or hasn't traded yet in this session. Triggers on "how do I get started", "API key is required", "Invalid API key", "401/412 from /agent/*", "set up OpenFinance", or any first call into a trading skill. Resolves the key from `OPENFINANCE_API_KEY` (or equivalent env / user-supplied value), confirms the format (`open_…`), verifies via GET /agent/wallets, and otherwise points the user to https://openfinance.tech to issue one.
---

# OpenFinance Setup

> **Publisher.** Part of the OpenFinance skill bundle (openfin-setup, openfin-troubleshooting, openfin-hyperliquid, openfin-relay, openfin-onramp, openfin-polymarket, openfin-onchain) — all maintained by OpenFinance (https://openfinance.tech). Install as a set, not individually.

Agents only need one thing to use the OpenFinance backend: a valid API key.
Account and wallet setup happen out-of-band on openfinance.tech — by
the time an agent is involved, the user already has (or needs) a key.

## Step 1 — Locate the API key

Check, in order:

1. Env var `OPENFINANCE_API_KEY` (preferred).
2. Any project-level config the agent already has loaded (`.env`, secrets
   manager, MCP config, etc.).
3. The current conversation — the user may have pasted it.

A valid key looks like `open_` followed by an opaque token.

## Step 2 — If no key, ask

If none of the above turns up a key, ask the user **once**:

> I need an OpenFinance API key (`open_…`) to call the backend. If you
> already have one, paste it here. If not, generate one at
> [openfinance.tech](https://openfinance.tech) and paste it back.

Do **not** invent, guess, or proceed without one. Do not echo the key back
in chat once received — store it for the session and use it in headers.

## Step 3 — Verify

One call confirms the key works and the wallets are provisioned:

```http
GET /agent/wallets
x-api-key: open_…
```

Expected:

```json
{ "ethereum": "0x…", "solana": "…" }
```

- Either field may be `null` if that chain isn't provisioned for the user
  on openfinance.tech. Read-only and same-chain EVM flows still work; only
  Solana-origin Relay executes need the Solana wallet.
- `401 Invalid API key` → key is wrong or malformed; ask again or send the
  user back to openfinance.tech.
- `412 Server is not authorized for this user` → the user signed up but
  hasn't completed setup on openfinance.tech. Send them there.

## Auth header on every call

All `/agent/*` routes (except public Polymarket reads) take:

```http
x-api-key: open_…
```

`Authorization: Bearer open_…` also works if the framework prefers Bearer.

## MCP equivalent

The same wallet check via the MCP tool: `get_wallet_addresses` (no args
needed when the MCP host has `apiKey` configured at server level).
Returns `{ ethereum, solana }`.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `401 Invalid API key` | Key not sent, malformed, or revoked | Confirm `open_` prefix; reissue at openfinance.tech |
| `412 Server is not authorized for this user` | User signed up but didn't finish setup | Send user to openfinance.tech to complete setup |
| `400 User has no Solana wallet provisioned` | Solana wallet not enabled for the user | User enables Solana wallet on openfinance.tech |

## What NOT to do

- **Don't ship the raw API key into LLM context or logs.** Pass it through
  headers only.
- **Don't regenerate the key per call.** It's long-lived — cache for the
  session.
- **Don't try to onboard the user yourself.** Account and wallet
  setup happens on openfinance.tech, not via the agent.
