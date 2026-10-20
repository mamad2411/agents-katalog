---
name: android-voice-assistant
description: "Replace Google Assistant on Android with a custom VoiceInteractionService — custom wake word detection (Porcupine, OpenWakeWord), ADB-based deployment without root, audio routing to self-hosted backends (Hermes, Home Assistant, custom API)."
version: 1.1.0
author: the operator / Agent Universe
license: proprietary
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [android, voice, assistant, wake-word, voiceinteractionservice, porcupine, hotword, soundtrigger, vosk, traefik, reverse-proxy]
    triggers: [android-voice, android-assistant, replace-google-assistant, custom-wake-word-android, hey-jippity, voiceinteractionservice, custom-apk-android, wakehermesclaw, adb-reverse-proxy, hermes-api-proxy, android-wake-word-build]
    related_skills: [voice-agent-architecture, hermes-agent]
---

# Android Voice Assistant — Custom Wake Word & Backend Integration

> Replace Google Assistant with a custom Android voice assistant app that uses a custom wake word (e.g. "Hey Jippity") and routes audio to your own backend (Hermes Agent, Home Assistant, or any API).

## Pre-Built Option: WakeHermesClaw (Fast Path)

**Before building from scratch, check if WakeHermesClaw meets your needs.** It is an open-source Android voice client that supports Hermes + OpenClaw backends, has wake word detection (Vosk), VoiceInteractionService integration, TTS, Wear OS, and the Mobile Bridge — all out of the box.

| Feature | WakeHermesClaw | Custom Build |
|---------|---------------|--------------|
| VoiceInteractionService | Built-in | Build it |
| Wake word | Vosk (grammar-based) | Porcupine/Vosk/any |
| Wake word config | Dual: OpenClaw + Hermes targets | Single custom |
| Hermes API | HTTP + Gateway | Build it |
| TTS | Edge, ElevenLabs, OpenAI, VOICEVOX | Build it |
| Setup time | 5 minutes (install + configure) | Days-weeks |
| License | MIT | Your choice |

**GitHub:** `github.com/yuga-hashimoto/openclaw-assistant`

**Quick install:**
```bash
# Download latest APK from releases page
curl -sL -o assistant.apk \\
  https://github.com/yuga-hashimoto/openclaw-assistant/releases/latest/download/OpenClawAssistant-v2.4.9.1.apk

adb install -r assistant.apk
```

> **Build reference:** See `references/2026-06-22-jippity-build-notes.md` for a complete walkthrough of building a custom APK, modifying defaults, deploying via ADB, configuring Traefik routing, and automating the setup via ADB taps — all without touching the phone screen.

The skill content below covers both the fast path (install existing app) and the build-from-scratch path.

## Architecture Overview

```
Phone ────────────────────────────────────────────┐
                                                   │
  "Hey Jippity" ──► Wake Word Engine (Vosk /      │
                    Porcupine / OpenWakeWord)      │
                         │                         │
                         ▼                         │
              VoiceInteractionService               │
              (system-level assistant)              │
              ┌─────────────────────────┐           │
              │ Dual-wake-word routing: │           │
              │ "hey claw" → OpenClaw  │           │
              │ "hey jippity" → Hermes │           │
              └─────────────────────────┘           │
                         │                         │
                    Capture Audio ──────────────────┤
                         │                         │
                         ▼                         │
               Your Backend (Hermes / API) ────────┤
              (STT → LLM → TTS)                    │
                         │                         │
                    Audio Response ◄────────────────┘
```

### Two Audio Layers on Android

| Layer | Description | Customizable? | Battery Impact |
|-------|-------------|---------------|----------------|
| **SoundTrigger HAL** (DSP hardware) | Low-power always-listening on dedicated DSP chip. Pre-loaded with "Ok Google"/"Hey Google" sound models. | ❌ No (vendor firmware) | ~0% (hardware) |
| **Software detection** (VoiceInteractionService + HotwordDetectionService) | Main CPU processes audio through a wake word engine like Porcupine. | ✅ Yes — any wake word | ~1-3% battery/day |

**Key insight:** You cannot change the DSP hotword without root + custom firmware, but you CAN:
1. Use software-based wake word detection for YOUR custom phrase ("Hey Jippity")
2. Optionally intercept the DSP's "Hey Google" trigger and route it through your service too
3. Replace Google Assistant as the system default entirely — no root needed

## The VoiceInteractionService (System Hook)

This is the Android API for replacing the system default assistant. Google Assistant is just one implementation of this service.

### Required Components

