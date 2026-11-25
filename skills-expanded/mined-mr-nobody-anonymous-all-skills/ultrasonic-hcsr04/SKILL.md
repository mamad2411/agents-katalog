---
name: ultrasonic-hcsr04
description: "Use when wiring or coding an HC-SR04 (or HC-SR04P/RCWL-1601/US-100) ultrasonic distance sensor on Arduino, ESP32, Pico, or any 3.3V/5V MCU. Covers the 5V-echo-into-3.3V-pin trap, voltage divider values, ping timing limits, timeout handling that doesn't crash or block, temperature compensation, multi-sensor crosstalk scheduling, and mounting geometry for floor robots."
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


# HC-SR04 Ultrasonic Distance Sensor

## What it actually is

A 40 kHz ultrasonic transducer pair with a tiny MCU on board. You pulse TRIG high for ≥10 µs;
the board emits an 8-cycle 40 kHz burst, then raises ECHO and holds it high until the reflection
returns (or until its internal ~38 ms timeout). Distance is encoded **in the width of the ECHO
high pulse**, not in any serial protocol.

```
distance = (echo_high_time × speed_of_sound) / 2     # /2 because sound goes out AND back
```

At 20 °C: speed of sound ≈ 343 m/s → **distance_cm = duration_µs / 58.2** (the classic /58).
Equivalently duration_µs × 0.0343 / 2.

| Spec | Value | Practical reality |
|---|---|---|
| Range (datasheet) | 2–400 cm | Trust 3–250 cm. Beyond 250 cm only flat hard walls return reliably |
| Resolution | 3 mm | Real-world repeatability ±5–10 mm after median filtering |
| Beam angle | ~15° cone | Wide enough to catch table legs you didn't aim at |
| Supply current | ~15 mA during ping, ~2 mA idle | Fine from MCU 5V rail |
| Min object size | — | Soft/angled/thin objects (cloth, foam, chair legs at 45°) often return NOTHING |
| Internal timeout | ~38 ms ECHO high | This is why your reading of "655 cm" appears: that's the timeout, not a distance |

## 5V vs 3.3V — the #1 way people fry pins or get garbage

There are TWO common variants and they look nearly identical:

| Variant | VCC | ECHO output level | Safe on ESP32/Pico/3.3V boards? |
|---|---|---|---|
| **HC-SR04** (classic, blue PCB) | 5V only — at 3.3V VCC it pings weakly or not at all | **5V** | NO — ECHO will overdrive a 3.3V GPIO |
| **HC-SR04P** / **HC-SR04+** (often "P" silkscreened, sometimes 3-pin mode jumper) | 3.0–5.5V | Follows VCC | Yes, run it at 3.3V directly |
| **RCWL-1601** (Adafruit 4007) | 3–5.5V | Follows VCC | Yes |
| **US-100** (5 pins, jumper) | 3–5V | Follows VCC; also has UART mode with built-in temp compensation | Yes |

**Rule for an AI generating wiring instructions: assume classic 5V HC-SR04 unless the user
says "P" variant.** Classic part on a 3.3V board:

- Power VCC from **5V** (VBUS on Pico, VIN/5V on ESP32 devkit).
- TRIG: 3.3V GPIO output drives it fine — the HC-SR04 registers ≥2.4V as high. No level shifter needed on TRIG.
- ECHO: **MUST be divided down**. 5V into an ESP32 or RP2040 pin is out of absolute-maximum spec; it may work for weeks then kill the pin, or inject current through the protection diode and corrupt ADC readings elsewhere.

### Voltage divider for ECHO (the standard fix)

```
ECHO ──[ 1kΩ ]──┬──→ MCU GPIO (3.3V logic)
                │
              [ 2kΩ ]
                │
               GND
```

5V × 2k/(1k+2k) = **3.33V**. Also fine: 1k/1.8k (3.21V), 10k/20k (higher impedance — still OK
because edge timing at these pulse widths tolerates the extra RC, but stay ≤10k top resistor;
100k dividers visibly slope the edges and skew µs timing).

