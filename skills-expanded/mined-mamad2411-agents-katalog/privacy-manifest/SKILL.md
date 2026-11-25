---
name: privacy-manifest
description: Draft or review an Apple privacy manifest for an app or package.
disable-model-invocation: true
---
# Privacy Manifest

Create or review a `PrivacyInfo.xcprivacy` file for an Apple app or package.

## When to Use

- When adding a new SDK, tracking surface, or required-reason API.
- Before TestFlight or App Store submission.

## Inputs

- Collected data types and tracking behavior
- SDKs or APIs that require reason declarations
- App targets or packages affected

## Instructions

1. Identify collected data, tracking declarations, and required-reason APIs.
2. Align the manifest with actual app behavior and third-party SDK usage.
3. Call out gaps between the manifest, `Info.plist`, and entitlements.
4. List reviewer follow-ups before release.

## Output

- A manifest checklist with any required declarations and open questions.
