---
name: esp32-serial-diag
description: ESP32 serial diagnostics in non-TTY environments — pyserial workarounds
  for pio device monitor / arduino-cli monitor failures, DTR/RTS soft-reset, boot
  log interpretation, and OLED I2C 4-pin label disambiguation. Use when verifying
  ESP32 firmware liveness from Hermes terminal, docker, SSH pipe, or any non-interactive
  context where pio device monitor crashes with termios.error.
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- esp32
- serial
- pyserial
- platformio
- oled
- i2c
- diagnostics
- non-tty
related_skills:
- exploit-development
---

# ESP32 Serial Diagnostics (Non-TTY Environments)

## Trigger

- You need to read ESP32 serial output from Hermes terminal (docker, SSH pipe, background process)
- `pio device monitor` or `arduino-cli monitor` crashed with `termios.error`
- You need to soft-reset an ESP32 and read the boot log without physical access to the EN button
- User asks about OLED pin labels (e.g. "my OLED only has GND VDD SCK SDA")
- You need to verify firmware is running on an ESP32 that has no Serial.print output
- nRF24 `radio.begin()` returns FAIL and you need to diagnose SPI bus / hardware vs software
- Multiple nRF24 modules on shared SPI bus all report FAIL

## The Core Problem

PlatformIO's `pio device monitor` and Arduino CLI's `monitor` both try to open a TTY terminal session. In non-TTY environments (Hermes terminal, docker container, SSH pipe, subprocess), `termios.tcgetattr()` fails:

```
termios.error: (19, 'Operation not supported by device')
```

**Solution**: Always use `pyserial` directly via `python3 -c "..."`. Never attempt `pio device monitor` or `arduino-cli monitor` from Hermes terminal.

## Method A: Read-Only Serial (firmware already running)

```bash
python3 -c "
import serial, time
ser = serial.Serial('/dev/cu.usbserial-210', 115200, timeout=1)
buf = b''
start = time.time()
while time.time() - start < 12:
    if ser.in_waiting:
        buf += ser.read(ser.in_waiting)
    else:
        time.sleep(0.15)
ser.close()
print(buf.decode('utf-8', errors='replace')[:1500])
"
```

## Method B: Soft-Reset + Boot Log (no EN button needed)

Toggle DTR/RTS via pyserial to reset the ESP32 — equivalent to pressing EN:

```bash
python3 -c "
import serial, time
ser = serial.Serial('/dev/cu.usbserial-210', 115200, timeout=1)
time.sleep(0.3)
ser.dtr = True; ser.rts = True    # EN low = reset hold
time.sleep(0.1)
ser.dtr = False; ser.rts = False   # release reset = boot
time.sleep(0.5)
buf = b''; start = time.time()
while time.time() - start < 10:
    data = ser.read(4096)
    if data: buf += data
    else: time.sleep(0.05)
ser.close()
print(buf.decode('utf-8', errors='replace'))
"
```

## Boot Log Interpretation

| Pattern | Meaning | Action |
|---------|---------|--------|
| `boot:0x13 (SPI_FAST_FLASH_BOOT)` | ✅ Normal boot, firmware loaded | Proceed |
| `boot:0x3 (DOWNLOAD_BOOT)` | ⚠️ GPIO0 held low, stuck in download mode | Check wiring — CSN pin may be pulling GPIO0 low |
| `E (xxx) psram: PSRAM ID read error: 0xffffffff` | ℹ️ Normal for ESP32-D0WD-V3 (no PSRAM) | Ignore |
| `No bootable app partitions` | ❌ Flash corrupted / interrupted | Re-flash |
| Boot log then silence | ✅ Normal — firmware running, no Serial.print in setup() | Verify via OLED or heartbeat patch |

### When silence after boot is normal

Many ESP32 firmware projects (RF Jammer, jammers, sensor nodes) only call `Serial.begin(115200)` in setup() without any `Serial.print()`. The UI is entirely on OLED or physical indicators. Absence of serial output after the boot log does NOT mean firmware isn't running.

To confirm `loop()` is alive, inject a heartbeat:
```cpp
// Add at top of loop():
static uint32_t _hb = 0;
if (millis() - _hb > 5000) {
  Serial.println(F("[DIAG] Heartbeat"));
  _hb = millis();
}
```
Re-compile, flash, and watch for "[DIAG] Heartbeat" every 5 seconds. Revert after diagnosis.

## OLED I2C 4-Pin Label Disambiguation

Cheap SSD1306 OLED modules use non-standard pin labels. The same I2C bus has multiple naming conventions:

