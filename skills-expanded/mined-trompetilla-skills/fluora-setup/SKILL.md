---
name: fluora-setup
description: Interactive setup wizard for Fluora marketplace integration. Installs fluora-mcp, generates wallet, configures mcporter, and guides funding.
homepage: https://fluora.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "requires": { "bins": ["node", "npm"] },
        "install":
          [
            {
              "id": "fluora-mcp",
              "kind": "node",
              "package": "fluora-mcp",
              "bins": ["fluora-mcp"],
              "label": "Install fluora-mcp (global)",
            },
          ],
      },
  }
---

# Fluora Setup - Interactive Onboarding Wizard

Complete setup wizard for accessing the Fluora marketplace. Handles wallet generation, mcporter configuration, and funding instructions.

## What This Skill Does

Automates the entire Fluora setup process:
1. ✅ Installs `fluora-mcp` globally
2. ✅ Generates wallet (auto-creates `~/.fluora/wallets.json`)
3. ✅ Extracts wallet address from private key
4. ✅ Displays funding instructions
5. ✅ Configures mcporter with Fluora registry
6. ✅ Verifies setup is working

## Prerequisites

- Node.js 18+
- npm
- mcporter installed (optional, will guide if missing)

## Usage

### From OpenClaw Agent

```typescript
// Run interactive setup
await setupFluora();

// With options
await setupFluora({
  skipMcporterConfig: false,
  fundingAmount: 10 // in USDC
});
```

### Direct Script Usage

```bash
# Interactive setup (recommended)
node setup.js

# Skip mcporter config
node setup.js --skip-mcporter

# Custom funding amount
node setup.js --funding 10
```

## What Gets Created/Modified

### 1. Global Package
```bash
npm install -g fluora-mcp
```

### 2. Wallet File
```
~/.fluora/wallets.json
```

Auto-generated on first run with structure:
```json
{
  "BASE_MAINNET": {
    "privateKey": "0x..."
  }
}
```

### 3. mcporter Config
```
~/.openclaw/workspace/config/mcporter.json
```
(or `~/.mcporter/mcporter.json` if workspace config doesn't exist)

Adds Fluora registry:
```json
{
  "mcpServers": {
    "fluora-registry": {
      "command": "npx",
      "args": ["fluora-mcp"],
      "env": {
        "ENABLE_REQUEST_ELICITATION": "true",
        "ELICITATION_THRESHOLD": "0.01"
      }
    }
  }
}
```

**Note:** mcporter looks for config in current directory first, then `~/.mcporter/`. The workspace config works from any directory inside `~/.openclaw/workspace/`.

## Wallet Funding

The skill will display your wallet address and instructions:

```
Your Fluora Wallet Address:
0x1234567890abcdef1234567890abcdef12345678

To fund your wallet:
1. Open Coinbase, Binance, or your preferred exchange
2. Send $1 USDC to the address above
3. **Important:** Select "Base" network (NOT Ethereum mainnet)
4. Wait ~1 minute for confirmation
```

### Network Details
- **Network:** Base (Coinbase L2)
- **Token:** USDC
- **Recommended amount:** $1 for testing
- **Gas fees:** $0 (paid by service provider)

### Where to Get USDC on Base

**From an exchange:**
- Coinbase: Withdraw USDC → Select "Base" network
- Binance: Withdraw USDC → Select "Base" network
- OKX: Similar process

**Bridge from Ethereum:**
- https://bridge.base.org
- Transfer USDC from Ethereum → Base

**Buy directly on Base:**
- Use Coinbase Wallet or Rainbow Wallet
- Buy USDC directly on Base

## Verification

The skill automatically verifies:
- ✅ fluora-mcp installed
- ✅ Wallet file exists
- ✅ Private key is valid
- ✅ Wallet address derived correctly
- ✅ mcporter config is valid JSON
- ✅ Fluora registry configured

Optional: Check wallet balance (after funding)

## Return Value

```json
{
  "success": true,
  "walletAddress": "0x...",
  "privateKeyPath": "~/.fluora/wallets.json",
  "mcporterConfigured": true,
  "funded": false,
  "nextSteps": [
    "Fund wallet with $1 USDC on Base",
    "Test with: mcporter call fluora-registry.exploreServices",
    "Start building with workflow-to-monetized-mcp"
  ]
}
```

## After Setup

### Test Your Setup

```bash
# List available services
mcporter call 'fluora-registry.exploreServices()'

# Use a service (requires funded wallet)
mcporter call 'fluora-registry.useService' --args '{
  "serviceId": "example",
  "serverUrl": "https://...",
  "serverId": "...",
  "params": {}
}'
```

### Start Building

Now you can use the other Fluora skills:
1. **workflow-to-monetized-mcp** - Generate your own service
2. **railway-deploy** - Deploy to Railway
3. **fluora-publish** - List on marketplace

## Troubleshooting

### "fluora-mcp not found"
```bash
npm install -g fluora-mcp
```

### "wallets.json not created"
Run `npx fluora-mcp` manually once, then re-run setup.

### "Invalid private key"
The key in `~/.fluora/wallets.json` should be 0x-prefixed hex string (66 characters).

### "Wrong network"
Make sure you're sending USDC on **Base** network, not Ethereum mainnet or other L2s.

### "Still no balance after funding"
- Check transaction on Base block explorer: https://basescan.org
- Wait 1-2 minutes for confirmation
- Verify you sent to the correct address

## Security Notes

### Private Key Safety
- `~/.fluora/wallets.json` contains your private key
- Keep this file secure (default permissions: 600)
- Never commit to git
- Never share the private key
- This wallet is for **buying services**, not storing large amounts

### Best Practices
- Fund with small amounts initially ($1 for testing)
- Monitor spending in Fluora dashboard
- Rotate wallets if compromised
- Use separate wallet for each OpenClaw instance

## Cost Summary

### Setup Costs
- fluora-mcp: Free (npm package)
- Wallet generation: Free
- Initial funding: $1 USDC (you choose)

### Ongoing Costs
- Service calls: $0.001-0.20 per call (varies by service)
- Gas fees: $0 (paid by service provider)

### Example Usage
- $1 USDC → ~50-1000 calls (depending on service)
- Most calls are $0.001-0.02

## Resources

- Fluora marketplace: https://fluora.ai
- Base network: https://base.org
- Block explorer: https://basescan.org
- USDC info: https://www.circle.com/en/usdc
