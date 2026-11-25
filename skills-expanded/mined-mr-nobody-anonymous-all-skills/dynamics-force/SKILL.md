---
name: dynamics-force
description: "Use when a robot arm moves fast, interacts with the environment (contact, insertion, polishing, human contact), or position control alone is failing — torque ripple, overshoot at speed, crashes on contact. Provides rigid-body dynamics, torque vs position control, impedance/admittance control design with starting gains, F/T sensor integration, and current-based collision detection."
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


# Robot Dynamics & Force Control

Kinematics tells you *where* the robot is. Dynamics tells you *what torques it takes to get there* — and what happens when it touches something. This skill covers the point where position control stops being enough: fast motion, contact tasks, and safety.

**The single most important rule in this domain: a position-controlled robot in contact with a stiff environment is a force amplifier with no upper bound.** 1 mm of position error against a 10⁶ N/m surface is 1000 N. Everything in force control exists to break that amplification.

---

## 1. When Kinematics Isn't Enough

Pure kinematic (position) control assumes the low-level joint servos perfectly reject all torque disturbances. That assumption breaks when:

| Symptom | Dynamic cause |
|---|---|
| Tracking error grows with speed, worst mid-trajectory | Unmodeled inertia/Coriolis torques exceed servo bandwidth |
| Overshoot/oscillation on fast stops | Kinetic energy ½ω^T M(q) ω must go somewhere; PD gains too low to absorb it |
| Sag when payload added, droop at horizontal poses | Gravity torque not feedforward-compensated |
| Path error on curved high-speed moves | Coriolis/centrifugal terms (quadratic in velocity — invisible at low speed, dominant at high speed) |
| Robot crashes/faults the instant it touches a surface | Position control + stiff environment = unbounded force |
| Vibration at specific poses | Configuration-dependent inertia changes the resonant frequency; fixed gains tuned at one pose are wrong at another |

Rule of thumb: if joint velocities exceed ~25% of rated max, or if the tool will *touch* anything whose position you don't know to better than your servo stiffness allows, you need dynamics.

---

## 2. The Equations of Motion (the part you actually use)

For an n-DOF rigid manipulator:

```
M(q) q̈ + C(q, q̇) q̇ + g(q) + F_f(q̇) = τ + J(q)^T F_ext
```

- `M(q)` — n×n symmetric positive-definite mass/inertia matrix. Configuration-dependent: an arm stretched out has far more effective inertia at the shoulder than folded up (for a point mass m at reach r, reflected inertia goes as m·r² — doubling reach quadruples shoulder inertia).
- `C(q,q̇)q̇` — Coriolis/centrifugal torques, quadratic in velocity. Key property: `Ṁ − 2C` is skew-symmetric (used in stability proofs, and a good unit test for your dynamics code).
- `g(q)` — gravity torques. Usually the *largest* term for industrial arms at normal speeds. Compensate this first; it's 80% of the benefit for 20% of the work.
- `F_f(q̇)` — friction. Typically modeled as `F_v q̇ + F_c sign(q̇)` (viscous + Coulomb). On geared robots friction can be 10–30% of rated torque. Never use raw `sign()` in code — see §8.
- `τ` — motor torques (after gearbox), `J^T F_ext` — external wrench mapped to joint torques.

**Worked example — why gravity compensation matters.** A 2-link planar arm, links 1 m each, masses 10 kg and 5 kg at link midpoints, both links horizontal:

```
τ_shoulder = m1·g·0.5 + m2·g·(1 + 0.5) = 10·9.81·0.5 + 5·9.81·1.5 = 49 + 73.6 ≈ 123 N·m
τ_elbow    = m2·g·0.5 = 24.5 N·m
```

123 N·m of static torque before the arm even moves. A PD controller without gravity feedforward must generate this through position *error* — with Kp = 1000 N·m/rad that's a 7° permanent sag at the shoulder. This is why "my arm droops" is always a gravity-model problem, not a gain problem.

**Worked example — Coriolis at speed.** Same arm, shoulder swinging at 2 rad/s, elbow extending at 2 rad/s: the Coriolis torque on the shoulder is on the order of `2·m2·l1·lc2·sin(q2)·q̇1·q̇2` ≈ 2·5·1·0.5·sin(45°)·2·2 ≈ 28 N·m. At 0.2 rad/s each it would be 0.28 N·m — negligible. Quadratic scaling means a robot tuned at commissioning speed misbehaves when production cranks the override to 100%.

