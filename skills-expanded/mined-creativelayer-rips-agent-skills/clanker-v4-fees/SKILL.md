# Clanker V4 Fee Claiming Skill

Claim creator fees from Clanker V4 deployed tokens with proper decimal safety.

## Overview

Clanker V4 tokens generate creator fees that are deposited into a fee locker contract. Each token has separate fee pools for WETH rewards and native token rewards. This skill shows how to check and claim these fees safely.

## Prerequisites

```bash
npm install clanker-sdk viem @privy-io/node
```

## Key Concepts

### Fee Separation

Clanker V4 stores fees in separate pools:
- **WETH fees** - Trading fees paid in WETH
- **Token fees** - Trading fees paid in the native token

You must check and claim each type separately.

### Decimal Safety

**CRITICAL**: Token amounts are returned as raw BigInt (wei). Always convert to human-readable format using `formatEther()` or `formatUnits()`.

**Sanity check**: If claimed amount > total token supply, your math is wrong (forgot to convert from wei).

## Setup

```javascript
const { Clanker } = require('clanker-sdk/v4');
const { createPublicClient, createWalletClient, http, formatEther } = require('viem');
const { PrivyClient } = require('@privy-io/node');
const { createViemAccount } = require('@privy-io/node/viem');

// Contract addresses (Base)
const CONTRACTS = {
  WETH: '0x4200000000000000000000000000000000000006',
  YOUR_TOKEN: '0x...' // Your deployed token address
};

// Initialize Clanker SDK
const clanker = new Clanker({ 
  wallet: walletClient, 
  publicClient 
});
```

## Check Available Rewards

### Check WETH Rewards

```javascript
const wethRewards = await clanker.availableRewards({
  token: CONTRACTS.WETH,
  rewardRecipient: walletAddress
});

const wethAmount = parseFloat(formatEther(wethRewards));
console.log(`WETH rewards: ${wethAmount} WETH`);
```

### Check Token Rewards

```javascript
const tokenRewards = await clanker.availableRewards({
  token: CONTRACTS.YOUR_TOKEN,
  rewardRecipient: walletAddress
});

const tokenAmount = parseFloat(formatEther(tokenRewards)); // Assumes 18 decimals
console.log(`Token rewards: ${tokenAmount} TOKENS`);

// SANITY CHECK: Verify against total supply
if (tokenAmount > EXPECTED_MAX_SUPPLY) {
  throw new Error(`Token amount looks wrong: ${tokenAmount} (check decimal conversion)`);
}
```

### For Non-18-Decimal Tokens

```javascript
const { formatUnits } = require('viem');

// For 6-decimal tokens (like USDC)
const tokenAmount = parseFloat(formatUnits(tokenRewards, 6));

// For any decimal count
const tokenAmount = parseFloat(formatUnits(tokenRewards, TOKEN_DECIMALS));
```

## Claim Rewards

### Claim WETH Rewards

```javascript
const wethClaimTx = await clanker.claimRewards({
  token: CONTRACTS.WETH,
  rewardRecipient: walletAddress
});

console.log(`WETH claim tx: ${wethClaimTx}`);
```

### Claim Token Rewards

```javascript
const tokenClaimTx = await clanker.claimRewards({
  token: CONTRACTS.YOUR_TOKEN,
  rewardRecipient: walletAddress
});

console.log(`Token claim tx: ${tokenClaimTx}`);
```

## Complete Example

Here's a working fee claim script with proper decimal handling and thresholds:

