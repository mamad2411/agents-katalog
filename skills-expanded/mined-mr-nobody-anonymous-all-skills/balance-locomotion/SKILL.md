---
name: balance-locomotion
description: "Use when building or debugging self-balancing robots (two-wheel balancers, Segway-style platforms) or balance-aware legged locomotion (ZMP-based walking). Provides the inverted pendulum math, a complete IMU→filter→PID→motor recipe with exact starting gains, deadband/backlash compensation, ZMP fundamentals, steering mixing, and the diagnosis tree for oscillation and drift on real hardware."
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


# Balance Control & Locomotion

This skill covers dynamic balance: keeping an inherently unstable plant (an inverted pendulum) upright with active control. It applies to two-wheeled balancing robots, Segway-style personal transporters, reaction-wheel balancers, and the ZMP foundation used in bipedal walking.

**The single most important fact:** balance is a *fast* problem. A typical hobby-sized balancer (30 cm tall) has a natural fall time constant of ~175 ms. Your entire sense→filter→compute→actuate loop must run at least 10x faster than that, with consistent timing. Almost every "my robot won't balance" problem is a timing, latency, or actuator-nonlinearity problem — not a gain-tuning problem.

---

## 1. The Inverted Pendulum Model

### 1.1 Linearized dynamics

A body of mass `m` with center of mass (CoM) at height `L` above the wheel axle, tilted by angle `θ` from vertical:

```
θ̈ = (g / L) · sin(θ)  ≈  (g / L) · θ        (small angle)
```

Define the **fall time constant**:

```
τ = sqrt(L / g)
```

Worked example: hobby balancer, CoM 30 cm above axle:

```
τ = sqrt(0.30 / 9.81) = 0.175 s
```

Uncontrolled, tilt error grows as `e^(t/τ)` — it **doubles every τ·ln(2) ≈ 121 ms**. This number drives every design decision:

- **Control loop rate** must satisfy `loop period << τ`. Rule of thumb: loop period ≤ τ/20. For τ = 175 ms → loop ≥ 115 Hz. **Use 200 Hz** (5 ms) as the standard for hobby/small platforms; 500 Hz–1 kHz for small or aggressive machines.
- **Total latency budget** (sensor sample → torque at wheel) must be < ~τ/10 ≈ 15–20 ms. A 50 ms Bluetooth link in the loop makes balance impossible regardless of gains.
- **Taller robots are easier.** L = 1 m → τ = 0.32 s. A full-size Segway (CoM ~1 m) is a far more forgiving plant than a 10 cm toy (τ = 0.10 s, needs ≥ 400 Hz and very low backlash).

### 1.2 Full cart-pole equations (when you need them)

With cart (wheel/base) mass `M`, pendulum mass `m`, CoM distance `L`, horizontal force `F` at the axle:

```
(M + m)·ẍ + m·L·θ̈·cos(θ) − m·L·θ̇²·sin(θ) = F
L·θ̈ + ẍ·cos(θ) − g·sin(θ) = 0
```

Linearized about upright (θ ≈ 0), state `x = [position, velocity, θ, θ̇]`:

```
ẍ = ( F − m·g·θ ) / M                      (approx, m·L·θ̈ term folded in)
θ̈ = ( (M+m)·g·θ − F ) / (M·L)
```

You only need the full model for LQR design or simulation. For PID on a real robot, the key takeaways from the model are:

1. **Non-minimum-phase behavior**: to move forward, the robot must first lean forward, which requires the wheels to briefly move *backward*. Position control of a balancer always shows this initial reverse motion — it is physics, not a bug.
2. **The control input is wheel torque, the controlled variable is tilt.** Position/velocity is controlled indirectly by commanding a tilt setpoint. This gives the standard **cascade architecture** (§3).

### 1.3 Wheel torque sizing

Required torque to hold a static lean of θ:

```
T = m·g·L·sin(θ)     (per robot; divide by 2 per wheel)
```

Worked example: m = 1.0 kg, L = 0.30 m, recover from 15°:

```
T = 1.0 · 9.81 · 0.30 · sin(15°) = 0.76 N·m total → 0.38 N·m per wheel
```

Add 2–3x margin for dynamic recovery (you must *accelerate* the base under the CoM, not just hold). Spec motors for **~1 N·m stall per wheel** for a 1 kg robot, with no-load speed ≥ 2x your top driving speed. Geared DC motors with metal gearboxes (e.g., 1:30, 12 V, 350+ RPM) are standard. Avoid high gear ratios (>1:75) — backlash and reflected inertia kill balance (§6).

