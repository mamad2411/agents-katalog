---
name: servos
description: "Use when controlling hobby servos (SG90, MG90S, MG996R, DS3218) or continuous-rotation servos from Arduino, ESP32, Pico, or any MCU. Covers 50Hz PWM timing, real pulse ranges (500-2400µs, not 1000-2000), power architecture that prevents jitter and brownouts, current spike handling, detach strategies, and multi-servo control."
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


# Hobby Servo Control (SG90 / MG90S / MG996R class)

Expert knowledge for generating correct servo code and wiring on the first try. The two failure modes that account for ~90% of servo problems in the field are (1) powering the servo from the MCU board's 5V pin and (2) assuming the pulse range is 1000–2000µs. Both are addressed below with numbers.

## 1. The signal: what a servo actually expects

- **Frame rate: 50Hz** (20ms period). The servo only cares about the HIGH pulse width within each frame, not the duty cycle as a percentage. Analog servos tolerate 40–60Hz; digital servos (MG996R is analog; DS3218 digital) often accept up to 333Hz but NEVER assume — 50Hz always works.
- **Pulse width encodes position.** Nominal spec says 1000µs = 0°, 1500µs = center, 2000µs = 180°. **This is wrong for almost every real servo.**

### Real-world pulse ranges (measured, typical)

| Servo | Full range pulses | Mechanical range | Stall current @ 5V | Idle/moving current |
|---|---|---|---|---|
| SG90 (9g, plastic gears) | ~500–2400µs | ~180° (often 170–190°) | ~650–800mA | 10mA idle / 100–250mA moving |
| MG90S (metal gears) | ~500–2400µs | ~180° | ~700mA–1A | similar to SG90 |
| MG996R | ~500–2500µs | ~180° (many units only ~120° on 1000–2000µs!) | **~2.5A** (datasheet says 1.4A @ 6V, real units spike higher) | 10mA idle / 500–900mA moving |
| DS3218 (digital) | ~500–2500µs | 180° or 270° variants | ~2.8A @ 6.8V | higher idle (~50mA, digital holds position actively) |

**Consequence:** if you use the Arduino default `servo.attach(pin)` (which maps 0–180° to 544–2400µs) you get nearly full range. If you write raw PWM assuming 1000–2000µs, you get roughly **half the mechanical range** and users report "my servo only moves 90°".

**Calibrate per unit.** Same model, different factory batch = different endpoints. Step pulses down from 1500µs in 20µs decrements until you hear the gear buzz at the mechanical stop, back off 20–40µs, that's your real minimum. Repeat upward. **Holding a servo against its mechanical stop draws stall current continuously and strips plastic gears (SG90) in minutes.**

## 2. Power architecture — the #1 cause of "random" failures

### Never power any servo from the MCU board's 5V pin

- Arduino Uno's 5V rail through the USB port is fused at ~500mA total; through the barrel jack the onboard regulator can supply ~800mA–1A *before thermal limiting* and that includes the board itself.
- An SG90's **startup/stall spike is 650–800mA**; an MG996R spikes **2A+** on every direction change. The spike lasts 5–50ms — long enough to sag the 5V rail below the brownout threshold (~4.3V for a 16MHz AVR, 3.3V LDO dropout on ESP32 boards).
- Symptoms of shared power: MCU resets when servo moves, servo "jitters" or twitches randomly, USB device disconnects, ESP32 brownout detector trips (`Brownout detector was triggered`), serial garbage.

### Correct wiring

```
External 5–6V supply (+) ──────── Servo RED
External supply (−/GND) ──┬────── Servo BROWN/BLACK
                          └────── MCU GND          ← COMMON GROUND, mandatory
MCU GPIO ────────────────────────  Servo ORANGE/YELLOW/WHITE (signal)
```

