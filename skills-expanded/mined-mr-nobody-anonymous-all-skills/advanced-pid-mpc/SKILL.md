---
name: advanced-pid-mpc
description: "Use when designing or tuning control loops beyond a single PID — cascade (current/velocity/position) architectures, feedforward (gravity, Stribeck friction), gain scheduling, LQR, and Model Predictive Control. Provides bandwidth-separation rules, discretization-correct implementations, worked cartpole LQR example, exact starting gains, and the failure modes that destroy actuators on real hardware."
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


# Advanced Control: Cascade PID, Feedforward, LQR, MPC

This skill covers the control knowledge that separates "PID that works in sim" from
"control that ships on a robot." Everything here is written so generated code is safe
and correct on real hardware the first time. Read the **Safety Invariants** section
before writing any control code.

---

## 0. Safety Invariants (non-negotiable in generated code)

Every control loop you write MUST have, in this order of priority:

1. **Output saturation** — clamp the command to actuator limits *before* it leaves the
   controller. Never rely on the driver to clamp.
2. **Anti-windup tied to that saturation** — integrators must stop accumulating (or
   back-calculate) when the output is saturated. An unclamped integrator after 2 s of
   stall can command full torque for seconds after the obstruction clears.
3. **Watchdog on the setpoint/feedback stream** — if no new measurement arrives within
   2–3 control periods, command zero torque (or hold position with reduced gains),
   never "use the last value forever."
4. **Rate limit on setpoint changes at the outermost loop** — a step position command
   to a high-gain loop is a torque impulse. Trapezoidal or jerk-limited profiles only.
5. **Sane startup** — initialize integrator to 0, derivative filter state to the first
   measurement (not 0), and the first commanded output to the current actuator state.
   A controller that wakes up commanding a step has killed more gearboxes than bad gains.
6. **NaN guard** — `if (!isfinite(u)) u = 0;` costs nothing. A NaN propagated to a motor
   driver is undefined behavior at 48 V.

```cpp
// Canonical safe output stage — use this pattern in every loop.
double clamp_cmd(double u, double u_min, double u_max, bool& saturated) {
    if (!std::isfinite(u)) { saturated = true; return 0.0; }
    saturated = (u <= u_min) || (u >= u_max);
    return std::clamp(u, u_min, u_max);
}
```

---

## 1. Discrete PID Done Correctly

Most "PID bugs" are discretization bugs. The textbook continuous form
`u = Kp·e + Ki·∫e + Kd·de/dt` must be implemented with these four corrections:

### 1.1 Derivative on measurement, filtered

Differentiate the **measurement**, not the error (kills derivative kick on setpoint
steps), and low-pass filter it. Raw backward-difference of an encoder amplifies
quantization noise by `1/dt` — at 1 kHz that's ×1000.

The filter: first-order with time constant `Tf = Kd/(Kp·N)`, `N = 8…20` typical.
Equivalently, derivative cutoff `f_d ≈ N / (2π·Td)` where `Td = Kd/Kp`. Start with
`N = 10`. If derivative term still looks like grass on a scope, drop N or fix your
velocity estimate (see §1.4).

### 1.2 Anti-windup: conditional integration or back-calculation

- **Conditional (clamping):** integrate only when output is not saturated, or when the
  error would drive the output *out* of saturation. Simple, robust, use by default.
- **Back-calculation:** `i += Ki·e·dt + (u_clamped − u_raw)·dt/Tt`, with tracking time
  `Tt ≈ sqrt(Ti·Td)` or just `Tt = Ti/2`. Smoother recovery; use when the loop sits in
  saturation routinely (e.g., velocity loops during accel-limited moves).

### 1.3 Reference implementation (C++, fixed-rate ISR or RT thread)

