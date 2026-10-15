---
name: interswitch-web-checkout
description: >-
  Interswitch Web Checkout — Inline Checkout (JavaScript widget) and Web Redirect
  (HTML form POST) for accepting payments on your website. Use this skill whenever
  building a checkout page, integrating Interswitch payment gateway, implementing
  inline checkout popup, web redirect payments, handling payment callbacks, or
  confirming transaction status via server-side requery. Also use when you see
  references to webpayCheckout, inline-checkout.js, pay_item_id, merchant_code,
  or newwebpay URLs.
---

# Interswitch Web Checkout

Accept payments on your website using Interswitch's Web Checkout — either via the Inline Checkout JavaScript widget or the Web Redirect HTML form.

## Checkout Methods

| Method | How It Works | Best For |
| --- | --- | --- |
| **Inline Checkout** | JavaScript popup overlay on your page | Modern SPAs, no page redirect |
| **Web Redirect** | HTML form POST redirects to Interswitch | Traditional server-rendered apps |

## Payment Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| `merchant_code` | Your merchant code (e.g., `MX6072`) | Yes |
| `pay_item_id` | Payment item identifier (e.g., `9405967`) | Yes |
| `txn_ref` | Unique transaction reference (you generate) | Yes |
| `amount` | Amount in **minor currency** (kobo) — `10000` = ₦100 | Yes |
| `currency` | Currency code: `566` (NGN) | Yes |
| `cust_id` | Customer email or ID | Yes |
| `cust_name` | Customer name | No |
| `pay_item_name` | Item description | No |
| `site_redirect_url` | URL to redirect after payment | Web Redirect only |

## Test vs Live URLs

| Environment | URL |
| --- | --- |
| Test | `https://newwebpay.qa.interswitchng.com` |
| Live | `https://newwebpay.interswitchng.com` |

## Inline Checkout (Recommended)

### Include the Script

```html
<!-- Test -->
<script src="https://newwebpay.qa.interswitchng.com/inline-checkout.js"></script>

<!-- Live -->
<script src="https://newwebpay.interswitchng.com/inline-checkout.js"></script>
```

### Initialize Payment

```html
<button id="pay-btn">Pay ₦100</button>

<script>
document.getElementById('pay-btn').addEventListener('click', function () {
  const request = {
    merchant_code: 'MX6072',
    pay_item_id: '9405967',
    txn_ref: 'TXN_' + Date.now(),
    amount: 10000,            // ₦100 in kobo
    currency: 566,            // NGN
    cust_id: 'customer@email.com',
    onComplete: function (response) {
      console.log('Payment response:', response);
      // ALWAYS verify server-side before fulfilling order
      verifyTransaction(response.txnref);
    },
    mode: 'TEST'              // Remove for production
  };

  window.webpayCheckout(request);
});
</script>
```

### React/Next.js Integration

```typescript
'use client';

import { useEffect, useRef } from 'react';

declare global {
  interface Window {
    webpayCheckout: (request: InterswitchCheckoutRequest) => void;
  }
}

interface InterswitchCheckoutRequest {
  merchant_code: string;
  pay_item_id: string;
  txn_ref: string;
  amount: number;
  currency: number;
  cust_id: string;
  cust_name?: string;
  pay_item_name?: string;
  onComplete: (response: InterswitchPaymentResponse) => void;
  mode?: 'TEST' | 'LIVE';
}

interface InterswitchPaymentResponse {
  txnref: string;
  payRef: string;
  retRef: string;
  cardNum: string;
  apprAmt: number;
  resp: string;      // '00' = success
  desc: string;
}

function useInterswitchCheckout(isTest = true) {
  const loaded = useRef(false);

  useEffect(() => {
    if (loaded.current) return;
    const script = document.createElement('script');
    script.src = isTest
      ? 'https://newwebpay.qa.interswitchng.com/inline-checkout.js'
      : 'https://newwebpay.interswitchng.com/inline-checkout.js';
    script.async = true;
    document.body.appendChild(script);
    loaded.current = true;
  }, [isTest]);

  return (request: InterswitchCheckoutRequest) => {
    if (window.webpayCheckout) {
      window.webpayCheckout(request);
    }
  };
}

export default function CheckoutButton() {
  const checkout = useInterswitchCheckout(true);

  const handlePay = () => {
    checkout({
      merchant_code: 'MX6072',
      pay_item_id: '9405967',
      txn_ref: `TXN_${Date.now()}`,
      amount: 10000,
      currency: 566,
      cust_id: 'customer@email.com',
      onComplete: async (response) => {
        if (response.resp === '00') {
          // Verify server-side
          const result = await fetch('/api/verify-payment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ txnRef: response.txnref }),
          });
          const data = await result.json();
          if (data.verified) {
            // Fulfill order
          }
        }
      },
      mode: 'TEST',
    });
  };

  return <button onClick={handlePay}>Pay ₦100</button>;
}
```

