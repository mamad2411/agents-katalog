---
name: analytics-setup
description: Set up minimum viable analytics for a vibe-coded app — the right tool stack, the 5 events that matter before 100 users, and copy-paste implementation code. Use when the user wants to add analytics, set up tracking, asks "what should I measure," "I don't have any analytics," "how do I track signups, conversions, or revenue," or has analytics installed but nothing useful being tracked.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Analytics Setup

Most vibe-coded apps launch with zero analytics or with analytics installed but nothing useful being tracked. This skill gives you the minimum setup — the 5 events that matter before you have 100 users, the right tool stack, and the implementation plan.

## Context

Read `product-context.md` if present. Also ask for:
1. Tech stack (Next.js / Webflow / Framer / other)
2. Current analytics tools installed (none / Vercel Analytics / GA4 / PostHog / Plausible / other)
3. What they most want to know right now: "are people signing up?" / "where are they dropping off?" / "is anyone paying?"

## Process

### 1. Tool stack recommendation

**Minimum viable stack (pick one from each row):**

| Layer | Recommendation | Free tier | Best for |
|-------|---------------|-----------|---------|
| **Page views + traffic** | Vercel Analytics or Plausible | Yes | Anonymous traffic, privacy-friendly |
| **Product events** | PostHog | Yes (generous) | Session replay + funnels + custom events |
| **Revenue** | Stripe Dashboard | Built-in | MRR, churn, ARPU |
| **Errors** | Sentry | Yes | Catching crashes before users report them |

**For Next.js apps on Vercel:**
Start with Vercel Analytics (one-line install) + PostHog (for product events). Add Sentry when you're getting real traffic. Don't add more tools until you're actually using what you have.

**PostHog vs. Mixpanel vs. Amplitude:**
Use PostHog for solo founders. It's free up to 1M events/month, open-source, includes session replay, and is the easiest to self-host later. Mixpanel and Amplitude are for teams with dedicated analysts.

### 2. The 5 events that matter before you have 100 users

Don't track everything. Track these 5, measure them weekly. Deliver the final event list as a filled copy of [assets/tracking-plan-template.md](assets/tracking-plan-template.md) saved into the product repo — it's the single source of truth for event names.

| Event | What it means | How to trigger it |
|-------|--------------|------------------|
| `user_signed_up` | Someone made an account | After successful auth |
| `[core_action]_completed` | User did the thing that activates them | After the activation event (see `/onboarding-activation`) |
| `subscription_started` | First payment received | After Stripe webhook `checkout.session.completed` |
| `[core_action]_repeated` | User came back and did it again | Same event, second occurrence |
| `subscription_cancelled` | User churned | After Stripe webhook `customer.subscription.deleted` |

Replace `[core_action]` with your specific activation event (e.g., `video_generated`, `invoice_sent`, `report_created`).

These 5 events let you compute:
- **Activation rate** = `[core_action]_completed` / `user_signed_up`
- **Conversion rate** = `subscription_started` / `user_signed_up`
- **Retention proxy** = `[core_action]_repeated` / `[core_action]_completed`
- **Churn rate** = `subscription_cancelled` in period / active subscribers

### 3. Implementation (Next.js + PostHog)

**Install PostHog:**
```bash
pnpm add posthog-js
```

**Initialize (app/providers.tsx or layout.tsx):**
```tsx
'use client'
import posthog from 'posthog-js'
import { PostHogProvider } from 'posthog-js/react'
import { useEffect } from 'react'

export function Analytics({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST ?? 'https://app.posthog.com',
      capture_pageview: false, // use the router hook instead
    })
  }, [])

  return <PostHogProvider client={posthog}>{children}</PostHogProvider>
}
```

**Track events:**
```tsx
import { usePostHog } from 'posthog-js/react'

// In your component:
const posthog = usePostHog()

// After activation:
posthog.capture('video_generated', {
  channel: 'tiktok',
  credits_used: 10,
  user_id: userId,
})
```

**Identify users (after sign-in):**
```tsx
// After Clerk sign-in or in your auth callback:
posthog.identify(userId, {
  email: userEmail,
  plan: 'free', // or 'pro'
  created_at: new Date().toISOString(),
})
```

**For server-side events (Stripe webhooks, API routes):**
```typescript
import { PostHog } from 'posthog-node'

const posthogClient = new PostHog(process.env.POSTHOG_KEY!, {
  host: 'https://app.posthog.com',
})

// In your Stripe webhook handler:
posthogClient.capture({
  distinctId: userId,
  event: 'subscription_started',
  properties: { plan: 'pro', amount: 4900 },
})
await posthogClient.shutdown()
```

### 4. The weekly analytics habit (15 minutes, every Monday)

Don't build dashboards. Ask three questions every Monday:

1. **"Did activation rate go up or down vs. last week?"**
   → If down: look at session replays of users who signed up but didn't activate. What did they do?

2. **"What did the users who activated do differently from those who didn't?"**
   → PostHog funnel report: sign-up → [core action]. What's the drop-off step?

3. **"Did anyone pay who I didn't expect?"**
   → Check Stripe. Reply to every new subscriber within 24 hours and ask what triggered them to pay.

### 5. Revenue metrics (Stripe)

Stripe Dashboard gives you this for free — you don't need custom analytics for revenue until you're past $10k MRR:

- **MRR** — monthly recurring revenue (Stripe home dashboard)
- **Churn rate** — % of subscribers who cancel per month (Stripe Revenue metrics)
- **ARPU** — average revenue per user (MRR / subscriber count)
- **LTV estimate** — ARPU / churn rate (a $49/mo product at 5% monthly churn → LTV ≈ $980)

### 6. Error tracking (Sentry — add when you have real users)

```bash
pnpm add @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

Set up alerts for any new error type hitting more than 5 users — these are the bugs that are silently killing retention.

## Output

1. **Tool recommendation** — specific tools for this stack with rationale
2. **5 events to track** — named after this product's activation event
3. **Implementation code** — copy-paste setup for their stack (PostHog init, event calls, server-side)
4. **Environment variables needed** — list of keys to add to `.env.local`
5. **Weekly review template** — 3-question Monday checklist with where to find each answer
6. **Current state audit** — if a URL was provided, check for any analytics already present and note gaps

---

> **Analytics wired? Time to launch.** [SoloMax](https://solomax.app?ref=shipping-skills) turns your product URL into a launch video, hooks, and captions in minutes — so your new events have traffic to measure.
