---
name: pid-control
description: "Use when implementing or tuning PID control loops on robots — motor speed control, line followers, balance bots, heading hold, position control. Provides exact tuning procedures (P-only first, oscillate-then-halve), anti-windup integral clamping, derivative-on-measurement to eliminate setpoint kick, weighted-sensor line-follower PID, fixed sample-time enforcement, and integer-math PID for 8-bit AVR. Working code in MicroPython, Arduino C++, and Python/ROS2."
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


# PID Control for Robots

PID is one equation and a hundred ways to get it wrong. This skill encodes the correct
implementation patterns and the exact tuning procedure that works on real hardware.

```
output = Kp*error + Ki*∫error·dt + Kd*d(error)/dt
```

## Decision table — what controller do you actually need?

| Plant | Controller | Why |
|---|---|---|
| Line follower (differential drive) | PD | Integral causes wandering on straights; line position has no steady-state offset to fix |
| Motor speed (RPM hold under load) | PI | Friction/load causes steady-state error → need I. D amplifies encoder quantization noise |
| Balance robot (inverted pendulum) | PD (angle) + PI (velocity) cascade | Pure PID on angle alone drifts; cascade is the only stable structure |
| Heading hold (IMU yaw) | P or PD | Gyro heading is smooth; D optional. NEVER let error wrap discontinuously (see angle wrap) |
| Position servo (encoder counts) | PD, add weak I only if it stops short | Strong I on position = overshoot + limit-cycle hunting |
| Temperature (hotend, etc.) | PI or PID with long sample time | Slow plant; D helps against overshoot, sample at 0.1–1 s |
| Drone attitude rate loop | PID at 250 Hz–8 kHz | High rate mandatory; D-term needs low-pass filter |

Rule: **start with P only. Add D if it overshoots. Add I if it settles offset from target. Never start with all three.**

---

## The reference implementation (get these 6 things right)

Every correct PID has all six. Most broken PIDs are missing 2–3 of them.

1. **Fixed sample time** — compute at a constant Δt; don't recompute Kd/Ki scaling every loop from a jittery measured dt.
2. **Derivative on measurement, not error** — eliminates "derivative kick" when the setpoint changes.
3. **Integral anti-windup** — clamp the integral term (not just the output) so it can't wind up while the output is saturated.
4. **Output clamping** — limit to actuator range and tell the integrator about it.
5. **Bumpless re-enable** — when toggling the controller on, initialize `last_measurement` and integral so the output doesn't jump.
6. **D-term low-pass filter** — raw derivative of a noisy sensor is garbage; filter it.

### MicroPython (ESP32 / RP2040 / micro:bit) — complete class

```python
import time

class PID:
    def __init__(self, kp, ki, kd, setpoint=0.0,
                 out_min=-100.0, out_max=100.0,
                 sample_ms=20, d_alpha=0.2):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.setpoint = setpoint
        self.out_min, self.out_max = out_min, out_max
        self.sample_ms = sample_ms
        self.dt = sample_ms / 1000.0
        self.d_alpha = d_alpha          # D low-pass: 0.1 heavy, 1.0 none
        self._i = 0.0
        self._last_meas = None
        self._d_filt = 0.0
        self._last_t = time.ticks_ms()

    def reset(self, measurement):
        """Call before (re)enabling. Bumpless start."""
        self._i = 0.0
        self._last_meas = measurement
        self._d_filt = 0.0
        self._last_t = time.ticks_ms()

    def update(self, measurement):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_t) < self.sample_ms:
            return None                 # not time yet — caller keeps last output
        self._last_t = now

        error = self.setpoint - measurement

        # Integral with anti-windup clamp (clamp the TERM, in output units)
        self._i += self.ki * error * self.dt
        if self._i > self.out_max: self._i = self.out_max
        elif self._i < self.out_min: self._i = self.out_min

        # Derivative on MEASUREMENT (note the minus sign), low-pass filtered
        if self._last_meas is None:
            self._last_meas = measurement
        d_raw = -(measurement - self._last_meas) / self.dt
        self._d_filt += self.d_alpha * (d_raw - self._d_filt)
        self._last_meas = measurement

        out = self.kp * error + self._i + self.kd * self._d_filt
        if out > self.out_max: out = self.out_max
        elif out < self.out_min: out = self.out_min
        return out
```

