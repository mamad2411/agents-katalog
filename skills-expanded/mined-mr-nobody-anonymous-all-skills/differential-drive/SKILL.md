---
name: differential-drive
description: "Use when writing code for a two-wheeled robot (differential drive) — driving straight, turning, odometry, or velocity control. Provides exact kinematics (v_l/v_r to linear/angular velocity and back), turning-radius math, encoder odometry with slip-aware error budgets, motor deadband compensation (~20% PWM), gyro-assisted straight-line driving, point turns vs arc turns, and working MicroPython, Arduino C++, and ROS 2 code patterns."
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


# Differential Drive: Kinematics, Odometry, and Motor Control

A differential-drive robot has two independently driven wheels on a common axis plus
passive casters/ball supports. Everything — driving straight, turning, odometry —
reduces to choosing two wheel velocities `v_l` and `v_r`. This file gives the exact
math, the hardware realities that break the math, and code that compensates.

## 0. Symbols and Units (use SI everywhere, convert at the edges)

| Symbol | Meaning | Unit |
|--------|---------|------|
| `v_l`, `v_r` | left/right wheel linear (ground-contact) velocity | m/s |
| `v` | robot linear velocity (body frame, +x forward) | m/s |
| `ω` (omega) | robot angular velocity, CCW positive (right-hand rule, z up) | rad/s |
| `L` | track width = distance between wheel ground-contact CENTERS | m |
| `r` | wheel radius | m |
| `R` | turning radius (ICC distance from robot center) | m |
| `θ` (theta) | robot heading in world frame, CCW from +x | rad |
| `N` | encoder counts per wheel revolution (AFTER gearbox, AFTER quadrature decode) | counts/rev |

**The #1 silent bug:** `N` confusion. A "TT motor with 20 CPR encoder" usually means
20 counts per MOTOR shaft rev. With a 1:48 gearbox and 4x quadrature decoding,
counts per WHEEL rev = 20 × 48 = 960 (if 20 already includes quadrature) or
20 × 4 × 48 = 3840 (if 20 is PPR per channel). **Measure it:** rotate the wheel
exactly 10 turns by hand, read the count, divide by 10. Do this once, hardcode the
measured value with a comment.

**The #2 silent bug:** `L` is the distance between tire contact patch centers, not
chassis width. Wide tires squirm; effective `L` is typically 1.02–1.10× the geometric
value. Calibrate it (Section 6).

## 1. Forward Kinematics: (v_l, v_r) → (v, ω)

```
v = (v_r + v_l) / 2
ω = (v_r - v_l) / L
```

Convention check: `v_r > v_l` ⇒ `ω > 0` ⇒ robot turns LEFT (CCW). If your robot
turns the wrong way, you have left/right swapped somewhere — fix the wiring label,
not the sign in the math.

Wheel surface speed from angular speed: `v_wheel = ω_wheel × r`. From encoders:

```
v_wheel = (Δcounts / N) × 2πr / Δt
```

## 2. Inverse Kinematics: (v, ω) → (v_l, v_r)

```
v_l = v - ω·L/2
v_r = v + ω·L/2
```

This is the function every velocity controller calls. Always saturate symmetrically —
if one wheel exceeds max speed, scale BOTH so the turn radius is preserved:

```python
def inverse_kinematics(v, omega, L, v_max):
    vl = v - omega * L / 2
    vr = v + omega * L / 2
    m = max(abs(vl), abs(vr))
    if m > v_max:           # preserve curvature, sacrifice speed
        vl *= v_max / m
        vr *= v_max / m
    return vl, vr
```

Clipping each wheel independently (the naive mistake) changes the turn radius at
high speed and makes the robot understeer into walls.

## 3. Turning Radius Math

Instantaneous Center of Curvature (ICC) lies on the wheel axis line.

```
R = (L/2) × (v_r + v_l) / (v_r - v_l)        # signed; +R = ICC to robot's left
```

| Case | Wheel speeds | Motion |
|------|-------------|--------|
| `v_l = v_r` | equal | straight line, R = ∞ |
| `v_l = -v_r` | equal & opposite | point turn (spin in place), R = 0 |
| `v_l = 0` | one stopped | pivot about left wheel, R = L/2 |
| `v_r = k·v_l`, k>1 | unequal same sign | arc, R = (L/2)(k+1)/(k−1) |

