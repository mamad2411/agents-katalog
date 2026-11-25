---
name: interswitch-testing
description: >-
  Interswitch Testing — test credentials, test cards, sandbox URLs, environment
  switching, and testing strategies for all Interswitch APIs. Use this skill whenever
  testing Interswitch integrations, using test card numbers, configuring the sandbox
  environment, verifying payment flows with test data, or debugging test transactions.
  Also use when you see references to test credentials, sk_test_, sandbox URLs,
  test card numbers (5061050254756707864, 4000000000002503), or QA environments.
---

# Interswitch Testing Guide

Comprehensive testing guide with test credentials, test cards, sandbox URLs, and testing strategies.

## Test Environments

| Service | Test URL |
| --- | --- |
| Passport (OAuth) | `https://passport.k8.isw.la` |
| Collections | `https://qa.interswitchng.com` |
| Web Checkout | `https://newwebpay.qa.interswitchng.com` |
| Passport v2 (Collections) | `https://passport.k8.isw.la` |
| Wallet Services | `https://qa.interswitchng.com` |

| Service | Live URL |
| --- | --- |
| Passport (OAuth) | `https://passport.interswitchng.com` |
| Collections | `https://saturn.interswitchng.com` |
| Web Checkout | `https://newwebpay.interswitchng.com` |
| Passport v2 | `https://passport.interswitchng.com` |

## Test Credentials

### General Test Credentials

| Parameter | Value |
| --- | --- |
| Client ID | `IKIAB23A4E2756605C1ABC33CE3C287E27267F660D61` |
| Secret Key | `secret` |
| Pay Item ID | `9405967` |
| Merchant Code | `MX6072` |

### Card Payment API Credentials

| Parameter | Value |
| --- | --- |
| Client ID | `IKIA3B827951EA3EC2E193C51DA1D22988F055FD27DE` |
| Secret Key | `ajkdpGiF6PHVrwK` |
| Merchant Code | `MX21696` |
| Pay Item ID | `4177785` |

## Test Cards

### Verve Cards (Success)

| Card Number | Expiry | CVV | PIN | OTP |
| --- | --- | --- | --- | --- |
| `5061050254756707864` | 06/26 | 111 | 1111 | — |
| `5060990580000217499` | 03/50 | — | — | — |

### Visa Cards (Success)

| Card Number | Expiry | CVV | PIN | OTP |
| --- | --- | --- | --- | --- |
| `4000000000002503` | 03/50 | 111 | — | — |

### Mastercard (Success)

| Card Number | Expiry | CVV | PIN | OTP |
| --- | --- | --- | --- | --- |
| `5123450000000008` | 01/39 | 100 | 1111 | 123456 |

### Failure Test Cards

| Card Number | Scenario | Expected Response |
| --- | --- | --- |
| `5061050254756707865` | Timeout | Transaction timeout |
| `5061050254756707866` | Insufficient funds | Code: 51 |
| `5061050254756707867` | No card record | Card not found |

## Environment Configuration

```typescript
interface InterswitchConfig {
  environment: 'test' | 'live';
  clientId: string;
  secretKey: string;
  merchantCode: string;
  payItemId: string;
  passportUrl: string;
  collectionsBaseUrl: string;
  webCheckoutUrl: string;
}

function getConfig(): InterswitchConfig {
  const isLive = process.env.INTERSWITCH_ENVIRONMENT === 'live';

  return {
    environment: isLive ? 'live' : 'test',
    clientId: process.env.INTERSWITCH_CLIENT_ID!,
    secretKey: process.env.INTERSWITCH_SECRET_KEY!,
    merchantCode: process.env.INTERSWITCH_MERCHANT_CODE!,
    payItemId: process.env.INTERSWITCH_PAY_ITEM_ID!,
    passportUrl: isLive
      ? 'https://passport.interswitchng.com'
      : 'https://passport.k8.isw.la',
    collectionsBaseUrl: isLive
      ? 'https://saturn.interswitchng.com'
      : 'https://qa.interswitchng.com',
    webCheckoutUrl: isLive
      ? 'https://newwebpay.interswitchng.com'
      : 'https://newwebpay.qa.interswitchng.com',
  };
}
```

