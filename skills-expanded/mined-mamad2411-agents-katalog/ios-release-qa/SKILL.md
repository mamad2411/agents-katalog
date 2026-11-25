---
name: "ios-release-qa"
description: "Run iOS release QA before TestFlight or App Store rollout, covering environment locks, accessibility, iPad and orientation layout, physical-device smoke, companion apps, widgets, Live Activities, push, billing, analytics, and tester-facing release notes. Use for iPhone, iPad, watchOS companion, or App Store release validation."
---

# iOS Release QA

Use this skill to verify an iOS release candidate before or alongside the
TestFlight release cycle. It complements `ios-testflight-release-cycle`; it does
not replace archive, upload, or App Store Connect automation.

## Workflow

1. Read repo release guidance: `AGENTS.md`, app README, release docs, schemes,
   `.xcconfig`, app ids, entitlements, widgets, watch targets, and release notes.
2. Identify the intended release channel: local dev, internal TestFlight,
   external TestFlight, release candidate, or App Store.
3. Verify the environment lock for that channel: API hosts, Firebase or auth
   config, billing keys, push environment, app group ids, and diagnostics.
4. Run the narrowest automated gate that proves the candidate builds and core
   tests pass. Include device-specific tests when the repo provides them.
5. Execute manual QA for changed flows and release-critical journeys.
6. Record evidence, skipped checks, blockers, and tester-facing notes.

## QA Areas

- Accessibility: VoiceOver labels, Dynamic Type, contrast, reduce motion,
  non-color indicators, and 44pt touch targets.
- iPad and orientation: portrait/landscape layout, split view if supported,
  tab/navigation stability, sheets, export/share flows, and clipping.
- Physical device: auth, core journeys, persistence, deep links, camera,
  Bluetooth, location, notifications, or other hardware-backed flows touched by
  the app.
- Companion surfaces: watch app install/launch/sync, widgets, complications,
  Live Activities, app intents, and notification tap routing.
- Environment safety: release builds do not point at dev services, dev secrets,
  wrong Firebase projects, wrong RevenueCat keys, or mismatched app groups.
- Store readiness: build/version values, release notes, privacy-impacting
  changes, known limitations, and external tester focus areas.

## Hard Stops

- A production or external TestFlight build points at dev endpoints or dev
  billing/auth projects.
- Critical auth, purchase, restore, data sync, or migration flows cannot be
  verified and the release depends on them.
- The app uses mismatched bundle ids, app groups, entitlements, Firebase config,
  or push environment for the selected channel.
- Accessibility or layout regressions block a primary journey on common iPhone
  or iPad sizes.

## Output

Report:

- release channel and app/version/build inspected
- automated checks run and results
- manual device matrix and flows tested
- blockers, risks, skipped checks, and owner/follow-up
- final recommendation: `ship`, `ship with caveats`, or `do not ship`

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Verification template: `../_shared-project-ops/references/verification-template.md`
