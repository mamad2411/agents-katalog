---
name: yookassa
description: Russian payment gateway integration using YooKassa. Use when creating payments, processing transactions, handling webhooks, managing refunds, or implementing Russian fiscalization via 54-FZ.
keywords: [payment, gateway, yookassa, russia, 54-fz, sbp]
---

# Yookassa Payment Gateway

## Quick Reference

| Concept | Details |
|---------|---------|
| **API Version** | v3 |
| **Base URL** | `https://api.yookassa.ru/v3` |
| **Auth** | Basic (shop_id:secret_key) |
| **Required Header** | `Idempotence-Key` (UUID v4, unique per operation) |
| **Primary SDK** | `@a2seven/yoo-checkout` |
| **Amount Format** | String with 2 decimals: `"100.00"` |
| **Currency** | `RUB` (primary), `USD`, `EUR` supported |

## When to Use

Use this skill when you need to:
- Create one-time or recurring payments
- Handle Russian payment methods (SBP, SberPay, YooMoney, T-Pay, Mir)
- Implement 54-FZ fiscalization (receipts)
- Process refunds and cancellations
- Handle async payment confirmation via webhooks
- Implement two-stage (hold + capture) payments
- Manage saved payment methods for returning customers

## Core Payment Flow

```
1. Create Payment → 2. Redirect User → 3. Webhook (status update) → 4. Verify → 5. Capture (if two-stage)
```

### One-Stage (Auto-Capture)
```
Create Payment (capture: true) → User Pays → Webhook: succeeded → Done
```

### Two-Stage (Hold + Capture)
```
Create Payment (capture: false) → User Pays → Webhook: waiting_for_capture → Capture Payment → Webhook: succeeded
```

## Payment Status Lifecycle

```
pending → waiting_for_capture → succeeded
                              → canceled
pending → succeeded (one-stage)
pending → canceled
```

## SDK Quick Start

```typescript
import { YooCheckout } from '@a2seven/yoo-checkout';

const checkout = new YooCheckout({
  shopId: process.env.YOOKASSA_SHOP_ID!,
  secretKey: process.env.YOOKASSA_SECRET_KEY!,
});
```

## Critical Rules

1. **Always use idempotency keys** - Every create/capture/cancel/refund needs a unique `Idempotence-Key`
2. **Never trust client-side** - Always verify payment status server-side via API or webhooks
3. **Amount is a string** - `{ value: "100.00", currency: "RUB" }` not a number
4. **Webhooks require 200 response** - Return HTTP 200 within 10 seconds or Yookassa retries
5. **Verify webhook IPs** - Whitelist Yookassa IP ranges for security
6. **54-FZ receipts** - Required for Russian merchants; include `receipt` object with items

## See Also

- `references/api-authentication.md` - Auth, headers, and idempotency details
- `references/sdk-types.md` - Complete TypeScript types, interfaces, and method signatures
- `references/payment-flow.md` - Complete lifecycle patterns and status transitions
- `references/payment-methods.md` - All payment method specs and configurations
- `references/webhooks.md` - Webhook security, events, and handling
- `references/receipts-fiscalization.md` - 54-FZ requirements and receipt formatting
- `references/error-handling.md` - HTTP codes, retries, and error patterns
- `examples/quick-start.ts` - Basic payment creation
- `examples/two-stage-payment.ts` - Hold and capture pattern
- `examples/webhook-handler.ts` - Express webhook endpoint
- `examples/refund-processing.ts` - Refund examples
