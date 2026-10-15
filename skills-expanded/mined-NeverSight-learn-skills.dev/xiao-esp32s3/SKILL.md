---
name: xiao-esp32s3
description: >
  Operate a Seeed XIAO ESP32S3 board with arduino-cli on Windows: install the
  core, compile, upload, read serial output, and run verified examples (blink,
  serial, touch, ADC, PWM, WiFi scan/AP, BLE, deep sleep). Use this skill
  WHENEVER the task involves an ESP32S3 / XIAO board, arduino-cli, flashing a
  sketch, reading the serial monitor, COM ports, or any embedded/Arduino work
  — even for a "simple" LED change. It contains verified commands and known
  pitfalls (DTR reset, deep-sleep USB drop, PSRAM flag) that prevent wasted
  debugging time.
license: MIT
compatibility: Windows + PowerShell 5.1, arduino-cli >= 1.x, esp32 core 3.x
---

# XIAO ESP32S3 via arduino-cli (Windows)

Everything below was verified on real hardware (esp32 core 3.3.10, 2026-07).
Follow it literally and you will not need to troubleshoot.

Paths below are relative to this skill's folder. `<PORT>` is the board's COM
port and `<SKETCH_DIR>` is a sketch folder in the user's workspace.

## One-time setup (skip any step that is already true)

```powershell
arduino-cli version                          # confirm arduino-cli exists
arduino-cli core list                        # is esp32:esp32 3.x installed?
# if not (this downloads ~1 GB and can take several minutes — use a long timeout):
arduino-cli core update-index
arduino-cli core install esp32:esp32
```

## Finding the board

```powershell
arduino-cli board list
```

The XIAO usually shows as an unidentified "Serial Port (USB)" — that row's
port (e.g. `COM4`) is `<PORT>`. If NO port appears: the board may be in deep
sleep (port only exists while awake — see pitfall 2), or needs bootloader
mode (hold the BOOT button while plugging in USB; port number may change).

## Standard workflow

```powershell
# sketch layout rule: folder name and .ino name must match:  my_sketch\my_sketch.ino

# compile (first compile of a session takes 1-3 min; cached after)
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32S3 <SKETCH_DIR>

# upload
arduino-cli upload -p <PORT> --fqbn esp32:esp32:XIAO_ESP32S3 <SKETCH_DIR>

# read serial for 10 s (NEVER `arduino-cli monitor` — it blocks forever)
powershell -File scripts\read_serial.ps1 -Port <PORT> -Seconds 10

# optional: send a line to the board and read the response
powershell -File scripts\read_serial.ps1 -Port <PORT> -Seconds 10 -Send "hello"
```

PowerShell 5.1 has no `&&`. Chain with `;` or `if ($?) { ... }`.

## Verified example sketches

`assets/sketches/` contains 11 sketches that all compiled, uploaded, and ran
on real hardware. Copy the closest one into the user's workspace as a
starting point instead of writing from scratch. See `references/examples.md`
for what each proves and its expected output.

## Sketch rules that prevent bugs

- `Serial.begin(115200);` then `delay(3000);` before the first print — USB CDC
  needs time to enumerate, otherwise early output is silently lost.
- The user LED is `LED_BUILTIN` (GPIO21) and is **inverted**: `LOW` = ON,
  `HIGH` = OFF. `analogWrite(LED_BUILTIN, 0)` = full brightness.
- ADC: call `analogReadResolution(12)`; read raw with `analogRead(A0)` and
  millivolts with `analogReadMilliVolts(A0)`. A floating pin reads noisy
  60–160 raw — that is normal, not a bug.
- Touch: `touchRead(T2)` (T2 = GPIO2 = pin D1). Baseline ≈ 17,500; the value
  RISES well above 40,000 when touched (opposite of original ESP32).
- `WiFi.macAddress()` returns `00:00:00:00:00:00` until WiFi is started with
  `WiFi.mode(WIFI_STA)` — not an error.
- Networking in core 3.x: use `NetworkClient` / `NetworkServer`
  (old `WiFiClient` / `WiFiServer` names may not exist).

## Pin map (XIAO ESP32S3)

| Label | GPIO | Notes |
|-------|------|-------|
| D0 | 1 | A0, touch T1 |
| D1 | 2 | A1, touch T2 |
| D2 | 3 | A2, touch T3 |
| D3 | 4 | A3, touch T4 |
| D4 | 5 | SDA, touch T5 |
| D5 | 6 | SCL, touch T6 |
| D6 | 43 | UART TX (Serial1) |
| D7 | 44 | UART RX (Serial1) |
| D8 | 7 | SPI SCK |
| D9 | 8 | SPI MISO |
| D10 | 9 | SPI MOSI |
| user LED | 21 | inverted (LOW = on) |

## Known pitfalls — read before "debugging"

1. **Opening the COM port resets the board** (DTR toggle → `rst:0x15
   USB_UART_CHIP_RESET`). Every serial read starts from a fresh boot. This
   also wipes `RTC_DATA_ATTR` variables, so you cannot observe deep-sleep
   boot counts through a serial monitor. It is not a crash.
2. **Deep sleep makes the COM port disappear.** USB CDC powers down during
   sleep, so the port vanishes and Windows plays disconnect/connect sounds
   every cycle. This is normal and is the correct evidence that sleep works.
   Verify the cycle with `scripts\watch_port.ps1 -Port <PORT>` (logs
   appear/disappear timestamps) instead of opening the port. To reflash a
   sleeping board, catch the short awake window, or hold the BOOT button
   while plugging USB (bootloader mode; the port number may change).
3. **`arduino-cli monitor` never exits.** In an automated session it hangs
   your shell. Always use `scripts\read_serial.ps1`, which has a deadline.
4. **PSRAM reads 0 bytes by default.** The default build has PSRAM disabled.
   If a sketch needs PSRAM (camera, big buffers), add
   `--board-options PSRAM=opi` to BOTH compile and upload commands.
5. **`netsh wlan show networks` is cached** and may not show a SoftAP the
   board just created. Trust the board's serial output ("AP IP address:
   192.168.4.1"); test the AP from a phone instead.
6. **Upload fails / port busy**: make sure no serial reader is still running
   (only one process can hold the port). If the board looks bricked, use
   bootloader mode (pitfall 2).
7. **First compile is slow** (cold cache, big toolchain). Do not kill it
   before ~3 minutes; use a generous timeout.
8. **Board can get stuck in reset after a serial session** (only the ROM
   banner `ESP-ROM:esp32s3-...` prints, app never boots, SoftAP/servers die).
   Cause: DTR/RTS line state left by the PC when closing the port. Recover
   with `arduino-cli upload` (esptool's reset sequence fixes it). If a
   headless demo (web server etc.) must keep running, avoid opening the
   serial port at all — use mDNS or the router's DHCP table to find the
   board instead of reading its IP over serial.
9. **Same-name Edge Impulse library swap needs `--clean`.** Replacing the
   `<project>_inferencing` library with a rebuilt copy (same version) leaves
   stale objects in arduino-cli's cache — symptoms: `objs.a ... is not an
   object` link errors or edits that appear to have no effect. Always pass
   `--clean` on the first compile after swapping the library.

## Verifying without human eyes

- LED/PWM: also print state to serial each cycle so the log proves behavior.
- WiFi scan / BLE scan: success = a numbered list of networks/devices.
- SoftAP: success = serial prints the AP IP; full HTTP test needs a phone.
- Deep sleep: success = `watch_port.ps1` shows a stable disappear/appear
  cycle matching the programmed sleep time (+ ~3 s awake).