| Module Label | Standard Name | Meaning | ESP32 GPIO |
|--------------|--------------|---------|------------|
| VCC / VDD | VCC | Power positive | 3.3V (⚠️ NOT 5V for SSD1306) |
| GND | GND | Ground | GND |
| SCL / SCK | SCL | I2C clock | GPIO 22 |
| SDA | SDA | I2C data | GPIO 21 |

**Critical confusion point**: On a 4-pin I2C OLED, **SCK = SCL** (I2C clock), NOT SPI clock. This trips up users who associate SCK with SPI.

**How to identify I2C vs SPI OLED**:
- **4 pins** (GND/VDD/SCK/SDA or GND/VCC/SCL/SDA) → I2C, use table above
- **7 pins** (GND/VCC/D0/D1/DC/CS/RESET) → SPI, different wiring entirely
- **7 pins** (GND/VCC/SCK/MOSI/DC/CS/RESET) → SPI with standard SPI labels

When the user says "my OLED only has GND VDD SCK SDA", it's an I2C OLED with variant labels. Map VDD→3.3V, SCK→GPIO22(SCL), SDA→GPIO21.

## ESP32 D0WD-V3 Specific Notes

- **No PSRAM**: `E (xxx) psram: PSRAM ID read error: 0xffffffff` in boot log is normal
- **Flash mode**: Must use DIO (not QIO) — `board_build.flash_mode = dio` in platformio.ini
- **Upload baud**: 460800 generally works; 921600 may cause `Unable to verify flash chip connection` on some boards. Drop to 460800 if upload fails at 921600
- **USB-UART chip**: CP2102 (Silicon Labs) — DTR/RTS reset sequence works reliably

## Common Serial Ports

Check both:
```bash
ls /dev/cu.usbserial-* /dev/cu.SLAB_USBtoUART* /dev/cu.usbmodem* 2>/dev/null
```

- `/dev/cu.usbserial-*` → CP2102 (most ESP32 DevKit boards)
- `/dev/cu.SLAB_USBtoUART*` → CP2102 alternate name (older macOS drivers)
- `/dev/cu.usbmodem*` → CH340 (some clone boards)

## SPI Bus + nRF24 Hardware Diagnosis (Non-TTY)

When `radio.begin()` returns FAIL for all nRF24 modules on a shared SPI bus, use a raw SPI register read to distinguish software vs hardware problems. This is the fastest way to isolate the fault without a logic analyzer.

### Diagnostic Procedure

1. **Flash the diagnostic sketch** — see `references/spi-nrf24-diag.md` for the complete PlatformIO sketch. It toggles CSN/CE pins, does a raw `SPI.transfer()` read of the nRF24 CONFIG register (address 0x00), and reports `radio.begin()` status per radio.
2. **Interpret the CONFIG register value**:

| Raw CONFIG | Diagnosis | Action |
|------------|-----------|--------|
| 0xFF | MISO line not connected or nRF24 has no power | Check MISO wire, 3.3V supply, GND |
| 0x00 | MISO pulled LOW (short, broken wire, or nRF24 GND disconnected) | Check MISO wire continuity, check nRF24 GND |
| 0x08 | nRF24 alive, power-down mode | Software issue — check `SPI.begin()` ordering |
| 0x0C | nRF24 alive, standby mode | Software issue — check `SPI.begin()` ordering |

3. **If GPIO toggle OK but CONFIG = 0x00/0xFF**: the ESP32 pins work but SPI bus is dead — hardware problem (wiring, power, GND), not software.
4. **Isolate by testing one radio at a time**: disconnect all nRF24 modules, connect only Radio A with a 10µF cap across VCC-GND, re-run. If A passes, add B. If A still fails, the problem is wiring or power to that specific radio.

### Shared SPI Bus Init Order (multiple nRF24 on one VSPI bus)

When multiple nRF24 modules share one SPI bus, initialization order is critical:

**CORRECT** (CSN HIGH before SPI.begin):
1. Set ALL CSN pins → OUTPUT + HIGH (deselect all slaves)
2. Set ALL CE pins → OUTPUT + LOW
3. `delay(10)`
4. `SPI.begin(SCK, MISO, MOSI)` — AFTER CSN pins are HIGH
5. `delay(10)`
6. `RadioA.begin()` then `RadioA.powerDown()` — CSN_B/CSN_C already HIGH
7. `RadioB.begin()` then `RadioB.powerDown()`
8. `RadioC.begin()`

**WRONG** (causes all-FAIL): `SPI.begin()` before CSN pins set HIGH → bus noise on MISO → all `begin()` calls fail.

