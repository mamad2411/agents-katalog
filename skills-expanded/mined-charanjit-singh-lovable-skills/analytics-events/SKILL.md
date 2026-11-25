---
name: analytics-events
description: >-
  Use when adding product analytics (PostHog, GA4, Plausible), event tracking,
  funnels, or conversion measurement. Not for server logs only or A/B infra
  unless events are part of the task.
---

# Analytics events

## Naming convention

`object_action` in snake_case, stable over time:

- `signup_completed`
- `project_created`
- `checkout_started`
- `subscription_upgraded`

Document events in a short table in code or README when adding new ones.

## Implementation

- Wrap provider in one module: `lib/analytics.ts` with `track(event, properties?)`.
- Call after success (mutation resolved), not on click before confirm.
- Include `user_id` only if provider docs allow and privacy policy covers it — prefer anonymous until identified.

```ts
export function track(event: string, properties?: Record<string, unknown>) {
  if (import.meta.env.DEV) return; // or mirror to console in dev
  posthog?.capture(event, properties);
}
```

## Page views

- SPA: track on route change (`useEffect` on `location.pathname`) or provider's React integration.

## Privacy

- No passwords, tokens, full credit card numbers, or health data in properties.
- Cookie consent banner if required (EU/UK).

## Key funnels (define with user)

Typical: visit → signup → activation → paid. Map 3–5 events minimum for new products.

## StrictMode and double-firing

React 18+ in dev mounts twice. Guard one-shot events:

```ts
const fired = useRef(false);
useEffect(() => {
  if (fired.current) return;
  fired.current = true;
  track("checkout_started", { plan });
}, []);
```

Or fire from event handlers (clicks, mutations resolved) rather than mount effects whenever possible.

## Avoid

- Duplicate events on StrictMode double mount without guard.
- Tracking every keystroke.
- Different event names per page for the same action.
- Sending PII (email, names) as event properties unless your privacy policy and provider support it.
