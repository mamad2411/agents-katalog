---
name: firmware-deployment
description: "Use when flashing, updating, or recovering firmware on classroom robots (ESP32, RP2040/Pico, AVR/Arduino) — covers mpremote/esptool/avrdude/UF2 tooling, ESP32 OTA with dual partitions, firmware version checks, safe-mode boot on crash loops, serial REPL debugging, and mass-flashing 30 robots from one laptop. Provides exact commands, baud rates, partition tables, working MicroPython/C++ code, and recovery procedures."
category: robotics
domain: robotics
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "rahulbachina/robotics-skills"
  commit: "e69d9828fb"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# Firmware Deployment for Classroom Robots

Expert knowledge for deploying firmware to fleets of student robots: ESP32 (MicroPython + Arduino C++), RP2040/Pico (UF2 + MicroPython), and AVR/Arduino Uno/Nano. Optimized for the worst-case environment: 30 robots, 1 laptop, 45-minute class period, USB hubs of unknown quality, students who unplug things mid-flash.

---

## 1. Tooling Comparison — Pick the Right Flasher

| Tool | Targets | Transport | Speed (typical) | Needs driver? | Brick risk | Best for |
|---|---|---|---|---|---|---|
| `esptool.py` | ESP32/ESP8266/ESP32-S2/S3/C3 | Serial (USB-UART or native USB) | 460800–921600 baud, ~10s for 1.5MB | CP210x/CH340 on Win | Low (ROM bootloader is mask ROM, unbrickable) | Full firmware images, MicroPython base install |
| `mpremote` | Any MicroPython board | Serial raw-REPL | ~9 KB/s file copy | Same as above | None (only writes files) | Deploying .py app code on top of MicroPython |
| `avrdude` | ATmega328P (Uno/Nano), ATmega2560 | Serial via Optiboot bootloader, or ISP | 115200 baud (Uno), 57600 (old Nano) | CH340 for clones | Medium if fuses touched via ISP — never touch fuses in classroom | Arduino .hex deployment |
| UF2 drag-drop | RP2040 (Pico), SAMD21/51, nRF52 | USB Mass Storage (BOOTSEL) | ~2s for typical UF2 | None — appears as drive | Effectively zero (BOOTSEL ROM is immutable) | Classroom RP2040 — most student-proof option |
| `picotool` | RP2040 | USB (BOOTSEL mode) | Same as UF2 | libusb (Zadig on Win) | Zero | Scripted RP2040 flashing, reading board info |
| `arduino-cli` | Anything Arduino-core supports | Wraps avrdude/esptool | n/a | n/a | Low | Compile + upload C++ in one command |
| ESP32 OTA | ESP32 family | WiFi (HTTP/HTTPS) | ~30–60s per robot, parallelizable | None | Low IF dual-partition + rollback configured | Updating a fleet already in the field |

**Decision rule:**
- RP2040 fleet → UF2 for base firmware, `mpremote` for app code. Lowest support burden.
- ESP32 fleet → `esptool` once for MicroPython, then `mpremote` for app code, then OTA after WiFi works.
- AVR fleet → `arduino-cli compile && arduino-cli upload`. No OTA possible; plan around USB.
- Never use Arduino IDE GUI for fleet work — it cannot be scripted.

### Exact install commands

```bash
pip install esptool mpremote adafruit-ampy   # ampy only as fallback
pip install picotool  # or download binary; on Windows run Zadig once for BOOTSEL device
# arduino-cli
winget install ArduinoSA.CLI   # or: brew install arduino-cli
arduino-cli core install arduino:avr esp32:esp32
```

---

## 2. ESP32 Flashing with esptool — Exact Commands

### Identify chip and port first

```bash
esptool.py --port COM7 chip_id
# Output tells you: ESP32-D0WD-V3, ESP32-S3, etc. Flash size: read with
esptool.py --port COM7 flash_id
```

Port discovery:
- Windows: `mode` or `python -m serial.tools.list_ports -v` → COM ports. CP210x = "Silicon Labs", CH340 = "USB-SERIAL CH340".
- Linux: `/dev/ttyUSB0` (CP210x/CH340) or `/dev/ttyACM0` (native USB on S2/S3/C3). Add user to `dialout` group or every flash fails with permission denied.
- macOS: `/dev/cu.usbserial-*` or `/dev/cu.SLAB_USBtoUART`. Use `cu.*` not `tty.*` (tty blocks on DCD).

