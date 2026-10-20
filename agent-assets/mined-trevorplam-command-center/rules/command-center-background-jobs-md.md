---
description: Run Background Jobs and Concurrency Checks
globs: ['**/jobs/**/*.ts', '**/workers/**/*.ts', '**/queues/**/*.ts', '**/webhooks/**/*.ts']
---

# Infrastructure: Background Jobs & Concurrency

<audit_rules>

- You MUST verify that background jobs are processed asynchronously via a durable queue (e.g., Redis/BullMQ), NEVER using synchronous `setTimeout` or blocking request threads.
- You MUST ensure every job has robust retry logic with exponential backoff for transient failures.
- You MUST implement a dead-letter queue (DLQ) for jobs that fail consistently after maximum retries.
- You MUST verify idempotency keys are used for critical operations (e.g., payment processing) to prevent duplicate execution during retries.
- You MUST ensure webhook endpoints acknowledge receipt immediately (HTTP 200) and offload the actual processing to a background job.
- You MUST enforce concurrency controls to respect third-party API rate limits (e.g., Resend, Stripe) when processing batches.
  </audit_rules>

<example_good>

```typescript
// Webhook handler offloading to a queue
export async function POST(req: Request) {
  const payload = await req.json()
  const signature = req.headers.get('stripe-signature')

  // Verify signature and push to queue, return 200 immediately
  await paymentQueue.add('process-webhook', payload, {
    jobId: payload.id, // Idempotency key
    attempts: 3,
    backoff: { type: 'exponential', delay: 1000 },
  })

  return NextResponse.json({ received: true })
}
```

</example_good>

<example_bad>

```typescript
// BAD: Processing webhook synchronously and blocking
export async function POST(req: Request) {
  const payload = await req.json()

  // If this takes >10s, Stripe will timeout and retry, causing duplicates
  await processHeavyDatabaseOperation(payload)
  await sendWelcomeEmail(payload)

  return NextResponse.json({ success: true })
}
```

</example_bad>