```cpp
struct PID {
    // Gains (parallel form: u = Kp*e + Ki*∫e + Kd*de/dt)
    double Kp, Ki, Kd;
    double Tf;          // derivative filter time constant = Kd/(Kp*N)
    double u_min, u_max;
    // State
    double integ = 0.0;
    double d_filt = 0.0;     // filtered derivative of MEASUREMENT
    double y_prev;
    bool   first = true;

    double update(double sp, double y, double dt, double ff = 0.0) {
        if (first) { y_prev = y; first = false; }       // sane startup
        const double e = sp - y;

        // Derivative on measurement, first-order filtered (Tustin-stable form)
        const double d_raw = (y - y_prev) / dt;
        d_filt += dt / (Tf + dt) * (d_raw - d_filt);
        y_prev = y;

        const double u_raw = ff + Kp * e + integ - Kd * d_filt;  // note minus: d(meas)
        bool sat;
        const double u = clamp_cmd(u_raw, u_min, u_max, sat);

        // Conditional integration: only integrate if not saturated,
        // or if error pushes us back toward the linear region.
        if (!sat || (e * u_raw < 0.0))
            integ += Ki * e * dt;

        return u;
    }
    void reset(double y_now) { integ = 0; d_filt = 0; y_prev = y_now; first = false; }
};
```

Key details an AI agent must not "simplify away":
- `−Kd·d_filt` (derivative of measurement enters with a minus sign).
- `reset()` takes the current measurement — call it on mode switches (see §6 bumpless transfer).
- `ff` is the feedforward injection point (§3). Feedforward goes *before* the clamp.

### 1.4 Velocity estimation — the real derivative problem

For motor loops, don't differentiate position in the PID at all. Use one of:
- **Encoder count-per-period** at high speed; **period-between-edges (1/T method)** at
  low speed; blend around ~1 rev/s. This is what good servo drives do.
- **Tracking loop / PLL observer:** a 2nd-order observer on position whose internal
  rate state is your velocity. Bandwidth 5–10× your velocity-loop bandwidth.
- **Kalman/alpha-beta** if you also fuse accelerometer or current-derived torque.

Backward difference of a 4096-count encoder at 1 kHz has velocity resolution
`2π/4096/0.001 ≈ 1.53 rad/s` — useless for a 10 rad/s motion. Do the math like this
*before* blaming gains.

---

## 2. Cascade Control: Current → Velocity → Position

The industry-standard servo architecture. Three nested loops, innermost fastest:

```
pos_ref ──► [Position PI(D)] ──vel_ref──► [Velocity PI] ──iq_ref──► [Current PI] ──► PWM ──► Motor
                 ▲                             ▲                          ▲
              position                      velocity                  phase current
              (encoder)                  (observer, §1.4)             (shunt/ADC)
```

### 2.1 Why cascade beats one big PID

- Each loop linearizes and protects the layer above: the current loop turns a messy
  R-L-back-EMF electrical system into a near-ideal torque source; the velocity loop
  hides friction and load-inertia variation from the position loop.
- Limits become physically meaningful: clamp `iq_ref` = torque limit, clamp `vel_ref`
  = speed limit. Constraint handling falls out for free.
- You tune three easy first/second-order problems instead of one fourth-order one.

### 2.2 Bandwidth separation — the one rule that matters

**Each outer loop must be 4–10× slower than the loop inside it.** Below 4×, the loops
fight: the outer loop "sees" the inner loop's dynamics and the cascade analysis
(inner loop ≈ unity gain) breaks, producing oscillation that no amount of gain
tweaking fixes.

Typical numbers for a brushless servo joint:

| Loop      | Bandwidth (closed-loop) | Sample rate        | Controller |
|-----------|------------------------|--------------------|------------|
| Current   | 1–4 kHz                | 10–40 kHz (PWM-synced) | PI       |
| Velocity  | 100–400 Hz             | 1–10 kHz           | PI (+ FF)  |
| Position  | 10–60 Hz               | 1–4 kHz            | P or PD (+ FF) |

Note the position loop is often just **P**: the velocity loop's integrator already
gives zero steady-state error to constant disturbances, and a position integrator
adds phase lag and limit-cycle risk against stiction. Add position-I only if you have
verified steady-state error from something the velocity integrator can't cancel
(e.g., velocity-loop offset), and keep it tiny with a tight clamp.

### 2.3 Tuning order and exact starting values

Always tune **inside out**. Never touch the position gain until the velocity loop is
verified with a step on a scope.

