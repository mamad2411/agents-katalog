# Rips Consignment Withdrawal Skill

Check and withdraw consignment earnings from the Rips platform using Bearer token authentication.

## Overview

The Rips platform allows agents to earn USDC through token consignment deals. This skill shows how to check pending earnings and withdraw them when they exceed a threshold.

## Authentication

Rips uses simple Bearer token authentication - one API key per agent, no per-request wallet signatures needed.

### Getting Your API Key (One-Time Setup)

1. **Get nonce**: `GET /api/agent/nonce?address=<WALLET>`
2. **Register**: `POST /api/agent/register` with signed message
3. **Save the API key** from the response (shown only once!)

```javascript
// Step 1: Get nonce
const nonceRes = await fetch('https://my.rips.app/api/agent/nonce?address=' + walletAddress);
const { nonce, message } = await nonceRes.json();

// Step 2: Sign message with your wallet
const signature = await walletClient.signMessage({ message });

// Step 3: Register
const registerRes = await fetch('https://my.rips.app/api/agent/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    address: walletAddress, 
    signature, 
    nonce 
  })
});

const { apiKey, agentId } = await registerRes.json();
// SAVE THIS API KEY - it won't be shown again!
```

## Core Operations

### Check Deal Earnings

```javascript
const DEAL_ID = 'your-deal-uuid';
const API_KEY = 'rips_agent_live_...';

const response = await fetch(`https://my.rips.app/api/agent/deals/${DEAL_ID}`, {
  headers: { 
    'Authorization': `Bearer ${API_KEY}` 
  }
});

const data = await response.json();
const deal = data.deal || data;

const earnings = {
  pending: deal.pendingEarnings || 0,          // USD amount
  total: deal.totalUsdPaid || 0,               // Total earned
  available: deal.availableBalance || 0,        // Available to withdraw
  status: deal.status,                         // Deal status
  pendingFormatted: deal.pendingPayoutFormatted || `$${(deal.pendingEarnings || 0).toFixed(2)}`
};
```

### Request Withdrawal

```javascript
const withdrawRes = await fetch(`https://my.rips.app/api/agent/deals/${DEAL_ID}/withdraw`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ type: 'earnings' })
});

const withdrawData = await withdrawRes.json();
```

The response contains a `transactions[]` array with prepared calldata:

```json
{
  "transactions": [
    {
      "step": 1,
      "description": "Claim USDC from consignment manager",
      "to": "0x...",
      "data": "0x...",
      "value": "0"
    },
    {
      "step": 2,
      "description": "Transfer USDC to wallet",
      "to": "0x...",
      "data": "0x...",
      "value": "0"
    }
  ]
}
```

### Execute Withdrawal Transactions

**IMPORTANT**: When multiple transactions are returned, wait 2+ block confirmations between them.

```javascript
async function executeTxs(publicClient, walletClient, transactions) {
  const results = [];
  
  for (const tx of transactions) {
    console.log(`Step ${tx.step}: ${tx.description}`);
    
    const hash = await walletClient.sendTransaction({
      to: tx.to,
      data: tx.data,
      value: BigInt(tx.value || '0'),
    });
    
    console.log(`TX: ${hash}`);
    const receipt = await publicClient.waitForTransactionReceipt({ hash });
    console.log(`Status: ${receipt.status}`);
    
    results.push({ 
      step: tx.step, 
      description: tx.description, 
      hash, 
      status: receipt.status 
    });
    
    // Wait between multi-step transactions
    if (transactions.length > 1) {
      console.log('Waiting for confirmations...');
      await new Promise(r => setTimeout(r, 5000));
    }
  }
  
  return results;
}
```

## Complete Example

Here's a working script that checks earnings and withdraws if above a threshold:

```javascript
#!/usr/bin/env node

const fs = require('fs');
const { createPublicClient, createWalletClient, http } = require('viem');
const { base } = require('viem/chains');
const { PrivyClient } = require('@privy-io/node');
const { createViemAccount } = require('@privy-io/node/viem');

const CONFIG = {
  dealId: 'your-deal-uuid',
  threshold: 5.0, // $5 minimum
  rpcUrl: 'https://base-mainnet.g.alchemy.com/v2/YOUR_KEY',
  walletAddress: '0x...',
  walletId: 'your-wallet-id'
};

// Load credentials
function loadCredentials() {
  const privySecrets = JSON.parse(fs.readFileSync('secrets/privy-wallet.json', 'utf8'));
  const ripsConfig = JSON.parse(fs.readFileSync('secrets/rips.json', 'utf8'));
  const authKey = fs.readFileSync('secrets/privy-auth-key.txt', 'utf8').trim();
  
  return { privySecrets, ripsConfig, authKey };
}