---

## 2. Sensing: IMU and the Complementary Filter

### 2.1 Why you need fusion

- **Accelerometer** gives absolute tilt (`θ_acc = atan2(a_x, a_z)`) but is corrupted by linear acceleration — exactly what a balancing robot produces constantly. Accelerometer-only tilt on a moving balancer is garbage at high frequency.
- **Gyroscope** gives clean angular rate but integrating it drifts (bias drift: typically 0.5–2 °/min for MEMS like MPU-6050/ICM-20602 after rough bias calibration).

The **complementary filter** trusts the gyro at high frequency and the accelerometer at low frequency:

```c
// Run at exactly the loop rate, dt in seconds (e.g., 0.005 for 200 Hz)
theta_acc = atan2f(ax, az);                    // radians; axis choice per mounting
theta = ALPHA * (theta + gyro_rate * dt)       // gyro integration path
      + (1.0f - ALPHA) * theta_acc;            // accel correction path
```

### 2.2 Choosing ALPHA

ALPHA sets the crossover time constant: `tau_filter = ALPHA·dt / (1 − ALPHA)`.

| ALPHA @ 200 Hz | tau_filter | Use |
|---|---|---|
| 0.98 | 0.245 s | Default starting point |
| 0.995 | 1.0 s | Aggressive robots, vibration-heavy |
| 0.95 | 0.095 s | Very quiet drivetrain only |

**Start with ALPHA = 0.98 at 200 Hz.** If the robot's estimated angle "follows" its own acceleration (tilt estimate dips when it lunges), increase ALPHA. If the angle slowly drifts and the robot creeps/leans over 30+ seconds, your gyro bias calibration is bad — fix that first, don't decrease ALPHA below ~0.95.

**Critical: ALPHA depends on dt.** If you change loop rate, recompute: `ALPHA = tau_filter / (tau_filter + dt)`.

### 2.3 IMU setup checklist (do these or fail)

1. **Gyro bias calibration at boot**: average ≥ 500 samples while *provably stationary* (check accel variance; abort and retry if the robot is moving). Subtract this bias from every reading. Skipping this gives degrees-per-minute drift that no filter fixes.
2. **Mount the IMU at/near the axle axis if possible**, rigidly, on vibration isolation (foam tape works). Mounting high on the body adds centripetal/tangential acceleration into the accel reading: `a_extra = L_imu·θ̈` — at L_imu = 0.25 m and θ̈ = 20 rad/s², that's 5 m/s² of false signal, half a g.
3. **Configure the IMU's hardware DLPF** (digital low-pass filter). MPU-6050: set DLPF_CFG = 3 (44 Hz accel / 42 Hz gyro). Raw 1 kHz unfiltered output aliases motor vibration into your tilt estimate.
4. **Read via interrupt or fixed-rate timer**, never "as fast as possible" — jittery dt corrupts the integration. Use the IMU's data-ready interrupt at your loop rate, or a hardware timer.
5. **Sign/axis sanity test before closing the loop**: tilt the robot forward by hand; verify θ goes positive (your convention), gyro rate is positive during the tilting motion, and motor command (open-loop print) would drive wheels forward. Three sign errors = "balances" by slamming into the floor.
6. **Find the true balance point.** The mechanical vertical is not the CoM-vertical. Either trim a setpoint offset (`theta_setpoint ≈ ±1–3°` typical) or let the outer velocity loop find it automatically (§3.3). Symptom of a wrong setpoint: robot balances but constantly drives in one direction.

### 2.4 When to upgrade to Mahony/Madgwick/Kalman

Complementary filter is sufficient for planar balance. Upgrade only when you need full 3D attitude (quaternion), e.g., balancing + ramp estimation or legged robots. Mahony with `Kp = 2·(1−ALPHA)/dt` behaves nearly identically in the planar case. A hand-rolled Kalman filter with mistuned Q/R is *worse* than a complementary filter — don't reach for it to fix a problem you haven't diagnosed.

---

## 3. The Control Architecture: Cascaded PID at 200 Hz

### 3.1 Structure