### Flash MicroPython (classic ESP32, 4MB flash)

```bash
esptool.py --chip esp32 --port COM7 erase_flash
esptool.py --chip esp32 --port COM7 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20240602-v1.23.0.bin
```

**Offsets differ by chip — wrong offset = boot loop, not error:**

| Chip | MicroPython offset | Notes |
|---|---|---|
| ESP32 (classic) | `0x1000` | Bootloader at 0x1000 |
| ESP32-S2 | `0x1000` | |
| ESP32-S3 | `0x0` | Bootloader at 0x0 — most common student-help-desk mistake |
| ESP32-C3 | `0x0` | Same |

### Baud rate reality

- 921600: works on short good cables direct to laptop. Fails (`Invalid head of packet`) on cheap hubs.
- 460800: the reliable default. Use this for classroom.
- 115200: fallback when 460800 throws checksum errors. ~40s per flash.
- If `Failed to connect: Timed out waiting for packet header` → hold BOOT (GPIO0) while esptool retries, or board lacks auto-reset circuit (some bare DevKitC clones with bad transistors). Holding BOOT during power-up always works.

### Arduino C++ on ESP32 via arduino-cli

```bash
arduino-cli compile --fqbn esp32:esp32:esp32 --build-path ./build sketch/
arduino-cli upload --fqbn esp32:esp32:esp32 -p COM7 --input-dir ./build sketch/
# Compile ONCE, upload the same ./build to all 30 robots. Never recompile per robot.
```

---

## 3. mpremote — App Code Deployment on MicroPython

`mpremote` talks raw-REPL over serial. It cannot run while anything else holds the port (close Thonny, close PuTTY, kill stray `screen`).

```bash
mpremote connect COM7 ls                      # list files on board
mpremote connect COM7 cp main.py :main.py     # deploy single file
mpremote connect COM7 cp -r lib/ :            # deploy whole lib tree
mpremote connect COM7 run test_motors.py      # run WITHOUT copying (great for debug)
mpremote connect COM7 exec "import machine; machine.reset()"
mpremote connect COM7 repl                    # interactive REPL, Ctrl-] to exit
mpremote connect COM7 mip install umqtt.simple  # install package from micropython-lib
```

**Auto-connect shortcut**: `mpremote ls` with no `connect` grabs the first MicroPython board found — never use this with a hub full of robots; always specify the port.

**The main.py trap**: if `main.py` has a tight loop with no `sleep`, the raw REPL can't interrupt it and mpremote times out. Recovery:

```bash
mpremote connect COM7 exec --no-follow "1"   # sometimes enough
# If not: hold Ctrl-C in `mpremote repl` immediately after pressing the board's RESET
# If main.py crashes the board before USB enumerates: erase_flash and start over.
```

Prevent it: see safe-mode pattern in §6.

---

## 4. RP2040 / Pico — UF2 and picotool

### UF2 flow (zero-tooling, student-safe)

1. Hold BOOTSEL, plug USB (or tap RUN while holding BOOTSEL). Board mounts as `RPI-RP2` drive.
2. Copy `firmware.uf2` onto the drive. Board auto-reboots when copy completes. Done.

Scripted (Windows PowerShell):

```powershell
$drive = (Get-Volume -FileSystemLabel "RPI-RP2" -ErrorAction SilentlyContinue).DriveLetter
if ($drive) { Copy-Item firmware.uf2 "${drive}:\" }
```

### picotool for scripting

```bash
picotool info -a                      # board id, flash size, current binary name
picotool load firmware.uf2 -f        # -f force: reboots a RUNNING board into BOOTSEL first
picotool reboot                       # back to app
```

`picotool load -f` only works if the running firmware was built with stdio USB enabled (MicroPython: yes). If the app crashed hard, you must use the physical BOOTSEL button — there is no software path.

**Flash-nuke**: if a Pico's MicroPython filesystem is corrupted (board boots but `ls` shows garbage / OSError 5), flash `flash_nuke.uf2` (official Raspberry Pi binary) then re-flash MicroPython. 10 seconds, fixes 95% of "weird Pico" tickets.

---

## 5. AVR / Arduino — avrdude

