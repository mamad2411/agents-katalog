---
name: imu-mpu6050
description: "Use when wiring or coding an MPU6050 (or MPU6500/9250-family) IMU for tilt sensing, balance robots, shake detection, or orientation. Covers I2C addressing, register-level init, gyro drift, complementary filter, vibration isolation, calibration, and the failure modes that wreck first attempts."
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


# MPU6050 IMU — Tilt, Orientation, Shake Detection

The MPU6050 is a 6-axis IMU: 3-axis accelerometer + 3-axis gyroscope on one die, I2C interface, built-in temperature sensor. It is the default IMU in hobby robotics (GY-521 breakout). It boots in SLEEP MODE and outputs garbage until you wake it — that single fact explains 50% of "my IMU returns zeros / -1 / 340" forum posts.

## Electrical & Wiring

### Voltage rules
- The MPU6050 **chip** is 3.3 V only (VDD 2.375–3.46 V). The **GY-521 breakout** has an onboard 3.3 V regulator (662K) so its VCC pin accepts 5 V.
- I2C lines: the GY-521 has 4.7 kΩ pull-ups to **3.3 V** on board. SDA/SCL from a 5 V Arduino works in practice because the AVR reads >0.6·Vcc... marginally. It works; it's not spec-clean. With ESP32/Pico (3.3 V logic) there is no issue at all.
- Current draw: ~3.8 mA full operation. Negligible — but power it from the MCU's 3.3 V/5 V rail, **never** from a rail shared with motors (see vibration/noise section).

### Wiring table

| GY-521 pin | Arduino Uno | ESP32 (default) | Raspberry Pi Pico (I2C0 default) | Notes |
|---|---|---|---|---|
| VCC | 5V | 3V3 | 3V3 (pin 36) | GY-521 regulator handles 5 V; bare chip = 3.3 V only |
| GND | GND | GND | GND | Common ground with MCU mandatory |
| SCL | A5 | GPIO22 | GP5 | |
| SDA | A4 | GPIO21 | GP4 | |
| XDA/XCL | — | — | — | Aux I2C for slave magnetometer; leave unconnected |
| AD0 | GND or float | GND or float | GND or float | LOW → 0x68, HIGH → 0x69 |
| INT | optional | optional GPIO | optional GPIO | Data-ready / motion interrupt; not needed for polling |

- **AD0 floating** reads as LOW on GY-521 (it has a pull-down) → address **0x68**. Tie AD0 to 3.3 V for **0x69** (lets you run two MPU6050s on one bus).
- Keep I2C wires < 20 cm at 400 kHz. Longer runs: drop to 100 kHz or add stronger pull-ups (2.2 kΩ).

