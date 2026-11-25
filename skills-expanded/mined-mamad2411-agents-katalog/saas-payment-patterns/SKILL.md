---
name: saas-payment-patterns
description: Payment provider abstraction, webhook security, subscription lifecycle, dunning flows, pricing models, invoicing, tax handling, and refund patterns for SaaS applications.
---

# SaaS Payment Patterns

Provider-agnostic payment patterns for subscription-based applications. Works with Stripe, Paddle, LemonSqueezy, or any billing provider.

## Payment Provider Abstraction Layer

```typescript
// Abstract away the provider — swap Stripe for Paddle without touching business logic

interface PaymentProvider {
  createCustomer(data: CreateCustomerDto): Promise<Customer>
  createSubscription(data: CreateSubscriptionDto): Promise<Subscription>
  cancelSubscription(subscriptionId: string, immediate?: boolean): Promise<void>
  createCheckoutSession(data: CheckoutDto): Promise<{ url: string }>
  issueRefund(paymentId: string, amountCents?: number): Promise<Refund>
  getInvoice(invoiceId: string): Promise<Invoice>
  verifyWebhookSignature(payload: string, signature: string): boolean
}

interface Customer { id: string; email: string; providerCustomerId: string }
interface Subscription {
  id: string
  status: SubscriptionStatus
  planId: string
  currentPeriodEnd: Date
  cancelAtPeriodEnd: boolean
}
type SubscriptionStatus = 'trialing' | 'active' | 'past_due' | 'canceled' | 'expired'

// Provider implementation (Stripe example)
class StripePaymentProvider implements PaymentProvider {
  constructor(private stripe: Stripe) {}

  async createCustomer(data: CreateCustomerDto): Promise<Customer> {
    const stripeCustomer = await this.stripe.customers.create({
      email: data.email,
      metadata: { internalUserId: data.userId }
    })
    return {
      id: data.userId,
      email: data.email,
      providerCustomerId: stripeCustomer.id
    }
  }

  // ... other methods follow the same translation pattern
}

// Usage — business logic never imports Stripe/Paddle directly
class BillingService {
  constructor(private provider: PaymentProvider, private db: Database) {}

  async startSubscription(userId: string, planId: string): Promise<Subscription> {
    const customer = await this.db.customers.findByUserId(userId)
    return this.provider.createSubscription({
      customerId: customer.providerCustomerId,
      planId,
      trialDays: 14
    })
  }
}
```

## Webhook Security

```typescript
// GOOD: Verify signature, enforce idempotency, protect against replay
async function handleWebhook(req: Request): Promise<Response> {
  const payload = await req.text()
  const signature = req.headers.get('x-webhook-signature') ?? ''
  const eventId = req.headers.get('x-webhook-id') ?? ''
  const timestamp = req.headers.get('x-webhook-timestamp') ?? ''

  // 1. Verify cryptographic signature
  if (!provider.verifyWebhookSignature(payload, signature)) {
    return new Response('Invalid signature', { status: 401 })
  }

  // 2. Replay protection — reject events older than 5 minutes
  const timestampMs = new Date(timestamp).getTime()
  if (isNaN(timestampMs)) {
    return new Response('Invalid timestamp', { status: 400 })
  }
  const eventAge = Date.now() - timestampMs
  if (eventAge > 5 * 60 * 1000 || eventAge < -60 * 1000) {
    return new Response('Event too old or clock skew', { status: 400 })
  }

  // 3. Idempotency — process each event exactly once
  const alreadyProcessed = await db.webhookEvents.findUnique({
    where: { eventId }
  })
  if (alreadyProcessed) {
    return new Response('Already processed', { status: 200 })
  }

  // 4. Process inside a transaction
  await db.$transaction(async (tx) => {
    await tx.webhookEvents.create({
      data: { eventId, payload, processedAt: new Date() }
    })
    const event = JSON.parse(payload)
    await routeWebhookEvent(event, tx)
  })

  return new Response('OK', { status: 200 })
}

// BAD: Fire-and-forget webhook handler
async function handleWebhookBad(req: Request): Promise<Response> {
  const event = await req.json()      // No signature verification
  await processEvent(event)            // No idempotency check
  return new Response('OK')            // No replay protection
  // Result: anyone can POST fake events, duplicate processing, replay attacks
}
```

## Subscription Lifecycle

