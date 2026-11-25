---
name: interswitch-cardless
description: >-
  Interswitch Cardless Payments API — generate single and bulk paycodes for ATM
  cash withdrawal without a card. Use this skill whenever implementing cardless
  withdrawal, generating paycodes for customers, managing bulk paycode operations,
  or building cash disbursement platforms. Also use when you see references to
  paycode, cardless withdrawal, /api/v1/paycode, ATM withdrawal without card,
  or paycode generation endpoints.
---

# Interswitch Cardless Payments API

Generate paycodes that allow customers to withdraw cash from ATMs without a physical card.

## Cardless Payment Flow

1. Customer requests withdrawal (specify amount)
2. System generates a paycode
3. Customer receives paycode via SMS/app
4. Customer enters paycode at any Interswitch-enabled ATM
5. Cash is dispensed

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/paycode` | POST | Generate single paycode |
| `/api/v1/paycode/bulk` | POST | Generate bulk paycodes |
| `/api/v1/paycode/{code}` | GET | Check paycode status |
| `/api/v1/paycode/{code}` | DELETE | Cancel a paycode |

## Generate Single Paycode

```typescript
interface PaycodeRequest {
  amount: number;              // Amount in kobo
  senderName: string;
  senderPhone: string;         // +234XXXXXXXXXX
  beneficiaryPhone: string;    // +234XXXXXXXXXX
  beneficiaryName: string;
  transactionRef: string;
  currency?: string;           // Default: 'NGN'
  expiryMinutes?: number;      // Paycode validity period
}

interface PaycodeResponse {
  responseCode: string;
  responseDescription: string;
  paycode: string;             // The generated paycode
  transactionRef: string;
  amount: number;
  expiryDate: string;
}

async function generatePaycode(
  data: PaycodeRequest
): Promise<PaycodeResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/paycode`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Paycode generation failed: ${response.status}`);
  }

  return response.json();
}
```

## Generate Bulk Paycodes

```typescript
interface BulkPaycodeRequest {
  entries: PaycodeRequest[];
  batchRef: string;            // Unique batch reference
}

interface BulkPaycodeResponse {
  responseCode: string;
  batchRef: string;
  paycodes: PaycodeResponse[];
  successCount: number;
  failureCount: number;
}

async function generateBulkPaycodes(
  data: BulkPaycodeRequest
): Promise<BulkPaycodeResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/paycode/bulk`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(`Bulk paycode generation failed: ${response.status}`);
  }

  return response.json();
}
```

## Check Paycode Status

```typescript
async function getPaycodeStatus(
  paycode: string
): Promise<PaycodeResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/paycode/${encodeURIComponent(paycode)}`,
    { method: 'GET', headers }
  );

  return response.json();
}
```

## Cancel Paycode

```typescript
async function cancelPaycode(
  paycode: string
): Promise<{ responseCode: string; responseDescription: string }> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/paycode/${encodeURIComponent(paycode)}`,
    { method: 'DELETE', headers }
  );

  return response.json();
}
```

## Complete Flow Example

```typescript
// 1. Generate paycode for customer
const paycode = await generatePaycode({
  amount: 500000,              // ₦5,000
  senderName: 'John Doe',
  senderPhone: '+2348012345678',
  beneficiaryPhone: '+2349087654321',
  beneficiaryName: 'Jane Doe',
  transactionRef: `PC_${Date.now()}_${crypto.randomUUID().slice(0, 8)}`,
  expiryMinutes: 60,           // Valid for 1 hour
});

console.log('Paycode:', paycode.paycode);
console.log('Expires:', paycode.expiryDate);

// 2. Send paycode to beneficiary (via your SMS/notification system)
await sendSMS(
  '+2349087654321',
  `Your withdrawal code is ${paycode.paycode}. Amount: ₦5,000. Expires: ${paycode.expiryDate}`
);

// 3. Check status periodically
const status = await getPaycodeStatus(paycode.paycode);
if (status.responseCode === '00') {
  console.log('Paycode already used');
}

// 4. Cancel if needed
const cancellation = await cancelPaycode(paycode.paycode);
console.log('Cancelled:', cancellation.responseCode);
```

## Use Cases

- **Corporate disbursements** — Salary payments to unbanked workers
- **Emergency cash** — Send money to family members without bank accounts
- **Agent banking** — Cash distribution through ATM networks
- **Cash vouchers** — Promotional cash rewards

## Best Practices

1. **Set reasonable expiry times** — Don't leave paycodes valid indefinitely
2. **Notify beneficiaries** — Send paycode via SMS immediately
3. **Monitor usage** — Track redemption rates and expired paycodes
4. **Implement cancellation** — Allow senders to revoke unused paycodes
5. **Secure delivery** — Ensure paycodes are sent through secure channels
