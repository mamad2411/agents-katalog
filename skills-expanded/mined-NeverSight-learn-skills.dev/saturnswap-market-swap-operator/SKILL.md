---
name: saturnswap-market-swap-operator
description: |
  OPERATOR SKILL — requires manual confirmation for every action.
  Use this skill to sign and submit market swap transactions on SaturnSwap.
  Triggers after saturnswap-market-swap has created an unsigned transaction.
  "sign swap", "submit swap transaction", "execute the swap", "confirm swap".
version: 1.0.0
---

# SaturnSwap Market Swap Operator

Sign and submit market swap transactions. This is an OPERATOR skill — every
action requires explicit user confirmation.

## Prerequisites

- An unsigned transaction from `saturnswap-market-swap` (transactionId + hexTransaction)
- A wallet signing key (PAYMENT_SKEY_HEX or PAYMENT_SKEY_CBOR env var, or MCP wallet)

## Flow

1. **Receive unsigned tx** from the guidance skill
2. **Sign locally** using CSL or MeshJS (never send private keys to the API)
3. **Confirm with user** — show tx ID and ask for explicit "submit" confirmation
4. **Submit** — call `submitOrderTransaction` with signed hex
5. **Report result** — show transaction ID or error

## Scripts

### Sign and Submit

```bash
node scripts/sign-and-submit.js --address <bech32> --txid <transactionId> --hex <unsignedHex>
```

Signs the transaction using the configured wallet key, then submits to SaturnSwap.

## Safety Rules

- **NEVER auto-submit** — always require explicit user confirmation before submission
- **NEVER log or display private keys**
- **Verify the transaction ID** matches what the user approved in the guidance step
- If signing fails, do NOT retry automatically — report the error
- After submission, report the on-chain transaction ID for verification
