---
name: ios-privacy-performance-release-proof
description: Audit and plan iOS privacy manifests, required-reason APIs, test plans, Swift Testing/XCTest coverage, OSLog/signposts/MetricKit diagnostics, accessibility task evidence, system-surface behavior, archive validation, TestFlight, App Store Connect, and release claims. Use when a feature touches protected data, third-party SDKs, performance-sensitive UI, accessibility, widgets, App Intents, Live Activities, extensions, or any signed/distributed build.
allowed-tools: Read, Grep, Glob
---

# iOS Privacy, Performance, and Release Proof

## Overview

Use this skill to turn an iOS feature claim into a traceable privacy, test, performance, accessibility, system-surface, and release-evidence plan. Inspect the real target before recommending configuration, and keep every evidence layer separate.

## Read before acting

- Inspect the `.xcodeproj`/`.xcworkspace`, schemes, test plans, targets, deployment target, SDK/toolchain, build configurations, Info.plist values, entitlements, capabilities, bundle identifiers, package dependencies, extensions, and supported device families.
- Read the [framework availability and device-proof matrix](../ios-knowledge-base/references/40-framework-routes/08-framework-availability-and-device-matrix.md), [source-review checklist](../ios-knowledge-base/references/60-verification/00-source-review-checklist.md), [build/device/release checklist](../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md), [accessibility checklist](../ios-knowledge-base/references/60-verification/02-accessibility-and-adaptability-checklist.md), [AI evaluation checklist](../ios-knowledge-base/references/60-verification/03-ai-evaluation-and-safety-checklist.md), and [system-surface checklist](../ios-knowledge-base/references/60-verification/05-system-surface-checklist.md).
- Refresh the exact [official source registry](../ios-knowledge-base/references/sources/official-source-registry.md) and current Apple pages before making an API, availability, policy, or App Store claim.

## Evidence ladder

Record the strongest level actually observed:

| Level | Can support | Cannot support alone |
| --- | --- | --- |
| Official source | Documented API behavior, constraints, availability language, or policy requirement | This target’s configuration, compilation, permission state, user experience, or release behavior |
| Static target inspection | Target membership, bundle resources, build settings, entitlements, and intended route | A successful build, valid signing, device behavior, or system delivery |
| Compile/unit/fixture test | API compatibility and deterministic domain behavior | Hardware, protected services, model quality, accessibility ergonomics, APNs, or production state |
| Preview/simulator/UI test | Layout, fixtures, navigation, and selected automatable flows | Physical sensors, VoiceOver/Voice Control/Switch Control behavior, thermal state, paired devices, or production services |
| Physical debug device | Hardware, permission, assistive technology, system surface, and device lifecycle behavior | Distribution metadata, TestFlight processing, App Review, or production server health |
| Signed archive/TestFlight | Packaging, signing, entitlements, store-like build, and beta behavior | App Review approval, live production rollout, all devices/regions, or server reliability |
| Production evidence | The tested live route/environment | Universal behavior across OS versions, devices, accounts, languages, or future SDKs |

Never write “works,” “private,” “accessible,” “fast,” or “release-ready” without naming the target, OS, device, build/configuration, environment, operation, and evidence level.

## Fast path

Run change-impact triage across privacy, required-reason APIs, performance, accessibility, artifact integrity, and distribution. Execute only the affected evidence lanes, capture a baseline and delta, and reserve a full release audit for changes that cross a release or system boundary.

## Evidence report

```text
Claim:
Target/scheme/test plan:
Deployment target and SDK:
Bundle ID/version/build/device family:
Privacy manifest and App Store privacy status:
Capabilities/entitlements/permissions:
Device/OS/settings/account/server/APNs state:
Operation exercised:
Tests and artifacts:
Performance workload and metric:
Observed result:
Negative cases:
What this proves:
What it does not prove:
Next gate:
```

Do not include secrets, raw model prompts/responses, health/contact/call payloads, private tokens, or unnecessary user media in the report. Redact logs and screenshots.

## Hard boundaries

- Never call a privacy manifest, accessibility audit, performance baseline, archive, or TestFlight upload a universal privacy, accessibility, speed, approval, or production guarantee.
- Never print credentials, sensitive payloads, or unnecessary identifiers while collecting diagnostics or release evidence.
- Never add tracking, remote processing, broad permissions, or release metadata merely to make a check pass; record the missing boundary instead.

## Related routes

- [Availability and device-proof matrix](../ios-knowledge-base/references/40-framework-routes/08-framework-availability-and-device-matrix.md)
- [Source review checklist](../ios-knowledge-base/references/60-verification/00-source-review-checklist.md)
- [Build/device/release checklist](../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md)
- [Accessibility checklist](../ios-knowledge-base/references/60-verification/02-accessibility-and-adaptability-checklist.md)
- [AI evaluation and safety checklist](../ios-knowledge-base/references/60-verification/03-ai-evaluation-and-safety-checklist.md)
- [System-surface checklist](../ios-knowledge-base/references/60-verification/05-system-surface-checklist.md)
- [Official source registry](../ios-knowledge-base/references/sources/official-source-registry.md)

Further sections — read when the above is not enough: `references/details.md`.
