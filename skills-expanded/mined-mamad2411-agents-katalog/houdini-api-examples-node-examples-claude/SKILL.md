# Houdini Swap — Node.js Integration Guide

This file gives AI assistants full context to build any backend integration with the Houdini Swap API using Node.js + TypeScript.

---

## Project Setup

```bash
yarn install
cp .env.example .env   # fill in your API key/secret
yarn run:standard      # test with a standard swap example
yarn run:private
yarn run:dex
```

**Stack:** Node.js 18+, TypeScript, Viem (for DEX wallet ops), dotenv

---

## Environment Variables

```env
HOUDINI_API_KEY=your_key
HOUDINI_API_SECRET=your_secret

# DEX swaps only
WALLET_PRIVATE_KEY=0x...

# Optional RPC overrides (defaults to public RPCs)
ETHEREUM_RPC_URL=
BASE_RPC_URL=
ARBITRUM_RPC_URL=
POLYGON_RPC_URL=
OPTIMISM_RPC_URL=
```

---

## Existing Utilities — Reuse These

### `src/helpers.ts`

```typescript
// Authenticated fetch to Houdini API
fetchFromHoudini<T>(endpoint: string, options: FetchOptions): Promise<T>

// Status helpers
getStatusName(code: number): string   // 0-8 → "WAITING", "COMPLETED", etc.
getHopStatus(code: number): string    // 1-5 for private swap hops
formatTime(isoString: string): string
sleep(ms: number): Promise<void>
```

### `src/wallet.ts` (DEX swaps only)

```typescript
createWallet(privateKey: Hex, chainId: number)  // returns { walletClient, publicClient, account, chain }
sendTransaction(walletClient, publicClient, params) // sign + broadcast + wait
estimateGas(publicClient, account, params)
getExplorerUrl(chainId, txHash)
validatePrivateKey(key: string): Hex
```

Supported chains: Ethereum (1), Base (8453), Arbitrum (42161), Polygon (137), Optimism (10).

### `src/types.ts`

All TypeScript types for every API request and response. Always import from here — never redefine types.

Key types: `QuoteResponse`, `SwapOrder`, `SwapStatus`, `DexQuoteResponse`, `DexApproveResponse`, `DexExchangeResponse`, `Signature`, `SignatureObject`, `SwapStatusCode`, `HopStatusCode`.

---

## API Reference

### Base URLs

- Swap API: `https://api-partner.houdiniswap.com`
- Token Search: `https://api-dev-partner.houdiniswap.com/v2`

### Authentication

Every request needs:
```
Authorization: API_KEY:API_SECRET
x-user-ip: <user IP>
x-user-agent: <user agent string>
x-user-timezone: America/New_York
```

`fetchFromHoudini()` handles all of this automatically.

---

### Token Search — `GET /v2/tokens`

```typescript
const res = await fetch('https://api-dev-partner.houdiniswap.com/v2/tokens?term=eth&pageSize=20', {
  headers: { Authorization: `${API_KEY}:${API_SECRET}` }
});
// { tokens: Token[], total: number, totalPages: number }
```

Each token has: `id`, `symbol`, `name`, `icon`, `chainData.shortName`, `chainData.name`, `price`, `hasDex`, `hasCex`.

---

### Quote — `GET /quote`

```typescript
const quote = await fetchFromHoudini<QuoteResponse>('/quote', {
  params: { from: 'ETH', to: 'USDC', amount: '1', anonymous: false }
});
// quote.amountOut, quote.quoteId, quote.duration
```

Set `anonymous: true` for a private (multi-hop) quote.

---

### Create Swap — `POST /exchange`

```typescript
const order = await fetchFromHoudini<SwapOrder>('/exchange', {
  method: 'POST',
  body: {
    amount: 1,
    from: 'ETH',
    to: 'USDC',
    addressTo: '0xRecipientAddress',
    receiverTag: '',       // memo/tag, leave empty unless token requires it
    anonymous: false,      // true = private swap
    ip: '192.168.1.1',
    userAgent: 'Mozilla/5.0...',
    timezone: 'America/New_York',
  }
});
// User must send order.inAmount of order.inSymbol to order.senderAddress
```