```
VoiceInteractionService (system-facing)
├── AndroidManifest.xml — declares the service with BIND_VOICE_INTERACTION
├── res/xml/voice_interaction.xml — metadata linking to hotword/visual services
├── Service implementation — extends VoiceInteractionService
├── HotwordDetectionService — runs wake word detection (isolated process)
└── Callback handler — receives detection events, captures audio, sends to backend
```

### Manifest Requirements

```xml
<service
    android:name=".CustomVoiceInteractionService"
    android:permission="android.permission.BIND_VOICE_INTERACTION"
    android:exported="true">
    <intent-filter>
        <action android:name="android.service.voice.VoiceInteractionService" />
    </intent-filter>
    <meta-data
        android:name="android.voice_interaction"
        android:resource="@xml/voice_interaction" />
</service>

<service
    android:name=".CustomHotwordDetectionService"
    android:permission="android.permission.BIND_HOTWORD_DETECTION_SERVICE"
    android:isolatedProcess="true"
    android:exported="true" />

<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.RECORD_BACKGROUND_AUDIO" />
<uses-permission android:name="android.permission.CAPTURE_AUDIO_HOTWORD" />
<uses-permission android:name="android.permission.MANAGE_HOTWORD_DETECTION" />
```

### Voice Interaction Metadata (`res/xml/voice_interaction.xml`)

```xml
<voice-interaction-service
    android:hotwordDetectionService=".CustomHotwordDetectionService"
    android:supportsAssist="true"
    android:supportsLocalInteraction="true" />
```

## Wake Word Detection Options

| Engine | Quality | Offline | Cost | Custom Words | Footprint |
|--------|---------|---------|------|--------------|-----------|
| **Porcupine (Picovoice)** | ⭐⭐⭐⭐⭐ 98% | ✅ Yes | Free tier | Unlimited via Console | ~2MB |
| **OpenWakeWord** | ⭐⭐⭐⭐ | ✅ Yes | Free (Apache 2.0) | Train your own | ~5MB |
| **Snowboy** (deprecated) | ⭐⭐⭐ | ✅ Yes | Free | Train your own | ~1MB |
| **Vosk** | ⭐⭐⭐⭐ | ✅ Yes | Free (Apache 2.0) | Grammar-based KWS + continuous dictation | ~40MB |
| **Porcupine is recommended** — highest accuracy, smallest footprint, easiest custom word training. Create an account at console.picovoice.ai, type your wake phrase, download the `.ppn` file.

**Vosk Grammar-Based KWS** — The WakeHermesClaw app uses Vosk in keyword-spotting mode. Vosk takes a word list as a JSON array and returns confidence scores for each detected phrase. This avoids needing a separate wake word model — any English phrase works out of the box:

```kotlin
// Vosk grammar-mode keyword spotting
val wakeWords = listOf("hey jippity", "hey claw", "hey hermes")
val wakeWordsJson = (wakeWords + "[unk]").joinToString(
    "\", \"", "[\"", "\"]"
)
val rec = Recognizer(model, 16000f, wakeWordsJson)
speechService = SpeechService(rec, 16000f)
speechService.startListening(callback)
```

Vosk returns results like `[hey jippity](0.92)` with confidence scores. The `[unk]` token absorbs non-matching speech so the engine does not lock up. Model size ~40MB (bundled in APK assets).

## Building from Source (Custom APK)

When you need to change defaults (wake words, package name, pre-configured URLs), build a custom APK from the WakeHermesClaw source.

### Prerequisites

```bash
# JDK 17+
choco install openjdk --version 17.0.2

export JAVA_HOME="/c/Program Files/OpenJDK/jdk-17.0.2"
export PATH="$JAVA_HOME/bin:$PATH"
```

### Modify Defaults

**Wake words** — change the defaults in `SettingsRepository.kt`:
```kotlin
// Before: const val DEFAULT_OPENCLAW_WAKE_WORD = "hey claw"
// After:
const val DEFAULT_OPENCLAW_WAKE_WORD = "hey jippity"
const val DEFAULT_HERMES_WAKE_WORD = "hey jippity"
```

**Package name** — the debug build adds `.debug` suffix. Remove it for clean package name:
```kotlin
// In build.gradle.kts, change or comment:
// applicationIdSuffix = ".debug"   // comment out for same package as release
```

### Handle Firebase Build Dependency

The build requires `google-services.json` and the Google Services plugin. For custom builds without Firebase:

```kotlin
// In app/build.gradle.kts — comment out the plugins:
// id("com.google.gms.google-services")
// id("com.google.firebase.crashlytics")
```

The Firebase implementation dependencies can stay — they resolve from Maven without the plugin. The `FIREBASE_ENABLED` BuildConfig field gates Firebase code at runtime, so the APK works without a real API key.

