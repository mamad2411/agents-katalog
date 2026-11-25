---
name: android-feature-flags
description: Use when a feature, screen or component must be switchable on or off from the backend or on the device in the Android app (AgenticApp).
---

# Android feature flags

## How it decides

1. Launch extra or on-device toggle (`FF_<key>`) – used by tests and the Settings screen in Dev and SYST.
2. Backend value from `GET /api/feature-flags` – `{ "flags": { "<key>": true } }`.
3. `defaultValue` in `FeatureFlag` – used offline or before the backend answers.

## Adding a flag

1. Add an entry to `FeatureFlag` with the backend key, for example `ORDER_HISTORY("order_history", false)`. Use the same key as iOS and web.
2. Use a safe default (usually `false` for new work).
3. Gate the UI: `FeatureGate(FeatureFlag.ORDER_HISTORY) { … }`, or in logic: `LocalFeatureFlags.current.isEnabled(FeatureFlag.ORDER_HISTORY)`.
4. Add the key to `assets/fixtures/feature-flags.json` (and the iOS fixture).
5. Test both states: a unit test with `FeatureFlagService`, and a UI test launched with `launch("FF_order_history" to false)`.

## Rules

- Merge unfinished work behind a flag that defaults to `false`.
- Remove the flag and its dead branch once the feature is fully live.
