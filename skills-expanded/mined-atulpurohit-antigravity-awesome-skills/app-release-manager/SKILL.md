---
name: app-release-manager
description: "Manage the complete mobile app release lifecycle from versioning to store submission."
category: mobile
tags: [release,mobile,deployment,versioning,stores]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# App Release Manager

## Purpose
Orchestrate reliable mobile app releases with minimal risk and smooth store submissions.

## Release Process

### Pre-Release Checklist
```
Code quality:
[ ] All tests passing (unit, integration, E2E)
[ ] No P0/P1 bugs open
[ ] Performance profiled, no regressions
[ ] Accessibility audit passed

App metadata:
[ ] Version number incremented correctly
[ ] What's New text written (< 4000 chars, no marketing speak)
[ ] Screenshots updated if UI changed significantly
[ ] Content rating still accurate
[ ] Privacy policy updated if new data collected

Store compliance:
[ ] No private APIs used
[ ] All permissions justified with usage descriptions
[ ] No third-party SDK violating store policies
```

### Version Management
```bash
# Sync versions across platforms
VERSION="1.3.0"
BUILD_NUMBER="143"

# iOS (Xcode project)
xcrun agvtool new-marketing-version $VERSION
xcrun agvtool new-version -all $BUILD_NUMBER

# Android (build.gradle)
sed -i "s/versionName ".*"/versionName "$VERSION"/" app/build.gradle
sed -i "s/versionCode [0-9]*/versionCode $BUILD_NUMBER/" app/build.gradle
```

### Phased Rollout
```
Day 1: 1% → internal team only (smoke test)
Day 3: 10% → catch critical issues
Day 7: 50% → monitor crash rates, ratings
Day 14: 100% → full release

Stop criteria:
- Crash rate > 2x previous version baseline
- Rating drops more than 0.3 stars
- ANR rate > 1.5x baseline
```

## Outputs
1. Release checklist template
2. Automated version bumping
3. Phased rollout plan
4. Store submission automation
5. Post-release monitoring dashboard