---
name: apktool
description: Android application reverse engineering, resource decoding, Smali bytecode disassembly, resource modification, and rebuild toolchain. Decodes binary XML resources (resources.arsc, AndroidManifest.xml, layouts, drawables) to human-readable form, disassembles classes.dex into Smali bytecode for step-by-step logic inspection, enables asset and resource patching, rebuilds modified packages, and integrates with zipalign and apksigner for signature re-alignment. Use when decompiling Android APKs, analyzing Smali code, modifying app manifests or assets, or rebuilding and testing modified Android binaries.
---

# Apktool — Android Binary Reverse Engineering & Resource Toolchain

A specialized toolchain and methodology for reverse engineering third-party, closed, binary Android applications (APKs and AABs). Apktool decodes binary resources to nearly original form and rebuilds them after modifications, allowing fine-grained inspection of Smali bytecode, layout XMLs, manifests, and compiled assets.

## Core Capabilities

1. **Binary XML & Resource Decoding:** Decodes binary XMLs (`AndroidManifest.xml`, layout files, value tables) and `resources.arsc` into human-readable XML files.
2. **Smali Disassembly:** Disassembles Dalvik executable (`.dex`) files into structured Smali assembly representation, preserving package and class hierarchy.
3. **Resource Modification & Injection:** Allows direct modification of assets, strings, styles, drawables, and permission declarations.
4. **Rebuilding & Repackaging:** Reassembles modified Smali code and decoded resources back into a valid APK structure.
5. **Framework Management:** Installs and manages OEM-specific framework files required for decoding proprietary manufacturer resources (Samsung, HTC, LG, Xiaomi).
6. **Signing & Alignment Pipeline:** Completes the workflow with `zipalign` 4-byte boundary alignment and `apksigner` cryptographic verification.

---

## Installation & Setup

### Prerequisites
- Java Runtime Environment (JRE) or Java Development Kit (JDK) 11 or higher
- Android SDK Build-Tools (for `zipalign` and `apksigner`)

### Execution Wrapper
Ensure `apktool.jar` is available on the system PATH or invoke directly via Java:

```bash
# Direct jar invocation
java -jar apktool.jar <command> [options]

# Via wrapper script (if installed globally)
apktool <command> [options]
```

---

## Operational Workflows

### 1. Decoding an APK (Decompilation)

Decode an APK including resources and Smali code into a designated output directory:

```bash
# Standard complete decode
apktool d target_app.apk -o output_dir

# Force overwrite existing output directory
apktool d -f target_app.apk -o output_dir

# Decode without decompiling code (resources only)
apktool d -s target_app.apk -o output_dir_resources_only

# Decode without decoding resources (code/smali only)
apktool d -r target_app.apk -o output_dir_smali_only

# Keep broken or unresolvable resources for salvage analysis
apktool d -k target_app.apk -o output_dir
```

### 2. Output Directory Structure

When decoded, the project directory contains:
- `AndroidManifest.xml`: Clean, readable manifest showing all activities, services, broadcast receivers, content providers, intent filters, and permissions.
- `apktool.yml`: Build metadata containing version info, compression flags, and original framework dependencies.
- `res/`: Decoded resources (values/strings.xml, layout/*.xml, drawable/*.xml, xml/network_security_config.xml).
- `smali/` (and `smali_classes2/`, `smali_classes3/` for Multidex): Disassembled Smali code files mirroring the Java package hierarchy.
- `assets/`: Raw embedded application assets (fonts, JSON databases, local bundles, HTML/JS assets).
- `lib/`: Native shared libraries (`.so`) organized by ABI (`arm64-v8a`, `armeabi-v7a`, `x86`, `x86_64`).
- `original/`: Original `META-INF/` signatures and untouched manifest.

### 3. Smali Code Inspection & Patching

Inspect and modify Smali instructions inside `smali/` or `smali_classes*/`:

- **Bypassing Certificate Pinning:**
  Locate `TrustManager` implementations or OkHttp `CertificatePinner` calls in Smali and replace conditional verification jumps with unconditional return statements (`return-void`).
- **Disabling Root Detection:**
  Find methods checking for `su` binaries or test-keys build tags, and patch return values to return `const/4 v0, 0x0` followed by `return v0`.
- **Enabling Debugging & Cleartext Traffic:**
  Edit `AndroidManifest.xml` to add `android:debuggable="true"` and `android:usesCleartextTraffic="true"` inside the `<application>` tag.
- **Configuring Custom Network Security:**
  Inject a custom `res/xml/network_security_config.xml` to trust user-installed CA certificates for proxy traffic inspection.

### 4. Handling OEM Framework Dependencies

When decoding applications that rely on vendor-specific system resources:

```bash
# Install framework file into Apktool local store
apktool if framework-res.apk

# Install custom tag framework (e.g. for specific OEM builds)
apktool if com.htc.resources.apk -t htc
```

### 5. Rebuilding the APK

Reassemble the modified project directory into an APK package:

```bash
# Standard rebuild
apktool b output_dir -o modified_app_unsigned.apk

# Rebuild with aapt2 enabled (recommended for modern Android Gradle Plugin outputs)
apktool b --use-aapt2 output_dir -o modified_app_unsigned.apk
```

### 6. Alignment & Cryptographic Signing

A rebuilt APK must be aligned and signed before installation on a device or emulator:

```bash
# Step 1: Align package on 4-byte boundaries
zipalign -p -f -v 4 modified_app_unsigned.apk modified_app_aligned.apk

# Step 2: Generate debug keystore if not already present
keytool -genkey -v -keystore debug.keystore -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10000 -storepass android -keypass android -dname "CN=Android Debug,O=Android,C=US"

# Step 3: Sign using apksigner (v1, v2, and v3 signature schemes)
apksigner sign --ks debug.keystore --ks-pass pass:android --key-pass pass:android --out modified_app_signed.apk modified_app_aligned.apk

# Step 4: Verify signature integrity
apksigner verify -v modified_app_signed.apk
```

---

## Defensive & Owner Security Auditing Recipes

### Security Audit Checklist with Apktool
1. **Manifest Exposure:** Check for exported components lacking proper permission gates (`android:exported="true"`).
2. **Backup Protection:** Verify `android:allowBackup="false"` to prevent unauthorized ADB data extraction.
3. **Hardcoded Secrets:** Search through `res/values/strings.xml`, `assets/`, and Smali string definitions for embedded tokens, private keys, and backend API credentials.
4. **Network Security Configuration:** Inspect `res/xml/network_security_config.xml` for cleartext exceptions or insecure base-config definitions.
5. **Dynamic Code Loading:** Search Smali for `DexClassLoader`, `InMemoryDexClassLoader`, or `PathClassLoader` instances executing untrusted external bytecode.

---

## Technical Constraints & Troubleshooting

- **Duplicate Resource Errors (`aapt: duplicate resource`):** Use the `--use-aapt2` flag during build to resolve resource namespace conflicts.
- **Multidex Reconstruction:** Apktool automatically detects multiple DEX folders (`smali_classes2`, `smali_classes3`) and repackages them into corresponding DEX files during compilation.
- **Resource ID Collisions:** When editing XML attributes, reference existing public IDs defined in `res/values/public.xml` to prevent build breakage.
- **Smali Syntax Validation:** Ensure local register allocations (`.locals` count) accommodate any added variables or constants before rebuilding.