Usage — motor speed loop on ESP32 at 50 Hz:

```python
pid = PID(kp=0.8, ki=2.0, kd=0.0, setpoint=120.0,   # 120 RPM target
          out_min=0, out_max=1023, sample_ms=20)
pid.reset(read_rpm())
last_out = 0
while True:
    out = pid.update(read_rpm())
    if out is not None:
        last_out = out
    pwm.duty(int(last_out))
    time.sleep_ms(2)        # loop faster than sample_ms; PID gates itself
```

### Arduino C++ — float version

```cpp
class PID {
public:
  PID(float kp, float ki, float kd, float outMin, float outMax,
      uint32_t sampleMs)
    : kp_(kp), ki_(ki), kd_(kd), outMin_(outMin), outMax_(outMax),
      sampleMs_(sampleMs), dt_(sampleMs / 1000.0f) {}

  void reset(float meas) {
    i_ = 0; lastMeas_ = meas; dFilt_ = 0; lastMs_ = millis(); init_ = true;
  }
  void setpoint(float sp) { sp_ = sp; }

  // Returns true when a new output was computed (out is updated).
  bool update(float meas, float &out) {
    uint32_t now = millis();
    if (now - lastMs_ < sampleMs_) return false;
    lastMs_ += sampleMs_;            // += not =, prevents drift accumulation
    if (!init_) reset(meas);

    float err = sp_ - meas;

    i_ += ki_ * err * dt_;
    i_ = constrain(i_, outMin_, outMax_);

    float dRaw = -(meas - lastMeas_) / dt_;
    dFilt_ += 0.2f * (dRaw - dFilt_);           // alpha = 0.2
    lastMeas_ = meas;

    out = constrain(kp_ * err + i_ + kd_ * dFilt_, outMin_, outMax_);
    return true;
  }
private:
  float kp_, ki_, kd_, outMin_, outMax_, sp_ = 0;
  float i_ = 0, lastMeas_ = 0, dFilt_ = 0, dt_;
  uint32_t sampleMs_, lastMs_ = 0;
  bool init_ = false;
};
```

Note `lastMs_ += sampleMs_` (not `= now`): keeps the long-run average rate exact even
when individual loop iterations jitter. If the loop falls more than 2 periods behind,
resync: `if (now - lastMs_ > 2*sampleMs_) lastMs_ = now;`

---

## Tuning procedure: oscillate-then-halve (works every time)

Do this on the real robot, on the real surface, at the real battery voltage.
A half-charged LiPo gives different gains than a full one — tune at nominal voltage
or normalize output by measured battery voltage.

**Step 1 — P only.** Ki = Kd = 0. Start Kp tiny (output barely responds).
Double Kp until the system **oscillates continuously** around the setpoint
(steady, not growing). That Kp is the *ultimate gain* Ku. Note the oscillation
period Tu in seconds (time one full cycle with a stopwatch or log timestamps).

**Step 2 — Halve it.** Set `Kp = 0.5 * Ku`. For most hobby robots this alone is
80% of the result. If response is sluggish, try 0.6·Ku.

**Step 3 — Add D if it overshoots.** Start `Kd = Kp * Tu / 8`. Increase until
overshoot is gone; back off 20%. If the actuator buzzes/chatters, your D is too
high or unfiltered — lower `d_alpha` (more filtering) before lowering Kd.

**Step 4 — Add I only if steady-state error remains.** Start `Ki = Kp / Tu` and
halve it if you see slow overshoot ("integral hump"). Verify anti-windup: hold
the robot so it can't reach setpoint for 5 s, release — it must NOT lunge.

