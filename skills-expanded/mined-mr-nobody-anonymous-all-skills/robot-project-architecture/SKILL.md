---
name: robot-project-architecture
description: "Use when starting any robot codebase, restructuring a messy robot project, or reviewing robot code organization. Provides the HAL (Hardware Abstraction Layer) pattern, pin/threshold constant conventions, behavior-vs-driver separation, simulation-first development, mock-sensor testing harnesses, and the wiring-photo README standard — for MicroPython, Arduino C++, and ROS 2 Python projects."
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


# Robot Project Architecture

The #1 cause of unmaintainable robot code is mixing three concerns in one file:
**what pin things are on**, **how to talk to hardware**, and **what the robot decides to do**.
This skill enforces the separation that lets you swap a sensor, change a pin, or run the
whole brain on a laptop without touching behavior logic.

## The Three-Layer Rule (non-negotiable)

```
┌─────────────────────────────────────────────┐
│  BEHAVIOR LAYER        behaviors/*.py       │  "follow the line", "avoid the wall"
│  knows: distances(cm), speeds(-1.0..1.0)    │  NEVER imports machine/RPi.GPIO/Wire
├─────────────────────────────────────────────┤
│  HAL / DRIVER LAYER    drivers/*.py         │  "set PWM duty", "read ADC, convert to cm"
│  knows: registers, pulses, duty cycles      │  NEVER contains decisions or thresholds
├─────────────────────────────────────────────┤
│  CONFIG LAYER          config.py / pins.h   │  pin numbers, calibration, thresholds
│  knows: numbers only — zero logic           │  the ONLY file that changes when you rewire
└─────────────────────────────────────────────┘
```

Litmus tests:
- Can you change `TRIG_PIN = 5` to `TRIG_PIN = 17` by editing exactly one line in one file? If not, fail.
- Can you run the behavior layer on a desktop with `python -m pytest` and zero hardware attached? If not, fail.
- Does any behavior file contain the number `65535`, `1023`, or a register address? Fail — that's driver leakage.

## Canonical Directory Layouts

### MicroPython (Pico/ESP32)

```
robot/
├── README.md            # MUST contain wiring photo + table (see below)
├── config.py            # ALL pins, calibration constants, thresholds
├── main.py              # boot entry: wires drivers → behavior, runs loop
├── drivers/
│   ├── motors.py        # DRV8833/L298N/TB6612 PWM driver
│   ├── ultrasonic.py    # HC-SR04 echo timing
│   ├── line_sensors.py  # TCRT5000 array ADC reads
│   └── imu.py           # MPU6050 I2C
├── behaviors/
│   ├── line_follow.py   # pure logic, takes sensor values, returns motor commands
│   └── avoid.py
├── mocks/
│   ├── mock_motors.py   # same interface as drivers/motors.py, records calls
│   └── mock_ultrasonic.py
└── tests/
    └── test_line_follow.py   # runs on DESKTOP python, uses mocks
```

### Arduino C++ (PlatformIO — use it; Arduino IDE flat-folder is a dead end past 200 lines)

```
robot/
├── README.md
├── platformio.ini
├── include/
│   └── config.h         # ALL #define PIN_xxx, thresholds, calibration
├── lib/
│   ├── Motors/          # Motors.h/.cpp — class with setSpeed(float l, float r)
│   ├── Ultrasonic/
│   └── LineArray/
├── src/
│   ├── main.cpp         # setup(): construct drivers; loop(): behavior tick
│   └── behaviors/
│       ├── LineFollow.h/.cpp
│       └── Avoid.h/.cpp
└── test/
    └── test_line_follow/test_main.cpp   # pio test -e native (desktop)
```

### ROS 2 (Python, Humble/Jazzy)

