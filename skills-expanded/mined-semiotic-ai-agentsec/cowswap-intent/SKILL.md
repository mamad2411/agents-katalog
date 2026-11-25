---
name: cowswap-intent
description: Submit a CoW Protocol intent — sign an EIP-712 Order, post to api.cow.fi, solver settles. Off-chain only until settlement; uses Permit2 for token approval. Soft-cancel via API. Use when the user wants gasless or batched MEV-protected swaps.
---

# cowswap-intent — submit an intent-based swap (off-chain signed)

## When to use

User explicitly asked to swap tokens with MEV protection or no upfront gas.
CoW Protocol orders are **intents**, not transactions: the user signs an
EIP-712 Order off-chain, the solver settles it on-chain. The signer never
broadcasts a tx.

## Required environment

```bash
export PRIVATE_KEY=0x...                    # the signer
export COW_API="https://api.cow.fi/mainnet" # or /xdai, /arbitrum_one, /base, /sepolia
```

The signer's address is `owner` — they receive `buyToken`, pay `sellToken`.

## Procedure

### Step 1 — Quote

```bash
sellToken="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"   # USDC mainnet
buyToken="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"    # WETH mainnet
sellAmount="1000000000"                                    # 1000 USDC (6 decimals)
owner=$(cast wallet address --private-key "$PRIVATE_KEY")

quote=$(curl -sS -X POST "${COW_API}/api/v1/quote" \
  -H 'Content-Type: application/json' \
  -d "{
    \"sellToken\": \"${sellToken}\",
    \"buyToken\": \"${buyToken}\",
    \"sellAmountBeforeFee\": \"${sellAmount}\",
    \"from\": \"${owner}\",
    \"kind\": \"sell\",
    \"signingScheme\": \"eip712\"
  }")

buyAmount=$(echo "$quote" | jq -r '.quote.buyAmount')
feeAmount=$(echo "$quote" | jq -r '.quote.feeAmount')
quoteId=$(echo "$quote" | jq -r '.id')

echo "$quote" | jq '{
  buyAmount: .quote.buyAmount,
  feeAmount: .quote.feeAmount,
  expiration: .expiration
}'
```

### Step 2 — Confirm with the user

Show the buy amount, fee, and expiration. Ask "shall I proceed?". Do not
continue until they say yes.

### Step 3 — Sign Permit2 typed-data

CoW Protocol uses Permit2 via the GPv2VaultRelayer. The relayer at
`0xC92E8bdf79f0507f65a392b0ab4667716BFE0110` is the spender; sign a Permit2
`PermitTransferFrom` so the solver can pull `sellToken` at settlement.

```bash
relayer="0xC92E8bdf79f0507f65a392b0ab4667716BFE0110"

cat > /tmp/permit2.json <<EOF
{
  "types": {
    "EIP712Domain": [
      {"name": "name", "type": "string"},
      {"name": "chainId", "type": "uint256"},
      {"name": "verifyingContract", "type": "address"}
    ],
    "PermitTransferFrom": [
      {"name": "permitted", "type": "TokenPermissions"},
      {"name": "spender", "type": "address"},
      {"name": "nonce", "type": "uint256"},
      {"name": "deadline", "type": "uint256"}
    ],
    "TokenPermissions": [
      {"name": "token", "type": "address"},
      {"name": "amount", "type": "uint256"}
    ]
  },
  "domain": {
    "name": "Permit2",
    "chainId": 1,
    "verifyingContract": "0x000000000022D473030F116dDEE9F6B43aC78BA3"
  },
  "primaryType": "PermitTransferFrom",
  "message": {
    "permitted": {"token": "${sellToken}", "amount": "${sellAmount}"},
    "spender": "${relayer}",
    "nonce": "0",
    "deadline": "$(($(date +%s) + 3600))"
  }
}
EOF

permit2Sig=$(cast wallet sign-typed-data --private-key "$PRIVATE_KEY" --data-file /tmp/permit2.json)
```

### Step 4 — Sign the Order typed-data

The Order is the heart of a CoW intent. Default `validTo` is one hour out so
the solver has plenty of time to settle. `partiallyFillable: false` keeps the
order all-or-nothing.

