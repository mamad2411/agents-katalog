---
name: flipper-zero-firmware
description: Flash, replace, or reflash Flipper Zero firmware — official release,
  custom forks (Momentum, Unleashed, Xtreme), or community Chinese-localized builds.
  Covers device-variant matching, .tgz extraction, DFU recovery, pre/post verification,
  and partial-translation awareness for forked firmware.
version: 1.0.0
category: hardware
license: MIT
metadata:
  hermes_origin: import
tags:
- flipper
- firmware
- flash
- dfu
- momentum
- unleashed
- qflipper
related_skills:
- flipper-zero-backup
- hardware-iot-hacking
---

# Flipper Zero Firmware Modification

Flash a new firmware onto a Flipper Zero (real / original hardware, not clones/clipper unless specified). Pairs with the `flipper-zero-backup` skill — **always run a full backup first**.

## ⚠️ Pre-flight: Backup is non-negotiable

Before any flash operation, run the `flipper-zero-backup` skill's full 3-layer backup. The flash process preserves `/ext` (SD card) but wipes `/int` (settings, BT pairing, Dolphin level). A backup gives you a one-command restore path if anything goes wrong.

## Determine the correct firmware variant

**Hardware variants** (from `device_info` output, `origin` field and `hardware_name`):

| `origin` field | Variant name to use | GitHub release asset suffix |
|---|---|---|
| `Official` | real / original | `original` or `real` |
| `Flipper` (clone boards) | clone | `clone` |
| Clipper hardware | clipper | `clipper` |

**Verify before flashing** — match what your device reports, NOT what the GitHub release page labels. Real hardware bought from Flipper Devices uses `original`. Clones sold on AliExpress/Taobao typically report `Flipper` as origin and need the `clone` variant.

```bash
# Capture device identity before flashing
~/.hermes/hermes-agent/venv/bin/python <<'PY'
import serial, time
ser = serial.Serial('/dev/cu.usbmodemflip_Ur1nicar1', 230400, timeout=2)
time.sleep(0.3)
ser.reset_input_buffer()
ser.write(b'device_info\r\n')
time.sleep(0.5)
print(ser.read(ser.in_waiting).decode('utf-8', errors='replace'))
ser.close()
PY
```

Look at: `origin`, `hardware_name`, `firmware_version`, `firmware_branch`.

## ⚠️ Pick the right install mode — DFU flash ≠ full update package install

There are **two distinct ways** to flash a firmware and they do different things:

| Mode | What gets installed | When to use |
|---|---|---|
| **DFU flash** (`qFlipper-cli firmware <file.dfu>`) | Single DFU image burned into internal flash. **Does NOT unpack `resources.tar.gz` / `firstboot.bin` / external .fap manifests.** | Quick fix, reverting, or when you don't need new resources. Also a step in the updater flow below. |
| **Full update package install** (`update install /ext/path/update.fuf` after staging) | DFU image + all bundled resources + firstboot + app manifests unpacked into `/int` and `/ext/apps/`. **Required for Chinese-language builds, any fork that ships resources.tar.gz > a few MB, or when you want bundled external apps.** | The "real" install. Use this by default. |

**Symptom of doing the wrong one**: user reports "大部分都還是英文啊" (or any feature relying on bundled resources appears missing). The fix is NOT a font hunt — it's that `resources.tar.gz` was never deployed. Re-do with the full update flow.

## Choose the right file format

| File format | What it contains | Flash via | Gotcha |
|---|---|---|---|
| `.tgz` | Full update package: `firmware.dfu` + `radio.bin` + `updater.bin` + `splash.bin` + `resources.tar.gz` + `update.fuf` + (sometimes `firstboot.bin`) | qFlipper GUI Install from file, OR stage to `/ext/update/<name>/` + `update install` | Use this for the full install mode |
| `.dfu` (extracted from .tgz) | Single DFU image | `qFlipper-cli firmware <file.dfu>` | DFU-only mode — incomplete for Chinese/resource-heavy builds |
| `.zip` | Same contents as .tgz in zip format | Unzip, treat like .tgz | Same as .tgz |

