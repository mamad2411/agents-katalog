---
name: interswitch-transactions
description: >-
  Interswitch Transactions API — debit wallets, requery transaction status, reverse
  transactions, and manage payment lifecycle. Use this skill whenever debiting
  wallet accounts, checking transaction status by reference, performing transaction
  reversals, requerying completed payments, or building transaction management flows.
  Also use when you see references to /api/v1/transaction, transact, reverse,
  transaction requery, or responseCode handling.
---

# Interswitch Transactions API

Manage wallet debits, transaction status checks, reversals, and requery operations.

## Transaction Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/transaction/transact` | POST | Debit a wallet |
| `/api/v1/transaction/reverse` | POST | Reverse a transaction |
| `/api/v1/transaction/{reference}` | GET | Get transaction by reference |
| `/collections/api/v1/gettransaction.json` | GET | Requery a web checkout payment |

## Debit Wallet

```typescript
interface DebitWalletDto {
  customerId: string;          // Wallet PAN or ID
  amount: number;              // In minor currency (kobo)
  currency: string;            // '566' for NGN
  transactionRef: string;      // Unique transaction reference
  pin: string;                 // Wallet 4-digit PIN
  requestorId?: string;        // Merchant/partner identifier
  terminalId?: string;
  paymentCode?: string;
}

interface TransactionResponse {
  responseCode: string;
  responseDescription: string;
  amount: number;
  transactionRef: string;
  paymentId: string;
  remittanceAmount?: number;
}

async function debitWallet(
  data: DebitWalletDto
): Promise<TransactionResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_WALLET_BASE_URL}/api/v1/transaction/transact`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Debit failed: ${response.status}`);
  }

  return response.json();
}
```

## Get Transaction by Reference

```typescript
async function getTransactionByReference(
  reference: string
): Promise<TransactionResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_WALLET_BASE_URL}/api/v1/transaction/${encodeURIComponent(reference)}`,
    {
      method: 'GET',
      headers,
    }
  );

  if (!response.ok) {
    throw new Error(`Transaction lookup failed: ${response.status}`);
  }

  return response.json();
}
```

## Reverse Transaction

```typescript
interface ReverseTransactionDto {
  transactionRef: string;    // Original transaction reference
  amount: number;            // Amount to reverse (kobo)
  reversalRef?: string;      // Unique reversal reference
}

async function reverseTransaction(
  data: ReverseTransactionDto
): Promise<TransactionResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_WALLET_BASE_URL}/api/v1/transaction/reverse`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Reversal failed: ${response.status}`);
  }

  return response.json();
}
```

## Transaction Requery (Web Checkout Payments)

**CRITICAL**: Always requery transactions server-side after web checkout. Never trust client-side callbacks alone.

```typescript
interface RequeryResponse {
  Amount: number;
  ResponseCode: string;
  ResponseDescription: string;
  MerchantReference: string;
  PaymentReference: string;
  TransactionDate: string;
  RetrievalReferenceNumber: string;
  CardNumber?: string;
}

async function requeryTransaction(
  merchantCode: string,
  transactionRef: string
): Promise<RequeryResponse> {
  const headers = await getAuthHeaders();

  const url = new URL(
    `${process.env.INTERSWITCH_COLLECTIONS_BASE_URL}/collections/api/v1/gettransaction.json`
  );
  url.searchParams.set('merchantcode', merchantCode);
  url.searchParams.set('transactionreference', transactionRef);
  url.searchParams.set('amount', '0'); // 0 returns any amount

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers,
  });

  if (!response.ok) {
    throw new Error(`Requery failed: ${response.status}`);
  }

  return response.json();
}
```

## Response Codes

| Code | Description | Action |
| --- | --- | --- |
| `00` | Approved / Successful | Transaction completed |
| `Z0` | Transaction not found | Verify reference and retry |
| `Z1` | Pending | Check again later |
| `Z6` | Pending reversal | Monitor for completion |
| `T0` | OTP required | Prompt for OTP validation |
| `T1` | 3D Secure required | Redirect to 3DS page |
| `51` | Insufficient funds | Notify customer |
| `91` | Issuer unavailable | Retry later |
| `06` | Transaction error | Investigate and contact support |

## Complete Transaction Flow

```typescript
// 1. Initiate debit
const txn = await debitWallet({
  customerId: walletPan,
  amount: 50000, // ₦500.00
  currency: '566',
  transactionRef: `TXN_${Date.now()}_${crypto.randomUUID().slice(0, 8)}`,
  pin: customerPin,
});

// 2. Check response
if (txn.responseCode === '00') {
  console.log('Payment successful:', txn.transactionRef);
} else if (txn.responseCode === 'T0') {
  // Handle OTP
  console.log('OTP required for:', txn.paymentId);
} else {
  console.error('Payment failed:', txn.responseDescription);
}

// 3. Always requery to confirm
const confirmed = await getTransactionByReference(txn.transactionRef);
console.log('Confirmed status:', confirmed.responseCode);

// 4. Reverse if needed
if (needsReversal) {
  const reversal = await reverseTransaction({
    transactionRef: txn.transactionRef,
    amount: txn.amount,
  });
  console.log('Reversal:', reversal.responseCode);
}
```

## Best Practices

1. **Generate unique transaction refs** — Use timestamps + UUIDs
2. **Always requery** — Never rely solely on initial response
3. **Implement idempotency** — Store refs to prevent duplicate charges
4. **Handle all response codes** — Map codes to user-friendly messages
5. **Log transactions securely** — Never log PINs or full card numbers