5-pin **US-100 in UART mode** (jumper on): send 0x55, read 2 bytes big-endian = distance in mm,
already temperature compensated. If a US-100 is available, prefer UART mode — it removes the
level-shift, timeout, and temperature problems entirely.

### Full wiring table — ESP32 DevKit + classic HC-SR04

| HC-SR04 pin | Connects to | Notes |
|---|---|---|
| VCC | ESP32 `VIN`/`5V` (USB 5V) | NOT 3V3 — classic part is unreliable at 3.3V |
| GND | ESP32 `GND` | Common ground is mandatory |
| TRIG | GPIO 5 (any output-capable pin; avoid 34–39, input-only) | Direct, no divider |
| ECHO | 1k from ECHO → GPIO 18, 2k from GPIO 18 → GND | Divider node goes to the pin |

### Raspberry Pi Pico + classic HC-SR04

| HC-SR04 pin | Pico pin | Notes |
|---|---|---|
| VCC | VBUS (pin 40) | 5V from USB |
| GND | GND (pin 38) | |
| TRIG | GP15 | direct |
| ECHO | GP14 **via 1k/2k divider** | RP2040 pins are NOT 5V tolerant |

### Arduino Uno/Nano (5V boards)

Everything direct: VCC→5V, TRIG→D9, ECHO→D10, no divider. (Uno R4 is 5V-tolerant on GPIO too.)

## Code that works

### MicroPython (Pico / ESP32)

```python
from machine import Pin, time_pulse_us
import time

TRIG = Pin(15, Pin.OUT, value=0)
ECHO = Pin(14, Pin.IN)

def read_distance_cm(temp_c=20.0):
    """Returns distance in cm, or None if no echo (nothing in range).
    None is a VALID result — never let it crash the control loop."""
    TRIG.value(0)
    time.sleep_us(5)
    TRIG.value(1)
    time.sleep_us(10)          # >=10us trigger pulse
    TRIG.value(0)
    # 30ms timeout ~= 5m round trip; time_pulse_us returns -1/-2 on timeout
    duration = time_pulse_us(ECHO, 1, 30000)
    if duration < 0:
        return None            # timeout: no object, or sensor disconnected
    speed = 331.3 + 0.606 * temp_c      # m/s, temperature compensated
    return (duration * speed / 10000) / 2   # us * m/s -> cm, halved for round trip

def read_filtered_cm(n=5):
    """Median of n pings. ~60ms apart to respect sensor recovery time."""
    vals = []
    for _ in range(n):
        d = read_distance_cm()
        if d is not None:
            vals.append(d)
        time.sleep_ms(60)
    if not vals:
        return None
    vals.sort()
    return vals[len(vals) // 2]
```

`time_pulse_us` is the correct primitive — it busy-waits in C with µs accuracy. Do NOT write a
Python while-loop polling `ECHO.value()`; interpreter jitter adds ±several hundred µs (= ±5+ cm)
and you'll write your own buggy timeout.

### Arduino C++ (non-blocking pattern for robot loops)

```cpp
const uint8_t TRIG_PIN = 9;
const uint8_t ECHO_PIN = 10;

// Simple blocking read — fine for prototypes, BAD inside a motor control loop
// (pulseIn blocks up to timeout; default timeout is 1 SECOND — always pass your own!)
float readDistanceCm(float tempC = 20.0) {
  digitalWrite(TRIG_PIN, LOW);  delayMicroseconds(5);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);  // 30ms cap
  if (duration == 0) return -1.0;            // timeout sentinel; check before use!
  float speed = 331.3 + 0.606 * tempC;       // m/s
  return (duration * speed / 10000.0) / 2.0; // cm
}

// Non-blocking read via interrupt — use this on a moving robot.
volatile unsigned long echoStart = 0;
volatile long echoDuration = -1;             // -1 = no result yet

void echoISR() {
  if (digitalRead(ECHO_PIN)) echoStart = micros();
  else                       echoDuration = micros() - echoStart;
}

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(ECHO_PIN), echoISR, CHANGE);
}

unsigned long lastPing = 0;
float lastDistanceCm = -1;

void loop() {
  unsigned long now = millis();
  if (now - lastPing >= 60) {                // 60ms minimum between pings
    lastPing = now;
    if (echoDuration > 0 && echoDuration < 30000)
      lastDistanceCm = echoDuration / 58.2;
    else
      lastDistanceCm = -1;                   // timeout or stale
    echoDuration = -1;
    digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10); digitalWrite(TRIG_PIN, LOW);
  }
  // ... rest of robot loop runs at full speed, never blocked by the sensor
}
```

