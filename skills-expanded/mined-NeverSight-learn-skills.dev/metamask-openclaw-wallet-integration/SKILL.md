---
name: metamask-openclaw-wallet-integration
description: Connect MetaMask wallets, read balances, sign messages, and send transactions on EVM chains with a safety-first TypeScript SDK
triggers:
  - "integrate MetaMask wallet into my dapp"
  - "connect to MetaMask and read user balance"
  - "sign a message with MetaMask"
  - "send a transaction using OpenClaw"
  - "switch MetaMask to a different network"
  - "set up wallet connection in my web3 app"
  - "handle MetaMask account changes"
  - "prepare an Ethereum transfer with user approval"
---

# MetaMask OpenClaw Wallet Integration

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

**OpenClaw** is a safety-first TypeScript toolkit and SDK for integrating MetaMask wallets into dapps. Built on the official MetaMask SDK, it provides a clean API for:

- Connecting wallets (desktop browser, mobile browser, QR code to MetaMask Mobile)
- Reading account balances across EVM chains (Ethereum, Polygon, Base, Arbitrum, Optimism, Linea)
- Signing messages (user approves in MetaMask UI)
- Preparing and sending transactions (user approves amount and gas)
- Switching networks with automatic chain addition
- Reacting to account/network changes

**Safety guarantee**: OpenClaw never requests or handles seed phrases or private keys. All sensitive operations require user approval in the MetaMask UI.

## Installation

### As a library (npm/yarn/pnpm)

```bash
npm install metamask-openclaw-skill
# or
yarn add metamask-openclaw-skill
# or
pnpm add metamask-openclaw-skill
```

### From source

```bash
git clone https://github.com/veryyoldman/metamask-openclaw-skill.git
cd metamask-openclaw-skill
npm install
npm run build
```

### Windows one-command install

```cmd
git clone https://github.com/veryyoldman/metamask-openclaw-skill.git && cd metamask-openclaw-skill && npm install && npm run build
```

## Quick Start

### Basic library usage

```typescript
import { OpenClaw } from "metamask-openclaw-skill";

// Initialize
const claw = new OpenClaw({
  dappMetadata: {
    name: "My Dapp",
    url: "https://mydapp.example"
  },
  // Optional: provide Infura key for reliable RPC
  infuraApiKey: process.env.INFURA_API_KEY
});

// Connect wallet (triggers MetaMask popup or QR code)
await claw.connect();

// Get current state
const { account, chainId } = claw.getState();
console.log(`Connected: ${account} on chain ${chainId}`);
```

### CLI usage

```bash
# Connect and display address + network
node dist/cli/openclaw.js connect

# Check balance
node dist/cli/openclaw.js balance

# Prepare a transfer (user approves in MetaMask)
node dist/cli/openclaw.js send 0xRecipientAddress 0.001
```

### Browser usage (zero build)

```html
<!DOCTYPE html>
<html>
<head>
  <title>OpenClaw Demo</title>
</head>
<body>
  <button id="connect">Connect MetaMask</button>
  <div id="info"></div>

  <script type="module">
    import { OpenClaw } from './dist/index.js';

    const claw = new OpenClaw({
      dappMetadata: { name: "Demo", url: window.location.href }
    });

    document.getElementById('connect').onclick = async () => {
      await claw.connect();
      const { account, chainId } = claw.getState();
      const balance = await claw.getBalance();
      document.getElementById('info').innerText = 
        `${account}\nChain: ${chainId}\nBalance: ${balance.formatted} ${balance.symbol}`;
    };
  </script>
</body>
</html>
```

## Core API

### Constructor options

```typescript
interface OpenClawOptions {
  dappMetadata: {
    name: string;      // Your dapp name
    url: string;       // Your dapp URL
    iconUrl?: string;  // Optional icon
  };
  infuraApiKey?: string;  // Optional Infura key for RPC
  defaultChainId?: string; // e.g. "0x1" for Ethereum mainnet
}

const claw = new OpenClaw(options);
```

### Connection methods

```typescript
// Connect to MetaMask (shows popup or QR)
await claw.connect();

// Disconnect
claw.disconnect();

// Check connection status
const isConnected = claw.isConnected();

// Get current state
const state = claw.getState();
// Returns: { account: string | null, chainId: string | null }
```