```
                 ┌────────────── outer loop (20–50 Hz) ──────────────┐
 velocity_cmd ──►│ velocity PI  ──► theta_setpoint (±limit ~8°)      │
 (from RC/auto)  └────────────────────────────────────────────────────┘
                                        │
                 ┌────────────── inner loop (200 Hz) ─────────────────┐
                 │ theta_error = theta_setpoint − theta               │
                 │ balance PID ──► motor_cmd (symmetric)              │
                 └────────────────────────────────────────────────────┘
                                        │
 steer_cmd ────────────────► mixing ──► left = motor_cmd + steer
                                        right = motor_cmd − steer
                                        │
                            deadband compensation ──► PWM
```

The inner (balance) loop stabilizes tilt. The outer (velocity) loop commands a tilt setpoint to achieve desired ground speed — and as a side effect automatically finds the true balance point and prevents runaway drift. Steering is mixed in *after* the balance controller (§7).

### 3.2 Inner balance loop — the exact recipe

```c
// ===== 200 Hz, driven by hardware timer or IMU data-ready interrupt =====
// All angles in degrees here (common convention for hobby tuning);
// be consistent — gains below assume degrees.

float theta_err = theta_setpoint - theta;          // deg
integral += theta_err * dt;                        // deg·s
integral = clampf(integral, -I_LIMIT, I_LIMIT);    // anti-windup, MANDATORY

// Derivative on measurement, using the GYRO directly — not d(error)/dt.
// The gyro IS dθ/dt: clean, no numerical differentiation, no setpoint kick.
float dtheta = gyro_rate_filtered;                 // deg/s

float u = KP * theta_err + KI * integral - KD * dtheta;   // motor units
u = clampf(u, -U_MAX, U_MAX);

// If output saturated, freeze the integrator (conditional integration):
if (fabsf(u) >= U_MAX) integral -= theta_err * dt;
```

**Three non-negotiable details in that code:**

1. **D-term = gyro, not differentiated angle.** Differentiating the fused angle amplifies filter noise and adds a sample of delay. The gyro is a free, clean derivative.
2. **Anti-windup.** During a push or stall, the integrator winds up and the robot violently overshoots on recovery. Clamp the integral AND use conditional integration.
3. **Output limit with headroom.** Cap |u| at ~90% of max PWM so steering mix (§7) and deadband offset (§5) still have authority.

### 3.3 Outer velocity loop

Wheel velocity from encoders (average of both wheels), low-pass filtered (~10 Hz cutoff):

```c
// ===== 50 Hz (every 4th inner-loop tick) =====
float v_err = velocity_cmd - wheel_velocity;       // m/s or counts/s
v_integral += v_err * dt_outer;
v_integral = clampf(v_integral, -VI_LIMIT, VI_LIMIT);

theta_setpoint = -(KV_P * v_err + KV_I * v_integral);  // NOTE the sign:
// to move FORWARD the robot must lean FORWARD (positive θ by our convention),
// so a positive v_err must produce a forward-lean setpoint. Verify your signs.
theta_setpoint = clampf(theta_setpoint, -8.0f, 8.0f);  // deg — hard limit!
```

The ±8° setpoint clamp is a safety limit: beyond ~10–15° lean, recovery torque exceeds typical motor capability and the robot is committed to falling.

The velocity loop's I-term **automatically trims the balance point**: if the mechanical zero is off by 2°, the robot starts to drift, velocity error builds, and the integrator shifts theta_setpoint until drift stops. This is why the cascade is strongly preferred over angle-only PID.

**No encoders?** The robot can still balance (inner loop only) but will drift and slowly wander; it cannot reject a sloped floor. Encoders — even cheap quadrature on the motor shaft — are effectively mandatory for a useful robot.

### 3.4 Starting gains and tuning order

Gains are plant-dependent, but for a ~1 kg, ~30 cm CoM robot, 12 V geared DC motors, PWM range ±255, angles in degrees:

| Gain | Start value | Range to explore |
|---|---|---|
| KP (per deg) | 15 | 5–40 |
| KD (per deg/s) | 0.6 | 0.2–2.5 |
| KI (per deg·s) | 60 | 0–150 |
| I_LIMIT | (U_MAX/2)/KI | — |
| KV_P (deg per m/s) | 3 | 1–10 |
| KV_I | 0.5 | 0.1–2 |

**Tuning procedure (do it in this order, one gain at a time):**

