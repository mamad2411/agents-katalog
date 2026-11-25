# Get eSIM Skill

Purchase eSIM data packages using USDC on Base Sepolia via the x402 protocol.

## Description

This skill enables AI agents to purchase eSIM data packages for users. It uses the x402 payment protocol to pay with USDC on the Base Sepolia testnet, then delivers the eSIM installation page.

## Prerequisites

- A wallet that supports Base/Base Sepolia with USDC (see `wallet` skill or use your own)
- USDC balance for purchases
- ETH for gas (if using `transfer` scheme)

## Invocation

Use this skill when a user:
- Asks for an eSIM or mobile data
- Needs cellular data for travel
- Wants to buy a data plan for a specific country
- Mentions needing connectivity abroad

## Important: Transaction Timing

Crypto and eSIM transactions are NOT instant. Expect:
- **USDC transfer**: 5-15 seconds for on-chain confirmation
- **Purchase completion**: Additional 3-30 seconds for API to verify the transaction on-chain
- **Total purchase flow**: Can take 30-60 seconds from payment initiation to eSIM delivery

Inform the user that the purchase is processing and to wait for confirmation.

## Workflow

1. **Discover needs**: Ask the user which country they need data for
2. **Search packages**: Query esimqr.link for available packages
3. **Present options**: Show available data plans with prices
4. **Get selection**: User picks a package
5. **Confirm purchase**: Show price and wallet balance, get confirmation
6. **Execute x402 flow**:
   - POST to /api/agent/purchase → receive 402 with payment details
   - Pay using your wallet (see Payment Schemes below)
   - Retry POST with payment proof header
7. **Deliver eSIM**: Return the `esimPageUrl` - a user-friendly page with QR code and install buttons

## Example Conversation

```
User: I need an eSIM for my trip

Agent: I can help you get an eSIM! Which country are you traveling to?

User: USA

Agent: Let me search for USA eSIM packages...

[Searches packages]

I found these options for USA:
- US_100MB_7: 100MB / 7 Days - $0.50
- US_1_7: 1GB / 7 Days - $1.18
- US_3_7: 3GB / 7 Days - $2.50
- US_5_30: 5GB / 30 Days - $4.99

Which package would you like?

User: 1GB 7 days

Agent: The US 1GB 7-Day plan costs $1.18 USDC.

My wallet balance: $10.00 USDC

Shall I purchase this eSIM now?

User: Yes

Agent: Initiating purchase...

[Executes x402 payment flow]

✓ Payment sent: 1.18 USDC
✓ Transaction: 0xabc123...

Your eSIM is ready! Install it here:
https://esimqr.link/web3/esim/agent_1707184523_abc123

This link shows a QR code you can scan in your phone's Settings
under Cellular/Mobile Network.
```

## API Endpoints

Base URL: `https://esimqr.link`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/web3/packages?q={country}` | GET | Search packages |
| `/api/agent/quote?packageCode={code}` | GET | Get price quote |
| `/api/agent/purchase` | POST | Initiate/complete purchase |
| `/api/agent/esim/{id}` | GET | Get eSIM status |

## Payment Schemes (x402)

The 402 response offers two payment options in the `accepts` array. Choose based on your wallet capabilities:

| Scheme | Header | Wallet Requirements | Gas |
|--------|--------|---------------------|-----|
| `exact` | `PAYMENT-SIGNATURE` | EIP-3009 signing (Circle, x402 SDK) | Gasless |
| `transfer` | `X-PAYMENT` | Standard USDC transfer | You pay gas |

### Which Scheme to Use

- **Use `exact` if**: Your wallet supports EIP-3009 `transferWithAuthorization` signing (Circle wallets, x402-compatible SDKs). Benefits: gasless - the facilitator broadcasts for you.

- **Use `transfer` if**: Your wallet can do standard USDC transfers but doesn't support EIP-3009. Works with any wallet that supports Base/Base Sepolia. You pay gas fees.

- **Not sure?**: The `transfer` scheme works with any USDC-capable wallet.

### Exact Scheme Flow (gasless):
1. POST `/api/agent/purchase` → receive 402 with EIP-3009 parameters
2. Sign a `transferWithAuthorization` message (no on-chain tx needed)
3. Retry POST with header: `PAYMENT-SIGNATURE: <base64-encoded-payload>`
4. Facilitator broadcasts the transaction for you

### Transfer Scheme Flow:
1. POST `/api/agent/purchase` → receive 402 with payment details
2. Transfer USDC on-chain to `payTo` address
3. Retry POST with header: `X-PAYMENT: txHash=0x...,nonce=...`

## Network Configuration

| Parameter | Value |
|-----------|-------|
| Network | Base Sepolia Testnet |
| Chain ID | 84532 |
| USDC Token | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| USDC Decimals | 6 |

## API Response Examples

### Search Packages
```json
GET /api/web3/packages?q=US

{
  "packages": [
    {"packageCode": "US_1_7", "name": "United States 1GB 7Days", ...}
  ]
}
```

### Quote
```json
GET /api/agent/quote?packageCode=US_1_7

{
  "packageCode": "PHAJHEAYP",
  "slug": "US_1_7",
  "planName": "United States 1GB 7Days",
  "usdcAmount": "1.18",
  "paymentDetails": {
    "recipient": "0xCA16Ea02C7BB4Cf00101A468627f9D54e8434Ce2",
    "chainId": 84532
  }
}
```

### 402 Payment Required
```json
POST /api/agent/purchase
Body: {"packageCode": "US_1_7"}

{
  "x402Version": 2,
  "accepts": [
    {"scheme": "exact", ...},
    {"scheme": "transfer", "amount": "1180000", "payTo": "0xCA16...", "extra": {"nonce": "abc123"}}
  ]
}
```

### Purchase Success
```json
POST /api/agent/purchase
Headers: X-PAYMENT: txHash=0x...,nonce=abc123
Body: {"packageCode": "US_1_7"}

{
  "success": true,
  "esimId": "agent_1707184523_abc123",
  "esimPageUrl": "https://esimqr.link/web3/esim/agent_1707184523_abc123",
  "esimDetails": {
    "iccid": "8901234...",
    "activationCode": "LPA:1$..."
  }
}
```

## Files

- `esim_api.py` - API client for esimqr.link (can be used directly by agents)

## Dependencies

```
requests>=2.28.0
```

## Hackathon Submission

- **Track**: Agentic Commerce
- **Protocol**: x402 (HTTP 402 Payment Required)
- **Network**: Base Sepolia
- **Payment**: USDC

Submitted to: https://www.moltbook.com/m/usdc
