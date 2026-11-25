---
name: stripe-skill-generator
description: "Generate a project-specific payments skill for Stripe integration. Use when a project has stripe in integrations. Triggers on: generate stripe skill, create payment patterns, stripe-skill-generator."
type: meta
generates: payments
trigger:
  integration: stripe
---

# Stripe Skill Generator

Generate a project-specific `payments` skill that documents exactly how Stripe payments work in THIS project.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing Stripe implementation
3. Ask clarifying questions about payment patterns
4. Generate `docs/skills/payments/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Look for:
- Integration with name "stripe"
- `capabilities.payments: true`

---

## Step 2: Analyze Existing Stripe Implementation

```bash
# Find Stripe-related files
find . -type f \( -name "*stripe*" -o -name "*payment*" -o -name "*subscription*" \) | grep -v node_modules

# Find webhook handlers
find . -type f -name "*.ts" | xargs grep -l "stripe.*webhook\|webhook.*stripe" 2>/dev/null

# Find Stripe client initialization
grep -r "new Stripe\|stripe\(" --include="*.ts" | head -10

# Check for subscription logic
grep -r "subscription\|customer" --include="*.ts" | grep -i stripe | head -10
```

---

## Step 3: Clarifying Questions

```
I found the following Stripe patterns:

Payment Model: [one-time / subscription / both]
Webhook Handler: [path if found]
Stripe Client: [path if found]

Please confirm or correct:

1. What payment model do you use?
   A. Subscriptions only (SaaS)
   B. One-time payments only
   C. Both subscriptions and one-time
   D. Usage-based billing
   E. Mix

2. How is Stripe customer linked to user?
   A. stripe_customer_id on user record
   B. stripe_customer_id on organization
   C. Separate customers table
   D. Other: [specify]

3. What Stripe features do you use?
   A. Checkout Sessions (hosted checkout)
   B. Payment Intents (custom checkout)
   C. Customer Portal
   D. Billing Portal
   E. Multiple of above

4. How are webhooks handled?
   A. Single webhook endpoint
   B. Multiple endpoints by event type
   C. Third-party webhook service
```

---

## Step 4: Generate the Skill

Create `docs/skills/payments/SKILL.md`:

```markdown
---
name: payments
description: "Handle Stripe payments, subscriptions, and billing in [PROJECT_NAME]"
project-specific: true
generated-by: stripe-skill-generator
generated-at: [DATE]
---

# Payments Skill

How Stripe payments and subscriptions work in this project.

---

## Quick Reference

| Task | How |
|------|-----|
| Create checkout session | `createCheckoutSession()` |
| Get customer portal | `createPortalSession()` |
| Check subscription status | `getSubscriptionStatus()` |
| Handle webhook | `/api/webhooks/stripe` |

---

## Architecture

- **Payment Model:** [Subscriptions / One-time / Both]
- **Stripe Customer:** Linked to [User / Organization]
- **Checkout:** [Stripe Checkout / Custom]
- **Webhook Endpoint:** `[WEBHOOK_PATH]`

---

## Key Files

| File | Purpose |
|------|---------|
| `[STRIPE_CLIENT_PATH]` | Stripe client initialization |
| `[CHECKOUT_PATH]` | Checkout session creation |
| `[WEBHOOK_PATH]` | Webhook handler |
| `[SUBSCRIPTION_PATH]` | Subscription utilities |

---

## Creating a Checkout Session

### For Subscriptions