### Reading data

```typescript
// Get native token balance
const balance = await claw.getBalance();
// Returns: { formatted: string, symbol: string, raw: string }
// Example: { formatted: "1.234", symbol: "ETH", raw: "1234000000000000000" }

// Get balance for specific address
const balance = await claw.getBalance("0xOtherAddress");
```

### Signing messages

```typescript
// Sign a message (user approves in MetaMask)
const signature = await claw.signMessage("Hello, Web3!");
// Returns: string (hex signature)
```

### Network switching

```typescript
// Switch to a different network
await claw.switchChain("0x89"); // Polygon
await claw.switchChain("0x2105"); // Base
await claw.switchChain("0xa4b1"); // Arbitrum

// If the network isn't in MetaMask, it will be added (user approves)
```

### Sending transactions

```typescript
// Send native token (user approves amount + gas in MetaMask)
const txHash = await claw.sendNative({
  to: "0xRecipientAddress",
  amount: "0.001" // in native token (e.g. ETH, POL)
});
console.log(`Transaction sent: ${txHash}`);
```

### Event handling

```typescript
// Listen for account or network changes
claw.onChange((state) => {
  console.log("Wallet changed:", state);
  // state: { account: string | null, chainId: string | null }
});

// Remove listener
const unsubscribe = claw.onChange(handler);
unsubscribe();
```

## Configuration

### Environment variables

```bash
# .env file
INFURA_API_KEY=your_infura_key_here
```

```typescript
import { OpenClaw } from "metamask-openclaw-skill";

const claw = new OpenClaw({
  dappMetadata: {
    name: process.env.DAPP_NAME || "My Dapp",
    url: process.env.DAPP_URL || "http://localhost:3000"
  },
  infuraApiKey: process.env.INFURA_API_KEY
});
```

### Supported networks

| Network          | Chain ID    | Symbol |
|------------------|-------------|--------|
| Ethereum Mainnet | `0x1`       | ETH    |
| Polygon          | `0x89`      | POL    |
| Arbitrum One     | `0xa4b1`    | ETH    |
| OP Mainnet       | `0xa`       | ETH    |
| Base             | `0x2105`    | ETH    |
| Linea            | `0xe708`    | ETH    |
| Sepolia (testnet)| `0xaa36a7`  | ETH    |

Add custom networks in `src/chains.ts`.

## Common Patterns

### React integration

```typescript
import { OpenClaw } from "metamask-openclaw-skill";
import { useEffect, useState } from "react";

function WalletButton() {
  const [claw] = useState(() => new OpenClaw({
    dappMetadata: { name: "My App", url: window.location.href }
  }));
  const [account, setAccount] = useState<string | null>(null);
  const [balance, setBalance] = useState<string>("");

  useEffect(() => {
    claw.onChange((state) => {
      setAccount(state.account);
      if (state.account) {
        claw.getBalance().then(b => setBalance(`${b.formatted} ${b.symbol}`));
      }
    });
  }, [claw]);

  const handleConnect = async () => {
    await claw.connect();
    const state = claw.getState();
    setAccount(state.account);
    if (state.account) {
      const b = await claw.getBalance();
      setBalance(`${b.formatted} ${b.symbol}`);
    }
  };

  return (
    <div>
      {!account ? (
        <button onClick={handleConnect}>Connect MetaMask</button>
      ) : (
        <div>
          <p>{account}</p>
          <p>{balance}</p>
        </div>
      )}
    </div>
  );
}
```

### Transfer with confirmation

```typescript
async function sendTokens(claw: OpenClaw, recipient: string, amount: string) {
  const state = claw.getState();
  if (!state.account) {
    throw new Error("No wallet connected");
  }

  const balance = await claw.getBalance();
  if (parseFloat(balance.formatted) < parseFloat(amount)) {
    throw new Error("Insufficient balance");
  }

  const txHash = await claw.sendNative({ to: recipient, amount });
  console.log(`Transfer initiated: ${txHash}`);
  return txHash;
}
```

### Multi-chain balance checker