```bash
# Uno (Optiboot, 115200):
avrdude -c arduino -p atmega328p -P COM7 -b 115200 -D -U flash:w:firmware.hex:i
# Old-bootloader Nano clones (57600 — the #1 clone gotcha):
avrdude -c arduino -p atmega328p -P COM7 -b 57600 -D -U flash:w:firmware.hex:i
# Mega2560 (stk500v2):
avrdude -c wiring -p atmega2560 -P COM7 -b 115200 -D -U flash:w:firmware.hex:i
```

- `-D` = don't erase EEPROM/chip; required with Optiboot.
- `avrdude: stk500_recv(): programmer is not responding` → wrong baud (try 57600), wrong `-c`, or another program holds the port.
- `not in sync: resp=0x00` repeatedly on Nano clone → it's an old-bootloader board: 57600.
- **Never** issue `-U lfuse/-U hfuse` in a classroom context. A wrong fuse byte (e.g., selecting external crystal that doesn't exist) bricks the chip beyond serial recovery — requires high-voltage programmer.
- AVR has no OTA, no filesystem, no REPL. Every code change = USB cable. Budget class time accordingly.

---

## 6. ESP32 OTA — Dual Partition Updates

### Partition table (4MB flash, the one to use)

`partitions_two_ota.csv`:

```csv
# Name,   Type, SubType,  Offset,   Size
nvs,      data, nvs,      0x9000,   0x5000
otadata,  data, ota,      0xe000,   0x2000
app0,     app,  ota_0,    0x10000,  0x180000
app1,     app,  ota_1,    0x190000, 0x180000
spiffs,   data, spiffs,   0x310000, 0xF0000
```

Two 1.5MB app slots. `otadata` records which slot is active. Update flow: download new image into the INACTIVE slot → verify → mark pending → reboot → new firmware must call "mark valid" or the bootloader rolls back next reset.

Arduino IDE/cli: select partition scheme `min_spiffs` or `default` (both have ota_0/ota_1). FQBN flag: `--fqbn esp32:esp32:esp32:PartitionScheme=default`.

### Arduino C++ OTA pull-updater (robot polls a server)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <Update.h>
#include <esp_ota_ops.h>

#define FW_VERSION 7  // bump every release — integer compare, never string compare

void checkForUpdate(const char* baseUrl) {
  HTTPClient http;
  http.begin(String(baseUrl) + "/version.txt");
  if (http.GET() != 200) { http.end(); return; }
  int remote = http.getString().toInt();
  http.end();
  if (remote <= FW_VERSION) return;          // <= not != : prevents downgrade ping-pong

  http.begin(String(baseUrl) + "/firmware.bin");
  if (http.GET() != 200) { http.end(); return; }
  int len = http.getSize();
  if (len <= 0 || !Update.begin(len)) { http.end(); return; }
  size_t written = Update.writeStream(http.getStream());
  http.end();
  if (written == (size_t)len && Update.end(true)) {
    ESP.restart();                            // bootloader boots new slot
  } else {
    Update.abort();                           // partial write: slot discarded, old fw keeps running
  }
}

void setup() {
  // FIRST THING after confirming the app works (WiFi up, sensors respond):
  esp_ota_mark_app_valid_cancel_rollback();
  // If you skip this and CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE is on,
  // the bootloader reverts to the old slot on the next reset. That's the feature.
}
```

**Rules that prevent fleet bricks:**
1. Version file and firmware.bin are uploaded to the server in this order: bin first, version.txt last. Robots that poll mid-upload see old version number + complete old logic — never new number + half-uploaded bin.
2. `Update.begin(len)` with real Content-Length, never `UPDATE_SIZE_UNKNOWN`, so a truncated download fails the size check.
3. Call `esp_ota_mark_app_valid_cancel_rollback()` only AFTER self-test passes (motors respond, WiFi reconnects). A new firmware that boots but can't reach WiFi will roll back automatically — exactly what you want.
4. Robots check for updates at boot + every N minutes with jitter (`delay(random(0, 30000))` before first check) — 30 robots hitting one classroom Pi server simultaneously will time out half of them.
5. Keep firmware < 1.4MB (slot is 1.5MB). Check `arduino-cli compile` output line "Sketch uses X bytes".

### MicroPython OTA

MicroPython on ESP32 normally updates by replacing `.py` files, not the firmware image — use `mpremote` over WebREPL or a tiny self-updater:

```python
# ota_app.py — updates application files, not the interpreter
import urequests, machine, os

VERSION = 7
BASE = "http://192.168.4.1:8000"

def check_update():
    try:
        r = urequests.get(BASE + "/version.txt", timeout=5)
        remote = int(r.text.strip()); r.close()
    except Exception:
        return
    if remote <= VERSION:
        return
    try:
        r = urequests.get(BASE + "/app.py", timeout=15)
        body = r.text; r.close()
        if len(body) < 100 or "def main" not in body:   # sanity gate
            return
        with open("app_new.py", "w") as f:
            f.write(body)
        os.rename("app_new.py", "app.py")               # atomic-ish: never half-written app.py
        machine.reset()
    except Exception:
        try: os.remove("app_new.py")
        except OSError: pass
```

Write to a temp file and rename — a power cut during `open("app.py","w")` leaves a robot with an empty app.py and no recovery except USB.

---

## 7. Version Checks — Fleet Hygiene

Every firmware must self-report its version. Non-negotiable for fleet work.

```python
# boot.py (MicroPython) — robot prints identity on every boot
VERSION = "2.3.1"
ROBOT_ID = "robot-07"   # written once per robot at provisioning, stored in robot_id.txt
print(f"[FW] {ROBOT_ID} v{VERSION}")
```

```cpp
// Arduino: respond to a serial query so the flash script can audit
void serialEvent() {
  if (Serial.readStringUntil('\n') == "VERSION?") {
    Serial.printf("robot-%02d v%d\n", ROBOT_ID, FW_VERSION);
  }
}
```

Audit a hub of robots:

```bash
for p in $(python -m serial.tools.list_ports -q); do
  v=$(mpremote connect $p exec "import app; print(app.VERSION)" 2>/dev/null)
  echo "$p -> ${v:-NO RESPONSE}"
done
```

Rules:
- Integer or semver-tuple compare, never string compare ("10" < "9" lexically).
- Version lives in ONE place in code; flash scripts read it from the source, not from a README.
- After a classroom flash session, run the audit loop and require all robots to report the same version before class starts. A mixed-version fleet produces "it works on robot 3 but not robot 12" bugs that eat the whole lesson.

---

## 8. Safe-Mode Boot — Surviving Student Crash Loops

The classic failure: student deploys `main.py` with an infinite loop that crashes or hard-blocks → board reboots → main.py runs again → REPL unreachable → "the robot is dead."

### MicroPython safe-mode pattern (boot.py)

```python
# boot.py — DO NOT let students edit this file
import machine, os, time

CRASH_FILE = "crash_count.txt"
MAX_CRASHES = 3

def read_crashes():
    try:
        with open(CRASH_FILE) as f:
            return int(f.read())
    except (OSError, ValueError):
        return 0

def write_crashes(n):
    with open(CRASH_FILE, "w") as f:
        f.write(str(n))

crashes = read_crashes()

# A reset caused by the watchdog or a hard fault means the app died
if machine.reset_cause() in (machine.WDT_RESET, machine.HARD_RESET):
    crashes += 1
    write_crashes(crashes)
else:
    write_crashes(0)          # clean power-on resets the counter

if crashes >= MAX_CRASHES:
    print("[SAFE MODE] app crashed %d times — main.py NOT run" % crashes)
    write_crashes(0)
    import sys
    sys.exit()                 # boot.py exits, main.py is SKIPPED, REPL is live
```

And in main.py, feed a watchdog so hangs (not just crashes) trigger the counter:

```python
import machine
wdt = machine.WDT(timeout=8000)   # 8s; ESP32 min is ~1s, max varies
while True:
    wdt.feed()
    step()                         # student code — if it blocks >8s, WDT resets, counter increments
```

Also teach the manual escape: hold the BOOT/USER button during reset and check it in boot.py:

```python
import machine
if machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP).value() == 0:
    print("[SAFE MODE] button held"); import sys; sys.exit()