### Build

```bash
cd /path/to/openclaw-assistant
export FIREBASE_ENABLED=false
chmod +x gradlew
./gradlew assembleStandardDebug

# APK at: app/build/outputs/apk/standard/debug/openclaw-<git-tag>-debug.apk
```

### Known Build Issues

- **`processStandardDebugGoogleServices`** task fails if the Google Services plugin is present but no `google-services.json` exists. Fix: comment out the plugin.
- **Long first build** — Gradle downloads dependencies. 4-5 minutes on first build, ~1 minute subsequent.
- **Git describe** — `getTagName()` runs `git describe --tags` and appends `-dirty` if the tree has uncommitted changes. This is cosmetic.

## ADB Deployment (No Root)

### MSYS2 Path Translation (Windows Git-Bash Fix)

When running ADB commands from Git-Bash on Windows, paths starting with `/` (like `/sdcard/`) get translated to Windows paths. **Always run this at the top of every ADB session:**

```bash
export MSYS2_ARG_CONV_EXCL="*"
```

This disables all MSYS2 path translation. Without it:
- `adb shell cat /sdcard/file` → tries to read `C:/Program Files/Git/sdcard/file` on the phone
- `adb pull /sdcard/file .` → fails with "No such file or directory"

Alternative: use double-slash for key paths: `//sdcard/file`, but the env var approach is more thorough.

### Unlocking the Phone for UI Automation

```bash
# Wake screen
adb shell input keyevent KEYCODE_WAKEUP

# Dismiss keyguard (works on Android 16+)
adb shell wm dismiss-keyguard
```

`wm dismiss-keyguard` bypasses the lock screen without needing the PIN/pattern. Works on all Android versions that support the `wm` command. If the device has a lockscreen, the keyguard is dismissed temporarily for shell commands.

### Installing the APK

```bash
adb install -r custom-assistant.apk

# Grant permissions
adb shell dumpsys package com.example.assistant | grep CAPTURE_AUDIO_HOTWORD

# Set as default assistant (two methods — try both)
# Method 1: Secure settings
adb shell settings put secure voice_interaction_service \
    com.example.assistant/.CustomVoiceInteractionService
adb shell settings put secure assistant \
    com.example.assistant/.CustomVoiceInteractionService

# Method 2: Role manager (Android 10+)
adb shell cmd role set-bypassing-role-qualification true
adb shell cmd role add-role-holder android.app.role.ASSISTANT \
    com.example.assistant
```

**Note:** On some Android versions, the settings are cleared when the APK is reinstalled. You'll need to re-run the commands after each `adb install`.

### Verification

```bash
# Check if it is set
adb shell settings get secure voice_interaction_service
adb shell settings get secure assistant

# Watch logs for your service
adb logcat -s VIS SHotwordDetectionSrvc AlwaysOnHotword

# Verify the VoiceInteractionManager has picked up the change
adb shell dumpsys voiceinteraction | grep mComponent

# Restore Google Assistant if needed
adb shell settings put secure voice_interaction_service \
    com.google.android.googlequicksearchbox/com.google.android.voiceinteraction.GsaVoiceInteractionService
```

### Debug APK Inspection via `run-as`

If you built a debug APK (or a debuggable build), you can access the app's data directory:

```bash
# Drop into the app's shell context
adb shell run-as com.example.assistant

# List encrypted shared preference files
ls /data/data/com.example.assistant/shared_prefs/

# Read them (they're XML with encrypted blobs — for size/update checks)
wc -c /data/data/com.example.assistant/shared_prefs/openclaw.backends.secure.xml
```

This is useful for verifying that backend configs were written after deep-link import, without needing to navigate the app UI. Note that EncryptedSharedPreferences content is AES-256-GCM encrypted via Android Keystore — the raw XML only shows encrypted payloads, not plaintext config.

### Compose UI Automation for Enabling Hotword Detection

The WakeHermesClaw app uses Jetpack Compose, so some buttons may not respond to `input tap` coordinates reliably. Use repeated taps at slightly different y-coordinates within the target bounds:

```bash
# 1. Open the app to the Home screen
adb shell am start -n com.example.assistant/.MainActivity

# 2. Find the Wake Word toggle switch bounds via uiautomator
adb shell uiautomator dump /data/local/tmp/ui.xml
adb shell grep "Wake Word" /data/local/tmp/ui.xml

# Look for: bounds="[873,1393][982,1494]" (the switch/toggle component)
# The parent card shows: "open claw / hey jippity (OFF)"
# Tap the toggle to enable it — try multiple y positions for reliability
adb shell input tap 928 1444

# 3. Verify the status changed from (OFF) to (ON)
adb shell uiautomator dump /data/local/tmp/ui_after.xml
adb shell grep "Wake Word" /data/local/tmp/ui_after.xml
# Should show: "... hey jippity (ON)"

# 4. Verify the HotwordService is running via notification
adb shell dumpsys notification | grep -A5 -i "hotword_channel"
```