---

### Swap Status — `GET /status`

```typescript
const status = await fetchFromHoudini<SwapStatus>('/status', {
  params: { houdiniId: order.houdiniId }
});
```

**Status codes:**

| Code | Meaning |
|------|---------|
| 0 | WAITING — waiting for deposit |
| 1 | CONFIRMING |
| 2 | EXCHANGING |
| 3 | ANONYMIZING (private swaps) |
| 4 | COMPLETED ✓ |
| 5 | EXPIRED |
| 6 | FAILED |
| 7 | REFUNDED |
| 8 | DELETED |

Terminal states (stop polling): `>= 4`.

For private swaps, also track `status.inStatus` and `status.outStatus` (hop codes 1–5).

---

### DEX Quote — `GET /dexQuote`

```typescript
const quotes = await fetchFromHoudini('/dexQuote', {
  params: { tokenIdFrom, tokenIdTo, amount, slippage: 0.5 }
});
// Array of { swap, amountOut, quoteId, route }
// swap values: "un" = Uniswap, "cs" = CowSwap, "su" = SushiSwap, etc.
```

---

### DEX Approve — `POST /dexApprove`

Returns approvals (ERC-20 allowance txs) and signatures (EIP-712) needed before the swap.

```typescript
const { approvals, signatures } = await fetchFromHoudini<DexApproveResponse>('/dexApprove', {
  method: 'POST',
  body: { tokenIdFrom, tokenIdTo, amount, addressFrom, swap, route }
});

// 1. Broadcast each approval tx with sendTransaction()
// 2. Sign each signature with walletClient.signTypedData()
```

---

### DEX Exchange — `POST /dexExchange`

```typescript
const exchange = await fetchFromHoudini<DexExchangeResponse>('/dexExchange', {
  method: 'POST',
  body: {
    tokenIdFrom, tokenIdTo, amount, addressFrom, addressTo,
    route, swap, quoteId,
    signatures: collectedSignatures,   // from signTypedData
    destinationTag: '',
    deviceInfo: 'web', isMobile: false, walletInfo: 'MetaMask',
    slippage: 0.5,
  }
});

if (exchange.metadata.offChain) {
  // CowSwap: no tx needed, Houdini handles it
} else {
  const { hash } = await sendTransaction(walletClient, publicClient, {
    to: exchange.metadata.to as Hex,
    data: exchange.metadata.data as Hex,
    value: BigInt(exchange.metadata.value || '0'),
    account, chain,
  });
  await fetchFromHoudini('/dexConfirmTx', {
    method: 'POST',
    body: { houdiniId: exchange.houdiniId, txHash: hash }
  });
}
```

---

## Swap Flow Patterns

### Standard / Private swap

```typescript
// 1. Quote
const quote = await fetchFromHoudini<QuoteResponse>('/quote', {
  params: { from, to, amount, anonymous }
});

// 2. Create order
const order = await fetchFromHoudini<SwapOrder>('/exchange', {
  method: 'POST',
  body: { amount: parseFloat(amount), from, to, addressTo, receiverTag: '', anonymous, ip, userAgent, timezone }
});

console.log(`Send ${order.inAmount} ${order.inSymbol} to ${order.senderAddress}`);

// 3. Poll status
for (let i = 0; i < 180; i++) {
  const s = await fetchFromHoudini<SwapStatus>('/status', { params: { houdiniId: order.houdiniId } });
  if (s.status >= 4) break;
  await sleep(10_000);
}
```

### DEX swap (full flow)

See `examples/dex-swap-example.ts` for the complete working implementation including:
- Multi-provider quote selection
- ERC-20 approval broadcasting
- EIP-712 signing (including chained signatures for some providers)
- Transaction broadcasting with Viem
- Off-chain order handling (CowSwap)

---

## Adding New Scripts

Follow the pattern in `examples/standard-swap-example.ts`:
1. Import from `../src/helpers` and `../src/types`
2. Define a `CONFIG` object at the top
3. Write an `async function main()` and call it at the bottom
4. Add a script to `package.json`: `"run:myexample": "ts-node examples/my-example.ts"`
