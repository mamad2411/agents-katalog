---
description: Run Analytics, Privacy, and Conversion Tracking Checks
globs: ['**/analytics/**/*.ts', '**/tracking/**/*.ts', '**/components/providers/analytics*.tsx']
---

# Business: Analytics & Privacy Standards

<audit_rules>

- You MUST ensure critical user journey events (e.g., `checkout_started`, `payment_completed`, `sign_up`) are explicitly tracked with rich metadata payloads.
- You MUST verify that tracking code respects user privacy and consent management configurations (e.g., GDPR/CCPA). Do NOT initialize tracking scripts until consent is granted.
- You MUST ensure Personally Identifiable Information (PII) like raw email addresses or passwords are NEVER sent to analytics providers. Use hashed identifiers instead.
- You MUST verify that conversion funnels have tracking at every step to identify drop-off points.
- You MUST ensure analytics events use a consistent naming taxonomy (e.g., `noun_action` like `button_clicked`).
  </audit_rules>

<example_good>

```typescript
// Checking consent and hashing PII
import { hash } from '@/lib/crypto'
import { getConsent } from '@/lib/consent'

export function trackLogin(user: User) {
  if (!getConsent('analytics')) return

  analytics.track('user_logged_in', {
    userId: hash(user.id),
    method: 'email',
    timestamp: new Date().toISOString(),
  })
}
```

</example_good>

<example_bad>

```typescript
// BAD: Ignoring consent and leaking PII
export function trackLogin(user: User) {
  analytics.track('login', {
    email: user.email, // CRITICAL: PII Leak
    password: user.password, // CRITICAL: Secret Leak
  })
}
```

</example_bad>