## Install mode A — Full update package (RECOMMENDED, default)

This is the **only** mode that fully installs Chinese-language Momentum-CN or any fork with bundled resources.

```bash
# 1. Download the .tgz
cd ~/Desktop/<some_backup_dir>/momentum_cn
curl -sL "https://github.com/<owner>/<repo>/releases/download/<tag>/<file>.tgz" -o firmware.tgz

# 2. Extract it locally to see the structure
mkdir -p /tmp/fw && tar -xzf firmware.tgz -C /tmp/fw/
ls /tmp/fw/f7-update-*/   # verify all 6-7 files present

# 3. Stage the entire package to /ext/update/<name>/ on the Flipper SD card
#    Use serial CLI storage write_chunk for each file (works headless, no qFlipper GUI needed).
#    See scripts/stage_update_package.sh for the full implementation.
#    This uploads all files (typically 15 MB total) to /ext/update/<name>/.

# 4. From the Flipper serial CLI, run:
#      update install /ext/update/<name>/update.fuf
#    The Flipper's updater:
#      - Verifies SHA of all components
#      - Loads updater.bin into RAM and reboots into it
#      - RAM updater applies firmware.dfu + radio.bin + resources + firstboot
#      - Reboots into new firmware
#    The CLI session disconnects during the reboot. Wait 60-90 s, then re-probe.

# 5. Verify — see "Verify after flash" below.
```

**Why this is the default**: in live testing (2026-06-30), DFU-only flash of Momentum-CN gave a Flipper showing firmware `v1.1.4` but most UI in English with only `紅外` Chinese — because `resources.tar.gz` (which contains all the resource pack + extracted icons) was never deployed. The full `update install` flow fixed it on the second pass.

## Install mode B — DFU flash only (escape hatch)

Use this only when:
- You're restoring the stock firmware and don't need bundled resources
- You're brick-recovering and the Flipper can't boot to CLI
- The user explicitly asks for the fastest flash and accepts partial deployment

```bash
# 1. Extract .dfu from the .tgz
mkdir -p /tmp/fw && tar -xzf firmware.tgz -C /tmp/fw/
cp /tmp/fw/f7-update-*/firmware.dfu /tmp/fw/firmware.dfu

# 2. Kill stale qFlipper
pkill -9 -f qFlipper 2>/dev/null
sleep 2

# 3. Flash
qFlipper-cli firmware /tmp/fw/firmware.dfu
```

**What qFlipper-cli does automatically (verified live):**

1. Protobuf version negotiation
2. Storage info / stat / datetime sync
3. **Backup /int** (it preserves your settings! ⚠️ but you should still have your own backup)
4. Start Recovery Mode → System Reboot
5. **Firmware Download** (~3-5 minutes, "Firmware Download @Ur1nicar")
6. Exit Recovery Mode
7. **Restore /int** from the auto-backup
8. System Reboot
9. Done — "All done! Thank you."

Total time: ~5 minutes from start to fully booted new firmware.

**⚠️ DO NOT unplug USB or press Flipper buttons during the flash.** The auto-backup of /int happens internally — if it fails, you'll lose settings, but your own backup will save you.

**⚠️ DO NOT use this mode for resource-heavy forks** (Momentum-CN, Unleashed, anything with `resources.tar.gz` > 1 MB). The DFU image alone does not include the resource pack.

## Flash via qFlipper GUI (alternative)

If CLI gives trouble (e.g. persistent "Permission error while locking the device"):

1. Open qFlipper app
2. Connect to Flipper (auto-detected)
3. Click "Install from file" (or "Update" → "Install from file")
4. Select the `.tgz` file directly (qFlipper GUI accepts .tgz; only CLI rejects it)
5. Wait for completion

GUI is slower to start but more tolerant of edge cases.

## DFU recovery (the ultimate safety net)

If the flash fails partway and the Flipper won't boot normally, recover via DFU:

**To enter DFU mode:**
- **From CLI**: `power reboot2dfu` (cleanest path, no screen interaction)
- **From device**: Hold LEFT + BACK for 5 seconds → release BACK, keep holding LEFT until blue LED appears
- **From hard brick**: Unplug USB, hold OK + BACK for 30 seconds, then plug USB

**Once in DFU mode:**
```bash
# Flash the full DFU image
qFlipper-cli firmware /path/to/full_image.dfu

# Or use qFlipper GUI → Repair (auto-downloads latest official)
```

The DFU bootloader lives in protected ROM — it cannot be overwritten by any firmware flash. **Even a complete brick is recoverable via DFU.** This is your safety net; always have the official firmware .dfu on disk before starting any custom flash.

## Verify after flash

After the device reboots into new firmware:

```python
import serial, time
ser = serial.Serial('/dev/cu.usbmodemflip_Ur1nicar1', 230400, timeout=2)
time.sleep(0.3)
ser.reset_input_buffer()
ser.write(b'device_info\r\n')
time.sleep(0.5)
out = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
# Check these fields:
#   firmware_origin_fork    (should match what you flashed — "Momentum", "Unleashed", etc.)
#   firmware_version        (e.g. "v1.1.4" for Momentum, "1.4.3" for official)
#   firmware_branch         (e.g. "v1.1.4" or "release")
#   hardware_name           (sanity: should still be your device)
ser.close()
```

**Cross-check**: If you flashed Momentum and the device still reports `firmware_origin_fork: Official`, the flash didn't take effect. Don't panic — re-flash or DFU recover.

### "Is this Momentum or Official?" — definitive diagnostic

The **only** reliable fork discriminator in `device_info` output is **`firmware_origin_fork`**:

```
firmware_origin_fork   = "Official"   → stock flipperdevices/flipperzero-firmware
firmware_origin_fork   = "Momentum"   → kalicyh Momentum (or Momentum-CN)
firmware_origin_fork   = "Unleashed"  → DarkFlippers Unleashed
firmware_origin_fork   = "Xtreme"     → Xtreme
```

**Common false-positive signals to ignore:**

- ❌ **`protobuf version: 0.25`** — **NOT** a Momentum marker. Official firmware 1.4.3 also reports `protobuf version: 0.25` (verified live 2026-06-30). Don't conclude "this is Momentum" just because qFlipper RPC reports 0.25.
- ❌ **`firmware_commit` not in `directory.json`** — the firmware CDN manifest at `update.flipperzero.one/firmware/directory.json` only lists `version`, `timestamp`, `changelog`, and `files` per release. It does **not** carry `commit` hashes, so you cannot cross-check a running `firmware_commit` against the manifest. Custom forks built on top of Official source can legitimately share commit strings with stock firmware.
- ❌ **`firmware_version: 1.4.3` matches release** — Momentum is built on top of Official source so its `firmware_version` field reads the upstream version it was forked from. A match does NOT prove it's Official.

**Sample `device_info` from a stock Official 1.4.3 Flipper (verified live, 2026-06-30):**

```
firmware_version              : 1.4.3
firmware_commit               : 8622f1a2
firmware_branch               : 1.4.3
firmware_branch_num           : 0
firmware_build_date           : 05-12-2025
firmware_target               : 7
firmware_api_major            : 87
firmware_api_minor            : 1
firmware_origin_fork          : Official
firmware_origin_git           : https://github.com/flipperdevices/flipperzero-firmware
hardware_model                : Flipper Zero
hardware_uid                  : DAE9650127E18000
hardware_otp_ver              : 2
hardware_ver                  : 12
hardware_target               : 7
hardware_region               : 4
hardware_region_provisioned   : TW
hardware_name                 : Ur1nicar
```

**One-liner to dump just the fork discriminator + version via pyserial:**

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

Default baud **115200** works for read-only CLI queries on stock 1.4.3 (firmware default). 230400 is also fine and documented in the backup skill — both work, just use 115200 if you're scripting from a fresh state.