```
robot_ws/src/
├── robot_bringup/       # launch files + YAML params (this IS the config layer)
│   ├── launch/robot.launch.py
│   └── config/params.yaml      # pins, topics, rates, thresholds
├── robot_drivers/       # nodes that touch hardware, publish sensor_msgs
│   ├── motor_node.py    # subscribes /cmd_vel, drives GPIO
│   └── sonar_node.py    # publishes sensor_msgs/Range
├── robot_behaviors/     # nodes with ZERO hardware imports
│   └── wall_follow_node.py     # subscribes /range, publishes /cmd_vel
└── robot_sim/           # Gazebo/mock publishers for desktop dev
```

ROS 2 enforces the HAL boundary for you via topics: behavior nodes talk `geometry_msgs/Twist`
and `sensor_msgs/Range`, never GPIO. If a behavior node imports `RPi.GPIO`, the architecture
is broken.

## Layer 1: config.py — Numbers Only

Every pin, every threshold, every calibration constant. Grouped, commented with WHY.

```python
# config.py — Pico W line follower. Edit pins here ONLY. See README wiring photo.

# ── Motor driver: TB6612FNG ──────────────────────────────────────
# VM = 6V battery pack, VCC = Pico 3V3, STBY tied HIGH to 3V3
PIN_MOTOR_L_PWM  = 16   # PWMA
PIN_MOTOR_L_IN1  = 17   # AIN1
PIN_MOTOR_L_IN2  = 18   # AIN2
PIN_MOTOR_R_PWM  = 19   # PWMB
PIN_MOTOR_R_IN1  = 20   # BIN1
PIN_MOTOR_R_IN2  = 21   # BIN2
MOTOR_PWM_FREQ   = 20_000   # 20 kHz: above audible whine; TB6612 max 100 kHz
MOTOR_DEADBAND   = 0.12     # duty below this, motors stall and buzz — measured

# ── HC-SR04 ultrasonic ───────────────────────────────────────────
# ECHO is 5V! Divider: 1k from ECHO, 2k to GND, tap to pin (3.3V ≈ 5×2/3)
PIN_TRIG = 3
PIN_ECHO = 2
SONAR_TIMEOUT_US = 30_000   # 30 ms ≈ 5 m max range; prevents infinite blocking

# ── TCRT5000 line array (3x analog) ─────────────────────────────
PIN_LINE_L = 26   # ADC0
PIN_LINE_C = 27   # ADC1
PIN_LINE_R = 28   # ADC2
# Calibrated 2026-06-01 on matte black tape / white foam board:
LINE_BLACK_RAW = 48_000   # u16 reading on tape
LINE_WHITE_RAW = 9_000    # u16 reading on board
LINE_THRESHOLD = 28_000   # midpoint-ish; re-run calibrate.py if surface changes

# ── Behavior tuning ──────────────────────────────────────────────
BASE_SPEED   = 0.55
TURN_GAIN    = 0.8     # P gain for line follow
STOP_DIST_CM = 12.0
LOOP_HZ      = 50
```

Arduino equivalent — `include/config.h`:

```cpp
#pragma once
// Pins ONLY change here. Wiring photo in README.md.

// TB6612FNG — VM=6V pack, VCC=5V, STBY→5V
constexpr uint8_t PIN_MOTOR_L_PWM = 5;    // must be PWM-capable (UNO: 3,5,6,9,10,11)
constexpr uint8_t PIN_MOTOR_L_IN1 = 4;
constexpr uint8_t PIN_MOTOR_L_IN2 = 7;
constexpr uint8_t PIN_MOTOR_R_PWM = 6;
constexpr uint8_t PIN_MOTOR_R_IN1 = 8;
constexpr uint8_t PIN_MOTOR_R_IN2 = 12;

// HC-SR04 — ECHO through 1k/2k divider (UNO is 5V-tolerant but keep habit)
constexpr uint8_t PIN_TRIG = 9;
constexpr uint8_t PIN_ECHO = 10;
constexpr unsigned long SONAR_TIMEOUT_US = 30000UL;

constexpr float STOP_DIST_CM = 12.0f;
constexpr float BASE_SPEED   = 0.55f;     // -1.0 .. 1.0, mapped to 0-255 in driver
constexpr uint16_t LOOP_PERIOD_MS = 20;   // 50 Hz
```

