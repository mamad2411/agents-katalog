---
name: xcode-ios
description: "Configure Xcode targets, simulators, signing, SwiftUI or UIKit projects, and archive or export workflows."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["xcode", "ios", "signing", "simulator", "swift", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Xcode iOS Development AI Skill Guide

## Overview & Engine Architecture

Xcode builds iOS apps via targets, schemes, and provisioning. Source compiles to app bundles run on Simulator or devices; distribution uses Archive + Organizer/Transporter. Agents treat signing (Team ID, bundle ID, entitlements) as first-class config, keep secrets out of the repo, and align deployment target with API usage.

```
Xcode project / workspace
  -> Target + Scheme
      -> Compile / Link / Resource copy
          -> .app on Simulator/device
          -> Archive -> IPA / App Store Connect
```

## When to use this skill

- Creating or debugging iOS app targets in Xcode
- Fixing code signing and capability entitlements
- Running Simulator tests and capturing crashes
- Preparing TestFlight / App Store archives

## Operational directives

1. Keep bundle identifier stable; changing it breaks provisioning and push.
2. Prefer Automatic Signing for small teams; document manual profiles for enterprise.
3. Declare capabilities (Push, Associated Domains, Keychain) only when used.
4. Match Swift language mode / iOS deployment target to CI Mac image.
5. Never commit `.p12` / provisioning profiles with private keys into public repos.

## Project hygiene checklist

```
- [ ] Unique bundle ID per app/environment
- [ ] Deployment target documented
- [ ] Scheme shared for CI (`xcshareddata`)
- [ ] Secrets via CI vars / Xcode Cloud - not source
- [ ] Archive succeeds on a clean DerivedData
```

## Commands

```bash
xcodebuild -list
xcodebuild -scheme Inventory -destination 'platform=iOS Simulator,name=iPhone 16' test
xcodebuild -scheme Inventory -configuration Release archive -archivePath build/Inventory.xcarchive
xcrun simctl list devices
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Entitlement/profile mismatch | Install failures | Sync capabilities + profile |
| Hardcoded absolute SDK paths | Breaks CI | Use Xcode defaults |
| Ignoring privacy manifests | App Store issues | Declare required reason APIs |
| Testing only newest Simulator | Miss older OS bugs | Matrix a few iOS versions |

## Best practices

- Use xcconfig files for build settings shared across targets.
- Keep SPM/CocoaPods versions locked; resolve on CI cleanly.
- Capture `.crash` / metric kit data for release regressions.
- For SwiftUI previews, keep sample data free of production credentials.

## Limitations

- Full iOS signing requires Apple Developer Program access.
- Some device APIs are unavailable or stubbed on Simulator.
- Mac Catalyst / multiplatform targets add separate constraints.

## Related skills

- `@swift` - language and concurrency patterns
- `@react-native` / `@flutter` - cross-platform apps using Xcode underneath
- `@firebase` - push and analytics on iOS