```javascript
#!/usr/bin/env node

const fs = require('fs');
const { createPublicClient, createWalletClient, http, formatEther } = require('viem');
const { base } = require('viem/chains');
const { PrivyClient } = require('@privy-io/node');
const { createViemAccount } = require('@privy-io/node/viem');

// Dynamic import for ESM clanker-sdk
async function loadClankerSDK() {
  const clankerModule = await import('clanker-sdk/v4');
  return clankerModule.Clanker;
}

const CONTRACTS = {
  WETH: '0x4200000000000000000000000000000000000006',
  YOUR_TOKEN: '0x6B08F0255f0236e13e17dDD953CFd73Befcf5BE1' // Example: CLAWN
};

const WALLET = {
  ADDRESS: '0x79Bed28E6d195375C19e84350608eA3c4811D4B9',
  ID: 'ia5n10ug5xeyy2fxbareo1ar'
};

const THRESHOLDS = {
  WETH: 0.001,    // 0.001 WETH minimum
  TOKEN: 1000     // 1000 tokens minimum
};

const RPC_URL = 'https://base-mainnet.g.alchemy.com/v2/YOUR_KEY';

// Setup wallet
async function setupWallet() {
  const privySecrets = JSON.parse(fs.readFileSync('secrets/privy-wallet.json', 'utf8'));
  const authKey = fs.readFileSync('secrets/privy-auth-key.txt', 'utf8').trim();
  
  const privy = new PrivyClient({ 
    appId: privySecrets.appId, 
    appSecret: privySecrets.appSecret 
  });
  
  const account = createViemAccount(privy, {
    walletId: WALLET.ID,
    address: WALLET.ADDRESS,
    authorizationContext: { 
      authorization_private_keys: [authKey] 
    }
  });
  
  const publicClient = createPublicClient({
    chain: base,
    transport: http(RPC_URL)
  });
  
  const walletClient = createWalletClient({
    account,
    chain: base,
    transport: http(RPC_URL)
  });
  
  return { publicClient, walletClient };
}

// Check rewards
async function checkRewards(publicClient, walletClient) {
  const Clanker = await loadClankerSDK();
  const clanker = new Clanker({ wallet: walletClient, publicClient });
  
  // Check WETH rewards
  const wethRewards = await clanker.availableRewards({
    token: CONTRACTS.WETH,
    rewardRecipient: WALLET.ADDRESS
  });
  
  // Check token rewards
  const tokenRewards = await clanker.availableRewards({
    token: CONTRACTS.YOUR_TOKEN,
    rewardRecipient: WALLET.ADDRESS
  });
  
  // Convert to human-readable (assumes 18 decimals)
  const wethAmount = parseFloat(formatEther(wethRewards));
  const tokenAmount = parseFloat(formatEther(tokenRewards));
  
  console.log(`WETH rewards: ${wethAmount} WETH`);
  console.log(`Token rewards: ${tokenAmount} TOKEN`);
  
  // Sanity check for token (example: CLAWN total supply is 100B)
  if (tokenAmount > 100_000_000_000) {
    throw new Error(`Token amount looks wrong: ${tokenAmount} (> 100B total supply)`);
  }
  
  return {
    weth: { amount: wethAmount, raw: wethRewards },
    token: { amount: tokenAmount, raw: tokenRewards }
  };
}

// Claim rewards
async function claimRewards(publicClient, walletClient, rewards, dryRun = false) {
  const Clanker = await loadClankerSDK();
  const clanker = new Clanker({ wallet: walletClient, publicClient });
  
  const results = {
    weth: { claimed: false, amount: rewards.weth.amount, tx: null },
    token: { claimed: false, amount: rewards.token.amount, tx: null }
  };
  
  const claimActions = [];
  
  // Check thresholds
  if (rewards.weth.amount >= THRESHOLDS.WETH) {
    claimActions.push({ type: 'WETH', contract: CONTRACTS.WETH });
  }
  
  if (rewards.token.amount >= THRESHOLDS.TOKEN) {
    claimActions.push({ type: 'TOKEN', contract: CONTRACTS.YOUR_TOKEN });
  }
  
  if (claimActions.length === 0) {
    console.log('No rewards above threshold');
    return results;
  }
  
  if (dryRun) {
    console.log(`DRY RUN: Would claim ${claimActions.length} reward type(s)`);
    return results;
  }
  
  // Claim each type
  for (const action of claimActions) {
    console.log(`Claiming ${action.type} rewards...`);
    
    const tx = await clanker.claimRewards({
      token: action.contract,
      rewardRecipient: WALLET.ADDRESS
    });
    
    console.log(`${action.type} claim tx: ${tx}`);
    
    // Update results
    if (action.type === 'WETH') {
      results.weth.claimed = true;
      results.weth.tx = tx;
    } else if (action.type === 'TOKEN') {
      results.token.claimed = true;
      results.token.tx = tx;
    }
    
    // Wait between claims
    if (claimActions.length > 1) {
      console.log('Waiting between claims...');
      await new Promise(resolve => setTimeout(resolve, 10000));
    }
  }
  
  return results;
}

async function main() {
  const startTime = Date.now();
  
  try {
    const args = process.argv.slice(2);
    const dryRun = args.includes('--dry-run');
    
    if (args.includes('--help')) {
      console.log(`