1. **Verify the loop runs at exactly 200 Hz** (toggle a GPIO, check on scope/logic analyzer). Fix timing before touching gains.
2. **KP only** (KI=KD=0): hold the robot, increase KP until it pushes back firmly when tilted and oscillates ~2–4 Hz when released. If it never oscillates before hitting U_MAX, you're torque-limited — check deadband (§5) and motor sizing.
3. **Add KD**: increase until the KP oscillation damps out. Too much KD → high-frequency buzz/chatter (motor "growl"); back off 30%.
4. **Add KI**: removes steady-state lean. Too much → slow 0.5–1 Hz wallow. Keep KI as low as achieves zero steady lean within ~2 s.
5. **Close the velocity loop** with small KV_P; raise until position holds against gentle pushes without inducing fore-aft pacing.
6. Push-test from all directions; tune on the actual floor surface (carpet vs hardwood changes effective deadband and grip).

**Reading the oscillation — diagnosis by frequency:**

| Symptom | Frequency | Cause | Fix |
|---|---|---|---|
| Fast buzz/chatter | > 8 Hz | KD too high, or noisy gyro path | Lower KD; check IMU DLPF; check vibration |
| Crisp rocking | 2–5 Hz | KP too high (or KD too low) | Classic P-oscillation: lower KP or raise KD |
| Slow wallow | 0.5–1 Hz | KI too high / windup | Lower KI, check anti-windup |
| Limit-cycle "shuffle" ±small angle, constant amplitude, never converges | 1–4 Hz | **Deadband or backlash** — not gains | §5, §6. No gain change fixes a deadband limit cycle. |
| Pacing back and forth across the floor | < 0.5 Hz | Outer loop too aggressive or sign-marginal | Lower KV_P; verify outer-loop sign |

### 3.5 LQR alternative

If you have a decent model, LQR on state `[x, ẋ, θ, θ̇]` gives the cascade structure automatically as `u = −K·x` with K = [k1 k2 k3 k4]. Typical Q = diag(1, 1, 100, 10), R = 1, solved with `scipy.signal` / `control.lqr`. In practice LQR and well-tuned cascaded PID perform nearly identically on this plant; PID is easier to field-tune. Use LQR when you also need it for a more complex platform (e.g., wheeled-biped) anyway.

---

## 4. Safety Layer (write this before tuning)

```c
// Tilt cutoff: beyond recoverable angle, kill motors immediately.
if (fabsf(theta) > 35.0f) {           // deg
    motors_disable();
    state = FALLEN;                    // require explicit re-arm
}
// Arming: only enable balance when robot is held near upright and still.
if (state == FALLEN && fabsf(theta) < 3.0f && fabsf(gyro_rate) < 10.0f) {
    integral = 0; v_integral = 0;     // ALWAYS reset integrators on arm
    state = BALANCING;
}
```

Without the cutoff, a fallen robot drives its wheels at full power across the floor / off the bench. Without integrator reset on re-arm, the first second after pickup is violent. Also implement: command timeout (RC link loss → velocity_cmd = 0), battery undervoltage → controlled shutdown.

---

## 5. Motor Deadband Compensation

**This is the #1 reason hobby balancers shuffle and never settle.** Geared DC motors do not move below a minimum PWM — static friction in the gearbox and brushes creates a deadband, typically **8–20% of full PWM** (e.g., PWM 25–50 out of 255 on a 12 V TT-motor or 25GA gearmotor).

Inside the deadband the plant gain is **zero**: the controller commands small corrections, nothing happens, the error grows until the command exits the deadband, the wheel jumps, overshoots — a textbook limit cycle. The signature: constant-amplitude rocking (~±1–3°) that no gain combination removes.

### 5.1 Measure it

```c
// Open-loop test, robot propped up, wheels free:
// ramp PWM from 0 upward in steps of 1, log the PWM at which the wheel
// FIRST rotates. Do both directions, both motors. Repeat at low battery.
```

Expect asymmetry: left/right and fwd/rev deadbands differ by ±20%. Store four values.

### 5.2 Compensate

```c
int apply_deadband(float u, int db_pos, int db_neg) {
    if (u >  0.5f) return (int)( u + db_pos);   // jump over the dead zone
    if (u < -0.5f) return (int)( u - db_neg);
    return 0;                                    // true zero stays zero
}
// db values: use ~85–90% of the measured breakaway PWM, NOT 100%.
// Full compensation makes the effective gain near zero infinite → chatter.
```

