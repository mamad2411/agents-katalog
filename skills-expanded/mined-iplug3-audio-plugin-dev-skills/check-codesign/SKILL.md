---
name: check-codesign
description: Check macOS code signature, hardened runtime, entitlements, and notarization of audio plugin bundles (.vst3, .component, .clap, .app/.appex). Use when user says "check code signing", "check codesign", "check signature", "verify signing", "check notarization", "why won't plugin load", "hardened runtime", "check entitlements", or a plugin fails to load in a signed DAW.
compatibility: macOS only. Uses codesign, spctl, and stapler from Xcode command-line tools.
metadata:
  author: Oli Larkin
  version: 0.0.1
---

# macOS Code Signature Check

## Why This Matters

macOS DAWs built with hardened runtime (Logic Pro, GarageBand, recent versions of Ableton Live, etc.) will refuse to load unsigned or incorrectly signed plugins. Gatekeeper and library validation enforcement mean that even a plugin passing all functional tests can silently fail to load if its code signature is missing, invalid, or lacks required entitlements.

## Plugin Bundle Locations

| Format | Extension | Typical Paths |
|--------|-----------|---------------|
| AudioUnit v2 | `.component` | `~/Library/Audio/Plug-Ins/Components/`, `/Library/Audio/Plug-Ins/Components/` |
| AudioUnit v3 | `.appex` (inside `.app`) | Built into host app bundle |
| VST3 | `.vst3` | `~/Library/Audio/Plug-Ins/VST3/`, `/Library/Audio/Plug-Ins/VST3/` |
| CLAP | `.clap` | `~/Library/Audio/Plug-Ins/CLAP/`, `/Library/Audio/Plug-Ins/CLAP/` |

## Instructions

1. Locate the plugin bundle on disk
2. Run `codesign -vvv --deep --strict /path/to/plugin.bundle` to verify the signature
3. Run `codesign -d --verbose=4 /path/to/plugin.bundle` to display signing details
4. Check for hardened runtime flag in the output (flags should include `runtime`)
5. Run `codesign -d --entitlements - /path/to/plugin.bundle` to inspect entitlements
6. If the plugin is distributed outside the App Store, check notarization with `spctl --assess`
7. See Common Issues below if verification fails

## Basic Usage

```bash
# Verify the code signature is valid (deep checks nested code)
codesign -vvv --deep --strict /path/to/plugin.vst3

# Display full signing information
codesign -d --verbose=4 /path/to/plugin.vst3

# Display entitlements
codesign -d --entitlements - /path/to/plugin.vst3

# Display just the signing identity (Team ID and certificate name)
codesign -d --verbose=1 /path/to/plugin.vst3
```

## Checking Hardened Runtime

Hardened runtime is required for notarization and for loading into DAWs that enforce library validation.

```bash
# Check flags — look for "runtime" in the flags line
codesign -d --verbose=4 /path/to/plugin.vst3
```

In the output, look for the `flags` line:

- `flags=0x10000(runtime)` — hardened runtime is enabled
- `flags=0x0(none)` — hardened runtime is **not** enabled (will fail in hardened DAWs)

## Entitlements for Audio Plugins

Audio plugins that use JIT compilation, dynamically generated code, or load other unsigned libraries typically need specific entitlements.

| Entitlement | Purpose |
|------------|---------|
| `com.apple.security.cs.disable-library-validation` | Load unsigned or differently-signed libraries/plugins |
| `com.apple.security.cs.allow-unsigned-executable-memory` | JIT / writable-executable memory (some DSP code, scripting engines) |
| `com.apple.security.cs.allow-jit` | MAP_JIT support for JIT compilers |
| `com.apple.security.cs.allow-dyld-environment-variables` | Allow DYLD_* environment variables |

```bash
# View entitlements as XML plist
codesign -d --entitlements - --xml /path/to/plugin.vst3

# View entitlements in human-readable form
codesign -d --entitlements - /path/to/plugin.vst3
```

**Note:** The DAW (host) must also have `com.apple.security.cs.disable-library-validation` for it to load third-party plugins that are signed with a different Team ID.

