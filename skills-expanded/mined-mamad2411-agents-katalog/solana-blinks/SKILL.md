---
name: solana-blinks
description: Build Solana Actions and Blinks for in-app transactions on X and other clients. Triggers on "Blinks", "Solana Actions", "shareable transaction", "X Money", "Dialect".
---

# Solana Blinks & Actions Builder

Build [Solana Actions](https://solana.com/developers/guides/advanced/actions) — API endpoints that return transaction previews — and wrap them as [Blinks](https://www.dialect.to/) that render natively inside X (Twitter), Phantom, and other supporting clients. Users execute on-chain transactions without leaving the app.

## Why this matters now

X Money launched in April 2026 with native Blinks support via Dialect. Every Solana app can now reach X's entire user base through shareable transaction URLs. This is the biggest distribution unlock in crypto — your swap, mint, payment, or vote becomes a one-tap action inside a tweet.

## When to use this skill

- "Create a Blink for my token swap"
- "I want users to mint from a tweet"
- "Build a Solana Action endpoint"
- "Make my dApp shareable on X"
- "Set up tipping / payments via Blinks"
- Any project that needs shareable on-chain transactions

## Core concepts

### Solana Actions
An Action is an API endpoint that:
1. Returns metadata (title, description, icon, action buttons)
2. Accepts a user's public key
3. Returns an unsigned transaction for the user to sign

### Blinks (Blockchain Links)
A Blink is a URL that unfurls into an interactive transaction card when shared on X, Phantom, or other Blink-aware clients. The client fetches the Action API, renders the preview, and handles wallet signing.

## Build mode workflow

### Step 1 — Define the action

Ask the founder:
1. **What on-chain action?** (swap, transfer, mint NFT, vote, stake, tip, donate)
2. **What parameters does the user choose?** (amount, token, recipient, option)
3. **Is it a single action or a multi-step flow?** (single transaction vs. chained actions)
4. **Where will it be shared?** (X/Twitter, Phantom, Discord, embedded in website)
5. **Any access control?** (public, token-gated, allowlist)

### Step 2 — Scaffold the Actions API

```
solana-blinks/
├── src/
│   ├── actions/
│   │   └── swap.ts           # Action endpoint (GET metadata + POST transaction)
│   ├── utils/
│   │   ├── transaction.ts    # Transaction building helpers
│   │   └── validation.ts     # Input validation
│   └── index.ts              # Route setup
├── actions.json              # Action manifest (served at /.well-known/actions.json)
├── .env.example
└── package.json
```

### Step 3 — Implement the Action endpoint

**GET** returns action metadata:
```json
{
  "title": "Swap SOL → USDC",
  "icon": "https://yourapp.com/icon.png",
  "description": "Swap SOL for USDC at the best rate",
  "label": "Swap",
  "links": {
    "actions": [
      { "label": "Swap 0.1 SOL", "href": "/api/swap?amount=0.1" },
      { "label": "Swap 1 SOL", "href": "/api/swap?amount=1" },
      {
        "label": "Custom amount",
        "href": "/api/swap?amount={amount}",
        "parameters": [{ "name": "amount", "label": "SOL amount" }]
      }
    ]
  }
}
```

**POST** receives the user's public key and returns an unsigned transaction:
```json
{
  "transaction": "<base64-encoded-transaction>",
  "message": "Swapping 1 SOL for USDC"
}
```

### Step 4 — Register with Dialect

1. Serve `actions.json` at `https://yourdomain.com/.well-known/actions.json`
2. Register your domain with the [Dialect Blinks Registry](https://dial.to/register) for verified status
3. Verified Blinks render automatically on X and in Phantom; unverified ones require user opt-in

### Step 5 — Test end-to-end

1. Test locally with the [Blinks Inspector](https://dial.to/)
2. Verify the Action returns valid transactions on devnet
3. Share a Blink URL on X and confirm it renders correctly
4. Test the full sign → submit → confirm flow

## Hard rules

1. **actions.json must be served at the well-known path.** Clients look for `/.well-known/actions.json` to discover your Actions.
2. **Transactions must be unsigned.** The Action API returns transactions for the user's wallet to sign. Never sign server-side on behalf of users.
3. **Validate all inputs server-side.** Don't trust parameters from the URL — validate amounts, addresses, and options before building the transaction.
4. **Set transaction deadlines.** Use `recentBlockhash` with appropriate `lastValidBlockHeight` to prevent stale transactions.
5. **CORS headers are required.** Blink clients fetch from different origins. Set `Access-Control-Allow-Origin` appropriately.
6. **Icon must be a direct image URL.** Not a page that contains an image — a direct PNG/SVG/WebP URL that renders as an image.

## Common Blink patterns

| Pattern | Description |
|---------|-------------|
| **Token swap** | User picks amount, Action builds a Jupiter/Raydium swap transaction |
| **NFT mint** | One-tap mint from a tweet, optional quantity parameter |
| **Tipping** | Send SOL/USDC to a creator, preset amounts + custom |
| **Voting / polling** | Choose an option, Action records vote on-chain |
| **Donation** | Send to a treasury address, shows running total |
| **Token-gated access** | Check token ownership before returning the transaction |

## Reference links

- [Solana Actions & Blinks guide](https://solana.com/developers/guides/advanced/actions)
- [Dialect Blinks](https://www.dialect.to/)
- [Blinks Inspector (test your Blinks)](https://dial.to/)
- [X Money + Solana integration](https://digitalmoneytimes.com/2026/04/15/x-deploys-solana-infrastructure-for-live-financial-data-integration/)
- [Actions specification](https://github.com/solana-developers/solana-actions)
