---
name: stripe-integration
description: >
  Trigger when the user wants to add Stripe payments to their app — subscriptions, one-time charges, webhooks, customer portal, or billing management. Also trigger for Stripe-related debugging, webhook verification, or migrating from another payment provider.
source:
  repository: armaneker/claude-code-skills
  original_path: saas-builder-kit/skills/stripe-integration
  original_name: stripe-integration
status: canonical
---
# Stripe Integration

You are an expert in Stripe's API and billing patterns. Generate working, production-safe Stripe integration code — not pseudocode.

## Workflow

1. **Identify the billing model:**
   - Subscriptions (recurring SaaS billing)
   - One-time payments (products, services)
   - Usage-based billing (metered)
   - Combination

2. **Identify the stack:** Next.js, Express, Fastify, other

3. **Check what already exists:** ask if they have a Stripe account, existing products/prices, or a customer model in the DB

## Setup

```bash
npm install stripe @stripe/stripe-js
```

```typescript
// lib/stripe.ts — singleton server-side client
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-06-20',
  typescript: true,
});
```

Required env vars:
```
STRIPE_SECRET_KEY=sk_live_...        # or sk_test_... for development
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
```

## Subscription Billing (Most Common SaaS Pattern)

### 1. Create Stripe Customer on User Signup

```typescript
// Called when a new user registers
export async function createStripeCustomer(user: { id: string; email: string; name: string }) {
  const customer = await stripe.customers.create({
    email: user.email,
    name: user.name,
    metadata: { userId: user.id },
  });

  // Save customer.id to your DB
  await db.user.update({
    where: { id: user.id },
    data: { stripeCustomerId: customer.id },
  });

  return customer;
}
```

### 2. Checkout Session (Subscription)

```typescript
// POST /api/billing/checkout
export async function createCheckoutSession(req: Request, res: Response) {
  const { priceId } = req.body;
  const user = req.user!;

  const session = await stripe.checkout.sessions.create({
    customer: user.stripeCustomerId,
    mode: 'subscription',
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.APP_URL}/billing/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.APP_URL}/billing`,
    subscription_data: {
      metadata: { userId: user.id },
    },
    allow_promotion_codes: true,
  });

  res.json({ url: session.url });
}
```

### 3. Customer Portal (Self-Service Billing)

```typescript
// POST /api/billing/portal
export async function createPortalSession(req: Request, res: Response) {
  const user = req.user!;

  const session = await stripe.billingPortal.sessions.create({
    customer: user.stripeCustomerId!,
    return_url: `${process.env.APP_URL}/settings/billing`,
  });

  res.json({ url: session.url });
}
```

### 4. One-Time Payment

```typescript
const session = await stripe.checkout.sessions.create({
  customer: user.stripeCustomerId,
  mode: 'payment',
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${process.env.APP_URL}/success`,
  cancel_url: `${process.env.APP_URL}/pricing`,
  payment_intent_data: {
    metadata: { userId: user.id, productId: priceId },
  },
});
```

## Webhook Handler (Critical — Do Not Skip)

The webhook is how your app learns about payment events. **Never trust the checkout redirect alone.**

```typescript
// POST /api/webhooks/stripe
import { buffer } from 'micro'; // or use express.raw()

export async function stripeWebhook(req: Request, res: Response) {
  const sig = req.headers['stripe-signature'] as string;
  const rawBody = req.body; // must be raw Buffer, not parsed JSON

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(rawBody, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    return res.status(400).send('Webhook Error');
  }

  // Handle events
  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;
      await handleCheckoutComplete(session);
      break;
    }
    case 'customer.subscription.updated': {
      const subscription = event.data.object as Stripe.Subscription;
      await handleSubscriptionUpdate(subscription);
      break;
    }
    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription;
      await handleSubscriptionDeleted(subscription);
      break;
    }
    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice;
      await handlePaymentFailed(invoice);
      break;
    }
  }

  res.json({ received: true });
}

async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId ?? session.subscription_data?.metadata?.userId;
  if (!userId) return;

  if (session.mode === 'subscription') {
    const subscription = await stripe.subscriptions.retrieve(session.subscription as string);
    await db.user.update({
      where: { id: userId },
      data: {
        subscriptionId: subscription.id,
        subscriptionStatus: subscription.status,
        planId: subscription.items.data[0].price.id,
        currentPeriodEnd: new Date(subscription.current_period_end * 1000),
      },
    });
  }
}

async function handleSubscriptionUpdate(subscription: Stripe.Subscription) {
  const userId = subscription.metadata.userId;
  await db.user.update({
    where: { stripeCustomerId: subscription.customer as string },
    data: {
      subscriptionStatus: subscription.status,
      planId: subscription.items.data[0].price.id,
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  });
}
```

**Next.js webhook setup** — disable body parsing for the webhook route:
```typescript
// app/api/webhooks/stripe/route.ts
export const runtime = 'nodejs'; // required for Buffer access

export async function POST(req: NextRequest) {
  const body = await req.text(); // raw string, not parsed
  const sig = req.headers.get('stripe-signature')!;
  // ... same verification logic
}
```

## Checking Subscription Status (Gate Features)

```typescript
export function isPremium(user: User): boolean {
  return (
    user.subscriptionStatus === 'active' ||
    user.subscriptionStatus === 'trialing'
  );
}

// Middleware
export const requirePremium = (req: AuthRequest, res: Response, next: NextFunction) => {
  if (!isPremium(req.user!)) {
    return res.status(402).json({ error: 'Premium subscription required' });
  }
  next();
};
```

## Common Pitfalls — Avoid These

- **Trusting the success redirect URL instead of webhooks** — the redirect can be skipped; webhooks are authoritative
- **Parsing the webhook body as JSON** — `stripe.webhooks.constructEvent` needs the raw Buffer/string
- **Not storing `stripeCustomerId` on your user** — you'll need it for every billing operation
- **Hardcoding price IDs** — store them in env vars (`STRIPE_PRICE_PRO_MONTHLY=price_xxx`)
- **Not handling `invoice.payment_failed`** — users in dunning need to be notified or downgraded
- **Missing idempotency keys on manual charges** — use `stripe.charges.create({ idempotencyKey: ... })` for retryable operations
- **Webhook handler returning 500** — Stripe retries for 3 days; always return 200 and handle errors internally

## Local Webhook Testing

```bash
stripe listen --forward-to localhost:3000/api/webhooks/stripe
# Prints a webhook secret — use it as STRIPE_WEBHOOK_SECRET in .env.local
stripe trigger checkout.session.completed
```

## Purpose
Add Stripe payments (subscriptions, one-time charges) to an app.

## When NOT to use
- Non-Stripe providers.

## Inputs
Plans/prices, stack, webhook endpoint.

## Output requirements
Checkout/subscription flow with verified webhooks.

## Example
```text
Create Checkout session for plan price; handle `invoice.paid` webhook.
```

## Related skills
stripe-integration-expert