- **Common ground is non-negotiable.** Signal is referenced to ground; without it the servo sees floating garbage and twitches or does nothing.
- Supply sizing: **1A per SG90, 2.5–3A per MG996R**, peak. A 4-servo MG996R arm needs a 10A-capable 6V supply (or accept that simultaneous moves will sag).
- Voltage: SG90 rated 4.8–6V. MG996R 4.8–7.2V (faster and stronger at 6V). **Do not feed servos 7.4V 2S LiPo directly unless the servo is explicitly rated for it (DS3218 is, SG90 is not — it will overheat and die).** Use a 5V/6V UBEC (switching BEC, e.g. 5A UBEC, ~£5) between LiPo and servos.
- **Decoupling:** 470–1000µF electrolytic across the servo power rail, close to the servos, plus 100nF ceramic. This absorbs the direction-change spikes. Without it, even a beefy supply shows jitter over long thin wires.
- Signal voltage: servos read the signal pin fine at **3.3V logic** (ESP32, Pico) when powered at 5–6V — threshold is typically ~2.5V. No level shifter needed for the signal in 99% of cases. If a specific servo is marginal at 3.3V signal + 6V power, drop servo supply to 5V or add a shifter.

### Brown wire / connector pinout (JR/Futaba standard)

| Wire | Meaning |
|---|---|
| Brown or Black | GND |
| Red (center pin — protects against reversed plug) | V+ |
| Orange / Yellow / White | Signal |

## 3. Code — Arduino C++

### Standard servo (positional)

```cpp
#include <Servo.h>   // AVR: uses Timer1 → kills PWM on pins 9 & 10 (Uno)
                     // Up to 12 servos per timer on AVR.

Servo arm;

const int ARM_PIN = 9;
// Calibrated endpoints for THIS unit (see calibration procedure above):
const int ARM_MIN_US = 560;
const int ARM_MAX_US = 2380;

void setup() {
  arm.attach(ARM_PIN, ARM_MIN_US, ARM_MAX_US);  // ALWAYS pass explicit min/max
  arm.write(90);            // go to center; write() maps 0-180 onto min/max us
  delay(500);               // give it time to physically arrive — write() returns instantly!
}

void loop() {
  arm.writeMicroseconds(1500);  // preferred for precision: ~10x finer than write(degrees)
}
```

Key facts:
- `write(angle)` returns **immediately**; the servo takes time to travel (SG90: ~0.12s/60° no load → ~0.4s for 180°; MG996R: ~0.17s/60°). If you `write(0); write(180);` back-to-back, it only goes to 180. There is **no position feedback** — you cannot ask a standard servo where it is.
- `writeMicroseconds()` gives ~1900 discrete steps over full range vs 180 for `write()`. Use it for smooth motion.
- **ESP32 (Arduino core 3.x):** classic `Servo.h` doesn't work. Use `ESP32Servo` library — API-compatible, plus call `ESP32PWM::allocateTimer(0..3)` in setup and `servo.setPeriodHertz(50)` before attach. ESP32-S3/C3 LEDC channels are limited; each servo consumes one.
- **AVR `Servo.h` disables `analogWrite` on pins 9/10 (Uno/Nano)** even if the servo is attached elsewhere — it commandeers Timer1. On Mega it takes 11–13 first, then more timers as you add servos.

### detach() — the jitter killer and gear saver

```cpp
arm.write(targetAngle);
delay(travelTimeMs(currentAngle, targetAngle));  // wait for physical arrival
arm.detach();          // stop sending pulses → servo goes limp, zero jitter, zero hold current
// Reattach before next move:
arm.attach(ARM_PIN, ARM_MIN_US, ARM_MAX_US);
```

- An attached analog servo constantly micro-corrects against its own potentiometer noise → audible buzz + jitter + heat, especially under static load near a pulse-range edge.
- `detach()` cuts the pulse train. Analog servos go limp (no holding torque!). **Do not detach if the servo must hold a load against gravity** (robot arm joint) — it will fall. Detach is for: grippers at rest, pan/tilt parked, anything spring-returned or friction-held.
- Some digital servos hold last position on signal loss; analog ones never do. Don't rely on it.

### Smooth motion (sweep without snapping)

```cpp
// Move at controlled speed instead of full slew rate:
void moveTo(Servo &s, int fromUs, int toUs, int stepUs, int stepDelayMs) {
  int dir = (toUs > fromUs) ? 1 : -1;
  for (int us = fromUs; dir * (toUs - us) > 0; us += dir * stepUs) {
    s.writeMicroseconds(us);
    delay(stepDelayMs);          // 15-20ms ≈ one frame; smaller is pointless at 50Hz
  }
  s.writeMicroseconds(toUs);
}
// Non-blocking version: do one step per loop() pass using millis() timing.
```

