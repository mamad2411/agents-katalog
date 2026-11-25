---
name: tpl-situacao-integracao-api-terceiros
description: Template do pack (situacao/09-integracao-api-terceiros.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/09-integracao-api-terceiros.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Third-Party API Integration

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/09-integracao-api-terceiros.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when integrating external APIs — payment gateways (Stripe, PagSeguro), communication services (SendGrid, Twilio), OAuth providers, data providers, or any external system you consume but don't control. External APIs have versioned contracts, rate limits, downtime, and breaking changes. This configuration prevents those realities from cascading into your application.

## OBJECTIVES
- Integrate external APIs through a proper abstraction layer
- Handle every failure mode gracefully (rate limits, downtime, timeouts, 4xx/5xx)
- Make the integration testable without calling the real API
- Monitor for deprecation warnings and version changes
- Ensure webhook security when receiving events from third parties

## APPROACH RULES

1. **Anti-Corruption Layer (ACL) is mandatory.** Never call a third-party SDK or HTTP client directly from business logic. Wrap it in an adapter class that speaks your domain language. Example: `StripeClient.createCustomer()` wraps Stripe's SDK — your `OrderService` never imports Stripe directly.

2. **Map external errors to internal errors.** Stripe throws `StripeCardDeclinedError`. Your code throws `PaymentDeclinedError`. Internal code should never catch external SDK error classes.

3. **Every external call needs a timeout.** Network calls without timeouts hang forever. Default timeout: 5-10 seconds. Adjust per endpoint characteristics.

4. **Idempotency keys for all mutating calls.** Any POST that creates or modifies a resource must include an idempotency key. This prevents duplicate charges/orders if requests are retried.

5. **Retry with exponential backoff for transient failures.** Retry on 429 (rate limit) and 5xx errors. Do not retry on 4xx (client errors — they will keep failing). Cap at 3 retries with exponential backoff + jitter.

6. **Never store raw API responses.** Map them to your domain types immediately. If the third-party changes a field name, you update one place (the adapter).

7. **Webhook security is non-negotiable.** Verify webhook signatures. Reject requests without a valid signature. Replay attack prevention: check event timestamp is within 5 minutes.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| HTTP 429 Too Many Requests | Implement exponential backoff with jitter. Respect `Retry-After` header if present. Log throttling occurrences. |
| HTTP 503 / connection timeout | Retry up to 3 times. If still failing, throw `ExternalServiceUnavailableError` and activate fallback. |
| HTTP 401 Unauthorized | Do NOT retry. Token is invalid or expired. Handle token refresh flow or surface auth config error. |
| HTTP 400 Bad Request | Do NOT retry. A mapping/validation error on your side. Log the request body for debugging. |
| Webhook received | Verify signature FIRST before any processing. Respond HTTP 200 immediately, process async. |
| API deprecation warning in response headers | Create a ticket immediately. Never ignore `Deprecation` or `Sunset` headers. |
| No OpenAPI spec available | Write types manually from API docs. Add a note to re-check when the API version changes. |
| API requires OAuth flow | Implement token refresh automatically. Never require user to re-auth due to expired token. |
| Need to test integration | Use the sandbox/test environment during development. Use recorded fixtures (VCR/nock) for unit tests. |
| Third party data doesn't match your schema | Apply data normalization in the adapter. Never let invalid external data reach your database. |

## Adapter Pattern Template

```typescript
// External dependency isolated here only
import Stripe from 'stripe'

// Your domain types — no Stripe types leak out
export interface CreatePaymentResult {
  paymentId: string
  status: 'succeeded' | 'requires_action' | 'failed'
  errorCode?: string
}

export class PaymentGateway {
  private stripe: Stripe

  constructor(apiKey: string) {
    this.stripe = new Stripe(apiKey, { apiVersion: '2024-06-20' })
  }

  async createPayment(
    amountCents: number,
    currency: string,
    customerId: string,
    idempotencyKey: string
  ): Promise<CreatePaymentResult> {
    try {
      const intent = await this.stripe.paymentIntents.create(
        { amount: amountCents, currency, customer: customerId },
        { idempotencyKey }
      )
      return { paymentId: intent.id, status: 'succeeded' }
    } catch (err) {
      if (err instanceof Stripe.errors.StripeCardError) {
        return { paymentId: '', status: 'failed', errorCode: err.code }
      }
      throw new ExternalServiceError('PaymentGateway', err)
    }
  }
}
```

## Webhook Security Template

```typescript
// Stripe webhook signature verification
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature']
  
  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET)
  } catch (err) {
    return res.status(400).send(`Webhook signature verification failed: ${err.message}`)
  }
  
  // Respond immediately, process asynchronously
  res.status(200).json({ received: true })
  
  // Process in background
  processWebhookEvent(event).catch(logger.error)
})
```

## DO NOT

- **DO NOT** import third-party SDK classes directly in business logic or controllers
- **DO NOT** store raw third-party API responses in the database — map to your schema
- **DO NOT** log full request/response bodies that may contain PAN, CVV, or auth tokens
- **DO NOT** process a webhook before verifying its signature
- **DO NOT** make synchronous HTTP calls in request handlers — always async/await
- **DO NOT** ignore the `Deprecation` and `Sunset` headers in API responses
- **DO NOT** hardcode API endpoints (they change) — use SDK or configurable base URL
- **DO NOT** catch all errors and swallow them — map to domain errors and let them propagate

## OUTPUT FORMAT

For each third-party integration, produce:

**Integration Spec Document:**
```markdown
## Integration: [Service Name]

### SDK/Method
- SDK: stripe-node v14
- API Version: 2024-06-20 (pinned)
- Authentication: Secret key (env: STRIPE_SECRET_KEY)

### Adapter Class
- Location: src/infrastructure/payment/StripeGateway.ts
- Interface: src/domain/PaymentGateway.ts (interface definition)

### Operations Implemented
| Operation | Method | Idempotent? | Retry? |
|-----------|--------|-------------|--------|
| Create payment | POST /payment_intents | Yes (idempotency key) | No (card errors) |
| Refund | POST /refunds | Yes | Yes (network errors) |

### Error Mapping
| Stripe Error | Internal Error |
|-------------|----------------|
| StripeCardError | PaymentDeclinedError |
| StripeConnectionError | ExternalServiceUnavailableError |

### Testing Strategy
- Unit tests: mock PaymentGateway interface
- Integration tests: Stripe test mode with test cards
- Webhook tests: Stripe CLI `stripe trigger` command
```

## QUALITY GATES

- [ ] Zero direct third-party SDK imports outside the adapter layer
- [ ] All external calls have explicit timeouts configured
- [ ] All mutating external calls have idempotency keys
- [ ] Error mapping table documented (external error → internal error)
- [ ] Webhook signature verification implemented and tested
- [ ] Retry logic implemented with exponential backoff for transient errors
- [ ] Integration tests use sandbox/test environment (never production for tests)
- [ ] `Deprecation`/`Sunset` header monitoring in place (log warning)
- [ ] No secrets hardcoded — loaded from environment variables
- [ ] Adapter has 100% unit test coverage with mocked HTTP layer
