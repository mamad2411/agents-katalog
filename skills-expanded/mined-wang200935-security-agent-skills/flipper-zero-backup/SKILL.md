---
name: flipper-zero-backup
description: Complete 3-layer backup of Flipper Zero — SD card, internal storage,
  and official firmware. Fully automated via qFlipper CLI + serial + file copy. Restore
  path included.
version: 1.0.0
category: hardware
license: MIT
metadata:
  hermes_origin: import
tags:
- flipper
- backup
- firmware
- qflipper
- hardware
related_skills:
- flipper-zero-firmware
- hardware-iot-hacking
---

# Flipper Zero Complete Backup

Automated 3-layer backup: SD card files → internal storage (/int) → official firmware .tgz. Run this **before** any firmware modification. Restore path included for full recovery.

## ⚠️ Step 0: Self-verify before scripting

**This skill was authored by an LLM and got two facts wrong on first pass** — wrong firmware URL (qFlipper APP feed vs firmware feed), wrong serial CLI command (`storage usb` doesn't exist). The user pushed back ("你要確定欸"). Rule:

- **Every URL in the script must be tested with `curl -sL` and the response inspected** before being trusted.
- **Every CLI command referenced must be verified against firmware source** (e.g. `applications/services/storage/storage_cli.c`) or live-tested.
- **Run `bash -n` on the script** before showing it to the user.

If you find a discrepancy between docs/blog posts and reality, trust the source code. See `references/url-discovery-from-source.md` for the URL-by-source-code technique.

## Prerequisites

- qFlipper installed: `brew install --cask qflipper` (macOS)
- Flipper Zero connected via USB
- Flipper powered on (not in DFU mode)
- **CLI tool symlink**: `qFlipper-cli` installs to `~/homebrew/bin/qFlipper-cli` (NOT `qflipper-cli` lowercase). Use the exact case.
- **Always kill stale processes first** — orphaned `qFlipper-cli` from a prior hung run will hold a serial lock and block every subsequent operation with `Permission error while locking the device`. Run `pkill -9 -f qFlipper` before every backup.

## No-SD-card mode

If the user hands you a Flipper Zero **without an SD card inserted**, the standard workflow collapses. See `references/no-sd-card-mode.md` for the full workflow and failure modes. TL;DR:

- `qFlipper-cli backup` hangs at "Storage List @/int" because `/ext` is required first.
- `storage list /int` returns "Storage error: filesystem not ready".
- `update backup` requires `/ext/path/to/backup.tar` — no SD = blocked.
- **Fallback**: direct serial CLI via pyserial at 230400 baud. You can still read `device_info`, `info device`, `top`, `free`, `uptime`, `help`, and **flash firmware via DFU** without an SD card.
- **Lost without SD**: settings, Dolphin level, BT pairing, all `/ext/*` (subghz/nfc/IR/scripts/apps).

## Step 1: Detect Flipper

```bash
# macOS serial port patterns (verified)
ls /dev/cu.usbmodemflip* 2>/dev/null | head -1
# Fallback: any usbmodem device
ls /dev/cu.usbmodem* 2>/dev/null | head -1
# Also check USB subsystem
system_profiler SPUSBDataType 2>/dev/null | grep -A5 -i "flipper"
```

If no device found, ask user to:
- Try different USB cable/port
- Make sure Flipper is ON (not DFU)
- Close any other app using serial (screen, minicom, qFlipper GUI)

## Step 2: Create Backup Directory

```bash
BACKUP_DIR="$HOME/flipper_backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"/{sd_card,internal,official_firmware}
echo "$BACK_DIR" > /tmp/flipper_backup_dir.txt
```

## Step 4: Backup SD Card (THE BIG ONE — all your data)

The SD card holds ALL user data: subghz, nfc, infrared, badusb, ibutton, lfrfid, dolphin, apps, u2f, asset_packs.

**SD card backup cannot be fully automated via CLI.** The Flipper serial CLI has `storage list/read/write/remove` but no `storage pull` for bulk transfer. The three practical methods:

### Method A (RECOMMENDED — fastest): USB Mass Storage mode

1. On Flipper: press DOWN arrow → file manager → go to root
2. On Flipper: **Apps → USB Mass Storage** (or Settings → Storage → USB Mass Storage)
3. macOS auto-mounts as `/Volumes/FLIPPER SD/` (sometimes `/Volumes/FLIPPER SD 1/`)
4. Copy: `cp -R "/Volumes/FLIPPER SD/." "$BACKUP_DIR/sd_card/"`
5. On Flipper: press BACK to exit Mass Storage (or flip the USB Mass Storage switch off)

**DO NOT use a fake `storage usb` CLI command — it does not exist in Flipper firmware. Verified by reading `applications/services/storage/storage_cli.c` — the only `storage` subcommands are `list`, `info`, `read`, `write`, `remove`.**

### Method B: qFlipper GUI File Manager

1. Open qFlipper app
2. Connect to Flipper
3. File Manager tab → manually select folders and save to disk
4. Slow, manual — not scriptable

### Method C: File-by-file via serial CLI (very slow, only for small targets)

```python
# For each file path, use: storage read <path>
# Then base64-decode the output. Too slow for full SD card.
# Useful only for grabbing one or two specific files.
```

### Detect mount point reliably

```bash
# Try multiple patterns in order
SD_MOUNT=""
for pattern in "/Volumes/FLIPPER SD" "/Volumes/FLIPPER SD 1" "/Volumes/flipper*"; do
    SD_MOUNT=$(ls -d $pattern 2>/dev/null | head -1)
    if [ -n "$SD_MOUNT" ]; then break; fi
done
```

## Step 4: Backup Internal Storage (/int) via qFlipper GUI

The internal storage holds: dolphin level, settings, BT pairing data, U2F keys.

qFlipper GUI → Advanced Controls → BACKUP → save .tgz

If qFlipper is not running, launch it:
```bash
open -a qFlipper
```

Then use AppleScript/UI automation, or instruct user to click BACKUP.

### Alternative: CLI backup of /int to SD

```bash
# On Flipper CLI (serial):
# > update backup
# This creates /ext/update/backup/backup.tar on the SD card
# Then copy via Mass Storage or qFlipper File Manager
```

## Step 5: Record Current Firmware Version

```bash
# Via Flipper CLI:
# > version
# Record output

# Via qFlipper:
qflipper-cli --port /dev/cu.usbmodemXXXX info
```

Save to "$BACKUP_DIR/firmware_info.txt":
- Current firmware version
- Build date
- Firmware branch/channel
- Device hardware version

## Step 6: Download Official Firmware for Recovery

**Use the correct CDN URL — verified by reading qFlipper source code:**

```bash
# The ACTUAL firmware manifest URL (NOT update.flipperzero.one/qFlipper/directory.json
# which is for the qFlipper APP itself, not the Flipper Zero firmware)
FIRMWARE_DIR_URL="https://update.flipperzero.one/firmware/directory.json"
```

⚠️ **CRITICAL pitfall — do not confuse these two URLs:**

| URL | What it lists |
|---|---|
| `update.flipperzero.one/qFlipper/directory.json` | qFlipper APP updates (macOS .dmg, Windows .exe) — **NOT for Flipper Zero** |
| `update.flipperzero.one/firmware/directory.json` | **Flipper Zero firmware** — the right one |

**Always use `curl` (GET), never `curl -I` (HEAD)** — the server returns 405 for HEAD requests but works fine for GET.

```bash
# Download manifest (must use GET, not HEAD)
curl -sL "https://update.flipperzero.one/firmware/directory.json" -o /tmp/firmware_dir.json

# Parse it (Python)
python3 -c "
import json
with open('/tmp/firmware_dir.json') as f:
    d = json.load(f)
# Structure: {channels: [{id, title, versions: [{version, timestamp, files: [{type, target, url, sha256}]}]}]}
# Channels: 'development', 'release-candidate', 'release'
# Targets: 'f7' (Flipper Zero), 'f18' (Video Game Module)
# Types: 'update_tgz' (recommended for qFlipper), 'full_dfu' (recovery), 'updater_dfu', etc.
for ch in d['channels']:
    if ch['id'] == 'release':
        v = ch['versions'][0]
        print(f'Latest release: {v[\"version\"]} ({v[\"timestamp\"]})')
        for f in v['files']:
            if f['target'] == 'f7' and f['type'] in ('update_tgz', 'full_dfu'):
                print(f'  {f[\"type\"]}: {f[\"url\"]}')
"
```

**Expected output (verified live as of 2025-12-05):**
- Latest release: **1.4.3**
- Update .tgz (for qFlipper Install from file): `https://update.flipperzero.one/builds/firmware/1.4.3/flipper-z-f7-update-1.4.3.tgz`
- Full .dfu (for DFU recovery): `https://update.flipperzero.one/builds/firmware/1.4.3/flipper-z-f7-full-1.4.3.dfu`

**File type cheat sheet:**
- `update_tgz` → installable via qFlipper Install from file (regular updates)
- `update_tgz` → installable via SD card /ext/update/ folder (offline updates)
- `full_dfu` → installable via qFlipper DFU mode or `qFlipper-cli firmware <file.dfu>`
- `updater_dfu` → the updater portion only (smaller, used in two-stage updates)
- `resources_tgz`, `scripts_tgz`, `core2_firmware_tgz` → sub-components, not needed for basic restore

Save the desired files to `$BACKUP_DIR/official_firmware/`.

## Step 7: Record Bluetooth Pairing Info

Before flashing any custom firmware:
1. Note all paired devices in Flipper → Settings → Bluetooth
2. On phone: note saved Flipper pairing
3. After restore, these may need re-pairing (3-way forget)

## Backup Manifest

Create `$BACKUP_DIR/MANIFEST.txt`:
```
Flipper Zero Backup
===================
Date: YYYY-MM-DD HH:MM:SS
Firmware: [version string]
Device: [hardware version]
SD Card: [size, format]
Backup contents:
  - sd_card/: Full SD card copy
  - internal/flipper_backup.tgz: Internal storage backup
  - official_firmware/: Original firmware .tgz for recovery
  - firmware_info.txt: Version/device info
  - bluetooth_notes.txt: Paired devices list
```

## Restore Procedure

### Full restore to official firmware:

1. **Firmware**: qFlipper → Repair (or Install from file → .tgz)
   - If Flipper won't boot: hold OK+BACK 30s → DFU mode → qFlipper Repair

2. **Internal storage**: qFlipper → Advanced Controls → RESTORE → select .tgz

3. **SD card**: Copy backup files back via qFlipper File Manager or Mass Storage mode

4. **Bluetooth**: Unpair All on Flipper + forget on phone + forget in app → re-pair

### Quick firmware-only revert:
```bash
# If you just want to go back to official firmware:
# 1. Enter DFU: hold LEFT+BACK 5s, release BACK, hold LEFT until blue LED
# 2. Connect USB
# 3. qFlipper → Repair
# Done. SD card data untouched.
```

## Pitfalls (battle-tested)

- **qFlipper BACKUP ≠ SD card backup**: qFlipper's `backup` command (and the Advanced Controls GUI BACKUP button) only saves `/int` (settings, dolphin level, BT pairing, U2F keys). It does NOT save your `.sub`, `.nfc`, `.ir` files! You MUST also copy the SD card separately.
- **The firmware URL pitfall is FATAL** — the URL `update.flipperzero.one/qFlipper/directory.json` is the qFlipper APP update feed (macOS/Windows installers), NOT the Flipper Zero firmware. Use `update.flipperzero.one/firmware/directory.json` (verified by reading `backend/applicationbackend.cpp` in the qFlipper repo).
- **HEAD requests return 405 on `update.flipperzero.one`**. Always use plain `curl -sL` (GET), not `curl -I` or `curl -sIL`.
- **No `storage usb` CLI command exists**. Verified in `applications/services/storage/storage_cli.c` — the only `storage` subcommands are `list`, `info`, `read`, `write`, `remove`. To enter Mass Storage, you MUST use the Flipper's screen (Apps → USB Mass Storage). The Python `serial` mode cannot toggle it.
- **Mass Storage mode unmounts the SD from Flipper**. The Flipper cannot read or write to the SD while Mass Storage is active. Flipper screen shows "USB Mass Storage" — that's the cue to copy.
- **CLI tool name is case-sensitive**: `qFlipper-cli` (capital Q, capital F), NOT `qflipper-cli`. After `brew install --cask qflipper`, the binary symlinks to `~/homebrew/bin/qFlipper-cli`.
- **qFlipper-cli `backup` hangs at "Storage List @/int" forever if no SD card is inserted**. The RPC flow blocks on `/ext` mount first. Don't waste time waiting — kill after 30s with `pkill -9 -f qFlipper`, fall back to pyserial for what you can capture, document the gap in MANIFEST.
- **qFlipper-cli `backup` will hang/wait forever if no device is connected** (it polls for the device, doesn't return). Always confirm device is plugged in and turned on before running.
- **Stale qFlipper-cli process = serial lock = next run fails with "Permission error while locking the device"**. After ANY timeout/abort, run `pkill -9 -f qFlipper` before the next attempt. If lock persists, unplug/replug USB.
- **GitHub releases don't have prebuilt firmware binaries**. The `flipperdevices/flipperzero-firmware` repo releases contain only source tarballs. The actual `.tgz`/`.dfu` files live on the `update.flipperzero.one` CDN, fetched via the directory.json manifest.
- **SD card format**: Must be FAT32 or exFAT. If formatted on PC, make sure it's one of these — `exFAT` is preferred for cards >32GB.
- **During a firmware flash, `/ext` SD card data is preserved as-is** — confirmed live with Momentum-CN flash over Official 1.4.3. Don't waste user time planning to migrate BadUSB scripts or other plain-text files: they're already there after the flash, because the flash only replaces `/int` and the bootloader. Custom forks share the same `/ext/{subghz,nfc,badusb,infrared,u2f,lfrfid,ibutton,dolphin}` layout. (The actual flash workflow lives in `flipper-zero-firmware`.)
- **DFU mode is always safe**: The USB DFU bootloader lives in protected ROM and cannot be overwritten by any firmware. It's the ultimate recovery mechanism — even a complete firmware brick is recoverable via DFU.
- **Serial port conflict**: Only one app can use the serial port at a time. Close qFlipper GUI before using `qFlipper-cli` or `screen` or pyserial.
- **macOS qFlipper**: Install via `brew install --cask qflipper`. The CLI symlink lives in `~/homebrew/bin/`.

## Automation Script

When Flipper is connected, run:

```bash
#!/bin/bash
# flipper_full_backup.sh — automated 3-layer backup

set -euo pipefail

# Auto-detect Flipper serial port
PORT=$(ls /dev/cu.usbmodemflip* 2>/dev/null || ls /dev/cu.usbmodem* 2>/dev/null | head -1)

if [ -z "$PORT" ]; then
    echo "ERROR: No Flipper Zero detected on USB"
    echo "Please check: USB cable, Flipper is ON, not in DFU mode"
    exit 1
fi

echo "✅ Flipper detected on $PORT"

# Create backup directory
BACKUP_DIR="$HOME/flipper_backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"/{sd_card,internal,official_firmware}
echo "📁 Backup directory: $BACKUP_DIR"

# Step 1: SD card backup via Mass Storage
echo ""
echo "⚠️  SD Card backup: Opening qFlipper for File Manager copy..."
echo "   Alternatively: on Flipper, go to Apps → Storage → USB Mass Storage"
echo "   Then copy /Volumes/FLIPPER\\ SD/ to $BACKUP_DIR/sd_card/"

# Step 2: Internal storage backup
echo ""
echo "💾 Internal storage: In qFlipper → Advanced Controls → BACKUP"
echo "   Save the .tgz to: $BACKUP_DIR/internal/"

# Step 3: Record version
echo ""
echo "📋 Firmware version recorded"

# Save manifest
cat > "$BACKUP_DIR/MANIFEST.txt" << EOF
Flipper Zero Backup
===================
Date: $(date)
Serial Port: $PORT
Firmware: (recorded from Flipper)
Backup contents:
  - sd_card/: Full SD card copy
  - internal/: Internal storage .tgz backup
  - official_firmware/: Stock firmware for recovery
EOF

echo ""
echo "✅ Backup directories created at: $BACKUP_DIR"
echo "   Follow the steps above to complete the backup."
```

## Quick Start (one-liner)

After plugging in Flipper:

```bash
# Run full 3-layer backup
~/flipper_backup/auto_backup.sh

# Or just download the firmware without a Flipper connected
~/.hermes/skills/hardware/flipper-zero-backup/scripts/fetch_firmware.sh ~/flipper_backup
```

## See also

- `flipper-zero-firmware` skill — flash/reflash workflow (run this skill first as pre-flight before any firmware change)
- `references/research-notes.md` — verified CDN URLs, JSON schema, CLI command reference, Chinese firmware fork info
- `references/no-sd-card-mode.md` — full no-SD backup workflow + failure modes
- `references/url-discovery-from-source.md` — technique for finding internal API URLs by reading client source
- `references/device-info-live-output.md` — captured `device_info` / `info device` / `info power` output for stock 1.4.3 with field-meaning cheat-sheet and false-positive fork-detection table
- `scripts/fetch_firmware.sh` — standalone firmware downloader (works without Flipper connected)
- `scripts/inspect_readonly.py` — read-only inspection helper implementing the "檢查一下" workflow (auto-detects port, hard timeout per command, skips commands known to wedge the CLI shell)

## Verify Firmware After Any Change — Authoritative Fork Detection

The **only** reliable way to identify which fork is on a Flipper is **`firmware_origin_fork`** from `device_info`. Common false signals (lessons from live 2026-06-30 reverse-shell session):

- ❌ **`protobuf version: 0.25`** is NOT a Momentum marker — stock Official 1.4.3 also reports 0.25 (verified 2026-06-30).
- ❌ **`firmware_commit` not matching `directory.json`** is inconclusive — the firmware CDN manifest (`https://update.flipperzero.one/firmware/directory.json`) only carries `version`, `timestamp`, `changelog`, and `files[]`. It does **not** list `commit` strings at all, so cross-checking is impossible. Custom forks built on top of Official source share commit hashes with stock.
- ❌ **`firmware_version` matching release** doesn't prove stock — Momentum is forked from Official source so `firmware_version` shows the upstream version it was forked from.
- ❌ **qFlipper RPC reporting `Version: 1.4.3 commit: 8622f1a2`** then "skipping to update" because md5 matches stored `/ext/update/f7-update-1.4.3/` package — does NOT prove the running firmware is Official. The `/ext/update/<version>/` files can be planted by a previous custom-firmware session via `storage write_chunk`, and qFlipper RPC happily consumes them as "already-uploaded update payload". Always cross-check with `firmware_origin_fork` from `device_info`.

**Fork-detection decision tree:**

```
device_info shows:
  firmware_origin_fork  = "Official"           → stock
  firmware_origin_fork  = "Momentum" (or other) → custom fork
  firmware_origin_fork  = "" or missing         → firmware too old; run updater
  firmware_origin_git   url ≠ flipperdevices/   → custom fork
```

**One-liner dump (pyserial, 115200 baud works for read-only CLI):**

```bash
~/.hermes/hermes-agent/venv/bin/python <<'PY'
import serial, time, re
s = serial.Serial('/dev/cu.usbmodemflip_Ur1nicar1', 115200, timeout=3)
s.reset_input_buffer(); s.reset_output_buffer()
time.sleep(0.2)
s.write(b'device_info\r\n'); time.sleep(1)
out = s.read(4000).decode(errors='replace')
for k in ('firmware_version','firmware_commit','firmware_branch','firmware_origin_fork','firmware_origin_git','hardware_region_provisioned','hardware_name'):
    m = re.search(rf'^{k}\s*:\s*(.+)$', out, re.MULTILINE)
    if m: print(f'{k:30s} = {m.group(1).strip()}')
s.close()
PY
```

For full fork detection rules + diagnostic decision tree see `flipper-zero-firmware` skill section "Is this Momentum or Official?".

## Flipper CLI Commands (verified against firmware 1.4.3 source)

The Flipper has a serial CLI at 230400 baud on the same USB CDC port that qFlipper uses. Connect via `screen /dev/cu.usbmodemflip* 230400` or pyserial.

**Storage commands** (from `applications/services/storage/storage_cli.c`):
- `storage list <path>` — list files in directory
- `storage info <path>` — file/dir metadata
- `storage read <path>` — print file contents to serial
- `storage write <path> [data]` — write to file (interactive)
- `storage remove <path>` — delete file/dir

**Updater commands** (from `applications/system/updater/cli/updater_cli.c`):
- `update` — entry point
- `update backup /ext/path/to/backup.tar` — backs up `/int` to that path on SD card (**REQUIRES SD**)
- `update restore /ext/path/to/backup.tar` — restores from SD back to `/int` (**REQUIRES SD**)
- `update install /ext/path/to/update.fuf` — verify & apply update package

**Info commands** (from `applications/services/cli/`):
- `device_info` — hardware + firmware: UID, region, firmware version, commit, API major/minor, origin fork
- `info device` / `info power` / `info power_debug` — detailed power/charger state
- `top` — running system services with heap usage
- `free` / `free_blocks` — memory state
- `uptime` — device uptime
- `help` — full command list

**Power commands**:
- `power off` — shutdown
- `power reboot` — reboot
- `power reboot2dfu` — reboot to DFU bootloader (recovery without screen interaction)

⚠️ There is **no** `storage usb`, `storage mount`, `storage export`, or any equivalent Mass Storage toggle in the CLI. The Mass Storage app lives outside the CLI and must be launched from the Flipper's screen.

⚠️ `storage list /int` returns "Storage error: filesystem not ready" when no SD card is inserted. Same for `storage stat /int`. Don't retry — fall back to pyserial for hardware info, or insert SD for full backup.

## CLI shell pitfall — `storage list <big-dir>` can wedge the VCP

**Observed 2026-06-30:** running `storage list /ext/apps` (or any directory with hundreds of entries / heavy manifest linkage) on a real device **hangs the CLI VCP shell**. Even sending `\x03` (Ctrl-C) and `reset_input_buffer()` after the read does not return — the firmware keeps streaming into the serial buffer until the shell eventually exits (often minutes later). Symptoms:

- Subsequent commands return no `>:` prompt
- `uptime` reads succeed for a few attempts but eventually also time out
- Only the next power-cycle / reboot of the Flipper clears it

**Mitigation:**

1. **Always wrap each CLI call in a hard timeout** (`signal.alarm(N)`) — bail out on the FIRST hang, don't retry. Repeated reads just queue more bytes into the same stuck shell.
2. **Prefer `qFlipper-cli` for bulk operations** — it talks protobuf-over-serial RPC, not the CLI shell, and is not blocked by the VCP shell hang.
3. For read-only inspection, prefer these in order (fastest → slowest, smallest directory first):
   - `device_info` (read single response, ~200 bytes)
   - `info device` (~1 KB)
   - `info power` (~1 KB)
   - `uptime`, `date`, `free`, `free_blocks` (~50 bytes each)
   - `storage info /int` / `storage info /ext` (~200 bytes)
   - `storage list /int` (10 entries, ~600 bytes)
   - **AVOID** `storage list /ext/apps` and `storage list /ext/apps_data` if `apps/` is large — these routinely hang the CLI shell on a populated SD card.
4. **After a hang**: stop the python script. The Flipper serial is still alive; qFlipper CLI / RPC will still work. But do not try to recover the CLI shell — wait for the next power-cycle.

## CLI banner / first-prompt gotcha

When you open `/dev/cu.usbmodemflip_*` with pyserial, the FIRST command read often returns just the ASCII-art welcome banner (~700 bytes) followed by `>:`. The actual command output comes **after** `>:`. Always:

- Send `\r\n` first (or `echo hi`) and **wait for the banner to fully print** before parsing
- Use `out.rsplit('>:', 1)[1]` to extract only the command response, not the banner
- If you skip this and the banner is still flushing, your first real command will appear "empty" / "stuck" — this is not a real hang, just timing

Reference one-liner that handles banner correctly:

```python
import serial, time, signal, re
s = serial.Serial('/dev/cu.usbmodemflip_Ur1nicar1', 115200, timeout=4)
def cli(cmd, wait=1.5):
    for _ in range(2):
        s.write(b"\x03"); time.sleep(0.2)  # abort any prior top/storage list
    s.flushInput(); s.flushOutput()
    s.write((cmd + "\r\n").encode()); time.sleep(wait)
    out = s.read(8000).decode(errors='replace')
    if '>:' in out:
        return out.rsplit('>:', 1)[1].strip()
    return out.strip()

def alarm_handler(sig, frame): raise TimeoutError
signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(15)  # hard kill per command
try:
    print(cli('device_info'))
finally:
    signal.alarm(0)
```

## `/ext/update/<version>/` residual files — never auto-cleaned

**Observed 2026-06-30:** if a previous session did `storage write_chunk` to push a fake update package (e.g. `/ext/update/f7-update-1.4.3/{firmware.dfu, radio.bin, resources.ths, splash.bin, update.fuf, updater.bin}`), those files **stay on the SD card forever** even after the firmware itself is reflashed to a different build. qFlipper RPC's "Verify checksum → skip update" logic will accept them as a legitimate update payload and tell you "already up to date" without actually flashing.

To clean them:

```bash
# From Flipper CLI (when SD is mounted, USB Mass Storage mode):
rm -rf /ext/update/f7-update-<version>
# OR: from Mac when SD is mounted via USB Mass Storage:
rm -rf /Volumes/FLIPPER\ SD/update/f7-update-<version>
```

Before declaring a custom firmware is "bricks-locked" by `Storage write` protection, **check `/ext/update/` first** — that residual payload may be why qFlipper thinks it's already flashed.

## Tools

- `qFlipper`: Official GUI — backup/restore, file manager, firmware install, DFU repair
- `qFlipper-cli`: CLI version of qFlipper (case-sensitive binary name in `~/homebrew/bin/`)
  - Subcommands: `backup <file.tgz>`, `restore <file.tgz>`, `erase`, `wipe`, `firmware <file.dfu>`, `core2radio <file.bin>`, `core2fus <file.bin> <addr>`
  - **No pull/file-manager subcommand** — SD card access must go through GUI or Mass Storage
  - **Hangs at "Storage List @/int" if no SD card** — kill after 30s, fall back to pyserial
  - **Leaves serial lock if killed mid-flight** — always `pkill -9 -f qFlipper` before retry
- `pyserial`: Python serial communication with Flipper CLI (230400 baud). **The reliable fallback when qFlipper-cli hangs or fails on no-SD Flipper.**
- `screen`: Terminal serial client (`screen /dev/cu.usbmodemXXXX 230400`)
- Flipper CLI commands: `storage list/info/read/write/remove`, `update backup/restore/install`, `device_info`, `info device/power/power_debug`, `top`, `free`, `free_blocks`, `uptime`, `power off/reboot/reboot2dfu`, `help`