Ziegler–Nichols classic (`Kp=0.6Ku, Ki=1.2Ku/Tu, Kd=0.075KuTu`) is aggressive and
overshoots ~25%. For robots prefer the gentler table:

| Want | Kp | Ki | Kd |
|---|---|---|---|
| No overshoot (position, arm) | 0.2·Ku | 0.4·Ku/Tu | 0.066·Ku·Tu |
| Some overshoot OK (speed) | 0.45·Ku | 0.54·Ku/Tu | 0 |
| Classic ZN (fast, overshoots) | 0.6·Ku | 1.2·Ku/Tu | 0.075·Ku·Tu |

**Tuning sanity checks**
- If you can't make it oscillate even at huge Kp: actuator is saturating before
  instability — your output range is too small for the demanded correction, or
  there's deadband (motor doesn't move below PWM ~15–25% on cheap gearmotors —
  add a feedforward offset: `if out>0: out += deadband`).
- Oscillation period Tu ≈ 2× your control loop period means you're sampling too
  slowly — the loop itself is the dominant delay. Sample ≥ 10× faster than Tu.

---

## Derivative kick — why derivative-on-measurement

With D on error: when setpoint jumps from 0→100, `d(error)/dt` spikes to infinity
for one sample → actuator slams full output for one tick. With D on measurement,
`d(setpoint)/dt` term vanishes (setpoint is constant between changes) and:

```
d(error)/dt = d(sp)/dt - d(meas)/dt = -d(meas)/dt
```

Hence the minus sign in the code above. Same damping behavior during disturbances,
zero kick on setpoint changes. **Always use derivative-on-measurement on robots**
— setpoints change constantly (joystick, path follower).

## Integral windup — the failure mode and the fix

Scenario: robot wheel is blocked. Error stays large. Integral grows unbounded.
Obstacle removed → robot launches at full power and overshoots wildly for seconds
while the integral unwinds. This is the #1 PID bug in student robots.

Fixes, in order of preference:
1. **Clamp the integral term** to output limits (done in code above). Simple, sufficient.
2. **Conditional integration**: only integrate when output is NOT saturated:
   ```python
   if out_min < unclamped_out < out_max:
       self._i += self.ki * error * self.dt
   ```
3. **Back-calculation**: `i += kt * (out_clamped - out_unclamped)` with `kt ≈ ki/kp`.
   Better tracking, rarely needed on hobby robots.

Also: **reset the integral to 0 when the controller is disabled or the target mode
changes** (e.g., line follower picked up off the floor — sensors read "all white",
integral winds up, robot spins when set back down).

---

## Line follower PID (the canonical build)

### Weighted sensor position

With N reflectance sensors (e.g., QTR-8A: 8 sensors, 9.525 mm pitch), compute a
continuous line position instead of bang-bang:

```python
# weights: sensor i at position i*1000 → line position 0..(N-1)*1000
# center = (N-1)*1000/2.  For 8 sensors: 0..7000, center 3500.
def read_line(sensors_norm):           # values normalized 0..1000, 1000 = on line
    num = den = 0
    for i, v in enumerate(sensors_norm):
        if v > 50:                     # noise floor
            num += i * 1000 * v
            den += v
    if den == 0:
        return None                    # line lost
    return num // den                  # 0..7000
```

**Calibrate per session**: sweep the robot over the line for 3 s at startup,
record per-sensor min/max, normalize: `norm = 1000*(raw-min)/(max-min)`. Skipping
calibration is why "it worked yesterday" robots fail — ambient light shifted.

### The PD steering loop

