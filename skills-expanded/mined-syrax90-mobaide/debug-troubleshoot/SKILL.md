---
name: debug-troubleshoot
description: How to debug and troubleshoot the Claude Mobile project (Android Kotlin client + Python FastAPI server). Use this skill whenever the user asks to debug, troubleshoot, diagnose, investigate, or fix any failure in this repo — server crashes, Android app bugs, connectivity issues, WebSocket disconnects, PTY problems, build/run errors — even if they don't say the word "debug".
---

# Debugging & Troubleshooting — Claude Mobile

This project has two sides: a **Python FastAPI server** (`mobaide_agent/`) and an **Android Kotlin client**. Most issues live at one of those ends or in the transport between them (WebSocket / cross-platform PTY). Diagnose accordingly.

## 1. Run the server

To reproduce server-side issues or watch live logs, run it directly so stdout/stderr land in your terminal:

```bash
cd D:/ML/Projects/claude_mobile/mobaide_agent
conda activate claude-mobile
python -m mobaide
```

The `claude-mobile` conda env has the right Python and dependencies — don't try to invoke the module from the system Python.

## 2. Android side — use the Android SDK CLI tools

`platform-tools` and `cmdline-tools` are on the system `Path`. Prefer these over scripts or workarounds — they are faster, more reliable, and what the user expects you to use.

| Tool | Use it for |
|---|---|
| `adb devices` | Check which devices/emulators are connected before doing anything else |
| `adb logcat` (filter by tag/package) | **Primary** source of truth for Android-side failures — runtime logs, stack traces, crashes |
| `adb install` / `adb uninstall` | APK lifecycle |
| `adb push` / `adb pull` / `adb shell` | Move files, run device commands |
| `sdkmanager` | View/install/update SDK packages |
| `apkanalyzer` | Inspect APK contents (size, manifest, dex) |
| `avdmanager` | Manage Android Virtual Devices |

Before writing a script to manipulate or inspect a device, check whether a single `adb` command does the job. It almost always does.

## 3. Triage order

Work in this order — it minimizes wasted effort:

1. **Reproduce** the failure (run server as in §1; use the app or `adb` as in §2).
2. **Collect logs from both sides simultaneously** — server stdout *and* `adb logcat`. Many bugs only make sense when you can correlate them.
3. **Isolate the layer**: client UI → client networking → WebSocket transport → server handler → PTY/subprocess. Cross-platform PTY and the WebSocket bridge are the most common failure points; check them early when symptoms involve hangs, disconnects, or garbled output.
4. **Form a hypothesis**, then make the smallest change that tests it. Don't rewrite surrounding code while debugging.

## 4. When stuck

- Re-read the actual error/stack trace before guessing.
- Confirm assumptions about which process and which env the failing code is running in (server vs. device, conda env vs. system Python).
- If a tool seems "broken", verify the command itself with `adb devices` / `python -m mobaide --help` etc. before assuming a deeper bug.