## Checking Notarization

Notarized plugins have been scanned by Apple and stapled with a ticket, allowing them to pass Gatekeeper on first launch without an internet check.

```bash
# Check if a notarization ticket is stapled to the bundle
stapler validate /path/to/plugin.vst3

# Force an online notarization check (even without a stapled ticket)
codesign -v --check-notarization /path/to/plugin.vst3

# Check Gatekeeper assessment (requires the bundle to be in a standard location or downloaded)
spctl --assess --verbose=4 --type exec /path/to/plugin.vst3
```

For installer packages (`.pkg`):

```bash
spctl --assess --verbose=4 --type install /path/to/installer.pkg
```

## Checking a DAW Host

If a plugin won't load, it can help to check the host DAW's own signing and entitlements to understand its library validation policy.

```bash
# Check if a DAW has library validation disabled (allows loading third-party plugins)
codesign -d --entitlements - /Applications/SomeDAW.app

# Look for com.apple.security.cs.disable-library-validation = true
```

## Note on `--deep`

The `--deep` flag is deprecated for signing as of macOS 13. When signing, sign each nested component individually instead. `--deep` is still valid for verification.

## Ad-Hoc Signatures

Ad-hoc signed binaries (signed with `-` instead of a Developer ID) have limited trust:

```bash
# Identify ad-hoc signing — authority will show as empty or "(unavailable)"
codesign -d --verbose=1 /path/to/plugin.vst3
```

Ad-hoc signed plugins will **not** load in DAWs with hardened runtime and library validation unless the DAW explicitly disables library validation.

## Re-signing a Plugin (Development)

During development you may need to re-sign a plugin to test with a specific identity or entitlements.

```bash
# Sign with your Developer ID and hardened runtime
codesign --force --sign "Developer ID Application: Your Name (TEAMID)" \
  --options runtime \
  --timestamp \
  /path/to/plugin.vst3

# Sign with entitlements file
codesign --force --sign "Developer ID Application: Your Name (TEAMID)" \
  --options runtime \
  --timestamp \
  --entitlements entitlements.plist \
  /path/to/plugin.vst3

# Ad-hoc sign for local development (no Apple Developer account)
codesign --force --sign - /path/to/plugin.vst3
```

A minimal `entitlements.plist` for audio plugins:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
</dict>
</plist>
```

## Common Issues

### Plugin Not Loading in DAW (No Error)

The most common cause is a code signature problem. Check in this order:

1. **Unsigned:** `codesign -v` reports `code object is not signed at all` — sign the plugin
2. **Ad-hoc signed:** Authority shows `(unavailable)` — sign with a Developer ID for distribution
3. **No hardened runtime:** Flags show `0x0(none)` — re-sign with `--options runtime`
4. **Modified after signing:** `a sealed resource is missing or invalid` — rebuild and re-sign
5. **Team ID mismatch:** DAW enforces library validation and plugin is signed by a different team — DAW needs `disable-library-validation` entitlement

### "code signature invalid" After Rebuild

Building replaces binaries inside the bundle, invalidating the signature. Always sign **after** the final build step. Most build systems (Xcode, CMake) can be configured to sign automatically as a post-build step.

### Resource Envelope Issues

```
a sealed resource is missing or invalid
```

- A file inside the bundle was added or modified after signing
- Re-sign the bundle after all contents are finalized
- Use `codesign -vvv` to see which specific resource failed

### "not notarized" Warning on User Machines

```bash
# Check if the ticket is stapled
stapler validate /path/to/plugin.vst3

# If not stapled, staple after notarization
xcrun stapler staple /path/to/plugin.vst3
```

### Architecture Mismatches

Universal binaries must have valid signatures for all architectures:

```bash
# List architectures in the binary
lipo -info /path/to/plugin.vst3/Contents/MacOS/plugin

# Verify signature for a specific architecture
codesign -vvv --arch arm64 /path/to/plugin.vst3
codesign -vvv --arch x86_64 /path/to/plugin.vst3
```
