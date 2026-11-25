---
name: m5stack-cores3
description: "Use when writing firmware for M5Stack CoreS3 / CoreS3 SE (ESP32-S3 dev kit with screen) — Grove port wiring, M5 MicroPython/UIFlow2 APIs, Arduino M5Unified, AXP2101 power chip gotchas, and the M5 Unit ecosystem. Provides exact pin maps, I2C addresses, power rails, working code patterns, and debugging checklists so hardware code works first try."
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


# M5Stack CoreS3 / CoreS3 SE — Expert Firmware Knowledge

## 1. Hardware Identity — know exactly which board you have

| Property | CoreS3 | CoreS3 SE |
|---|---|---|
| MCU | ESP32-S3 (dual-core LX7 @ 240 MHz) | same |
| Flash / PSRAM | 16 MB flash / 8 MB PSRAM (octal) | 16 MB / 8 MB |
| Screen | 2.0" IPS 320×240, ILI9342C, capacitive touch (FT6336U) | same |
| Camera | GC0308 (0.3 MP) | **none** |
| Mic | dual ES7210 ADC mics | single mic |
| RTC | BM8563 | BM8563 |
| IMU | BMI270 + BMM150 mag | BMI270 (no magnetometer on most SE units) |
| Battery | 500 mAh internal | **none internal** (battery bottom optional) |
| Proximity | LTR-553ALS (light/prox) | none |
| USB | USB-C, native USB-OTG (S3) + no separate UART chip | same |

Critical implication: **the CoreS3 SE has no internal battery** — it dies instantly on USB unplug unless a battery base (e.g., Battery Bottom2) is attached. Don't write "low battery" logic assuming a battery exists.

The ESP32-S3 has **no DAC** (unlike original ESP32). Audio out goes through the **AW88298 I2S amplifier** to the built-in 1 W speaker. Never use `dac` APIs.

## 2. Grove Ports — wiring tables (the #1 source of mistakes)

Three HY2.0-4P (Grove) ports on the bottom edge. Colors and roles:

| Port | Color | Role | Pin 1 (signal) | Pin 2 (signal) | Pin 3 | Pin 4 |
|---|---|---|---|---|---|---|
| **Port A** | Red | I2C (external) | **G1 = SCL** | **G2 = SDA** | 5V | GND |
| **Port B** | Black | GPIO / ADC | **G8** (in) | **G9** (out) | 5V | GND |
| **Port C** | Blue | UART | **G18 = RXD** | **G17 = TXD** | 5V | GND |

Memorize the cable color code on the Grove lead: **yellow = pin 1, white = pin 2, red = 5V, black = GND**.

So on Port A: yellow wire = SCL (G1), white wire = SDA (G2). This is **reversed vs. original M5Stack Core/Core2** where Port A was G22/G21 — never copy old Core pin numbers.

### Internal vs external I2C — two separate buses
- **Internal bus (I2C0)**: G11 = SCL, G12 = SDA. Hosts AXP2101 (0x34), AW9523 (0x58), FT6336U touch (0x38), BM8563 RTC (0x51), BMI270 (0x69), AW88298 amp (0x36), ES7210 (0x40/0x41... varies).
- **External Grove Port A (I2C1)**: G1 = SCL, G2 = SDA. This is where Units plug in.
- **NEVER scan or write blindly to the internal bus.** Writing wrong registers to the AXP2101 (0x34) can cut power to the screen or brown out the board.

In M5 MicroPython, `M5.begin()` configures the internal bus; for Port A units use:
```python
from machine import I2C, Pin
i2c1 = I2C(1, scl=Pin(1), sda=Pin(2), freq=100000)  # Port A
print(i2c1.scan())  # expect e.g. [104] for MPU-style unit at 0x68
```
Start at 100 kHz. Many Grove units (especially with long daisy-chained cables) fail at 400 kHz. Only raise to 400 kHz after the scan is stable.

### Port voltage facts
- Grove ports supply **5 V** on the red wire (boosted from USB/battery), but **GPIO logic is 3.3 V**. Units are designed for this (5 V power, 3.3 V signaling).
- Max combined 5 V Grove output: budget ~500 mA from USB; heavy loads (servo units, NeoPixel strips) need the DC 5 V input or an external supply.
- Port B G8/G9 are also usable as ADC (ADC1 channels). ADC range with 11 dB attenuation ≈ 0–3.1 V, NOT 5 V. Divider needed for 5 V analog signals.

