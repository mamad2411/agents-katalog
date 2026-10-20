# Privy Wallet Skill

Server-side wallet management using Privy's agent wallet infrastructure.

## Overview

Privy provides custodial wallets that AI agents can use to sign transactions without managing raw private keys. This skill shows how to integrate Privy wallets with viem for transaction signing.

## Setup

### 1. Install dependencies

```bash
npm install @privy-io/node viem
```

### 2. Get your credentials from Privy

You need:
- **App ID** and **App Secret** from your Privy dashboard
- **Wallet ID** from when you created the server wallet
- **Authorization private key** (P-256, base64 DER format)

### 3. Store credentials securely

```json
// secrets/privy-wallet.json
{
  "appId": "your-app-id",
  "appSecret": "your-app-secret", 
  "walletId": "your-wallet-id",
  "address": "0x..."
}
```

```
// secrets/privy-auth-key.txt
MHcCAQEE... (base64 DER private key)
```

## Usage

### Creating a viem account

```javascript
import { PrivyClient } from '@privy-io/node';
import { createViemAccount } from '@privy-io/node/viem';
import { createWalletClient, http } from 'viem';
import { base } from 'viem/chains';

// Load your credentials
const creds = JSON.parse(fs.readFileSync('secrets/privy-wallet.json', 'utf8'));
const authKey = fs.readFileSync('secrets/privy-auth-key.txt', 'utf8').trim();

// Create Privy client
const privy = new PrivyClient({ 
  appId: creds.appId, 
  appSecret: creds.appSecret 
});

// NOTE: Use object constructor, NOT positional args:
// new PrivyClient(appId, appSecret) - FAILS SILENTLY
// new PrivyClient({ appId, appSecret }) - CORRECT

// Create viem account
const account = createViemAccount(privy, {
  walletId: creds.walletId,
  address: creds.address,
  authorizationContext: {
    authorization_private_keys: [authKey]  // NOTE: snake_case!
  }
});

// Create wallet client for transactions
const walletClient = createWalletClient({ 
  account, 
  chain: base, 
  transport: http('https://mainnet.base.org') 
});

// Now you can send transactions
const txHash = await walletClient.sendTransaction({
  to: '0x...',
  value: parseEther('0.01'),
});
```

## Common Gotchas

### 1. Snake case for authorization keys

The Privy SDK uses `authorization_private_keys` (snake_case), not camelCase:

```javascript
// ✅ Correct
authorizationContext: {
  authorization_private_keys: [authKey]
}

// ❌ Wrong - will silently fail
authorizationContext: {
  authorizationPrivateKeys: [authKey]
}
```

### 2. Import from the right package

```javascript
// ✅ Correct
import { PrivyClient } from '@privy-io/node';
import { createViemAccount } from '@privy-io/node/viem';

// ❌ Wrong - different package
import { PrivyClient } from '@privy-io/server-auth';
```

### 3. Key format

The auth key should be base64-encoded DER format (no PEM headers):
```
MHcCAQEEIIoKFwm6iEf/AjsCYUW3q9OcbfzwyDeXiv31SLRVj60ZoAoGCCqGSM49AwEHoUQDQgAE...
```

## Generating a new auth key

If you need to generate a P-256 key pair:

```javascript
import { generateP256KeyPair } from '@privy-io/node';

const keypair = await generateP256KeyPair();
console.log('Public key:', keypair.publicKey);   // For Privy dashboard
console.log('Private key:', keypair.privateKey); // Store securely!
```

## See Also

- [Privy Docs](https://docs.privy.io)
- [viem Docs](https://viem.sh)