### I2C identity check
Register 0x75 (WHO_AM_I) returns **0x68** regardless of AD0 (upper 6 bits of address). Clone chips sometimes return 0x98, 0x72, or 0x70 (that's actually an MPU6500/9250 — different registers for some features, same basics). If a library hard-fails on WHO_AM_I with a clone, patch the check, don't replace the board.

## Register-Level Init (what every library does under the hood)

Minimum viable init — without step 1 you read all zeros:

```
0x6B PWR_MGMT_1  ← 0x00   # wake from sleep (POR value is 0x40 = SLEEP bit set)
                 ← 0x01   # BETTER: clock source = X-gyro PLL, more stable than internal 8MHz RC
0x1B GYRO_CONFIG ← 0x00   # ±250 °/s  (131 LSB per °/s)
0x1C ACCEL_CONFIG← 0x00   # ±2 g      (16384 LSB per g)
0x1A CONFIG      ← 0x03   # DLPF 44Hz accel / 42Hz gyro — KEY for motor vibration
0x19 SMPLRT_DIV  ← 0x04   # sample rate = 1kHz/(1+4) = 200 Hz
```

### Full-scale ranges and sensitivities

| GYRO_CONFIG FS_SEL | Range | LSB/(°/s) | | ACCEL_CONFIG AFS_SEL | Range | LSB/g |
|---|---|---|---|---|---|---|
| 0x00 | ±250 °/s | 131.0 | | 0x00 | ±2 g | 16384 |
| 0x08 | ±500 °/s | 65.5 | | 0x08 | ±4 g | 8192 |
| 0x10 | ±1000 °/s | 32.8 | | 0x10 | ±8 g | 4096 |
| 0x18 | ±2000 °/s | 16.4 | | 0x18 | ±16 g | 2048 |

Pick the **smallest range that won't clip**: balance robot → ±250 °/s and ±2 g (max resolution). Drone/fast arm → ±1000 °/s. Shake detection → ±8 g (a sharp shake easily exceeds 2 g and clips at the rail, making magnitude thresholds unreliable).

### Burst-read the data block
Registers 0x3B–0x48: AXH,AXL, AYH,AYL, AZH,AZL, TH,TL, GXH,GXL, GYH,GYL, GZH,GZL. Always read all 14 bytes in ONE transaction — per-register reads can mix samples from different measurement instants. Values are **big-endian signed 16-bit**.

Temperature: `°C = raw/340 + 36.53`. The infamous "constant 36.5" bug = reading temp registers thinking they're accel (offset error in the burst read).

## Gyro Drift and the Complementary Filter — the core knowledge

### Why neither sensor alone works
- **Gyro**: measures angular *rate*. Integrating rate → angle accumulates bias error. A typical uncalibrated MPU6050 gyro bias of 1–3 °/s means your "angle" drifts **60–180° per minute**. Calibration reduces bias but never to zero, and it shifts with temperature (~±0.02 °/s per °C). Gyro-only angle is unusable beyond ~10 seconds.
- **Accelerometer**: measures gravity direction → absolute tilt with no drift. But it also measures *every other acceleration* — motor vibration, robot movement, bumps. Raw accel angle on a robot with running motors is noise of ±5–20°.

### The complementary filter (use this, not Kalman, for tilt)
Gyro = good short-term, bad long-term. Accel = bad short-term, good long-term. Blend:

```
angle = alpha * (angle + gyro_rate * dt) + (1 - alpha) * accel_angle
```

- **alpha = 0.98** is the canonical starting value at 100–250 Hz loop rate. Effective time constant τ = alpha·dt/(1−alpha); at dt=10 ms, alpha=0.98 → τ ≈ 0.49 s. Accel corrects drift over ~half a second; gyro dominates faster motion.
- Vibration-heavy robot → raise alpha to 0.99–0.995 (trust accel less). Sluggish drift correction / robot mostly static → 0.95–0.97.
- alpha is **loop-rate dependent**. If you tune at 100 Hz then change loop to 250 Hz, recompute: keep τ constant → `alpha = τ/(τ+dt)`.
- A full Kalman filter on an MPU6050 for 2-axis tilt gains you almost nothing over complementary and costs CPU + tuning pain. Use Kalman/Madgwick/Mahony only when you need full 3D quaternion orientation or sensor fusion with a magnetometer.

### Tilt angle math (accelerometer)
With Z up when flat:

```
pitch = atan2(-ax, sqrt(ay² + az²))   # rotation about Y
roll  = atan2( ay, az)                # rotation about X
```

- Use `atan2`, never `asin(ax/g)` — asin clips/NaNs when |ax| > g during vibration.
- **Yaw cannot be obtained from accel** (gravity is symmetric about vertical). Gyro-integrated yaw drifts forever; absolute yaw needs a magnetometer (MPU9250/HMC5883L) — say so instead of pretending gyro yaw is stable.
- Roll formula degenerates near pitch = ±90° (gimbal-ambiguity of Euler angles). For a balance robot (one axis, small angles) this never matters; for full 3D use quaternions.
- Sign conventions vary with mounting orientation. **Always verify empirically**: tilt the physical board one way, print the angle, fix signs to match your robot's convention. Do not trust copy-pasted formulas blind.

### dt measurement
Compute dt from a real timer (`time.ticks_us()` / `micros()`), not the nominal loop period. A 20% dt error = 20% gyro scaling error = persistent angle error during motion. Guard against the first-iteration huge dt and timer wraparound (`ticks_diff` on MicroPython handles wrap).

## Calibration on Flat Surface at Boot

Do this **every boot**, robot stationary and level, motors OFF:

1. Discard first ~100 ms of samples (sensor settling after wake).
2. Average 500–2000 samples (~1–2 s at 1 kHz internal rate).
3. Gyro offsets = the averages (true rate is zero). Subtract from every subsequent reading.
4. Accel offsets: average minus expected (0, 0, +16384 raw at ±2 g for Z-up). Subtract.
5. **Sanity-check**: if any gyro average exceeds ~300 raw (≈2.3 °/s) or accel deviates >2000 raw from expected, the robot was moving or not level — repeat or flag. A calibration captured while a kid is holding the robot poisons everything downstream.

Gyro offsets drift with temperature: a robot calibrated cold at 20 °C, running warm at 40 °C, regains ~0.4 °/s bias. The complementary filter's accel term absorbs this for tilt; gyro-yaw does not get this luxury.

Persisting offsets to flash/EEPROM is fine for accel (mechanical, stable) but gyro offsets should be re-measured at boot anyway — it costs 1 second.

## Motor Vibration — mount on foam

Brushed DC and especially cheap gear motors put 50–500 Hz vibration into the chassis. Consequences:
- Accel angle noise ±10°+ → complementary filter output oscillates → balance robot shakes itself to death in a feedback loop (PID reacts to vibration, motors vibrate more).
- Severe vibration can *clip* the accelerometer at ±2 g; clipped data is asymmetric → a **false steady-state tilt offset** appears only when motors run. If your balance robot leans consistently once motors start, suspect clipping before suspecting PID.

Mitigation stack, in order of effectiveness:
1. **Mechanical isolation**: mount the IMU on 3–6 mm soft foam (double-sided foam tape, two stacked layers) or rubber grommets. This is worth more than any software filter. Do not bolt the breakout rigidly to the motor plate.
2. **Hardware DLPF**: CONFIG register 0x1A ← 0x03 (44 Hz accel / 42 Hz gyro, +4.9 ms delay). Costs latency; 0x03 is the sweet spot for balance robots. Never leave DLPF at 0x00 (260 Hz, no filtering) on a motorized robot.
3. **Range headroom**: if clipping, go to ±4 g.
4. Raise complementary alpha (0.99) so vibration-corrupted accel has less influence.
5. Place IMU at the robot's center of rotation if possible (reduces linear acceleration from rotation: a = ω²r).

Also: motors brown-out shared supplies. If the MPU6050 resets mid-run (it re-enters sleep → suddenly all-zero reads), the cause is usually motor-induced voltage dip. Separate logic supply or fat capacitor (470 µF+) on the logic rail.

## Shake Detection

Compute acceleration magnitude and compare against gravity:

```
mag_g = sqrt(ax² + ay² + az²) / 16384.0      # at ±2g; use 4096 at ±8g
delta = abs(mag_g - 1.0)                      # deviation from gravity
```

Thresholds (set range to **±8 g** first — shakes clip ±2 g):

| delta threshold | Detects |
|---|---|
| 0.3–0.5 g | gentle shake / firm tap |
| 0.8–1.5 g | deliberate shake |
| > 2.5 g | hard impact / drop |

Robustness rules:
- Require N consecutive samples (or M of last K) above threshold — a single spike is electrical noise or a tap, not a shake.
- Add a **debounce/refractory period** of 300–1000 ms after a detection, or one physical shake fires 10 events.
- Magnitude-based detection is orientation-independent (no calibration needed) — this is why you use |a| − 1g, not per-axis thresholds.
- Hardware alternative: the MPU6050 motion-interrupt (MOT_THR 0x1F, MOT_DUR 0x20, INT_ENABLE 0x38 ← 0x40) fires the INT pin on motion — useful for wake-from-sleep, overkill for a polling robot loop.

## MicroPython (ESP32 / Pico) — complete working pattern

```python
from machine import I2C, Pin
import time, math, struct

MPU = 0x68

# Pico: I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)   # ESP32 pins

def w(reg, val): i2c.writeto_mem(MPU, reg, bytes([val]))

# --- init ---
w(0x6B, 0x01)        # wake, clock = X-gyro PLL
time.sleep_ms(100)   # settle
w(0x1B, 0x00)        # gyro ±250 °/s
w(0x1C, 0x00)        # accel ±2 g
w(0x1A, 0x03)        # DLPF 44/42 Hz
w(0x19, 0x04)        # 200 Hz sample rate

def read_raw():
    d = i2c.readfrom_mem(MPU, 0x3B, 14)           # one burst read
    ax, ay, az, t, gx, gy, gz = struct.unpack('>7h', d)
    return ax, ay, az, gx, gy, gz

# --- calibration: flat, still, motors off ---
gx_off = gy_off = gz_off = 0
N = 500
time.sleep_ms(100)
for _ in range(N):
    _, _, _, gx, gy, gz = read_raw()
    gx_off += gx; gy_off += gy; gz_off += gz
    time.sleep_ms(2)
gx_off //= N; gy_off //= N; gz_off //= N
# sanity: abs(offset) > 300 raw means robot was moving during cal

# --- complementary filter loop ---
ALPHA = 0.98
pitch = 0.0
last = time.ticks_us()

while True:
    ax, ay, az, gx, gy, gz = read_raw()
    now = time.ticks_us()
    dt = time.ticks_diff(now, last) / 1_000_000
    last = now
    if dt <= 0 or dt > 0.5:        # first pass / hiccup guard
        continue

    gyro_y = (gy - gy_off) / 131.0                       # °/s
    accel_pitch = math.degrees(
        math.atan2(-ax, math.sqrt(ay*ay + az*az)))

    pitch = ALPHA * (pitch + gyro_y * dt) + (1 - ALPHA) * accel_pitch
    # use pitch for PID...; print sparingly (printing kills loop rate)
```

Shake detection variant (set `w(0x1C, 0x10)` for ±8 g, divisor 4096):

```python
SHAKE_G = 1.0
HITS_NEEDED = 3
REFRACTORY_MS = 800
hits, last_shake = 0, 0

ax, ay, az, *_ = read_raw()
mag = math.sqrt(ax*ax + ay*ay + az*az) / 4096.0
if abs(mag - 1.0) > SHAKE_G:
    hits += 1
    if hits >= HITS_NEEDED and time.ticks_diff(time.ticks_ms(), last_shake) > REFRACTORY_MS:
        last_shake = time.ticks_ms()
        hits = 0
        on_shake()
else:
    hits = 0
```

## Arduino C++ — complete working pattern

```cpp
#include <Wire.h>
const uint8_t MPU = 0x68;
float gxOff = 0, gyOff = 0, gzOff = 0;
float pitch = 0;
unsigned long lastUs = 0;
const float ALPHA = 0.98;

void wreg(uint8_t r, uint8_t v) {
  Wire.beginTransmission(MPU); Wire.write(r); Wire.write(v);
  Wire.endTransmission();
}

void readRaw(int16_t &ax, int16_t &ay, int16_t &az,
             int16_t &gx, int16_t &gy, int16_t &gz) {
  Wire.beginTransmission(MPU); Wire.write(0x3B);
  Wire.endTransmission(false);              // repeated start, no stop
  Wire.requestFrom(MPU, (uint8_t)14);
  ax = Wire.read() << 8 | Wire.read();
  ay = Wire.read() << 8 | Wire.read();
  az = Wire.read() << 8 | Wire.read();
  Wire.read(); Wire.read();                 // temperature, discard
  gx = Wire.read() << 8 | Wire.read();
  gy = Wire.read() << 8 | Wire.read();
  gz = Wire.read() << 8 | Wire.read();
}

void setup() {
  Wire.begin();
  Wire.setClock(400000);
  wreg(0x6B, 0x01);   // wake, PLL clock — WITHOUT THIS ALL READS ARE 0
  delay(100);
  wreg(0x1B, 0x00);   // ±250 °/s
  wreg(0x1C, 0x00);   // ±2 g
  wreg(0x1A, 0x03);   // DLPF 44/42 Hz
  wreg(0x19, 0x04);   // 200 Hz

  // calibrate: flat, still
  long sx = 0, sy = 0, sz = 0;
  int16_t ax, ay, az, gx, gy, gz;
  for (int i = 0; i < 500; i++) {
    readRaw(ax, ay, az, gx, gy, gz);
    sx += gx; sy += gy; sz += gz;
    delay(2);
  }
  gxOff = sx / 500.0; gyOff = sy / 500.0; gzOff = sz / 500.0;
  lastUs = micros();
}

void loop() {
  int16_t ax, ay, az, gx, gy, gz;
  readRaw(ax, ay, az, gx, gy, gz);

  unsigned long now = micros();
  float dt = (now - lastUs) / 1e6;          // unsigned math survives wrap
  lastUs = now;

  float gyroY = (gy - gyOff) / 131.0;       // °/s
  float accelPitch = atan2(-(float)ax,
        sqrt((float)ay*ay + (float)az*az)) * 57.2958;

  pitch = ALPHA * (pitch + gyroY * dt) + (1 - ALPHA) * accelPitch;
  // feed pitch to PID. Avoid Serial.print every loop on AVR — it
  // throttles you to ~50 Hz and wrecks the filter tuning.
}
```

Note on `Wire.requestFrom` blocking: a flaky bus (loose jumper) makes I2C calls on AVR hang or return junk. Check `Wire.endTransmission()` return (0 = success) in init and halt with an error blink if nonzero — a robot balancing on garbage data is a faceplant.

## The 5 Mistakes Everyone Makes

1. **Not waking the chip** (PWR_MGMT_1 stays 0x40) → all sensor reads return 0. Symptom: angle is exactly 0 forever, temperature reads 36.53 °C.
2. **Gyro-only angle** ("the gyro gives me the angle, accel is noisy so I dropped it") → drifts 1–3°/s, robot leans over within a minute. Always fuse.
3. **Rigid mounting next to motors, DLPF off** → angle noise ±10°, PID oscillation, mysterious tilt offset from accel clipping. Foam tape + CONFIG=0x03.
4. **Calibrating while moving / not level / motors running** → permanent angle offset baked into every reading. Calibrate flat, still, motors off, and sanity-check the offsets.
5. **Fixed dt assumption** (`angle += gyro * 0.01` while the loop actually runs at variable rate because of Serial prints) → angle scale error proportional to timing error. Measure dt with micros()/ticks_us().

Bonus clone trap: WHO_AM_I ≠ 0x68 on counterfeit chips makes Adafruit/Jeff Rowberg libraries refuse to init. The sensor itself usually works — bypass the ID check.

## Debugging Checklist

1. `i2c.scan()` / I2C scanner sketch → device at 0x68 (or 0x69)? No → wiring, AD0, pull-ups, common GND.
2. Read 0x75 → 0x68? Other value → clone, proceed but patch ID checks. No ACK → bus problem.
3. Read 0x6B → must be 0x00/0x01 after your init. If 0x40, your wake write didn't land (check endTransmission return).
4. Flat on table: raw accel ≈ (0, 0, +16384), raw gyro within ±150 of 0. Az ≈ −16384 → board is upside down relative to your math.
5. Rotate slowly by hand: gyro signs match your angle convention? Fix signs now, not after PID tuning.
6. Print accel_pitch and fused pitch side by side: at rest they agree; during a flick, fused follows smoothly while accel spikes. Fused snapping to every accel spike → alpha too low or dt broken.
7. Angle stable at rest but ramps once motors run → vibration (foam + DLPF) or supply dip resetting the chip (re-read 0x6B mid-run: if it reverted to 0x40, brownout reset).
8. Values freeze entirely → I2C bus lockup (long wires, EMI from motor leads crossing SDA/SCL). Reroute I2C away from motor wires; on ESP32 re-init the bus on timeout.