### M-Bus (bottom 30-pin bus)
Stacking modules (Battery Bottom, Servo module, LAN module) use the M-Bus. Pins of note: G35/G36/G37 are SPI (shared with LCD — do not repurpose), G6/G7 free GPIO on some bases. Check the module's schematic; M-Bus pin conflicts with the LCD SPI are the classic "screen goes white when I init my module" bug.

## 3. Power: AXP2101 PMU gotchas (read before anything battery/peripheral related)

The CoreS3 uses an **AXP2101** PMU plus an **AW9523B** GPIO expander on the internal I2C bus. Together they gate power to nearly everything:

| Rail / expander pin | Controls |
|---|---|
| AXP2101 ALDO3 | 3.3 V to camera + sensors |
| AXP2101 ALDO4 | TF card + peripherals (3.3 V) |
| AXP2101 BLDO1 | AW88298 speaker amp power |
| AXP2101 BLDO2 | LCD backlight rail (brightness via AXP, not PWM pin!) |
| AXP2101 DLDO1 | LCD logic / touch |
| AW9523 P0_x / P1_x | Bus power enable, camera reset, speaker enable, **boost 5 V enable for Grove** |

Gotchas, in order of how often they bite:

1. **Screen brightness is NOT a PWM GPIO.** It's the AXP2101 BLDO2 voltage. Use `M5.Lcd.setBrightness(0-255)` (M5Unified/M5 MicroPython) — never try `ledcWrite` on a backlight pin; there isn't one.
2. **`M5.begin()` (or `M5.config()` + begin in Arduino) MUST run first.** It programs the AXP2101 rails. Skip it and: screen stays black, speaker silent, SD card invisible, Grove 5 V may be off. ~90% of "my CoreS3 is dead" reports are a sketch that never called begin.
3. **Grove 5 V can be switched off.** The boost enable goes through the AW9523. M5 firmware enables it in begin; if you bit-bang the AW9523 yourself you can kill power to all attached units.
4. **Battery charge current default is conservative** (~200 mA). Via M5Unified: `M5.Power.setBatteryCharge(true)`; charge current setters exist but leave defaults unless you know the attached battery's rating.
5. **Power off / deep sleep**: `M5.Power.powerOff()` actually cuts rails via AXP. `M5.Power.timerSleep(seconds)` uses the BM8563 RTC to wake. Plain `esp_deep_sleep_start()` leaves AXP rails up → sleep current is tens of mA instead of ~2 mA. Always go through `M5.Power`.
6. **Reading battery**: `M5.Power.getBatteryLevel()` → 0–100; `M5.Power.getBatteryVoltage()` → mV. On a CoreS3 SE without battery these return junk (often 0 or stale) — guard with `M5.Power.getBatteryLevel() >= 0 and isCharging` logic rather than trusting one read.
7. **USB current**: the board can draw >500 mA peaks with WiFi TX + screen + speaker; on weak USB ports this resets the board mid-WiFi-connect. Symptom: reboot exactly when `WiFi.begin()` runs. Fix: better cable/port or attach battery.

## 4. UIFlow2 vs raw MicroPython vs Arduino — choose deliberately

| Option | What it is | Use when |
|---|---|---|
| **UIFlow2 firmware** (M5 MicroPython) | M5's MicroPython fork with `M5` module baked in; flash via M5Burner; code via web IDE or any MPY tool (mpremote/Thonny) | Default for education / fast iteration. The `M5`, `Widgets`, `unit`, `hardware` modules only exist here. |
| **Vanilla MicroPython** | Generic ESP32-S3 build | Almost never — you lose all M5 drivers (AXP init, LCD, touch) and must reimplement PMU bring-up. Avoid. |
| **Arduino + M5Unified** | C++ lib `M5Unified` (+ `M5GFX`) | Performance, camera work, BLE-heavy apps, production firmware. |
| **ESP-IDF + M5Unified** | Same lib, IDF component | Advanced production. |

