---
name: line-following
description: "Use when writing code for line-following robots using reflectance sensors (TCRT5000, QRE1113, or arrays like QTR-8A/8RC, 5-channel TCRT5000 boards). Provides analog vs digital mode selection, startup calibration sweep, weighted-average position algorithm, sensor mounting geometry, ambient light rejection, and the PID line-follow loop that actually works."
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


# Line Following with Reflectance Sensors (TCRT5000 / QRE1113 / QTR arrays)

## How these sensors actually work

A reflectance sensor = IR LED (~950nm) + phototransistor in one package, both pointing down. White surface reflects IR → phototransistor conducts → output voltage drops (in the common pull-up wiring). Black tape absorbs IR → little reflection → output stays high.

**Critical fact most code gets backwards:** with the standard wiring (phototransistor collector → ADC pin, pull-up to VCC, emitter → GND):
- **WHITE surface → LOW reading** (more reflection, transistor conducts harder)
- **BLACK line → HIGH reading**

Some breakout boards invert this with a comparator or different topology. **Never assume polarity — measure it during calibration** and store a `whiteIsLow` flag, or normalize so 0 = white, 1000 = black regardless of hardware.

### TCRT5000 vs QRE1113

| Property | TCRT5000 | QRE1113 |
|---|---|---|
| Package | 10×6×7mm through-hole pair | 3.6×2.9mm SMD |
| Optimal sensing distance | 2.5mm (datasheet peak), usable 0.2–15mm | 3mm peak, usable 1–6mm |
| IR LED forward current | 60mA max, run at 20–30mA | 50mA max, run at 20–25mA |
| IR LED forward voltage | ~1.25V | ~1.2V |
| LED series resistor @5V | 150–220Ω (for ~20mA) | 150–220Ω |
| LED series resistor @3.3V | 100Ω (for ~20mA) | 100Ω |
| Phototransistor pull-up | 10kΩ (analog), 4.7k–10kΩ typical | 10kΩ |
| Crosstalk between adjacent | Significant under 10mm spacing | Lower (built-in barrier on some) |

The QRE1113 is what Pololu QTR arrays use. The TCRT5000 is what cheap 5-channel Chinese boards use.

## Wiring

### Bare TCRT5000 (analog mode) — the wiring that works

```
TCRT5000 pin    →  Connection
─────────────────────────────────────────────
LED Anode (A)   →  220Ω resistor → 5V (or 100Ω → 3.3V)
LED Cathode (K) →  GND
Photo Collector →  ADC pin  AND  10kΩ resistor → VCC (pull-up)
Photo Emitter   →  GND
```

Identifying pins on the bare part: the LED is the **blue/clear** dome, phototransistor is the **black** dome. Longer leg = anode on the LED side, collector on the transistor side (verify with datasheet — clones vary).

### Common 5-channel TCRT5000 board (TCRT5000-5CH)

| Board pin | Connect to | Notes |
|---|---|---|
| VCC | 5V (most boards) or 3.3V | Check comparator (LM393 works 3.3–5V) |
| GND | GND | |
| OUT1–OUT5 / D1–D5 | GPIO inputs | Digital, threshold set by onboard trimpot |
| A1–A5 (if present) | ADC pins | **Use these if they exist** |

**Trap:** boards powered at 5V output 5V digital HIGH. On a 3.3V MCU (ESP32, Pico, most ARM boards) this damages pins over time. Either power the board at 3.3V (works if it uses LM393), or add a voltage divider (e.g. 2.2kΩ/3.3kΩ) per output.

### QTR-8A (analog) / QTR-8RC (RC/digital-timed)

- QTR-**8A**: 8 analog outputs, needs 8 ADC pins (or a mux). 0–VCC analog out.
- QTR-**8RC**: outputs are charged HIGH then you time the decay — works on any digital pins, no ADC needed, but timing-sensitive (use the Pololu QTRSensors library on Arduino; on MicroPython bit-bang with `time.ticks_us()`).
- Both have an **LEDON pin** — drive it from a GPIO so you can strobe the emitters (see ambient light section). Tie HIGH if you don't.
- 3.3V operation: cut the 3.3V bypass jumper per Pololu docs, or just power VCC at 3.3V on newer revisions.

## Analog vs digital mode — pick analog, here's why