Use 85–90% of measured breakaway: slight under-compensation leaves a tiny dead zone (fine); over-compensation creates a relay around zero (chatter at the loop rate).

### 5.3 Battery sag interaction

Deadband in PWM counts is really a *voltage* threshold. As the battery sags (3S LiPo: 12.6 V full → 10.5 V cutoff, plus 0.5–1.5 V sag under load), the same PWM delivers less voltage:

- Effective deadband **grows** as battery drains → robot that balanced perfectly at full charge limit-cycles at 30% charge.
- Loop gain **drops** ∝ V_batt → sluggish response when drained.

**Fix: voltage-normalize the output.**

```c
float v_batt = read_battery_voltage();            // filtered, ~1 Hz update
float scale  = V_NOMINAL / fmaxf(v_batt, V_MIN);  // e.g., 11.1f / v_batt
int pwm = apply_deadband(u * scale, db_pos * scale, db_neg * scale);
```

Measure battery voltage through a divider on an ADC pin; one resistor divider eliminates an entire class of "it worked yesterday" reports.

### 5.4 Better: inner current/velocity loop

The clean fix for deadband + sag is a fast inner motor loop: per-motor velocity PI at 1 kHz (encoders) or current control (driver with current sense, e.g., DRV8876, or FOC controllers like ODrive/SimpleFOC for BLDC). Then the balance loop commands wheel velocity/torque instead of raw PWM, and deadband disappears from its view. For BLDC + FOC platforms (hoverboard motors), torque control is native — these make dramatically better balancers than brushed gearmotors.

---

## 6. Backlash and Mechanical Realities

**Gearbox backlash** — typically 1–3° at the output of cheap plastic gearboxes, 0.5–1° for decent metal ones — is a deadband in *position* with a nastier property: when the correction reverses direction, the motor spins through the lash with zero torque transmitted, then *impacts* the load. Effects:

- Limit cycle similar to PWM deadband, but with an audible clack-clack.
- The impact injects vibration straight into the IMU → corrupted accel → worse estimate → bigger correction → louder clacking. A self-feeding loop.

Mitigations, in order of effectiveness:
1. **Buy lower-backlash drive**: belt drive, or direct-drive hub/BLDC motors (zero gearbox). This is why hoverboard-motor balancers feel "locked" upright.
2. Keep gear ratio modest (≤1:50); lash and reflected inertia scale with ratio.
3. **Mechanical preload**: slight constant torque bias (robot trimmed to lean against one gear flank) keeps the lash taken up while station-keeping.
4. Reduce KD slightly — D-term direction reversals are what exercise the lash fastest.

**Other mechanical rules:**
- **Put the CoM high.** Counterintuitive but correct: higher CoM → larger τ → slower fall → easier control. Battery at the top of the robot, not the bottom.
- **Wheel grip matters**: wheel slip = lost control authority. Soft rubber/foam tires; if it slips during recovery on hard floor, the controller cannot save it.
- **Rigidity**: a flexing chassis between IMU and axle adds an unmodeled resonance, often at 10–30 Hz, which KD will excite.

---

## 7. Segway-Style Steering Mixing

Steering must not disturb balance. Mix the yaw command symmetrically *after* the balance output, with its own (optional) yaw-rate loop:

```c
// steer_cmd: from RC stick or yaw-rate PI on gyro-z (recommended)
float yaw_err  = yaw_rate_cmd - gyro_z;             // deg/s
steer = KYAW_P * yaw_err;                            // simple P often suffices
steer = clampf(steer, -STEER_MAX, STEER_MAX);        // ≤ ~30% of U_MAX

left_cmd  = u + steer;
right_cmd = u - steer;

// CRITICAL: preserve the COMMON-MODE (balance) component when clamping.
// Naive per-channel clipping steals balance authority during hard turns.
float over = fmaxf(fabsf(left_cmd), fabsf(right_cmd)) - U_MAX;
if (over > 0) {                       // reduce STEER first, never balance
    float s = fmaxf(0.0f, fabsf(steer) - over) * signf(steer);
    left_cmd = u + s;  right_cmd = u - s;
    left_cmd = clampf(left_cmd, -U_MAX, U_MAX);
    right_cmd = clampf(right_cmd, -U_MAX, U_MAX);
}
```