```python
KP = 0.07          # start: max_speed_delta / max_error = e.g. 250/3500
KD = 0.6           # typically 5–15× KP for line followers
BASE = 160         # base PWM out of 255 — tune speed AFTER tuning PID
CENTER = 3500
last_err = 0
last_pos = CENTER

while True:
    pos = read_line(read_sensors())
    if pos is None:
        # line lost: steer hard toward last known side
        pos = 0 if last_pos < CENTER else 7000
    last_pos = pos
    err = pos - CENTER                 # -3500..+3500
    d = err - last_err                 # fixed loop period → dt folded into KD
    last_err = err
    steer = KP * err + KD * d
    set_motors(BASE - steer, BASE + steer)   # clamp inside set_motors to 0..255
    time.sleep_ms(5)                   # ~200 Hz; keep CONSTANT
```

Line-follower specifics:
- **No integral.** Curves are disturbances, not steady-state errors; I makes the
  robot weave on straights and blow corners.
- dt is folded into KD because the loop period is fixed — this only works if the
  period really is fixed. One `print()` in the loop adds ms of jitter and detunes D.
- **Sign check first**: push the robot left of the line by hand — left motor must
  speed up. If it slams the wrong way, flip the sign of `steer`, don't "tune around it."
- Allow negative motor speeds (reverse inner wheel) for hairpins:
  `set_motors(BASE - steer, BASE + steer)` clamped to −255..255 corners far harder
  than clamping at 0.
- Tune at low BASE speed, then raise BASE. KP roughly holds; KD usually needs increasing
  with speed.

---

## Angle wrap (heading PID) — mandatory

Yaw error must be wrapped to (−180°, +180°] or the robot takes the 350° route:

```python
def angle_err(sp_deg, meas_deg):
    e = (sp_deg - meas_deg) % 360.0
    if e > 180.0: e -= 360.0
    return e
```

C++: `float e = fmodf(sp - meas + 540.0f, 360.0f) - 180.0f;`
Feed this wrapped error into the PID. Also wrap the *measurement delta* used by
the D term, or D spikes every time heading crosses ±180°.

---

## Integer PID for AVR (ATmega328 @ 16 MHz, no FPU)

Float math on AVR: a single float multiply ≈ 80–140 cycles; the full float PID
costs ~1500 cycles ≈ 94 µs. Fine at 1 kHz. But inside an encoder ISR or a 10 kHz
current loop, use fixed-point:

```cpp
// Q8.8 fixed point: gains scaled by 256. dt folded into KI_Q8/KD_Q8 at compile time.
// Tune in float, then: KP_Q8 = round(kp*256), KI_Q8 = round(ki*dt*256),
// KD_Q8 = round(kd/dt*256).
#define KP_Q8  154L     // 0.60
#define KI_Q8   31L     // 0.12 (already includes dt)
#define KD_Q8  512L     // 2.00 (already includes /dt)
#define OUT_MAX 255L
#define OUT_MIN (-255L)
#define I_MAX  (OUT_MAX << 8)   // integral stored in Q8 output units

static int32_t i_q8 = 0;
static int16_t lastMeas = 0;

int16_t pid_update(int16_t sp, int16_t meas) {
  int16_t err = sp - meas;

  i_q8 += KI_Q8 * err;
  if (i_q8 >  I_MAX) i_q8 =  I_MAX;
  if (i_q8 < -I_MAX) i_q8 = -I_MAX;

  int32_t d_q8 = -KD_Q8 * (int32_t)(meas - lastMeas);
  lastMeas = meas;

  int32_t out = (KP_Q8 * err + i_q8 + d_q8) >> 8;
  if (out > OUT_MAX) out = OUT_MAX;
  if (out < OUT_MIN) out = OUT_MIN;
  return (int16_t)out;
}
```

Integer PID rules:
- All intermediates `int32_t`. `KP_Q8 * err` with int16 err can hit ±21 bits — int16 overflow
  is the classic "works until error gets big, then motor reverses" bug.
- Fold dt into the I and D gains at compile time (constant sample rate enforced by timer).
- `>> 8` on negatives is arithmetic shift on AVR-GCC (implementation-defined but
  consistent); acceptable here, or add rounding: `(x + 128) >> 8`.