```typescript
async function checkBalanceOnChains(claw: OpenClaw, chains: string[]) {
  const balances: Record<string, string> = {};
  
  for (const chainId of chains) {
    await claw.switchChain(chainId);
    const balance = await claw.getBalance();
    balances[chainId] = `${balance.formatted} ${balance.symbol}`;
  }
  
  return balances;
}

// Usage
const balances = await checkBalanceOnChains(claw, ["0x1", "0x89", "0x2105"]);
console.log(balances);
// { "0x1": "1.5 ETH", "0x89": "100 POL", "0x2105": "0.5 ETH" }
```

### Safe message signing

```typescript
async function signAuthMessage(claw: OpenClaw, nonce: string) {
  const state = claw.getState();
  if (!state.account) {
    throw new Error("No wallet connected");
  }

  const message = `Sign to authenticate\nAddress: ${state.account}\nNonce: ${nonce}`;
  const signature = await claw.signMessage(message);
  
  return { message, signature, address: state.account };
}
```

## Troubleshooting

### "MetaMask not detected"

**Solution**: Ensure MetaMask extension is installed and enabled. On mobile, use the in-app browser or scan the QR code.

```typescript
if (!window.ethereum) {
  alert("Please install MetaMask: https://metamask.io/download/");
}
```

### Connection hangs in Node.js CLI

**Cause**: Waiting for MetaMask Mobile QR scan.

**Solution**: The CLI prints a QR code. Open MetaMask Mobile and scan it.

### "User rejected the request"

**Cause**: User clicked "Cancel" or "Reject" in MetaMask.

**Solution**: Catch the error and prompt the user to try again.

```typescript
try {
  await claw.connect();
} catch (error) {
  if (error.code === 4001) {
    console.log("User rejected connection");
  }
}
```

### Balance shows "0.0" on testnet

**Cause**: No funds in the test account.

**Solution**: Get testnet ETH from a faucet:
- Sepolia: https://sepoliafaucet.com/

### Chain switch fails

**Cause**: Network not configured in MetaMask.

**Solution**: OpenClaw automatically adds the network (user approves). Ensure chain details are correct in `src/chains.ts`.

### Infura rate limiting

**Cause**: No Infura API key or exceeded free tier.

**Solution**: Sign up at https://infura.io/ and set `INFURA_API_KEY` environment variable.

```typescript
const claw = new OpenClaw({
  dappMetadata: { name: "App", url: "https://app.example" },
  infuraApiKey: process.env.INFURA_API_KEY // Add this
});
```

## Safety & Security

**OpenClaw never:**
- Requests your seed phrase or private keys
- Signs or sends anything without user approval in MetaMask UI
- Stores sensitive data

**Always:**
- User approves every signature and transaction in MetaMask
- Keys remain in MetaMask's secure vault
- Only public addresses are exposed to the dapp

**Never** enter your Secret Recovery Phrase anywhere except the official MetaMask app when restoring a wallet. OpenClaw will never ask for it.

## AI Agent Usage

When helping users with OpenClaw:

1. **Never** generate or request seed phrases or private keys
2. **Always** defer fund movements to user approval via `sendNative()`
3. **Verify** the user has MetaMask installed before suggesting connection
4. **Use** `getBalance()` for read-only balance checks
5. **Encourage** testnet usage (Sepolia) for learning
6. **Remind** users that they approve all signatures and transactions in MetaMask

Example safe agent response:
```
I can help you prepare a transaction using OpenClaw. Here's the code:

await claw.sendNative({ to: "0xRecipient", amount: "0.001" });

This will show a MetaMask popup where YOU approve the amount and gas.
OpenClaw never handles your keys — you stay in full control.
```

## Additional Resources

- **Repository**: https://github.com/veryyoldman/metamask-openclaw-skill
- **Examples**: See `examples/basic-dapp` for a working browser demo
- **MetaMask SDK Docs**: https://docs.metamask.io/sdk/
- **Security Policy**: See `SECURITY.md` in the repository
- **Contributing**: See `CONTRIBUTING.md` in the repository

---

**Keywords**: metamask, wallet integration, web3, ethereum, evm, polygon, base, arbitrum, sign message, send transaction, dapp, typescript, sdk
