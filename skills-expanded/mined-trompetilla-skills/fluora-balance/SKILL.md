---
name: fluora-balance
description: Check USDC balance of your Fluora wallet on Base network. Quick balance checks for budgeting and monitoring spending.
homepage: https://fluora.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires": { "bins": ["node"] },
        "install": [],
      },
  }
---

# Fluora Balance - Wallet Balance Checker

Quickly check your Fluora wallet's USDC balance on Base network. Essential for monitoring spending and ensuring you have funds before making service purchases.

## What This Skill Does

- ✅ Reads your Fluora wallet from `~/.fluora/wallets.json`
- ✅ Derives wallet address from private key
- ✅ Queries USDC balance on Base network
- ✅ Displays formatted balance with clear status
- ✅ Provides funding instructions if balance is zero

## Prerequisites

- Node.js 18+
- Fluora wallet already set up (run `fluora-setup` first)
- Internet connection (queries Base RPC)

## Installation

```bash
cd fluora-balance
npm install  # Installs ethers.js
```

## Usage

### Quick Balance Check

```bash
# Check your Fluora wallet balance
node balance.js
```

**Output:**
```
💰 Checking USDC balance on Base...
Wallet: 0x7DC445b40719ab48209017f61e23D4c6D771744E

═══════════════════════════════════════════
✓ Balance: 4.85 USDC
═══════════════════════════════════════════
```

### Check Any Wallet Address

```bash
# Check specific address
node balance.js 0x1234567890abcdef1234567890abcdef12345678
```

### From OpenClaw Agent

```javascript
import { getBalance } from './balance.js';

// Check your Fluora wallet
const result = await getBalance();
console.log(`Balance: ${result.balance} ${result.symbol}`);

// Check specific address
const result = await getBalance('0x...');
```

### Programmatic Usage

```javascript
import { getBalance } from './balance.js';

try {
  const result = await getBalance();
  
  if (result.hasBalance) {
    console.log(`You have ${result.balance} ${result.symbol}`);
  } else {
    console.log('Wallet needs funding');
  }
  
} catch (error) {
  console.error('Failed to check balance:', error);
}
```

## Return Value

```json
{
  "address": "0x7DC445b40719ab48209017f61e23D4c6D771744E",
  "balance": "4.85",
  "symbol": "USDC",
  "raw": "4850000",
  "hasBalance": true
}
```

## Use Cases

### Before Service Purchase

```bash
# Check if you have enough funds
node balance.js

# If balance is low, fund wallet
# Then try service again
```

### Budget Monitoring

```bash
# Daily balance check
node balance.js > daily-balance.log

# Compare over time
diff yesterday.log today.log
```

### Spending Alerts

```javascript
const { getBalance } = require('./balance');

// Check balance before expensive operation
const result = await getBalance();
if (parseFloat(result.balance) < 5.0) {
  console.warn('⚠️  Low balance! Consider funding wallet.');
}
```

### Multiple Wallets

```bash
# Check different wallets
node balance.js 0xWallet1...
node balance.js 0xWallet2...
node balance.js 0xWallet3...
```

## Network Details

- **Network**: Base (Coinbase L2)
- **Chain ID**: 8453
- **RPC**: https://mainnet.base.org
- **Token**: USDC
- **Contract**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **Decimals**: 6
- **Block Explorer**: https://basescan.org

## Funding Your Wallet

If balance is zero, the tool will display funding instructions:

```
⚠️  Your wallet has no USDC.
To fund your wallet:
  1. Send USDC to the address above
  2. Select "Base" network (NOT Ethereum mainnet)
  3. Check balance on: https://basescan.org
```

### Funding Options

**From Exchange:**
- **Coinbase**: Withdraw USDC → Select "Base" network
- **Binance**: Withdraw USDC → Select "Base" network
- **OKX**: Similar process

**Bridge from Ethereum:**
- https://bridge.base.org

**Buy Directly:**
- Coinbase Wallet (buy USDC on Base)
- Rainbow Wallet (buy USDC on Base)

## Troubleshooting

### "Fluora wallet not found"

Run setup first:
```bash
cd ../fluora-setup
node setup.js
```

Or install fluora-mcp:
```bash
npm install -g fluora-mcp
npx fluora-mcp  # Creates wallet
```

### "Error checking balance: network error"

**Network issues:**
- Check internet connection
- Base RPC may be temporarily down
- Try again in a few seconds

**Alternative RPC:**
Edit `balance.js` line 11:
```javascript
// Use your own RPC endpoint
const BASE_RPC = "https://base-mainnet.g.alchemy.com/v2/YOUR_KEY";
```

### "Invalid address"

Make sure wallet address is:
- 42 characters long
- Starts with `0x`
- Valid Ethereum address format

### Balance shows 0 but you funded

**Possible reasons:**
1. Transaction still pending (~1-2 min)
2. Wrong network (sent on Ethereum instead of Base)
3. Wrong token (sent ETH instead of USDC)
4. Wrong address

**Check on block explorer:**
```bash
# Replace with your address
open "https://basescan.org/address/0xYourAddress"
```

## Integration with Fluora Ecosystem

This skill complements:

1. **fluora-setup** - Initial wallet creation
2. **fluora-balance** (this skill) - Ongoing monitoring ←
3. **fluora-skill** - Spending tracker
4. **workflow-to-monetized-mcp** - Earning tracker

## Cost

- **Balance check**: Free (read-only RPC call)
- **No gas fees**: Only queries data, doesn't send transactions
- **No API key needed**: Uses public Base RPC

## Performance

- **Typical query time**: 200-500ms
- **Rate limits**: None (public RPC)
- **Caching**: Not needed (balance changes frequently)

## Security

### Private Key Safety

- **Reads** from `~/.fluora/wallets.json`
- **Derives** address locally (never sends private key)
- **Only queries** blockchain (read-only)
- **No network exposure** of private key

### Best Practices

- Keep `~/.fluora/wallets.json` secure (permissions: 600)
- Never share your private key
- Check wallet address before funding
- Verify network is "Base" when sending

## Comparison with Other Methods

| Method | Speed | Cost | Reliability |
|--------|-------|------|-------------|
| fluora-balance | Fast | Free | High |
| BaseScan website | Medium | Free | High |
| ethers.js manual | Fast | Free | High |
| Block explorer API | Fast | Rate limited | Medium |

## Resources

- Fluora: https://fluora.ai
- Base network: https://base.org
- Block explorer: https://basescan.org
- USDC info: https://www.circle.com/en/usdc
- Ethers.js docs: https://docs.ethers.org

## Future Enhancements

Potential additions:
- Transaction history
- Spending analytics
- Balance alerts (push notifications)
- Multi-wallet support
- Gas balance (ETH) checking
- Price conversion (USDC → USD)
