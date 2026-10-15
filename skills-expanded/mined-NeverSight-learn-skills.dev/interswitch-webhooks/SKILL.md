---
name: interswitch-webhooks
description: >-
  Interswitch Webhooks — receive real-time event notifications for transactions,
  subscriptions, payment links, and invoices. Validate signatures with HmacSHA512,
  handle retry logic, and process all event types. Use this skill whenever setting
  up webhook endpoints, validating X-Interswitch-Signature headers, handling async
  payment confirmations, processing subscription lifecycle events, or debugging
  webhook delivery. Also use when you see references to X-Interswitch-Signature,
  HmacSHA512, webhook event types, or Quickteller Business webhook configuration.
---

# Interswitch Webhooks

Receive real-time event notifications for transactions, subscriptions, payment links, and invoices via webhook callbacks.

## Setup

Configure webhooks through the **Quickteller Business** dashboard:

1. Log in to Quickteller Business
2. Navigate to **Settings → Webhooks**
3. Enter your webhook URL (must be HTTPS)
4. Select event types to subscribe to
5. Copy your webhook secret key for signature verification

## Event Types

### Transaction Events

| Event | Description |
| --- | --- |
| `TRANSACTION.CREATED` | Transaction initiated |
| `TRANSACTION.UPDATED` | Transaction status changed |
| `TRANSACTION.COMPLETED` | Transaction finalized (success or failure) |

### Subscription Events

| Event | Description |
| --- | --- |
| `SUBSCRIPTION.CREATED` | New subscription created |
| `SUBSCRIPTION.TRANSACTION_SUCCESSFUL` | Subscription payment succeeded |
| `SUBSCRIPTION.TRANSACTION_FAILURE` | Subscription payment failed |
| `SUBSCRIPTION.CANCELLED` | Subscription cancelled |

### Payment Link Events

| Event | Description |
| --- | --- |
| `PAYMENT_LINK.CREATED` | Payment link generated |
| `PAYMENT_LINK.COMPLETED` | Payment via link completed |

### Invoice Events

| Event | Description |
| --- | --- |
| `INVOICE.CREATED` | Invoice generated |
| `INVOICE.PAID` | Invoice payment received |

## Webhook Payload Structure

```typescript
interface WebhookPayload {
  eventType: string;          // e.g., 'TRANSACTION.COMPLETED'
  eventId: string;            // Unique event identifier
  timestamp: string;          // ISO 8601 timestamp
  data: {
    transactionRef: string;
    amount: number;
    currency: string;
    responseCode: string;
    responseDescription: string;
    paymentReference?: string;
    customerEmail?: string;
    [key: string]: unknown;
  };
}
```

## Signature Verification (CRITICAL)

Every webhook request includes an `X-Interswitch-Signature` header containing an HmacSHA512 hash of the request body using your secret key.

**Always verify the signature before processing any webhook event.**

```typescript
import crypto from 'crypto';

function verifyWebhookSignature(
  body: string,            // Raw request body (NOT parsed JSON)
  signature: string,       // X-Interswitch-Signature header
  secretKey: string        // Your webhook secret key
): boolean {
  const hash = crypto
    .createHmac('sha512', secretKey)
    .update(body)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(hash),
    Buffer.from(signature)
  );
}
```

## Express.js Webhook Handler

```typescript
import express from 'express';
import crypto from 'crypto';

const app = express();

// CRITICAL: Use raw body for signature verification
app.post(
  '/webhooks/interswitch',
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    const signature = req.headers['x-interswitch-signature'] as string;
    const rawBody = req.body.toString();

    // 1. Verify signature
    if (!signature) {
      return res.status(401).end();
    }

    const isValid = verifyWebhookSignature(
      rawBody,
      signature,
      process.env.INTERSWITCH_WEBHOOK_SECRET!
    );

    if (!isValid) {
      return res.status(401).end();
    }

    // 2. Return 200 IMMEDIATELY (before processing)
    res.status(200).end();

    // 3. Process event asynchronously
    const event: WebhookPayload = JSON.parse(rawBody);
    await processWebhookEvent(event);
  }
);
```

## Next.js Route Handler

```typescript
// app/api/webhooks/interswitch/route.ts
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

export async function POST(request: NextRequest) {
  const rawBody = await request.text();
  const signature = request.headers.get('x-interswitch-signature');

  // Verify signature
  if (!signature) {
    return NextResponse.json({ error: 'Missing signature' }, { status: 401 });
  }

  const hash = crypto
    .createHmac('sha512', process.env.INTERSWITCH_WEBHOOK_SECRET!)
    .update(rawBody)
    .digest('hex');

  const isValid = crypto.timingSafeEqual(
    Buffer.from(hash),
    Buffer.from(signature)
  );

  if (!isValid) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  // Return 200 immediately
  const event: WebhookPayload = JSON.parse(rawBody);

  // Process asynchronously (queue recommended for production)
  processWebhookEvent(event).catch(console.error);

  return new NextResponse(null, { status: 200 });
}
```

## Event Processing

```typescript
async function processWebhookEvent(event: WebhookPayload): Promise<void> {
  // Idempotency check — prevent duplicate processing
  const alreadyProcessed = await checkEventProcessed(event.eventId);
  if (alreadyProcessed) return;

  switch (event.eventType) {
    case 'TRANSACTION.COMPLETED':
      await handleTransactionCompleted(event.data);
      break;

    case 'TRANSACTION.UPDATED':
      await handleTransactionUpdated(event.data);
      break;

    case 'SUBSCRIPTION.TRANSACTION_SUCCESSFUL':
      await handleSubscriptionPayment(event.data);
      break;

    case 'SUBSCRIPTION.CANCELLED':
      await handleSubscriptionCancelled(event.data);
      break;

    case 'INVOICE.PAID':
      await handleInvoicePaid(event.data);
      break;

    default:
      console.log('Unhandled event type:', event.eventType);
  }

  // Mark event as processed for idempotency
  await markEventProcessed(event.eventId);
}

async function handleTransactionCompleted(
  data: WebhookPayload['data']
): Promise<void> {
  if (data.responseCode === '00') {
    // Payment successful — fulfill order
    await fulfillOrder(data.transactionRef);
  } else {
    // Payment failed
    await markOrderFailed(data.transactionRef, data.responseDescription);
  }
}
```

## Retry Policy

| Behavior | Value |
| --- | --- |
| Max retries | 5 attempts |
| Retry condition | Non-200 HTTP response |
| Retry interval | Exponential backoff |
| Response requirement | HTTP 200 with no body |

**Critical**: Return HTTP 200 immediately with an empty body. Any other status code triggers retries.

## Best Practices

1. **Return 200 immediately** — Process events asynchronously
2. **Use raw body** for signature verification — Do NOT parse before verifying
3. **Implement idempotency** — Store processed event IDs to prevent duplicates
4. **Use timing-safe comparison** — `crypto.timingSafeEqual` prevents timing attacks
5. **Queue processing** — Use a job queue (Bull, BullMQ) for production workloads
6. **Log all events** — Store webhook payloads for debugging and audit
7. **Handle all event types** — Even if you only care about some, log the rest
8. **Set up monitoring** — Alert on high failure rates or missing events
