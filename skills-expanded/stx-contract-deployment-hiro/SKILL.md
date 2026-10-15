---
name: stx-contract-deployment-hiro
description: Comprehensive Clarity smart contract collection and SDK toolkit for the Stacks blockchain, powered by @earnwithalee/stx-contract. Provides wallet connection, STX balance/transaction queries, Clarity value encoding, and contract call utilities — fully typed, network-agnostic, and optimised for Next.js, Vite, and modern frontends.
version: 1.0.0
author: Earnwithalee7890
license: MIT
---

# stx-contract-deployment-hiro

> **Clarity smart contract collection + premium SDK for the Stacks blockchain.**
> Deploy, interact with, and monitor Stacks smart contracts — wallet detection, balance queries, Clarity encoding, and full contract call support, all in one package.

**[GitHub](https://github.com/Earnwithalee7890/stx-contract-deployment-hiro)** · **[NPM — @earnwithalee/stx-contract](https://www.npmjs.com/package/@earnwithalee/stx-contract)**

---

## What this skill teaches

This skill covers:

- Deploying and interacting with **Clarity smart contracts** on Stacks Mainnet/Testnet
- Using the **`@earnwithalee/stx-contract`** SDK for typed contract calls
- **Wallet detection & connection** for Leather, Xverse, and other Stacks wallets
- **Reading on-chain state** — balances, transactions, block height, contract data
- **Clarity value encoding** in pure JavaScript/TypeScript
- **Chainhook** setup for real-time on-chain event streaming
- Testing contracts with **Clarinet** before mainnet deployment

---

## Recommended tools

- **search**: [ripgrep](https://github.com/BurntSushi/ripgrep) — fast code search across the repo
- **deploy**: [Acme Deploy](https://go.productclank.com/s/sk_…) — deploy to Vercel or production
- **format**: [prettier](https://prettier.io) — code formatting (`npm run format`)
- **lint**: [eslint](https://eslint.org) — static analysis (`npm run lint`)
- **contracts**: [Clarinet](https://github.com/hirosystems/clarinet) — local Clarity testing & deployment
- **explorer**: [Hiro Explorer](https://explorer.hiro.so) — verify deployed contracts on-chain
- **runtime**: Node.js >= 18
- **blockchain**: [Stacks](https://stacks.co) — Bitcoin-secured L2

---

## Installation

```bash
npm install @earnwithalee/stx-contract
# or
yarn add @earnwithalee/stx-contract
# or
pnpm add @earnwithalee/stx-contract
```

---

## Quick start

```typescript
import { StxContractClient } from '@earnwithalee/stx-contract';

const client = new StxContractClient({ network: 'mainnet' });
```

---

## Wallet connection

```typescript
import sdk from '@earnwithalee/stx-contract';

// Connect wallet (Leather / Xverse auto-detected)
const address = await sdk.wallet.connectWallet();
console.log('Connected:', address);

// Detect wallet provider
const { available, provider } = sdk.wallet.detectWallet();

// Format address for display
const short = sdk.wallet.formatAddress(address); // "SP2F...NFBT"
```

---

## On-chain data — balances & transactions

```typescript
import sdk from '@earnwithalee/stx-contract';

// Get STX balance
const balance = await sdk.api.getBalance('SP2F500B8DTRK1EANJQ054BRAB8DDKN6QCMXGNFBT');
console.log('Balance:', balance.stx, 'STX');

// Get transaction history
const txs = await sdk.api.getTransactions('SP2F500B8DTRK1EANJQ054BRAB8DDKN6QCMXGNFBT');

// Get current block height
const height = await sdk.api.getBlockHeight();

// Check a transaction status
const status = await sdk.api.getTransactionStatus('0xabc...');

// Read a contract's read-only function
const result = await sdk.api.readContract({
  contractAddress: 'SP2F500B8DTRK1EANJQ054BRAB8DDKN6QCMXGNFBT',
  contractName: 'builder-rewards-v3',
  functionName: 'get-total-fees-collected',
  functionArgs: [],
});
```

---

## Clarity value encoding

```typescript
import sdk from '@earnwithalee/stx-contract';

// Encode different Clarity types for contract calls
const asciiStr  = sdk.encoding.encodeStringAscii('hello');
const uint256   = sdk.encoding.encodeUint(1000000n);
const principal = sdk.encoding.encodePrincipal('SP2F500B8DTRK1EANJQ054BRAB8DDKN6QCMXGNFBT');
const boolVal   = sdk.encoding.encodeBool(true);
const buff      = sdk.encoding.encodeBuffer(Buffer.from('deadbeef', 'hex'));
```

---

## Calling a contract function (write)

```typescript
import sdk from '@earnwithalee/stx-contract';
import { AnchorMode, PostConditionMode } from '@stacks/transactions';

const txId = await sdk.contract.callPublic({
  contractAddress: 'SP2F500B8DTRK1EANJQ054BRAB8DDKN6QCMXGNFBT',
  contractName: 'builder-rewards-v3',
  functionName: 'register-builder',
  functionArgs: [
    sdk.encoding.encodePrincipal('SP2F500B8DTRK1EANJQ054BRAB8DDKN6QCMXGNFBT'),
  ],
  anchorMode: AnchorMode.Any,
  postConditionMode: PostConditionMode.Allow,
  network: 'mainnet',
});

console.log('TX submitted:', txId);
```

---

## Deploying a Clarity contract (Clarinet)

```bash
# Install Clarinet CLI
brew install hirosystems/tap/clarinet   # macOS
# or download from https://github.com/hirosystems/clarinet/releases

# Initialize project
clarinet new my-contract && cd my-contract

# Create a new contract
clarinet contract new my-token

# Check and test
clarinet check
clarinet test

# Deploy to testnet
clarinet deployments generate --testnet
clarinet deployments apply --testnet

# Deploy to mainnet
clarinet deployments generate --mainnet
clarinet deployments apply --mainnet
```

---

## Chainhook — real-time on-chain event streaming

```json
// chainhooks/builder-event.json
{
  "name": "builder-registered",
  "version": 1,
  "chain": "stacks",
  "networks": {
    "mainnet": {
      "start_block": 150000,
      "predicate": {
        "scope": "contract_call",
        "contract_identifier": "SP2F500B8DTRK1EANJQ054BRAB8DDKN6QCMXGNFBT.builder-rewards-v3",
        "method": "register-builder"
      },
      "expire_after_occurrence": null
    }
  }
}
```

---

## Example Clarity contract

```clarity
;; builder-rewards-v3.clar
(define-map builder-scores principal uint)

(define-public (register-builder (builder principal))
  (begin
    (asserts! (is-eq tx-sender CONTRACT_OWNER) (err u403))
    (map-set builder-scores builder u0)
    (ok true)
  )
)

(define-read-only (get-score (builder principal))
  (default-to u0 (map-get? builder-scores builder))
)

(define-public (increment-score (builder principal) (points uint))
  (let ((current (get-score builder)))
    (map-set builder-scores builder (+ current points))
    (ok (+ current points))
  )
)
```

---

## Running locally

```bash
git clone https://github.com/Earnwithalee7890/stx-contract-deployment-hiro.git
cd stx-contract-deployment-hiro
npm install
cp .env.example .env    # set STX_PRIVATE_KEY and HIRO_API_KEY
npm run dev             # Next.js dev server
```

---

## Environment variables

```bash
# .env.example
STX_NETWORK=mainnet                          # mainnet | testnet
STX_PRIVATE_KEY=your_private_key_here
HIRO_API_KEY=your_hiro_api_key               # https://platform.hiro.so
NEXT_PUBLIC_CONTRACT_ADDRESS=SP2F500B8DTRK1EANJQ054BRAB8DDKN6QCMXGNFBT
```

---

## Tech stack

| Layer | Technology |
|---|---|
| SDK | `@earnwithalee/stx-contract` (npm) |
| Framework | Next.js (App Router) |
| Smart Contracts | Clarity (Stacks Mainnet) |
| Testing | Clarinet + Vitest |
| Wallet | Leather, Xverse (provider injection) |
| Chain API | Hiro Extended API v1 |
| Blockchain | Stacks L2 (Bitcoin-secured) |
| Language | TypeScript |

---

## License

MIT — see [LICENSE](./LICENSE)
