---
name: obstacle-state-machines
description: "Use when writing obstacle-avoidance, wall-following, or maze-navigation code for wheeled robots with ultrasonic/IR sensors. Provides finite-state-machine architecture (enum states, transition tables, non-blocking millis()/asyncio patterns), single-sensor wall following with P-control, Bug-0/1/2 algorithms, ultrasonic failure modes on soft/angled surfaces, and the delay()-kills-responsiveness fix."
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


# Obstacle Avoidance State Machines & Wall Following

Expert reference for writing robot navigation FSMs that work first try. Covers
Arduino C++ (UNO/Nano/ESP32) and MicroPython (Pico/ESP32), plus ROS2 notes.

---

## 1. The Core Rule: Never Block

A robot control loop must run at **20–100 Hz** (10–50 ms per iteration). Every
`delay(500)` is 500 ms during which:

- the sensor is not read (robot travels 10 cm at 0.2 m/s — into the wall),
- the motors keep doing whatever they were last told,
- the kill switch / serial commands are ignored.

**`delay()` is only acceptable for the HC-SR04 inter-ping settle (≥ 29 ms is
the spec; 60 ms between pings prevents echo cross-talk) — and even that should
be a millis() gate, not a delay.**

### Loop budget table (typical 2-wheel differential robot)

| Item | Time | Notes |
|---|---|---|
| HC-SR04 ping (4 m max range) | up to 23.5 ms blocking in `pulseIn` | set timeout! default `pulseIn` timeout is 1 s |
| HC-SR04 ping with 30000 µs timeout | ≤ 30 ms | clamps worst case (~5 m) |
| Sharp IR analog read | ~0.1 ms | 10-bit ADC, instant |
| VL53L0X I2C read | ~1 ms (continuous mode) | use continuous, not single-shot (single-shot = 30+ ms) |
| Motor PWM update | < 0.1 ms | |
| FSM logic | < 0.1 ms | |
| Target loop period | 50 ms (20 Hz) min, 20 ms (50 Hz) good | |

If you only have one HC-SR04, ping every 60 ms and run FSM logic every loop
on the cached reading.

---

## 2. FSM Skeleton — Arduino C++ (the canonical pattern)

