---
name: saturnswap-liquidity
description: |
  Use this skill when the user wants to add or withdraw liquidity on SaturnSwap.
  Triggers on: "add liquidity", "provide liquidity", "LP on SaturnSwap",
  "withdraw liquidity", "remove liquidity", "manage my liquidity position",
  "deposit ADA into pool", "liquidity provision". Use saturnswap-liquidity-operator
  to execute transactions.
version: 1.0.0
---

# SaturnSwap Liquidity Management

Guide users through adding and withdrawing liquidity on SaturnSwap DEX.

## Capabilities

- Add liquidity to an existing pool (ADA or token side)
- Withdraw liquidity from a position
- View current liquidity positions (delegates to saturnswap-portfolio)

## Add Liquidity Flow

1. **Find the pool** — look up by ticker or pool ID
2. **Check existing positions** — see if user already has a position in this pool
3. **Determine amount** — how much ADA or tokens to deposit
4. **Build transaction** — call `createAddLiquidity`
5. **Hand off to operator** — for signing and submission

## Withdraw Liquidity Flow

1. **List positions** — show user's liquidity positions
2. **Select position** — identify which pool/contract to withdraw from
3. **Determine amount** — partial or full withdrawal
4. **Build transaction** — call `createWithdrawLiquidity`
5. **Hand off to operator** — for signing and submission

## Scripts

### Create Add Liquidity Transaction

```bash
node scripts/create-add-liquidity.js --address <bech32> --contract <liquidityPoolContractId> [--policy <policyId>] [--asset <assetName>] --amount <display-units> [--no-defaults]
```

- `--policy ""` and `--asset ""` (or omitted) = adding ADA side
- `--policy <id> --asset <name>` = adding token side
- `--no-defaults` = disable auto chunk sizing

### Create Withdraw Liquidity Transaction

```bash
node scripts/create-withdraw-liquidity.js --address <bech32> --contract <liquidityPoolContractId> [--policy <policyId>] [--asset <assetName>] --amount <display-units>
```

## Key Concepts

- Liquidity on SaturnSwap works as **chunked limit orders** spread across price points
- When you add liquidity, the API splits your deposit into multiple limit orders
- `useDefaults: true` lets the API choose optimal chunk sizes
- `liquidityPoolContractId` is the UUID of your specific liquidity position (not the pool ID)
- You can have multiple positions in the same pool
- Positions track `ada_order_token_one_amount` and `order_token_two_amount` separately
- `waiting_*` amounts are funds being rebalanced between chunks

## Safety Rules

- Always show current position stats before adding/withdrawing
- Confirm the exact amount and side (ADA vs token) with the user
- Warn about impermanent loss for volatile pairs
- Display units only — 100 ADA means `tokenAmount: 100`