Rules:
- **Use `constexpr`, not `#define`** in C++ (type-checked, scoped). MicroPython: plain module constants.
- Every calibrated number gets a date + surface comment. Thresholds rot.
- Voltage-divider and level-shift notes live next to the pin they protect.
- Never duplicate a constant. If two files need `STOP_DIST_CM`, both import config.

## Layer 2: Drivers — Hardware In, Physics Out

A driver converts hardware weirdness into SI-ish units and a clean interface. It takes
config values via constructor — **drivers never import config directly** (this is what
makes them mockable and reusable across robots).

### Motor driver pattern (MicroPython, TB6612/DRV8833)

```python
# drivers/motors.py
from machine import Pin, PWM

class Motors:
    """Differential drive. Speeds are -1.0..1.0. Handles deadband + sign."""

    def __init__(self, l_pwm, l_in1, l_in2, r_pwm, r_in1, r_in2,
                 freq=20_000, deadband=0.1):
        self._l = (PWM(Pin(l_pwm), freq=freq), Pin(l_in1, Pin.OUT), Pin(l_in2, Pin.OUT))
        self._r = (PWM(Pin(r_pwm), freq=freq), Pin(r_in1, Pin.OUT), Pin(r_in2, Pin.OUT))
        self._deadband = deadband
        self.stop()

    def set(self, left, right):
        self._one(self._l, left)
        self._one(self._r, right)

    def _one(self, ch, speed):
        pwm, in1, in2 = ch
        speed = max(-1.0, min(1.0, speed))
        if abs(speed) < self._deadband:
            in1.value(0); in2.value(0)          # coast
            pwm.duty_u16(0)
            return
        in1.value(1 if speed > 0 else 0)
        in2.value(0 if speed > 0 else 1)
        # remap deadband..1.0 → deadband..1.0 duty so low commands still move
        pwm.duty_u16(int(abs(speed) * 65535))

    def stop(self):
        self.set(0, 0)

    def brake(self):                              # short-brake: both inputs HIGH
        for _, in1, in2 in (self._l, self._r):
            in1.value(1); in2.value(1)
```

### Sensor driver pattern (HC-SR04, non-blocking-ish)

```python
# drivers/ultrasonic.py
from machine import Pin, time_pulse_us
import time

class Ultrasonic:
    """Returns cm, or None on timeout/out-of-range. Never raises in the loop."""

    def __init__(self, trig, echo, timeout_us=30_000):
        self._trig = Pin(trig, Pin.OUT, value=0)
        self._echo = Pin(echo, Pin.IN)
        self._timeout = timeout_us

    def read_cm(self):
        self._trig.value(0); time.sleep_us(2)
        self._trig.value(1); time.sleep_us(10)   # datasheet: >=10 µs trigger
        self._trig.value(0)
        t = time_pulse_us(self._echo, 1, self._timeout)
        if t < 0:
            return None                           # -1 timeout-high, -2 timeout-low
        return (t * 0.0343) / 2                   # 343 m/s at 20°C
```