**Key**: `SPI.begin(18, 19, 23)` must come AFTER all CSN pins are HIGH. RF24's internal `SPI.begin()` is not sufficient when CSN pins are already configured as OUTPUT — the explicit `SPI.begin()` after CSN-HIGH is the reliable sequence.

### GPIO Strapping Pins to Avoid for nRF24 CSN

ESP32 strapping pins have boot-time requirements that conflict with nRF24 CSN's idle-HIGH requirement:

| GPIO | Strapping | CSN-safe? | CE-safe? |
|------|-----------|-----------|----------|
| 0 | Bootstrap (LOW = download) | ❌ | ❌ |
| 2 | Must be LOW at boot | ❌ (CSN idle=HIGH conflicts) | ⚠️ (CE idle=LOW=OK) |
| 5 | Must be HIGH at boot | ⚠️ (CSN idle=HIGH = OK) | ❌ |
| 12 | Must be LOW | ❌ | ⚠️ |
| 13 | Normal | ✅ | ✅ |
| 15 | Must be LOW | ❌ | ✅ (CE idle=LOW=OK) |
| 17 | Normal | ✅ | ✅ |

**GPIO 2 as CSN is the #1 cause of RadioC FAIL** — CSN needs idle HIGH but GPIO 2 must be LOW at boot. The CSN pull-up to VCC fights the strapping requirement. Use GPIO 13 instead.

## Pitfalls

1. **Never use `pio device monitor` from Hermes terminal** — it will crash with `termios.error: (19)`. Always use pyserial.

2. **DTR/RTS reset sequence matters** — different USB-UART chips may map DTR/RTS to different ESP32 pins. CP2102 standard: RTS→EN, DTR→GPIO0. If Method B doesn't produce boot log, try swapping DTR and RTS in the sequence.

3. **`boot:0x3 (DOWNLOAD_BOOT)` means a GPIO is held LOW** — On ESP32, GPIO0 (boot pin) must be HIGH at boot. If using GPIO2 as CSN for an nRF24, ensure the nRF24's CSN pull-up isn't interfering. GPIO2 and GPIO15 also have boot strapping functions.

4. **Upload at 921600 can fail intermittently** — Error: `Unable to verify flash chip connection (Packet content transfer stopped)`. Drop to 460800 in platformio.ini: `upload_speed = 460800`.

5. **OLED SCK ≠ SPI SCK** — On 4-pin I2C OLEDs, the SCK pin is I2C clock (SCL → GPIO22), NOT the SPI SCK pin (GPIO18). This is the #1 wiring confusion for ESP32 + OLED projects.

6. **Raw SPI register reads are unreliable before `radio.begin()`** — `SPI.transfer()` to read nRF24 CONFIG (0x00) before RF24 `begin()` will return 0x00 even on healthy modules, because the RF24 library's `begin()` performs full SPI mode initialization. **Always use `radio.begin()` return value as the pass/fail criterion**, not raw SPI reads. Raw reads of 0x00 do NOT prove the module is dead.

7. **Never change firmware pin definitions without ensuring the physical wire has been moved first** — If you change `NRF_CSN_PIN_C` from GPIO 2 to GPIO 13 in `config.h` but the user hasn't moved the wire, ALL radios may FAIL (not just the one you changed), because the SPI bus state gets corrupted by the mismatched CSN pin. Correct sequence: (1) tell user to move the wire → (2) user confirms done → (3) then change firmware → (4) compile-flash-verify. Skipping step 1-2 turns a 1-radio problem into a 3-radio outage.

8. **Pin-swap diagnostic methodology for persistent Radio FAIL** — When a specific radio (e.g. Radio C) fails `begin()` regardless of which CE/CSN pin combination you try (test 4+ combos like CE={15,14,27} × CSN={13,2}), while other radios on the same SPI bus pass, the problem is hardware-level: either the module's VCC/GND/MISO wire is loose, or the module itself is dead. No amount of firmware changes will fix this. Tell the user to check: (a) nRF24 VCC 3.3V, (b) GND continuity, (c) MISO wire from that module to the shared bus, (d) try swapping the module with a known-good one.

## Related Skills

- `esp32-embedded-development` — Full ESP32 firmware authoring, compile-flash-verify workflow
- `esp32-jammer-diag` — Jammer-specific diagnostics (nRF24 register dump, RPD cross-test, flash recovery)
- `RF Jammer-master` — RF Jammer v2 multi-protocol jammer (3× nRF24, OLED menu, 8 attack modes)
- `esp32-nrf24-jammer-builder` — ESP32 + dual nRF24 jammer hardware builder