**Current loop (PI):** with motor phase inductance `L` [H] and resistance `R` [Ω],
pole-zero cancellation design for target current bandwidth `ω_c` [rad/s]:

```
Kp_i = L · ω_c          Ki_i = R · ω_c
```

Example: `L = 0.5 mH`, `R = 0.3 Ω`, target 2 kHz → `ω_c = 2π·2000 ≈ 12566` →
`Kp_i = 6.28 V/A`, `Ki_i = 3770 V/(A·s)`. Limit `ω_c ≤ 2π · f_pwm/10`.

**Velocity loop (PI):** with total reflected inertia `J` [kg·m²], torque constant `Kt`
[N·m/A], target bandwidth `ω_v` (≤ ω_c/5):

```
Kp_v = J · ω_v / Kt          Ki_v = Kp_v · ω_v / 5      (zero a half-decade below ω_v)
```

Example: `J = 2e-4 kg·m²` (motor + reflected load), `Kt = 0.1 N·m/A`, `ω_v = 2π·200`:
`Kp_v = 2e-4 · 1257 / 0.1 = 2.51 A/(rad/s)`, `Ki_v ≈ 631`.

⚠️ `J` includes load reflected through the gearbox: `J = J_motor + J_load/N²`. If the
load inertia varies (a robot arm's does, by 3–10× over the workspace), tune at **max**
inertia for stability, accept sluggishness at min inertia, or gain-schedule (§4).

**Position loop (P):** target `ω_p ≤ ω_v/5`:

```
Kp_p = ω_p     [ (rad/s)/rad — i.e., velocity command per radian of error ]
```

Example: `ω_v = 2π·200` → choose `ω_p = 2π·30 ≈ 188`, so `Kp_p = 188 s⁻¹`. That means
1 mrad of error commands 0.188 rad/s. Sanity-check the number this way every time.

### 2.4 Cascade-specific pitfalls

- **Inner-loop saturation starves the outer loop.** When `iq_ref` clamps, the velocity
  loop is open-loop; its integrator winds up. Anti-windup must exist at *every* level,
  and ideally the inner loop reports saturation upward so the outer integrator halts.
- **Velocity command must be rate-limited** to the accel the current limit can deliver
  (`a_max = Kt·i_max/J`), or the velocity loop lives in saturation during moves.
- **Different sample rates:** the outer loop must use feedback aligned in time with
  its own rate. Don't feed a 10 kHz velocity estimate's instantaneous sample to a
  1 kHz position loop without anti-alias treatment (average over the outer period).

---

## 3. Feedforward: Do the Physics, Let PID Clean Up Residuals

Feedback reacts to error that has already happened. Feedforward commands what physics
says will be needed, so the feedback term handles only model error. On a well-built
servo axis, feedforward carries 80–95% of the command during motion.

### 3.1 Kinematic feedforward (velocity + acceleration)

Given a trajectory `(q_d, q̇_d, q̈_d)`:

```
vel_ref  = Kp_p·(q_d − q) + q̇_d                 // velocity FF into position loop
iq_ref   = PI_v(vel_ref − q̇) + (J·q̈_d + B·q̇_d)/Kt   // accel + viscous FF into velocity loop
```

Velocity feedforward alone typically reduces tracking error during constant-velocity
segments by 10–100×. If you generate trajectories without `q̇_d, q̈_d`, fix the
trajectory generator — numerical differentiation of `q_d` at runtime is acceptable
only if the trajectory is smooth (quintic/trapezoidal), never for raw teleop input.

### 3.2 Gravity feedforward

For a manipulator, compute `g(q)` from the dynamics model (use Pinocchio or KDL —
don't hand-derive beyond 2 DOF):

```python
import pinocchio as pin
tau_g = pin.computeGeneralizedGravity(model, data, q)   # N·m per joint
iq_ff = tau_g / (Kt * gear_ratio * gear_efficiency)
```

Two production realities:
- **Gear efficiency is direction-dependent** (η ≈ 0.7–0.9 driving, can differ
  back-driving; worm gears may not back-drive at all). Holding torque against gravity
  ≠ lowering torque. If you see the arm sag only when moving down, this is why.
- Payload changes `g(q)`. Either re-identify (`payload mass estimation from steady
  iq at two poses), or leave the residual to the integrator and accept a transient
  on pickup/release.

Without gravity FF, the position/velocity integrators hold the arm — meaning every
mode switch or reset drops the arm until the integrator re-winds. Gravity FF makes
controllers swappable.

### 3.3 Friction feedforward — the Stribeck model

Friction torque as a function of velocity:

```
τ_f(v) = [ τ_c + (τ_s − τ_c)·exp(−(v/v_s)²) ]·sgn(v) + B·v
```

- `τ_c` — Coulomb (kinetic) friction. - `τ_s` — static friction (breakaway), τ_s > τ_c.
- `v_s` — Stribeck velocity, the speed at which friction drops from static toward
  Coulomb. Typically 0.001–0.1 rad/s for geared joints.
- `B` — viscous coefficient.

The **Stribeck dip** (friction decreasing as speed rises from zero) is what causes
stick-slip: at crawl speeds the system is locally a *negative*-damping plant, and a
PI velocity loop limit-cycles (hunting). Symptoms: ±a few encoder counts oscillation
at standstill, audible ticking, position "breathing."

**Identification procedure** (do this, don't guess):
1. Command constant velocities spanning 0.001–10 rad/s in both directions (current
   control mode, or read steady-state `iq` in velocity mode).
2. Record steady-state torque (`τ = Kt·iq`) at each speed. Subtract gravity at the
   test pose (or use a gravity-free axis/orientation).
3. Fit the 4 parameters per direction (friction is asymmetric — fit + and − separately).
4. Breakaway `τ_s`: ramp current slowly from zero, record the value at first motion,
   repeat 10×, take the median (it varies with dwell time and temperature — expect
   ±20%).

**Applying it:** feedforward `τ_f(v_ref)` using the *reference* velocity, not measured
(measured velocity near zero is noise, and `sgn(noise)` chatter will excite everything).
Use a smooth sign: `tanh(v_ref/v_blend)` with `v_blend ≈ 2–5× velocity noise floor`.
**Undercompensate**: apply 70–90% of identified Coulomb friction. Overcompensation
flips the sign of effective friction → guaranteed limit cycle, worse than none.

```python
def friction_ff(v_ref, tau_c, tau_s, v_s, B, v_blend, scale=0.8):
    stribeck = tau_c + (tau_s - tau_c) * np.exp(-(v_ref / v_s) ** 2)
    return scale * stribeck * np.tanh(v_ref / v_blend) + B * v_ref
```

Friction changes ~1–2%/°C and with grease age. A compensation tuned cold will
overcompensate warm. If precision matters across thermal range, scale by a
temperature term or use adaptive friction observers — but try the 0.8 scale first.

---

## 4. Gain Scheduling

When plant parameters vary substantially with an observable variable (arm pose →
inertia, airspeed → aero effectiveness, payload → mass), one gain set cannot be both
stable at the worst case and crisp at the best case. Schedule the gains.

**Rules that keep it safe:**
1. **Schedule on slow, measured variables** (pose, speed regime, mass estimate), never
   on the loop's own fast error signal — that creates a hidden nonlinear feedback path.
2. **Interpolate, never switch.** Linear interpolation between gain sets over the
   scheduling variable. Hard switches inject command steps. If you must switch modes,
   use bumpless transfer (§6).
3. **Tune each operating point as a frozen linear problem**, verify stability margins
   at each, then verify at the *midpoints* — interpolated gains between two stable
   sets are not automatically stable, though for PID on mechanical plants they almost
   always are if the points are ≤2× apart in parameter value.
4. **Rate-limit the scheduling variable's effect**: cap gain slew to e.g. 20%/s.

**Worked pattern — inertia-scheduled velocity loop for a 2-link arm:** reflected
inertia at the shoulder varies as `J(q2) = J0 + J1·cos(q2)` (max arm extended). Since
`Kp_v = J·ω_v/Kt` (§2.3), keep the *bandwidth* constant by scheduling:

```python
def scheduled_kp_v(q2, J0, J1, omega_v, Kt):
    J = J0 + J1 * np.cos(q2)        # closed-form reflected inertia
    return J * omega_v / Kt          # constant ω_v across the workspace
```

This is "exact" gain scheduling (inverse-plant). Same idea: schedule current-loop
gains on bus voltage, velocity gains on identified payload mass.

---

## 5. LQR — Linear Quadratic Regulator

### 5.1 What it is, in one breath

For linear dynamics `ẋ = Ax + Bu`, LQR finds the state-feedback `u = −Kx` minimizing
`J = ∫(xᵀQx + uᵀRu)dt`. Solve the continuous algebraic Riccati equation (CARE) for P,
then `K = R⁻¹BᵀP`. Use it when you have a decent linear model and a *multivariable*
problem where nested PIDs would need hand-coordination (balancing robots, cartpole,
drone attitude, anything with coupled states).

### 5.2 Choosing Q and R — Bryson's rule

Don't guess raw numbers. Normalize by maximum acceptable excursions:

```
Q_ii = 1 / (x_i,max)²        R_jj = 1 / (u_j,max)²
```

Then iterate: state too sloppy → raise its Q entry ×10; control too violent/saturating
→ raise R ×10. Q/R only matter as ratios. LQR has guaranteed margins (≥60° phase,
infinite gain margin) **for full-state feedback with a perfect model only** — those
guarantees evaporate with observers and delays, so still verify (§5.5).

### 5.3 Worked example: cartpole stabilization

Cart mass `M = 1.0 kg`, pole mass `m = 0.1 kg`, pole half-length `l = 0.5 m`,
`g = 9.81`. State `x = [p, ṗ, θ, θ̇]` (θ = 0 upright), input `u` = cart force [N].
Linearized about upright:

```
A = [[0, 1, 0,               0],
     [0, 0, -m·g/M,          0],        # = -0.981
     [0, 0, 0,               1],
     [0, 0, (M+m)·g/(M·l),   0]]        # = 21.582
B = [[0], [1/M], [0], [-1/(M·l)]]       # = [0, 1, 0, -2]
```

(Point-mass-pole convention; if using a uniform rod, moment terms change — state your
convention before generating code.)

```python
import numpy as np
from scipy.linalg import solve_continuous_are

M, m, l, g = 1.0, 0.1, 0.5, 9.81
A = np.array([[0,1,0,0],[0,0,-m*g/M,0],[0,0,0,1],[0,0,(M+m)*g/(M*l),0]])
B = np.array([[0],[1/M],[0],[-1/(M*l)]])

# Bryson: |p|<0.5 m, |ṗ|<1, |θ|<0.1 rad, |θ̇|<0.5 ; |u|<10 N
Q = np.diag([1/0.5**2, 1/1.0**2, 1/0.1**2, 1/0.5**2])   # [4, 1, 100, 4]
R = np.array([[1/10**2]])                                 # [0.01]

P = solve_continuous_are(A, B, Q, R)
K = np.linalg.solve(R, B.T @ P)
# K ≈ [[-20.0, -29.4, -160.5, -36.5]]   (sign convention: u = -K x)

eig = np.linalg.eigvals(A - B @ K)
# All real parts negative; fastest pole ≈ -8.4 rad/s → sample ≥ 20× faster (§5.4)
```

Sanity-read the gains: position gain −20 N/m, pole-angle gain −160 N/rad — the
controller pushes the cart *under* a falling pole (the −160·θ term dominates), which
is physically what balancing requires. Always sanity-read K like this; a sign error
here is a runaway cart.

For trajectory tracking, regulate the error: `u = u_ff − K(x − x_d)`. For nonlinear
systems, re-linearize and re-solve along the trajectory = **TVLQR** (the standard
companion to trajectory optimization).

### 5.4 Discretization — where LQR designs die

Closed-loop poles at `s = −8.4 rad/s` need a sample rate honoring two constraints:
- **Rule of thumb:** `f_s ≥ 20–30 × f_bw` (closed-loop bandwidth in Hz). Here
  bw ≈ 8.4/2π ≈ 1.3 Hz → 50 Hz absolute floor, run 100–200 Hz.
- **The killer is latency, not sample rate.** One full sample of delay costs
  `phase lag = 360°·f·Ts` at frequency f — at bandwidth with `f_s = 20·f_bw`, that's
  18° of your phase margin gone, *plus* computation delay, *plus* ZOH lag (≈ half a
  sample). Budget: total delay < 1/(10·ω_bw) seconds.

Do it properly: discretize the plant (`scipy.signal.cont2discrete`, ZOH) and solve the
**discrete** ARE (`solve_discrete_are`) at your actual Ts; if you can't, the continuous
K is fine when `f_s > 30× bandwidth`. Never apply continuous-K at `f_s < 10×` — it will
oscillate and you'll mis-blame Q/R. If your control output is applied one cycle late
(common in ROS pipelines), augment the discrete model with a delay state
`x_aug = [x; u_prev]` and design against that.

### 5.5 You don't have full state

LQR needs all of x. With encoders only, you estimate velocity (§1.4) or build a Kalman
filter → LQG. **LQG has no guaranteed margins** (Doyle, 1978 — the famous one-line
abstract: "There are none."). After designing LQG, *measure* margins: inject a swept
sine or chirp at the plant input in sim, compute the loop transfer, demand ≥6 dB gain
margin and ≥35–45° phase margin. If short, speed up the observer (5–10× the controller
bandwidth) or use Loop Transfer Recovery / just retune with more R.

---

## 6. Bumpless Transfer (mode switching)

Any switch — manual→auto, PID→LQR, gain-set A→B, e-stop recovery — must not step the
output. Standard technique: at the switch instant, back-solve the incoming
controller's integrator so its output equals the outgoing controller's last output:

```cpp
// Switching into PID at time t0, previous output u_prev:
pid.reset(y_now);                       // derivative state = current measurement
pid.integ = u_prev - pid.Kp * (sp - y_now) - ff_now;   // output continuity
```

Also ramp the *setpoint* from current position to target after any re-engage; never
re-engage onto a stale setpoint.

---

## 7. Model Predictive Control

### 7.1 The concept in five lines

At every control step: (1) measure/estimate state x; (2) solve, over a horizon of N
steps, for the input sequence minimizing a cost (tracking error + effort) **subject to
explicit constraints** (input limits, state limits, obstacle half-planes); (3) apply
only the first input; (4) repeat next step (receding horizon). For linear models +
quadratic cost + linear constraints it's a QP — convex, solvable in microseconds to
milliseconds with the right solver.

MPC is "constrained LQR re-solved online." With no active constraints and infinite
horizon, linear MPC *is* LQR.

### 7.2 When MPC is worth it — and when it isn't

**Worth it when:**
- Constraints are routinely *active* and define performance: torque-limited swing-up,
  legged-robot friction cones and ZMP bounds, mobile-robot obstacle avoidance,
  battery/thermal-limited drones. PID+clamps handles constraints by saturating
  (reactive); MPC *plans* around them (anticipatory).
- You need **preview**: known future reference (a path) or disturbance (terrain ahead).
  Nothing in the PID/LQR family uses future information.
- Strong MIMO coupling + constraints together (quadruped whole-body control).

**Not worth it when:**
- A single joint/axis with rare saturation → cascade PID + FF matches MPC performance
  at 1% of the engineering cost. This is most industrial axes.
- You cannot maintain a model. MPC degrades *worse* than PID under model error —
  it confidently optimizes the wrong plant.
- Your compute/latency budget can't fit the solve (§7.4). A late MPC output is worse
  than an on-time PID output.

Honest engineering default: **cascade PID with feedforward inside, MPC outside** —
e.g., MPC at 50–100 Hz produces joint/body trajectories respecting constraints; joint
servos at 1–10 kHz track them. This is how Boston-Dynamics-style and most legged/
mobile stacks actually work.

### 7.3 Formulation skeleton (linear MPC as a QP)

```
min  Σ_{k=0}^{N-1} (x_k−x_ref)ᵀQ(x_k−x_ref) + u_kᵀR u_k + Δu_kᵀS Δu_k  +  x_NᵀP x_N
s.t. x_{k+1} = A_d x_k + B_d u_k          (discretized model, §5.4)
     u_min ≤ u_k ≤ u_max                  (hard — actuators physically clamp anyway)
     x_min ≤ x_k ≤ x_max  (+ slack σ_k ≥ 0, cost ρ·σ²)   (SOFT — see below)
```

Non-obvious but critical choices:
- **Terminal cost P = discrete-ARE solution** (the LQR cost-to-go). This is the cheap
  approximation of an infinite horizon and is the single biggest stability lever in
  practical MPC. Without a terminal cost, short horizons cause myopic, oscillatory,
  or unstable behavior.
- **State constraints must be soft** (slack variables with heavy penalty,
  ρ ≈ 10³–10⁶ × tracking weights). A hard state constraint + one disturbance =
  infeasible QP = solver returns garbage or nothing = robot falls. Input constraints
  stay hard.
- **Δu penalty S** smooths chatter and respects rate limits; it's also your knob
  against solver-to-solver jitter.
- **Horizon N:** cover the dominant dynamics — `N·Ts ≈ 1–2× the slowest relevant time
  constant`. Quadrotor position: N·Ts ≈ 1–2 s. Quadruped balance: 0.5–1.5 gait cycles.
  Longer horizons cost O(N) to O(N³) depending on solver; condensing vs. sparse
  formulations trade differently (sparse wins for N ≳ 20).

### 7.4 Tools and real-time budget

| Tool | Use case |
|------|----------|
| OSQP | Linear MPC QP workhorse; warm-startable; embeddable C |
| acados | Nonlinear MPC (SQP-RTI), code-gen, the current robotics standard |
| CasADi | Prototyping NMPC, derivative generation (feeds acados/IPOPT) |
| qpOASES / HPIPM | Embedded dense / sparse QPs inside acados |
| Crocoddyl / OCS2 | DDP/iLQR-style whole-body MPC for legged robots |

Real-time rules:
- **Warm-start every solve** from the previous solution shifted one step. Cold-start
  NMPC at 100 Hz does not converge in budget.
- **Real-Time Iteration (RTI):** run exactly one SQP iteration per control step. The
  solution is slightly suboptimal but on time, and converges across steps. This is the
  standard NMPC-on-robots trick.
- Solve time must fit: budget ≤ 50% of the control period, and **apply the input at a
  fixed phase** of the cycle (compute-then-hold), not "whenever the solver finishes" —
  jittery latency is destabilizing even when average latency is fine.
- **Always have a fallback:** if the solver fails/exceeds budget, apply the previous
  plan's next input (you stored the whole sequence — use it), decaying toward a safe
  command (zero torque / gravity-compensation) after 2–3 consecutive failures. Log
  every solver failure; a 0.1% failure rate is a crash waiting for the wrong moment.

### 7.5 MPC failure modes seen in production

- **Model mismatch → steady-state offset.** MPC has no integrator by default. Fix:
  disturbance observer / offset-free MPC (augment a constant input disturbance state,
  estimate it, include in prediction). Do this from day one; everyone needs it.
- **Infeasibility cascades** from hard state constraints (fix: slacks, §7.3).
- **Reference far outside the feasible set** makes the QP fight constraints all
  horizon long → erratic. Pre-filter references to something reachable.
- **Discretization mismatch**: model discretized at Ts but loop actually runs at
  1.3·Ts under load → systematic prediction error. Measure your real loop period.

---

## 8. Control Loop Frequency: Rules of Thumb, with Reasons

The chain of inequalities to design by:

```
f_sample ≥ 10–30 × f_closed-loop-bandwidth        (20× is the safe default)
f_closed-loop ≤ (1/5 … 1/10) × inner-loop bandwidth      (cascade separation, §2.2)
f_closed-loop ≤ (1/5) × first structural resonance        (or notch it, see below)
total latency  ≤ 1/(10 × ω_bw)  seconds                   (latency dominates, §5.4)
```

- **Why 10–30× and not Nyquist's 2×:** Nyquist is about reconstruction, not control.
  Each sample period of effective delay (ZOH ≈ Ts/2, compute, transport) eats phase
  margin: at 10× you lose ~18–27° at bandwidth; at 20× ~9–14°. You typically only have
  45–60° to spend.
- **Structural resonance is the usual true limit**, not the sample rate. A belt axis
  with first resonance at 80 Hz caps your position bandwidth near 15–25 Hz regardless
  of how fast you sample, unless you add a notch filter at the resonance (then re-check
  phase: notches cost phase below their center frequency).
- **Filters count as delay.** A 2nd-order Butterworth LPF at f_c contributes ~90° of
  phase at f_c and ~12° at f_c/4. Put your derivative/velocity filters at ≥5× the
  loop bandwidth or account for them explicitly.
- **ROS 2 reality:** a vanilla rclcpp timer callback has ms-level jitter — fine for a
  20 Hz planner, fatal for a 1 kHz servo. High-rate loops belong in `ros2_control`'s
  realtime update loop (controller as a plugin, SCHED_FIFO, locked memory), on a
  PREEMPT_RT kernel, or on the motor-drive MCU itself, with ROS supervising at low
  rate. Never put a torque loop behind a DDS topic hop.

### Quick reference: typical rates on real robots

| System | Loop | Rate |
|---|---|---|
| BLDC servo drive | current | 10–40 kHz |
| Servo drive | velocity / position | 1–10 kHz / 1–4 kHz |
| Manipulator joint impedance | torque loop | 1–4 kHz |
| Quadruped whole-body MPC | MPC / leg servo | 50–500 Hz / 1–10 kHz |
| Quadrotor | attitude rate / position | 0.5–8 kHz / 50–250 Hz |
| Mobile base | velocity / nav | 50–200 Hz / 10–20 Hz |

---

## 9. Debugging Methodology (in order; don't skip steps)

1. **Plot, don't stare.** Log setpoint, measurement, each PID term (P, I, D, FF)
   separately, raw output, clamped output, saturation flag — at full loop rate. If you
   can't log at loop rate, you can't debug the loop.
2. **Verify timing first.** Measure actual loop period jitter and sensor latency
   (toggle a GPIO / timestamp at source). >10% period jitter or one unaccounted period
   of delay explains most "mystery oscillations." Do this before touching a gain.
3. **Verify the plant model with a step/chirp in open loop** (small, safe amplitude):
   does measured `J` match assumed `J`? A 2× inertia error makes every model-based
   gain in this document 2× wrong.
4. **Classify the oscillation:**
   - Frequency near loop bandwidth, grows with Kp → ordinary gain margin; reduce Kp
     or add phase (better velocity estimate, less filter lag).
   - Constant small amplitude at standstill, frequency low and amplitude ~encoder
     counts → stiction limit cycle (§3.3) or position-integrator hunting; reduce/clamp
     position-I, fix friction FF scale.
   - Frequency = a structural resonance, independent of gains → mechanical; notch or
     lower bandwidth.
   - Appears only after saturating moves → windup; verify anti-windup actually engages
     (log the flag).
   - Appears only at one pose/payload → parameter variation; gain-schedule (§4).
5. **One change at a time, scope step response after each.** Overshoot ~10–20% and one
   visible undershoot ≈ ζ ≈ 0.5–0.7 — healthy. Tune Kp for rise, zero location
   (Ki/Kp) for settling, never chase noise with Kd.
6. **For MPC:** log solver status, iterations, solve time, active-set changes, and the
   *predicted vs. realized* state one step ahead. Persistent one-step prediction error
   is model mismatch — fix the model or add the disturbance observer before touching
   weights.

---

## 10. Decision Guide

```
Single axis, constraints rarely active            → PID (+ FF). Done. (§1–3)
Servo axis, performance matters                   → Cascade PI/P + vel/accel/gravity/friction FF (§2–3)
Parameters vary >2× with measurable variable      → + gain scheduling (§4)
Coupled MIMO, good linear model, no hard limits   → LQR / LQG (verify margins) (§5)
Constraints define performance, preview available → MPC outside, servo loops inside (§7)
Nonlinear + constrained + fast (legged, agile)    → NMPC (acados RTI) or DDP, 50–500 Hz, with PID fallback
```

The fallback chain on hardware is always: **fancy controller → cascade PID → zero
torque / gravity comp → mechanical brake.** Build the bottom layers first and keep
them armed.
