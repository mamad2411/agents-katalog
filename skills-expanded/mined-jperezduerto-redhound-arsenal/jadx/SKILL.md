---
name: jadx
description: >
  Decompile and reverse engineer Android APK, DEX, AAR, and JAR files using JADX
  (skylot/jadx, 43k+ stars). Use when performing mobile application security assessments,
  hunting for hardcoded secrets/API keys, analyzing AndroidManifest.xml for exported
  components, reverse engineering API calls, or preparing for dynamic analysis with
  Frida. Covers jadx CLI and jadx-gui, output structure, deobfuscation options,
  Smali vs Java output, Gradle export, thread tuning, secret/key hunting workflows,
  and integration with Frida for dynamic analysis following static review.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/skylot/jadx
---

# jadx Agent Skill

## When to Use This Skill

Use this skill when:
- Performing a mobile application security assessment on an Android APK
- Hunting for hardcoded API keys, tokens, credentials, or sensitive data in APK source
- Analyzing AndroidManifest.xml for attack surface (exported activities, deep links)
- Reverse engineering API endpoints, authentication flows, or cryptographic implementations
- Deobfuscating obfuscated Android code before dynamic analysis with Frida
- The user has a .apk, .dex, .aar, or .jar file to analyze

## What JADX Does

JADX is a DEX to Java decompiler. It converts Dalvik bytecode (`.dex` files inside `.apk`) back into human-readable Java source code. Unlike Smali disassemblers (baksmali) that produce assembly-level output, JADX produces near-original Java, making it significantly easier to read business logic, API integrations, and security controls. JADX supports APK, DEX, AAR, JAR, ZIP, and class files. The GUI (jadx-gui) adds search, navigation, and cross-reference features critical for efficient code review.

## Installation

```bash
# Kali Linux
sudo apt update && sudo apt install jadx
jadx --version

# Download pre-built release (recommended — always latest)
# From: https://github.com/skylot/jadx/releases/latest
wget https://github.com/skylot/jadx/releases/latest/download/jadx-<version>.zip
unzip jadx-<version>.zip -d /opt/jadx
chmod +x /opt/jadx/bin/jadx /opt/jadx/bin/jadx-gui
ln -s /opt/jadx/bin/jadx /usr/local/bin/jadx
ln -s /opt/jadx/bin/jadx-gui /usr/local/bin/jadx-gui

# macOS via Homebrew
brew install jadx

# Build from source
git clone https://github.com/skylot/jadx.git
cd jadx && ./gradlew dist
# Output: build/jadx/bin/jadx and jadx-gui

# Docker (CLI only)
docker run --rm -v $(pwd):/work ghcr.io/skylot/jadx jadx --help

# Verify
jadx --version
```

## Core Concepts

### Android APK Structure

An APK is a ZIP archive. JADX processes the following components:

```
target.apk (ZIP)
├── AndroidManifest.xml      — App permissions, components, intents (binary XML)
├── classes.dex              — Main Dalvik bytecode → JADX decompiles to Java
├── classes2.dex             — Additional DEX (multidex apps)
├── classes3.dex             — Further DEX shards
├── resources.arsc           — Compiled string/layout resources
├── res/                     — XML layouts, drawables, raw assets
│   ├── layout/
│   ├── values/strings.xml
│   └── raw/                 — Potential: keys, certs, config files
├── assets/                  — Arbitrary files bundled with app
│   └── config.json          — Often contains URLs, tokens
├── lib/                     — Native libraries (.so)
│   ├── arm64-v8a/
│   └── x86_64/
└── META-INF/                — Signing info (certificates)
    ├── CERT.RSA
    └── MANIFEST.MF
```

### Smali vs JADX Java Output

| | Smali | JADX Java |
|---|-------|-----------|
| Output level | Dalvik assembly (register-based) | Java source |
| Readability | Low — requires Dalvik expertise | High — readable business logic |
| Accuracy | Exact (1:1 with bytecode) | ~95% — some constructs can't round-trip |
| Use case | Patching, exact byte modification | Code review, logic analysis |
| Tool | baksmali / apktool | jadx |

JADX is preferred for static analysis. Use apktool + smali for patching/instrumentation.

### Obfuscation