### Computing dynamics in code

Never hand-derive M, C, g for more than 2 links. Use:

- **Pinocchio** (C++/Python) — the industry standard. Fast recursive algorithms (RNEA for inverse dynamics, CRBA for M(q), ABA for forward dynamics).
- **`KDL`** — ships with ROS, fine for chains, slower.
- **MuJoCo / Drake** — if you're already simulating there.
- The robot's URDF must have **correct inertial tags**. A URDF with default `<inertia ixx="1" .../>` placeholders will produce garbage torques. Get inertias from CAD or the manufacturer's datasheet; for a quick sanity check, each link's inertia must satisfy the triangle inequality (ixx + iyy ≥ izz, etc.) or Pinocchio/physics will be wrong.

```python
import pinocchio as pin
model = pin.buildModelFromUrdf("arm.urdf")
data = model.createData()

# Inverse dynamics: torque needed for (q, v, a) — RNEA, O(n)
tau = pin.rnea(model, data, q, v, a)

# Gravity vector alone (v = a = 0)
g = pin.computeGeneralizedGravity(model, data, q)

# Mass matrix — CRBA
M = pin.crba(model, data, q)

# Coriolis matrix
C = pin.computeCoriolisMatrix(model, data, q, v)
```

**Unit test your dynamics** before trusting them on hardware:
1. `tau = rnea(q, 0, 0)` must equal `g(q)` exactly.
2. `M(q)` symmetric, all eigenvalues > 0, at every test pose.
3. Energy check in simulation: with τ = 0 and no friction/gravity, kinetic energy ½q̇ᵀMq̇ must be constant to integration tolerance.
4. Skew-symmetry: `x^T (Ṁ − 2C) x ≈ 0` for random x.

---

## 3. Torque Control vs Position Control

### Position control (what 95% of industrial robots run)
Each joint runs a fast inner loop (current → velocity → position, cascaded, 1–10 kHz inner rates). You command q_des; the drive does the rest. High gear ratios (50:1–160:1 harmonic drives) make the arm *stiff* and mask dynamics — reflected rotor inertia scales as gear ratio², so the motor-side inertia dominates and link-side dynamic coupling looks like a small disturbance.

- **Pros:** precise (±0.02 mm repeatability), robust to payload model error, simple to program.
- **Cons:** mechanically stiff (10⁵–10⁷ N/m at the flange). Contact with a rigid surface generates huge forces from tiny errors. Cannot regulate force. Dangerous around humans without external sensing.

### Torque control (research arms, cobots: Franka, KUKA iiwa, UR e-series partially)
You command joint torques directly at 0.5–4 kHz (Franka: 1 kHz hard real-time; miss the deadline and the arm reflexes to a stop). The arm is only as stiff as your control law makes it — which is the entire point.

