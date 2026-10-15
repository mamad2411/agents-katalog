---
name: drainerless-web3-rescue
description: |
  Expert-level skill for building Web3 applications focused on secure asset rescue,
  EIP-7702 sponsored transactions, EIP-712 typed signatures, EIP-2612 Permit flows,
  anti-MEV strategies, Flashbots/TitanBuilder integration, multi-chain DApps with
  viem/wagmi, Solidity smart contract security, and high-performance blockchain bots.
  Covers wallet rescue from compromised wallets, airdrop claiming, token factories,
  CREATE2 deterministic deployment, and Cloudflare Pages deployment patterns.
---

# DrainerLESS Web3 Rescue — Complete Knowledge Base

This skill encapsulates months of production development across two interconnected projects:

1. **DrainerLESS DApp** — A Next.js 16 multi-chain Web3 platform (drainerless.xyz) for secure token/NFT/ETH rescue from compromised wallets
2. **Bot Ultimate EIP-7702** — A high-performance TypeScript CLI bot for automated rescue operations with anti-MEV protection

## Table of Contents

1. [Core Concepts & Problem Domain](#1-core-concepts--problem-domain)
2. [Technology Stack](#2-technology-stack)
3. [EIP-7702 Deep Dive](#3-eip-7702-deep-dive)
4. [EIP-712 Typed Signatures](#4-eip-712-typed-signatures)
5. [EIP-2612 Permit Rescue Flow](#5-eip-2612-permit-rescue-flow)
6. [Smart Contract Architecture](#6-smart-contract-architecture)
7. [DApp Architecture (Next.js + Wagmi + Reown)](#7-dapp-architecture-nextjs--wagmi--reown)
8. [Bot Architecture & Anti-MEV Strategies](#8-bot-architecture--anti-mev-strategies)
9. [Multi-Chain Network Configuration](#9-multi-chain-network-configuration)
10. [Viem Patterns & Best Practices](#10-viem-patterns--best-practices)
11. [Deployment & Infrastructure](#11-deployment--infrastructure)
12. [Security Patterns](#12-security-patterns)
13. [Common Pitfalls & Solutions](#13-common-pitfalls--solutions)
14. [Code Patterns Reference](#14-code-patterns-reference)

---

## 1. Core Concepts & Problem Domain

### The Problem
When a wallet is compromised (private key leaked), a **drainer bot** monitors the wallet and instantly steals any ETH or tokens sent to it. The wallet owner cannot:
- Send ETH to pay gas for token transfers (drainer steals the ETH first)
- Execute any transaction requiring gas

### The Solution: Sponsored Transactions via EIP-7702
**EIP-7702** allows a **secure wallet (sponsor)** to pay gas on behalf of the compromised wallet, enabling atomic rescue operations:

```
┌─────────────────────────────────────────────────────────┐
│  Compromised Wallet (has tokens, no ETH, drainer active) │
│                         ↓                                │
│  EIP-7702 Authorization: delegate to rescue contract     │
│                         ↓                                │
│  Secure Wallet (sponsor): pays gas, sends rescue tx      │
│                         ↓                                │
│  Atomic Execution:                                       │
│    1. Claim airdrop (if applicable)                      │
│    2. Transfer tokens to safe destination                │
│    3. Sweep remaining ETH                                │
│    4. (Optional) Undelegate                              │
└─────────────────────────────────────────────────────────┘
```

### Rescue Methods

| Method | Use Case | Standard |
|--------|----------|----------|
| **EIP-7702 Rescue** | Universal — tokens, NFTs, ETH, custom calls | EIP-7702 + EIP-712 |
| **Permit Rescue** | ERC20 tokens with EIP-2612 support | EIP-2612 |
| **Bundle Rescue** | Multi-step operations (gas send + claim + sweep) | Flashbots/Titan |
| **Gasless Rescue** | Meta-transactions via Gelato relayer | ERC-2771 |

---

## 2. Technology Stack

### DApp (Frontend)
```json
{
  "framework": "Next.js 16 (App Router, static export)",
  "language": "TypeScript / TSX",
  "blockchain": "viem ^2.47, wagmi ^3.5",
  "wallet_connection": "@reown/appkit (WalletConnect v2)",
  "ui": "TailwindCSS 4, lucide-react icons",
  "i18n": "i18next (EN/ES)",
  "state": "React Context (LogContext, SidebarContext), @tanstack/react-query",
  "deployment": "Cloudflare Pages (wrangler)",
  "encryption": "jsencrypt (RSA for private key protection in bundles)",
  "gasless": "@gelatocloud/gasless (meta-transactions)"
}
```

### Bot (Backend CLI)
```json
{
  "runtime": "Node.js + ts-node",
  "language": "TypeScript (strict mode)",
  "blockchain": "viem ^2.21",
  "logging": "winston (structured JSON, file rotation)",
  "env": "dotenv (multi-env support: .env-airdrop, .env-unlock, etc.)",
  "mev_protection": "TitanBuilder, MEV Blocker, Flashbots Fast",
  "architecture": "Modular (config → loader → builder → executor → retry)"
}
```

### Smart Contracts
```json
{
  "language": "Solidity ^0.8.24",
  "standards": "EIP-7702, EIP-712, EIP-2612, ERC-20, ERC-721, ERC-1155, EIP-1153",
  "libraries": "OpenZeppelin (Ownable, ReentrancyGuard, Pausable)",
  "deployment": "Safe Singleton Factory (CREATE2)",
  "compiler": "solc via scripts/compile-rescuer.js"
}
```

---

## 3. EIP-7702 Deep Dive

### What is EIP-7702?
EIP-7702 allows an EOA (Externally Owned Account) to temporarily delegate its execution capabilities to a smart contract. The EOA's bytecode is set to point to the contract, enabling the EOA to execute contract logic as if it were a smart contract.

### Authorization List
The EOA owner signs an **authorization** that specifies which contract to delegate to:

```typescript
// Signing EIP-7702 authorization with viem
const compromisedWalletClient = createWalletClient({
  account: compromisedAccount,
  chain: networkConfig.chain,
  transport: http(rpcUrl)
});

const signedAuthorization = await compromisedWalletClient.signAuthorization({
  contractAddress: rescueContractAddress,  // Contract to delegate to
  chainId: networkConfig.chainId,
  nonce: compromisedNonce,  // CRITICAL: Must match current EOA nonce
});
```

### Sending EIP-7702 Transactions
The **sponsor** (secure wallet) sends the transaction with the authorization list:

```typescript
const tx = {
  account: secureAccount,           // Sponsor pays gas
  to: rescueContractAddress,        // Call goes to the rescue contract
  value: totalValueRequired,        // ETH needed for claim fees
  data: callData,                   // Encoded function call
  authorizationList: [signedAuthorization],  // EIP-7702 delegation
  chainId: networkConfig.chainId,
  nonce: sponsorNonce,
  type: 'eip7702' as const,
  gas: gasLimit,
  maxFeePerGas: boostedMaxFee,
  maxPriorityFeePerGas: boostedPriority,
};
```

### Key EIP-7702 Gotchas

1. **Nonce Sensitivity**: The authorization nonce MUST exactly match the compromised wallet's current nonce. If another transaction lands first, the nonce changes and the authorization becomes invalid.

2. **Gas Estimation Failures**: Many RPC nodes don't properly simulate EIP-7702 in `eth_estimateGas`. The delegation isn't applied during simulation, so subcalls hit a plain EOA (no code) and return abnormally low estimates.
   ```typescript
   // SOLUTION: Detect and correct low estimates
   const MIN_REALISTIC_GAS = 100000n;
   if (gasEstimate < MIN_REALISTIC_GAS) {
     gasEstimate = MIN_REALISTIC_GAS + (BigInt(subcalls.length) * 200000n);
   }
   ```

3. **Gas Floor & Cap**: Always enforce minimum 500,000 gas for EIP-7702 transactions and cap at 30M (block gas limit).

4. **Simulation Unreliability**: Never rely on `eth_call` simulation for EIP-7702. Execute directly.

---

## 4. EIP-712 Typed Signatures & V2 Anti-MEV / Anti-Replay Mechanics

The `DrainerLESSRescuer.sol` V2 contract incorporates rigorous cryptographic protections designed to withstand frontrunning and replay attacks from bots that have access to the compromised wallet's private keys.

### 1. Offline Signature Pre-Computation
All cryptographic data (EIP-7702 authorization list and EIP-712 batch signatures) is constructed and signed **100% offline**. No transaction metadata, parameters, or intent are exposed on-chain or in public mempools prior to the exact block of execution. This prevents MEV bots from frontrunning based on mempool indexing.

### 2. Tight Parameter Coupling (Dependability)
Rather than verifying loose parameters, the EIP-712 typed signature binds every detail of the transaction. The signature is mathematically coupled to:
- **`receiver`**: The destination safe wallet. Locked inside the signature; a malicious sponsor cannot alter it to hijack the funds.
- **`treasury`**: The fee destination address.
- **`delegateContract`**: Hardcoded to the rescue contract's address (`_SELF`). This prevents "contract swap" attacks where a malicious contract tries to reuse the signature.
- **`nonce` & `deadline`**: Replay protection and short expiration time window.
- **`operationsHash`/`subCallsHash`**: The hash of all batch subcalls, targets, values, and gas limits. A change in a single byte or value in any subcall invalidates the entire signature.

### 3. EIP-712 Domain Separator verifyingContract
To ensure the signature is uniquely bound to the specific compromised EOA:
```solidity
function _domainSeparator(address account) internal view returns (bytes32) {
    if (account == _SELF && block.chainid == _CACHED_CHAIN_ID) {
        return _CACHED_DOMAIN_SEPARATOR;
    }
    return keccak256(abi.encode(
        EIP712_DOMAIN_TYPEHASH,
        NAME_HASH,
        VERSION_HASH,
        block.chainid,
        account // verifyingContract is the compromised EOA address
    ));
}
```
> [!IMPORTANT]
> The `verifyingContract` is the **compromised EOA address** (not the rescue contract). Since EIP-7702 turns the EOA into a smart contract context, scoping the signature verification to the EOA address prevents it from being used to execute actions on behalf of other delegated wallets.

### 4. Bytecode & Extcode Check (`_verifyDelegation`)
To prevent spoofing or unauthorized entry points, the contract inspects the delegated EOA's bytecode length and prefix using inline assembly:
```solidity
function _verifyDelegation(address account) internal view {
    address self = _SELF;
    bool valid;
    assembly ("memory-safe") {
        let size := extcodesize(account)
        switch eq(size, 23) // EIP-7702 extcode size is exactly 23 bytes
        case 1 {
            let ptr := mload(0x40)
            extcodecopy(account, ptr, 0, 23)
            let first3 := shr(232, mload(ptr)) // Extcode starts with 0xef0100
            let codeAddr := shr(96, mload(add(ptr, 3))) // Delegated contract address
            valid := and(eq(first3, 0xef0100), eq(codeAddr, self))
        }
        default { valid := 0 }
    }
    if (!valid) revert NotDelegatedToContract();
}
```

### 5. Signature Malleability Protection (EIP-2)
The contract rejects signature replication by verifying that `s` is within the lower half of the curve, rejecting high-s values:
```solidity
if (uint256(s) > 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0) {
    return address(0);
}
```
This blocks attackers from modifying signature bytes to create a different transaction hash that would bypass transaction trackers.

### 6. Temporal and Cross-Chain Hardening
- **Chain ID Validation**: Prevents cross-chain replays by including `block.chainid` inside the domain separator.
- **Short-Lived Expirations**: Signatures carry a strict expiration (typically `block.timestamp + 60` seconds). This eliminates long-term signature viability; if a transaction is sandwich-attacked or delayed, the signature expires and cannot be executed later.
- **Per-Namespace Nonces**: Multi-thread execution (ERC20, NFT, ETH, BATCH, GENERIC) ensures that a failed attempt in one category doesn't block executions in others, preventing denial of service via nonce exhaustion.

### How It Works
For ERC-20 tokens that implement `EIP-2612 (permit())`, the compromised wallet can sign a gasless approval:

```
1. compromised wallet signs permit(spender=rescueContract, value, deadline, v, r, s)
2. safe wallet calls rescueContract.rescueWithPermit(token, compromised, amount, deadline, v, r, s)
3. Contract: permit() → transferFrom(compromised → contract) → split fee → send to safe wallet
```

### Implementation Pattern

```typescript
// Sign EIP-2612 permit with compromised wallet's private key
const domain = {
  name: tokenName,
  version: '1',
  chainId: chainId,
  verifyingContract: tokenContract,
};

const types = {
  Permit: [
    { name: 'owner', type: 'address' },
    { name: 'spender', type: 'address' },
    { name: 'value', type: 'uint256' },
    { name: 'nonce', type: 'uint256' },
    { name: 'deadline', type: 'uint256' },
  ]
};

const message = {
  owner: compromisedAddress,
  spender: rescueContractAddress,
  value: amount,
  nonce: nonce,
  deadline: deadline,
};

// Sign using viem's signTypedData
const signature = await compromisedAccount.signTypedData({ domain, types, primaryType: 'Permit', message });
```

### Batch Permit Rescue
The contract supports rescuing multiple tokens in a single transaction:
```solidity
function batchRescue(
  address[] tokenContracts,
  address compromisedWallet,
  uint256[] amounts,
  uint256[] deadlines,
  uint8[] v, bytes32[] r, bytes32[] s
) external;
```

---

## 6. Smart Contract Architecture

### DrainerLESSRescuer (Main Rescue Contract)
```
DrainerLESSRescuer.sol — Stateless EIP-7702 Rescue Contract V2
├── rescueERC20(account, receiver, treasury, token, amount, deadline, sig)
├── rescueETH(account, receiver, treasury, amount, deadline, sig)
├── rescueNFTs(account, receiver, items[], deadline, sig)
├── rescueBatch(account, receiver, treasury, operations[], deadline, sig)
├── batchTransactions(account, targets[], values[], data[], gasLimits[], revertOnError, deadline, sig)
└── getNonce(account, namespace) → per-namespace nonce tracking
```

**Key Properties:**
- **Stateless**: No owner, no admin, no pause, no blocklist
- **10% fee** (1000 BPS) — hardcoded, transparent
- **EIP-1153 transient storage** for reentrancy guard
- **Solady-style safe transfers** (USDT compatible — handles non-standard returns)
- **EIP-2 low-s** signature malleability protection
- **EIP-7702 delegation verification** (`address(this) != _SELF`)
- **MAX_OPERATIONS = 50** per batch (gas safety)
- **GAS_SAFETY_BUFFER = 40000** for post-loop logic

### RescuePermitV2 (Permit Rescue Contract)
```
RescuePermitV2.sol — EIP-2612 Permit-Based Rescue
├── rescueWithPermit(token, compromised, amount, deadline, v, r, s)
├── batchRescue(tokens[], compromised, amounts[], deadlines[], v[], r[], s[])
├── calculateFee(amount) → (feeAmount, userAmount)
└── Owner functions: setTreasury(), setFee(), pause/unpause
```

### Contract Deployment Pattern (CREATE2)
Use Safe Singleton Factory for deterministic addresses across chains:
```
Address: 0x77027228cA4c200977b413bA80a54E43B9017702 (same on all networks)
Factory: Safe Singleton Factory (0x914d7Fec6aaC8cd542e72Bca78B30650d45643)
Salt: Custom salt to achieve vanity address ending in "7702"
```

---

## 7. DApp Architecture (Next.js + Wagmi + Reown)

### Project Structure
```
src/
├── app/
│   ├── providers.tsx          # Wagmi + Reown AppKit + i18n setup
│   ├── layout.tsx             # Root layout
│   ├── page.tsx               # Landing page
│   ├── components/
│   │   ├── EIP7702Client.tsx      # Main EIP-7702 rescue UI (1800+ lines)
│   │   ├── EIP7702GaslessClient.tsx # Gelato gasless rescue
│   │   ├── RescuePermit.tsx       # EIP-2612 permit rescue
│   │   ├── BundlesClient.tsx      # Multi-step bundle rescue
│   │   ├── CREATE2Client.tsx      # Deterministic deployment
│   │   ├── UndelegateClient.tsx   # EIP-7702 undelegation
│   │   ├── NFTMintClient.tsx      # NFT minting tool
│   │   └── airdrop/              # Airdrop factory components
│   ├── lib/
│   │   └── networks/
│   │       ├── definitions.ts     # Single source of truth for chains
│   │       ├── types.ts           # NetworkDefinition interface
│   │       └── index.ts           # Helper functions
│   ├── contexts/
│   │   ├── LogContext.tsx         # Centralized logging
│   │   └── SidebarContext.tsx     # Sidebar state
│   └── hooks/
│       └── useViewport.ts        # Responsive viewport hook
├── contracts/                    # Solidity sources + ABIs
└── i18n.js                       # Internationalization (97K+ translations)
```

### Provider Setup Pattern (Reown AppKit + Wagmi)
```typescript
// 1. Import centralized network definitions
import { getAllChains, generateTransports } from './lib/networks';

// 2. Create WagmiAdapter with auto-generated config
const wagmiAdapter = new WagmiAdapter({
  networks: getAllChains(),
  projectId: 'your-reown-project-id',
  transports: generateTransports(),
});

// 3. Create AppKit instance
createAppKit({
  adapters: [wagmiAdapter],
  networks: getAllChains(),
  defaultNetwork: mainnet,
  features: { analytics: false, email: false, swaps: false, onramp: false },
  siwx: new ReownAuthentication({ required: false }),
});

// 4. Wrap app with providers
<WagmiProvider config={wagmiAdapter.wagmiConfig}>
  <QueryClientProvider client={queryClient}>
    {children}
  </QueryClientProvider>
</WagmiProvider>
```

### Network Definition Pattern (Single Source of Truth)
```typescript
interface NetworkDefinition {
  chain: Chain;                    // viem chain object
  features: {
    eip7702: boolean;             // Supports EIP-7702
    permit: boolean;              // Supports EIP-2612
  };
  rpc: {
    envKey: string;               // e.g., 'NEXT_PUBLIC_RPC_ETHEREUM'
    fallbackUrl?: string;         // Public fallback RPC
  };
  metadata: {
    displayName: string;          // Human-readable name
  };
}

// Add a new network: just add entry here, everything auto-generates
const NETWORKS: NetworkDefinition[] = [
  { chain: mainnet, features: { eip7702: true, permit: true },
    rpc: { envKey: 'NEXT_PUBLIC_RPC_ETHEREUM', fallbackUrl: '...' },
    metadata: { displayName: 'Ethereum' } },
  // ...
];
```

---

## 8. Bot Architecture & Anti-MEV Strategies

### 4 Operation Modes

| Mode | Entry Point | Trigger | Use Case |
|------|------------|---------|----------|
| **Airdrop** | `src/index.ts` | Timestamp scheduling | Claim airdrops at exact time |
| **Unlock** | `src/index-unlock.ts` | Mempool monitoring (WebSocket) | Rescue when token trading unlocks |
| **Bundles** | `src/bundles-titan/index.ts` | TitanBuilder eth_sendBundle | Private multi-tx rescue |
| **NOW** | `src/now/index.ts` | Immediate Multicall3 batch | Mass rescue of many wallets |

### Module Architecture
```
src/
├── config.ts              # Multi-env config loader with validation
├── types.ts               # All TypeScript interfaces
├── networks.ts            # Auto-detect chain from RPC, RPCManager setup
├── logger.ts              # Winston structured logging
├── wallet-loader.ts       # Load private keys from pk.txt
├── calldata-loader.ts     # Load claim configs from JSON
├── transaction-builder.ts # Build subcalls (claim + transfer + sweep)
├── eip712-signer.ts       # EIP-712 signing for all operation types
├── executor.ts            # Core execution engine (1100+ lines)
├── retry-executor.ts      # Block-by-block retry with claim detection
├── rpc-manager.ts         # Multi-RPC fallback + simultaneous execution
├── titan-builder.ts       # TitanBuilder integration (sendRaw + sendBundle)
├── multicall-builder.ts   # Multicall3 batch transaction builder
└── index.ts               # Airdrop mode entry point
```

### RPC Manager Pattern
```typescript
class RPCManager {
  // Sequential fallback: try each RPC until one works
  async executeWithFallback<T>(operation: (rpc: string) => Promise<T>): Promise<T>;

  // Parallel execution: fire on ALL RPCs, use first success
  async executeSimultaneously<T>(operation: (rpc: string) => Promise<T>): Promise<T>;
}

// Usage: reads use fallback (efficiency), writes use simultaneous (speed)
const receipt = await readRpcManager.executeWithFallback(getReceipt);
const hash = await rpcManager.executeSimultaneously(sendTransaction);
```

### Anti-MEV Strategy

1. **Separate Read/Write RPCs**: Read from public RPCs (fast), write to MEV-protected RPCs
   ```
   READ_RPC_URLS=https://eth.llamarpc.com,https://rpc.ankr.com/eth
   RPC_URLS=https://rpc.mevblocker.io/fast,https://rpc.flashbots.net/fast
   ```

2. **TitanBuilder Integration**: Private transaction submission to block builder
   ```typescript
   // eth_sendRawTransaction (fastest, no block targeting)
   await sendRawToTitan(signedTx);
   
   // eth_sendBundle (atomic multi-tx, targets specific blocks)
   await sendBundleToTitan(signedTxs, targetBlockHex);
   ```

3. **Deterministic Hash Tracking**: Sign locally, compute hash via keccak256 before transmitting (MEV RPCs return null hashes)
   ```typescript
   const signedTx = await secureAccount.signTransaction(finalTx);
   const hash = keccak256(signedTx); // Known before broadcast
   ```

4. **EIP-712 Deadline**: 60-second signature expiry prevents replay
   ```typescript
   const deadline = BigInt(Math.floor(Date.now() / 1000) + 60);
   ```

5. **Priority Fee Boosting**: Configurable gas tip multipliers to outbid bots
   ```typescript
   // Option 1: Multiplier (e.g., 1.5x)
   boostedPriority = basePriority + extraFee;
   // Option 2: Explicit Gwei value
   boostedPriority = parseUnits(config.maxPriorityFeeGwei.toString(), 9);
   ```

### Retry-Per-Block Strategy
When competing with drainer bots, the retry executor:
1. Sends rescue transaction
2. Polls for receipt within 2.5 block times
3. If reverted: checks if airdrop already claimed (to avoid wasting gas)
4. If unclaimed: rebuilds with fresh nonce and retries in next block
5. Smart claim detection: excludes own tx hash to avoid false positives

### Warm-Up Window (5-second pre-fetch)
For timestamp-scheduled operations, the bot:
1. Sleeps until 5 seconds before target time
2. Pre-fetches ALL nonces (secure + compromised + contract), gas fees, and block number in parallel
3. Enters high-precision busy-wait loop for remaining time
4. Fires immediately at target timestamp with pre-fetched data

```typescript
if (totalWait > 5000) {
  await sleep(totalWait - 5000);
  preFetchedMap = await warmUpGroupData(config, group, networkConfig);
  await waitForPreciseTime(remaining);
}
```

### Multicall3 EIP-7702 Batch Rescue (Mode NOW)

Rescuing assets from dozens of compromised wallets sequentially invites frontrunning—an active drainer bot will detect the first transfer and frontrun subsequent actions. The **NOW** mode batches multiple wallet rescues into **a single atomic transaction** sponsored by a single secure wallet using **Multicall3**.

#### 1. The aggregate3 Mechanism
The sponsor calls Multicall3's `aggregate3(Call3[] calls)` function. Each compromised wallet's operations run inside its own independent `batchTransactions` call within the multicall:

```typescript
const MULTICALL3_ADDRESS = '0xcA11bde05977b3631167028862bE2a173976CA11';

// Grouping multiple compromised EOA rescues into one sponsored transaction
const calls = [];
const authorizations = [];

for (const wallet of wallets) {
  // 1. Build calls
  calls.push({
    target: rescueContractAddress,
    allowFailure: true, // CRITICAL: Allow individual wallet failures
    callData: encodedBatchTransactionsData,
    value: claimFeeWei, // Value matches the native airdrop fee if required
  });
  
  // 2. Gather signed EIP-7702 authorizations (EVM applies delegation during execution)
  authorizations.push(signedAuthorization);
}
```

#### 2. Tolerating Individual Failures (`allowFailure = true`)
By setting `allowFailure: true` inside `Call3` elements, the multicall execution continues even if one of the wallets fails. For example, if a token balance was already claimed/frontrun on wallet A, its subcall reverts, but the transaction still executes successfully for wallets B, C, and D. This prevents one corrupted config or bot failure from reverting the entire batch.

#### 3. EIP-7702 Authorization Alignment
The single multicall transaction carries the `authorizationList` containing EIP-7702 signatures for **all** compromised EOAs. In the same transaction:
1. The EVM temporarily installs the `DrainerLESSRescuer` code on all EOA addresses in the batch.
2. The transaction calls Multicall3.
3. Multicall3 performs internal `DELEGATECALL` / `CALL` calls to the rescue contract, which executing in the context of each delegated EOA, extracts the assets.

#### 4. The ETH Sweep Challenge & Solution
- **The Problem**: A standard `batchTransactions` call handles ERC-20, NFT, and arbitrary target claims, but native ETH sweeps cannot easily be predicted and dynamically batch-routed in a single signature without risking over-drafting native gas balances or conflicting fees.
- **The Solution**: For wallets requiring both token extraction and a native ETH sweep, the bot builds **two separate calls per wallet** in the multicall bundle:
  1. A `batchTransactions` sub-call (executing under the EIP-712 `NS_GENERIC` namespace) containing token claims, transfer fee splits, and transfers.
  2. A subsequent `rescueETH` sub-call (executing under the EIP-712 `NS_ETH` namespace) with `amount = 0` (sweep all) and `treasury = destination` (resulting in a 0% fee bypass). This sweeps the wallet's final native balance cleanly.
  
Both signatures are generated offline, and both calls are aggregated in sequence in the same Multicall3 batch.

---

## 9. Multi-Chain Network Configuration

### Supported Chains (DApp)
Ethereum, Base, Arbitrum, BSC, Polygon, Optimism, Linea, zkSync, Scroll, Unichain,
Berachain, Ink, Blast, Gnosis, Mantle, Avalanche, Cronos, Sonic, Story, Mode, BOB,
Lisk, Fraxtal, Zora, Monad Testnet, Sepolia, Base Sepolia.

### Chain-Specific Block Times
```typescript
const BLOCK_TIMES_MS: Record<number, number> = {
  1:     12000,  // Ethereum
  8453:  2000,   // Base
  56:    3000,   // BSC
  42161: 250,    // Arbitrum
  10:    2000,   // Optimism
  137:   2000,   // Polygon
};
```

### RPC Override Pattern (Anti-MEV)
```typescript
// CRITICAL: Override viem's embedded public RPCs to prevent mempool exposure
function overrideChainRpcs(chain: Chain, rpcUrls: string[]): Chain {
  return {
    ...chain,
    rpcUrls: {
      default: { http: rpcUrls },
    },
  };
}
```

---

## 10. Viem Patterns & Best Practices

### Client Creation
```typescript
// Public client (read-only operations)
const publicClient = createPublicClient({
  chain: networkConfig.chain,
  transport: http(rpcUrl)
});

// Wallet client (signing + sending)
const walletClient = createWalletClient({
  account: privateKeyToAccount(privateKey),
  chain: networkConfig.chain,
  transport: http(rpcUrl)
});
```

### ABI Encoding
```typescript
// Encode function call data
const callData = encodeFunctionData({
  abi: contractAbi,
  functionName: 'batchTransactions',
  args: [account, targets, values, data, gasLimits, revertOnError, deadline, signature],
});

// Parse inline ABI (concise)
const ERC20_ABI = parseAbi([
  'function transfer(address to, uint256 amount) returns (bool)',
  'function balanceOf(address) view returns (uint256)',
]);
```

### Event Decoding
```typescript
for (const log of receipt.logs) {
  try {
    const decoded = decodeEventLog({
      abi: contractAbi,
      data: log.data,
      topics: log.topics,
    });
    if (decoded.eventName === 'SubCallExecuted') {
      // Process event
    }
  } catch (e) {
    // Not our event, skip
  }
}
```

### Revert Reason Decoding
```typescript
// Decode known Solidity errors
const result = decodeErrorResult({
  abi: parseAbi([
    'error EnforcedPause()',
    'error ERC20InsufficientBalance(address sender, uint256 balance, uint256 needed)',
    'error NotDelegatedToContract()',
    'error InvalidSignature()',
    'error SignatureExpired()',
  ]),
  data: revertData,
});

// Decode generic Error(string)
if (response.startsWith('0x08c379a0')) { /* ABI-decode string */ }

// Decode Panic(uint256)
if (response.startsWith('0x4e487b71')) { /* Extract panic code */ }
```

### BigInt Gas Math (Basis Points)
```typescript
// CORRECT: Use basis points for exact math
const multiplierBps = BigInt(Math.floor(gasMultiplier * 10000));
const finalGasLimit = (gasEstimate * multiplierBps) / 10000n;

// WRONG: Floating point arithmetic on BigInt
// const finalGasLimit = BigInt(Math.ceil(Number(gasEstimate) * 1.3));
```

---

## 11. Deployment & Infrastructure

### Cloudflare Pages (Static Export)
```javascript
// next.config.mjs
const nextConfig = {
  output: 'export',  // Static site generation
  env: {
    NEXT_PUBLIC_GIT_BRANCH: process.env.CF_PAGES_BRANCH || getGitInfo('git rev-parse --abbrev-ref HEAD'),
    NEXT_PUBLIC_GIT_COMMIT_HASH: process.env.CF_PAGES_COMMIT_SHA?.slice(0, 7),
  },
};
```

```bash
# Deploy command
npm run build && wrangler pages deploy out
```

### Wrangler Configuration
```toml
name = "drainerless"
pages_build_output_dir = "out"
compatibility_flags = [ "nodejs_compat" ]

[[kv_namespaces]]
binding = "RESCUE_DATA"
id = "..."

[vars]
NEXT_PUBLIC_RPC_ETHEREUM = "https://..."
```

### Cloudflare Functions (Serverless Backend)
```
functions/
├── api/
│   └── rescue.ts  # KV storage for rescue data
```

---

## 12. Security Patterns

### Private Key Handling
```typescript
// NEVER log private keys
// Validate format before use
if (!key.match(/^0x[0-9a-fA-F]{64}$/)) {
  throw new Error('Invalid private key format');
}

// RSA encryption for browser-to-server key transport (BundlesClient)
const encrypt = new JSEncrypt();
encrypt.setPublicKey(RSA_PUBLIC_KEY);
const encrypted = encrypt.encrypt(privateKey);
```

### Address Validation
```typescript
import { isAddress, getAddress } from 'viem';

// Always validate and checksum
if (!isAddress(address)) throw new Error('Invalid address');
const checksummed = getAddress(address);
```

### Fee Structure
```
DApp:  10% fee (hardcoded in smart contract, FEE_BPS = 1000)
Bot:   Configurable (FEE_BPS env variable, default 1000 = 10%)
Split: fee → treasury, remainder → destination
```

### Transient Storage Reentrancy Guard (EIP-1153)
```solidity
// Gas-efficient reentrancy protection using transient storage
bytes32 private constant _REENTRANCY_SLOT = keccak256("REENTRANCY_GUARD");

modifier nonReentrant() {
  assembly {
    if tload(_REENTRANCY_SLOT) { revert(0, 0) }
    tstore(_REENTRANCY_SLOT, 1)
  }
  _;
  assembly {
    tstore(_REENTRANCY_SLOT, 0)
  }
}
```

---

## 13. Common Pitfalls & Solutions

### 1. EIP-7702 Gas Estimation Returns Too Low
**Problem**: RPC doesn't apply delegation during `eth_estimateGas`
**Solution**: Detect estimates below 100K gas and apply heuristic fallback

### 2. MEV RPCs Return Null Transaction Hash
**Problem**: `eth_sendRawTransaction` via MEV endpoints returns `null`
**Solution**: Sign locally and compute `keccak256(signedTx)` before broadcast

### 3. Nonce Race Condition
**Problem**: Between nonce fetch and tx send, another tx lands
**Solution**: Pre-fetch nonces during 5-second warm-up window, use `blockTag: 'pending'`

### 4. USDT Non-Standard Transfer
**Problem**: USDT's `transfer()` doesn't return `bool`
**Solution**: Use Solady-style safe transfer that handles missing return values

### 5. Multiple Parallel edits to Same File
**Problem**: Concurrent file operations corrupt code
**Solution**: Always make sequential edits, use single comprehensive replace

### 6. Webpack Polyfill Issues (MetaMask SDK)
**Problem**: `@metamask/sdk` tries to import react-native modules
**Solution**: IgnorePlugin in webpack config for `@react-native-async-storage`

### 7. ox Dependency Conflict (viem/wagmi)
**Problem**: Version conflicts between wagmi and viem on the `ox` package
**Solution**: `"overrides": { "ox": "^0.11.3" }` in package.json

---

## 14. Code Patterns Reference

### Claim Config JSON Format
```json
[
  {
    "address": "0xCompromisedWallet",
    "amount": "100.5",
    "calldata": "0xClaimFunctionCalldata...",
    "claimFee": "0.00033",
    "sweepEth": true,
    "timestamp": "2026-06-07T11:00:01.000Z"
  }
]
```

### Environment File Pattern (Multi-Mode)
```bash
# .env-airdrop — Scheduled airdrop claim
SECURE_WALLET_PRIVATE_KEY=0x...
TREASURY_ADDRESS=0x...
DESTINATION_ADDRESS=0x...
RPC_URLS=https://rpc.mevblocker.io/fast,https://rpc.flashbots.net/fast
READ_RPC_URLS=https://eth.llamarpc.com,https://rpc.ankr.com/eth
RESCUE_CONTRACT_ADDRESS=0x77027228cA4c200977b413bA80a54E43B9017702
AIRDROP_CONTRACT_ADDRESS=0x...
TOKEN_ADDRESS=0x...
CLAIMS_CONFIG_PATH=./claims-config.json
EXECUTION_TIMESTAMP=1749286801
RETRY_ENABLED=true
RETRY_MAX_ATTEMPTS=5
TITAN=true
GAS_MULTIPLIER=1.3
PRIORITY_FEE_MULTIPLIER=1.5
```

### SubCall Structure
```typescript
interface SubCall {
  target: Address;        // Contract to call
  data: `0x${string}`;   // Encoded function call
  value: bigint;          // ETH to send (for claim fees)
  metadata: {
    type: 'claim' | 'fee_transfer' | 'user_transfer' | 'eth_sweep';
    token?: Address;
    amount?: string;
    recipient?: Address;
  };
}
```

### Wallet Timestamp Grouping
```typescript
// Group wallets by execution timestamp for optimal batch processing
const groupMap = new Map<number, { wallet, claimConfig }[]>();
for (const wallet of wallets) {
  const ts = resolveWalletTimestamp(claimConfig.timestamp, config.executionTimestamp);
  if (!groupMap.has(ts)) groupMap.set(ts, []);
  groupMap.get(ts)!.push({ wallet, claimConfig });
}
const sortedTimestamps = [...groupMap.keys()].sort((a, b) => a - b);
```

---

## Quick Reference: Key Addresses & Constants

| Item | Value |
|------|-------|
| DrainerLESSRescuer | `0x77027228cA4c200977b413bA80a54E43B9017702` |
| Multicall3 | `0xcA11bde05977b3631167028862bE2a173976CA11` |
| Fee BPS | `1000` (10%) |
| Max Operations | `50` per batch |
| Gas Safety Buffer | `40000` |
| EIP-712 Deadline | `60 seconds` |
| Contract Name | `DrainerLESSRescuer` |
| Contract Version | `2` |
| TitanBuilder RPC | `https://rpc.titanbuilder.xyz` |
| TitanBuilder Stats | `https://stats.titanbuilder.xyz` |

---

## When to Use Each Rescue Method

```
Is the token ERC-20 with permit() support?
  ├─ YES → Use Permit Rescue (simplest, no EIP-7702 needed)
  └─ NO
     ├─ Is the wallet compromised with active drainer?
     │   ├─ YES → Use EIP-7702 Rescue (sponsor pays gas)
     │   └─ NO → Direct transfer (no rescue needed)
     ├─ Need to claim airdrop first?
     │   ├─ YES, known timestamp → Bot: Airdrop Mode
     │   └─ YES, waiting for unlock → Bot: Unlock Mode
     ├─ Multiple wallets to rescue?
     │   ├─ < 5 wallets → Bot: Sequential mode
     │   └─ > 5 wallets → Bot: Multicall/NOW mode
     └─ Need maximum MEV protection?
         └─ YES → Bot: Titan Bundles Mode
```
