---
name: xiao-i2c-sensors
description: >
  Bring up I2C sensors on a XIAO ESP32S3 and stream their values to serial:
  BH1750 ambient light, BME280 temperature/pressure/humidity, and BNO055 9-DOF
  fused orientation, individually as unit tests or all three together on one
  bus. Use this skill WHENEVER the task involves I2C sensors on an ESP32S3 —
  wiring one up, "센서 값 읽어줘", a sensor that answers the scan but reads
  zeros, unit-testing a module before trusting it, deciding whether a 0x76
  part is a BME280 or a BMP280, or a BNO055 whose orientation stays at 0.
  It carries hardware-verified sketches and the address/clock traps that make
  a healthy-looking sensor return nothing.
license: MIT
compatibility: Windows + PowerShell 5.1, arduino-cli >= 1.x, esp32 core 3.x
---

# I2C sensors on the XIAO ESP32S3

Bus pins are fixed by the board: **SDA = D4 = GPIO5**, **SCL = D5 = GPIO6**.
`Wire.begin(D4, D5)` — the no-argument form picks the wrong pins.

Read the `xiao-esp32s3` skill for the compile/upload workflow, and
`xiao-serial-monitor` for watching the output.

## Always scan before writing driver code

Module silkscreens lie and address straps vary between clones. One scan
settles both, and everything downstream depends on being right about it:

```powershell
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32S3 -u -p <PORT> assets\sketches\i2c_scan
```

`i2c_scan` prints every responding address, guesses the part, and then reads
the ID register of anything at 0x76 and 0x29 so the guess becomes a fact.
Verified output on the reference board:

```
  0x23  BH1750 (ADDR=L)
  0x29  BNO055 (ADDR=H)
  0x76  BME280/BMP280 (SDO=L)
  0x76 chip id = 0x60  -> BME280
  0x29 chip id = 0xA0  -> BNO055
```

## Sketches

| Sketch | What it does |
|---|---|
| `assets/sketches/i2c_scan` | scan + chip-ID identification |
| `assets/sketches/test_bh1750` | BH1750 unit test, 5 automated checks |
| `assets/sketches/test_bme280` | BME280 unit test, 8 automated checks |
| `assets/sketches/test_bno055` | BNO055 unit test, 10 automated checks |
| `assets/sketches/sensors_all` | all three streaming together, 1 Hz |

Copy the one you need into the user's workspace (folder name must match the
`.ino` name) rather than writing a driver from scratch. All five were run on
real hardware; the unit tests all pass at 5/5, 8/8, 10/10.

Libraries:

```powershell
arduino-cli lib install "BH1750"
arduino-cli lib install "Adafruit BME280 Library"
arduino-cli lib install "Adafruit BNO055"
```

`sensors_all` output, one line per second:

```
lux     48.3 | 25.86C 1006.31hPa  42.7%RH | H  359.9 R    7.9 P   -5.2 | cal 1300
```

`cal` is the BNO055's four calibration bytes (sys/gyro/accel/mag), each 0–3.

## Handing the stream to the user

A sensor stream is something the user watches, not something you screenshot
once. Verify it yourself with a bounded read, then tell them how to open it
themselves — the `xiao-serial-monitor` skill covers both halves:

```powershell
.\scripts\mon.ps1 -Seconds 15    # your check; returns
mon                              # theirs; runs until Ctrl+C
```

Never launch the interactive monitor from a tool call — it never returns and
the session hangs. Close instead with a handoff that names the command, how to
run it, and how to stop it:

> 센서 값이 1초마다 흐르고 있습니다. 직접 보시려면:
> ```
> ! D:\path\to\mon.ps1
> ```
> Claude Code에서 `!` 를 붙이면 이 세션에서 바로 실행됩니다. Ctrl+C로 종료.
> 프로필 단축키를 넣으셨다면 새 터미널에서 `mon` 만 쳐도 됩니다.

This matters more for sensors than for most things: the interesting part is
what happens when the user covers the light sensor, breathes on the humidity
sensor, or rotates the IMU. None of that shows up in a capture you took while
the board sat still on a desk.

## How these unit tests are built

Two rules make the difference between a test that proves something and a test
that just prints numbers:

**Bounds-check, don't eyeball.** Every reading is asserted against the
datasheet range, because the failure that actually happens is a dead bus
returning `0`, `NaN`, or a pegged rail — not a part that is 2 % out of
calibration. The strongest single check in the set is the BNO055's gravity
magnitude: however the board is lying, `|g|` must come out near 9.8 m/s², so
one assertion covers all three accelerometer axes and their scaling at once.

**Never assert something that needs a human hand.** An early version of the
BH1750 test asserted that consecutive readings differ, reasoning that a frozen
bus repeats itself. Under steady room light a healthy sensor returns exactly
46.7 lx every time, so the test failed on working hardware whenever nobody
happened to be waving at it. Checks that need physical stimulus — covering the
light sensor, breathing on the humidity sensor, moving the IMU to calibrate —
belong in a printed "manual check" section that is not scored. Keep the
automated count honest and it stays worth reading.

## Pitfalls

These each cost a debugging session once.

1. **A BNO055 at 0x29 will not talk to the default driver.** The Adafruit
   library constructor defaults to 0x28; a module with ADDR/COM3 strapped high
   sits at 0x29 and `begin()` fails while the scan shows the device plainly.
   Pass it explicitly: `Adafruit_BNO055 bno(55, 0x29, &Wire);`

2. **`setExtCrystalUse(true)` silently zeroes the BNO055.** Many clone modules
   have no 32 kHz crystal fitted, and selecting an absent clock source parks
   the chip in idle with every output stuck at `0.00` — temperature, gravity,
   euler angles, all of it. The trap is that it still looks healthy: the
   power-on self test reports `0x0F` and `system_error` stays `0`. Leave it on
   the internal oscillator unless you have confirmed the crystal exists.

   Guard against it by checking the mode rather than the self test:

   ```cpp
   uint8_t sysStat, selfTest, sysErr;
   bno.getSystemStatus(&sysStat, &selfTest, &sysErr);
   // 5 = sensor fusion algorithm running. Anything else and the
   // orientation numbers are not real, whatever self_test says.
   ```

3. **0x76 does not mean BME280.** BMP280 shares the address and has no
   humidity channel, so a humidity read returns garbage rather than an error.
   Read chip-ID register `0xD0`: `0x60` = BME280, `0x58` = BMP280,
   `0x61` = BME680, `0x55` = BMP180. Decide the driver from that, not the
   module's label.

4. **BH1750 needs ~120 ms after `begin()` before the first conversion.**
   Reading immediately returns a stale or zero value that looks like a wiring
   fault. The tests wait 200 ms.

5. **One missing module should not silence the others.** In `sensors_all`
   each sensor is probed independently and a missing one is reported once at
   startup, then skipped. A single loose wire otherwise takes the whole stream
   down and sends you looking for a software bug.

6. **Keep serial output ASCII.** The Windows console reads the port as the
   ANSI codepage, so Korean or accented text in `Serial.print` comes back as
   mojibake in captured logs. Put the explanation in comments, keep the
   printed strings English.

## Adding another I2C sensor

Scan first and confirm the address; identify the part from its ID register
where one exists; bounds-check every reading against the datasheet; and keep
any check that needs a human hand out of the automated score. That is the
whole method — the five sketches here are just instances of it.
