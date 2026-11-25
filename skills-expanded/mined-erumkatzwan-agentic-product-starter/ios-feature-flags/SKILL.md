---
name: ios-feature-flags
description: Use when a feature, screen or component must be switchable on or off from the backend or on the device in the iOS app (AgenticApp).
---

# iOS feature flags

## How it decides

1. Launch argument or on-device override (`FF_<key>`) – used by tests and the Settings screen in Dev and SYST.
2. Backend value from `GET /feature-flags` – `{ "flags": { "<key>": true } }`.
3. `defaultValue` in `FeatureFlag` – used offline or before the backend answers.

## Adding a flag

1. Add a case to `FeatureFlag` with the backend key as raw value, for example `case orderHistory = "order_history"`.
2. Set a safe `defaultValue` (usually `false` for new work).
3. Gate the UI: `FeatureGate(.orderHistory) { … }`, or in logic: `featureFlags.isEnabled(.orderHistory)`.
4. Add the key to `Resources/Fixtures/feature-flags.json`.
5. Test both states: a unit test with `FeatureFlagService`, and a UI test launched with `-FF_order_history NO`.

## Rules

- Merge unfinished work behind a flag that defaults to `false`.
- Remove the flag and its dead branch once the feature is fully live.