Rule: **UIFlow2 firmware = M5 MicroPython.** "UIFlow" the visual editor just generates this MicroPython. You can ignore blocks entirely and write Python against the same firmware. To get it: M5Burner → CoreS3 → UIFlow2.x firmware → flash at 921600 baud. After flashing, the REPL is available over USB (it's native USB-CDC; if the port vanishes after a crash, hold reset, or hold G0/BtnA-area boot button while plugging in to enter download mode).

Do not mix ecosystems in one answer: `from m5stack import lcd` is the **old Core/UIFlow1 API** and does not exist on CoreS3. The CoreS3 API is `import M5; from M5 import Lcd`.

## 5. M5 MicroPython (UIFlow2) — working patterns

### Minimal correct skeleton
```python
import os, sys, io
import M5
from M5 import Lcd, Speaker, Imu, Touch, Widgets

M5.begin()                 # MANDATORY first — inits AXP2101, LCD, touch, IMU
Widgets.fillScreen(0x222222)

label = Widgets.Label("Hello", 10, 10, 1.0,
                      0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

while True:
    M5.update()            # MANDATORY in loop — feeds touch/buttons/IMU
    if M5.Touch.getCount() > 0:
        x = M5.Touch.getX(); y = M5.Touch.getY()
        label.setText(f"{x},{y}")
```
Two non-negotiables: `M5.begin()` once, `M5.update()` every loop iteration. Without `M5.update()`, touch and the virtual buttons never register.

### Virtual buttons (CoreS3 has NO physical A/B/C buttons)
The bottom strip of the touch screen maps to BtnA/BtnB/BtnC:
```python
if M5.BtnA.wasPressed(): ...
if M5.BtnB.wasHold(): ...      # also: isPressed(), wasReleased(), wasClicked()
```
These only work after `M5.update()`. The left-side physical button is reset/power (hold 6 s = off when on battery), not readable from code.

### LCD direct drawing (M5GFX-style API)
```python
Lcd.fillScreen(0x000000)
Lcd.setTextColor(0x00FF00, 0x000000)
Lcd.setCursor(0, 0)
Lcd.print("line\n")
Lcd.drawCircle(160, 120, 50, 0xFF0000)
Lcd.fillRect(0, 200, 320, 40, 0x0000FF)
Lcd.drawImage("/flash/img.png", 0, 0)   # PNG/JPG/BMP from flash
Lcd.setRotation(1)   # 0-3; default 1 = landscape, USB on left
```
Colors are 24-bit `0xRRGGBB` ints in M5 MicroPython (converted internally to RGB565). Screen is 320×240 in default rotation.

For flicker-free animation use a canvas (sprite):
```python
cv = M5.Lcd.newCanvas(320, 240, 16)   # 16-bit color sprite in PSRAM
cv.fillScreen(0x000000)
cv.drawCircle(x, y, 10, 0xFFFFFF)
cv.push(0, 0)
```

### Speaker (I2S → AW88298, 1 W)
```python
Speaker.setVolumePercentage(0.6)         # 0.0–1.0; >0.8 distorts on the tiny driver
Speaker.tone(2000, 300)                  # freq Hz, duration ms — non-blocking
while Speaker.isPlaying(): pass          # wait if you need sequencing
Speaker.playWavFile("/flash/beep.wav")   # 16-bit PCM WAV; 8/16/22.05/44.1 kHz mono is safest
```
Mistakes: calling `tone()` back-to-back without checking `isPlaying()` truncates notes; WAVs above 44.1 kHz stereo stutter; speaker shares I2S with mic config — don't manually reconfigure I2S pins.

### IMU (BMI270)
```python
ax, ay, az = Imu.getAccel()    # in g; z ≈ +1.0 flat on table
gx, gy, gz = Imu.getGyro()     # deg/s
```
Tilt detection pattern: `pitch = math.degrees(math.atan2(ax, az))`. The BMI270 needs a few hundred ms after begin before readings settle — discard the first ~10 samples. There is no built-in AHRS in MicroPython; do complementary filtering yourself if you need stable angles.

### RTC (BM8563)
```python
from hardware import RTC8563   # UIFlow2
rtc = RTC8563()
rtc.setDateTime((2026, 6, 10, 2, 14, 30, 0))   # y,m,d,weekday,h,m,s
print(rtc.getDateTime())
```
The RTC keeps time when powered off (backed by main battery on CoreS3). For NTP: `import ntptime; ntptime.settime()` after WiFi, then copy into RTC.

### WiFi
```python
import network, time
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ssid", "pass")
t0 = time.ticks_ms()
while not wlan.isconnected():
    if time.ticks_diff(time.ticks_ms(), t0) > 15000:
        raise RuntimeError("wifi timeout")
    time.sleep_ms(200)
print(wlan.ifconfig())
```
ESP32-S3 is **2.4 GHz only**. A 5 GHz-only SSID fails silently in a connect loop — always timeout and report.

### Grove Units, the UIFlow2 way
UIFlow2 ships a `unit` package with drivers for the whole unit ecosystem:
```python
from hardware import I2C, UART
from unit import ENVUnit, ToFUnit, PIRUnit, RGBUnit, ServoUnit, UltrasonicI2CUnit

i2c1 = I2C(1, scl=1, sda=2, freq=100000)        # Port A
env = ENVUnit(i2c=i2c1, type=3)                  # ENV III (SHT30 0x44 + QMP6988 0x70)
print(env.read_temperature(), env.read_humidity(), env.read_pressure())

tof = ToFUnit(i2c1)                              # VL53L0X @ 0x29
print(tof.get_distance())                        # mm

pir = PIRUnit((8, 9))                            # Port B — digital in on G8
if pir.get_status(): ...

rgb = RGBUnit((8, 9), number=3)                  # NeoPixel SK6812 on Port B
rgb.set_color(0, 0xFF0000)
```
Pattern: I2C units take the I2C object (Port A); GPIO units take the pin tuple `(in_pin, out_pin)` = `(8, 9)` for Port B; UART units take port C pins `(18, 17)`.

## 6. Arduino / M5Unified — working patterns

`platformio.ini` that actually works:
```ini
[env:cores3]
platform = espressif32
board = m5stack-cores3
framework = arduino
monitor_speed = 115200
build_flags = -DBOARD_HAS_PSRAM -DARDUINO_USB_CDC_ON_BOOT=1
lib_deps = m5stack/M5Unified@^0.2.7
```
`ARDUINO_USB_CDC_ON_BOOT=1` is required or `Serial.print` goes nowhere (native USB).

```cpp
#include <M5Unified.h>

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);                       // AXP2101 + LCD + touch + IMU init
  M5.Display.setTextSize(2);
  M5.Display.setBrightness(128);
  M5.Speaker.setVolume(128);
}

void loop() {
  M5.update();                         // touch + virtual buttons
  if (M5.BtnA.wasPressed()) M5.Speaker.tone(2000, 100);

  auto t = M5.Touch.getDetail();
  if (t.wasPressed()) M5.Display.fillCircle(t.x, t.y, 5, GREEN);

  float ax, ay, az;
  if (M5.Imu.getAccel(&ax, &ay, &az)) { /* g units */ }
}
```
Use `M5Unified`, NOT the old `M5CoreS3` or `M5Stack` libraries — those have stale AXP code and conflict with M5Unified. `M5.Display` is an M5GFX `LGFX` — full sprite support:
```cpp
M5Canvas canvas(&M5.Display);
canvas.createSprite(320, 240);        // lives in PSRAM
canvas.fillSprite(BLACK);
canvas.drawString("60fps", 10, 10);
canvas.pushSprite(0, 0);
```

External I2C in Arduino: `Wire.begin(2, 1);  // SDA=G2, SCL=G1 — Port A`. `Wire1` is claimed by M5Unified for the internal bus; don't re-begin it.

UART Port C: `Serial2.begin(115200, SERIAL_8N1, 18, 17); // RX=G18, TX=G17`.

## 7. Unit ecosystem — I2C address map (collision avoidance)

Common Grove units and their fixed addresses on Port A:

| Unit | Chip | Addr |
|---|---|---|
| ENV III / ENV IV | SHT30/SHT40 + QMP6988/BMP280 | 0x44 + 0x70 / 0x76 |
| ToF | VL53L0X | 0x29 |
| Ultrasonic (I2C) | RCWL-9620 | 0x57 |
| TVOC/eCO2 | SGP30 | 0x58 ⚠ collides with internal AW9523 — fine, it's a different bus, but never wire it to internal I2C |
| Heart (MAX30100) | MAX30100 | 0x57 ⚠ collides with Ultrasonic |
| ADC Unit | ADS1100 | 0x48 |
| DAC Unit | MCP4725 | 0x60 |
| EXT.IO2 | STM32 | 0x45 |
| Joystick | custom | 0x52 |
| 8Servos / PCA9685-based | PCA9685 | 0x40 |
| PaHub (I2C hub) | PCA9548A | 0x70 ⚠ collides with QMP6988 (ENV III) |

Rules: (1) daisy-chaining I2C units is fine if addresses differ; (2) same-address units need a **PaHub**; (3) PaHub at 0x70 + ENV III's QMP6988 at 0x70 on the same root bus = broken — put the ENV unit behind the hub. Always `i2c.scan()` at startup and assert expected addresses before reading; a missing unit otherwise manifests as `OSError: [Errno 19] ENODEV` mid-run.

GPIO units (PIR, Dual Button, Relay, RGB LED, Vibrator) go on **Port B only** (G8 in, G9 out). UART units (GPS, Finger, CamS3-as-serial, LoRa) go on **Port C** (G18 RX, G17 TX). Plugging a UART unit into Port A does nothing and damages nothing — it just won't talk; check port assignment first when a unit is "dead."

Servo note: a single hobby servo's signal can run from G9 (Port B) but power it from the 5 V pin only for micro servos (<300 mA stall). Anything bigger: external 5–6 V supply, common ground, signal from G9.

## 8. Free GPIO budget (what you can actually use)

Pins exposed and safe: **G1, G2 (Port A), G8, G9 (Port B), G17, G18 (Port C), G5, G6, G7, G13, G14** (M-Bus, check base module conflicts). Reserved — do not touch: G35/36/37 (LCD SPI + PSRAM octal lines on S3!), G11/G12 (internal I2C), G0 (boot strap), G45/46 (straps). Repurposing G35–37 bricks the running firmware until reflash. ADC-capable among free pins: G8, G9 (ADC1). PWM (LEDC) works on any free GPIO.

## 9. Debugging checklist (run top to bottom)

1. **Black screen, no life** → Did the code call `M5.begin()` before anything else? Is the brightness set to 0? Try `M5.Lcd.setBrightness(200)`.
2. **No serial output (Arduino)** → `ARDUINO_USB_CDC_ON_BOOT=1` missing, or you opened the monitor before the native USB re-enumerated. Add `while(!Serial && millis()<3000);`.
3. **Port disappears / can't flash** → crashed firmware holding USB. Power off fully (hold reset/power 6+ s or unplug+battery off), then hold the BOOT (G0) button while plugging USB → download mode → flash.
4. **Touch/buttons never fire** → missing `M5.update()` in the loop.
5. **I2C unit ENODEV** → wrong port (unit on B/C instead of A), wrong bus (used internal G11/12), or address collision. Run `i2c.scan()` on bus 1 (G1/G2) and compare against the table above. Then drop freq to 100 kHz.
6. **Board reboots when WiFi starts** → USB power brown-out. Better cable/port, or battery attached. Watch for `rst:0x10 (RTCWDT_RTC_RESET)` in boot log.
7. **Speaker silent** → volume 0, or audio file format unsupported (must be PCM WAV), or another sketch reconfigured I2S. `Speaker.tone(2000,200)` is the minimal smoke test.
8. **High sleep current** → used raw esp deep sleep instead of `M5.Power.timerSleep()` / `M5.Power.deepSleep()`; AXP rails still on.
9. **SD card not found** → ALDO4 off (begin not called), or card >32 GB not FAT32. CS is G4, shared SPI with LCD — use M5's SD helpers, don't roll your own SPI init.
10. **IMU all zeros** → reading before init settled; wait 200 ms after begin, discard first samples. On SE, magnetometer calls fail — there is no BMM150.
11. **Unit works alone, fails daisy-chained** → bus capacitance. Shorten cables, drop to 100 kHz, or insert PaHub.
12. **Camera code on an SE** → no camera. `esp_camera_init` will fail; gate camera features on board detect.

## 10. Anti-patterns (things AIs/beginners always get wrong)

- Using old Core/Core2 pin numbers (G21/G22 I2C, G39 buttons). CoreS3 is a different pinout entirely.
- `from m5stack import lcd` / `lcd.print()` — UIFlow1 API, does not exist on CoreS3.
- PWM-ing a "backlight pin" — brightness is the AXP2101 BLDO2 rail.
- Polling physical BtnA/B/C GPIOs — they're touch-virtual; only `M5.BtnX` after `M5.update()` works.
- `dacWrite()` / `machine.DAC` — ESP32-S3 has no DAC; audio is I2S only.
- Assuming 5 V-tolerant GPIO — it's 3.3 V logic; 5 V sensor outputs need a divider.
- Writing to I2C 0x34 (AXP2101) directly "to set brightness" — use M5.Power/M5.Lcd APIs; raw writes can power-cycle rails.
- Blocking `time.sleep(10)` loops in MicroPython while expecting touch to respond — touch needs `M5.update()` cadence ≤ ~50 ms.
- Forgetting WiFi is 2.4 GHz only.
- Mixing `M5Unified` with legacy `M5CoreS3.h` in one Arduino project — duplicate AXP init, undefined behavior.