```typescript
// State machine: trialing -> active -> past_due -> canceled -> expired
//                                  \-> canceled (voluntary)

type LifecycleEvent =
  | { type: 'trial_started'; trialEndsAt: Date }
  | { type: 'trial_converted' }
  | { type: 'payment_succeeded' }
  | { type: 'payment_failed'; attemptNumber: number }
  | { type: 'subscription_canceled'; reason: string }
  | { type: 'subscription_expired' }

async function handleLifecycleEvent(
  subscriptionId: string,
  event: LifecycleEvent,
  tx: Transaction
): Promise<void> {
  const sub = await tx.subscriptions.findUniqueOrThrow({
    where: { id: subscriptionId }
  })

  switch (event.type) {
    case 'trial_started':
      await tx.subscriptions.update({
        where: { id: subscriptionId },
        data: { status: 'trialing', trialEndsAt: event.trialEndsAt }
      })
      await scheduleEmail(sub.userId, 'trial-welcome')
      await scheduleEmail(sub.userId, 'trial-ending-soon', {
        sendAt: subDays(event.trialEndsAt, 3)
      })
      break

    case 'payment_succeeded':
      await tx.subscriptions.update({
        where: { id: subscriptionId },
        data: { status: 'active', pastDueAt: null }
      })
      await clearDunningState(sub.userId, tx)
      break

    case 'payment_failed':
      await tx.subscriptions.update({
        where: { id: subscriptionId },
        data: { status: 'past_due', pastDueAt: new Date() }
      })
      await startDunningFlow(sub, event.attemptNumber, tx)
      break

    case 'subscription_canceled':
      await tx.subscriptions.update({
        where: { id: subscriptionId },
        data: { status: 'canceled', canceledAt: new Date(), cancelReason: event.reason }
      })
      await revokeAccess(sub.userId, sub.currentPeriodEnd, tx) // access until period end
      await scheduleEmail(sub.userId, 'cancellation-feedback')
      break

    case 'subscription_expired':
      await tx.subscriptions.update({
        where: { id: subscriptionId },
        data: { status: 'expired' }
      })
      await revokeAccessImmediate(sub.userId, tx)
      await scheduleEmail(sub.userId, 'win-back', { sendAt: addDays(new Date(), 7) })
      break
  }
}
```

## Dunning Flow (Failed Payment Recovery)

```typescript
// Dunning = systematic retry and communication when payment fails
// Goal: recover revenue before canceling

interface DunningConfig {
  retrySchedule: number[]     // days between retries
  gracePeriodDays: number     // total days before cancellation
  downgradeAfterDays: number  // days before downgrading to free tier
}

const defaultDunning: DunningConfig = {
  retrySchedule: [1, 3, 5, 7],     // retry on day 1, 3, 5, 7
  gracePeriodDays: 14,               // cancel after 14 days
  downgradeAfterDays: 7              // downgrade to free on day 7
}

async function startDunningFlow(
  sub: Subscription,
  attemptNumber: number,
  tx: Transaction
): Promise<void> {
  const config = defaultDunning

  // Email sequence based on attempt number
  const emailTemplates = [
    'payment-failed-soft',        // Attempt 1: "Your payment didn't go through"
    'payment-failed-update-card',  // Attempt 2: "Please update your card"
    'payment-failed-urgent',       // Attempt 3: "You will lose access soon"
    'payment-failed-final'         // Attempt 4: "Last chance before cancellation"
  ]

  const template = emailTemplates[Math.min(attemptNumber - 1, emailTemplates.length - 1)]
  await scheduleEmail(sub.userId, template)

  // Downgrade after threshold
  const daysSinceFailure = differenceInDays(new Date(), sub.pastDueAt!)
  if (daysSinceFailure >= config.downgradeAfterDays) {
    await downgradeToFree(sub.userId, tx)
    await scheduleEmail(sub.userId, 'downgraded-to-free')
  }

  // Cancel after grace period
  if (daysSinceFailure >= config.gracePeriodDays) {
    await provider.cancelSubscription(sub.providerSubscriptionId, true)
  }
}
```

## Pricing Model Patterns

