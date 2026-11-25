---
name: feature-flags
description: Feature flags via Firebase Remote Config — gradual rollouts, per-environment values, and flag naming conventions. Use when adding a feature flag, implementing a gradual rollout, or reading Remote Config values in the app.
---

## Overview

Feature flags live in Firebase Remote Config. The app reads cached values at startup; you control which value each environment (qa, stg, prd) receives without shipping a new build.

## Naming convention

All Remote Config keys follow `APP_flag_name` in `snake_case`, where `APP` is the platform prefix (`mobile`, `web`, etc.). The app code strips the prefix internally — use only the flag name in code:

```ts
// Firebase dashboard key: mobile_show_new_onboarding
// In code:
const showNewOnboarding = getBooleanRemoteConfigValue('show_new_onboarding');
```

## Flag types

Define flags in `configurations.ts` grouped by type. Default values are used when the app can't reach Firebase:

```ts
const booleanConfigurations = {
  show_new_onboarding: false,
};

const stringConfigurations = {
  api_base_url: 'https://api.example.com',
};

const numberConfigurations = {
  search_results_limit: 10,
};
```

For complex flags, use a JSON string and parse it in code:

```ts
// Firebase value: '{ "show": true, "discount": 5 }'
const rawConfig = getStringRemoteConfigValue('discount_banner');
const config = JSON.parse(rawConfig) as { show: boolean; discount: number };
```

## Per-environment values

Create one condition per environment in the Firebase console using the app ID or version as the target. Evaluation order matters — the first matching condition wins. Naming convention for conditions: `Mobile QA`, `Mobile Stg`, `Mobile Prod`. Use colors to distinguish (green = prod, orange = stg, pink = qa).

## Gradual rollouts (production only)

Use Firebase's Rollout feature to release a new flag value to a percentage of production users:

1. In QA/stg, set the value directly — no rollout needed.
2. In prod, create a Rollout on the parameter:
   - Start at **5%** of users with a target condition (e.g. app version ≥ current).
   - Monitor crash rates and analytics.
   - Increment the percentage over time until 100%.

The rollout acts as an override evaluated before your regular conditions. Users outside the rollout still receive the regular condition value.

## Reading values in the app

Fetch and activate should happen as early as possible in the app lifecycle (before the first screen renders):

```ts
const fetchedRemotely = await remoteConfig().fetchAndActivate();
```

After activation, read values synchronously — the SDK returns the cached value immediately:

```ts
import { getBooleanRemoteConfigValue } from '@<app-name>/remote-config';

const isEnabled = getBooleanRemoteConfigValue('show_new_onboarding');
```

Values update on the next cold start after a fetch, not mid-session. The minimum fetch interval is configured in `firebase.ts` — do not set it below 1 hour in production.
