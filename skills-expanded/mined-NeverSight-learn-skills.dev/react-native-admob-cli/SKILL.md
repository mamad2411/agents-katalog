---
name: react-native-admob-cli
description: Bare React Native CLI AdMob adapter for react-native-google-mobile-ads. Use only when the project is bare React Native CLI or a bare RN native app with ios/ and android/, and the user asks to integrate, configure, debug, or audit Google Mobile Ads/AdMob code, consent, ATT, test IDs, banner, interstitial, rewarded, app-open placement, or release readiness. Do not use for Expo-managed apps, Flutter apps, generic AdMob console automation, or store deployment except to route to the appropriate skill.
---

# React Native AdMob CLI

Use this skill as a thin safety adapter for bare React Native CLI AdMob work.
Its value is preventing Expo plugin snippets, Flutter widget examples, and
AdMob-console automation assumptions from being applied to a bare RN project.

Before changing code, classify the project:

- Bare RN CLI: `package.json` uses React Native, and both `ios/` and `android/`
  exist.
- Expo-managed or EAS-first app shell: route to `integrating-google-ads`,
  `store-admob`, or `store-deploy` instead.
- Flutter app: route to `admob-ux-best-practices` or Flutter-specific guidance.
- Unknown: inspect project files first; ask only if the app shell remains unclear.

## Reference Map

Read only the files needed for the task:

- `references/rn-cli-setup.md`: package manager, app IDs, native config, rebuilds.
- `references/privacy-consent.md`: UMP, ATT, initialization ordering, test consent.
- `references/ad-components.md`: RN TypeScript ad-unit config and ad components.
- `references/monetization-strategy.md`: format choice, caps/floors, experiments, metrics.
- `references/loading-lifecycle.md`: preload, state, reload, app-open, cooldown rules.
- `references/mediation-native.md`: Android/iOS mediation and native config checks.
- `references/policy-ux-checklist.md`: RN ad placement safety and policy review.
- `references/store-release-checklist.md`: AdMob IDs, iOS privacy, release checks.
- `references/troubleshooting.md`: no-fill, startup crashes, app ID, test-device issues.

When the task touches native config, consent APIs, ATT, SKAdNetwork, or ad
lifecycle behavior, verify current Invertase and Google docs before editing.
Treat examples in references as implementation patterns, not permanent API truth.
When the task touches revenue strategy, mediation, native partner setup, or
debug evidence, load the matching reference first and keep claims measurable.

## Ownership

This skill owns:

- bare RN CLI project detection and routing
- `react-native-google-mobile-ads` setup for bare RN
- root `app.json` `react-native-google-mobile-ads` config
- consent and initialization sequencing before ad loading
- monetization guidance for format selection, caps/floors, metrics, and tests
- ad lifecycle guidance for preload, reload, app-open age, cooldown, and failure
- RN-safe banner/interstitial/rewarded/app-open implementation patterns
- mediation/native checks for Android, iOS, adapter freshness, and privacy disclosure
- revenue/debugging evidence: ILRD, ResponseInfo, Ad Inspector, and release proof
- local verification and troubleshooting

Delegate:

- Expo plugin setup: `integrating-google-ads`
- AdMob account/app/ad-unit provisioning: `store-admob`
- store submission and deployment orchestration: `store-deploy`
- general ad placement policy: `admob-ux-best-practices`, translated into RN

## Hard Rules

- Do not put bare RN App IDs under `expo.plugins`.
- Do not copy Flutter widgets or Dart code into RN.
- Do not mutate an AdMob account, browser session, app store listing, or
  production project without explicit user approval.
- Do not load ads before consent/request configuration and
  `mobileAds().initialize()` have completed or intentionally settled.
- Do not claim any ad format has universal revenue superiority; require metrics,
  experiments, and retention impact before revenue conclusions.
- Do not paste static adapter matrices or platform ad-network ID lists; verify
  current Google, partner, and Invertase docs when native/mediation details matter.
- Use Google test IDs in development; never test with production units unless the
  device is registered as a test device.
- Ad failures, mediation gaps, or revenue debug failures must not block the core
  app flow; capture evidence and degrade gracefully.

## Verification

Prefer the narrowest reliable proof available:

- static proof: dependency present, `app.json` app IDs present, debug code uses
  `TestIds`, and ad loading is gated by consent/init
- code proof: TypeScript/lint/tests for added components or config modules
- native proof: `npx pod-install`, Android/iOS debug build, or existing project
  build command when feasible
- real device/simulator proof: Google test ad label or captured load log

If no device or simulator is available, report that limitation and provide the
static/build evidence instead.