ProGuard/R8 obfuscation renames classes (`com.example.MainActivity` → `a.b.c`), methods, and fields. JADX's `--deobf` flag uses heuristics to restore readable names where possible and generates a mapping file. Third-party obfuscators (DexGuard, Obfuscapk) may require manual renaming.

## CLI Reference

```bash
# Basic decompile APK to output directory
jadx -d /tmp/output target.apk

# Decompile DEX file
jadx -d /tmp/output classes.dex

# Decompile AAR (Android library)
jadx -d /tmp/output library.aar

# Decompile JAR
jadx -d /tmp/output target.jar

# Key flags
--deobf                   # Enable deobfuscation (rename short identifiers)
--deobf-min LEN           # Min identifier length to deobf (default: 3)
--deobf-max LEN           # Max identifier length to deobf (default: 64)
--deobf-rewrite-cfg       # Rewrite CFG with deobfuscated names
--deobf-use-sourcename    # Use source file attribute for class names
-t N / --threads-count N  # Thread count (default: CPU cores)
--no-res                  # Skip resource decompilation (faster, Java only)
--no-src                  # Skip source decompilation (resources only)
-e / --export-gradle      # Export as Android Studio Gradle project
--show-bad-code           # Include code that failed to decompile
--no-imports              # Don't add import statements (raw class names)
--single-class CLASS      # Decompile only one class
--output-format (folder|single-file)  # Output format
-v                        # Verbose
--log-level (quiet|progress|error|warn|info|debug)
--fs-case-sensitive       # Case-sensitive file system (macOS default: insensitive)

# Full decompile with deobfuscation, all threads, Gradle export
jadx -d /tmp/output --deobf --deobf-min 2 -t 8 -e target.apk

# Fast partial decompile (Java source only, no resources)
jadx -d /tmp/output --no-res -t 8 target.apk

# Extract resources only (strings, layouts)
jadx -d /tmp/output --no-src target.apk
```

## JADX-GUI Usage

```bash
# Launch GUI
jadx-gui
jadx-gui target.apk  # Open directly

# GUI key features:
# File → Open (APK/DEX/JAR/AAR)
# File → Save All → saves decompiled source
# Navigation → Class tree on left panel
# Search:
#   Text search: Ctrl+F (current file), Ctrl+Shift+F (all code)
#   Class search: Ctrl+N
#   Method search: Ctrl+Alt+M
#   Field search: Ctrl+F3
# Right-click → Find Usage (cross-references)
# Right-click → Jump to Declaration
# Code → Rename (deobfuscation — rename a class/method interactively)
```

## Output Structure

After `jadx -d /tmp/output target.apk`:

```
/tmp/output/
├── sources/               # Decompiled Java source
│   ├── com/
│   │   └── example/
│   │       └── app/
│   │           ├── MainActivity.java
│   │           ├── network/
│   │           │   └── ApiClient.java
│   │           └── utils/
│   │               └── CryptoUtils.java
│   └── kotlin/            # Kotlin standard library (decompiled)
├── resources/             # Decompiled resources
│   ├── AndroidManifest.xml  # Decoded binary XML
│   ├── res/
│   │   ├── values/
│   │   │   └── strings.xml
│   │   └── layout/
│   └── assets/
└── jadx-input-mapping.txt # Deobfuscation mapping (if --deobf used)
```

## Common Workflows

### Initial APK Triage

```bash
# Step 1: Unzip and inspect raw structure
cp target.apk target.zip && unzip target.zip -d raw_apk/
ls raw_apk/

# Step 2: Decompile
jadx -d /tmp/decompiled --deobf -t 8 target.apk

# Step 3: Read AndroidManifest.xml
cat /tmp/decompiled/resources/AndroidManifest.xml

# Step 4: Find the application's package name
grep "package=" /tmp/decompiled/resources/AndroidManifest.xml | head -1
```

### Hunting for Hardcoded Secrets