\`\`\`typescript
import { stripe } from '@/lib/stripe'
import { createClient } from '@/lib/supabase/server'

export async function createCheckoutSession(priceId: string) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  if (!user) throw new Error('Unauthorized')
  
  // Get or create Stripe customer
  let customerId = user.user_metadata.stripe_customer_id
  
  if (!customerId) {
    const customer = await stripe.customers.create({
      email: user.email,
      metadata: {
        user_id: user.id,
        organization_id: user.user_metadata.organization_id,
      },
    })
    customerId = customer.id
    
    // Save customer ID to user
    await supabase.auth.updateUser({
      data: { stripe_customer_id: customerId }
    })
  }
  
  const session = await stripe.checkout.sessions.create({
    customer: customerId,
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: \`\${process.env.NEXT_PUBLIC_URL}/billing?success=true\`,
    cancel_url: \`\${process.env.NEXT_PUBLIC_URL}/billing?canceled=true\`,
    metadata: {
      user_id: user.id,
      organization_id: user.user_metadata.organization_id,
    },
  })
  
  return session.url
}
\`\`\`

### For One-Time Payments

\`\`\`typescript
const session = await stripe.checkout.sessions.create({
  customer: customerId,
  mode: 'payment',
  payment_method_types: ['card'],
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: \`\${process.env.NEXT_PUBLIC_URL}/purchase/success\`,
  cancel_url: \`\${process.env.NEXT_PUBLIC_URL}/purchase/canceled\`,
})
\`\`\`

---

## Customer Portal

Let customers manage their subscription:

\`\`\`typescript
export async function createPortalSession() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  const customerId = user?.user_metadata.stripe_customer_id
  if (!customerId) throw new Error('No Stripe customer')
  
  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: \`\${process.env.NEXT_PUBLIC_URL}/billing\`,
  })
  
  return session.url
}
\`\`\`

---

## Webhook Handler

\`\`\`typescript
// [WEBHOOK_PATH]
import { NextRequest, NextResponse } from 'next/server'
import { stripe } from '@/lib/stripe'
import { headers } from 'next/headers'

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!

export async function POST(request: NextRequest) {
  const body = await request.text()
  const signature = headers().get('stripe-signature')!
  
  let event
  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret)
  } catch (err) {
    console.error('Webhook signature verification failed')
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }
  
  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckoutCompleted(event.data.object)
      break
    case 'customer.subscription.updated':
      await handleSubscriptionUpdated(event.data.object)
      break
    case 'customer.subscription.deleted':
      await handleSubscriptionDeleted(event.data.object)
      break
    case 'invoice.payment_failed':
      await handlePaymentFailed(event.data.object)
      break
    default:
      console.log(\`Unhandled event type: \${event.type}\`)
  }
  
  return NextResponse.json({ received: true })
}

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  const orgId = session.metadata?.organization_id
  const subscriptionId = session.subscription as string
  
  // Update organization with subscription info
  await supabase
    .from('organizations')
    .update({
      stripe_subscription_id: subscriptionId,
      subscription_status: 'active',
      plan: 'pro', // or derive from price
    })
    .eq('id', orgId)
}
\`\`\`

---

## Checking Subscription Status

\`\`\`typescript
export async function getSubscriptionStatus(orgId: string) {
  const { data: org } = await supabase
    .from('organizations')
    .select('subscription_status, plan, stripe_subscription_id')
    .eq('id', orgId)
    .single()
  
  return {
    isActive: org?.subscription_status === 'active',
    plan: org?.plan ?? 'free',
    subscriptionId: org?.stripe_subscription_id,
  }
}

// In a component or middleware
const { isActive, plan } = await getSubscriptionStatus(orgId)

if (!isActive || plan === 'free') {
  redirect('/billing/upgrade')
}
\`\`\`

---

## Protecting Premium Features

\`\`\`typescript
// Middleware or component
import { getSubscriptionStatus } from '@/lib/stripe'

export async function requirePlan(requiredPlan: 'pro' | 'enterprise') {
  const { plan, isActive } = await getSubscriptionStatus(orgId)
  
  if (!isActive) {
    throw new Error('Subscription required')
  }
  
  const planHierarchy = { free: 0, pro: 1, enterprise: 2 }
  if (planHierarchy[plan] < planHierarchy[requiredPlan]) {
    throw new Error(\`\${requiredPlan} plan required\`)
  }
}
\`\`\`

---

## Environment Variables

\`\`\`bash
# .env.local
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Price IDs
STRIPE_PRO_PRICE_ID=price_...
STRIPE_ENTERPRISE_PRICE_ID=price_...
\`\`\`

---

## Testing

### Local Webhook Testing

\`\`\`bash
# Install Stripe CLI
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
\`\`\`

### Test Cards

| Card Number | Result |
|-------------|--------|
| 4242424242424242 | Success |
| 4000000000000002 | Decline |
| 4000002500003155 | Requires 3DS |

---

## Checklist

When adding payment features:

- [ ] Use test mode keys in development
- [ ] Verify webhook signature
- [ ] Handle all relevant webhook events
- [ ] Update subscription status in database
- [ ] Test with Stripe CLI locally
- [ ] Handle failed payments gracefully
- [ ] Log errors but don't expose to users
```

---

## Step 5: Update project.json

Add to `skills.generated[]`:

```json
{
  "name": "payments",
  "generatedFrom": "stripe-skill-generator",
  "generatedAt": "2026-02-20"
}
```
