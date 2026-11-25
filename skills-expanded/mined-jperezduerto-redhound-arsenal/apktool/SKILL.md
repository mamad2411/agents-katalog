---
name: apktool
description: >
  Reverse engineer Android APKs using Apktool. Use when decoding APKs to smali
  and resources, rebuilding modified APKs, bypassing certificate pinning, injecting
  Frida gadgets, analyzing AndroidManifest.xml for attack surface, modifying
  network security config, or performing combined static analysis with jadx. Covers
  installation, decode/rebuild workflow, framework management, smali code structure,
  APK signing, manifest analysis, certificate pinning bypass, Frida gadget
  injection, and integration with jadx for full decompilation.
metadata:
  author: redhoundinfosec
  version: '1.0'
  reference: https://github.com/iBotPeaches/Apktool
---

# apktool Agent Skill

## When to Use This Skill

Use this skill when:
- Reverse engineering Android APKs (decode resources, smali, manifests)
- Modifying APK resources, strings, layouts, or smali code and rebuilding
- Bypassing certificate pinning via network_security_config.xml modification
- Injecting Frida gadget into an APK for dynamic analysis without root
- Analyzing AndroidManifest.xml for exported components, permissions, deep links
- Installing OEM/vendor frameworks for decompiling system APKs
- Combining Apktool's resource decode with jadx's Java decompilation

## What Apktool Does

Apktool decodes Android APK files into their constituent resources: smali bytecode
(Dalvik disassembly), XML resources (layouts, strings, manifests), and assets.
It can then rebuild the modified directory back into a signed APK. Unlike jadx,
which decompiles to Java source, Apktool operates at the smali level — essential
for precise modifications, resource patching, and gadget injection that require
exact bytecode control.

## Installation

```bash
# Prerequisites: Java 8+ (Java 11+ recommended)
java -version  # verify

# Option 1: Direct download (recommended — always latest)
wget https://github.com/iBotPeaches/Apktool/releases/latest/download/apktool.jar
wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
chmod +x apktool
sudo mv apktool /usr/local/bin/
sudo mv apktool.jar /usr/local/bin/

# Option 2: Homebrew (macOS)
brew install apktool

# Option 3: Package manager (often outdated)
sudo apt install apktool

# Verify
apktool --version

# Windows
# Download apktool.jar and apktool.bat from releases
# Place both in C:\Windows\
```

## Core Workflow: Decode → Modify → Rebuild → Sign

```bash
# Step 1: Decode APK
apktool d target.apk

# Step 2: Modify files in target/ directory
# Step 3: Rebuild APK
apktool b target/ -o target_modified.apk

# Step 4: Sign APK (required for installation)
# Generate debug keystore (one-time)
keytool -genkey -v -keystore debug.keystore -alias debugkey \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -storepass android -keypass android \
  -dname "CN=Debug,O=Debug,C=US"

# Sign with apksigner (Android SDK Build Tools)
apksigner sign --ks debug.keystore --ks-key-alias debugkey \
  --ks-pass pass:android --key-pass pass:android \
  --out target_signed.apk target_modified.apk

# Or sign with jarsigner (older method)
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore debug.keystore -storepass android \
  target_modified.apk debugkey

# Install on device
adb install target_signed.apk
```

## Decode Options

```bash
# Standard decode (full: resources + smali)
apktool d target.apk

# Decode to specific output directory
apktool d target.apk -o /opt/analysis/target/

# Decode without disassembling smali (resources only)
apktool d target.apk --no-src

# Decode without decoding resources (smali only)
apktool d target.apk --no-res

# Force overwrite existing output directory
apktool d target.apk -f

# Decode with specific API level (for resource resolution)
apktool d target.apk --api 30

# Keep broken resources (don't fail on resource decode errors)
apktool d target.apk --keep-broken-res

# Decode specific framework-dependent APK
apktool d -t samsung target.apk
```

## Rebuild Options

```bash
# Basic rebuild
apktool b target/

# Rebuild to specific output file
apktool b target/ -o rebuilt.apk

# Force rebuild all (don't use cached resources)
apktool b target/ -f

# Rebuild with debug mode
apktool b target/ --debug

# Use aapt2 for rebuild (required for newer apps)
apktool b target/ --use-aapt2
```

## Framework Installation

OEM/vendor APKs depend on custom frameworks. Install them before decoding.