```bash
validTo=$(($(date +%s) + 3600))   # default: now + 1 hour
appData="0x0000000000000000000000000000000000000000000000000000000000000000"

cat > /tmp/order.json <<EOF
{
  "types": {
    "EIP712Domain": [
      {"name": "name", "type": "string"},
      {"name": "version", "type": "string"},
      {"name": "chainId", "type": "uint256"},
      {"name": "verifyingContract", "type": "address"}
    ],
    "Order": [
      {"name": "sellToken", "type": "address"},
      {"name": "buyToken", "type": "address"},
      {"name": "receiver", "type": "address"},
      {"name": "sellAmount", "type": "uint256"},
      {"name": "buyAmount", "type": "uint256"},
      {"name": "validTo", "type": "uint32"},
      {"name": "appData", "type": "bytes32"},
      {"name": "feeAmount", "type": "uint256"},
      {"name": "kind", "type": "string"},
      {"name": "partiallyFillable", "type": "bool"},
      {"name": "sellTokenBalance", "type": "string"},
      {"name": "buyTokenBalance", "type": "string"}
    ]
  },
  "domain": {
    "name": "Gnosis Protocol",
    "version": "v2",
    "chainId": 1,
    "verifyingContract": "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
  },
  "primaryType": "Order",
  "message": {
    "sellToken": "${sellToken}",
    "buyToken": "${buyToken}",
    "receiver": "${owner}",
    "sellAmount": "${sellAmount}",
    "buyAmount": "${buyAmount}",
    "validTo": ${validTo},
    "appData": "${appData}",
    "feeAmount": "${feeAmount}",
    "kind": "sell",
    "partiallyFillable": false,
    "sellTokenBalance": "erc20",
    "buyTokenBalance": "erc20"
  }
}
EOF

orderSig=$(cast wallet sign-typed-data --private-key "$PRIVATE_KEY" --data-file /tmp/order.json)
```

### Step 5 — POST the order to api.cow.fi

```bash
postBody=$(jq -n \
  --arg sellToken "$sellToken" \
  --arg buyToken "$buyToken" \
  --arg owner "$owner" \
  --arg sellAmount "$sellAmount" \
  --arg buyAmount "$buyAmount" \
  --arg feeAmount "$feeAmount" \
  --arg appData "$appData" \
  --arg sig "$orderSig" \
  --arg quoteId "$quoteId" \
  --argjson validTo "$validTo" \
  '{
    sellToken: $sellToken,
    buyToken: $buyToken,
    receiver: $owner,
    sellAmount: $sellAmount,
    buyAmount: $buyAmount,
    validTo: $validTo,
    appData: $appData,
    feeAmount: $feeAmount,
    kind: "sell",
    partiallyFillable: false,
    sellTokenBalance: "erc20",
    buyTokenBalance: "erc20",
    signingScheme: "eip712",
    signature: $sig,
    from: $owner,
    quoteId: ($quoteId | tonumber)
  }')

orderUid=$(curl -sS -X POST "${COW_API}/api/v1/orders" \
  -H 'Content-Type: application/json' \
  -d "$postBody" | jq -r '.')

echo "Order UID: ${orderUid}"
```

### Step 6 — Poll for fill status (or soft-cancel)

```bash
# Poll the order endpoint until fulfilled or expired
curl -sS "${COW_API}/api/v1/orders/${orderUid}" | jq '{
  status: .status,
  executedSellAmount,
  executedBuyAmount,
  executedFeeAmount
}'

# Soft-cancel: tells the API to stop offering this order to solvers, but a
# solver that has already picked it up may still settle it on-chain.
curl -sS -X DELETE "${COW_API}/api/v1/orders/${orderUid}"
```

## Recurring orders (session keys)

For DCA / recurring buys, use the 1delta-style session-key pattern: sign
once with a long-lived `validTo` and let the agent re-post fresh orders
without bothering the user each time.

```bash
sessionValidTo=$(($(date +%s) + 86400 * 30))   # 30 days
# Persist (sellToken, buyAmount, validTo) and replay once per cron tick.
```

## Final report to the user

> "Order submitted. UID: `0x...`. Solver will settle within ~30s. I'll fetch
>  fill status if you want."

## Hard rules

- **Order is signed off-chain** — the signer pays no gas. Settlement is on
  the solver.
- **Soft-cancel is best-effort.** A solver that already pulled the order
  into a batch may still settle it on-chain. There is no on-chain cancel
  primitive; only the settlement contract's `setPreSignature(false)` works
  for `presign` scheme orders.
- **Never modify the typed-data** between sign and POST. The solver
  validates against the hash you signed.
