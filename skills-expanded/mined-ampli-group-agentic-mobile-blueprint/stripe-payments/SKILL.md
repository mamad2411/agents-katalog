---
name: stripe-payments
description: Integrate Stripe payments into the app — products, prices, checkout sessions, webhooks, customer portal, and subscription management. Use when setting up payments from scratch, adding a new product/plan, configuring webhooks, or debugging payment flows.
---

# Stripe Payments

## Stack

- **Stripe SDK** (server-side): Supabase Edge Functions handle all Stripe API calls
- **Stripe.js** (client-side): Frontend and mobile use Stripe's hosted checkout or `@stripe/stripe-react-native`
- **Webhooks**: Stripe → Edge Function → Supabase DB (source of truth for subscription state)

Never put the Stripe secret key in frontend or mobile code. Only the **publishable key** goes client-side.

---

## Setup

### Install dependencies

```bash
# Frontend
cd frontend && npm install @stripe/stripe-js @stripe/react-stripe-js

# Mobile
cd mobile && npx expo install @stripe/stripe-react-native
```

### Environment variables

```bash
# supabase/functions/.env.local
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# frontend/.env.local
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# mobile/.env.local
EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

Get keys from [dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys).

---

## Products and Prices

Create products in the Stripe dashboard or via CLI. Products represent what you sell; prices represent how much and how often.

### Stripe Dashboard (manual, recommended for first setup)

1. [dashboard.stripe.com/products](https://dashboard.stripe.com/products) → **Add product**
2. Fill in name, description, image
3. Add pricing:
   - **One-time:** flat amount
   - **Recurring:** monthly/annual, amount
4. Copy the **Price ID** (`price_...`) — you'll reference this in code

### Via Stripe CLI (scriptable)

```bash
stripe products create --name="Pro Plan" --description="Full access"
stripe prices create \
  --product=prod_xxx \
  --unit-amount=999 \
  --currency=usd \
  --recurring[interval]=month
```

---

## Edge Function: Create Checkout Session

```typescript
// supabase/functions/create-checkout/index.ts
import Stripe from "npm:stripe@14";
import { createClient } from "npm:@supabase/supabase-js@2";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!);

Deno.serve(async (req) => {
  const { priceId, userId, returnUrl } = await req.json();

  const session = await stripe.checkout.sessions.create({
    mode: "subscription",           // or "payment" for one-time
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${returnUrl}?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: returnUrl,
    metadata: { userId },           // passed back in webhook
    allow_promotion_codes: true,
    billing_address_collection: "auto",
  });

  return new Response(JSON.stringify({ url: session.url }));
});
```

Redirect the user to `session.url` — Stripe handles the entire payment flow.

---

## Edge Function: Webhooks

Webhooks are how Stripe tells your app about payment events. **This is the source of truth — never trust client-side "payment successful" redirects.**

```typescript
// supabase/functions/stripe-webhook/index.ts
import Stripe from "npm:stripe@14";
import { createClient } from "npm:@supabase/supabase-js@2";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!);
const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET")!;

Deno.serve(async (req) => {
  const signature = req.headers.get("stripe-signature")!;
  const body = await req.text();

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch {
    return new Response("Invalid signature", { status: 400 });
  }

  const supabase = createClient(
    Deno.env.get("PUBLIC_SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object as Stripe.CheckoutSession;
      const userId = session.metadata?.userId;
      await supabase.from("subscriptions").upsert({
        user_id: userId,
        stripe_customer_id: session.customer as string,
        stripe_subscription_id: session.subscription as string,
        status: "active",
      });
      break;
    }
    case "customer.subscription.updated":
    case "customer.subscription.deleted": {
      const sub = event.data.object as Stripe.Subscription;
      await supabase.from("subscriptions")
        .update({ status: sub.status })
        .eq("stripe_subscription_id", sub.id);
      break;
    }
  }

  return new Response(JSON.stringify({ received: true }));
});
```

**Key events to handle:**
- `checkout.session.completed` — user paid, activate subscription
- `customer.subscription.updated` — plan changed, update status
- `customer.subscription.deleted` — cancelled, downgrade access
- `invoice.payment_failed` — payment failed, notify user

---

## Webhook Setup

### Local development

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local edge function
stripe listen --forward-to http://localhost:54321/functions/v1/stripe-webhook

# Copy the webhook signing secret printed by the CLI → STRIPE_WEBHOOK_SECRET in .env.local
```

### Production

1. [dashboard.stripe.com/webhooks](https://dashboard.stripe.com/webhooks) → **Add endpoint**
2. Endpoint URL: `https://YOUR_PROJECT.supabase.co/functions/v1/stripe-webhook`
3. Events to send: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`
4. Copy **Signing secret** (`whsec_...`) → add to Supabase secrets:

```bash
supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## Customer Portal

Let users manage their subscription (cancel, update payment method, change plan):

```typescript
// supabase/functions/create-portal-session/index.ts
const session = await stripe.billingPortal.sessions.create({
  customer: stripeCustomerId,   // from your subscriptions table
  return_url: returnUrl,
});
return new Response(JSON.stringify({ url: session.url }));
```

Enable and configure the portal: [dashboard.stripe.com/settings/billing/portal](https://dashboard.stripe.com/settings/billing/portal)
- Set which plans users can switch to
- Enable/disable cancellation
- Configure cancellation flow (survey, retention offers)

---

## Database Schema

```sql
create table subscriptions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users not null,
  stripe_customer_id text unique,
  stripe_subscription_id text unique,
  stripe_price_id text,
  status text not null default 'inactive',  -- active | past_due | canceled | trialing
  current_period_end timestamptz,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- RLS: users can read their own subscription
alter table subscriptions enable row level security;
create policy "users read own" on subscriptions for select using (auth.uid() = user_id);
```

---

## Test Cards

| Card | Scenario |
|------|----------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0025 0000 3155` | Requires 3D Secure |
| `4000 0000 0000 9995` | Declined |
| `4000 0000 0000 0341` | Attaches successfully but payment always fails |

Any future expiry, any CVC, any postal code.

---

## Go Live Checklist

- [ ] Switch from `sk_test_` to `sk_live_` keys in Supabase secrets
- [ ] Switch publishable key to `pk_live_` in frontend/mobile env
- [ ] Create new webhook endpoint pointing to production (test and live webhooks are separate)
- [ ] Verify products/prices exist in live mode (test mode data doesn't carry over)
- [ ] Test a real payment with a real card
- [ ] Enable Radar fraud rules: [dashboard.stripe.com/radar/rules](https://dashboard.stripe.com/radar/rules)

---

## Gotchas

**Webhook signature verification fails** — The webhook secret for local CLI (`whsec_...` from `stripe listen`) is different from the production dashboard secret. Use the right one per environment.

**Missing `SUPABASE_SERVICE_ROLE_KEY`** — Webhook handler must use the service role key to bypass RLS when writing subscription data. The publishable key won't work.

**Duplicate webhook events** — Stripe can deliver the same event more than once. Use `upsert` instead of `insert`, or check for existing records before writing.

**Subscription not activating** — Webhook is not reaching the function. Check Stripe dashboard → Webhooks → Recent deliveries for errors.

**Apple/Google take 30% cut on mobile** — If your app sells digital goods or subscriptions through the mobile app, Apple and Google require you to use their in-app purchase system (not Stripe). Stripe is fine for web checkout. This is the "App Store tax" — plan around it.
