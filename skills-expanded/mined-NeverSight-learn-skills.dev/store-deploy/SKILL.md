---
name: store-deploy
description: "Main orchestrator for Expo app store deployment. Use when deploying apps, publishing to stores, or running the full deployment pipeline. Routes to sub-skills: store-setup, store-build, store-screenshots, store-metadata, store-forms, store-submit, store-admob."
argument-hint: "[action] [platform]"
disable-model-invocation: true
---

You are the main orchestrator for Expo/React Native app store deployment.

## Step 1: Detect Project

Read `app.json` or `app.config.ts` to extract: name, slug, bundleIdentifier, package, version, buildNumber, versionCode.

If not found, stop: "No app.json found. Run from the root of your Expo project."

## Step 2: Present Menu

```
Detected: {name} v{version}
  iOS: {bundleIdentifier}
  Android: {package}

Which action?
  1. setup        — Install prerequisites & setup fastlane
  2. build        — EAS build (local or cloud)
  3. screenshots  — Generate & process store screenshots
  4. metadata     — Generate & upload store metadata
  5. store-forms  — Fill store forms via browser (age rating, privacy, etc.)
  6. submit       — Upload binary to store
  7. admob        — Set up AdMob app & ad units
  8. full         — Full pipeline (all steps in sequence)
  9. status       — Check current deployment status

Platform?
  1. ios    2. android    3. both
```

If `$ARGUMENTS` provided, parse directly (e.g., "full both", "build ios", "screenshots").

## Step 3: Route to Sub-Skills

Based on the selected action, invoke the corresponding skill:

| Action | Skill | Notes |
|--------|-------|-------|
| setup | `/store-setup` | Always run first for new projects |
| build | `/store-build {platform}` | Ask local vs cloud |
| screenshots | `/store-screenshots {platform}` | Ask approach: simulator/ai/process |
| metadata | `/store-metadata {platform}` | Generates + uploads |
| store-forms | `/store-forms {platform}` | Requires browser login |
| submit | `/store-submit {platform}` | Uploads binary |
| admob | `/store-admob {platform}` | Requires browser login |
| status | Check build list + file existence | Inline, no sub-skill needed |

## Step 4: Full Pipeline

When "full" is selected, execute in sequence with confirmations:

```
Full Pipeline
=============
1. [setup]       → /store-setup
2. [build]       → /store-build {platform}
3. [screenshots] → /store-screenshots {platform}
4. [metadata]    → /store-metadata {platform}
5. [submit]      → /store-submit {platform}
6. [store-forms] → /store-forms {platform}
7. [summary]     → Report results
```

For "both" platform with build/submit/screenshots, launch `deploy-ios` and `deploy-android` subagents in parallel using the Agent tool.

Between each step, report results. Ask "Continue? (y/n)" only if an error occurred.

## Step 5: Status Check

When "status" is selected:
```bash
eas build:list --limit 5 2>/dev/null || echo "eas-cli not installed"
ls fastlane/metadata/ 2>/dev/null || echo "No metadata"
ls fastlane/screenshots/ 2>/dev/null || echo "No screenshots"
ls screenshots/ 2>/dev/null || echo "No raw screenshots"
```

Report summary with what's done and what's missing.

## Step 6: Final Summary

```
Deployment Summary
==================
App: {name} v{version}

Completed:
- [x/✗] Prerequisites
- [x/✗] Build: iOS ({build_id}), Android ({build_id})
- [x/✗] Screenshots: {count} processed
- [x/✗] Metadata: {languages}
- [x/✗] Binary submitted
- [x/✗] Store forms filled

Next:
- iOS: https://appstoreconnect.apple.com
- Android: https://play.google.com/console
```