A step smaller than the frame period changes nothing — the servo samples one pulse per 20ms frame. Effective speed = stepUs / stepDelayMs.

## 4. Code — MicroPython

### Raspberry Pi Pico (RP2040/RP2350)

```python
from machine import Pin, PWM

class ServoPico:
    # Calibrate MIN_US/MAX_US per unit. 500/2400 is the SG90 family typical.
    def __init__(self, pin, min_us=500, max_us=2400):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)                 # 20ms frame
        self.min_us, self.max_us = min_us, max_us

    def write_us(self, us):
        us = max(self.min_us, min(self.max_us, us))
        # duty_u16: 65535 = 100% of 20000us frame
        self.pwm.duty_u16(int(us * 65535 / 20000))

    def write_angle(self, deg):
        span = self.max_us - self.min_us
        self.write_us(self.min_us + int(span * deg / 180))

    def detach(self):                     # stop pulses -> servo goes limp, jitter stops
        self.pwm.duty_u16(0)

s = ServoPico(15)
s.write_angle(90)
```

- RP2040 PWM: 8 slices × 2 channels. **Two pins on the same slice share frequency** — fine for servos (all 50Hz), but don't mix a 50Hz servo and a 25kHz motor PWM on the same slice (GPIO N and N+1 where N even = same slice pair... specifically GPIO pairs (0,1),(2,3),... share slices).
- `duty_u16` resolution at 50Hz on RP2040 is excellent (~3800 steps across 500–2400µs) — no precision concerns.

### ESP32 MicroPython

```python
from machine import Pin, PWM
pwm = PWM(Pin(13), freq=50)

def write_us(pwm, us):
    pwm.duty_u16(int(us * 65535 / 20000))   # MicroPython >=1.20 has duty_u16 on ESP32

write_us(pwm, 1500)
# Older firmware only has duty() with 10-bit resolution: duty = us * 1024 // 20000
# -> only ~97 steps across full range = visibly steppy motion. Prefer duty_u16 / duty_ns.
pwm.duty_ns(1500_000)  # cleanest: pulse width directly in nanoseconds
```

- `duty_ns()` is the most readable and least error-prone API where available (sets pulse width directly).
- ESP32 brownout during servo spikes manifests as a silent reboot mid-script — check power before debugging code.

## 5. Continuous-rotation servos (FS90R, SG90-CR, modified MG996R)

**A continuous-rotation "servo" is not a positional device. The pulse commands SPEED and DIRECTION, not angle.** The internal pot is replaced by a fixed divider; the control loop never satisfies, so the motor spins.

| Pulse | Behavior |
|---|---|
| 1500µs | Stop (in theory) |
| <1500µs | Rotate one direction; further from 1500 = faster |
| >1500µs | Rotate other direction; further from 1500 = faster |
| ~1400 / ~1600µs | Near full speed already — speed curve is very steep, usable proportional band is only ±~80µs |

```cpp
Servo wheel;
wheel.attach(9);
wheel.writeMicroseconds(1500);  // stop — but see trim below
wheel.writeMicroseconds(1430);  // ~moderate speed, direction A
```

Critical facts:
- **The stop point is almost never exactly 1500µs.** FS90R has a trim potentiometer on the case — command 1500µs and turn the trim until it stops. Without trim, store a per-unit `STOP_US` calibration constant (find it by scanning 1480–1520).
- `write(90)` = stop, `write(0)`/`write(180)` = full speed opposite directions — but degree-based API on a speed device produces confusing code; always use `writeMicroseconds`.
- No odometry: you cannot know how far it has turned. For dead reckoning, add wheel encoders or time-based estimation (poor).
- To stop reliably and silently: send `STOP_US` for a few frames, then `detach()` — guarantees no creep from a miscalibrated stop point.

## 6. The five mistakes everyone makes