```cpp
// ----- States -----
enum class State : uint8_t {
  FORWARD,
  STOP_BEFORE_TURN,   // brief settle so ultrasonic isn't reading while vibrating
  BACK_UP,
  SCAN,               // optional: servo-sweep the sensor
  TURN_LEFT,
  TURN_RIGHT,
  STUCK_RECOVERY
};

State state = State::FORWARD;
unsigned long stateEntered = 0;     // millis() at last transition
unsigned long lastPing = 0;
float distCm = 999.0f;              // cached sensor value, cm
uint8_t consecutiveObstacles = 0;   // stuck detection

// ----- Transition helper: EVERY state change goes through this -----
void enterState(State s) {
  state = s;
  stateEntered = millis();
  // entry actions (set motors ONCE on entry, not every loop):
  switch (s) {
    case State::FORWARD:          driveLR(180, 180); break;   // PWM 0-255
    case State::STOP_BEFORE_TURN: driveLR(0, 0);     break;
    case State::BACK_UP:          driveLR(-150, -150); break;
    case State::TURN_LEFT:        driveLR(-160, 160); break;  // spin in place
    case State::TURN_RIGHT:       driveLR(160, -160); break;
    case State::STUCK_RECOVERY:   driveLR(-180, -120); break; // arc backward
    case State::SCAN:             driveLR(0, 0);     break;
  }
}

unsigned long inState() { return millis() - stateEntered; }

// ----- HC-SR04, non-blocking-ish (bounded pulseIn) -----
const uint8_t TRIG = 9, ECHO = 10;
float pingCm() {
  digitalWrite(TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  unsigned long us = pulseIn(ECHO, HIGH, 30000UL);  // 30 ms timeout — CRITICAL
  if (us == 0) return 999.0f;                       // timeout = no echo = treat as clear*
  return us / 58.0f;                                // 58 µs per cm round trip
}
// *see §6 — on soft/angled surfaces "no echo" can mean obstacle. If your arena
// has foam/fabric walls, treat timeout as OBSTACLE instead.

void loop() {
  unsigned long now = millis();

  // 1. Sense (rate-limited, cached)
  if (now - lastPing >= 60) {
    lastPing = now;
    float raw = pingCm();
    // median-of-3 to kill single-sample glitches:
    static float h[3] = {999, 999, 999};
    h[0] = h[1]; h[1] = h[2]; h[2] = raw;
    distCm = max(min(h[0], h[1]), min(max(h[0], h[1]), h[2]));  // median
  }

  // 2. Think + Act (transition table)
  switch (state) {
    case State::FORWARD:
      if (distCm < 20.0f) {
        consecutiveObstacles++;
        enterState(consecutiveObstacles >= 4 ? State::STUCK_RECOVERY
                                             : State::STOP_BEFORE_TURN);
      }
      break;

    case State::STOP_BEFORE_TURN:
      if (inState() >= 100) enterState(State::BACK_UP);
      break;

    case State::BACK_UP:
      if (inState() >= 350) enterState(State::TURN_RIGHT);   // or SCAN
      break;

    case State::TURN_RIGHT:
      // time-based turn: calibrate! ~400-600 ms for 90° at PWM 160 on carpet,
      // ~250-350 ms on hard floor. Battery sag changes this — see §8.
      if (inState() >= 450) {
        enterState(State::FORWARD);
        if (distCm > 40.0f) consecutiveObstacles = 0;  // genuinely clear
      }
      break;

    case State::STUCK_RECOVERY:
      if (inState() >= 900) { consecutiveObstacles = 0; enterState(State::TURN_LEFT); }
      break;

    case State::TURN_LEFT:
      if (inState() >= 450) enterState(State::FORWARD);
      break;

    case State::SCAN: /* see §5 */ break;
  }
  // NO delay() ANYWHERE in loop()
}
```

### Non-negotiable FSM rules

1. **One `enterState()` function.** Motors are commanded on *entry*, states are
   pure timers/conditions after that. Scattered `analogWrite` calls inside
   conditions = states fighting each other.
2. **Every state records its entry time.** All "do X for N ms" becomes
   `inState() >= N`. Zero `delay()`.
3. **Every state must have an exit.** A state with no timeout and no sensor
   condition is a freeze. Add a max-dwell watchdog if unsure:
   `if (inState() > 5000) enterState(State::STUCK_RECOVERY);`
4. **Hysteresis on thresholds.** Stop at < 20 cm, only resume FORWARD when
   > 40 cm. A single threshold at 20/20 causes oscillation at the boundary
   (robot twitches forward/back at exactly 20 cm).
5. **Stuck counter.** Corner trap = robot alternating TURN/FORWARD forever.
   Count consecutive obstacle detections without a clear run; after 3–4,
   escalate (back up further, turn the other way, or turn 180°).

---

## 3. FSM Skeleton — MicroPython (Pico / ESP32), asyncio version

`time.sleep()` in MicroPython = `delay()` in Arduino: same disease. Use
`uasyncio` so sensor task and FSM task run concurrently.

