---
name: analytics
description: Load analytics standards for this React Native / Expo project. Covers event naming, user identification, screen tracking, and privacy rules. Default provider is Firebase Analytics; PostHog and Amplitude are supported alternatives.
---

Apply the following analytics standards to all code in this project.

## Provider

**Default: Firebase Analytics** (`@react-native-firebase/analytics`) — already in the Firebase MCP stack.

Alternatives:

| Provider | Package | When to prefer |
| --- | --- | --- |
| Firebase Analytics | `@react-native-firebase/analytics` | Default — integrates with existing Firebase setup |
| PostHog | `posthog-react-native` | Product analytics, feature flags, session replay |
| Amplitude | `@amplitude/analytics-react-native` | Enterprise, cohort analysis, behavioral funnels |

## Abstraction layer (required)

Never call the provider SDK directly in components. Always go through a central `src/services/analytics/index.ts` using the Firebase v9 modular API:

```ts
// src/services/analytics/index.ts
import { getApp } from '@react-native-firebase/app';
import {
  getAnalytics,
  logEvent,
  setUserId,
  logScreenView,
} from '@react-native-firebase/analytics';

const getA = () => getAnalytics(getApp());

export const Analytics = {
  identify: (userId: string) => setUserId(getA(), userId),
  reset: () => setUserId(getA(), null),
  screen: (name: string) => logScreenView(getA(), { screen_name: name, screen_class: name }),
  track: (event: string, params?: Record<string, string | number | boolean>) =>
    logEvent(getA(), event, params),
};
```

This lets you swap providers without touching call sites.

## Event naming

- Use `snake_case` for all event names: `item_purchased`, `form_submitted`, `onboarding_completed`
- Prefix with the domain when ambiguous: `auth_login_success`, `payment_sheet_opened`
- Past tense for completed actions, present tense for states: `profile_updated`, `push_enabled`
- Never use spaces or special characters

## Screen tracking

Wire to the Expo Router navigation state — do not call `Analytics.screen()` manually in each screen. Create an `AnalyticsProvider` in `app/_layout.tsx` and wrap `<RootLayoutNav />` with it:

```tsx
// app/_layout.tsx
import { usePathname } from 'expo-router';
import { useEffect } from 'react';
import { Analytics } from '@services/analytics';

function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  useEffect(() => { Analytics.screen(pathname); }, [pathname]);
  return <>{children}</>;
}

// Inside RootLayout:
<AnalyticsProvider>
  <RootLayoutNav />
</AnalyticsProvider>
```

## User identification

```ts
// After successful sign-in
Analytics.identify(user.id);

// On sign-out
Analytics.reset();
```

Never identify before auth completes. Clear on sign-out.

## Privacy rules (non-negotiable)

- Never log PII in event properties: no names, emails, phone numbers, addresses, or DOBs
- Never log raw payment data: no card numbers, CVVs, or full PANs
- Never log auth tokens or session IDs
- User IDs passed to `identify()` must be your internal opaque ID (UUID) — not email or phone
- Sentry and Analytics are separate: do not cross-log breadcrumbs that contain user-identifiable info

## Switching providers

If the project uses PostHog or Amplitude instead of Firebase, ask for the relevant implementation pattern and it will be provided on demand.

## Querying GA4 data programmatically (agent access)

Firebase Analytics data lives in GA4 and is NOT reachable via the Firebase MCP or CLI —
only the **Google Analytics Data API** exposes it. One-time setup per project:

1. GCP console (the project behind Firebase) → enable **Google Analytics Data API**
   (and **Google Analytics Admin API** if you want property auto-discovery).
2. Create a service account — **no GCP IAM roles needed** — and download its JSON key.
3. Google Analytics → Admin → **Property access management** → add the service-account
   email as **Viewer**. (GA4 permissions live in Analytics, not GCP IAM.)
4. Store in Doppler: `GA4_CLIENT_EMAIL`, `GA4_PRIVATE_KEY`, `GA4_PROPERTY_ID`
   (numeric, from Admin → Property settings).

Query with zero dependencies (JWT via openssl, stdlib HTTP) — reference implementation
in reflect's `scripts/ga4-report.py`; run under `doppler run --config prd`. Core flow:

```
JWT{iss: client_email, scope: analytics.readonly, aud: oauth2.googleapis.com/token}
  → sign RS256 with openssl → POST /token → access_token
  → POST analyticsdata.googleapis.com/v1beta/properties/{ID}:runReport
    {dateRanges, dimensions: [{name: "date"}], metrics: [{name: "activeUsers"}, ...]}
```

Useful metrics: `activeUsers`, `newUsers`, `dauPerMau`, `sessions`, `screenPageViews`.
`activeUsers − newUsers` per day ≈ returning users (a practical retention floor).