```bash
# API keys, tokens, secrets — broad pattern
grep -rE "(api_key|apikey|api-key|secret|token|password|passwd|credential)" \
     /tmp/decompiled/sources/ \
     --include="*.java" -i -l | head -20

# Specific patterns
# AWS keys
grep -rE "AKIA[0-9A-Z]{16}" /tmp/decompiled/ --include="*.java" --include="*.xml"

# Google API keys
grep -rE "AIza[0-9A-Za-z\\-_]{35}" /tmp/decompiled/

# Firebase URLs
grep -rE "https://[a-z0-9-]+\.firebaseio\.com" /tmp/decompiled/

# Bearer tokens / JWTs
grep -rE "Bearer\s+[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+" /tmp/decompiled/

# Private keys
grep -rE "BEGIN (RSA |EC )?PRIVATE KEY" /tmp/decompiled/

# Database connection strings
grep -rE "(jdbc|mongodb|postgresql|mysql)://" /tmp/decompiled/ -i

# Hardcoded passwords / credentials
grep -rE "(password|passwd|secret)\s*=\s*['\"][^'\"]{4,}" /tmp/decompiled/sources/ -i

# Strings XML (compiled strings — often contains URLs and keys)
cat /tmp/decompiled/resources/res/values/strings.xml | grep -iE "key|token|secret|url|endpoint"

# Search assets directory
find /tmp/decompiled/resources/assets/ -type f | xargs grep -l "key\|secret\|token\|api" 2>/dev/null

# Config files in assets
cat /tmp/decompiled/resources/assets/config.json 2>/dev/null
find /tmp/decompiled/resources/assets/ -name "*.json" -exec cat {} \;
```

### AndroidManifest.xml Analysis

```bash
# Full manifest review
cat /tmp/decompiled/resources/AndroidManifest.xml

# Find exported components (attack surface)
# Exported Activity (accessible from other apps or ADB)
grep -A5 "activity" /tmp/decompiled/resources/AndroidManifest.xml | grep -i "exported=\"true\""

# Exported broadcast receivers (can receive intents from any app)
grep -A5 "receiver" /tmp/decompiled/resources/AndroidManifest.xml | grep -i "exported\|intent-filter"

# Exported content providers (data accessible without auth)
grep -A5 "provider" /tmp/decompiled/resources/AndroidManifest.xml | grep -i "exported\|authority"

# Deep links (custom URI schemes)
grep -B2 -A10 "scheme" /tmp/decompiled/resources/AndroidManifest.xml

# Permissions declared and used
grep "permission\|uses-permission" /tmp/decompiled/resources/AndroidManifest.xml

# Dangerous permissions
grep -iE "CAMERA|READ_CONTACTS|RECORD_AUDIO|ACCESS_FINE_LOCATION|READ_CALL_LOG|SEND_SMS|READ_EXTERNAL" \
     /tmp/decompiled/resources/AndroidManifest.xml

# Backup attribute (android:allowBackup="true" = ADB backup possible)
grep "allowBackup\|debuggable" /tmp/decompiled/resources/AndroidManifest.xml

# Network security config
grep "networkSecurityConfig" /tmp/decompiled/resources/AndroidManifest.xml
```

### Reverse Engineering API Calls

```bash
# Find network/HTTP client usage
grep -rl "OkHttpClient\|Retrofit\|HttpURLConnection\|Volley\|HttpClient" \
     /tmp/decompiled/sources/ --include="*.java"

# Extract base URLs
grep -rE "https?://[a-zA-Z0-9./_-]+" /tmp/decompiled/sources/ --include="*.java" | \
  grep -v "//\s" | sort -u

# Find Retrofit interface definitions (API endpoints)
grep -rE "@(GET|POST|PUT|DELETE|PATCH)\s*\([\"']" /tmp/decompiled/sources/ --include="*.java"

# Find authentication headers
grep -rE "Authorization|Bearer|X-API-Key|X-Auth" /tmp/decompiled/sources/ -i --include="*.java"

# Intercept certificate pinning implementation
grep -rE "CertificatePinner|TrustManager|X509|hostnameVerifier|checkServerTrusted" \
     /tmp/decompiled/sources/ --include="*.java" -l
```

### Gradle Export (For Android Studio)

```bash
# Export as importable Android Studio project
jadx -d /tmp/gradle_project --export-gradle target.apk

# Open in Android Studio:
# File → Open → navigate to /tmp/gradle_project → Open
# Build → Make Project (may fail due to decompilation artifacts but aids navigation)
```

## Advanced Techniques

### Deobfuscation Workflow