**Also verify SD card preservation:**
```bash
storage list /ext
# Should show same directories (apps, subghz, nfc, badusb, infrared, etc.)
# and same files as before the flash
```

## Post-flash: SD card content survives

**Confirmed live (2026-06-30, Momentum-CN v1.1.4 flash on Official 1.4.3):**
- All 28 SD card files preserved (subghz, nfc, IR, badusb scripts, u2f, dolphin manifest)
- `/int` settings auto-restored by qFlipper-cli
- Bluetooth pairing still in `.bt.keys`
- Dolphin level preserved

**No need to "migrate" BadUSB scripts or other plain-text assets** — they survive as-is, since custom forks don't touch `/ext` content during flash.

## Custom firmware fork gotchas

### Momentum / Unleashed / Xtreme (general)

- **BLE / Bluetooth pairing may need re-pair** after flash (3-way forget: phone forgets Flipper, Flipper forgets phone, re-pair)
- **Some apps are renamed or restructured** — old script paths in favorites may not resolve
- **CLI command names differ**: Momentum replaces `top` with `log`. Run `help` after flash to discover new commands.
- **Settings apps differ** — don't expect the same UI flow as official firmware

### Momentum-CN (Chinese-localized) specific

From the `kalicyh/Momentum-Firmware-CN` README:
- Chinese strings are **compiled into the firmware** via `localization/zh_CN/strings.json` (not loaded from SD card)
- Chinese font `primary_zh.u8f` is **compiled into the firmware** (verified: `extern const uint8_t primary_zh[]` in `canvas.c`)
- Optional font replacement: download `momentum-fw-cn-v<version>-zh-fonts.zip`, rename any `.u8f` to `primary_zh.u8f`, place in `/ext/zh_fonts/` (manual override)
- **All release variants are built with `MOMENTUM_UI_LANG=zh_CN`** — Chinese UI is always on
- **Partial translation is normal**: core UI (Settings, NFC, Sub-GHz, Infrared, iButton, LF RFID, BadUSB main flow) is fully translated; **app-internal text in some third-party .fap apps may still be English**. This is a known limitation, not a missing font.
- **245 external .fap apps included**, 243 have Chinese menu names; the remaining 2 keep English names
- 3 device variants in releases: `original` (real hardware), `clone`, `clipper`
- Branch name in repo is `CN-Clipper` (default), not `main`

**If user complains "大部分都還是英文啊" after flashing**: do NOT assume it's the partial-translation reality. Diagnose in this order:

1. **Did you use the full `update install` workflow, or just DFU flash?** If you ran `qFlipper-cli firmware <file.dfu>` instead of staging the full .tgz and running `update install`, then `resources.tar.gz` was never deployed. The Chinese strings compile into the firmware but the resource pack (icons, app manifests, font cache) lives separately. Re-do with the full update flow.
2. **Was the device rebooted after DFU flash?** After the updater finishes, the Flipper often ends up back in DFU mode (USB PID 0x5740) until the host re-enumerates. Force a USB reset by unplugging and replugging the Flipper USB cable.
3. **Is it actually a partial-translation reality?** Check core UI first — Settings, NFC menu, Sub-GHz menu, main menu labels. If those are still English, the install is incomplete. If those are Chinese but some third-party .fap screens are English, then yes, it's the partial-translation reality (see below).

**Partial-translation reality (after a verified full install)**:

- ✅ Fully Chinese: Settings, NFC menu, Sub-GHz menu, Infrared menu, iButton menu, LF RFID menu, BadUSB main flow, main menu labels
- ⚠️ May still be English: some third-party .fap apps, Dolphin animation titles, certain error messages
- The 245 bundled external apps: 243 have Chinese menu names (`name_zh` in application.fam), 2 don't
- The Chinese font is always rendered for non-ASCII characters (so Chinese text displays correctly even in partially-translated apps)

**Rule of thumb**: if the user names *specific screens* that are English (e.g. "NFC 選單是中文但 Sub-GHz frequency analyzer 還是英文"), it's the partial-translation reality. If they say "Settings 也是英文" or "整個 UI 還是英文", the install is incomplete — re-do with `update install`.