## .env.example

```env
# Interswitch Environment ('test' or 'live')
INTERSWITCH_ENVIRONMENT=test

# General Credentials
INTERSWITCH_CLIENT_ID=IKIAB23A4E2756605C1ABC33CE3C287E27267F660D61
INTERSWITCH_SECRET_KEY=secret
INTERSWITCH_MERCHANT_CODE=MX6072
INTERSWITCH_PAY_ITEM_ID=9405967

# Card Payment API Credentials (if using direct card API)
INTERSWITCH_CARD_CLIENT_ID=IKIA3B827951EA3EC2E193C51DA1D22988F055FD27DE
INTERSWITCH_CARD_SECRET_KEY=ajkdpGiF6PHVrwK
INTERSWITCH_CARD_MERCHANT_CODE=MX21696
INTERSWITCH_CARD_PAY_ITEM_ID=4177785

# Webhook
INTERSWITCH_WEBHOOK_SECRET=your_webhook_secret_here

# Wallet (optional)
INTERSWITCH_WALLET_BASE_URL=https://qa.interswitchng.com
```

## Testing Web Checkout

```typescript
// Use test credentials with web checkout
const testCheckoutConfig = {
  merchant_code: 'MX6072',
  pay_item_id: '9405967',
  txn_ref: `TEST_${Date.now()}`,
  amount: 10000,           // ₦100.00 (100 * 100 kobo)
  currency: 566,           // NGN
  site_redirect_url: 'http://localhost:3000/callback',
  mode: 'TEST',
};
```

## Testing Card Payments

```typescript
// Test Mastercard flow (with PIN + OTP)
const testCardPayment = {
  customerId: '1234567890',
  amount: '10000',
  currency: '566',
  transactionRef: `CARD_TEST_${Date.now()}`,
  // Encrypt test card: 5123450000000008, PIN: 1111, Expiry: 3901, CVV: 100
};

// Expected flow:
// 1. Submit payment → responseCode: 'T0' (OTP required)
// 2. Submit OTP '123456' → responseCode: '00' (Success)
```

## Testing Transfers

```typescript
// Test account validation
const testValidation = {
  bankCode: '058',            // GTBank test
  accountNumber: '0123456789', // Test account
};

// Test single transfer
const testTransfer = {
  amount: 100000,              // ₦1,000
  currency: 'NGN',
  // Use test bank codes and accounts
};
```

## Testing Webhooks Locally

Use a tunnel service to receive webhooks during local development:

```bash
# Using ngrok
npx ngrok http 3000

# Your webhook URL becomes: https://abc123.ngrok.io/api/webhooks/interswitch
```

### Manual Webhook Testing

```typescript
// Simulate a webhook payload for testing
const testWebhookPayload = {
  eventType: 'TRANSACTION.COMPLETED',
  eventId: `evt_${Date.now()}`,
  timestamp: new Date().toISOString(),
  data: {
    transactionRef: 'TEST_REF_123',
    amount: 10000,
    currency: 'NGN',
    responseCode: '00',
    responseDescription: 'Approved by Financial Institution',
  },
};

// Generate test signature
const testSignature = crypto
  .createHmac('sha512', process.env.INTERSWITCH_WEBHOOK_SECRET!)
  .update(JSON.stringify(testWebhookPayload))
  .digest('hex');

// Send test webhook
await fetch('http://localhost:3000/api/webhooks/interswitch', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Interswitch-Signature': testSignature,
  },
  body: JSON.stringify(testWebhookPayload),
});
```

## Going Live Checklist

- [ ] Replace test credentials with live credentials
- [ ] Update environment to `live` in .env
- [ ] Verify all URLs point to production endpoints
- [ ] Test with small real transactions first
- [ ] Set up webhook URL on live Quickteller Business account
- [ ] Enable proper error logging and monitoring
- [ ] Configure SSL/TLS on your server
- [ ] Implement rate limiting
- [ ] Set up transaction reconciliation
- [ ] Remove test card numbers from any hardcoded locations
