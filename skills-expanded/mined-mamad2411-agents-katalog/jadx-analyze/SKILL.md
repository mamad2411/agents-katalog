---
name: jadx-analyze
description: Decompile and analyze Android APK/DEX/AAB files using JADX — extract Java source code, resources, and AndroidManifest.xml. Use when the user asks to analyze an APK, reverse engineer an Android app, inspect app permissions, find hardcoded secrets, or understand app behavior.
---

# jadx-analyze — Android APK Decompilation & Analysis

Use JADX to decompile Android APK/DEX/AAB files into readable Java source code and decoded resources.

## Pre-check

1. **Verify JADX is available**: `ls /home/user/q7h2q9/tools/jadx/bin/jadx`
2. **Verify Java runtime**: `java -version` (JADX requires Java 11+)
3. **Verify input file**: `file <target>` — must be `.apk`, `.dex`, `.jar`, `.aab`, `.xapk`, or `.zip`

If JADX is missing, inform the user that JADX needs to be installed at `/home/user/q7h2q9/tools/jadx/`.

## Usage

```bash
/home/user/q7h2q9/tools/jadx/bin/jadx -d <output_dir> <input_file>
```

Common options:
- `-d <dir>` — output directory (required)
- `-r, --no-res` — skip resource decoding (faster, source only)
- `-s, --no-src` — skip source decompilation (resources only)
- `-j <N>` — thread count (default: 8)
- `--show-bad-code` — include incorrectly decompiled code instead of skipping
- `--decompilation-mode simple` — use simplified output for obfuscated code
- `--single-class <full.class.Name>` — decompile only one class

## Usage Examples

Full APK decompilation:
```bash
/home/user/q7h2q9/tools/jadx/bin/jadx -d /tmp/apk-out /path/to/app.apk
```

Source code only (skip resources, faster):
```bash
/home/user/q7h2q9/tools/jadx/bin/jadx -d /tmp/apk-out --no-res /path/to/app.apk
```

Decompile a single class:
```bash
/home/user/q7h2q9/tools/jadx/bin/jadx --single-class com.example.MainActivity --single-class-output /tmp/Main.java /path/to/app.apk
```

Handle obfuscated code:
```bash
/home/user/q7h2q9/tools/jadx/bin/jadx -d /tmp/apk-out --show-bad-code --decompilation-mode simple /path/to/app.apk
```

## Output Structure

```
<output_dir>/
├── sources/                    # Decompiled Java source code
│   └── com/example/app/
│       ├── MainActivity.java
│       ├── BuildConfig.java
│       └── ...
├── resources/                  # Decoded resources
│   ├── AndroidManifest.xml     # App manifest (permissions, activities, services)
│   ├── res/
│   │   ├── layout/             # UI layouts
│   │   ├── values/             # strings.xml, styles.xml, etc.
│   │   └── ...
│   └── assets/                 # Raw assets
└── ...
```

## Workflow

1. Run `jadx -d <output_dir> <apk>` and wait for completion
2. Read `resources/AndroidManifest.xml` first — understand permissions, components, intent filters
3. List `sources/` to identify key packages and classes
4. Focus on:
   - **Entry points**: Activities, Services, BroadcastReceivers declared in manifest
   - **Network code**: Classes using `HttpURLConnection`, `OkHttp`, `Retrofit`, `Volley`
   - **Crypto/auth**: Classes using `javax.crypto`, `java.security`, token storage
   - **Native libs**: `System.loadLibrary()` calls, JNI methods
5. Use `grep -r` to search for specific patterns across decompiled sources

## Common Analysis Tasks

### Find hardcoded secrets
```bash
grep -rn "api_key\|apikey\|secret\|password\|token\|Bearer" <output_dir>/sources/
```

### Find network endpoints
```bash
grep -rn "https\?://\|\.api\.\|/api/" <output_dir>/sources/
```

### Check permissions
```bash
grep "uses-permission" <output_dir>/resources/AndroidManifest.xml
```

### Find native library usage
```bash
grep -rn "System.loadLibrary\|System.load" <output_dir>/sources/
```

## Error Handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `java: command not found` | No Java runtime | Install Java 11+: `apt install openjdk-11-jre` |
| JADX hangs on large APK | Memory/thread issue | Reduce threads: `-j 2`, or add `--no-res` |
| Garbled class names (`a.b.c`) | ProGuard obfuscation | Normal; use `--show-bad-code`, check for mapping file |
| `ERROR - Conversion failed` | Malformed DEX | Try `--decompilation-mode fallback` |

## Integration with ida-analyze

For APKs with native libraries (`.so` files inside the APK):

1. Decompile the APK with jadx to find JNI entry points
2. Extract the `.so` from the APK: `unzip app.apk lib/arm64-v8a/*.so -d /tmp/`
3. Run `ida-analyze` on the `.so` for native code analysis
4. Cross-reference Java `native` method declarations with IDA decompiled C code

## Notes

- JADX 1.5.1 supports APK, DEX, JAR, AAB, XAPK, SMALI, and class files
- Output is Java source (not Smali), making it easier to read
- For large APKs, `--no-res` significantly speeds up processing
- Obfuscated apps may need `--show-bad-code` to see all decompiled output