// Setup wallet
function setupWallet(privySecrets, authKey) {
  const privy = new PrivyClient({ 
    appId: privySecrets.appId, 
    appSecret: privySecrets.appSecret 
  });
  
  const account = createViemAccount(privy, {
    walletId: CONFIG.walletId,
    address: CONFIG.walletAddress,
    authorizationContext: { 
      authorization_private_keys: [authKey] 
    }
  });
  
  const publicClient = createPublicClient({ 
    chain: base, 
    transport: http(CONFIG.rpcUrl) 
  });
  
  const walletClient = createWalletClient({ 
    account, 
    chain: base, 
    transport: http(CONFIG.rpcUrl) 
  });
  
  return { publicClient, walletClient };
}

// Check earnings
async function checkEarnings(apiKey) {
  const res = await fetch(`https://my.rips.app/api/agent/deals/${CONFIG.dealId}`, {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });
  
  if (!res.ok) {
    throw new Error(`Failed to get deal: HTTP ${res.status}`);
  }
  
  const data = await res.json();
  const deal = data.deal || data;
  
  return {
    pendingEarnings: deal.pendingEarnings || 0,
    totalEarned: deal.totalUsdPaid || 0,
    status: deal.status,
    pendingFormatted: deal.pendingPayoutFormatted || `$${(deal.pendingEarnings || 0).toFixed(2)}`
  };
}

// Request withdrawal
async function requestWithdraw(apiKey) {
  const res = await fetch(`https://my.rips.app/api/agent/deals/${CONFIG.dealId}/withdraw`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ type: 'earnings' })
  });
  
  if (!res.ok) {
    throw new Error(`Withdraw request failed: HTTP ${res.status}`);
  }
  
  return await res.json();
}

// Execute transactions
async function executeTxs(publicClient, walletClient, transactions) {
  const results = [];
  
  for (const tx of transactions) {
    console.log(`Step ${tx.step}: ${tx.description}`);
    
    const hash = await walletClient.sendTransaction({
      to: tx.to,
      data: tx.data,
      value: BigInt(tx.value || '0'),
    });
    
    console.log(`TX: ${hash}`);
    const receipt = await publicClient.waitForTransactionReceipt({ hash });
    
    results.push({ 
      step: tx.step, 
      hash, 
      status: receipt.status 
    });
    
    // Wait for confirmations between multi-step txs
    if (transactions.length > 1) {
      await new Promise(r => setTimeout(r, 5000));
    }
  }
  
  return results;
}

async function main() {
  try {
    const { privySecrets, ripsConfig, authKey } = loadCredentials();
    const earnings = await checkEarnings(ripsConfig.apiKey);
    
    console.log(`Pending: ${earnings.pendingFormatted}`);
    console.log(`Total earned: $${earnings.totalEarned.toFixed(2)}`);
    
    if (earnings.pendingEarnings >= CONFIG.threshold) {
      console.log(`Above $${CONFIG.threshold} threshold - withdrawing...`);
      
      const { publicClient, walletClient } = setupWallet(privySecrets, authKey);
      const response = await requestWithdraw(ripsConfig.apiKey);
      
      if (response.transactions?.length > 0) {
        const txResults = await executeTxs(
          publicClient, 
          walletClient, 
          response.transactions
        );
        
        console.log('Withdrawal completed:', txResults);
      } else {
        console.log('No transactions returned - may be auto-withdrawn');
      }
    } else {
      console.log(`Below $${CONFIG.threshold} threshold - skipping`);
    }
    
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
```

## Configuration Files

### secrets/rips.json
```json
{
  "apiKey": "rips_agent_live_...",
  "apiUrl": "https://my.rips.app"
}
```

### secrets/privy-wallet.json
```json
{
  "appId": "your-privy-app-id",
  "appSecret": "your-privy-app-secret",
  "walletId": "your-wallet-id",
  "address": "0x..."
}
```

### secrets/privy-auth-key.txt
```
MHcCAQEE... (base64 DER private key)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agent/nonce?address=<wallet>` | Get nonce for registration |
| POST | `/api/agent/register` | Register agent (one-time) |
| GET | `/api/agent/me` | Get agent info |
| GET | `/api/agent/deals/<id>` | Get deal details with earnings |
| POST | `/api/agent/deals/<id>/withdraw` | Request withdrawal calldata |

**Base URL**: `https://my.rips.app`

## Best Practices

1. **Store API keys securely** - they're shown only once during registration
2. **Check earnings regularly** - but don't spam the API
3. **Use sensible thresholds** - gas fees may exceed small earnings
4. **Wait for confirmations** - especially between multi-step withdrawals
5. **Handle errors gracefully** - network issues, insufficient earnings, etc.

## See Also

- [privy-wallet](../privy-wallet/) - For wallet setup
- [erc20](../erc20/) - For USDC token handling
- [rips-staking](../rips-staking/) - For RIPS staking rewards