Note: on Uno, interrupt-capable pins are only D2/D3 — move ECHO there for the ISR version.
ESP32/Pico can attach interrupts to any GPIO.

## Timing rules (violate these and readings go insane)

1. **≥60 ms between pings.** The datasheet says "suggested measurement cycle 60 ms". Ping faster
   and the previous burst's late reflections (off a far wall) arrive during the next measurement
   → phantom readings that jump between near and far. 16 Hz max per sensor. If you need faster
   reaction, that's what the non-blocking pattern + your control loop interpolating is for.
2. **TRIG pulse ≥10 µs.** 10 is the spec; 12–15 adds margin. A `digitalWrite` pair with no delay
   (~4 µs on a 16 MHz Uno) sometimes works, sometimes doesn't — classic "works on my desk" bug.
3. **Set your own timeout.** Arduino `pulseIn` defaults to 1,000,000 µs — a full second of frozen
   robot per missed echo. Use 25,000–30,000 µs (≈4–5 m max range). The sensor's own ECHO line
   drops after ~38 ms regardless.
4. **Drive TRIG low for a few µs before the pulse** (the `value(0); sleep_us(5)` prelude). If TRIG
   floated high before setup, the rising edge never happens.

## Timeout = "no object", not an error

A timeout occurs when: nothing within range, the target absorbed the sound (cloth, foam, your
cat), the target deflected it away (surface angled >~22° off perpendicular), or wiring is broken.
**All four are normal runtime conditions.** Code that does `if distance < 20: stop()` after a
read that returned `None`/`-1` will either crash (TypeError on None) or, with -1, interpret
"nothing detected" as "object at -1 cm = emergency stop forever".

Correct obstacle-avoidance predicate:

```python
d = read_distance_cm()
obstacle = d is not None and d < 20      # None means CLEAR (or unknown), not "0 cm"
```

If you must distinguish "clear" from "sensor dead": a healthy sensor pointed at open floor space
still returns *occasional* readings; 50 consecutive timeouts (≥3 s) means check the wiring.
Also distrust readings <2 cm — inside the blind zone the math produces garbage.

## Temperature compensation

Speed of sound: **v = 331.3 + 0.606 × T(°C)** m/s. The hardcoded /58 constant assumes ~20 °C.

| Temperature | Speed | Error if you assume 20 °C, target at 200 cm |
|---|---|---|
| 0 °C | 331 m/s | reads ~207 cm (+3.5%) |
| 20 °C | 343 m/s | correct |
| 35 °C | 352 m/s | reads ~195 cm (−2.5%) |

For "don't hit the wall" robots, ignore it. For mapping, docking alignment, or anything claiming
cm-level accuracy across rooms/outdoors, feed a DHT22/BME280/DS18B20 temperature into the formula
(as in the code above). Humidity adds <0.5% — not worth modeling.

## Multiple sensors — crosstalk

Two HC-SR04s pinged simultaneously hear each other's bursts: sensor A reports the distance along
the path emitter-B → wall → receiver-A. Symptom: readings that are *plausible but wrong*, often
only when both face the same general direction.

**Fix: ping sequentially, never concurrently.** Round-robin with the 60 ms gap *per ping*,
which means each sensor updates at 60 ms × N:

```python
sensors = [front, left, right]
i = 0
def update():           # call every 60ms (timer or loop scheduler)
    global i
    distances[i] = sensors[i].read()   # one ping per slot
    i = (i + 1) % len(sensors)
```