- Call from a timer ISR (e.g., Timer1 CTC at 1 kHz) so dt is exact. Reading the
  encoder count shared with another ISR requires `cli()/sei()` or `ATOMIC_BLOCK`.

---

## Sample time: the silent killer

PID gains are only meaningful at the dt they were tuned for. Consequences:

- **Tuned at 50 Hz, later loop slows to 20 Hz** (added a `Serial.print`, an I2C read,
  Wi-Fi blip): effective D drops 2.5×, system overshoots; effective I rises, hump appears.
- Fix: gate the PID on a timer (as in the code above), keep heavy I/O out of the
  control path, and **log your actual loop time** during bring-up:
  ```cpp
  static uint32_t worst=0; uint32_t t0=micros();
  /* control body */ ;
  uint32_t el=micros()-t0; if(el>worst){worst=el; Serial.println(worst);}
  ```
- How fast to sample: ≥ 10–20× the desired closed-loop bandwidth. Practical numbers:

| Loop | Rate |
|---|---|
| Motor speed (encoder) | 100–1000 Hz |
| Line follower steering | 100–500 Hz |
| Balance bot angle loop | ≥ 200 Hz (100 Hz is marginal) |
| Heading hold | 50–100 Hz |
| Position outer loop (cascade) | 1/5 to 1/10 of inner-loop rate |

- Encoder speed measurement at high rates: at 100 Hz with a 360 CPR encoder at 60 RPM
  you get only 3–4 counts per period → quantization noise destroys the D term.
  Either count over a longer window, measure period between edges instead of counts
  per window, or low-pass the measurement.

---

## Cascade for balance bots (structure, not just gains)

A single PID on tilt angle cannot keep a balance bot stationary — it balances while
drifting away. Correct structure:

```
target_velocity (0) → [PI velocity] → target_angle → [PD angle @ ≥200Hz] → motor PWM
        ↑ wheel encoder speed                ↑ complementary/Kalman-filtered IMU angle
```

- Inner PD on angle: tune first with the outer loop OFF (target_angle = trim angle).
  Robot should balance but drift.
- Outer PI on velocity, running 5–10× slower, outputs a *small* angle setpoint
  (clamp to ±3–5°!). Unclamped outer loops command 30° lean and the robot dives.
- Angle source: complementary filter `angle = 0.98*(angle + gyro*dt) + 0.02*accel_angle`
  at the inner-loop rate. Raw accelerometer angle alone is unusably noisy; raw gyro
  integration alone drifts.

---

## ROS2 pattern (Python, rclpy)

Don't trust callback timing for dt in ROS2 — measure it, but reject outliers:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class PidNode(Node):
    def __init__(self):
        super().__init__('pid_controller')
        self.declare_parameters('', [('kp', 1.0), ('ki', 0.0), ('kd', 0.0),
                                     ('out_min', -1.0), ('out_max', 1.0),
                                     ('rate_hz', 50.0)])
        p = self.get_parameter
        self.kp, self.ki, self.kd = (p('kp').value, p('ki').value, p('kd').value)
        self.out_min, self.out_max = p('out_min').value, p('out_max').value
        self.dt = 1.0 / p('rate_hz').value
        self.sp = 0.0; self.meas = None
        self.i = 0.0; self.last_meas = None; self.d_filt = 0.0
        self.create_subscription(Float64, 'setpoint', lambda m: setattr(self, 'sp', m.data), 10)
        self.create_subscription(Float64, 'measurement', lambda m: setattr(self, 'meas', m.data), 10)
        self.pub = self.create_publisher(Float64, 'control_effort', 10)
        self.create_timer(self.dt, self.step)        # timer drives dt, not callbacks

    def step(self):
        if self.meas is None: return
        if self.last_meas is None: self.last_meas = self.meas
        err = self.sp - self.meas
        self.i = max(self.out_min, min(self.out_max, self.i + self.ki*err*self.dt))
        d_raw = -(self.meas - self.last_meas) / self.dt
        self.d_filt += 0.2 * (d_raw - self.d_filt)
        self.last_meas = self.meas
        out = max(self.out_min, min(self.out_max,
                  self.kp*err + self.i + self.kd*self.d_filt))
        self.pub.publish(Float64(data=out))