```bash
# Install framework APK
apktool if framework-res.apk

# Install with tag (for multiple OEM frameworks)
apktool if samsung-framework.apk -t samsung

# List installed frameworks
apktool empty-framework-dir --list  # or manually:
ls ~/.local/share/apktool/framework/

# Remove all frameworks (reset)
apktool empty-framework-dir

# System APKs on device — pull framework first
adb pull /system/framework/framework-res.apk
apktool if framework-res.apk

# Then decode system APK
apktool d /system/app/SystemUI/SystemUI.apk
```

## Smali Code Structure

Smali is the human-readable form of Dalvik bytecode. Files map 1:1 to Java classes.

```smali
# File: smali/com/example/app/MainActivity.smali

.class public Lcom/example/app/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "MainActivity.java"

# Fields
.field private mApiKey:Ljava/lang/String;

# Method definition
.method public onCreate(Landroid/os/Bundle;)V
    .locals 2                    # number of local registers (v0, v1)

    # Call super
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    # Load constant string into v0
    const-string v0, "https://api.example.com"

    # Assign to field
    iput-object v0, p0, Lcom/example/app/MainActivity;->mBaseUrl:Ljava/lang/String;

    # Call method
    invoke-virtual {p0}, Lcom/example/app/MainActivity;->checkCertificate()V

    return-void
.end method
```

Key smali register conventions:
- `v0, v1, v2...` — local registers (count declared by `.locals N`)
- `p0` — `this` reference (instance methods)
- `p1, p2...` — method parameters

## AndroidManifest.xml Analysis

After decoding, inspect `AndroidManifest.xml` for attack surface:

```bash
# View decoded manifest
cat target/AndroidManifest.xml | grep -A3 "exported"

# Exported Activities (accessible without permission — entry points)
grep -n 'exported="true"' target/AndroidManifest.xml | grep "activity"

# Exported Services
grep -n 'exported="true"' target/AndroidManifest.xml | grep "service"

# Exported Content Providers (potential SQL injection, path traversal)
grep -n 'exported="true"' target/AndroidManifest.xml | grep "provider"

# Broadcast Receivers (potential intent injection)
grep -n 'exported="true"' target/AndroidManifest.xml | grep "receiver"

# Dangerous permissions requested
grep -n "permission" target/AndroidManifest.xml | grep -i "READ_CONTACTS\|RECORD_AUDIO\|CAMERA\|ACCESS_FINE_LOCATION"

# Deep link schemes (URL scheme handling — potential open redirect/CSRF)
grep -n "scheme\|host\|pathPrefix" target/AndroidManifest.xml

# Backup allowed (enables adb backup data exfiltration)
grep "allowBackup" target/AndroidManifest.xml

# Debuggable flag (allows adb debug attach)
grep "debuggable" target/AndroidManifest.xml
```

## Certificate Pinning Bypass (network_security_config.xml)

### Method 1: Modify network_security_config.xml
```bash
apktool d target.apk -o target/

# Check if network security config is referenced
grep "networkSecurityConfig" target/AndroidManifest.xml
# Look for: android:networkSecurityConfig="@xml/network_security_config"

# Edit (or create) res/xml/network_security_config.xml
cat > target/res/xml/network_security_config.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <!-- Trust system CAs (default) -->
            <certificates src="system" />
            <!-- Trust user-installed CAs (Burp cert) -->
            <certificates src="user" />
        </trust-anchors>
    </base-config>
</network-security-config>
EOF

# Ensure manifest references the config (if not already)
# In AndroidManifest.xml, add to <application> tag:
# android:networkSecurityConfig="@xml/network_security_config"

# Rebuild and sign
apktool b target/ -o target_patched.apk
apksigner sign --ks debug.keystore --ks-key-alias debugkey \
  --ks-pass pass:android --key-pass pass:android \
  --out target_signed.apk target_patched.apk
adb install target_signed.apk
```

### Method 2: Disable Pinning in Smali (Hard-coded pinning)
```bash
# Find pinning implementation
grep -r "CertificatePinner\|checkServerTrusted\|HostnameVerifier\|TrustManager" \
  target/smali/ -l

# Open the smali file and find the verification method
# Common pattern to patch: change return-void of checkServerTrusted
# Or: remove the certificate hash check (const-string with sha256/ hash)

# Example: Returning immediately from checkServerTrusted
# Original:
#   invoke-virtual {v0, p1}, Lsome/PinningClass;->verify(...)V
#   <complex validation logic>
# Patch: add 'return-void' after method entry or remove hash comparison
```

## Frida Gadget Injection

Inject Frida gadget into APK to enable dynamic instrumentation without root.