```bash
# Step 1: Decompile with --deobf
jadx -d /tmp/deobf --deobf --deobf-min 2 -t 8 target.apk

# Step 2: Check mapping file
cat /tmp/deobf/jadx-input-mapping.txt | head -50

# Step 3: In jadx-gui — rename interactively
# Right-click class/method → Rename → type readable name
# Renaming persists within the session and updates all references

# Step 4: Identify library code (ignore it)
# Common pattern: obfuscated classes in same package = app code; 
# well-named classes = third-party libs (OkHttp, Retrofit, Firebase)

# Step 5: Search for entry points
grep -r "extends Activity\|extends Fragment\|extends Service\|extends BroadcastReceiver" \
     /tmp/deobf/sources/ --include="*.java" -l
```

### Certificate Pinning Bypass Preparation

```bash
# Identify pinning implementation
grep -rE "CertificatePinner|TrustManager|checkValidity|pin\(" \
     /tmp/decompiled/sources/ --include="*.java" -l

# View the pinning code
grep -rA 20 "CertificatePinner" /tmp/decompiled/sources/ --include="*.java" | head -60

# Use this to write Frida hook targeting the exact method signature
```

### Integration with Frida (Static → Dynamic)

After static analysis with JADX, use Frida for dynamic instrumentation:

```bash
# 1. Install Frida
pip3 install frida-tools
frida --version

# 2. Push frida-server to device
adb push frida-server-<version>-android-arm64 /data/local/tmp/frida-server
adb shell chmod +x /data/local/tmp/frida-server
adb shell /data/local/tmp/frida-server &

# 3. List running apps
frida-ps -Ua

# 4. Hook method identified in JADX (example: bypass SSL pinning)
frida -U -n com.example.app -l ssl_bypass.js

# Example Frida hook based on JADX analysis:
# JADX found: com.example.app.network.ApiClient.buildOkHttpClient()
# Frida hook:
cat > hook.js << 'EOF'
Java.perform(function() {
    var ApiClient = Java.use("com.example.app.network.ApiClient");
    ApiClient.buildOkHttpClient.implementation = function() {
        console.log("[*] buildOkHttpClient called — bypassing pin");
        var client = this.buildOkHttpClient();
        return client;
    };
});
EOF
frida -U -n com.example.app -l hook.js

# 5. Trace all methods in a class (identified via JADX)
frida-trace -U -n com.example.app -j "com.example.app.auth.AuthManager!*"
```

### APKTool Comparison (When JADX Isn't Enough)

```bash
# JADX fails for: patching, smali-level modification, resource recompilation
# Use apktool for those cases:
apktool d target.apk -o /tmp/apktool_out   # Disassemble (Smali + resources)
# Edit Smali files...
apktool b /tmp/apktool_out -o patched.apk  # Rebuild
# Sign patched APK:
keytool -genkey -v -keystore debug.keystore -alias debug -keyalg RSA -keysize 2048 -validity 365
jarsigner -keystore debug.keystore patched.apk debug
zipalign -v 4 patched.apk patched_aligned.apk
adb install patched_aligned.apk
```

## Troubleshooting

**"No input files" or decompile produces empty output:**
```bash
# Verify APK is valid
file target.apk  # Should say "Zip archive data"
unzip -l target.apk | grep ".dex"  # Must contain at least one .dex
```

**Out of memory during decompile:**
```bash
# Increase JVM heap size (JADX shell script sets -Xmx)
# Edit /opt/jadx/bin/jadx: change -Xmx1g to -Xmx4g
# Or set environment variable:
export JAVA_OPTS="-Xmx4g"
jadx -d /tmp/out target.apk
```

**Some classes show as "// couldn't decompile method":**
```bash
# Add --show-bad-code to see attempted decompilation
jadx -d /tmp/out --show-bad-code target.apk
# Fall back to baksmali for those specific classes
baksmali disassemble classes.dex -o /tmp/smali_out
cat /tmp/smali_out/com/example/ProblemClass.smali
```

**GUI crashes on large APKs:**
- Increase heap: add `-J-Xmx4g` to jadx-gui launch command
- Use CLI (`jadx`) instead for decompile, then browse output in VS Code or grep

**Deobfuscation produces wrong names:**
- `--deobf` is heuristic — short identifiers renamed but may be wrong
- Use jadx-gui interactive renaming for accurate renaming based on code context
- Check ProGuard mapping file if available from the developer (`mapping.txt`)
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
