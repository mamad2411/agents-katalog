---
name: saas-analytics-patterns
description: SaaS analytics event taxonomy, metric formulas (MRR, churn, LTV), provider-agnostic tracking, funnel analysis, cohort setup, and privacy-respecting instrumentation.
---

# SaaS Analytics Patterns

Provider-agnostic analytics for SaaS products. Track what matters, name it consistently, respect privacy.

## Event Naming Convention

Use `object_action` format. Past tense for completed actions.

```typescript
// GOOD: structured object_action naming
const Events = {
  USER_SIGNED_UP: 'user_signed_up',
  PLAN_UPGRADED: 'plan_upgraded',
  PLAN_DOWNGRADED: 'plan_downgraded',
  PAYMENT_FAILED: 'payment_failed',
  TRIAL_STARTED: 'trial_started',
  FEATURE_USED: 'feature_used',
  INVITE_SENT: 'invite_sent',
  ONBOARDING_COMPLETED: 'onboarding_completed',
} as const

// BAD: ad-hoc, inconsistent naming
// 'click_upgrade_button'  -- UI action, not business event
// 'userSignedUp'          -- camelCase breaks grouping in dashboards
// 'Signed Up'             -- spaces break queries
// 'signup'                -- ambiguous (started? completed?)
```

## Analytics Provider Abstraction

Never couple your app to a specific vendor (Mixpanel, Amplitude, PostHog).

```typescript
interface AnalyticsProvider {
  identify(userId: string, traits: Record<string, unknown>): void
  track(event: string, properties?: Record<string, unknown>): void
  page(name: string, properties?: Record<string, unknown>): void
  reset(): void
}

class Analytics {
  private providers: AnalyticsProvider[] = []
  private consentGiven = false

  addProvider(p: AnalyticsProvider): void { this.providers = [...this.providers, p] }
  setConsent(granted: boolean): void { this.consentGiven = granted }

  track(event: string, properties: Record<string, unknown> = {}): void {
    if (!this.consentGiven) return
    const enriched = { ...properties, timestamp: new Date().toISOString() }
    for (const p of this.providers) p.track(event, enriched)
  }

  identify(userId: string, traits: Record<string, unknown> = {}): void {
    if (!this.consentGiven) return
    for (const p of this.providers) p.identify(userId, traits)
  }

  reset(): void { for (const p of this.providers) p.reset() }
}

export const analytics = new Analytics()
```

## SaaS Metric Formulas

```typescript
function calculateMetrics(d: {
  activeCustomers: number; customersAtPeriodStart: number; customersLost: number
  recurringRevenue: number; revenueLost: number
  totalAcquisitionSpend: number; newCustomers: number
}) {
  const mrr = d.recurringRevenue
  const arr = mrr * 12
  const churnRate = d.customersAtPeriodStart > 0
    ? (d.customersLost / d.customersAtPeriodStart) * 100 : 0
  const arpu = d.activeCustomers > 0 ? mrr / d.activeCustomers : 0
  const ltv = churnRate > 0 ? arpu * (1 / (churnRate / 100)) : 0
  const cac = d.newCustomers > 0 ? d.totalAcquisitionSpend / d.newCustomers : 0
  const ltvCacRatio = cac > 0 ? ltv / cac : 0  // target: > 3
  return { mrr, arr, churnRate, arpu, ltv, cac, ltvCacRatio }
}
```

## Event Taxonomy Design

Typed property schemas keep every event consistent and queryable.

```typescript
interface BaseProperties {
  timestamp: string
  platform: 'web' | 'ios' | 'android'
  session_id: string
}

interface BillingProperties extends BaseProperties {
  plan_id: string; plan_name: string
  amount_cents: number; currency: string
  previous_plan_id?: string
}

// GOOD: typed, every field documented
trackBilling(Events.PLAN_UPGRADED, {
  timestamp: new Date().toISOString(), platform: 'web', session_id: 'sess_abc',
  plan_id: 'plan_pro', plan_name: 'Pro', amount_cents: 4900,
  currency: 'USD', previous_plan_id: 'plan_free',
})

// BAD: analytics.track('upgraded', { plan: 'pro', price: 49 })
```

