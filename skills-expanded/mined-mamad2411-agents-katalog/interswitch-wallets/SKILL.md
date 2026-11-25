---
name: interswitch-wallets
description: >-
  Interswitch Wallet Services API — create virtual wallets, manage balances, fund
  wallets, and make purchases with virtual cards. Use this skill whenever creating
  customer wallets, checking wallet balances, retrieving wallet details, managing
  virtual card accounts, or building stored-value payment flows. Also use when you
  see references to /api/v1/wallet endpoint, wallet PAN, virtual account numbers,
  or wallet-based transactions.
---

# Interswitch Wallet Services API

Create and manage virtual wallets for merchants and consumers. Wallets include virtual card details (PAN, CVV, expiry) for card-based transactions.

## Wallet Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/wallet` | POST | Create a new wallet |
| `/api/v1/wallet/{walletId}` | GET | Get wallet details |
| `/api/v1/wallet/{walletId}/balance` | GET | Get wallet balance |

## Environment Variables

```env
# Add to your .env (see interswitch-setup for full config)
INTERSWITCH_WALLET_BASE_URL=https://qa.interswitchng.com  # Test
# INTERSWITCH_WALLET_BASE_URL=https://saturn.interswitchng.com  # Live
```

## Create Wallet

```typescript
interface CreateWalletDto {
  firstName: string;
  lastName: string;
  email: string;
  phoneNumber: string;  // Nigerian format: +234XXXXXXXXXX
  pin: string;          // 4-digit PIN
  dateOfBirth?: string; // YYYY-MM-DD
  bvn?: string;         // Bank Verification Number (11 digits)
}

interface WalletResponse {
  walletId: string;
  pan: string;            // Virtual card PAN
  expiry: string;         // YYMM format
  cvv: string;            // 3-digit CVV
  virtualCard: boolean;
  accountNumber: string;  // Virtual account number
  bankCode: string;
  status: string;
}

async function createWallet(
  data: CreateWalletDto
): Promise<WalletResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_WALLET_BASE_URL}/api/v1/wallet`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Create wallet failed: ${response.status}`);
  }

  return response.json();
}
```

### Input Validation

```typescript
import { z } from 'zod';

const createWalletSchema = z.object({
  firstName: z.string().min(2).max(50),
  lastName: z.string().min(2).max(50),
  email: z.string().email(),
  phoneNumber: z.string().regex(
    /^\+234[0-9]{10}$/,
    'Must be Nigerian phone format: +234XXXXXXXXXX'
  ),
  pin: z.string().regex(/^[0-9]{4}$/, 'Must be 4-digit PIN'),
  dateOfBirth: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  bvn: z.string().regex(/^[0-9]{11}$/, 'BVN must be 11 digits').optional(),
});
```

## Get Wallet Details

```typescript
async function getWalletDetails(
  walletId: string
): Promise<WalletResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_WALLET_BASE_URL}/api/v1/wallet/${encodeURIComponent(walletId)}`,
    {
      method: 'GET',
      headers,
    }
  );

  if (!response.ok) {
    throw new Error(`Get wallet failed: ${response.status}`);
  }

  return response.json();
}
```

## Get Wallet Balance

```typescript
interface WalletBalance {
  availableBalance: number;
  ledgerBalance: number;
  currency: string;
}

async function getWalletBalance(
  walletId: string
): Promise<WalletBalance> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_WALLET_BASE_URL}/api/v1/wallet/${encodeURIComponent(walletId)}/balance`,
    {
      method: 'GET',
      headers,
    }
  );

  if (!response.ok) {
    throw new Error(`Get balance failed: ${response.status}`);
  }

  return response.json();
}
```

## Virtual Card Details

When a wallet is created, it includes virtual card details:

```typescript
// WalletResponse includes:
// pan: '5061050200000000123'  — Virtual card number
// expiry: '2603'              — YYMM format
// cvv: '123'                  — 3-digit CVV
// virtualCard: true           — Confirms this is a virtual card

// These details can be used for:
// 1. Online payments (card-not-present)
// 2. Integration with payment gateways
// 3. Wallet-based purchases
```

## Complete Wallet Management Flow

```typescript
// 1. Create wallet for customer
const wallet = await createWallet({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  phoneNumber: '+2348012345678',
  pin: '1234',
});
console.log('Wallet ID:', wallet.walletId);
console.log('Virtual Card PAN:', wallet.pan);

// 2. Check balance before transaction
const balance = await getWalletBalance(wallet.walletId);
console.log('Available:', balance.availableBalance);

// 3. Get full wallet details
const details = await getWalletDetails(wallet.walletId);
console.log('Account Number:', details.accountNumber);
```

## Security Considerations

1. **Never expose wallet PAN/CVV** to client-side code
2. **Store wallet IDs**, not card details — retrieve when needed
3. **Validate phone numbers** — Nigerian format required (+234XXXXXXXXXX)
4. **PIN handling** — Never log or store PINs in plaintext
5. **BVN data** — Handle as PII, encrypt at rest
