---
name: mobile-crash
description: Mobile crash and stability specialist. Owns crash reporting integration (Crashlytics, Sentry, App Center, native), symbolication (dSYMs, ProGuard/R8 mappings), ANR/foreground-service issues, and stability triage. Auto-invoked for crash spikes, symbolication breakage, or stability/ANR investigation.
---

# Mobile Crash & Stability

A crash is a rage-quit and a one-star review. Symbolication, triage, and a
crash-free SLO are the difference between guessing and shipping.

## When to reach for this

- Integrating or auditing a crash-reporting SDK (Crashlytics, Sentry, App Center, BugSnag)
- Crash reports arriving unsymbolicated, or symbol upload silently broken in CI
- Investigating a crash spike, ANR cluster, or iOS watchdog kill after a release
- Defining crash-free SLOs, alerting, and hotfix gates for the release train

## Principles

1. **Symbols on every build, enforced in CI.** dSYM upload (iOS), ProGuard/R8
   mapping upload (Android), NDK symbols if native code ships. The CI job
   *fails* if upload fails — an unsymbolicated crash report is a write-only log.
2. **Crash-free is an SLO with a number.** ≥ 99.9% crash-free users is the
   common floor; alert when a release dips below baseline, don't wait for reviews.
   Google Play penalizes visibility above ~1.09% user-perceived crash rate and
   ~0.47% user-perceived ANR rate — treat those as hard ceilings, not targets.
3. **ANR is a main-thread budget problem.** Android raises an ANR when the main
   thread blocks input dispatch ~5 s; iOS watchdog kills (`0x8badf00d`) hit slow
   launches and hangs. Triage these as performance debt, not random noise.
4. **Group by signature, own by team.** Every crash group gets an owner and a
   severity; "assigned to nobody" is how 0.1% issues become 2% issues.
5. **Hotfix gates on regression, not vibes.** A new release that drops
   crash-free below the previous version's baseline halts the rollout ramp.
6. **Beta signal is a separate dashboard.** Track TestFlight / Play-testing-track
   crash-free independently — beta cohorts are small, so one device can swing
   the rate; compare trends, not absolutes.

## Symbolication checklist

| Platform | Artifact | Pipeline step | Verify by |
|---|---|---|---|
| iOS | dSYM per build (incl. frameworks) | upload in CI after archive; re-fetch from App Store Connect if Bitcode-era builds recompiled | a forced test crash symbolicates with file:line |
| Android (JVM) | ProGuard/R8 `mapping.txt` | upload keyed to versionCode in the release job | obfuscated frames resolve in the dashboard |
| Android (NDK) | unstripped `.so` symbols | `nativeSymbolUploadEnabled` / symbol upload task | native frames show function names |
| Both | crash SDK init | first thing in app start, before DI/network | test crash from a release-config build appears |

Triage workflow: new group → auto-assign by top frame's code owner → severity by
(users affected × blast radius) → regression label if introduced this version →
regressions above threshold open a hotfix ticket and block the ramp.

## Pitfalls

- Symbol upload "succeeding" against the wrong app ID or build UUID — verify with a
  deliberate crash per release, not by trusting the upload log
- Catching-and-swallowing exceptions to "fix" the crash rate; the corrupted state
  resurfaces as a worse crash elsewhere
- Counting OOM kills and iOS watchdog terminations as zero because the SDK's
  default config doesn't capture them
- Triaging by total event count instead of affected users — one looping device
  can fake a spike
- Crash spikes that are actually rollout-percentage artifacts: normalize by
  sessions on the new version before declaring a regression

---
*Related: `mobile-perf` (ANR/jank root cause), `mobile-release` (rollout halt
gates), `mobile-platform` (API-misuse crashes), `mobile-iap` (purchase-flow
crashes) · domain agent: `mobile-architect` · output/ADR format:
`playbook-conventions`*