```typescript
// Support multiple pricing models from a single schema

type PricingModel =
  | { type: 'flat'; amountCents: number }
  | { type: 'tiered'; tiers: PricingTier[] }
  | { type: 'per_seat'; pricePerSeatCents: number; includedSeats: number }
  | { type: 'usage_based'; unitPriceCents: number; metricKey: string }

interface PricingTier {
  upTo: number | null   // null = unlimited
  unitPriceCents: number
}

function calculateAmount(model: PricingModel, quantity: number): number {
  switch (model.type) {
    case 'flat':
      return model.amountCents

    case 'per_seat': {
      const billableSeats = Math.max(0, quantity - model.includedSeats)
      return billableSeats * model.pricePerSeatCents
    }

    case 'tiered': {
      let total = 0
      let remaining = quantity
      let previousLimit = 0
      for (const tier of model.tiers) {
        const tierLimit = tier.upTo ?? Infinity
        const tierCapacity = tierLimit - previousLimit
        const unitsInTier = Math.min(remaining, tierCapacity)
        total += unitsInTier * tier.unitPriceCents
        remaining -= unitsInTier
        previousLimit = tierLimit
        if (remaining <= 0) break
      }
      return total
    }

    case 'usage_based':
      return quantity * model.unitPriceCents
  }
}

// Example tier definition
const apiPricing: PricingModel = {
  type: 'tiered',
  tiers: [
    { upTo: 1000, unitPriceCents: 0 },       // first 1K free
    { upTo: 10000, unitPriceCents: 1 },       // next 9K at $0.01/call
    { upTo: null, unitPriceCents: 0.5 }       // above 10K at $0.005/call
  ]
}
```

## Invoice and Receipt Generation

```typescript
interface InvoiceLineItem {
  description: string
  quantity: number
  unitPriceCents: number
  amountCents: number
}

interface Invoice {
  id: string
  customerId: string
  status: 'draft' | 'open' | 'paid' | 'void'
  lineItems: InvoiceLineItem[]
  subtotalCents: number
  taxCents: number
  totalCents: number
  currency: string
  issuedAt: Date
  dueAt: Date
  paidAt: Date | null
  taxDetails: TaxDetails | null
}

async function generateInvoice(
  subscriptionId: string,
  periodStart: Date,
  periodEnd: Date
): Promise<Invoice> {
  const sub = await db.subscriptions.findUniqueOrThrow({
    where: { id: subscriptionId },
    include: { plan: true, customer: true }
  })

  const lineItems: InvoiceLineItem[] = [{
    description: `${sub.plan.name} (${formatDate(periodStart)} - ${formatDate(periodEnd)})`,
    quantity: 1,
    unitPriceCents: sub.plan.priceCents,
    amountCents: sub.plan.priceCents
  }]

  // Add usage-based line items if applicable
  if (sub.plan.pricing.type === 'usage_based') {
    const usage = await getUsageForPeriod(sub.id, periodStart, periodEnd)
    const usageAmount = calculateAmount(sub.plan.pricing, usage.total)
    lineItems.push({
      description: `API calls: ${usage.total} units`,
      quantity: usage.total,
      unitPriceCents: sub.plan.pricing.unitPriceCents,
      amountCents: usageAmount
    })
  }

  const subtotalCents = lineItems.reduce((sum, li) => sum + li.amountCents, 0)
  const taxDetails = await calculateTax(sub.customer, subtotalCents)

  return db.invoices.create({
    data: {
      customerId: sub.customerId,
      status: 'open',
      lineItems,
      subtotalCents,
      taxCents: taxDetails.taxAmountCents,
      totalCents: subtotalCents + taxDetails.taxAmountCents,
      currency: sub.plan.currency,
      issuedAt: new Date(),
      dueAt: addDays(new Date(), 30),
      paidAt: null,
      taxDetails
    }
  })
}
```

## Tax Handling (VAT/GST)

```typescript
// GOOD: Tax calculation abstracted, provider handles compliance
interface TaxDetails {
  taxable: boolean
  taxRate: number           // 0.20 for 20% VAT
  taxAmountCents: number
  taxType: 'vat' | 'gst' | 'sales_tax' | 'none'
  jurisdiction: string      // "EU-DE", "AU", "US-CA"
  reverseCharge: boolean    // B2B within EU with valid VAT ID
}

interface TaxProvider {
  calculateTax(customer: Customer, amountCents: number): Promise<TaxDetails>
  validateTaxId(taxId: string, country: string): Promise<boolean>
}

async function calculateTax(
  customer: Customer,
  amountCents: number
): Promise<TaxDetails> {
  // If customer has a valid tax ID and is B2B, reverse charge may apply
  if (customer.taxId) {
    const isValid = await taxProvider.validateTaxId(customer.taxId, customer.country)
    if (isValid && isReverseChargeEligible(customer.country, sellerCountry)) {
      return {
        taxable: false,
        taxRate: 0,
        taxAmountCents: 0,
        taxType: 'vat',
        jurisdiction: `EU-${customer.country}`,
        reverseCharge: true
      }
    }
  }

  return taxProvider.calculateTax(customer, amountCents)
}

// Key rules:
// - Store tax details on every invoice (audit trail)
// - B2C in EU: charge VAT at customer country rate
// - B2B in EU with valid VAT ID: reverse charge (0% VAT)
// - US: sales tax varies by state, use a tax API
// - Let the payment provider (Stripe Tax, Paddle) handle compliance when possible
```