The toggle switch bounds pattern for Compose views:
- The clickable area of a Switch in Compose is typically wider than the visual indicator
- Look for `class="android.view.View"` with `checkable="true"` and `checked="false"` near the Wake Word label
- Center of switch: `x = (left + right) / 2`, `y = (top + bottom) / 2`


## External API Access (Beyond Local Network)

The ADB reverse proxy only works over USB. For remote access, expose the Hermes API server through an existing reverse proxy.

### Traefik Route (if Traefik is already running)

Add a path-prefixed route to an existing domain that already has DNS pointing to your reverse proxy:

```yaml
# In your Traefik dynamic config (e.g. docker-fallback.yml)
http:
  routers:
    hermes-api:
      rule: "Host(`api.your-domain.example`) && PathPrefix(`/hermes`)"
      entryPoints:
        - websecure
      middlewares:
        - strip-hermes-prefix
      service: hermes-api
      tls:
        certresolver: letsencrypt
  middlewares:
    strip-hermes-prefix:
      stripPrefix:
        prefixes:
          - /hermes
  services:
    hermes-api:
      loadBalancer:
        servers:
          - url: 'http://host.docker.internal:8642'
        passHostHeader: true
```

The phone then connects to `https://api.your-domain.example/hermes` (Traefik strips the prefix before forwarding).

**Requirements:**
- DNS record for your domain must already point to the Traefik host (public IP)
- Hermes API server must bind to 0.0.0.0 or be reachable from Docker (use `host.docker.internal`)
- CORS headers must allow the phone app's origin

### ADB Reverse Proxy (Local USB)

```bash
# Phone localhost:8642 → host localhost:8642
adb reverse tcp:8642 tcp:8642
```

**Advantages over binding to 0.0.0.0 on WiFi:**
- No network exposure (secure)
- Works over USB (no WiFi needed)
- No firewall/port conflicts
- Survives device reconnection (re-run after disconnect/reconnect)

### ngrok / Cloudflare Tunnel

For temporary public URLs without DNS changes:

```bash
ngrok http 8642
# → https://xxxx-xx-xx-xx-xx.ngrok-free.app
```

### Deep-Link Setup for Hermes Configuration

The WakeHermesClaw app accepts configuration via custom URI scheme. **Use explicit component targeting (`-n`) — implicit `am start -d` may fail on Android 14+ due to package visibility restrictions:**

```bash
# BEST: explicit component targeting (works on all Android versions)
adb shell "am start -n com.openclaw.assistant/.ui.setup.HermesImportActivity \
  -d 'agentvoice://setup?hu=https://api.your-domain.example/hermes&hn=Jippity&hm=default'"

# FALLS BACK: implicit intent with target package (less reliable)
adb shell am start \
    -a android.intent.action.VIEW \
    -d "agentvoice://setup?hu=http://127.0.0.1:8642&hn=Jippity"
```

**IMPORTANT caveats:**
- **Release APKs (proguard-stripped):** The `HermesImportActivity` class may be stripped by R8/proguard in release builds. Only debug builds reliably retain all activities. Check with `adb shell dumpsys package com.example.assistant | grep Activity` — if only `MainActivity` shows, the import activity is gone and you must configure via the app UI.
- **EncryptedSharedPreferences** means you cannot inject settings via config files or SQLite — the deep-link is the ONLY ADB-accessible path to set backend connection details.
- **First tap required:** The deep link pre-fills the import form but the user (or an ADB `input tap`) must press "Add and open" to save.


## Pitfalls