To drive an arc of radius R at speed v: `ω = v / R`, then inverse kinematics.
Useful identity: `v_r / v_l = (R + L/2) / (R − L/2)`.

**Point turns vs arcs — when to use which:**
- Point turns (`v_l = -v_r`): precise heading changes when stationary, mazes,
  line-follower junction handling. BUT: both tires scrub sideways across their
  contact patches, so encoder-based heading from a point turn carries the worst
  slip error of any maneuver (expect 5–15% heading error on tile, worse on carpet
  — carpet fibers deflect the robot unpredictably). On carpet or high-grip rubber
  tires, prefer pivot turns (one wheel stopped) or use a gyro for the turn (Section 7).
- Arcs: faster (no stop), less slip, smoother odometry. Use whenever the path allows.
- Pivot turns (one wheel at 0): compromise — half the scrub of a point turn, turns
  about the stopped wheel, displaces the robot center by L/2 sideways per 90°.

## 4. Odometry (dead reckoning from encoders)

Per control tick (run at fixed Δt, 50–100 Hz typical; 20 Hz minimum for a slow robot):

```
d_l = 2πr × Δcounts_l / N        # left wheel distance this tick, meters
d_r = 2πr × Δcounts_r / N
d   = (d_r + d_l) / 2            # center distance
Δθ  = (d_r - d_l) / L            # heading change

# Exact arc update (use when |Δθ| > ~1e-4 rad):
if |Δθ| < 1e-4:
    x += d × cos(θ + Δθ/2)       # midpoint approximation — 2nd-order accurate
    y += d × sin(θ + Δθ/2)
else:
    R_icc = d / Δθ
    x += R_icc × (sin(θ + Δθ) - sin(θ))
    y += -R_icc × (cos(θ + Δθ) - cos(θ))
θ = wrap_to_pi(θ + Δθ)
```

The midpoint form `cos(θ + Δθ/2)` matters: using plain `cos(θ)` (Euler) accumulates
systematic error on every curve. Midpoint is free and 100× better at 50 Hz.

```python
def wrap_to_pi(a):
    return (a + math.pi) % (2 * math.pi) - math.pi
```

**Encoder delta with counter wraparound** (32-bit hardware counters, or 16-bit on
some timers): always compute deltas with wrapping subtraction:

```c
int32_t delta = (int32_t)(count_now - count_prev);  // wraps correctly for uint32
```

### Wheel slip reality — what odometry error to actually expect

Encoders measure WHEEL rotation, not GROUND motion. The difference is slip:

| Condition | Typical error |
|-----------|---------------|
| Smooth tile/wood, gentle accel, arcs only | 0.5–2% of distance, heading drifts ~1°/m |
| Same, with point turns | heading error 5–15% per point turn |
| Carpet | 2–5% distance; heading nearly useless after a few turns |
| Hard acceleration / wheel spin at launch | unbounded — encoder counts motion that never happened |
| Bump / cable crossing | step error, never recovers |
| Robot picked up ("kidnapped") | total loss; odometry cannot detect this |

Rules that follow from this:
1. **Limit acceleration in software** (slew-rate limit PWM or velocity setpoint,
   e.g. max 0.5 m/s² for a small robot) — most slip happens at launch and braking.
2. **Heading from encoders is the weak link.** Distance is decent; heading drifts.
   Fuse a gyro for θ (Section 7) and keep encoders for distance. This single change
   typically improves pose accuracy 10×.
3. Odometry is a RELATIVE sensor. Anything beyond ~5 m of travel needs an absolute
   correction (line detection, wall touch, AprilTag, lidar scan match).
4. Caster wheels on launch: a swiveling caster facing backward shoves the robot
   sideways when you start. If your robot veers only on the FIRST move, that's the
   caster, not your code.

## 5. Motor Reality: Deadband, PWM, and Why Open-Loop Fails

### Deadband (~20% PWM)

Brushed DC motors with gearboxes do not move below a threshold PWM — static friction
plus brush drag. Typical: 15–25% duty for TT motors / N20s on 6 V; can hit 30% with a
worm gearbox. The two motors NEVER have the same deadband (manufacturing spread is
±5–10%), which is the main reason `analogWrite(LEFT, 128); analogWrite(RIGHT, 128);`
does not drive straight.