**Digital mode** (comparator + trimpot, the D outputs on cheap boards):
- Output is just on/off line detection. Position resolution = number of sensors. With 5 sensors you get 5 discrete positions → the robot oscillates (bang-bang control) and falls off the line above ~0.3 m/s.
- The trimpot threshold is fixed at one surface/lighting condition. Move to a different table or venue lighting and it stops working. Competition killer.
- Acceptable ONLY for: simple stop-at-line detection, edge detection on sumo robots, or counting cross-lines.

**Analog mode**:
- Continuous reading per sensor → interpolated line position with ~10–50× the resolution of your sensor count.
- Calibratable in software at startup → immune to surface/lighting changes.
- Required for any PID line follower.

**Rule for code generation: if the robot follows a line, use analog. If the board only exposes digital outputs, tell the user to use the A pins or get a different board — don't write a PID follower on digital inputs, it will not work well.**

## Mounting geometry — this matters more than your code

- **Sensor height above surface: 2–10mm, optimum 3–5mm for TCRT5000, ~3mm for QRE1113.** Below 2mm: readings saturate and tiny floor bumps cause dropouts. Above 10mm: contrast collapses (white vs black difference shrinks below noise) and adjacent-sensor crosstalk pools. This is the #1 cause of "my line follower worked yesterday" — someone changed wheels/chassis and the height moved.
- **Mount sensors AHEAD of the drive wheels' axle**, by roughly 0.5–1× the wheelbase. Sensors behind or on the axle give the controller no preview → unstable at speed. Further ahead = more derivative gain effect = smoother but can cut corners.
- **Array spacing vs line width:** you want the line under **at least 2 sensors at all times** for interpolation to work. For standard 19mm (¾") electrical tape: sensor pitch ≤ 12mm works well (QTR-8A pitch is 9.525mm — designed for this). The cheap 5-ch TCRT boards have ~15mm pitch — marginal; the position estimate gets steppy between sensors. Total array width must exceed line width + maximum expected lateral error, or the robot loses the line in fast corners.
- Mount sensors **parallel to the floor**. A 10° tilt changes effective height across the array and skews calibration per-sensor (calibration partially compensates, but contrast still suffers on the high side).
- Paint/tape a **matte black shroud** around the array if competing under sunlight or halogen lights.

## Ambient light interference

Sunlight and incandescent/halogen lights are full of IR and will saturate phototransistors (readings pin to the "white" extreme everywhere). LED room lighting is mostly fine. Symptoms: robot works at home, fails at the venue near a window.

Defenses, in order of effectiveness:
1. **Physical shroud/skirt** around the sensor array, 2–5mm clearance to floor. Cheapest and best.
2. **Emitter strobing (differential measurement):** read with IR LED off, read with it on, subtract. Removes any constant ambient component.

```python
# MicroPython — strobed differential read (LEDON pin controls emitters)
def read_differential(adc, led_on_pin):
    led_on_pin.value(0)
    time.sleep_us(200)            # phototransistor fall time ~ tens of µs
    ambient = adc.read_u16()
    led_on_pin.value(1)
    time.sleep_us(200)
    lit = adc.read_u16()
    return max(0, ambient - lit)  # pull-up wiring: lit < ambient on white
```
   Cost: halves your sample rate. The 200µs settle is needed — TCRT5000 phototransistor rise/fall is ~10µs but the RC of the 10kΩ pull-up + pin capacitance dominates.
3. Calibrate **at the venue, on the actual track** — never reuse yesterday's calibration constants.

## Calibration sweep — non-negotiable, do it at every startup

Raw readings vary per sensor (LED brightness tolerance ±30%, transistor gain spread, height differences) and per surface. Calibration records min/max per sensor, then normalizes everything to a common 0–1000 scale.

**Procedure:** for ~2–4 seconds at startup, sweep the array across the line (either spin the robot in place over the line, or have the user slide it side to side) while recording each sensor's minimum and maximum.

```python
# MicroPython (RP2040/ESP32) — calibration + normalized read
import time
from machine import ADC, Pin

NUM = 5
adcs = [ADC(Pin(p)) for p in (26, 27, 28, 29, 25)]  # adjust pins
cal_min = [65535] * NUM
cal_max = [0] * NUM

def calibrate(ms=3000):
    # Robot should spin in place over the line during this.
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < ms:
        for i, a in enumerate(adcs):
            v = a.read_u16()
            if v < cal_min[i]: cal_min[i] = v
            if v > cal_max[i]: cal_max[i] = v
        time.sleep_ms(2)
    # Sanity check: a sensor that never saw contrast is broken/misaligned
    for i in range(NUM):
        if cal_max[i] - cal_min[i] < 3000:   # <~5% of full scale
            print("WARN: sensor", i, "low contrast", cal_min[i], cal_max[i])

def read_calibrated():
    """Returns list of 0..1000, where 1000 = black line, 0 = white."""
    out = []
    for i, a in enumerate(adcs):
        span = cal_max[i] - cal_min[i]
        if span < 1: span = 1
        v = (a.read_u16() - cal_min[i]) * 1000 // span
        out.append(min(1000, max(0, v)))
    return out
```

```cpp
// Arduino C++ — same logic, bare analog sensors
const uint8_t NUM = 5;
const uint8_t PINS[NUM] = {A0, A1, A2, A3, A4};
uint16_t calMin[NUM], calMax[NUM];

void calibrate(uint16_t ms = 3000) {
  for (uint8_t i = 0; i < NUM; i++) { calMin[i] = 1023; calMax[i] = 0; }
  uint32_t t0 = millis();
  while (millis() - t0 < ms) {           // spin robot over line meanwhile
    for (uint8_t i = 0; i < NUM; i++) {
      uint16_t v = analogRead(PINS[i]);
      if (v < calMin[i]) calMin[i] = v;
      if (v > calMax[i]) calMax[i] = v;
    }
  }
}

// 0 = white, 1000 = black
void readCalibrated(uint16_t out[NUM]) {
  for (uint8_t i = 0; i < NUM; i++) {
    int32_t span = (int32_t)calMax[i] - calMin[i];
    if (span < 1) span = 1;
    int32_t v = ((int32_t)analogRead(PINS[i]) - calMin[i]) * 1000 / span;
    out[i] = constrain(v, 0, 1000);
  }
}
```

Notes:
- During calibration, **spin the robot in place** under motor power (e.g. left motor +40%, right −40%, reverse halfway through). Automating this beats asking a kid to wave the robot around.
- If your wiring gives white = HIGH, flip the normalization (`1000 - v`) so the rest of the code can always assume **1000 = black**.
- Optionally persist cal_min/cal_max to flash/EEPROM as a fallback, but a fresh sweep always beats stored values.
- Using the Pololu QTRSensors Arduino library? `qtr.calibrate()` in a loop for ~400 iterations does exactly this; `qtr.readLineBlack(values)` does the position math below for you.

## Weighted-average position algorithm

Converts N normalized readings into a single line position. With sensors indexed 0..N-1, position scale 0..(N-1)*1000, center = (N-1)*500:

```
position = Σ(value[i] * i * 1000) / Σ(value[i])
```

Each sensor's reading weights its position. The result interpolates *between* sensors — this is where sub-sensor resolution comes from.

```python
# MicroPython — position with line-loss memory
last_position = (NUM - 1) * 500   # start assuming centered

def line_position():
    global last_position
    vals = read_calibrated()
    total = sum(vals)
    on_line = any(v > 200 for v in vals)   # noise floor threshold
    if not on_line:
        # Line lost: snap to the side we last saw it, so PID steers back hard
        if last_position < (NUM - 1) * 500:
            return 0
        return (NUM - 1) * 1000
    weighted = sum(v * i * 1000 for i, v in enumerate(vals))
    last_position = weighted // total
    return last_position
```

```cpp
// Arduino C++
uint16_t lastPosition = (NUM - 1) * 500;

uint16_t linePosition() {
  uint16_t v[NUM];
  readCalibrated(v);
  uint32_t weighted = 0, total = 0;
  bool onLine = false;
  for (uint8_t i = 0; i < NUM; i++) {
    if (v[i] > 200) onLine = true;       // ignore noise below 20%
    if (v[i] > 50) {                     // tiny values just add noise to the average
      weighted += (uint32_t)v[i] * i * 1000;
      total += v[i];
    }
  }
  if (!onLine)
    return (lastPosition < (uint16_t)(NUM - 1) * 500) ? 0 : (NUM - 1) * 1000;
  lastPosition = weighted / total;
  return lastPosition;
}
```

Key details:
- The `> 200` on-line check and `> 50` inclusion floor stop near-white noise from dragging the average toward center. Without these, position reads "centered" on a fully white floor — the robot drives straight off the track confidently.
- **Line-loss memory** (return hard left/right based on last seen side) is what lets the robot recover from sharp corners instead of wandering. Every competitive line follower has this.
- This is for a **black line on white**. White line on black: invert values first (`v = 1000 - v`).

## Closing the loop — PD controller (the part that makes it fast)

Don't use bang-bang ("if left sensor: turn left"). Use PD on position error. Integral term is usually unnecessary and causes windup in corners — start with Kp and Kd only.

```cpp
// Arduino C++ — PD line follow, 5 sensors, differential drive
const int16_t CENTER = (NUM - 1) * 500;   // 2000 for 5 sensors
float Kp = 0.08, Kd = 1.2;                // start: Kp small, Kd ≈ 15*Kp
int16_t lastError = 0;
const int16_t BASE_SPEED = 150;           // of 255 — tune up after stable
const int16_t MAX_SPEED  = 255;

void followStep() {
  int16_t error = (int16_t)linePosition() - CENTER;   // -2000..+2000
  int16_t correction = Kp * error + Kd * (error - lastError);
  lastError = error;
  int16_t left  = constrain(BASE_SPEED + correction, 0, MAX_SPEED);
  int16_t right = constrain(BASE_SPEED - correction, 0, MAX_SPEED);
  setMotors(left, right);
}
// Call followStep() at a FIXED rate (e.g. every 5ms). Kd is meaningless
// if loop timing jitters — use a timer or enforce the period.
```

Tuning order: (1) Kd=0, raise Kp until it oscillates, halve it. (2) Raise Kd until oscillation damps. (3) Raise BASE_SPEED, re-tune. Loop rate target: ≥100Hz; 200–500Hz for competition.

## The 5 mistakes everyone makes

1. **No calibration sweep** — hardcoded threshold like `if (analogRead(A0) > 512)`. Works on one floor, one day. Always calibrate at startup.
2. **Polarity assumed wrong** — code written for black=HIGH on a board that outputs black=LOW. Robot steers *away* from the line. Print raw values over white and black before writing logic.
3. **Sensor height wrong** — array bolted 15mm up "for ground clearance," contrast gone, calibration span tiny, position is noise. 3–5mm. Measure it.
4. **Digital outputs used for a PID follower** — 5 discrete positions can't feed a derivative term. Use analog outs.
5. **No line-loss handling** — line exits the array in a hairpin, weighted average returns garbage or center, robot drives straight into the wall. Remember the last side and saturate the steering toward it.

## Debugging checklist

- [ ] Print raw ADC per sensor over white, then black. Expect ≥40% of full-scale difference. Less → check height (3–5mm), LED resistor (LED should glow faintly purple on a phone camera), pull-up value.
- [ ] One sensor reads constant min or max → swapped collector/emitter, dead LED, or cold solder joint. Phone camera check: every emitter should glow.
- [ ] All sensors read "white" everywhere → ambient IR saturation (sunlight/halogen). Shroud it or strobe emitters.
- [ ] Position output jumps in steps of ~1000 instead of smoothly → you're reading digital outs, or inclusion floor too high.
- [ ] Robot oscillates at low speed → Kp too high or sensors mounted too close to the axle.
- [ ] Works slow, dies fast → loop rate too low (aim ≥100Hz), or sensors not far enough ahead of the wheels.
- [ ] ESP32 specific: don't use ADC2 pins (GPIO 0,2,4,12–15,25–27) if WiFi is on — ADC2 readings fail with WiFi active. Use ADC1 (GPIO 32–39).
- [ ] RP2040 specific: only 3 usable ADC pins (GPIO 26–28; 29 is VSYS sense on Pico). More than 3 analog sensors → use a 74HC4051 mux (S0–S2 to GPIOs, Z to one ADC pin, allow 10µs settle after channel switch) or use a QTR-8RC and timed digital reads.
- [ ] Readings noisy → take 3 readings and use the median; keep sensor wiring away from motor leads; add 100nF across the board's VCC/GND.