Rules:
- **Balance has priority.** When the sum saturates, sacrifice steering, never balance. The asymmetric-clip bug (one wheel clips, the other doesn't → net pitch torque error → faceplant mid-turn) is a classic.
- **Closed-loop yaw on gyro-z** compensates left/right motor mismatch and deadband asymmetry; open-loop differential PWM always curves.
- **Speed-dependent steering**: scale STEER_MAX down with forward speed (`steer_max = STEER_MAX / (1 + |v|/v_ref)`) — at speed, a hard differential command both destabilizes pitch (asymmetric traction) and can flip the robot outward.
- Apply **deadband compensation per wheel, after mixing**, with each wheel's own measured values.

Person-carrying Segway-style machines steer by handlebar lean (roll angle → yaw_rate_cmd) but the mixing math is identical. Add a roll-angle deadzone (±2°) and rate-limit the yaw command (~90°/s² max) to avoid passenger-induced oscillation.

---

## 8. ZMP: From Balancing to Walking

### 8.1 The concept

The **Zero Moment Point** is the point on the ground where the net moment of inertial + gravity forces has no horizontal component. Equivalent (on flat ground) to the center of pressure (CoP) under the feet.

**Stability criterion:** the robot does not tip over **iff the ZMP stays strictly inside the support polygon** (the convex hull of all ground contact points). When the ZMP reaches the polygon's edge, the foot starts to roll about that edge — the robot is tipping, and no ankle torque can stop it (only stepping can).

For the **Linear Inverted Pendulum Model (LIPM)** — CoM constrained to constant height `z_c`, point feet/massless legs:

```
x_zmp = x_com − (z_c / g) · ẍ_com
```

Worked example: humanoid, CoM height z_c = 0.8 m, CoM accelerating forward at ẍ = 1.0 m/s², CoM directly over ankle (x_com = 0):

```
x_zmp = 0 − (0.8 / 9.81)(1.0) = −0.082 m
```

The ZMP is 8.2 cm *behind* the CoM. If the foot is only 12 cm long heel-to-toe with the ankle centered (±6 cm support), this acceleration already puts the ZMP outside the polygon → the robot tips backward. This single equation explains why humanoids accelerate gently or must step.

The measured ZMP/CoP from foot force sensors (4 load cells or an FT sensor per foot):

```
x_cop = Σ(F_i · x_i) / Σ(F_i)
```

### 8.2 ZMP-based walking in one architecture

The classic (Kajita-style) preview-control pipeline still underlies most position-controlled humanoids:

```
Footstep plan (where/when each foot lands)
  → Reference ZMP trajectory (ZMP sits in each support foot, shifts at each step)
  → CoM trajectory generation: solve LIPM so that the resulting ZMP tracks the
    reference — Preview Control (needs ~1.6 s of future ZMP reference) or MPC
  → Inverse kinematics: feet + CoM trajectories → joint angles
  → Stabilizer (feedback layer, 200–1000 Hz):
      measure actual ZMP (foot F/T) and body attitude (IMU)
      • ankle strategy: torque about ankle shifts CoP   (small disturbances)
      • hip strategy: counter-rotate torso              (medium)
      • stepping: modify next footstep location          (large — capture point)
```

Key numbers: LIPM natural frequency `ω = sqrt(g/z_c)` (z_c = 0.8 m → ω = 3.5 rad/s, time constant 0.29 s — same instability math as §1). The **capture point** `x_cp = x_com + ẋ_com/ω` tells you where to step to come to rest; if the capture point leaves the reachable footstep region, a fall is inevitable.

### 8.3 What kills ZMP walkers in practice

- **Compliance you didn't model**: rubber foot soles and series elasticity shift the real ZMP from the commanded one. Measure CoP, close the loop on it — open-loop ZMP trajectories work only on rigid robots on rigid floors.
- **ZMP ≠ stability guarantee** on non-flat / non-rigid ground; the criterion assumes a planar rigid contact.
- **Timing**: late foot touchdown (ground lower than expected by even 5 mm) injects a large unplanned moment. Detect contact with force threshold, not trajectory time.
- Modern torque-controlled robots (and all RL-based locomotion) have moved beyond strict ZMP tracking, but ZMP/capture-point remain the vocabulary for analyzing and debugging *any* walker, and the standard approach for position-controlled hobby/research humanoids.

---

## 9. Complete Reference Implementation Skeleton (200 Hz, C/C++, MCU)

```c
// ============ main loop, driven by 200 Hz timer interrupt ============
volatile bool tick = false;
void timer_isr() { tick = true; }          // 5 ms period, hardware timer

void loop() {
    if (!tick) return;
    tick = false;
    uint32_t t0 = micros();                // watchdog the loop time

    // 1. SENSE (≤ 1 ms): read IMU over I2C @400kHz or SPI
    imu_read(&ax, &az, &gy);               // gy = pitch gyro, deg/s
    gy -= gyro_bias;

    // 2. ESTIMATE: complementary filter
    float theta_acc = atan2f(ax, az) * RAD2DEG;
    theta = 0.98f * (theta + gy * DT) + 0.02f * theta_acc;

    // 3. SAFETY
    if (fabsf(theta) > 35.0f) { motors_off(); state = FALLEN; }
    if (state != BALANCING) { try_arm(); return; }

    // 4. OUTER LOOP (every 4th tick): velocity → theta_setpoint
    if (++div4 >= 4) { div4 = 0; outer_velocity_loop(); }

    // 5. INNER LOOP: balance PID (gyro as D-term, anti-windup)
    float u = balance_pid(theta_setpoint - theta, gy);

    // 6. MIX steering, preserve common mode (see §7)
    mix_and_clamp(u, steer, &uL, &uR);

    // 7. ACTUATE: voltage-normalize + per-wheel deadband, write PWM
    float k = 11.1f / fmaxf(v_batt, 9.0f);
    set_motor_L(apply_deadband(uL * k, DB_L_POS * k, DB_L_NEG * k));
    set_motor_R(apply_deadband(uR * k, DB_R_POS * k, DB_R_NEG * k));

    // 8. INSTRUMENT: assert loop time
    if (micros() - t0 > 4000) overrun_count++;   // must stay << 5000 µs
}
```

Platform notes:
- **Arduino Uno/Nano (16 MHz AVR)**: feasible at 200 Hz only with float-light code and direct register PWM; avoid `Serial.print` in the loop (one 50-char print at 115200 baud = 4.3 ms = a whole tick). Log via binary telemetry or sparse prints.
- **ESP32 / STM32 / RP2040 / Teensy**: comfortable at 500 Hz–1 kHz. ESP32: pin the control task to core 1, keep WiFi/BT on core 0; never put the radio in the control path.
- **Raspberry Pi / Linux + ROS2**: do NOT run the 200 Hz balance loop through the ROS executor on a non-RT kernel — scheduling jitter (occasionally 10+ ms) will drop it. Run balance on an MCU (or RT thread with `SCHED_FIFO` + memory locking) and use ROS2 for the slow layers: `geometry_msgs/Twist` velocity commands in, odometry/IMU telemetry out, via micro-ROS or a serial bridge.

---

## 10. Debugging Methodology

When a balancer misbehaves, **diagnose in this order** — each layer invalidates tuning of the layers above it:

1. **Timing**: scope a GPIO toggle. Loop exactly 200 Hz? Jitter < 5%? Overruns zero?
2. **Estimate quality**: log θ and θ_acc while moving the robot by hand. θ smooth, tracks reality, no lag > ~20 ms, no drift over 60 s while still?
3. **Actuation linearity**: open-loop deadband sweep (§5.1) — recently? at current battery voltage? Both wheels symmetric within ~15%?
4. **Signs**: the §2.3 sign test, plus outer-loop sign and steering sign.
5. **Mechanical**: grab a wheel and rock it — how much lash? Anything loose? IMU mount solid?
6. **Only now, gains** — using the frequency table in §3.4.

Telemetry to log on every tick (binary, dump after run): `t, theta, theta_acc, gyro, theta_setpoint, u, uL, uR, v_batt, wheel_vel`. A 10-second capture plotted in Python answers 90% of questions. The most common findings, in observed order of frequency: loop running slower than believed (println in loop), deadband never compensated, gyro bias not calibrated, one motor wired reversed, battery sag, gearbox lash.

**Tools**: logic analyzer (loop timing), bench PSU instead of battery while tuning (removes the sag variable), phone slow-mo video (limit-cycle frequency measurable frame-by-frame), `pandas`/`matplotlib` for telemetry, and simulation (cart-pole in `gymnasium`/MuJoCo or a 20-line Euler integrator) to sanity-check gains before hardware.
