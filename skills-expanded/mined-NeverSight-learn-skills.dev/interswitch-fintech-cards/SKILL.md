---
name: interswitch-fintech-cards
description: >-
  Interswitch Fintech Card Processing API — debit, reverse, enquiry, and lien
  operations for fintech card programs. Use this skill whenever processing card
  debits through fintech programs, placing or releasing liens on card accounts,
  performing balance enquiries, or implementing fintech card transaction flows.
  Also use when you see references to fintech card processing, lien management,
  card debit/reversal, or /api/v1/fintech/cards endpoints.
---

# Interswitch Fintech Card Processing API

Process card debits, reversals, balance enquiries, and lien operations for fintech card programs.

## Operations

| Operation | Description |
| --- | --- |
| Debit | Charge a card account |
| Reversal | Reverse a previous debit |
| Enquiry | Check account balance |
| Lien | Place/release holds on funds |

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/fintech/cards/debit` | POST | Debit a card |
| `/api/v1/fintech/cards/reversal` | POST | Reverse a debit |
| `/api/v1/fintech/cards/enquiry` | POST | Balance enquiry |
| `/api/v1/fintech/cards/lien` | POST | Place a lien |
| `/api/v1/fintech/cards/lien/release` | POST | Release a lien |

## Card Debit

```typescript
interface FintechDebitRequest {
  pan: string;                 // Card PAN (encrypted)
  amount: number;              // In kobo
  currency: string;            // '566' for NGN
  transactionRef: string;
  terminalId: string;
  merchantCode: string;
  description?: string;
}

interface FintechTransactionResponse {
  responseCode: string;
  responseDescription: string;
  transactionRef: string;
  amount: number;
  balance?: number;
  authCode?: string;
}

async function debitCard(
  data: FintechDebitRequest
): Promise<FintechTransactionResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/fintech/cards/debit`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Reversal

```typescript
interface ReversalRequest {
  originalTransactionRef: string;  // Reference of the original debit
  amount: number;                  // Amount to reverse in kobo
  reversalRef: string;             // Unique reversal reference
  reason?: string;
}

async function reverseDebit(
  data: ReversalRequest
): Promise<FintechTransactionResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/fintech/cards/reversal`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Balance Enquiry

```typescript
interface EnquiryRequest {
  pan: string;                 // Card PAN (encrypted)
  terminalId: string;
}

interface EnquiryResponse {
  responseCode: string;
  availableBalance: number;
  ledgerBalance: number;
  currency: string;
}

async function balanceEnquiry(
  data: EnquiryRequest
): Promise<EnquiryResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/fintech/cards/enquiry`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Lien Management

A lien places a hold on funds in a card account, preventing the cardholder from using those funds until the lien is released.

### Place Lien

```typescript
interface LienRequest {
  pan: string;                 // Card PAN
  amount: number;              // Lien amount in kobo
  lienRef: string;             // Unique lien reference
  expiryDate?: string;         // When lien auto-releases
  reason: string;
}

interface LienResponse {
  responseCode: string;
  responseDescription: string;
  lienRef: string;
  amount: number;
  expiryDate: string;
}

async function placeLien(
  data: LienRequest
): Promise<LienResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/fintech/cards/lien`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

### Release Lien

```typescript
async function releaseLien(
  lienRef: string
): Promise<LienResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/fintech/cards/lien/release`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({ lienRef }),
    }
  );

  return response.json();
}
```

## Complete Processing Flow

```typescript
// 1. Check balance before debit
const balance = await balanceEnquiry({
  pan: encryptedPan,
  terminalId: 'TERM001',
});

if (balance.availableBalance < 500000) {
  console.log('Insufficient funds');
  return;
}

// 2. Place lien (optional — for pending transactions)
const lien = await placeLien({
  pan: encryptedPan,
  amount: 500000,   // ₦5,000
  lienRef: `LIEN_${Date.now()}`,
  reason: 'Pending purchase authorization',
});

// 3. Debit the card
const debit = await debitCard({
  pan: encryptedPan,
  amount: 500000,
  currency: '566',
  transactionRef: `DEB_${Date.now()}_${crypto.randomUUID().slice(0, 8)}`,
  terminalId: 'TERM001',
  merchantCode: process.env.INTERSWITCH_MERCHANT_CODE!,
  description: 'Product purchase',
});

// 4. Release lien after successful debit
await releaseLien(lien.lienRef);

if (debit.responseCode === '00') {
  console.log('Debit successful:', debit.transactionRef);
} else {
  // 5. Reverse on failure
  const reversal = await reverseDebit({
    originalTransactionRef: debit.transactionRef,
    amount: 500000,
    reversalRef: `REV_${Date.now()}`,
    reason: 'Processing error',
  });
  console.log('Reversed:', reversal.responseCode);
}
```

## Best Practices

1. **Encrypt PAN data** — Never send raw card numbers
2. **Use liens for pending auth** — Place liens for two-phase transactions
3. **Always release liens** — Even on failure, release holds
4. **Unique references** — Prevent duplicate debits with unique refs
5. **Reversal timeframes** — Process reversals promptly
6. **Balance checks** — Verify sufficient funds before debiting
