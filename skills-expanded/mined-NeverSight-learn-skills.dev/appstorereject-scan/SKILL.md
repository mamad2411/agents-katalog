---
name: appstorereject-scan
description: Proactive App Store and Google Play pre-submission scan. Checks your codebase for common rejection triggers before submitting an app for review. Use before first submission or app updates.
---

# Pre-Submission Scan

Scan the developer's codebase for common App Store and Google Play rejection triggers. All analysis happens locally — no code leaves the machine.

## Scan Lifecycle

### 1. Detect Platform & Framework

Check the project for these signals, in order:

| Signal | Framework | Platform |
|---|---|---|
| `app.json` or `app.config.js` with `"expo"` key | Expo | Check `platforms` field or ask |
| `react-native.config.js` or `"react-native"` in package.json dependencies | React Native CLI | Check for `ios/` and/or `android/` dirs |
| `.xcodeproj` or `.xcworkspace` (without react-native) | Native iOS | iOS |
| `build.gradle` with `android` namespace (without react-native) | Native Android | Android |

**Expo sub-detection:**
- If `ios/` and `android/` directories exist: Expo bare workflow (treat like RN CLI for native file access)
- If no `ios/`/`android/` dirs: Expo managed workflow (config lives in `app.json`)

If both iOS and Android targets detected, ask: "Scan iOS, Android, or both?"

### 2. Auto-Detect App Identity & Scan Type

Extract the bundle ID:
- **Native iOS:** `Info.plist` > `CFBundleIdentifier`
- **Expo:** `app.json` > `expo.ios.bundleIdentifier` or `expo.android.package`
- **React Native CLI:** `ios/<AppName>/Info.plist` or `android/app/build.gradle` > `applicationId`
- **Native Android:** `build.gradle` > `applicationId`

Confirm with the developer: "Detected bundle ID: `com.example.app`. Is this correct?"

Ask: "Is this your first submission to the App Store, or an update to an existing app?"

### 3. Auth Gate

Start the scan session (now that we have bundleId, scanType, and platform):
```
{baseDir}/../appstorereject/scripts/asr-api.sh POST "/api/scans/start" '{"bundleId":"<bundle_id>","scanType":"<first_submission|update>","platform":"<ios|android>"}'
```

- **200:** Proceed. Save the `scanToken` from the response.
- **403:** Show the error message to the developer (scan limit reached or app limit reached). Include the upgrade URL from the response.
- **401:** API key not set. Tell the developer to set up authentication (see hub skill instructions).

### 4. Load Platform Graph

Based on detected platform, read the appropriate graph:
- iOS: `{baseDir}/references/graph-ios.md`
- Android: `{baseDir}/references/graph-android.md`

The graph defines which sections to check and in what order. Each section has skip conditions — evaluate them before loading the section's checks.

### 5. Walk the Graph

For each section in the graph (unless skip condition is met):
1. Read the section's check file: `{baseDir}/references/checks-<section>.md`
2. Follow the framework-specific subsection matching step 1's detection
3. Execute each check (use Grep, Glob, Read tools to inspect the codebase)
4. Record findings in this format:
   - `guidelineCode`: The guideline (e.g., "5.1.1")
   - `confidence`: "high", "medium", or "low"
   - `checkId`: The check identifier (e.g., "missing_privacy_manifest")
   - `context`: A short description following the check's Context Template (max 200 chars, NO code snippets, NO file paths with usernames)

**Only load reference files for sections the graph reaches.** Skip sections whose skip condition is met.

### 6. Report to Developer

Present findings as a summary table:

```
| # | Guideline | Risk | Finding |
|---|-----------|------|---------|
| 1 | 5.1.1     | HIGH | PrivacyInfo.xcprivacy missing |
| 2 | 3.1.1     | HIGH | External payment link detected |
| 3 | 2.1       | MED  | Placeholder text in Settings screen |
```

For HIGH confidence findings, batch-fetch resolution details:
```
{baseDir}/../appstorereject/scripts/asr-api.sh GET "/api/rejections/batch?slugs=<slug1>,<slug2>,..."
```

Present each high-confidence finding with its resolution steps in the context of the developer's codebase. For medium/low findings, give a brief explanation and link to the full guide at appstorereject.com.

### 7. Report Analytics

After presenting findings:
```
{baseDir}/../appstorereject/scripts/asr-api.sh POST "/api/scans/complete" '<json>'
```

JSON body:
```json
{
  "scanToken": "<from step 3>",
  "bundleId": "<detected>",
  "platform": "ios|android",
  "framework": "native|expo|react-native",
  "findings": [
    {"guidelineCode": "5.1.1", "confidence": "high", "checkId": "missing_privacy_manifest", "context": "PrivacyInfo.xcprivacy missing"}
  ]
}
```

If this call fails, tell the developer: "Scan results were not recorded to your dashboard, but your findings are shown above."