```bash
# Step 1: Decode APK
apktool d target.apk -o target/

# Step 2: Download Frida gadget for target arch
# Check device arch: adb shell getprop ro.product.cpu.abi
# e.g., arm64-v8a, armeabi-v7a, x86, x86_64
ARCH=arm64-v8a
VER=$(curl -s https://api.github.com/repos/frida/frida/releases/latest | jq -r .tag_name)
wget "https://github.com/frida/frida/releases/download/${VER}/frida-gadget-${VER}-android-${ARCH}.so.xz"
unxz frida-gadget-*.so.xz
cp frida-gadget-*.so target/lib/${ARCH}/libfrida-gadget.so

# Step 3: Find the first loaded smali class (usually MainActivity)
# Add gadget load to the beginning of the static constructor or onCreate:
# In smali, find .method public constructor <init>()V or onCreate
# Add these lines at the start of the method:

# const-string v0, "frida-gadget"
# invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

# Step 4: Add INTERNET permission to manifest (if not present)
# <uses-permission android:name="android.permission.INTERNET" />

# Step 5: Rebuild and sign
apktool b target/ -o target_frida.apk
apksigner sign --ks debug.keystore --ks-key-alias debugkey \
  --ks-pass pass:android --key-pass pass:android \
  --out target_frida_signed.apk target_frida.apk

# Step 6: Install and run
adb install target_frida_signed.apk
adb shell am start -n com.target.app/.MainActivity

# Step 7: Attach Frida scripts
frida -U Gadget -l your_script.js
```

## Modifying Resources

```bash
# Edit string resources
nano target/res/values/strings.xml
# Change API endpoints, hardcoded URLs, flag values

# Edit layouts (for UI analysis or bypass)
# target/res/layout/activity_main.xml

# Change app package name (for parallel install)
# In AndroidManifest.xml: change package="com.target.app" to "com.target.app.test"
# Also update all smali references — complex; prefer dextools for this

# Disable root detection in smali
grep -r "isRooted\|RootBeer\|checkRootMethod" target/smali/ -l
# Open file, find method, replace return value with:
# const/4 v0, 0x0    # false
# return v0
```

## Integration with jadx

Apktool + jadx together provide the complete static analysis workflow:

```bash
# jadx: Java decompilation (human-readable source)
jadx target.apk -d jadx_output/
# Navigate: jadx_output/sources/com/target/app/

# Apktool: smali + resources (precise patching, resource decode)
apktool d target.apk -o apktool_output/

# Workflow:
# 1. Use jadx to understand app logic (Java code easier to read)
# 2. Find the class/method to patch
# 3. Open corresponding smali in apktool_output/
# 4. Apply targeted smali patch
# 5. Rebuild and sign with apktool

# Mass string extraction for analysis
grep -r "http\|https" jadx_output/sources/ | grep -v ".class"
grep -r "password\|secret\|api_key\|token" jadx_output/sources/ -i
```

## Common Smali Patching Patterns

```smali
# Disable boolean check (make method always return true)
.method public isLicensed()Z
    .locals 1
    const/4 v0, 0x1      # 0x1 = true
    return v0
.end method

# Disable boolean check (always return false — e.g., isRooted)
.method public isRooted()Z
    .locals 1
    const/4 v0, 0x0      # 0x0 = false
    return v0
.end method

# Disable void method (no-op a validation function)
.method public checkLicense()V
    .locals 0
    return-void
.end method

# Replace hardcoded URL
# Find: const-string v0, "https://prod.api.example.com"
# Replace with: const-string v0, "http://192.168.1.10:8080"
```

## Troubleshooting

**`brut.androlib.AndrolibException: Could not decode arsc file`**: App uses
non-standard resource encoding. Try `--keep-broken-res` flag.

**`aapt: error`**: Rebuild fails with resource errors. Use `--use-aapt2` flag.
If still failing, check that modified XML is valid (no syntax errors).

**`INSTALL_FAILED_UPDATE_INCOMPATIBLE`**: Signed with different key than installed version.
Uninstall first: `adb uninstall com.target.app`

**`INSTALL_PARSE_FAILED_NO_CERTIFICATES`**: APK not signed. Run apksigner step.

**Smali compile error**: Check that register count in `.locals N` matches actual
register usage. Adding instructions may require incrementing `.locals`.

**Framework not found**: Pull from device first:
`adb pull /system/framework/framework-res.apk && apktool if framework-res.apk`

**App crashes after patch**: Dalvik verifier rejected bytecode. Verify smali
syntax with `smali/baksmali` tools: `java -jar baksmali.jar d classes.dex`
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