Driver rules:
- Constructor takes pins/params; no module-level Pin() objects (kills testability,
  and on import order can fire GPIO before you're ready).
- Return `None` (or `std::optional` / NaN in C++) for sensor failure — never raise inside
  the control loop, never return a fake "999 cm" that behavior code will treat as real.
- All unit conversion happens HERE. Behavior code sees cm, m/s, degrees — never µs or raw ADC.
- One physical device per class. A "Robot" god-class that owns everything is the
  second-most-common architecture failure.

## Layer 3: Behaviors — Pure Functions Over State

A behavior takes sensor readings and elapsed time, returns actuator commands.
No hardware imports. No sleeps. No global state if you can avoid it.

```python
# behaviors/line_follow.py — desktop-testable, zero hardware imports

class LineFollow:
    def __init__(self, base_speed, turn_gain, threshold):
        self._base = base_speed
        self._gain = turn_gain
        self._thr = threshold
        self._last_error = 0   # remember direction when line lost

    def step(self, left_raw, center_raw, right_raw):
        """Returns (left_speed, right_speed) in -1.0..1.0."""
        on = lambda v: v > self._thr
        if on(center_raw) and not on(left_raw) and not on(right_raw):
            error = 0.0
        elif on(left_raw):
            error = -1.0
        elif on(right_raw):
            error = 1.0
        else:
            # line lost: spin toward last known side
            error = 2.0 if self._last_error >= 0 else -2.0
        if error:
            self._last_error = error
        turn = self._gain * error
        return (self._base + turn, self._base - turn)
```

```python
# main.py — the ONLY file that knows about all three layers
import time
import config as C
from drivers.motors import Motors
from drivers.line_sensors import LineArray
from drivers.ultrasonic import Ultrasonic
from behaviors.line_follow import LineFollow

motors = Motors(C.PIN_MOTOR_L_PWM, C.PIN_MOTOR_L_IN1, C.PIN_MOTOR_L_IN2,
                C.PIN_MOTOR_R_PWM, C.PIN_MOTOR_R_IN1, C.PIN_MOTOR_R_IN2,
                freq=C.MOTOR_PWM_FREQ, deadband=C.MOTOR_DEADBAND)
lines  = LineArray(C.PIN_LINE_L, C.PIN_LINE_C, C.PIN_LINE_R)
sonar  = Ultrasonic(C.PIN_TRIG, C.PIN_ECHO, C.SONAR_TIMEOUT_US)
brain  = LineFollow(C.BASE_SPEED, C.TURN_GAIN, C.LINE_THRESHOLD)

PERIOD_MS = 1000 // C.LOOP_HZ
try:
    while True:
        t0 = time.ticks_ms()
        d = sonar.read_cm()
        if d is not None and d < C.STOP_DIST_CM:
            motors.stop()
        else:
            l, c, r = lines.read()
            motors.set(*brain.step(l, c, r))
        # fixed-rate loop: sleep the REMAINDER, not a constant
        dt = time.ticks_diff(time.ticks_ms(), t0)
        time.sleep_ms(max(0, PERIOD_MS - dt))
except BaseException:
    motors.stop()      # ALWAYS stop motors on crash/Ctrl-C — runaway robots are real
    raise
```

The `try/except BaseException: motors.stop()` wrapper is mandatory in every main loop.
KeyboardInterrupt does not stop PWM on a Pico — the robot keeps driving with no brain.

### Arduino loop timing — never use bare delay()

```cpp
// src/main.cpp
#include "config.h"
#include <Motors.h>
#include <Ultrasonic.h>
#include "behaviors/LineFollow.h"

Motors motors(PIN_MOTOR_L_PWM, PIN_MOTOR_L_IN1, PIN_MOTOR_L_IN2,
              PIN_MOTOR_R_PWM, PIN_MOTOR_R_IN1, PIN_MOTOR_R_IN2);
Ultrasonic sonar(PIN_TRIG, PIN_ECHO, SONAR_TIMEOUT_US);
LineFollow brain(BASE_SPEED, 0.8f, 600);

unsigned long lastTick = 0;

void setup() {
    Serial.begin(115200);
    motors.begin();          // GPIO setup in begin(), NOT in constructor —
}                            // constructors run before init() configures the chip

void loop() {
    unsigned long now = millis();
    if (now - lastTick < LOOP_PERIOD_MS) return;   // fixed-rate, non-blocking
    lastTick = now;

    float d = sonar.readCm();                       // NAN on timeout
    if (!isnan(d) && d < STOP_DIST_CM) { motors.stop(); return; }

    auto cmd = brain.step(analogRead(A0), analogRead(A1), analogRead(A2));
    motors.set(cmd.left, cmd.right);
}
```

Critical Arduino rule: **hardware init goes in `begin()`, not constructors.** Global object
constructors run before the Arduino core initializes timers/GPIO; `pinMode` in a constructor
silently does nothing on some cores (notably ESP32 pre-2.x and some STM32 cores).

## Simulation-First Development

Order of operations for any new behavior — this saves hours of chasing "bugs" that are
actually logic errors:

1. **Write the behavior class** (pure logic).
2. **Write a desktop test** with hand-picked sensor values.
3. **Write a tiny step simulator** if the behavior has feedback dynamics (PID, wall follow).
4. Only THEN flash to hardware.

A 20-line simulator is enough for most differential-drive behaviors:

```python
# tests/test_line_follow.py — runs with plain `pytest` on your laptop
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from behaviors.line_follow import LineFollow

BLACK, WHITE = 48_000, 9_000

def make():
    return LineFollow(base_speed=0.5, turn_gain=0.8, threshold=28_000)

def test_centered_goes_straight():
    l, r = make().step(WHITE, BLACK, WHITE)
    assert abs(l - r) < 1e-6

def test_line_on_left_turns_left():
    l, r = make().step(BLACK, WHITE, WHITE)
    assert l < r        # left wheel slower → turns left

def test_line_lost_spins_toward_last_seen():
    b = make()
    b.step(BLACK, WHITE, WHITE)          # saw it on the left
    l, r = b.step(WHITE, WHITE, WHITE)   # now lost
    assert l < r                          # keeps turning left
```

The MicroPython gotcha: `machine` doesn't exist on desktop. Because behaviors never import
it, tests just work. If you need to test a driver's math (e.g., µs→cm), extract the pure
function:

```python
# in drivers/ultrasonic.py
def us_to_cm(t_us):           # module-level pure function — testable
    return (t_us * 0.0343) / 2
```

For Arduino, PlatformIO native tests do the same job:

```ini
; platformio.ini
[env:pico]
platform = raspberrypi
board = pico
framework = arduino

[env:native]                  ; pio test -e native — runs on your PC
platform = native
build_flags = -std=c++17
```

Keep behaviors in `lib/` or compile them into the native env; guard any Arduino.h usage
with `#ifdef ARDUINO`.

## Mock Drivers — Same Interface, Records Calls

Mocks let you run the **entire main loop** on a desk with the robot held in the air, or
with no robot at all. The contract: a mock implements the exact public interface of the
real driver.

```python
# mocks/mock_motors.py
class MockMotors:
    def __init__(self, *args, **kwargs):
        self.history = []           # list of (left, right) commands
    def set(self, left, right):
        self.history.append((left, right))
    def stop(self):
        self.history.append((0, 0))
    def brake(self):
        self.history.append(("BRAKE",))

# mocks/mock_ultrasonic.py
class MockUltrasonic:
    def __init__(self, readings):
        self._readings = iter(readings)   # scripted scenario
    def read_cm(self):
        return next(self._readings, None)
```

Scenario test of the full safety logic, no hardware:

```python
def test_emergency_stop_fires():
    sonar = MockUltrasonic([50.0, 30.0, 10.0])   # robot approaches wall
    motors = MockMotors()
    for _ in range(3):
        d = sonar.read_cm()
        if d is not None and d < 12.0:
            motors.stop()
        else:
            motors.set(0.5, 0.5)
    assert motors.history[-1] == (0, 0)
```

Selection between real and mock belongs in main, one place, via try-import:

```python
# main.py top
try:
    from drivers.motors import Motors          # fails on desktop: no `machine`
except ImportError:
    from mocks.mock_motors import MockMotors as Motors
    print("SIM MODE — mock motors")
```

This makes `python main.py` on a laptop a smoke test of your whole wiring graph.

## The Wiring-Photo README (every robot repo, no exceptions)

Six months from now, the robot is in a box and nobody remembers which white wire went
where. The README must contain, in this order:

1. **A photo of the actual wiring** (`docs/wiring.jpg`), taken from above, in focus,
   BEFORE you close the chassis. Re-take it every time wiring changes. A Fritzing diagram
   is a bonus, not a substitute — diagrams show intent, photos show truth.
2. **The wiring table** — the single source of truth alongside config:

```markdown
## Wiring (matches config.py — photo: docs/wiring.jpg)

| Device       | Device pin | MCU pin (GP#) | Notes                                  |
|--------------|-----------|---------------|----------------------------------------|
| TB6612FNG    | PWMA      | GP16          |                                        |
| TB6612FNG    | AIN1/AIN2 | GP17 / GP18   |                                        |
| TB6612FNG    | PWMB      | GP19          |                                        |
| TB6612FNG    | BIN1/BIN2 | GP20 / GP21   |                                        |
| TB6612FNG    | VM        | —             | 6V pack +, through switch + 5A fuse    |
| TB6612FNG    | VCC, STBY | 3V3           | STBY must be HIGH or nothing moves     |
| HC-SR04      | VCC       | VBUS (5V)     | sensor needs 5V supply                 |
| HC-SR04      | TRIG      | GP3           | 3.3V trigger works fine                |
| HC-SR04      | ECHO      | GP2           | via 1k/2k divider — ECHO is 5V out!    |
| TCRT5000 ×3  | OUT       | GP26/27/28    | ADC0/1/2                               |
| All grounds  | GND       | GND           | COMMON GROUND incl. motor pack         |
```

3. **Power section**: battery chemistry, voltage, what powers what, where the fuse is,
   and the sentence "motor power and logic power share ground but NOT positive rails."
4. **How to run**: flash command, calibration script, expected behavior on power-up.
5. **Calibration log**: date, surface, values (matches the comments in config).

## Mistakes Everyone Makes (architecture edition)

| Mistake | Symptom | Fix |
|---|---|---|
| Pins scattered across files | Rewire = 6-file hunt, one missed = "broken sensor" | Single config file, grep for `Pin(`/`pinMode` to verify nothing bypasses it |
| Thresholds inside behavior code | Re-tuning requires reflashing + hunting magic numbers | All tunables in config; behaviors take them as constructor args |
| Behavior reads GPIO directly | Can't test, can't sim, sensor swap rewrites the brain | Behavior takes values, returns commands. Period. |
| God `Robot` class owning everything | 800-line file, circular state, untestable | One class per device + thin composition in main |
| `delay(500)` / `time.sleep(0.5)` in loop | Sonar misses obstacles while sleeping; button presses lost | Fixed-rate loop with remainder-sleep (MicroPython) or millis() gate (Arduino) |
| Hardware init in C++ constructors | Pins "configured" before core init; works on UNO, dead on ESP32 | `begin()` method called from `setup()` |
| No motor-stop on exception | Crash → robot drives into wall at last commanded speed | `try/finally motors.stop()` around the loop; Arduino: watchdog + driver STBY pin |
| Sensor failure returns magic number (999) | Behavior treats 999 cm as "all clear" at the worst moment | Return None/NaN, handle explicitly in main |
| Calibration values hardcoded with no provenance | Robot works at home, fails at the competition venue lighting | Date + surface comment, plus a `calibrate.py` that prints config-ready lines |
| README has Fritzing but no photo | Diagram says GP5, actual wire on GP6 since March | Photo of real wiring, retaken on every change |
| Copy-pasting driver code between robots | Bug fixed in one robot, alive in three others | Drivers take pins via constructor → reusable as-is; consider a shared `drivers/` repo |
| Testing only on hardware | 45-minute flash-observe-guess cycles for a sign error | Desktop tests for behaviors first; hardware only validates the HAL |

## Debugging Checklist — "It compiles but the robot does nothing right"

Work the layers bottom-up. Never debug behavior logic until layers below are proven.

**Layer 0 — Power (do this FIRST, always):**
- [ ] Common ground between MCU, motor driver, and every sensor? (No common ground = readings that drift with motor load — the classic.)
- [ ] Motor supply sags under load? Measure battery voltage WHILE motors run. Below ~4.5V on a "6V" pack, brownouts reset the MCU mid-run (symptom: robot "reboots randomly").
- [ ] Logic powered from USB while motors on battery? Fine — but ground must still be common.

**Layer 1 — Config matches reality:**
- [ ] Open the wiring photo. Compare against config, pin by pin. (2 minutes; finds ~30% of "driver bugs".)
- [ ] Pin numbering scheme right? Pico GP numbers ≠ physical pins. ESP32 GPIO ≠ board silkscreen D-numbers.

**Layer 2 — Drivers in isolation (write `tools/test_motors.py` etc., keep them in the repo):**
- [ ] Motors: command (0.5, 0.5) with wheels OFF the ground. Both spin? Same direction? If one is reversed, swap its IN1/IN2 in config (or motor wires) — do NOT negate speeds in behavior code.
- [ ] Sonar: print `read_cm()` at 10 Hz, move your hand 10/20/50 cm. Values sane and stable ±1 cm?
- [ ] Line sensors: print raw values on tape vs. board. Is the gap > 3× the noise? If not, fix sensor height (TCRT5000 sweet spot: 2–10 mm) before touching the threshold.

**Layer 3 — Behavior on desktop:**
- [ ] Feed the exact raw values you just printed into the behavior test. Does it command what you expect? Sign errors (left/right swapped, error negated) live here and are invisible on hardware.

**Layer 4 — Integration:**
- [ ] Loop rate actual vs. target: print `dt` for 100 ticks. If a 50 Hz loop runs at 11 Hz, something blocks (usually sonar timeout or `print` over slow serial).
- [ ] Robot on a stand, run full stack, watch printed commands while you move stimuli by hand. Only when this is right does it touch the floor.

## Scaling Up: When to Add More Structure

Don't add these on day one. Add them at the trigger point:

- **State machine** — when main has 3+ `if mode ==` branches. Pattern: dict of
  `state -> step_fn`, each returns next state. Not a framework, 15 lines.
- **Event/command queue** — when adding a second input source (radio, button, serial cmd).
- **ROS 2** — when you have: multiple compute units, OR need nav/SLAM stacks, OR a team
  > 2 people. NOT for a single-MCU line follower; the overhead is real.
- **Logging to flash/SD** — first time you say "it failed but I didn't see why." Log
  `(t, sensors, command, state)` as CSV; replay through the behavior on desktop — this
  is the highest-leverage debugging tool in hobby robotics.

```python
# replay.py — desktop: re-run the brain over a real logged run
import csv
from behaviors.line_follow import LineFollow
brain = LineFollow(0.55, 0.8, 28_000)
with open("run_014.csv") as f:
    for t, l, c, r, cmd_l, cmd_r in csv.reader(f):
        new_l, new_r = brain.step(int(l), int(c), int(r))
        if abs(new_l - float(cmd_l)) > 0.01:
            print(f"t={t}: logged {cmd_l} vs new code {new_l:.2f}")
```

## New-Robot Checklist (copy into the first issue/commit)

- [ ] Directory layout from this skill (config / drivers / behaviors / mocks / tests / tools)
- [ ] config file with grouped, commented constants — pins verified against actual wiring
- [ ] One driver per device; constructor-injected pins; failure → None/NaN
- [ ] `begin()` pattern (Arduino) / no module-level Pin objects (MicroPython)
- [ ] Behaviors import nothing hardware-related — verified by running pytest on desktop
- [ ] Mock for every driver; main falls back to mocks on ImportError
- [ ] Motor-stop on any exception in main loop
- [ ] Fixed-rate loop (remainder sleep / millis gate), rate printed at boot
- [ ] `tools/` scripts: motor test, sensor print, calibrate (prints config-ready lines)
- [ ] README: wiring PHOTO, wiring table, power section, run instructions, calibration log
- [ ] First commit before any behavior work: drivers + tools proven on hardware
