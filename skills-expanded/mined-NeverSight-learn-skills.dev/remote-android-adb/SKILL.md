---
name: remote-android-adb
description: Run Android ADB commands against a phone connected to a remote physical machine over Tailscale + SSH. Use when OpenClaw runs on a VPS but ADB runs on a home/office Linux box with USB-attached Android devices.
---

# Remote Android ADB (Tailscale + SSH relay)

Use this skill when ADB is not local to the OpenClaw host.

## What this assumes

- OpenClaw runs on a VPS (or other remote host)
- A physical relay machine (e.g., Arch laptop, RPi, mini PC) has:
  - Android phone attached via USB
  - `adb` installed and working locally
  - Tailscale installed and connected
  - SSH server reachable over Tailscale

## Configuration

Create a JSON config (recommended path):

`~/.openclaw/remote-android-adb.json`

Use the schema in `references/config.example.json`.

Minimum required fields:
- `ssh_host`
- `ssh_user`
- `ssh_port`
- `ssh_identity_file`

Optional but recommended:
- `device_serial`
- `adb_path`
- `unlock` (macro + PIN + gesture settings for lockscreen automation)

## Unlock macro (config-driven)

Use `scripts/unlock_device.sh` to unlock without hardcoding credentials in scripts.

```bash
./scripts/unlock_device.sh --config ~/.openclaw/remote-android-adb.json
```

The macro is selected by `unlock.macro` in config. See:
- `references/config.example.json`
- `references/unlock-macros.md`

## Core command wrapper

Use `scripts/remote_adb.sh` to run all remote ADB commands.

```bash
# Check relay + adb devices
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json devices

# Run any adb subcommand remotely
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json shell getprop ro.product.model
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json shell dumpsys battery
```

If `device_serial` is set in config, the wrapper automatically adds `-s <serial>`.

## Lock-state helper

Use `scripts/is_locked.sh` to check lock state without screenshots.

```bash
# Minimal output: LOCKED or UNLOCKED
./scripts/is_locked.sh --config ~/.openclaw/remote-android-adb.json

# Include parsed diagnostics (showing/mIsShowing/interactive/screen)
./scripts/is_locked.sh --config ~/.openclaw/remote-android-adb.json --verbose
```

Detection rule used by helper:
- `showing=true` **or** `mIsShowing=true` => `LOCKED`
- otherwise => `UNLOCKED`

Quick toggle pattern:
```bash
state="$(./scripts/is_locked.sh --config ~/.openclaw/remote-android-adb.json)"
if [[ "$state" == "LOCKED" ]]; then
  ./scripts/unlock_device.sh --config ~/.openclaw/remote-android-adb.json
else
  ./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json shell input keyevent 26
fi
```

## Common workflows

### 1) Health check

```bash
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json devices
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json shell getprop ro.build.version.release
```

### 2) Launch app

```bash
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json \
  shell monkey -p com.android.settings -c android.intent.category.LAUNCHER 1
```

### 3) UI dump + screenshot

Use a dedicated screenshots folder in the workspace to avoid clutter.

```bash
mkdir -p ./artifacts/screenshots

./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json \
  shell uiautomator dump /sdcard/view.xml

./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json \
  shell screencap -p /sdcard/screen.png

# pull file from phone -> relay -> VPS workspace artifacts folder
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json \
  pull /sdcard/screen.png ./artifacts/screenshots/screen.png
```

### 4) Input automation

```bash
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json shell input tap 500 1200
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json shell input keyevent 3
./scripts/remote_adb.sh --config ~/.openclaw/remote-android-adb.json shell input text "hello%sworld"
```

## Execution strategy (UI automation)

- **Prefer XML/UIAutomator first** for deterministic UI actions (button taps, dialog confirmation, extracting control bounds/text).
- **Fallback to visual analysis (screenshots + vision)** when XML is unavailable, unstable, or semantically insufficient (for example, WebView/Chrome content not represented clearly in accessibility tree).
- For critical actions, use a **hybrid verify pattern**:
  1) attempt action using XML-derived coordinates/selectors,
  2) validate result via XML when possible,
  3) validate via screenshot/vision when XML cannot prove final state.
- If XML and visual signals conflict, prioritize whichever is more directly tied to the target state, and run an additional confirmation step before proceeding.

## Guardrails

- Prefer USB debugging on relay machine for stability.
- Keep SSH/Tailscale private; do not expose ADB to public internet.
- Use least privilege SSH keys.
- Pin device serial when multiple phones are attached.
- Re-run `devices` after reconnect events.
- Unless you are certain the phone is already unlocked (for example, you just unlocked it or successfully executed an unlock-required command immediately before), **check lock state first** with `scripts/is_locked.sh` and run `scripts/unlock_device.sh` if needed before continuing with the rest of the command sequence.

## References

- `references/config.example.json` - config schema example
- `references/setup-checklist.md` - end-to-end setup checklist