## Funnel Tracking

Track each lifecycle stage: signup, onboarding, activation, retention.

```typescript
const Funnel = {
  SIGNUP: 'funnel_signup_completed',
  ONBOARDING: 'funnel_onboarding_completed',
  ACTIVATION: 'funnel_activation_reached',
  RETAINED_D7: 'funnel_retained_day_7',
  RETAINED_D30: 'funnel_retained_day_30',
} as const

// Define activation with YOUR product's criteria
async function checkActivation(userId: string): Promise<boolean> {
  const projects = await db.project.count({ where: { userId } })
  const invites = await db.invite.count({ where: { invitedBy: userId } })
  if (projects >= 3 && invites >= 1) {
    analytics.track(Funnel.ACTIVATION, { user_id: userId, projects, invites })
    return true
  }
  return false
}
```

## Feature Flag + Analytics

Track experiment exposure, then correlate with conversion outcomes.

```typescript
function evaluateFlag(userId: string, flagKey: string): string {
  const variant = featureFlags.evaluate(flagKey, userId)
  analytics.track('feature_flag_evaluated', { flag_key: flagKey, variant, user_id: userId })
  return variant
}
// Correlate: SELECT variant, COUNT(*) FROM events
// WHERE event='plan_upgraded' AND user_id IN (
//   SELECT user_id FROM events WHERE event='feature_flag_evaluated'
//   AND flag_key='new_pricing') GROUP BY variant
```

## Server-Side vs Client-Side

```typescript
// CLIENT: UI interactions, page views (blockable by ad blockers)
analytics.track('button_clicked', { button_id: 'cta_hero' })

// SERVER: revenue, activation, lifecycle (never blocked = source of truth)
async function onSubscription(sub: Subscription): Promise<void> {
  await serverAnalytics.track('plan_upgraded', {
    user_id: sub.userId, plan_id: sub.planId, amount_cents: sub.amountCents,
  })
}
// Revenue + activation events: ALWAYS server-side
// UI interactions: client-side is acceptable
```

## Privacy-Respecting Analytics

```typescript
function privacyWrap(base: AnalyticsProvider): AnalyticsProvider {
  return {
    identify(userId, traits) {
      const hashed = createHash('sha256').update(userId).digest('hex')
      base.identify(hashed, { plan: traits.plan, signup_date: traits.signup_date })
    },
    track(event, props = {}) {
      const { email, ip_address, user_agent, user_id, ...safe } = props as Record<string, unknown>
      // Hash user_id if present to prevent PII leak to analytics provider
      if (user_id) (safe as Record<string, unknown>).user_id = createHash('sha256').update(String(user_id)).digest('hex').slice(0, 16)
      base.track(event, safe)
    },
    page: (n, p) => base.page(n, p),
    reset: () => base.reset(),
  }
}

function initAnalytics(consent: 'none' | 'essential' | 'full'): void {
  if (consent === 'none') return
  analytics.setConsent(true)
  if (consent === 'essential') analytics.addProvider(privacyWrap(serverProvider))
  if (consent === 'full') { analytics.addProvider(serverProvider); analytics.addProvider(clientProvider) }
}
```

## Cohort Analysis Setup

```typescript
function assignCohort(user: { id: string; createdAt: Date; plan: string }): void {
  const month = `${user.createdAt.getFullYear()}-${String(user.createdAt.getMonth() + 1).padStart(2, '0')}`
  analytics.identify(user.id, {
    cohort_signup_month: month,
    cohort_plan_at_signup: user.plan,
    cohort_channel: getAttributionChannel(user.id),
  })
}
// Retention query: SELECT cohort_signup_month,
//   DATEDIFF(week, first_seen, event_date) AS week_n,
//   COUNT(DISTINCT user_id) AS active
// FROM events GROUP BY 1, 2 ORDER BY 1, 2
```

**Key principles**: Name events `object_action`. Track revenue server-side. Abstract your provider from day one. Define activation explicitly. Strip PII before sending to any third party.