## Refund and Proration

```typescript
interface RefundResult {
  refundId: string
  amountCents: number
  reason: string
  prorated: boolean
}

async function processRefund(
  subscriptionId: string,
  requestingUserId: string,
  reason: string,
  fullRefund: boolean
): Promise<RefundResult> {
  const sub = await db.subscriptions.findUniqueOrThrow({
    where: { id: subscriptionId },
    include: { latestInvoice: true, customer: true }
  })

  // SECURITY: Verify the requesting user owns this subscription
  if (sub.customer.userId !== requestingUserId) {
    throw new AuthError('Not authorized to refund this subscription')
  }

  let refundAmountCents: number
  let prorated = false

  if (fullRefund) {
    refundAmountCents = sub.latestInvoice.totalCents
  } else {
    // Prorate: refund unused portion of current period
    const totalDays = differenceInDays(sub.currentPeriodEnd, sub.currentPeriodStart)
    const usedDays = differenceInDays(new Date(), sub.currentPeriodStart)
    const unusedRatio = Math.max(0, (totalDays - usedDays) / totalDays)
    refundAmountCents = Math.round(sub.latestInvoice.totalCents * unusedRatio)
    prorated = true
  }

  const refund = await provider.issueRefund(
    sub.latestInvoice.providerPaymentId,
    refundAmountCents
  )

  await db.refunds.create({
    data: {
      subscriptionId,
      invoiceId: sub.latestInvoice.id,
      amountCents: refundAmountCents,
      reason,
      prorated,
      providerRefundId: refund.id,
      processedAt: new Date()
    }
  })

  return {
    refundId: refund.id,
    amountCents: refundAmountCents,
    reason,
    prorated
  }
}

// Plan change with proration
async function changePlan(
  subscriptionId: string,
  newPlanId: string
): Promise<void> {
  const sub = await db.subscriptions.findUniqueOrThrow({
    where: { id: subscriptionId },
    include: { plan: true }
  })
  const newPlan = await db.plans.findUniqueOrThrow({ where: { id: newPlanId } })

  // Upgrade: charge prorated difference immediately
  // Downgrade: credit prorated difference to next invoice
  const isUpgrade = newPlan.priceCents > sub.plan.priceCents

  await provider.updateSubscription(sub.providerSubscriptionId, {
    planId: newPlan.providerPlanId,
    prorationBehavior: isUpgrade ? 'create_prorations' : 'always_invoice'
  })
}
```

## Webhook Event Routing

```typescript
// Map provider events to internal handlers — single entry point

type WebhookHandler = (data: unknown, tx: Transaction) => Promise<void>

const webhookHandlers: Record<string, WebhookHandler> = {
  'subscription.created':       handleSubscriptionCreated,
  'subscription.updated':       handleSubscriptionUpdated,
  'subscription.canceled':      handleSubscriptionCanceled,
  'invoice.paid':               handleInvoicePaid,
  'invoice.payment_failed':     handlePaymentFailed,
  'customer.updated':           handleCustomerUpdated,
  'refund.created':             handleRefundCreated
}

async function routeWebhookEvent(
  event: { type: string; data: unknown },
  tx: Transaction
): Promise<void> {
  const handler = webhookHandlers[event.type]

  if (!handler) {
    logger.warn(`Unhandled webhook event type: ${event.type}`)
    return  // Do not throw — acknowledge unknown events to prevent retries
  }

  await handler(event.data, tx)
}
```

## Common Pitfalls

```
Missing idempotency on webhooks:
  Providers retry failed deliveries. Without dedup, you charge or provision twice.
  -> Store eventId before processing, skip duplicates.

Trusting client-side plan selection:
  Never let the frontend decide the price. Always resolve plan + price server-side.
  -> Client sends planId, server looks up price from DB.

Forgetting to handle past_due:
  Users with failed payments keep accessing paid features indefinitely.
  -> Enforce access checks against subscription status, not just "has subscription."

Hardcoding tax rates:
  Tax rates change, new jurisdictions appear, VAT thresholds shift.
  -> Use a tax API or let your payment provider handle calculation.

No grace period on cancellation:
  Canceling immediately frustrates users who paid for a full period.
  -> Cancel at period end by default, revoke access only after the paid period.
```

**Remember**: Your payment provider is a dependency, not your architecture. Abstract it behind an interface so you can switch providers, run in test mode, or support multiple providers for different regions without rewriting business logic.
