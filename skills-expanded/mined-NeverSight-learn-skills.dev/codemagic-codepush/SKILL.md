---
name: codemagic-codepush
description: Configure and operate Codemagic-hosted CodePush for React Native iOS and Android apps, including native plugin wiring, deployment key/server URL setup, Codemagic CI integration, and OTA release lifecycle (release, promote, patch, rollback). Use when requests mention CodePush, codepush, OTA updates, @code-push-next/react-native-code-push, @codemagic/code-push-cli, codepush.pro, deployment keys, or staged iOS/Android rollout workflows.
---

# Codemagic CodePush Setup

Set up and maintain OTA update delivery for React Native apps through Codemagic-hosted CodePush (`https://codepush.pro`) across iOS and Android.

## Expected Output

Produce an implementation plan and then concrete edits/commands that include:

1. Native and JS integration steps for each requested platform.
2. Copy-paste snippets for exact files (`Info.plist`, `strings.xml`, `AppDelegate`, `MainApplication.kt`, `codemagic.yaml`).
3. CodePush app/deployment commands and how to retrieve deployment keys.
4. A release, verification, and rollback path.

## Workflow

1. Confirm scope and prerequisites.
2. Configure React Native client integration (JS + native).
3. Configure Codemagic CI and CodePush CLI auth.
4. Create platform apps/deployments and wire deployment keys.
5. Release to `Staging`, verify, then promote to `Production`.
6. Troubleshoot or rollback if verification fails.

## Step 1: Confirm Scope And Prerequisites

Do the following first:

1. Confirm the project is React Native (pure Expo managed workflow is not supported by the plugin setup).
2. Confirm Codemagic has provisioned a CodePush access token for the team.
3. Confirm whether the user wants setup for both platforms or only one.
4. Use separate CodePush app names per platform (for example `MyApp-iOS`, `MyApp-Android`).

If prerequisites are missing, stop and list what is needed.

## Step 2: Configure React Native Client Integration

1. Install plugin dependency:
   - `yarn add @code-push-next/react-native-code-push`
2. Wrap the app root component:
   - `import codePush from "@code-push-next/react-native-code-push";`
   - `export default codePush(App);`
3. Apply platform-native wiring:
   - iOS details: [references/setup-ios.md](references/setup-ios.md)
   - Android details: [references/setup-android.md](references/setup-android.md)

Always set both server URL and deployment key in native config:

1. iOS `Info.plist` keys: `CodePushServerURL`, `CodePushDeploymentKey`
2. Android `strings.xml` keys: `CodePushServerUrl`, `CodePushDeploymentKey`

## Step 3: Configure Codemagic CI + CLI

Follow [references/codepush-releases-codemagic-ci.md](references/codepush-releases-codemagic-ci.md) and [references/codepush-cli.md](references/codepush-cli.md) to ensure:

1. `@codemagic/code-push-cli` is installed in workflow scripts.
2. Login uses Codemagic server URL and token from environment variables.
3. Release commands target explicit platform app names and deployment channels.

Use [https://github.com/codemagic-ci-cd/code-push-pro](https://github.com/codemagic-ci-cd/code-push-pro) for CLI reference and ensure all commands align with the current CLI behavior, calling out any discrepancies from project docs.

## Step 4: Verify End-To-End

Follow [references/verification-and-troubleshooting.md](references/verification-and-troubleshooting.md):

1. Release to `Staging` first.
2. Validate update delivery and metrics.
3. Promote from `Staging` to `Production` only after validation.

## Execution Rules

1. Prefer exact file edits and commands over abstract guidance.
2. Keep platform differences explicit; never merge iOS and Android deployment keys.
3. Use long-form CLI flags when ambiguity exists (for example `--targetBinaryVersion`).
4. If a command in project docs differs from CLI docs, call out the difference and choose the current CLI behavior.