```

### Arduino equivalent

Use RTC memory (survives reset, not power cycle) + `esp_reset_reason()`:

```cpp
#include <esp_system.h>
RTC_NOINIT_ATTR int crashCount;

void setup() {
  esp_reset_reason_t r = esp_reset_reason();
  if (r == ESP_RST_PANIC || r == ESP_RST_TASK_WDT || r == ESP_RST_INT_WDT) crashCount++;
  else crashCount = 0;
  if (crashCount >= 3) { safeMode(); }  // serial-only loop: accepts OTA + VERSION?, no app logic
}
```

RP2040 MicroPython: same boot.py pattern works; also remind helpers that `flash_nuke.uf2` is the nuclear option (10 seconds, always works).

---

## 9. Serial REPL Debugging

### Terminal settings

115200 8N1, no flow control — for MicroPython REPL and Arduino `Serial.begin(115200)`. Mismatched baud shows garbage like `␀␀ÿ~ÿ` — it's the baud, not a broken board.

```bash
mpremote connect COM7 repl        # best for MicroPython
python -m serial.tools.miniterm COM7 115200   # works for anything
# PuTTY: Serial, COM7, 115200. Tera Term fine too. Avoid Arduino IDE monitor for REPL (no Ctrl-keys).
```

### REPL control keys (MicroPython)

| Key | Effect |
|---|---|
| Ctrl-C | KeyboardInterrupt — breaks a running loop (if it isn't blocked in C code) |
| Ctrl-D | Soft reset — re-runs boot.py + main.py, keeps filesystem |
| Ctrl-A | Raw REPL (what mpremote uses) — Ctrl-B to get back to friendly REPL |
| Ctrl-E | Paste mode — paste multi-line code without auto-indent mangling, Ctrl-D to run |

### Reading ESP32 boot output

After reset you always see ROM chatter at **74880 baud** equivalent garbage then 115200 text. Key lines:

- `rst:0x1 (POWERON_RESET)` — normal power-up
- `rst:0x8 (TG1WDT_SYS_RESET)` — task watchdog fired: code blocked too long
- `rst:0xc (SW_CPU_RESET)` + `Guru Meditation Error: Core 1 panic'ed (LoadProhibited)` — null/bad pointer in C++; `EXCVADDR: 0x00000000` confirms null deref
- `Brownout detector was triggered` — **power problem, not code**. Motors stalling drag 3V3 down. Fix wiring/battery; students will burn hours "debugging code" that is a sagging supply
- Boot loop printing `invalid header: 0xffffffff` — wrong flash offset (see §2 table) or erased flash with no firmware