3 sensors → each updates every 180 ms (≈5.5 Hz each). At 0.3 m/s robot speed that's 5.5 cm
travelled between updates of any one sensor — budget your stopping distance accordingly, or
ping the front sensor 2× per cycle.

You can share one TRIG pin across all sensors only if you *want* simultaneous pings (you don't).
Separate TRIG per sensor; ECHOs each need their own pin (+ divider on 3.3V boards).

Sensors facing opposite directions (front/back) generally can be paired in the same slot —
crosstalk requires a sound path between them. Side-by-side front sensors angled <30° apart
always need separate slots.

## Mounting on a floor robot

- **Height: 8–15 cm off the floor, aimed dead level.** The 15° cone half-angle is ~7.5°; mounted
  at 10 cm and level, the cone edge touches the floor at ~76 cm. Mount lower or tilt down even
  2–3° and the *floor itself* returns echoes at ~50–80 cm — the classic "robot sees a phantom
  wall on smooth concrete" bug. Carpet absorbs ultrasound, so the bug appears only when the robot
  moves to hard flooring, which makes it maddening to reproduce.
- Tilt **up** 1–2° if you can't mount high; you lose detection of very low obstacles but kill
  floor returns.
- Keep transducers **proud of the chassis** — any bezel/plate in front of the cans causes a
  fixed ~5–15 cm reflection that swamps everything ("sensor always reads 7 cm" = it's seeing
  its own mounting hole).
- Things HC-SR04 reliably misses at floor level: chair/table legs (thin, round), stair
  *drop-offs* (it can't see down — use a downward IR/ToF cliff sensor), soft furniture, mesh
  bins. Pair it with a bumper switch; the ultrasonic is the early warning, the bumper is truth.
- Vibration: motor PWM whine is electrical, not acoustic, but a chassis ringing at ~40 kHz
  harmonics from cheap geared motors *can* raise the noise floor — rubber-grommet the sensor
  mount if readings get noisy only when motors run. Also check this is not just supply droop:
  brushed motors sharing the 5V rail cause brownout pings; give the sensor its own regulator
  tap or a 100 µF cap at VCC.

## Debugging checklist

1. **Reads constant ~655/674 cm or pulseIn returns 0 always** → no echo ever: ECHO miswired,
   divider node not on the pin, sensor running at 3.3V (classic variant), or TRIG pulse too short.
2. **Reads 0 or tiny constant** → ECHO pin reads low permanently: swapped TRIG/ECHO, or divider
   resistors swapped (2k on top gives 1.67V — below ESP32's ~2.0V VIH threshold = "stuck low").
3. **Works at desk, garbage on robot** → motor supply droop (scope VCC during ping), or floor
   returns (re-aim level/up), or pinging faster than 60 ms.
4. **Random far readings mixed into good ones** → crosstalk from second sensor, or ping rate
   too high. Median-of-5 filter hides it; sequencing fixes it.
5. **Reads fine then pin dies weeks later (ESP32/Pico)** → you skipped the divider. Replace pin
   (use a different GPIO) AND add the divider.
6. **Soft objects invisible** → physics, not a bug. Add bumper/IR.
7. **Sensor warm to the touch / 5V rail sags** → reversed VCC/GND once; the onboard MCU is
   usually dead even if it looks alive. Replace the module ($1).

## Library notes

- Arduino: **NewPing** library handles timeouts, median filtering, and multi-sensor timing
  correctly (`sonar.ping_median(5)`, `NewPing::convert_cm`). Prefer it over raw pulseIn for
  anything beyond a demo. Its `ping_timer()` gives the non-blocking pattern without writing ISRs.
- MicroPython: no dominant library needed — `time_pulse_us` (shown above) is the whole driver.
- ESP32 Arduino core: `pulseIn` works but is jittery under WiFi; the interrupt pattern above,
  or NewPing with interrupts disabled around timing-critical sections, is more stable. If WiFi
  is active, pin readings can jump ±2 cm — median filter is mandatory.