- **Pros:** programmable compliance, force regulation, safe contact, can implement impedance control natively.
- **Cons:** accuracy depends on your dynamic model quality; gravity model error appears directly as drift; needs real-time computing (RT-PREEMPT kernel, no GC pauses — don't write the 1 kHz loop in garbage-collected languages).

### Computed torque (inverse dynamics control) — the bridge

If you have torque access and a good model, cancel the dynamics and impose linear error behavior:

```
τ = M(q)(q̈_des + Kd ė + Kp e) + C(q,q̇)q̇ + g(q)        where e = q_des − q
```

This makes each joint behave like `ë + Kd ė + Kp e = 0`. Choose per-joint:

```
Kp = ω² ,  Kd = 2ζω      with ζ = 1.0 (critical damping), ω = 2π·f
```

Start f at 5–10 Hz for a big arm, up to 20 Hz for a small stiff one. ω must be ≤ ~1/3 of the lowest structural resonance (harmonic drive joint resonances are typically 10–40 Hz — this is your ceiling, and why you can't just crank gains).

**Practical gravity-compensation-only mode** — the simplest useful torque controller, and the standard "hand-guiding" demo:

```
τ = g(q) + small damping (−D q̇)
```

If the arm drifts when you let go, your mass model is wrong (usually the unmodeled tool — add the tool's mass and CoM to the model; on Franka, set it via `setLoad()` rather than editing the URDF).

---

## 4. Impedance Control — the workhorse of contact tasks

**Concept.** Instead of controlling position *or* force, control the *relationship* between them. Make the end-effector behave like a mass-spring-damper anchored to a virtual setpoint:

```
F = K (x_des − x) + D (ẋ_des − ẋ)     [+ Λ(ẍ_des − ẍ) if you do full impedance]
```

Free space: spring pulls EE to x_des → behaves like position control. Contact: penetration is limited, force is K·δx → bounded, programmable. One controller, both regimes, no mode switching. This is why impedance control wins for insertion, polishing, and human interaction.

**Cartesian impedance law (torque-controlled robot):**

```
τ = J^T [ K (x_des − x) + D (ẋ_des − ẋ) ] + g(q) + C(q,q̇)q̇ + τ_null
```

with nullspace term for redundant (7-DOF) arms:

```
τ_null = (I − J^T (J^T)⁺) [ K_null (q_rest − q) − D_null q̇ ]
```

Without τ_null a 7-DOF arm's elbow drifts into joint limits while the EE holds pose perfectly. Always include it. `(J^T)⁺` should be the dynamically-consistent pseudoinverse if you can compute it; the plain Moore–Penrose pseudoinverse works acceptably for modest motions.

**Damping design — do not guess D.** For each Cartesian axis with stiffness k and effective mass m (from the task-space inertia Λ = (J M⁻¹ J^T)⁻¹):

```
d = 2 ζ √(k·m)        ζ = 0.7–1.0
```

A common, simpler factorized form used in practice (and in Franka's examples): `D = 2·ζ·sqrt(K)` elementwise after normalizing — fine to start, but if the arm buzzes in some poses and is sluggish in others, switch to the Λ-based design because task-space mass varies with configuration.

**Starting values (6-DOF Cartesian, medium arm like Franka/UR10e):**

| Task | K_trans (N/m) | K_rot (Nm/rad) | ζ |
|---|---|---|---|
| Hand-guiding / gravity-comp feel | 0–50 | 0–5 | 1.0 |
| Compliant insertion (peg-in-hole) | 300–800 | 20–50 | 0.8 |
| Surface following / polishing | 500 normal, 1500–3000 tangential | 50–150 | 0.7 |
| Stiff positioning with contact safety | 2000–4000 | 100–300 | 0.8 |

Franka hard limits: translational stiffness ≤ ~3000 N/m, rotational ≤ ~300 Nm/rad in their Cartesian impedance interface. Anisotropic K is the standard trick: stiff where you trust the geometry, soft along the uncertain axis (e.g., soft in Z for surface contact, stiff in XY for path accuracy).

**Minimal correct implementation (Python-style pseudocode, runs at ≥ 500 Hz):**

```python
# Setup (once)
K = np.diag([800, 800, 400, 30, 30, 30])      # soft in z for contact
D = 2.0 * 0.8 * np.sqrt(K)                     # factorized damping, zeta=0.8

def control_step(q, dq, x_des):
    pin.forwardKinematics(model, data, q, dq)
    x   = ee_pose(data)                        # SE(3)
    J   = pin.computeFrameJacobian(model, data, q, EE_FRAME,
                                   pin.LOCAL_WORLD_ALIGNED)
    err = pose_error(x_des, x)                 # 6-vec: [Δp; rotation log]
    dx  = J @ dq

    F_imp = K @ err - D @ dx                   # virtual wrench
    g     = pin.computeGeneralizedGravity(model, data, q)

    tau = J.T @ F_imp + g + nullspace_torque(q, dq, J)
    return np.clip(tau, -tau_limit, tau_limit)
```

Two details that break naive implementations:
- **Orientation error must be a proper rotation error** — `log(R_des R^T)` (axis-angle of the relative rotation), or the quaternion vector-part error with sign continuity (`if dot(q_des, q) < 0: q = -q`). Subtracting Euler angles will work in demos and fail at the wrap-around, hard, on hardware.
- **The desired pose must move smoothly.** Step changes in x_des inject a step force K·Δx. Filter or interpolate the setpoint; a 2 cm step with K=3000 N/m is a 60 N hammer blow.

### Admittance control — the same idea, inverted, for stiff robots

If your robot only accepts *position* commands (most industrial arms), you can't shape torque — instead, measure force and move the position setpoint:

```
Λ ẍ_c + D ẋ_c + K (x_c − x_des) = F_measured
```

Integrate this ODE each cycle to get a commanded pose x_c that "gives way" under measured force:

```python
def admittance_step(F_meas, x_des, dt):
    global x_c, dx_c
    ddx_c = inv(LAMBDA) @ (F_meas - D @ dx_c - K @ (x_c - x_des))
    dx_c += ddx_c * dt
    x_c   = integrate_pose(x_c, dx_c * dt)    # SE(3) integration, not naive add for rotation
    send_cartesian_position(x_c)
```

Starting values: Λ = diag(5–20 kg, 0.1–1 kg·m²), K and D as in the impedance table, loop at 250–1000 Hz (it must run faster than the robot's position-command interface consumes setpoints — UR: 500 Hz RTDE, Franka position interface: 1 kHz).

**Impedance vs admittance — the duality that decides which to use:**
- *Impedance* (torque-based) is **stable in stiff contact** but renders soft behavior poorly on high-friction geared robots (friction masks small commanded torques).
- *Admittance* (position-based) renders **soft behavior beautifully** on stiff robots, but goes **unstable against stiff environments**: the F/T sensor measures contact, the controller commands retreat, the stiff inner loop overshoots, contact force spikes, repeat — a chatter/bouncing limit cycle. Mitigations: increase virtual mass Λ and damping D, low-pass the force signal (but every Hz of filtering eats stability margin elsewhere), reduce inner-loop stiffness if possible. If the task is metal-on-metal contact with an admittance-controlled robot and it chatters, this is why — it is structural, not a tuning bug, and the honest fixes are more virtual inertia or a compliant pad on the tool.

### Direct force control / hybrid force-position

For explicit force regulation along one axis (press with exactly 20 N while wiping a surface): split Cartesian axes with a selection matrix S — force-controlled subspace gets a force PI loop, the rest stays position/impedance:

```
F_cmd_z: τ_f = J^T S [ Kf_p (F_des − F_meas) + Kf_i ∫(F_des − F_meas)dt ]
```

Start Kf_p ≈ 0.1–1 (dimensionless if output is a velocity offset: m/s per N → start 0.001–0.005), Kf_i small, and **always clamp the integrator** — when contact is lost, F_meas = 0 and the integrator winds up, then the robot lunges at the surface on re-contact. Anti-windup on the force integrator is not optional. Also gate the force loop on a contact-detection flag: pure force control in free space accelerates the arm until something stops it.

---

## 5. Force-Torque Sensor Integration

Typical hardware: ATI (Axia, Gamma, mini40/45), Bota, Robotiq FT-300, OnRobot HEX; or built-in joint-torque-derived estimates (Franka's O_F_ext_hat_K, iiwa). Wrist F/T sensors give clean 6-axis measurement at 1–7 kHz; joint-torque-based estimates are free but noisier and miss forces that don't produce joint torque in singular directions.

**The non-negotiable processing pipeline, in order:**

1. **Bias removal.** Every F/T sensor has a non-zero reading at zero load (temperature-dependent drift, mounting stress). Re-zero ("taring") at task start *in a known pose with no contact*. Drift can be several N over hours — re-tare between task cycles if force thresholds are tight.

2. **Gravity/payload compensation.** The tool below the sensor (gripper + part) has weight m_t·g and CoM r_t. As the wrist rotates, this load shows up as a *changing* force/torque that looks exactly like contact:

```
F_comp = F_raw − R_sensor_world^T (m_t · g_world)
T_comp = T_raw − r_t × (R_sensor_world^T m_t g_world)
```

Identify m_t and r_t by recording F_raw at 10–20 diverse orientations with no contact and least-squares fitting. A 1 kg gripper mis-compensated produces ~10 N of phantom "contact" force — more than most insertion task thresholds. **This is the #1 cause of "the force controller works in one orientation and not another."**

3. **Inertial compensation (fast motion only).** Accelerating the tool mass produces F = m_t·a at the sensor. Below ~1 m/s² ignore it; for fast force-controlled motion, subtract m_t·ẍ using filtered acceleration.

4. **Filtering.** Raw F/T is noisy (mechanical resonance of the tool on the sensor, often 100–500 Hz). Use a 2nd-order Butterworth low-pass; cutoff trade-off:
   - Force *display*/logging: 10 Hz.
   - Force *control loop*: 20–100 Hz — as high as noise allows, because filter phase lag directly erodes your stability margin (a 10 Hz filter adds ~ms-scale lag that can destabilize a stiff admittance loop).
   - Collision *detection*: lighter filtering (50–150 Hz) — latency is the enemy.

5. **Frame transforms.** Sensor measures in its own frame. Transform the wrench to the control frame (EE or task frame) with the adjoint:

```
F_ee = R · F_sensor
T_ee = R · T_sensor + p × (R · F_sensor)     # p = sensor origin → EE origin, in EE frame
```

Getting the lever-arm cross-product term wrong is the #2 integration bug: forces look right, torques are mysteriously offset, and force-controlled orientation behavior is wrong.

**ROS2:** sensors publish `geometry_msgs/WrenchStamped`; `ros2_control` has `force_torque_sensor_broadcaster`; admittance is available as `admittance_controller` in ros2_controllers (configure its `chainable` inner position controller, mass/damping/stiffness per axis). Check `frame_id` and verify sign conventions empirically — push on the tool in +X and confirm the reading; vendors disagree on whether the sensor reports the force *applied to* it or *exerted by* it.

**Hardware mounting:** the sensor's rated overload matters — a wrist sensor rated 500 N survives a position-control crash poorly. Mechanical fuses (shear pins, magnetic tool changers) are cheaper than sensors.

---

## 6. Collision Detection from Motor Current

You can detect collisions with **no extra sensors**: motor current is proportional to motor torque (τ_m = k_t · i), so unexpected torque = unexpected current.

**Method 1 — model-based residual (the right way when you can run a model):**

```
τ_expected = M(q)q̈ + C(q,q̇)q̇ + g(q) + F_f(q̇)
r = τ_measured − τ_expected          # τ_measured = k_t · gear_ratio · i  (per joint)
collision if |r_j| > threshold_j  for longer than t_min
```

The naive version needs q̈ (numerically differentiating velocity → noise). Production systems use the **generalized momentum observer** (De Luca et al.), which needs only q, q̇, τ:

```
p = M(q) q̇                                    # generalized momentum
ṙ = K_O ( ṗ_est_error )  →  implemented as:
r(t) = K_O [ p(t) − ∫₀ᵗ (τ + C^T q̇ − g + r) dt − p(0) ]
```

Each component r_j is a first-order-filtered estimate of the external torque on joint j, with bandwidth K_O. No acceleration needed. Set K_O = 10–50 rad/s per joint (higher = faster detection, more noise sensitivity). This is essentially what Franka and KUKA run internally.

```python
# Momentum observer, one step (run at control rate, dt ~ 1ms)
def momentum_observer_step(q, dq, tau_cmd, dt):
    global integral, r
    M = pin.crba(model, data, q)
    C = pin.computeCoriolisMatrix(model, data, q, dq)
    g = pin.computeGeneralizedGravity(model, data, q)
    p = M @ dq
    integral += (tau_cmd + C.T @ dq - g + r) * dt
    r = K_O @ (p - integral - p0)
    return r          # estimated external joint torques
```

**Method 2 — signature/learning-based (when no good model exists):** record current profiles over many clean executions of the *same* trajectory, build a per-sample envelope (mean ± kσ, k = 3–5), flag excursions. Works for fixed cyclic tasks (most industrial cells); breaks the moment the trajectory, payload, or temperature changes. Use it for legacy position-controlled robots where you only have drive current telemetry.

**Thresholds and the friction problem.** Detection sensitivity is limited by model error, and the dominant model error is **friction**: it's temperature-dependent (cold robot Monday morning has 20–40% higher friction than after 30 min warm-up), load-dependent, and direction-dependent. Practical numbers for a geared industrial arm:
- Achievable detection threshold: 5–20 N·m at proximal joints, 1–5 N·m distal — i.e., ~10–50 N at the end-effector. Good enough to protect equipment and detect crashes; **not** sensitive enough alone for ISO/TS 15066 power-and-force-limited human collaboration on a big arm (cobots achieve better via joint torque sensors).
- Use velocity-dependent thresholds: wide bands at velocity reversals (Coulomb friction sign flip is poorly modeled), tighter at steady motion.
- Require persistence: |r| > threshold for ≥ 2–5 ms to reject spikes; every ms of persistence adds reaction latency — budget total detect-to-brake at < 50 ms for safety claims.

**Reaction strategy** (in increasing gentleness): (a) category-1 stop (brakes); (b) zero-velocity hold; (c) **switch to gravity compensation** — the arm goes limp, which minimizes clamping force on a trapped person/part and is usually the right default for cobots; (d) reflex retreat along −r direction. Pick per-application; clamping scenarios (arm pinning something against a fixture) demand (c) or (d), because a braked stop *maintains* the clamping force.

**Distinguishing collision from contact task:** if you're running a force-controlled task, expected contact appears in r. Subtract the commanded/expected task wrench (J^T F_des) from the residual before thresholding, or mask the force-controlled axes.

---

## 7. Stability — why force control loops oscillate

The contact loop's stability is governed by the *product* of controller stiffness and environment stiffness against the sampling/filter delays:

- **Coupled stiffness:** in contact, effective stiffness is series: `k_eff = (1/K_ctrl + 1/k_env)⁻¹`. Against rigid steel (k_env → 10⁶–10⁷ N/m), k_eff ≈ K_ctrl — your controller sets the contact dynamics, which is the whole point of impedance control.
- **Passivity budget:** every delay (sensor filter, transport, ZOH at control rate, drive lag) injects phase loss. A discrete impedance controller at rate f_s rendering stiffness K is passive only up to roughly `K < d · f_s` regimes (Colgate–Hogan condition `K·T/2 < d` for the virtual wall case). Practical reading: **if it chatters, you need more damping, a faster loop, or less stiffness — in that order of preference.**
- **Symptom table:**
  - High-frequency buzz in free space → D too high relative to K, or noisy velocity estimate (filter q̇, don't raw-differentiate encoders at 1 kHz).
  - Bouncing on contact, grows then limit-cycles → admittance vs stiff environment (§4) or K too high for loop rate.
  - Slow oscillation (~1–3 Hz) hunting around setpoint → force-loop integrator gain too high or filter lag too large.
  - Works on foam, unstable on metal → environment stiffness entered the loop; reduce K_ctrl, add passive compliance (rubber pad at the tool — a $2 fix that buys orders of magnitude of stability margin and is standard practice, not a hack).

---

## 8. Production Failure Modes Checklist

These are the bugs that damage hardware. Check every one before first contact:

1. **No torque/force command saturation.** Always `clip(τ, ±τ_max)` AND rate-limit (`|Δτ| < τ_slew·dt`). A NaN or a pose-error spike (e.g., from a TF jump) otherwise commands max torque on all joints simultaneously.
2. **NaN propagation.** One NaN in q from a glitched encoder → NaN τ → drive fault or worse. Validate inputs: `if not np.isfinite(q).all(): trigger_safe_stop()`. Every cycle.
3. **Setpoint discontinuities.** New goal pose 30 cm away with K=2000 N/m = 600 N virtual force. Always interpolate x_des (trapezoidal or quintic, or a simple first-order filter with 0.5–2 s time constant for impedance targets).
4. **Wrong wrench sign or frame.** Verified empirically (§5) before closing any force loop. A sign error turns negative feedback into positive feedback: the robot *attacks* the surface.
5. **Gravity/payload model wrong after tool change.** Arm drifts in "gravity comp," phantom forces in F/T readings. Re-identify payload (mass + CoM) on every tool change; automate it.
6. **`sign(q̇)` friction compensation chatter.** At zero velocity, sign() flips at noise frequency → torque chatter → audible buzz, heat, instability. Use `tanh(q̇/v_eps)` with v_eps ≈ 0.01–0.05 rad/s, and compensate ≤ 80% of identified Coulomb friction (overcompensation is destabilizing — it's positive velocity feedback).
7. **Force-loop integrator windup on contact loss** (§4). Clamp and gate.
8. **Control-rate jitter on non-RT systems.** A 1 kHz impedance loop on a stock Linux kernel hiccups 5–20 ms under load; that's 5–20 lost cycles, and Franka-class interfaces hard-fault (`communication_constraints_violation`). Use PREEMPT_RT, pin the control thread (`SCHED_FIFO`, isolated core), pre-allocate everything, no logging/printing/allocation in the loop.
9. **Singularity in J^T mapping.** Near singularities, J^T maps finite Cartesian wrench to huge joint torques in some directions and nothing in others — impedance behavior degrades gracelessly. Monitor manipulability `√det(JJ^T)`; below threshold, damp Cartesian gains or use damped least-squares in any inverse you compute.
10. **Tare in contact.** Zeroing the F/T sensor while the tool touches something bakes the contact force into the bias; the controller then leans into the surface by exactly that force. Tare only in verified free space.
11. **Testing stiffness ramp.** First hardware bring-up of any impedance controller: start at 10% of target K, in free space, hand on the e-stop, ramp up over multiple runs. Then first contact against a *compliant* surface (foam block) before any rigid fixture.

---

## 9. Debugging Methodology

When a dynamics/force controller misbehaves, isolate layers bottom-up; never tune gains until the layers below are verified:

1. **Model layer:** does `rnea(q,0,0) == g(q)`? Does the arm hold still in pure gravity comp at 5+ diverse poses? Drift direction tells you which mass/CoM is wrong (drifts down = mass underestimated).
2. **Sensing layer:** plot compensated F/T while moving the *unloaded* arm slowly through orientations with no contact — should stay within ±1–2 N / ±0.2 N·m. If it swings with orientation: payload compensation wrong (§5.2).
3. **Free-space impedance:** push the EE by hand, release — it should return with one small overshoot (ζ≈0.7) or none (ζ=1). Oscillation in free space means D/K/velocity-filtering problems, *not* contact dynamics — fix here first.
4. **Compliant contact:** foam/spring target. Verify force ≈ K·δx as you command penetration.
5. **Real task.** Only now tune for the actual surface.

Log at full control rate during all of this: q, q̇, τ_cmd, τ_measured, F/T raw + compensated, x, x_des, and the residual r. Plot offline; oscillation frequency identifies the culprit (≥ structural resonance → mechanical; ≈ filter cutoff → filter lag; grows only in contact → environment-coupled).

**Tools:** Pinocchio + example-robot-data for models; MuJoCo or Drake for contact simulation (validate the controller in sim with a *stiff* contact model — soft sim contact hides instabilities that appear on real metal); `ros2_control` admittance_controller; `libfranka`/`franka_ros2` Cartesian impedance examples are a correct reference implementation worth reading line-by-line; PlotJuggler for control-rate log inspection.

---

## 10. Decision Guide

```
Need to regulate/limit force, or contact with uncertain geometry?
├─ No, just fast accurate motion
│   └─ Position control + feedforward: gravity comp first,
│      full inverse-dynamics feedforward if tracking at speed still poor
├─ Yes, robot is torque-controlled (Franka, iiwa, research arm)
│   └─ Cartesian impedance control (§4), anisotropic K per task table,
│      momentum-observer collision detection (§6) as the safety layer
├─ Yes, robot is position-only (UR, Fanuc, ABB, Kuka KR)
│   ├─ Has wrist F/T sensor → admittance control (§4),
│   │     beware stiff-environment chatter; add passive compliance
│   └─ No F/T sensor → add one for any real force task;
│         current-signature collision detection (§6 method 2) for crash protection only
└─ Need exact force on one axis (press 20 N) → hybrid: force PI on that axis,
      impedance/position on the rest, integrator clamped + contact-gated
```

The math here is decades old and settled. What separates working systems from broken ones is never the equations — it's payload compensation, frame conventions, setpoint smoothing, saturation, and respecting the stiffness-vs-loop-rate budget. Check the §8 list before the robot touches anything it can't afford to break.
