---
name: android-qa
description: Test an Android app on a real phone or an emulator using adb. Use when the user wants to install an APK they just compiled, walk through the app's screens, check the on-screen text, reproduce a bug, capture screenshots, read crash logs, or set up an Android testing environment from scratch. Covers both a physical device (USB or wireless debugging) and the emulator.
when_to_use: Trigger on requests like "test my Android app", "install this APK and check it", "why does this screen look wrong on a phone", "set up an Android emulator", "connect my phone for testing", "read the logs from my app", or any request to drive an Android device from the command line.
---

# Android QA

Drive an Android device (emulator or real phone) through `adb` to test the user's app.

**Full reference: [`AGENTS.md`](../../AGENTS.md) in this repository.** Read it before improvising
commands — it documents six verified traps, and one of them blinds you with no error output.

## 1. Find out what you're working with

```powershell
adb devices
```

If `adb` isn't on the PATH, look in `$env:ANDROID_HOME`, `$env:LOCALAPPDATA\Android\Sdk` and
`C:\Android\Sdk` before concluding it's missing. Android Studio installs it — many users
already have it.

| id looks like | mode |
|---|---|
| `emulator-5554` | emulator |
| `ZY22JMJD5R` | real device over USB |
| `192.168.1.50:5555` | real device over wireless |
| *(empty)* | nothing connected — see section 4 of `AGENTS.md` |

## 2. Know what your mode cannot do

Everything works in both modes **except these**, which are emulator-only:

- **Fake GPS** (`adb emu geo fix`) — on a physical phone this command does not exist
- Changing RAM
- Wiping to a clean state

If the user asks for one of these on a real device, **say so instead of trying it.**

## 3. The working loop

```powershell
adb install -r app.apk
adb shell pm list packages | Select-String their-app     # confirm the real package name
adb shell monkey -p PACKAGE -c android.intent.category.LAUNCHER 1
adb shell uiautomator dump /sdcard/ui.xml                # what's on screen
adb shell input tap 540 1200
adb logcat -d *:E
```

From the `uiautomator` dump, take each node's `text` and `bounds`. The centre of `bounds` is
where you tap. **Never eyeball pixels on a screenshot** — use the dump's coordinates.

## 4. Two traps that will bite you

**Screenshots corrupt silently in PowerShell.** `adb exec-out screencap -p > shot.png` produces
a broken PNG and reports no error — `>` is *text* redirection and destroys the binary. Always:

```powershell
adb shell screencap -p /sdcard/s.png
adb pull /sdcard/s.png shot.png
```

Verify the header is `89 50 4E 47`. If it's `EF BB BF`, the file is corrupt and you are blind.

**Fake GPS looks broken when it works.** `adb emu geo fix` returns `OK` but `dumpsys location`
keeps showing `last location=null` until some app requests location. That is not a failure —
don't go debugging it. Open an app that uses location, repeat the fix, then check again.

The other four traps are in `AGENTS.md` section 6.

## 5. Before reporting success

Show the user: a screenshot with a verified PNG header, an activity name that changed after a
tap, the number of UI elements read, and which mode you're in. If you couldn't verify
something, say so instead of assuming.