## Restore path (rolling back)

**To go back to a previously-working state:**

1. Plug in Flipper (powered on, normal mode)
2. `qFlipper-cli firmware ~/Desktop/FlipperBackup/official_firmware/flipper-z-f7-update-1.4.3.tgz` — wait, this fails (CLI wants DFU format). Use the .dfu:
3. `qFlipper-cli firmware ~/Desktop/FlipperBackup/official_firmware/flipper-z-f7-full-1.4.3.dfu`
4. Wait for completion (~3 minutes)
5. Optional: `qFlipper-cli restore ~/Desktop/FlipperBackup/internal/flipper_int_backup.tgz` to restore settings
6. Optional: copy back SD card content from `~/Desktop/FlipperBackup/sd_card/` if it was lost

## Pitfalls (battle-tested)

- **`qFlipper-cli firmware <file.tgz>` fails immediately** with "Please provide a firmware file in DFUse format." Must extract `firmware.dfu` from .tgz first. qFlipper GUI accepts .tgz; CLI only accepts .dfu.
- **DFU-only flash does NOT install the full update package.** `qFlipper-cli firmware <file.dfu>` (or qFlipper Repair on a stock .dfu) burns only the DFU image. It does NOT unpack `resources.tar.gz`, `firstboot.bin`, or external .fap app manifests that ship in the .tgz. Symptom: firmware version reads correctly, BLE/SD works, but UI is missing resources, fonts aren't applied, or bundled external apps aren't installed. For resource-heavy forks (Momentum-CN, anything with `resources.tar.gz` > 1 MB), use the **full update install flow** instead: stage the entire extracted .tgz to `/ext/update/<name>/`, then run `update install /ext/update/<name>/update.fuf`. See "Install mode A" above.
- **macOS locks the STM32WB55 USB DFU interface via AppleUSBDFU.kext.** After the updater reboots the Flipper into DFU, macOS auto-claims the device. dfu-util reports "No DFU capable USB device available" even though `ioreg` shows PID 0x5740. Workarounds: (1) physically unplug-replug the Flipper USB cable to force re-enumeration; (2) send a null/empty byte to the CDC serial port `/dev/cu.usbmodemflip_*` — the bootloader re-emits the Flipper CLI banner and the device exits DFU on its own; (3) use qFlipper GUI which has a recovery path that handles the kext claim internally. **Don't waste time on `brew install dfu-util` + libusb workarounds** — they all hit the same macOS kext claim.
- **Sending `\x00` (or any null byte) to the CDC serial port in DFU mode wakes the bootloader.** This was discovered live: after `update install` triggered a DFU reboot, the device stopped responding to qFlipper RPC, but writing `\x00\x00\x00\x00` to `/dev/cu.usbmodemflip_*` made the bootloader re-emit the full Flipper CLI banner and complete the install. Useful escape hatch when qFlipper is stuck and you don't want to ask the user to physically touch the cable.
- **Don't confuse the variant suffix** — flashing `clipper` firmware on real hardware can brick the device (it's not quite the same bootloader target). Verify via `device_info` first.
- **Serial CLI commands change after flashing custom firmware** — `top` becomes `log` on Momentum, etc. Don't blindly call familiar commands; check `help` first.
- **BLE pairing often needs re-pairing** after a flash, even when `/int/.bt.keys` is preserved. The pairing info is preserved but the actual BLE session is reset.
- **Stale qFlipper process = serial lock = next flash fails** with "Permission error while locking the device". Always `pkill -9 -f qFlipper` between flash attempts.
- **Don't disconnect during "Firmware Download" phase** — this is when the actual DFU write happens. Interrupting here can brick the device. Recovery: DFU mode.
- **Custom firmware SD card structure is the same as official** — no need to migrate files. Custom forks share the same `/ext/{subghz,nfc,badusb,infrared,u2f,lfrfid,ibutton,dolphin}` layout.
- **Custom firmware can include extra apps not in official** — Momentum/Unleashed ship with .fap apps pre-installed in `/ext/apps/`. These appear automatically on first boot.
- **Momentum's `nfc`/`subghz`/`ir` CLI commands** are NOT in the official CLI — they exist as external commands. If `help` doesn't show them, run `reload_ext_cmds` or check if the firmware has the relevant .fap installed.
- **`storage write_chunk` is the headless way to upload binary files to Flipper via serial CLI.** Protocol: `storage write_chunk <path> <bytes>` → wait for `Ready` prompt → send raw bytes → wait for `>` prompt back. No length terminator needed beyond the count. Verified for 15 MB+ uploads of update package contents (firmware.dfu, resources.tar.gz). For paths with spaces, wrap in double quotes: `storage write_chunk "/ext/badusb/CAUGHT IN 4K.txt" <bytes>`. After upload, verify with `storage stat <path>` — the size MUST match `wc -c` on the local file. MD5 verification via `storage md5 <path>` is unreliable because the CLI echoes the command before the hash, so parser noise can confuse the comparison.
- **`storage read` strips newlines inconsistently.** Files come back with mixed `\r\n` or just `\n` depending on file type. Always normalize to `\n` after downloading: `sed -i '' 's/\r$//' <file>`. NFC files in particular lose the `Filetype:` header if the parser grabs the wrong slice — verify the first line is `Filetype: Flipper NFC device` (or `Filetype: IR signals file` for .ir).
- **"Did you actually verify it?"** — Wang's hard rule after this session: never report a flash as "verified" without (1) checking `firmware_version` and `firmware_origin_fork` via `device_info`, (2) listing `/ext` and `/int` and confirming expected files, (3) for Chinese builds, opening the Flipper's main menu and confirming at least Settings shows Chinese. The user has corrected this twice. If you can't verify, say so.