**Compensation — remap commanded effort around the deadband:**

```c
// u in [-1, 1] commanded effort -> pwm duty out
int apply_deadband(float u, float deadband_frac, int pwm_max) {
    if (fabsf(u) < 0.02f) return 0;                    // true zero stays zero
    float mag = deadband_frac + (1.0f - deadband_frac) * fabsf(u);
    int pwm = (int)(mag * pwm_max);
    return (u > 0) ? pwm : -pwm;
}
// Calibrate deadband_frac PER MOTOR: ramp PWM up 1%/100ms, record duty where
// the wheel first sustains rotation (not just twitches). Do it on the ground
// surface you'll run on, with the robot's full weight on the wheels.
```

Without this remap, any PID whose output passes through zero will limp: small
corrections produce no motion, the integrator winds up, then the motor lurches.

### PWM frequency

- < 100 Hz: visible cogging, audible buzz, jerky low-speed motion.
- 1–4 kHz: works but whines audibly (annoying in kid projects).
- **20–25 kHz: inaudible, smooth — use this** if the driver supports it (DRV8833,
  TB6612FNG: yes, up to 100 kHz; L298N: keep ≤ 20 kHz, it's slow and lossy).
- ESP32 `ledcSetup(ch, 20000, 10)` → 20 kHz, 10-bit (0–1023). At 20 kHz you can't
  have more than ~12-bit resolution on most timers; 10-bit is plenty.
- Arduino Uno default `analogWrite` is 490/980 Hz — audible. Acceptable for a first
  build; change timer prescalers only if you know which timers `millis()` uses
  (Timer0 — don't touch it).

### Motor driver wiring (TB6612FNG — the sane default; avoid L298N for ≤9 V robots,
it drops 1.4–2.6 V internally, stealing a third of your battery)

| TB6612 pin | Connect to | Notes |
|------------|-----------|-------|
| VM | Battery + (4.5–13.5 V) | motor power, NOT 3.3/5 V rail |
| VCC | MCU 3.3 V or 5 V | logic power |
| GND | Common ground | MCU GND and battery GND MUST join |
| AIN1, AIN2 | 2 GPIO | direction, left motor |
| PWMA | PWM-capable GPIO | speed, left motor |
| BIN1, BIN2, PWMB | 3 GPIO | right motor |
| STBY | GPIO or tie HIGH | LOW = both motors off (use as e-stop) |
| AO1/AO2, BO1/BO2 | motor terminals | swap a pair to flip direction |

Truth table per channel: IN1=1,IN2=0 → forward; 0,1 → reverse; 0,0 → coast;
1,1 → brake. **Use brake (1,1) when stopping for odometry accuracy** — coast lets
the robot roll an extra few cm that the encoders DO record but a deadband-limited
controller can't correct.

Current numbers: TB6612 = 1.2 A continuous / 3.2 A peak per channel. TT motor stall
≈ 1.5–2.5 A at 6 V (fine, stalls are brief); N20 stall ≈ 0.7–1.6 A. A stalled motor
held at full PWM for seconds will brown out 4×AA alkalines — use NiMH or 2S LiPo
with a 5 V regulator for the MCU, and a 470–1000 µF electrolytic across VM/GND at
the driver. **Brownout symptom: MCU reboots the instant motors start.** That is a
power problem, not a code problem — shared AA pack, no bulk cap, or thin wires.

### Why driving straight open-loop is impossible

Equal PWM ≠ equal speed because: deadband mismatch, winding resistance spread
(±10%), gearbox friction spread, tire diameter spread (±1% diameter = 1 cm/m drift),
weight distribution, battery sag during the run. A typical "matched" motor pair
diverges 5–20% in speed at the same duty. **You need feedback: encoders, a gyro, or
both.** No amount of constant trim (`right_pwm = left_pwm * 1.07`) survives a
battery voltage change.

## 6. Calibration Procedure (do these IN ORDER, once per robot)

1. **N (counts/wheel-rev):** rotate each wheel 10 turns by hand, `N = counts/10`.
2. **r (wheel radius):** drive straight ~2 m, measure actual distance with a tape:
   `r_true = r_assumed × (measured / odometry_reported)`. Tire squish under load
   makes effective r ~1–3% smaller than the ruler says.
3. **L (track width):** command 10 point-turn revolutions (3600°) slowly. Measure
   actual rotation (mark on floor): `L_true = L_assumed × (odom_angle / actual_angle)`.
   Slip inflates apparent L; the calibrated value bakes average slip in. Recalibrate
   if you change floor surface.
4. **Deadband per motor, per direction** (forward and reverse differ): ramp test as
   in Section 5.
5. Optional: UMBmark (drive a 2 m square CW ×5 and CCW ×5, compare endpoint errors)
   separates L-error from wheel-diameter mismatch if you need <1% odometry.

## 7. Control Patterns That Work

### Pattern A: Per-wheel velocity PI + kinematics (the standard architecture)

```
target (v, ω) → inverse kinematics → (v_l*, v_r*) targets
            → per-wheel PI on encoder-measured speed → deadband remap → PWM
```

- PI, not PID: encoder velocity (counts differenced over 10–20 ms) is quantized and
  noisy; the D term amplifies that noise into motor chatter. Skip D or filter heavily.
- Run the loop at a FIXED rate from a hardware timer, 50–100 Hz. Variable-rate loops
  driven by `loop()` timing make Ki/Kd meaningless.
- Anti-windup is mandatory: clamp the integrator when output saturates.
- Velocity measurement at low speed: at 20 counts/tick you have 5% quantization. If
  the robot must creep, measure period-between-edges instead of counts-per-period,
  or filter with `v_f += 0.2 * (v_raw - v_f)`.

```cpp
// Arduino C++ — one wheel's PI velocity controller, called at exactly 50 Hz
struct WheelPI {
  float kp = 1.2f, ki = 8.0f;      // starting point for ~0.5 m/s max TT-motor bot
  float integ = 0, dt = 0.02f;
  float deadband = 0.20f;           // calibrated!
  float update(float v_target, float v_meas) {       // returns effort [-1,1]
    float err = v_target - v_meas;
    integ += err * dt;
    float u = kp * err + ki * integ;
    if (u > 1.0f)  { u = 1.0f;  integ -= err * dt; }  // anti-windup: undo
    if (u < -1.0f) { u = -1.0f; integ -= err * dt; }
    return u;
  }
};
```

Tuning recipe: set ki=0, raise kp until the wheel tracks a step with slight
overshoot, halve kp, then raise ki until steady-state error vanishes in <0.5 s.
Tune at half battery voltage so it still works when the pack sags.

### Pattern B: Gyro-stabilized straight line (works even WITHOUT encoders)

Heading hold beats wheel-speed matching for straightness because it closes the loop
on the thing you actually care about. With an MPU6050/ICM-20948/BNO055:

```python
# MicroPython (ESP32 / Pico) — drive straight using gyro z
import time
from machine import Pin, PWM, I2C

KP_HEADING = 2.0      # (effort per rad of heading error) start 1-4
BASE = 0.45           # base effort

def drive_straight(imu, motors, duration_s, base=BASE):
    heading = 0.0
    t_prev = time.ticks_us()
    end = time.ticks_add(time.ticks_ms(), int(duration_s * 1000))
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        now = time.ticks_us()
        dt = time.ticks_diff(now, t_prev) / 1_000_000
        t_prev = now
        gz = imu.gyro_z_rads() - GZ_BIAS      # bias: avg 200 samples at boot, ROBOT STILL
        heading += gz * dt                     # integrate yourself; dt from real clock
        corr = KP_HEADING * (0.0 - heading)    # target heading 0
        motors.set_effort(base - corr, base + corr)   # left, right
        time.sleep_ms(10)                      # ~100 Hz
    motors.brake()
```

Gyro facts you must respect:
- **Bias calibration at every boot, robot perfectly still**, ≥1 s of samples.
  Skipping this gives 0.5–3°/s of phantom rotation. MEMS gyro bias also drifts with
  temperature — long missions need re-zeroing or a magnetometer/landmark.
- Integrate with measured dt (`ticks_us` deltas), never an assumed loop period.
- Gyro gives heading RATE; integrated heading drifts ~1–5°/min after bias removal.
  Fine for runs of seconds-to-minutes; not for all-day localization.
- MPU6050 default full scale ±250°/s = 131 LSB/(°/s). A fast point turn can exceed
  250°/s and clip silently — set ±500°/s (65.5 LSB/(°/s)) for small robots.

### Pattern C: Gyro point turn (accurate turns despite slip)

```python
def turn_deg(imu, motors, degrees, effort=0.5):
    target = math.radians(degrees)         # +CCW
    turned = 0.0
    t_prev = time.ticks_us()
    sign = 1 if degrees > 0 else -1
    while abs(turned) < abs(target) - math.radians(2):   # stop 2 deg early: inertia
        now = time.ticks_us()
        dt = time.ticks_diff(now, t_prev) / 1_000_000
        t_prev = now
        turned += (imu.gyro_z_rads() - GZ_BIAS) * dt
        remaining = abs(target) - abs(turned)
        e = min(effort, max(0.25, effort * remaining / math.radians(45)))  # ramp down
        motors.set_effort(-sign * e, sign * e)
        time.sleep_ms(5)
    motors.brake()
    time.sleep_ms(150)                     # let it settle before next command
```

The "stop 2° early + ramp down + brake" trio is what makes turns repeatable; a bang-
bang turn overshoots 5–20° from rotational inertia.

### Pattern D: ROS 2 — cmd_vel to wheels and odom publication

Subscribe `geometry_msgs/Twist` on `/cmd_vel`: use `linear.x` (m/s) and
`angular.z` (rad/s); everything else is zero for diff drive. Publish
`nav_msgs/Odometry` on `/odom` and the `odom → base_link` TF.

```python
# ROS 2 (rclpy) skeleton — the parts people get wrong
import math, rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster

class DiffDrive(Node):
    def __init__(self):
        super().__init__('diff_drive')
        self.L, self.r, self.N = 0.16, 0.034, 1440.0     # CALIBRATED values
        self.x = self.y = self.th = 0.0
        self.create_subscription(Twist, 'cmd_vel', self.on_cmd, 10)
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf = TransformBroadcaster(self)
        self.create_timer(0.02, self.tick)               # 50 Hz fixed
        self.last_cmd_time = self.get_clock().now()

    def on_cmd(self, msg):
        self.last_cmd_time = self.get_clock().now()
        vl = msg.linear.x - msg.angular.z * self.L / 2
        vr = msg.linear.x + msg.angular.z * self.L / 2
        self.set_wheel_targets(vl, vr)                   # hardware layer

    def tick(self):
        # SAFETY: cmd_vel watchdog — stop if no command for 0.5 s
        if (self.get_clock().now() - self.last_cmd_time).nanoseconds > 5e8:
            self.set_wheel_targets(0.0, 0.0)
        dl, dr = self.read_encoder_deltas_m()            # hardware layer
        d, dth = (dr + dl) / 2, (dr - dl) / self.L
        self.x += d * math.cos(self.th + dth / 2)
        self.y += d * math.sin(self.th + dth / 2)
        self.th = math.atan2(math.sin(self.th + dth), math.cos(self.th + dth))
        now = self.get_clock().now().to_msg()
        o = Odometry()
        o.header.stamp, o.header.frame_id, o.child_frame_id = now, 'odom', 'base_link'
        o.pose.pose.position.x, o.pose.pose.position.y = self.x, self.y
        o.pose.pose.orientation.z = math.sin(self.th / 2)   # yaw-only quaternion
        o.pose.pose.orientation.w = math.cos(self.th / 2)
        o.twist.twist.linear.x = d / 0.02
        o.twist.twist.angular.z = dth / 0.02
        # Covariance: tell EKF that odom heading is untrustworthy
        o.pose.covariance[0] = o.pose.covariance[7] = 1e-3   # x, y
        o.pose.covariance[35] = 1e-1                          # yaw — large on purpose
        self.odom_pub.publish(o)
        t = TransformStamped()
        t.header.stamp, t.header.frame_id, t.child_frame_id = now, 'odom', 'base_link'
        t.transform.translation.x, t.transform.translation.y = self.x, self.y
        t.transform.rotation = o.pose.pose.orientation
        self.tf.sendTransform(t)
```

ROS-specific traps:
- Twist sign convention: `angular.z > 0` = CCW = left turn. Matches Section 1.
- Publish odom→base_link TF from exactly ONE node, or TF tree fights itself.
- `robot_localization` EKF fusing wheel odom + IMU: set odom yaw covariance high
  (as above) so the IMU wins heading — this is the standard slip workaround.
- The cmd_vel watchdog is not optional. Nav2/teleop crashing must not leave the
  robot driving into a wall.

## 8. Encoder Reading Done Right

- **Quadrature, 4x decode, in hardware where possible:** ESP32 → PCNT peripheral
  (or `ESP32Encoder` lib); RP2040 → PIO quadrature program; STM32 → timer encoder
  mode; Arduino Uno → pin-change interrupts (good to ~10 kHz total edge rate, above
  that you drop counts and odometry silently shrinks).
- Interrupt ISRs: increment a `volatile int32_t`, nothing else. Read it in the main
  loop with interrupts briefly disabled (AVR: `noInterrupts()/interrupts()`) — a
  16/32-bit read on 8-bit AVR is not atomic and will glitch by ±256 occasionally,
  which looks like random teleporting in odometry.
- Direction sign: define forward = positive counts for BOTH wheels at the software
  boundary. If a wheel counts backward, negate in the encoder read function, in one
  place, with a `# right encoder mounted mirrored` comment.
- Single-channel (non-quadrature) encoders, e.g. slotted-disc TT kits: they can't
  sense direction — they count UP while rolling backward. Infer sign from the
  commanded direction; accept that odometry breaks if the robot is pushed.

## 9. Debugging Checklist (in order — each step rules out a layer)

1. **Robot reboots when motors start** → power: shared battery sagging, missing bulk
   cap (470 µF at driver VM), missing common ground, or thin breadboard jumpers
   carrying motor current. Fix power before touching code.
2. **One motor doesn't move below ~25% but the other does at 15%** → normal deadband
   spread; calibrate per-motor deadband (Section 5).
3. **Wheels spin the wrong way** → swap that motor's two wires at the driver
   (preferred) or its IN1/IN2 in code. Re-verify: forward command → both wheels
   forward → positive encoder counts on both.
4. **Veers consistently to one side, same amount** → deadband/Kv mismatch; needs
   closed loop (Section 7 A or B). A constant trim is a trap (battery-dependent).
5. **Veers randomly, or only on first move** → swiveling caster, or wheel slip at
   launch → add acceleration limiting.
6. **Drives straight slow, curves fast** → asymmetric clipping in inverse
   kinematics (Section 2) or one motor hitting its top speed.
7. **Odometry distance ~right, heading garbage** → expected (slip). Fuse gyro.
8. **Odometry off by exact ratio (e.g. 2x or 4x)** → wrong N (quadrature factor or
   gearbox ratio). Re-measure by hand-rotation.
9. **Odometry jumps occasionally** → non-atomic counter reads (Section 8) or ISR
   doing too much work and dropping edges.
10. **Turns overshoot** → bang-bang turning; add ramp-down + early stop + brake
    (Pattern C). Also check gyro full-scale clipping (±250°/s default).
11. **PID oscillates/chatters** → loop rate not fixed, D on noisy velocity, or no
    deadband remap (controller dead zone around zero → limit cycle).
12. **Heading drifts while robot sits still** → gyro bias not calibrated this boot,
    or robot was moving during calibration.
13. **Works on bench (wheels up), fails on floor** → bench has no load: deadband,
    slip, and current draw all change under weight. Always calibrate and tune on
    the ground.

## 10. Quick Reference Card

```
v  = (vr + vl)/2                  vl = v − ωL/2
ω  = (vr − vl)/L                  vr = v + ωL/2
R  = (L/2)(vr+vl)/(vr−vl)         point turn: vl = −vr
Δθ = (dr − dl)/L                  pose update: use θ + Δθ/2 (midpoint)
deadband ≈ 20% PWM, per motor, per direction, calibrated under load
PWM 20 kHz (inaudible); TB6612 over L298N; bulk cap 470 µF at VM
straight line ⇒ closed loop (encoders and/or gyro) — never open loop
gyro: bias-cal every boot while still; integrate with measured dt
counts/wheel-rev: MEASURE by hand (10 turns), don't trust the datasheet
control loop: fixed 50–100 Hz, PI (no D), anti-windup, slew-limited accel
safety: cmd watchdog (0.5 s), STBY pin as e-stop, brake not coast at stops
```
