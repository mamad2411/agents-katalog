---
name: interswitch-payment-links
description: >-
  Interswitch Payment Links API — create shareable payment links, manage hosted
  fields, and process non-card payments. Use this skill whenever generating payment
  links for invoices, building no-code payment pages, implementing payment link
  management, or offering customers multiple payment options via links. Also use
  when you see references to payment links, Quickteller payment pages, pay-by-link,
  or non-card payment channels.
---

# Interswitch Payment Links API

Create and manage shareable payment links through the Quickteller Business platform. Enable customers to pay via a hosted payment page without building custom checkout UI.

## Payment Link Features

- **Shareable URLs** — Send payment links via email, SMS, WhatsApp
- **Multiple payment methods** — Card, bank transfer, USSD, QR code
- **Customizable** — Set amounts, descriptions, expiry dates
- **Trackable** — Monitor link status and payments

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/payment-links` | POST | Create payment link |
| `/api/v1/payment-links` | GET | List payment links |
| `/api/v1/payment-links/{linkId}` | GET | Get link details |
| `/api/v1/payment-links/{linkId}` | PUT | Update payment link |
| `/api/v1/payment-links/{linkId}` | DELETE | Deactivate payment link |

## Create Payment Link

```typescript
interface CreatePaymentLinkRequest {
  name: string;                // Link display name
  description?: string;
  amount: number;              // Fixed amount in kobo (0 for variable)
  currency: string;            // 'NGN'
  type: 'ONE_TIME' | 'REUSABLE';
  redirectUrl?: string;        // Post-payment redirect
  customerEmail?: string;      // Pre-fill customer email
  expiryDate?: string;         // ISO 8601 expiry
  metadata?: Record<string, string>;
  customFields?: {
    fieldName: string;
    fieldType: 'TEXT' | 'EMAIL' | 'PHONE' | 'NUMBER';
    required: boolean;
  }[];
}

interface PaymentLinkResponse {
  responseCode: string;
  linkId: string;
  url: string;                 // Shareable payment URL
  name: string;
  amount: number;
  currency: string;
  type: string;
  status: 'ACTIVE' | 'EXPIRED' | 'DEACTIVATED';
  createdAt: string;
  paymentCount: number;
  totalCollected: number;
}

async function createPaymentLink(
  data: CreatePaymentLinkRequest
): Promise<PaymentLinkResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/payment-links`,
    {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## List Payment Links

```typescript
interface ListPaymentLinksParams {
  page?: number;
  pageSize?: number;
  status?: 'ACTIVE' | 'EXPIRED' | 'DEACTIVATED';
}

async function listPaymentLinks(
  params: ListPaymentLinksParams = {}
): Promise<{ links: PaymentLinkResponse[]; totalCount: number }> {
  const headers = await getAuthHeaders();

  const url = new URL(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/payment-links`
  );
  if (params.page) url.searchParams.set('page', String(params.page));
  if (params.pageSize) url.searchParams.set('pageSize', String(params.pageSize));
  if (params.status) url.searchParams.set('status', params.status);

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers,
  });

  return response.json();
}
```

## Get Link Details

```typescript
async function getPaymentLink(
  linkId: string
): Promise<PaymentLinkResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/payment-links/${encodeURIComponent(linkId)}`,
    { method: 'GET', headers }
  );

  return response.json();
}
```

## Update Payment Link

```typescript
interface UpdatePaymentLinkRequest {
  name?: string;
  description?: string;
  amount?: number;
  expiryDate?: string;
  status?: 'ACTIVE' | 'DEACTIVATED';
}

async function updatePaymentLink(
  linkId: string,
  data: UpdatePaymentLinkRequest
): Promise<PaymentLinkResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/payment-links/${encodeURIComponent(linkId)}`,
    {
      method: 'PUT',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }
  );

  return response.json();
}
```

## Deactivate Payment Link

```typescript
async function deactivatePaymentLink(
  linkId: string
): Promise<{ responseCode: string }> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${process.env.INTERSWITCH_BASE_URL}/api/v1/payment-links/${encodeURIComponent(linkId)}`,
    { method: 'DELETE', headers }
  );

  return response.json();
}
```

## Use Case Examples

### Invoice Payment Link

```typescript
const invoiceLink = await createPaymentLink({
  name: 'Invoice #INV-2024-001',
  description: 'Payment for web development services',
  amount: 50000000,           // ₦500,000
  currency: 'NGN',
  type: 'ONE_TIME',
  customerEmail: 'client@example.com',
  redirectUrl: 'https://yoursite.com/payment/success',
  expiryDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
  metadata: {
    invoiceId: 'INV-2024-001',
    customerId: 'CUST_001',
  },
});

console.log('Payment link:', invoiceLink.url);
// Send to customer via email/SMS
```

### Donation Page (Variable Amount)

```typescript
const donationLink = await createPaymentLink({
  name: 'Support Our Cause',
  description: 'Donate any amount to our foundation',
  amount: 0,                  // Variable — customer chooses
  currency: 'NGN',
  type: 'REUSABLE',
  customFields: [
    { fieldName: 'Donor Name', fieldType: 'TEXT', required: true },
    { fieldName: 'Email', fieldType: 'EMAIL', required: true },
    { fieldName: 'Phone', fieldType: 'PHONE', required: false },
  ],
});

console.log('Donation page:', donationLink.url);
```

### Event Ticket

```typescript
const ticketLink = await createPaymentLink({
  name: 'Tech Conference 2025 - Regular Ticket',
  description: 'Access to all sessions and networking',
  amount: 2500000,            // ₦25,000
  currency: 'NGN',
  type: 'REUSABLE',
  redirectUrl: 'https://yoursite.com/ticket/confirmation',
  customFields: [
    { fieldName: 'Full Name', fieldType: 'TEXT', required: true },
    { fieldName: 'Company', fieldType: 'TEXT', required: false },
    { fieldName: 'Email', fieldType: 'EMAIL', required: true },
  ],
});
```

## Non-Card Payment Options

Payment links support multiple payment methods:

| Method | Description |
| --- | --- |
| Card | Debit/credit card (Verve, Visa, Mastercard) |
| Bank Transfer | Direct bank transfer |
| USSD | USSD banking codes |
| QR Code | Scan-to-pay |

## Webhooks for Payment Links

Payment link events are delivered via webhooks:

- `PAYMENT_LINK.CREATED` — Link generated
- `PAYMENT_LINK.COMPLETED` — Payment received via link

See `interswitch-webhooks` skill for webhook setup.

## Best Practices

1. **Set expiry dates** for one-time payment links
2. **Use metadata** to link payments back to your system records
3. **Monitor active links** — Deactivate expired or unused links
4. **Implement redirect handling** — Always verify payment server-side on redirect
5. **Track collections** — Use `totalCollected` and `paymentCount` for reporting