```python
import uasyncio as asyncio
from machine import Pin, PWM, time_pulse_us
import time

# ---- Motors: DRV8833/TB6612 style, 2 PWM pins per motor ----
class Motor:
    def __init__(self, pin_a, pin_b, freq=1000):
        self.a = PWM(Pin(pin_a)); self.b = PWM(Pin(pin_b))
        self.a.freq(freq); self.b.freq(freq)
    def drive(self, speed):                 # -1.0 .. 1.0
        duty = min(65535, int(abs(speed) * 65535))
        if speed >= 0: self.a.duty_u16(duty); self.b.duty_u16(0)
        else:          self.a.duty_u16(0);    self.b.duty_u16(duty)

left  = Motor(2, 3)
right = Motor(4, 5)
def drive_lr(l, r): left.drive(l); right.drive(r)

# ---- HC-SR04 ----
trig = Pin(14, Pin.OUT); echo = Pin(15, Pin.IN)
dist_cm = 999.0

def ping():
    trig.value(0); time.sleep_us(2)
    trig.value(1); time.sleep_us(10)
    trig.value(0)
    us = time_pulse_us(echo, 1, 30000)      # returns -1/-2 on timeout
    return 999.0 if us < 0 else us / 58.0

async def sensor_task():
    global dist_cm
    hist = [999.0] * 3
    while True:
        hist = hist[1:] + [ping()]
        dist_cm = sorted(hist)[1]           # median of 3
        await asyncio.sleep_ms(60)          # echo settle between pings

# ---- FSM ----
FORWARD, BACKUP, TURN, STUCK = 0, 1, 2, 3

async def fsm_task():
    state, entered = FORWARD, time.ticks_ms()
    stuck_count = 0
    drive_lr(0.6, 0.6)

    def enter(s, l, r):
        nonlocal state, entered
        state, entered = s, time.ticks_ms()
        drive_lr(l, r)

    while True:
        dwell = time.ticks_diff(time.ticks_ms(), entered)
        if state == FORWARD:
            if dist_cm < 20:
                stuck_count += 1
                if stuck_count >= 4: enter(STUCK, -0.7, -0.4)
                else:                enter(BACKUP, -0.5, -0.5)
        elif state == BACKUP:
            if dwell >= 350: enter(TURN, 0.6, -0.6)
        elif state == TURN:
            if dwell >= 450:
                enter(FORWARD, 0.6, 0.6)
                if dist_cm > 40: stuck_count = 0
        elif state == STUCK:
            if dwell >= 900: stuck_count = 0; enter(TURN, -0.6, 0.6)
        await asyncio.sleep_ms(20)          # 50 Hz FSM

async def main():
    asyncio.create_task(sensor_task())
    await fsm_task()

asyncio.run(main())
```

