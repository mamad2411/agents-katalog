---
name: native-app-config
description: >
  Configures Ditto native Apple and Android app permissions and capabilities: Info.plist, entitlements, AndroidManifest.xml, runtime permission gates and background limits. Shared by Swift, Kotlin, React Native and Expo, reusable by Flutter/.NET adapters. Does not choose SDK-language APIs.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Shared Ditto native application configuration

This skill owns OS configuration declarations once, independently of the SDK language.
Read only the target's reference. SDK/platform skills own installation, language APIs,
autolinking and the framework adapter that applies these declarations.

## Select a platform

- [Apple](references/apple.md): iOS/iPadOS, Catalyst and sandboxed macOS. Purpose strings
  and Bonjour are Info.plist keys; signing entitlements live in the target's entitlements file.
- [Android](references/android.md): merged manifest, API-versioned runtime permission
  requests, transport choices, denial handling and optional foreground service.
- [Permission plan](assets/android-permissions.ts): portable API 23/31/33 decisions used
  by the RN adapter and tested at boundary versions. Translate these decisions when
  implementing Kotlin, Flutter or .NET; don't copy TypeScript into those applications.

## Apply and verify

Identify the app target and configured transports. Merge declarations, preserving the
application's existing keys/permissions. For Expo use its config plugin and inspect
prebuild output; don't hand-edit files that clean prebuild regenerates. Other frameworks
apply the same OS values through their platform projects/config mechanisms.

Build-time declarations do not grant runtime access. Test grant, denial, revocation,
foreground/background transitions and local-data access independently. Inspect the
built artifact: Xcode target membership/signing and Android manifest merging can differ
from source files. Do not claim real radio coverage from simulator success.

Sources and target-specific exceptions are beside each declaration in the references.
No internal Ditto source checkout or other skill is required to apply this configuration.
