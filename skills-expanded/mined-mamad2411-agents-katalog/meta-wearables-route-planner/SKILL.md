---
name: meta-wearables-route-planner
description: Choose the correct Meta Wearables route across native iOS DAT, native Display, Ray-Ban Display Web Apps, phone fallback, and unsupported or unverified device requests. Use before implementation whenever a product mentions Ray-Ban Meta, Oakley Meta, Meta Glasses, Display, camera, audio, input, sensors, Gen 2, Gen 3, or the Meta Wearables SDK.
allowed-tools: Read, Grep, Glob
---

# Meta Wearables route planner

## Overview

Turn a wearable idea into a verified platform route before package imports, UI work, permissions, or marketing copy harden around an assumption.

## Read before acting

- Inspect the actual project, target platforms, deployment target, existing device integrations, and whether the requested surface is a companion app or a glasses-delivered experience.
- Read [platform and route selection](../meta-wearables-knowledge-base/references/70-meta-wearables/00-platform-and-route-selection.md), [device models and capability matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/05-device-models-and-capability-matrix.md), and [the Meta source registry](../meta-wearables-knowledge-base/references/sources/meta-wearables-source-registry.md).
- Read the [device-generation and runtime-support matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/16-device-generation-and-runtime-support-matrix.md) when product wording includes Gen 2, Gen 3, Meta Glasses, Display, or an SDK alias.
- Read the [version-dependency and device-compatibility route](../meta-wearables-knowledge-base/references/70-meta-wearables/26-version-dependency-and-device-compatibility-evidence.md) when wording includes firmware, companion/DAT-app version, support matrix, or compatibility failure.
- Read the [full SDK capability and source-conflict matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/15-full-sdk-capability-and-source-conflict-matrix.md) when the request says “full,” “regular SDK,” “all capabilities,” or parity.
- Load the portable [surface manifest](../meta-wearables-full-sdk-audit/references/surface-manifest.yaml) and resolve its `terminology_contract` before selecting a route; preserve ambiguous or unresolved status instead of translating user labels into SDK symbols.
- Read the [DAT Android API surface atlas](../meta-wearables-knowledge-base/references/70-meta-wearables/20-dat-android-api-surface-atlas.md) when Android/Kotlin/Java symbols, Maven coordinates, or 0.9 migration behavior is in scope.
- Read [Developer Center project and release operations](../meta-wearables-knowledge-base/references/70-meta-wearables/21-developer-center-project-and-release-operations.md) when account/team/project identity, tester access, versions, release channels, or telemetry is part of the route.
- Read [transport, audio, and runtime reliability](../meta-wearables-knowledge-base/references/70-meta-wearables/22-transport-audio-and-runtime-reliability.md) when the capability or failure involves Bluetooth, Wi-Fi/local network, HFP/A2DP, latency, backpressure, thermal/power, or link recovery.
- Read the [on-device compliance and runtime contract](../meta-wearables-knowledge-base/references/70-meta-wearables/17-on-device-compliance-and-runtime-contract.md) when the request says “on-device,” “local-first,” private, offline, low-latency, or asks where processing occurs.
- Read the [operational readiness and recovery route](../meta-wearables-knowledge-base/references/70-meta-wearables/18-operational-readiness-and-recovery.md) when the request includes firmware, companion versions, Developer Mode, release channels, update-required/device-unavailable errors, or recovery.
- Read the [application architecture and platform-boundaries route](../meta-wearables-knowledge-base/references/70-meta-wearables/19-application-architecture-and-platform-boundaries.md) when more than one surface, platform, capability, or phone fallback will share product behavior.
- Read [input, sensors, and physical interaction](../meta-wearables-knowledge-base/references/70-meta-wearables/24-input-sensors-and-physical-interaction.md) when the outcome depends on Display actions, D-pad/captouch, Neural Band/EMG, temple gestures, motion/orientation, geolocation, browser sensors, or an “on-device” sensor claim.
- Read the [security, attestation, and credential-boundaries route](../meta-wearables-knowledge-base/references/70-meta-wearables/25-security-attestation-and-credential-boundaries.md) when the outcome depends on bundle/package identity, Meta AI callbacks, Developer Mode, release channels, app attestation, credentials, Web App origin, privacy-manifest/App Store gates, or an “on-device” trust claim.
- Refresh the official [DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios), [DAT Android repository](https://github.com/facebook/meta-wearables-dat-android), [DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md), [DAT Android changelog](https://github.com/facebook/meta-wearables-dat-android/blob/main/CHANGELOG.md), [Wearables Developer Center](https://wearables.developer.meta.com/docs/develop/), and [Web Apps documentation](https://wearables.developer.meta.com/docs/develop/webapps).
- If the request says “regular SDK,” resolve the phrase against the current official docs and repository. Do not invent a second native iOS SDK or silently substitute Web Apps for DAT.

## Fast path

Resolve one request through the route map: exact surface, capability, runtime, fallback, and evidence. If labels such as “regular SDK” or “Gen 3” remain ambiguous, return a blocked or `to-verify` route instead of branching into every lane.

## Route map

| User outcome | Candidate route | Choose it when | First gate |
| --- | --- | --- | --- |
| iOS app discovers/uses supported glasses capabilities | native DAT iOS | the capability is exposed by the current DAT package and device | package/API and registration availability |
| Android app discovers/uses supported glasses capabilities | native DAT Android | the capability is exposed by the selected Maven artifact and device | Gradle/API and registration availability |
| glanceable native surface from the companion app | DAT Display | runtime device reports Display support | `DeviceType.supportsDisplay()` and physical model |
| HTML/CSS/JS experience delivered to Ray-Ban Display | Meta Wearables Web App | the target is explicitly the Web App surface | public HTTPS URL, 600×600, input/focus contract |
| wearer input, motion, orientation, or location | native Display, Web App, or phone fallback | the exact source is identified and the selected runtime exposes it | source/capability/permission or secure-context gate plus physical task |
| setup, consent, unavailable state, or unsupported device | phone-first fallback | wearable is absent, denied, disconnected, or not proven | useful phone workflow without wearable |
| “Gen 3 support” or unnamed future model | to-verify / blocked | official source and runtime mapping are missing | exact device type, firmware, capability, hardware |

The native DAT route and Web App route can coexist in one product, but they have different packages, lifecycle, deployment, and proof requirements.

Further sections — read when the above is not enough: `references/details.md`.