MicroPython gotchas:
- `time_pulse_us` timeout returns **-1** (pulse never started) or **-2**
  (pulse didn't end) — both negative, both "no reading". Check `us < 0`.
- Use `time.ticks_diff(time.ticks_ms(), t0)` — never plain subtraction;
  `ticks_ms()` wraps (~12.4 days on most ports, but ticks_diff is the contract).
- ESP32 `PWM.duty_u16` exists in recent firmware; older builds use
  `duty(0-1023)`. Check `machine.PWM` signature for the target firmware.
- One `uasyncio` task that never `await`s starves everything — every loop body
  must contain an `await asyncio.sleep_ms(...)`.

---

## 4. Wall Following with a Single Sensor

### 4a. Side-mounted sensor, proportional control (the right way)

Mount one ultrasonic/IR on the **side** (e.g., right side for right-wall
follow), angled **10–20° forward** so it sees the wall slightly ahead — this
gives phase lead and prevents the snake-weave that a perpendicular mount
produces.

```cpp
// Right-wall follow, P-control. Target gap 15 cm.
const float TARGET = 15.0f;
const float KP = 6.0f;          // PWM counts per cm of error — start 4-8
const int   BASE = 160;         // base PWM
const int   MAX_CORR = 70;      // clamp: never let one wheel reverse

void wallFollowStep(float sideCm) {
  float err = sideCm - TARGET;            // + = too far from wall
  // Lost-wall handling: convex corner / door gap → sensor reads huge.
  // DO NOT feed 200 cm into P-control (robot whips toward wall and hits
  // the corner edge). Saturate the error instead:
  err = constrain(err, -10.0f, 10.0f);
  int corr = constrain((int)(KP * err), -MAX_CORR, MAX_CORR);
  // too far (+err) → steer right (toward wall) → slow right wheel
  driveLR(BASE + corr, BASE - corr);      // for right-side wall
}
```

Tuning order: pick BASE so robot moves briskly but controllably → raise KP
until it oscillates around the wall → halve KP. No D-term needed at < 0.3 m/s
if the sensor is angled forward; if it weaves at higher speed, add
`KD * (err - prevErr) / dt` with KD ≈ 10–20× KP·dt.

**Convex corner (wall ends):** saturated error makes the robot arc gently
toward where the wall was, naturally wrapping the corner. If your arena has
sharp 90° outer corners, add an explicit state: `if sideCm > 50 for > 300 ms
→ WRAP_CORNER state: arc with fixed differential (inner wheel ~55% of outer)
until sideCm < 25 again, then resume P-control.`

**Concave corner (wall ahead):** a single side sensor cannot see it. Options:
(1) accept the bump with a bump switch → BACK_UP+TURN state; (2) angle the
sensor 30–45° forward so closing distance shows as falling side reading —
then `if sideCm < 8 → turn away hard`; (3) add a second front sensor (best).

### 4b. Front-mounted sensor on a servo (sweep follow)

One front HC-SR04 on an SG90: point it 45° toward the wall while driving, use
4a's P-control; on obstacle suspicion, stop, sweep 0°/45°/90°/135°/180°
(servo needs **120–200 ms per 45° step** to settle — `delay`-free via a SCAN
state with sub-steps), pick widest opening. SG90: 50 Hz PWM, ~500 µs = 0°,
~2400 µs = 180°; power it from 5 V supply **not** the Arduino 5 V pin if motors
share the rail (servo stall ≈ 650 mA, brownouts reset the MCU).

### 4c. Bang-bang (only for line-of-last-resort)

`if gap < 12: steer away; elif gap > 18: steer toward; else: straight.`
Works, but weaves visibly and corner behavior is poor. The dead band
(12–18 cm) is mandatory — without it the robot oscillates at the threshold.

---

## 5. Bug Algorithms (goal-seeking with obstacles)

Prereqs: heading source (IMU yaw, e.g. MPU-6050 gyro integration or BNO055)
and position estimate (wheel-encoder odometry). Goal as (x, y) or bearing.

| Algorithm | Rule | Path quality | Memory |
|---|---|---|---|
| **Bug-0** | Head to goal; on obstacle, follow wall until you can head to goal again | Can loop forever on spirals/C-shapes | none |
| **Bug-1** | On obstacle, circumnavigate the ENTIRE obstacle, remember the point closest to goal, return to it, leave | Provably complete, very slow (worst 1× full perimeter + return) | hit point + min point |
| **Bug-2** | Draw the m-line (start→goal). Follow wall; leave when you re-cross the m-line CLOSER to goal than the hit point | Usually much shorter; can be worse than Bug-1 on bad geometry | m-line + hit distance |

Bug-2 is the practical default. FSM states:

```
GO_TO_GOAL      → turn toward goal bearing, drive; front obstacle <20cm → record
                  hit point distance-to-goal, pick wall side, → FOLLOW_WALL
FOLLOW_WALL     → run §4a wall-follow; each step check:
                  on m-line (|cross-track| < 5 cm) AND dist-to-goal < hit-dist - 10 cm
                  → GO_TO_GOAL
AT_GOAL         → dist-to-goal < 10 cm → stop
```

Implementation traps:
- **m-line crossing needs tolerance.** Odometry drift means you never hit the
  line exactly. 5 cm corridor, plus require crossing (sign change of
  cross-track error), not just proximity, or the robot leaves immediately at
  the hit point.
- **"Closer than hit point" needs margin** (the `- 10 cm`), otherwise it
  detaches at the hit point itself and re-collides instantly.
- **Heading from gyro-only drifts ~1–4°/min (MPU-6050, calibrated bias).**
  Fine for 2-minute runs; for longer use BNO055 (fused, absolute) or
  re-zero against walls.
- **Encoder odometry:** x += d·cos(θ), y += d·sin(θ) with
  d = (dL+dR)/2, θ += (dR−dL)/track_width. Update at ≥ 50 Hz. Expect 5–10 %
  position error per 10 m traveled with cheap encoders on hard floor — worse
  on carpet (wheel slip).
- ROS2: nav2 exists; hand-rolled Bug-2 belongs in a single node subscribing
  `/scan` + `/odom`, publishing `/cmd_vel` from a 20 Hz timer callback. Never
  `time.sleep()` in a callback — store state, return; use the timer as the
  FSM tick. State pattern identical to §2 with `self.state`,
  `self.state_entered = self.get_clock().now()`.

---

## 6. Ultrasonic Reality: Soft, Angled, and Weird Surfaces

HC-SR04 facts: 40 kHz, ~15° effective beam half-cone, spec range 2–400 cm,
real reliable range 2–250 cm. Speed of sound 343 m/s at 20 °C
(58 µs/cm round trip); varies ±0.6 %/°C — irrelevant for obstacle avoidance,
relevant for mapping.

### Failure modes and what the reading looks like

| Surface / geometry | What happens | Reading you get |
|---|---|---|
| **Angled hard surface > ~45° off-perpendicular** | specular reflection bounces AWAY from sensor | timeout → "no obstacle" → robot drives into the wall it can't see |
| **Soft surfaces: foam, fabric, curtains, plush toys, carpet edge** | sound absorbed, weak/no echo | timeout or intermittent ~50 % dropout |
| **Thin objects: chair legs, table legs, cables** | beam mostly misses; echo only at exact alignment | flickering: 999, 999, 34, 999 |
| **Corner (two walls meeting)** | double/triple bounce path | reads LONGER than true distance |
| **Floor, when sensor tilted down or robot pitches** | ground return | constant ~20–40 cm phantom obstacle; mount sensor level, ≥ 5 cm up |
| **Another ultrasonic robot nearby** | cross-talk | random short readings |
| **Very close (< 2 cm)** | echo arrives during ring-down | garbage or max-range |

### Mitigations (in order of value)

1. **Decide the timeout semantics per arena.** Hard-walled arena: timeout =
   clear. Foam/cloth obstacles present: timeout = **assume obstacle** after N
   consecutive timeouts while a previous reading was closing
   (`distCm` was decreasing). Encode it:

```cpp
// Soft-surface-aware: closing-then-vanished = probably absorbed echo
static float lastGood = 999;
float raw = pingCm();
if (raw > 900) {                      // timeout
    timeoutStreak++;
    if (timeoutStreak >= 3 && lastGood < 60) distCm = lastGood; // hold last
    else distCm = 999;
} else { timeoutStreak = 0; lastGood = raw; distCm = raw; }
```

2. **Median-of-3 minimum** (shown in §2) — kills single-ping glitches without
   the lag of a moving average. Never use a plain mean: one 999 in the window
   poisons it.
3. **Fuse a fallback sensor for the blind cases:** front bump switch (catches
   everything ultrasonic misses, costs $0.30) or a Sharp GP2Y0A21 IR
   (10–80 cm, sees fabric fine, hates sunlight/black surfaces — they're
   complementary failure modes).
4. **Approach angle:** if wall-following with ultrasonic, keep the sensor
   within ±30° of perpendicular to the wall. The §4a 10–20° forward tilt is
   inside this; 45° mounts give intermittent specular dropouts on smooth walls.
5. **Don't ping while turning fast** — Doppler is negligible but the beam
   sweeps, so successive readings are of different objects; the median filter
   then "sees" phantoms. Sample but down-weight (or just ignore transitions)
   during TURN states; that's why §2 re-checks `distCm` only on TURN exit.
6. **VL53L0X/VL53L1X ToF as upgrade:** immune to softness/angle (optical),
   3 cm–2 m (L0X) / 4 m (L1X), I2C, ~$2. Fails instead on: direct sunlight,
   glass (sees through or reflects), matte black (short max range). Use
   continuous mode at 20–50 Hz.

---

## 7. Wiring Quick Reference

### HC-SR04 ↔ Arduino UNO/Nano (5 V logic)

| HC-SR04 | UNO | Note |
|---|---|---|
| VCC | 5V | needs 5 V; 3.3 V supply = flaky/short range |
| TRIG | D9 (any digital) | 10 µs HIGH pulse |
| ECHO | D10 (any digital) | 5 V output — fine on UNO |
| GND | GND | common ground with motor supply, ALWAYS |

### HC-SR04 ↔ Pico/ESP32 (3.3 V logic) — **ECHO needs level shift**

ECHO outputs 5 V; Pico/ESP32 pins are not 5 V tolerant. Divider:
ECHO —[1 kΩ]—●—[2 kΩ]— GND, tap ● to GPIO (gives 3.33 V). Or buy
HC-SR04P / RCWL-1601 (3.3 V native) and skip the divider. TRIG accepts
3.3 V fine.

### Motor driver baseline

| Driver | Logic | Motor V | Cont. current | Notes |
|---|---|---|---|---|
| L298N | 5 V | 7–35 V | 2 A/ch | drops ~2.5–4 V across it — a "6 V" motor on 7.4 V LiPo through L298N sees ~4.5 V. Legacy; avoid if possible |
| TB6612FNG | 2.7–5.5 V | 4.5–13.5 V | 1.2 A/ch (3.2 A peak) | ~0.25 V drop, the sane default |
| DRV8833 | 2.7–10.8 V (shared) | same | 1.5 A/ch | great for 2×AA–2S setups |

**Power architecture that prevents 90 % of "random resets":** motors on their
own battery rail (e.g., 6×AA or 2S LiPo through driver VM); MCU on its own
regulator from the same battery; grounds tied together at ONE point; 100 µF+
electrolytic across driver VM/GND; never power motors from the Arduino 5 V
pin. Symptom of getting this wrong: MCU resets exactly when motors start or
reverse (brushed-motor inrush is 4–10× rated current).

---

## 8. Timing-Based Turns: Calibration Reality

Open-loop timed turns (the `450 ms ≈ 90°` in §2) are fine for hobby robots but:

- **Battery sag changes turn rate ~20–30 %** across a discharge cycle. Fresh
  2S LiPo (8.4 V) vs sagged (7.0 V) at the same PWM ≠ same wheel speed.
  Mitigation A: measure battery via ADC divider, scale turn time
  `t = t_nominal * V_nominal / V_measured`. Mitigation B: use the gyro —
  MPU-6050 z-rate integration over a turn is accurate to ~2–3° and immune
  to sag, carpet, and wheel slip:

```cpp
// gyro-closed turn: works on any surface, any battery level
void turnDegrees(float deg) {     // + = CCW; call from a TURN state tick
  // integrate gz (deg/s, bias-corrected) * dt each loop;
  // exit state when |accum| >= |deg| - 3 (overshoot allowance)
}
```

- **Surface matters more than people expect:** the same 450 ms turn = ~90° on
  hardwood, ~60° on medium carpet (lateral wheel scrub). Calibrate on the
  competition surface.
- **Spin-in-place vs arc:** spin (wheels opposite) is most predictable; arc
  (one wheel stopped) drags the stopped wheel and stalls more on carpet.

---

## 9. Debugging Checklist

Work top to bottom; each item isolates one layer.

**Sensor layer**
- [ ] Print `distCm` at 10 Hz over serial while moving a book toward/away by
      hand. Stable ±1 cm at 30 cm? If readings are all 0 or all timeout:
      TRIG/ECHO swapped (most common wiring error) or no common ground.
- [ ] Readings fine at rest, garbage when motors run → electrical noise:
      shared ground path / missing capacitor / sensor wires bundled with motor
      wires (separate them, twist motor pairs).
- [ ] Constant ~25 cm phantom with nothing there → sensor sees the floor or a
      robot part (wheel, standoff) at the beam edge. Re-aim, raise it.

**Actuation layer**
- [ ] With FSM disabled, command each motor forward 1 s: correct wheel,
      correct direction? Wrong direction = swap that motor's two driver
      outputs (in wiring or in `driveLR`), don't compensate in FSM logic.
- [ ] Robot curves when commanded straight: normal (motor matching ±10 %).
      Add a trim constant (`driveLR(BASE+trim, BASE-trim)`); proper fix is
      encoder PI per wheel.

**FSM layer**
- [ ] Print state name on every transition. The transcript should read like a
      story; if you see TURN→FORWARD→TURN at 5 Hz, your hysteresis is missing
      or the turn duration is too short to actually clear the obstacle.
- [ ] Robot freezes: a state with no exit condition firing. Check every state
      has timeout OR sensor exit; add the max-dwell watchdog (§2 rule 3).
- [ ] Detects obstacle but turns too late (bumps first): loop period too long
      (`delay` left somewhere? unbounded `pulseIn`?) or threshold too short
      for speed. Stopping distance ≈ v·t_loop + braking; at 0.3 m/s and 20 Hz
      sensing, 20 cm threshold is comfortable, 8 cm is not.
- [ ] Works on bench (wheels up), fails on floor → load changes motor speed;
      timed turns under-rotate. Recalibrate on the floor / go gyro-closed (§8).

**System layer**
- [ ] Random resets when motors engage → power architecture (§7). Confirm by
      running MCU from USB + motors from battery: resets stop = power issue.
- [ ] Works 5 min then degrades → battery sag (§8) or driver thermal limit
      (L298N heatsink hot = derating).

---

## 10. Anti-Patterns (instant review failures)

```cpp
// ❌ THE classic: blocking avoidance "routine"
if (distance < 20) {
  stopMotors(); delay(500);
  backward();   delay(1000);   // 1.5 s blind and deaf
  turnRight();  delay(700);
  forward();
}
// ✅ states + millis() gates (§2). Same behavior, always responsive.

// ❌ unbounded pulseIn — blocks up to 1 s on absorbed echo (soft surface!)
long t = pulseIn(ECHO, HIGH);
// ✅ pulseIn(ECHO, HIGH, 30000UL) and handle 0.

// ❌ float equality / raw threshold without hysteresis
if (dist == 20.0) ...            // never true
if (dist < 20) turn(); else forward();   // oscillates at 20 cm
// ✅ enter-avoid at <20, resume-forward at >40.

// ❌ commanding motors every loop iteration from multiple places
// ✅ command once in enterState(); states own their motion.

// ❌ String concatenation for debug on AVR (heap fragmentation, eventual hang)
Serial.println("d=" + String(distCm));
// ✅ Serial.print("d="); Serial.println(distCm);

// ❌ averaging that includes timeout sentinel
avg = (a + b + 999.0) / 3;       // phantom "clear"
// ✅ median-of-3, or exclude sentinels.

// ❌ uint8_t for millis math; or subtracting without unsigned wrap-safety
if (millis() - stateEntered >= 450)   // ✅ this exact form IS wrap-safe
if (millis() >= stateEntered + 450)   // ❌ breaks at 49.7-day wrap & overflow
```

---

## 11. Threshold Cheat Sheet (0.2–0.3 m/s differential robot, 20 Hz loop)

| Parameter | Value | Why |
|---|---|---|
| Obstacle stop threshold | 18–25 cm | covers loop latency + stop distance |
| Resume-clear threshold | 2× stop threshold | hysteresis |
| Wall-follow target gap | 12–18 cm | inside ultrasonic sweet spot, room to correct |
| Wall-follow error clamp | ±10 cm | lost-wall protection |
| Ping interval (1 sensor) | 60 ms | spec ≥ 29 ms; 60 kills cross-echo |
| Ping interval (2+ sensors) | 60 ms round-robin, never simultaneous | cross-talk |
| Back-up duration | 300–500 ms | ~6–10 cm clearance |
| 90° timed turn | calibrate; 250–600 ms typical | surface + battery dependent |
| Servo settle per 45° | 150 ms | SG90 ~0.12 s/60° no-load, loaded slower |
| Stuck escalation | 3–4 consecutive detections | corner traps |
| FSM tick | 20–50 ms | responsiveness vs CPU |