```

ROS2 notes:
- Drive the PID from a **timer**, not from the measurement callback — sensor topics
  jitter and can burst.
- If the measurement topic goes stale (no msg for > 3 periods), publish 0 and reset
  the integral — controlling on a frozen measurement is how robots run into walls.
- For C++ production use `control_toolbox::Pid` (has anti-windup) or ros2_control's
  `pid_controller`; declare gains as parameters so `ros2 param set` retunes live.

---

## Mistakes everyone makes (checklist form)

1. **Sign error** — output drives error larger; system slams to a rail. Test open-loop
   first: positive output must move the measurement in the positive direction. If not,
   negate the output (or the gains), once, deliberately.
2. **Tuning Ki/Kd before Kp** — always P first.
3. **No anti-windup** — robot lunges after being blocked/held.
4. **D on error** — kick on every setpoint change.
5. **Unfiltered D on a noisy sensor** — motors buzz, gains seem "impossible to tune."
   Filter the D term or the measurement, not the output.
6. **Variable loop time** — prints, blocking I2C/`analogRead` chains, Wi-Fi. Gate on a timer.
7. **dt in wrong units** — ms vs s gives gains off by 1000×. Pick seconds, everywhere.
8. **Integral not reset on enable/mode-change** — robot jumps when controller re-engages.
9. **No deadband compensation** — small corrections do nothing (motor static friction),
   I winds up, robot oscillates slowly. Add feedforward offset past the deadband.
10. **Angle wrap ignored** — heading controller spins the long way at ±180°.
11. **Int16 overflow in integer PID** — works in small tests, reverses under large error.
12. **Tuning on blocks, deploying on carpet** — load changes the plant; tune in-situ.
13. **Battery sag detunes gains** — output is PWM duty but plant gain ∝ Vbat. Either
    retune per battery state or scale: `out *= V_nominal / V_measured`.
14. **Clamping output but not integral** — windup persists even though output "looks clamped."
15. **Setpoint steps for position loops** — feed a ramped/trapezoidal setpoint; a step
    demands infinite acceleration and guarantees overshoot complaints.

## Debugging checklist (run in order)

1. **Open-loop sanity**: command 25/50/75% output manually. Does the plant respond
   proportionally and in the expected direction? If not, fix hardware/sign before PID.
2. **Log the triplet**: timestamp, setpoint, measurement, output to serial/CSV every cycle.
   You cannot tune what you cannot plot. (Arduino: `Serial.print` CSV + Serial Plotter;
   ESP32: buffer in RAM, dump after run to avoid timing impact.)
3. **Check measured loop period**: mean and worst-case. Worst > 1.5× mean → fix timing first.
4. **Symptom table**:

| Symptom | Likely cause | Fix |
|---|---|---|
| Steady oscillation, constant amplitude | Kp at/over Ku | Halve Kp |
| Growing oscillation | Sign error, or dt mismatch, or transport delay | Open-loop test; check dt |
| Slow drift to one side, never reaches target | No I, or deadband | Add small Ki or deadband feedforward |
| Overshoots once then settles | Needs D, or I too high | Add Kd; halve Ki |
| Fast buzz/chatter at the actuator | Noisy D | Filter D (lower alpha) or reduce Kd |
| Slow large overshoot after being held | Integral windup | Anti-windup clamp + reset on enable |
| Fine at low speed, unstable at high speed | Plant gain rises with speed / battery sag | Gain-schedule or voltage-normalize |
| Works on bench, fails on floor | Different load/friction | Retune in-situ |
| Random twitches every N seconds | Blocking task in loop (Wi-Fi, GC, logging) | Move off control path; timer ISR |

5. **One change at a time.** Change one gain, run, log, compare. Two changes per test
   means you learn nothing.