### Debug printing that doesn't break timing

```python
DEBUG = True
def dbg(*a):
    if DEBUG: print(*a)
# print() at 115200 takes ~87µs/char. A 40-char line = 3.5ms — enough to wreck a 50Hz
# control loop if you print every iteration. Print every Nth loop or on change only.
```

---

## 10. Classroom Flash Loop — 1 Laptop, 30 Robots

### Hardware that makes this work

- **Powered** USB hub(s), 10-port, with per-port switches if possible. Unpowered hubs brown out at 3+ ESP32s (each draws 200–500mA spikes during flash/WiFi init).
- Short (30cm) known-good **data** cables, labeled. Half of all "flashing problems" are charge-only cables. Test every cable once with `esptool chip_id` and bin the failures.
- Label each robot AND its assigned port number. Robot ↔ port mapping kills 90% of "which robot did I just flash?" confusion.

### Strategy ladder (fastest first)

1. **OTA broadcast** (ESP32 fleet, already provisioned): put `firmware.bin` + `version.txt` on a laptop/Raspberry-Pi HTTP server on the classroom AP; robots self-update on boot. 30 robots in ~3 minutes, zero cables. This is the goal state.
2. **Parallel USB**: hub + script below. ~30 robots in 10–15 min.
3. **Sequential USB**: same script, one cable, conveyor-belt style. Have a student runner swap robots. ~25–40 min — only acceptable for the initial provisioning day.

### Parallel flash script (Python, works on Windows/macOS/Linux)

```python
#!/usr/bin/env python3
"""Flash app code to every MicroPython robot on the hub. pip install pyserial"""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from serial.tools import list_ports

FILES = ["app.py", "main.py", "lib/motors.py"]
EXPECT_VERSION = "2.3.1"

def is_robot(p):
    # CP210x VID 0x10C4, CH340 0x1A86, Espressif native 0x303A, Pico 0x2E8A
    return p.vid in (0x10C4, 0x1A86, 0x303A, 0x2E8A)

def flash(port):
    try:
        for f in FILES:
            subprocess.run(["mpremote", "connect", port, "cp", f, f":{f}"],
                           check=True, capture_output=True, timeout=60)
        out = subprocess.run(["mpremote", "connect", port, "exec",
                              "import app; print(app.VERSION)"],
                             check=True, capture_output=True, timeout=15, text=True)
        v = out.stdout.strip().splitlines()[-1]
        ok = (v == EXPECT_VERSION)
        subprocess.run(["mpremote", "connect", port, "exec",
                        "import machine; machine.reset()"], capture_output=True, timeout=10)
        return port, "OK" if ok else f"VERSION MISMATCH ({v})"
    except subprocess.TimeoutExpired:
        return port, "TIMEOUT (main.py blocking? hold BOOT + retry)"
    except subprocess.CalledProcessError as e:
        return port, f"FAIL: {e.stderr.decode(errors='replace')[:120]}"

ports = [p.device for p in list_ports.comports() if is_robot(p)]
print(f"Found {len(ports)} robots: {ports}")
with ThreadPoolExecutor(max_workers=8) as ex:        # >8 parallel serial ops gets flaky on Windows
    for port, status in ex.map(flash, ports):
        print(f"  {port}: {status}")
```