1. **Powering servos from the board's 5V pin.** Causes resets, jitter, brownouts, USB dropouts. External supply + common ground. (Exception: one SG90, briefly, unloaded, on a barrel-jack-powered Uno — works but is a habit that bites later.)
2. **Assuming 1000–2000µs full range.** Real range is ~500–2400µs; the default gives you ~half the travel. Pass explicit min/max to `attach()` or use `writeMicroseconds` with calibrated endpoints.
3. **No delay after `write()`.** The call returns instantly; the servo takes 0.1–0.5s to arrive. Sequencing moves without travel time = only the last command visibly executes; grabbing with a gripper before it arrives = dropped object.
4. **Driving into mechanical stops / past calibrated endpoints.** Continuous stall current (650mA SG90, 2.5A MG996R), heat, stripped plastic gears, sagging rail. Clamp commanded pulse to calibrated endpoints in software, always.
5. **Treating a continuous-rotation servo as positional** (writing "angles" expecting it to go there) — it spins forever. Conversely, expecting a positional servo to rotate continuously — it slams into its internal stop.

Bonus #6: forgetting common ground with the external supply — servo twitches randomly or ignores signal entirely. Bonus #7: on AVR, wondering why `analogWrite` on pin 9/10 stopped working after including `Servo.h`.

## 7. Multi-servo systems

- 1–12 servos on AVR: `Servo.h` (software-timed off Timer1, jitter ~ a few µs, fine for hobby use).
- ESP32: `ESP32Servo`, one LEDC channel each (hardware PWM, jitter-free), practical limit ~16 (8 on C3).
- **>8 servos or busy MCU: use a PCA9685 16-channel I2C PWM board.** It generates all pulses in hardware; MCU just writes registers. Caveats:
  - PCA9685 internal oscillator is nominally 25MHz but varies ±5–10% per board → pulse widths are off proportionally. Calibrate: set 50Hz, measure actual frame with a scope or logic analyzer, or empirically trim `setOscillatorFrequency()` (Adafruit lib) until 1500µs measures true.
  - 12-bit resolution at 50Hz = 4096 ticks / 20ms = **4.88µs per tick** — adequate (≈0.4° steps).
  - V+ servo rail on the PCA9685 board: feed it from your external supply (it has a terminal block + reverse-polarity protected on Adafruit version); the green terminal handles ~constant 10A claims poorly — for many MG996R, wire power to servos directly and use the board only for signals.
- **Stagger startup.** Attaching 6 servos simultaneously at boot makes all of them slew to their first commanded position at once — worst-case combined inrush. Attach + move them one at a time with 100–200ms gaps.

## 8. Debugging checklist (in order)

1. **Servo twitches/jitters or MCU resets when servo moves** → shared power. Move servo to external supply, verify common ground, add 470µF across servo rail.
2. **Servo does nothing** → check common ground first; then confirm signal pin actually outputs pulses (LED + resistor blinks dimly at 50Hz, or scope); then confirm supply ≥4.8V *under load* (multimeter on servo V+ while commanding movement — sag below 4.5V = supply inadequate).
3. **Only moves ~90–120° total** → using 1000–2000µs range. Widen to calibrated ~500–2400µs.
4. **Buzzes/vibrates at rest** → holding position against load or commanded past endpoint; either reduce load, back off pulse 20–40µs from the stop, or `detach()` if holding torque isn't needed.
5. **Moves to wrong/erratic positions** → frame rate wrong (check PWM freq is 50Hz, not 490Hz Arduino `analogWrite` default — never use raw `analogWrite` for servos on AVR); or long signal wire (>50cm) picking up noise — add 220–330Ω series resistor at the MCU pin and twist signal with ground.
6. **Continuous servo creeps when "stopped"** → stop point ≠ 1500µs. Adjust case trim pot or calibrate `STOP_US`, or detach after stopping.
7. **Works on USB power bench test, fails in robot** → battery sag under combined motor+servo load. Scope or log the 5V rail; separate servo BEC from logic BEC.
8. **Servo gets hot at idle** → commanded against a stop or carrying static load. Re-check endpoint clamps; consider a higher-torque servo or counterspring.
9. **ESP32 reboots with brownout message** → power, not code. See item 1.
10. **MG996R "dead" after a stall event** → stripped gear (metal gears still strip the final output gear's mating part) or burnt pot track. Open it: gear teeth visible damage = replace gear set (~£3) or servo.
