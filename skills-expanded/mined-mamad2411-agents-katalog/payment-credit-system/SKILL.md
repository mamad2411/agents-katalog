---
name: payment-credit-system
description: >
  Use this skill whenever implementing payment flows, credit deduction,
  subscription management, or Razorpay integration in Dukaan AI. Contains
  the exact plans, pricing, credit rules, Razorpay flow, and Worker API
  contract for payments.
---

# Dukaan AI — Payment & Credit System

## Plans Reference (Hard-coded in Flutter)

| Tier | Price | Monthly Ads | Key Features |
|---|---|---|---|
| Free | ₹0 | 3/month | Basic BG styles only |
| Dukaan | ₹99/month | 30/month | All BG styles, Hindi captions |
| Vyapaar | ₹199/month | 100/month | Everything + Khata + Catalogue |
| Utsav | ₹499/month | 500/month | Everything + bulk WhatsApp |

## Ad Packs (One-time Purchase)

| Pack | Price | Credits |
|---|---|---|
| Chhota | ₹29 | 10 ads |
| Bada | ₹59 | 25 ads |
| Super | ₹99 | 50 ads |

## Credit Rules

1. **1 credit = 1 ad generated** (background removal + background generation = 1 credit)
2. **Caption regeneration**: free (no credit deduction)
3. **Catalogue creation**: 2 credits
4. **UPI poster**: free
5. **Khata entry**: free
6. Monthly plans reset credits on billing anniversary, not calendar month
7. Free tier: 3 lifetime credits (no reset)

## Razorpay Payment Flow

### Step 1: Flutter requests order from Worker

```dart
// In PaymentRepository
final orderResponse = await cloudflareClient.post('/api/create-order', body: {
  'userId': userId,
  'planId': planId,          // 'dukaan_monthly' | 'ad_pack_chhota' etc.
  'amountPaise': amountPaise, // e.g. 9900 for ₹99
});
// Returns: { orderId, amount, currency: 'INR', keyId }
```

### Step 2: Flutter opens Razorpay checkout

```dart
// In RazorpayDatasource
final options = {
  'key': orderResponse.keyId,
  'order_id': orderResponse.orderId,
  'amount': orderResponse.amount,
  'currency': 'INR',
  'name': 'Dukaan AI',
  'description': planDisplayName,
  'prefill': {
    'contact': userPhone,
  },
  'theme': {'color': '#FF6F00'},
  'method': {'upi': true, 'card': false, 'netbanking': false, 'wallet': false},
};
_razorpay.open(options);
```

### Step 3: Flutter sends payment result to Worker for verification

```dart
// In PaymentRepository — called in _handlePaymentSuccess callback
final verifyResponse = await cloudflareClient.post('/api/verify-payment', body: {
  'userId': userId,
  'razorpayOrderId': payment.orderId,
  'razorpayPaymentId': payment.paymentId,
  'razorpaySignature': payment.signature,
});
// On success: Worker updates DB tier/credits, returns { success, newTier, newCredits }
```

### Step 4: Flutter invalidates providers

```dart
// After successful verification
ref.invalidate(profileProvider);    // refreshes credits + tier
ref.invalidate(pricingProvider);    // refreshes plan display
// Navigate to payment_success_screen
```

## Worker: create-order Contract

**Request** (POST `/api/create-order`):
```json
{
  "userId": "uuid",
  "planId": "dukaan_monthly",
  "amountPaise": 9900
}
```

**Response** (success):
```json
{
  "success": true,
  "data": {
    "orderId": "order_xxx",
    "amount": 9900,
    "currency": "INR",
    "keyId": "rzp_live_xxx"
  }
}
```

## Worker: verify-payment Contract

**Request** (POST `/api/verify-payment`):
```json
{
  "userId": "uuid",
  "razorpayOrderId": "order_xxx",
  "razorpayPaymentId": "pay_xxx",
  "razorpaySignature": "hmac_hex"
}
```

**Response** (success):
```json
{
  "success": true,
  "data": {
    "newTier": "dukaan",
    "newCredits": 30
  }
}
```

## CreditGuard Usage

Before any credit-consuming operation:

```dart
// lib/core/utils/credit_guard.dart
// Always call this before generateAd(), createCatalogue()
await CreditGuard.check(ref);
// Throws AppException.noCredits if credits_remaining == 0
// The exception is caught by AsyncValue.guard() and shows NoCreditsSheet
```

## Plan IDs (Exact Strings — Never Change)

```dart
// Used in API calls and DB
'free'
'dukaan_monthly'
'vyapaar_monthly'
'utsav_monthly'
'ad_pack_chhota'   // 10 credits, ₹29
'ad_pack_bada'     // 25 credits, ₹59
'ad_pack_super'    // 50 credits, ₹99
```

## Copilot Rules

1. **Never update credits_remaining directly from Flutter** — always via Worker verify-payment
2. **UPI-only checkout** — `method: { upi: true, card: false }` — target audience pays via UPI
3. **Always invalidate profileProvider after payment** — so credit display updates everywhere
4. **HMAC verification is mandatory** — never trust Flutter-side payment confirmation
5. **Insert pending transaction before Razorpay order** — so we have a record even if user closes app