For full-image flashing (esptool) the same pattern applies but cap `max_workers=4` — esptool at 460800 saturates cheap hub bandwidth, and parallel flashes start failing checksums above that.

### Classroom procedure (battle-tested)

1. Flash + verify ONE robot completely. Run it. Only then touch the other 29.
2. Run the parallel script. Triage failures into a "hospital" pile; don't debug them while 25 students wait.
3. Run the version audit (§7). Tape over USB ports if students should not reflash.
4. Hospital pile, in order: swap cable → swap hub port → hold BOOT during connect → `erase_flash` + full reinstall → `flash_nuke.uf2` (Pico) → hardware fault, swap robot.
5. Keep 2–3 pre-flashed spare robots. Swapping a robot takes 30 seconds; debugging one takes 20 minutes you don't have.

---

## 11. Debugging Checklist — "It Won't Flash"

Work top to bottom; each step is ~30 seconds.

1. **Cable**: swap for a known-good data cable. (~50% of all cases.)
2. **Port exists?** `python -m serial.tools.list_ports -v`. Nothing listed → driver (CH340/CP210x on Windows) or dead cable/board.
3. **Port busy?** Close Thonny, Arduino Serial Monitor, PuTTY, other mpremote. Windows error: `PermissionError(13, 'Access is denied')`; Linux: `Device or resource busy`.
4. **Linux permissions**: `sudo usermod -aG dialout $USER` then re-login.
5. **ESP32 won't enter bootloader**: hold BOOT while esptool prints `Connecting...`, release after `Chip is ESP32...`. If never: missing auto-reset circuit or board needs BOOT held through whole flash.
6. **Drop baud**: 921600 → 460800 → 115200. Hubs and long cables hate high baud.
7. **Wrong offset / chip flag**: ESP32-S3/C3 flash at 0x0 not 0x1000; `--chip auto` usually right but verify with `chip_id`.
8. **Nano clone**: try `-b 57600` (old bootloader).
9. **Pico invisible**: BOOTSEL held while plugging? Drive `RPI-RP2` mounted? If drive appears then vanishes during copy → bad cable or full drive (wrong UF2 family — e.g., RP2350 UF2 on RP2040 silently fails).
10. **Flashes OK but boot loops**: read serial at 115200 for reset cause (§9). `invalid header` = wrong offset. `Brownout` = power. Guru Meditation = code.
11. **MicroPython unresponsive after deploy**: main.py hard loop → safe-mode button / Ctrl-C spam during reset / erase_flash.
12. **Worked yesterday, dead today, no serial output at all, gets warm**: shorted board (student wiring 5V→3V3 or GPIO→GND with motor stall current). Retire it; don't sink time.

## 12. Mistakes Everyone Makes (Summary)

- Charge-only USB cables in the classroom cable bin.
- Flashing ESP32-S3 at 0x1000.
- String version comparison ("10" < "9").
- Skipping `erase_flash` when switching between Arduino C++ and MicroPython on the same ESP32 (leftover NVS/partitions cause ghost bugs).
- Letting students edit boot.py — keep safe-mode logic there and deploy only app.py/main.py.
- OTA without rollback marking: one bad release bricks-by-WiFi the entire fleet simultaneously. Dual partition + `esp_ota_mark_app_valid_cancel_rollback()` after self-test, always.
- Uploading version.txt before firmware.bin on the update server.
- 30 robots polling the OTA server at the same second — add jitter.
- Debugging the broken robot during class instead of swapping a spare.
- Touching AVR fuses. Ever.
