---
name: interswitch-card-payments
description: >-
  Interswitch Card Payments API — process card transactions directly via API, handle
  3D Secure (Visa/Mastercard), Hosted Fields for PCI compliance, and Google Pay.
  Use this skill whenever building a custom card payment flow, implementing 3D Secure
  authentication, using Hosted Fields for PCI-compliant card collection, integrating
  Google Pay, or processing direct card charges. Also use when you see references to
  authData, 3DSecure, OTP validation, Hosted Fields, payment-api endpoint, or card
  PIN/OTP submission.
---

# Interswitch Card Payments API

Process card payments directly via the Interswitch API with 3D Secure support, Hosted Fields, and Google Pay integration.

## Card Payment Flow

1. Collect card details (PAN, expiry, CVV, PIN)
2. Encrypt card data into `authData`
3. Send payment request with encrypted authData
4. Handle OTP/3D Secure if required
5. Verify transaction server-side

## Test Credentials (Card Payment API)

| Parameter | Value |
| --- | --- |
| Client ID | `IKIA3B827951EA3EC2E193C51DA1D22988F055FD27DE` |
| Secret Key | `ajkdpGiF6PHVrwK` |
| Merchant Code | `MX21696` |
| Pay Item ID | `4177785` |

## Card Data Encryption (authData)

Card details must be encrypted before transmission. The `authData` is a concatenation of card PAN, PIN, expiry, and CVV encrypted with the Interswitch modulus/exponent:

```typescript
import crypto from 'crypto';

interface CardDetails {
  pan: string;       // Card number (no spaces)
  pin: string;       // 4-digit PIN
  expiryDate: string; // YYMM format
  cvv: string;       // CVV/CVC
}

function generateAuthData(card: CardDetails): string {
  // Concatenate: 1PAN + 0PIN + EXPIRY + CVV (with length-prefixed fields)
  const cardData = `1${card.pan}0${card.pin}${card.expiryDate}${card.cvv}`;

  // Use Interswitch's public key for encryption
  // Get the actual modulus and exponent from Interswitch documentation
  const publicKey = crypto.createPublicKey({
    key: {
      kty: 'RSA',
      n: '<INTERSWITCH_MODULUS_BASE64URL>',
      e: 'AQAB', // 65537
    },
    format: 'jwk',
  });

  const encrypted = crypto.publicEncrypt(
    { key: publicKey, padding: crypto.constants.RSA_PKCS1_PADDING },
    Buffer.from(cardData)
  );

  return encrypted.toString('base64');
}
```

## Direct Card Payment

```typescript
interface CardPaymentRequest {
  customerId: string;
  amount: string;          // In minor currency (kobo)
  currency: string;        // '566' for NGN
  transactionRef: string;
  authData: string;        // Encrypted card data
}

interface CardPaymentResponse {
  amount: string;
  responseCode: string;
  responseDescription: string;
  paymentId: string;
  transactionRef: string;
  remittanceAmount: string;
  eciFlag?: string;
  message?: string;
}

async function initiateCardPayment(
  payment: CardPaymentRequest
): Promise<CardPaymentResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${getConfig().collectionsBaseUrl}/collections/api/v1/pay`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify(payment),
    }
  );

  return response.json();
}
```

## Handle OTP Validation

If `responseCode` is `T0` (OTP required):

```typescript
interface OTPValidationRequest {
  paymentId: string;
  transactionRef: string;
  otp: string;
}

async function validateOTP(
  request: OTPValidationRequest
): Promise<CardPaymentResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${getConfig().collectionsBaseUrl}/collections/api/v1/pay/validate`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify(request),
    }
  );

  return response.json();
}
```

## 3D Secure Transactions

For Visa/Mastercard 3D Secure:

```typescript
// Step 1: Initiate payment — if 3DS required, response includes:
// - responseCode: 'Z9' or 'S0'
// - eciFlag with redirect info

interface ThreeDSecureResponse {
  responseCode: string;
  redirectUrl: string;     // Redirect customer to this URL
  transactionId: string;
  md: string;              // Merchant Data for callback
}

// Step 2: Customer completes 3DS on bank's page
// Step 3: Bank redirects back to your callback URL
// Step 4: Complete the transaction

async function complete3DSTransaction(
  paymentId: string,
  transactionRef: string,
  eciFlag: string
): Promise<CardPaymentResponse> {
  const headers = await getAuthHeaders();

  const response = await fetch(
    `${getConfig().collectionsBaseUrl}/collections/api/v1/pay/validate`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify({ paymentId, transactionRef, eciFlag }),
    }
  );

  return response.json();
}
```

## Hosted Fields (PCI Compliant)

Hosted Fields let you collect card data securely without handling raw card numbers. Interswitch hosts the input fields in iframes:

```html
<!-- Include Hosted Fields SDK -->
<script src="https://newwebpay.qa.interswitchng.com/hosted-fields.js"></script>

<div id="card-number"></div>
<div id="card-expiry"></div>
<div id="card-cvv"></div>
<div id="card-pin"></div>

<button id="submit-payment">Pay</button>

<script>
const hostedFields = window.interswitchHostedFields({
  merchantCode: 'MX6072',
  payItemId: '9405967',
  transactionRef: 'TXN_' + Date.now(),
  amount: 10000,
  currency: 566,
  mode: 'TEST',
  fields: {
    cardNumber: { selector: '#card-number', placeholder: 'Card Number' },
    expirationDate: { selector: '#card-expiry', placeholder: 'MM/YY' },
    cvv: { selector: '#card-cvv', placeholder: 'CVV' },
    pin: { selector: '#card-pin', placeholder: 'PIN' },
  },
  onComplete: function (response) {
    console.log(response);
  },
});

document.getElementById('submit-payment').addEventListener('click', () => {
  hostedFields.submit();
});
</script>
```

## Google Pay Integration

```typescript
// Step 1: Check Google Pay availability
const paymentsClient = new google.payments.api.PaymentsClient({
  environment: 'TEST', // or 'PRODUCTION'
});

const isReadyToPayRequest = {
  apiVersion: 2,
  apiVersionMinor: 0,
  allowedPaymentMethods: [{
    type: 'CARD',
    parameters: {
      allowedAuthMethods: ['PAN_ONLY', 'CRYPTOGRAM_3DS'],
      allowedCardNetworks: ['VISA', 'MASTERCARD'],
    },
    tokenizationSpecification: {
      type: 'PAYMENT_GATEWAY',
      parameters: {
        gateway: 'interswitch',
        gatewayMerchantId: 'MX6072',
      },
    },
  }],
};

// Step 2: Request payment
const paymentDataRequest = {
  ...isReadyToPayRequest,
  transactionInfo: {
    totalPriceStatus: 'FINAL',
    totalPrice: '100.00',
    currencyCode: 'NGN',
  },
  merchantInfo: { merchantName: 'Your Store' },
};

const paymentData = await paymentsClient.loadPaymentData(paymentDataRequest);
// Step 3: Send paymentData.paymentMethodData.tokenizationData.token to your server
// Step 4: Process token via Interswitch API
```

## Security Best Practices

1. **Never log raw card data** — Only handle encrypted authData
2. **Use Hosted Fields** when possible for PCI compliance
3. **Always verify server-side** — Requery every transaction
4. **Handle all response codes** — Implement proper error flows for OTP, 3DS
5. **Use unique transaction references** — Prevent duplicate charges