- **CAPTURE_AUDIO_HOTWORD permission** — This is a signature|privileged permission. On non-rooted phones, you may need to pre-grant it via ADB or push a permissions XML to `/system/etc/permissions/`. Without it, `createAlwaysOnHotwordDetector()` returns `STATE_HARDWARE_UNAVAILABLE`.
- **DSP keyphrase mismatch** — `createAlwaysOnHotwordDetector()` requires a keyphrase the DSP supports (like "X Google" for the sample). For custom phrases, use the software-only path (HotwordDetectionService + Porcupine).
- **Settings cleared on reinstall** — Android clears `voice_interaction_service` and `assistant` secure settings when the APK is reinstalled. Always re-run the ADB commands after `adb install`.
- **Settings revert on reboot** — On some OEM ROMs (Xiaomi, Samsung), assistant settings may revert after reboot. Test thoroughly.
- **Porcupine license** — Free tier allows unlimited custom wake words and commercial use. Only the enterprise tier with larger models needs a paid plan. Verify terms at picovoice.ai.
- **Battery impact** — Software wake word detection uses the main CPU. Porcupine is efficient (~200ms inference per frame) but expect 1-3% extra battery per day vs DSP-only.
- **Audio routing latency** — The path from phone mic → Porcupine detection → your backend → STT → LLM → TTS → phone speaker adds latency. Start-to-finish is typically 2-4 seconds for good STT/TTS providers.
- **Android version differences** — VoiceInteractionService API has changed across Android versions. API 21 (Android 5) introduced `createAlwaysOnHotwordDetector()`. API 34 (Android 14) added `VisualQueryDetector`. Test on your target API level.
- **Android 14+ permission changes** — On Android 14+, `RECORD_AUDIO` is required as a runtime permission before starting a foreground service with `foregroundServiceType="microphone"`. `CAPTURE_AUDIO_HOTWORD` is now role-managed and cannot be granted via `pm grant` — the assistant role grants it automatically when set via secure settings.
- **EncryptedSharedPreferences** — Apps using EncryptedSharedPreferences (like WakeHermesClaw) cannot have their config injected via `adb shell` commands. The deep-link URI scheme is the only ADB-accessible configuration path. First-time setup requires the UI (open app → Settings → configure).
- **Settings cleared on APK reinstall** — Android resets `voice_interaction_service` and `assistant` secure settings on reinstall. Always re-run the ADB commands after `adb install`.
- **OEM-specific quirks** — Samsung devices may show the VoiceInteractionManager component correctly but the hotword service may not start until the permissions notification is addressed. Grant all permissions in the app info screen.
- **Screen lock blocks automation** — If the phone screen is locked, ADB UI automation (`input tap`, `screencap`) may not work. Use `adb shell wm dismiss-keyguard` to dismiss the lock screen temporarily. On Samsung One UI, also press `KEYCODE_WAKEUP` first to wake the display. Note: `wm dismiss-keyguard` only dismisses the security overlay — it does not disable the lockscreen, and the keyguard re-engages on next sleep.
- **Release APK proguard stripping** — When using a pre-built release APK, R8/proguard may strip non-launcher activities. The `HermesImportActivity` and settings activities may not be resolvable by component name. Build from source (debug mode) to retain all activities, or use the release APK knowing deep-link config won't work. Verify with: `adb shell dumpsys package com.example.assistant | grep Activity`
- **Debug APK `run-as` access** — A debuggable APK (`debuggable=true`) lets you use `adb shell run-as com.example.assistant` to inspect the app's data directory. This is useful for verifying backend configs were saved and checking encrypted preference file sizes. The app's UID shell can list files under `/data/data/com.example.assistant/shared_prefs/` even though the file contents are AES-256-GCM encrypted via Android Keystore.
- **MSYS2 path translation on Windows** — Git-Bash translates paths starting with `/` (like `/sdcard/`) when passed to `adb shell`. Use these workarounds:
  - **Double-slash prefix:** `//sdcard/file` prevents MSYS translation
  - **Environment variable:** `export MSYS2_ARG_CONV_EXCL="*"` disables all path translation
  - **Direct path:** Use `/data/local/tmp/` paths with `adb shell cat` instead of `adb pull`
- **Deep link alternatives when implicit intents fail** — If `am start -d "agentvoice://..."` fails with "Activity not started," use explicit component launch:
  ```bash
  adb shell "am start -n com.package/.ui.setup.HermesImportActivity \
    -d 'agentvoice://setup?hu=http://host:8642&hn=Jippity'"
  ```
  Note: the `-p` flag (target package) doesn't work inside `adb shell` on some versions — `-n` with explicit component is more reliable.

## When to Use

| Use This Skill | Don't Use This Skill |
|---------------|---------------------|
| Building an Android phone-side voice assistant | Server-side voice pipeline (use voice-agent-architecture) |
| Replacing Google Assistant on a phone | Smart speaker / Google Home hardware hacking |
| Custom wake word for your backend | Alexa/Siri skill development |
| ADB-deployable no-root assistant | Building a custom AOSP ROM |

## Related Skills

- **voice-agent-architecture** — Server-side voice pipeline (VAD→ASR→LLM→TTS), Discord/Twilio transports, Docker deployment. Use alongside this skill when building the backend the Android app talks to.
- **hermes-agent** — Configure Hermes Agent's voice mode, STT/TTS providers, gateway API — the backend your Android assistant routes to.
