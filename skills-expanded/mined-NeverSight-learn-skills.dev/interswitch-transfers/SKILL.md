---
name: interswitch-transfers
description: >-
  Interswitch Transfers API — validate bank accounts, initiate single and bulk fund
  transfers, check transfer status, and resolve bank codes. Use this skill whenever
  building payout flows, processing disbursements, validating bank accounts before
  transfer, generating MAC hashes for transfer security, or implementing bulk
  transfer operations. Also use when you see references to /api/v2/quickteller/payments/transfers,
  account validation, MAC hash, sender/beneficiary objects, or bank code resolution.
---

# Interswitch Transfers API

Process fund transfers to bank accounts and mobile wallets. Supports account validation, single transfers, bulk transfers, and status checks.

## Transfer Flow

1. **Validate account** — Confirm the destination account exists
2. **Build sender object** — Party initiating the transfer
3. **Build beneficiary object** — Receiving party details
4. **Initiate transfer** — Submit transfer request with MAC hash
5. **Check status** — Verify transfer completion

## Transfer Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v2/nameenquiry` | POST | Validate bank account |
| `/api/v2/quickteller/payments/transfers` | POST | Initiate single transfer |
| `/api/v2/quickteller/payments/transfers/bulk` | POST | Initiate bulk transfer |
| `/api/v2/quickteller/payments/transfers/{ref}` | GET | Check transfer status |

## Account Validation (Name Enquiry)

Always validate the destination account before initiating a transfer:

```typescript
interface AccountValidationRequest {
  bankCode: string;        // CBN bank code
  accountNumber: string;   // 10-digit NUBAN
}

interface AccountValidationResponse {
  responseCode: string;
  accountName: string;
  accountNumber: string;
  bankCode: string;
  bankName: string;
}

async function validateAccount(
  data: AccountValidationRequest
): Promise<AccountValidationResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v2/nameenquiry`,
    {
      method: 'POST',
      headers: {
        ...headers,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        bankCode: data.bankCode,
        accountId: data.accountNumber,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(`Account validation failed: ${response.status}`);
  }

  return response.json();
}
```

## MAC Hash Generation

Transfers require a MAC (Message Authentication Code) for security. The MAC is a SHA-512 hash of concatenated transfer fields:

```typescript
import crypto from 'crypto';

interface MACFields {
  amount: string;
  sendCurrency: string;
  receiveCurrency: string;
  paymentMethod: string;
  countryCode: string;
}

function generateMAC(fields: MACFields): string {
  // Concatenate fields in order
  const data = [
    fields.amount,
    fields.sendCurrency,
    fields.receiveCurrency,
    fields.paymentMethod,
    fields.countryCode,
  ].join('');

  return crypto
    .createHash('sha512')
    .update(data)
    .digest('hex');
}
```

## Single Transfer

```typescript
interface TransferParty {
  name: string;
  accountNumber: string;
  bankCode: string;
  accountType?: string;
  phoneNumber?: string;
  email?: string;
}

interface SingleTransferRequest {
  mac: string;                  // SHA-512 MAC hash
  beneficiary: TransferParty;
  sender: TransferParty;
  initiatingEntityCode: string; // Your merchant code
  transferAmount: {
    amount: number;             // In minor currency (kobo)
    currency: string;           // 'NGN'
  };
  paymentMethod: string;        // 'AC' for account
  terminatingEntityCode: string; // Beneficiary bank code
  countryCode: string;          // 'NG'
  transactionRef: string;
}

interface TransferResponse {
  responseCode: string;
  responseDescription: string;
  transactionRef: string;
  transferCode: string;
  paymentId: string;
}

async function initiateSingleTransfer(
  data: SingleTransferRequest
): Promise<TransferResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v2/quickteller/payments/transfers`,
    {
      method: 'POST',
      headers: {
        ...headers,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Transfer failed: ${response.status}`);
  }

  return response.json();
}
```

## Check Transfer Status

```typescript
async function checkTransferStatus(
  transactionRef: string
): Promise<TransferResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v2/quickteller/payments/transfers/${encodeURIComponent(transactionRef)}`,
    {
      method: 'GET',
      headers,
    }
  );

  if (!response.ok) {
    throw new Error(`Transfer status check failed: ${response.status}`);
  }

  return response.json();
}
```

## Complete Transfer Flow

```typescript
// 1. Validate destination account
const validation = await validateAccount({
  bankCode: '058',           // GTBank
  accountNumber: '0123456789',
});
console.log('Account Name:', validation.accountName);

// 2. Generate MAC hash
const mac = generateMAC({
  amount: '500000',          // ₦5,000
  sendCurrency: 'NGN',
  receiveCurrency: 'NGN',
  paymentMethod: 'AC',
  countryCode: 'NG',
});

// 3. Initiate transfer
const transfer = await initiateSingleTransfer({
  mac,
  sender: {
    name: 'Your Business',
    accountNumber: '9876543210',
    bankCode: '044',
  },
  beneficiary: {
    name: validation.accountName,
    accountNumber: '0123456789',
    bankCode: '058',
  },
  initiatingEntityCode: process.env.INTERSWITCH_MERCHANT_CODE!,
  transferAmount: {
    amount: 500000,
    currency: 'NGN',
  },
  paymentMethod: 'AC',
  terminatingEntityCode: '058',
  countryCode: 'NG',
  transactionRef: `TRF_${Date.now()}_${crypto.randomUUID().slice(0, 8)}`,
});

console.log('Transfer ref:', transfer.transactionRef);

// 4. Check status
const status = await checkTransferStatus(transfer.transactionRef);
console.log('Transfer status:', status.responseCode);
```

## Common Bank Codes

| Bank | Code |
| --- | --- |
| Access Bank | 044 |
| First Bank | 011 |
| GTBank | 058 |
| UBA | 033 |
| Zenith Bank | 057 |
| Stanbic IBTC | 221 |
| Fidelity Bank | 070 |
| Sterling Bank | 232 |
| Union Bank | 032 |
| Wema Bank | 035 |

## Best Practices

1. **Always validate accounts** — Use name enquiry before every transfer
2. **Confirm account name** with the user before proceeding
3. **Generate unique references** — Prevent duplicate transfers
4. **Check transfer status** — Don't assume success from initial response
5. **Secure MAC generation** — Never expose MAC concatenation logic client-side
6. **Rate limiting** — Implement throttling for bulk operations