Clanker V4 Fee Claim Script

Usage:
  node fee-claim.js           # Check and claim if above threshold  
  node fee-claim.js --dry-run # Check only, no claiming
  node fee-claim.js --help    # Show this help

Thresholds:
  - WETH: ${THRESHOLDS.WETH} minimum
  - TOKEN: ${THRESHOLDS.TOKEN.toLocaleString()} minimum

Important: 
  - WETH and token fees are separate pools
  - Token amounts are raw BigInt - use formatEther() for 18-decimal tokens
  - Sanity check: if claimed > total supply, math is wrong
      `);
      process.exit(0);
    }
    
    console.log(`Checking Clanker V4 fees... ${dryRun ? '(DRY RUN)' : ''}`);
    
    const { publicClient, walletClient } = await setupWallet();
    const rewards = await checkRewards(publicClient, walletClient);
    const claimResults = await claimRewards(publicClient, walletClient, rewards, dryRun);
    
    // Output result
    const result = {
      success: true,
      dryRun,
      rewards: {
        weth: {
          amount: rewards.weth.amount,
          aboveThreshold: rewards.weth.amount >= THRESHOLDS.WETH,
          claimed: claimResults.weth.claimed,
          tx: claimResults.weth.tx
        },
        token: {
          amount: rewards.token.amount,
          aboveThreshold: rewards.token.amount >= THRESHOLDS.TOKEN,
          claimed: claimResults.token.claimed,
          tx: claimResults.token.tx
        }
      },
      timestamp: new Date().toISOString(),
      executionTimeMs: Date.now() - startTime
    };
    
    console.log(JSON.stringify(result, null, 2));
    
  } catch (error) {
    const errorResult = {
      success: false,
      error: error.message,
      timestamp: new Date().toISOString(),
      executionTimeMs: Date.now() - startTime
    };
    
    console.log(JSON.stringify(errorResult, null, 2));
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
```

## Common Gotchas

### 1. Raw BigInt Values

```javascript
// ❌ Wrong - raw BigInt
console.log(rewards); // 1000000000000000000n

// ✅ Correct - converted to human readable  
console.log(formatEther(rewards)); // "1.0"
```

### 2. Separate Fee Pools

```javascript
// ❌ Wrong - only checks one pool
const rewards = await clanker.availableRewards({
  token: WETH_ADDRESS, 
  rewardRecipient: wallet
});

// ✅ Correct - check both pools
const wethRewards = await clanker.availableRewards({
  token: WETH_ADDRESS,
  rewardRecipient: wallet  
});

const tokenRewards = await clanker.availableRewards({
  token: YOUR_TOKEN_ADDRESS,
  rewardRecipient: wallet
});
```

### 3. Sanity Check Math

```javascript
// ✅ Good - verify amounts are reasonable
const tokenAmount = parseFloat(formatEther(tokenRewards));

if (tokenAmount > KNOWN_MAX_SUPPLY) {
  throw new Error(`Amount ${tokenAmount} exceeds max supply - check decimal conversion`);
}
```

## Configuration

### Environment Variables

```bash
export PRIVY_APP_ID="your-app-id"
export PRIVY_APP_SECRET="your-app-secret"  
export RPC_URL="https://base-mainnet.g.alchemy.com/v2/YOUR_KEY"
```

### Token Configuration

Update `CONTRACTS.YOUR_TOKEN` with your deployed token address. Ensure you have the correct decimal count for proper formatting.

## Error Handling

Common issues:
- **"Insufficient rewards"** - Below threshold or no fees accumulated
- **"Transaction reverted"** - Contract issue or insufficient gas
- **"Invalid token address"** - Token not deployed via Clanker V4
- **"Math overflow"** - Raw BigInt not converted properly

## See Also

- [Clanker SDK V4 Docs](https://github.com/clanktokens/clanker-sdk)
- [privy-wallet](../privy-wallet/) - For wallet setup
- [erc20](../erc20/) - For token operations
- [weth](../weth/) - For WETH handling