## Web Redirect

### HTML Form POST

```html
<!-- Test URL -->
<form method="POST" action="https://newwebpay.qa.interswitchng.com/collections/w/pay">
  <input type="hidden" name="merchant_code" value="MX6072" />
  <input type="hidden" name="pay_item_id" value="9405967" />
  <input type="hidden" name="txn_ref" value="TXN_1234567890" />
  <input type="hidden" name="amount" value="10000" />
  <input type="hidden" name="currency" value="566" />
  <input type="hidden" name="cust_id" value="customer@email.com" />
  <input type="hidden" name="site_redirect_url" value="https://yoursite.com/payment/callback" />
  <button type="submit">Pay ₦100</button>
</form>
```

### Handle Redirect Callback

After payment, Interswitch redirects to your `site_redirect_url` with query params:

```typescript
// GET /payment/callback?txnref=TXN_123&payRef=FBN|WEB|...&retRef=000123&resp=00&apprAmt=10000
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const txnRef = request.nextUrl.searchParams.get('txnref');
  const resp = request.nextUrl.searchParams.get('resp');

  if (!txnRef) {
    return NextResponse.redirect('/payment/failed');
  }

  // ALWAYS requery — never trust redirect params alone
  const verified = await requeryTransaction(txnRef);

  if (verified.ResponseCode === '00') {
    // Fulfill order
    return NextResponse.redirect('/payment/success');
  }

  return NextResponse.redirect('/payment/failed');
}
```

## Server-Side Transaction Requery (CRITICAL)

NEVER rely solely on client-side callbacks. Always verify payment status server-side:

```typescript
interface RequeryResponse {
  Amount: number;
  ResponseCode: string;
  ResponseDescription: string;
  MerchantReference: string;
  PaymentReference: string;
  RetrievalReferenceNumber: string;
  TransactionDate: string;
}

async function requeryTransaction(txnRef: string): Promise<RequeryResponse> {
  const config = getConfig();
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${config.collectionsBaseUrl}/collections/api/v1/gettransaction.json` +
    `?merchantcode=${config.merchantCode}&transactionreference=${txnRef}&amount=0`,
    { headers }
  );

  if (!response.ok) {
    throw new Error(`Requery failed: ${response.status}`);
  }

  return response.json();
}
```

## Response Codes

| Code | Description |
| --- | --- |
| `00` | Approved / Successful |
| `Z0` | Transaction pending |
| `Z6` | Pending (OTP validation) |
| `Z8` | Pending (bank redirect) |
| `Z9` | Pending (3D Secure) |
| `51` | Insufficient funds |
| `54` | Expired card |
| `55` | Incorrect PIN |
| `91` | Issuer/switch inoperative |

## Security Best Practices

1. **Always requery server-side** — Client callbacks can be spoofed
2. **Generate unique txn_ref** — Use UUID or timestamp-based references
3. **Validate amount** — Compare requery amount with expected amount
4. **Use HTTPS** — All redirect URLs must be HTTPS in production
5. **Store transaction state** — Log all payment attempts in your database