## Quick Start

```bash
# 0. Already done: full backup via flipper-zero-backup skill
#    ~/Desktop/FlipperBackup/ should have: internal/, sd_card/, official_firmware/

# 1. Identify device variant
ls /dev/cu.usbmodemflip* 2>/dev/null  # capture port
# Read device_info → confirm origin = "Official" → use "original" variant

# 2. Download firmware .tgz
cd ~/Desktop/FlipperBackup/momentum_cn
curl -sL "https://github.com/kalicyh/Momentum-Firmware-CN/releases/download/v1.1.4/momentum-fw-cn-v1.1.4-original.tgz" -o firmware.tgz

# 3. Extract .dfu
tar -xzf firmware.tgz
cp f7-update-*/firmware.dfu ./firmware.dfu

# 4. Kill stale qFlipper
pkill -9 -f qFlipper && sleep 2

# 5. Flash
qFlipper-cli firmware ./firmware.dfu
# Wait ~5 minutes for: auto-backup /int → recovery mode → download → exit recovery → restore /int → reboot

# 6. Verify
# Read device_info, check firmware_origin_fork = "Momentum"
# Check /ext/ for preserved files
```

## See also

- `flipper-zero-backup` skill — run this BEFORE any firmware modification
- `references/momentum-cn.md` — Momentum-CN specific install + Chinese font notes
- `references/variant-matching.md` — how to identify hardware variant from device_info
- `references/device-info-fields.md` — verified `device_info` output + field-by-field meaning + authoritative fork detection rule
- `scripts/verify_firmware.sh` — pyserial one-liner to dump fork-discriminating fields (`firmware_origin_fork`, etc.)

## Tools reference

- **qFlipper-cli** (`~/homebrew/bin/qFlipper-cli`) — CLI flash via `firmware <file.dfu>` subcommand
- **qFlipper GUI** — accepts .tgz directly; slower startup but more forgiving
- **pyserial** — direct serial CLI for verification + DFU recovery commands (`power reboot2dfu`)
- **DFU mode** — built into ROM, always accessible via screen combo or CLI command
- **curl + tar** — fetch and extract release artifacts