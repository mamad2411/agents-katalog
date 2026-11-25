---
name: sensor-fusion-kalman
description: "Use when fusing noisy sensors (IMU, GPS, wheel odometry, vision) into a state estimate, implementing or debugging a Kalman filter / EKF / UKF, tuning Q and R covariances, or configuring robot_localization in ROS2. Provides the math, worked examples, tuning methodology, and production failure modes."
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


# Sensor Fusion with Kalman Filters

State estimation is the foundation under everything else on the robot. If your pose estimate is wrong, your controller fights phantom errors, your planner plans from the wrong place, and your map smears. This skill covers the Kalman filter family from first principles to production deployment, with the tuning methodology that actually works on hardware.

## 0. Decision Guide — Which Filter?

| Situation | Filter | Why |
|---|---|---|
| Linear system, Gaussian noise (rare in robotics, common in subsystems: battery SoC, single-axis estimation) | KF | Optimal. No reason to use anything else. |
| Mildly nonlinear (differential drive / bicycle model odometry, GPS fusion, small heading uncertainty) | EKF | Industry default. 95% of mobile-robot fusion. |
| Strongly nonlinear or large heading/attitude uncertainty (>~30° std dev), bearing-only measurements, near-singularity geometry | UKF | No Jacobians, captures nonlinearity to 2nd order. ~2-3x compute of EKF. |
| Attitude-only from IMU, microcontroller, no spare cycles | Complementary filter / Mahony / Madgwick | Tuning is one parameter. Good enough for many platforms. |
| Multimodal posterior (global localization, kidnapped robot) | Particle filter | KF family is unimodal-Gaussian; it cannot represent "I'm in one of three corridors." |
| Smoothing over a trajectory window, loop closures | Factor graph (GTSAM, iSAM2) | Filters marginalize; smoothers re-linearize. Use for SLAM backends. |

If you are fusing IMU + wheel odometry + GPS on a ground robot: EKF (or `robot_localization` which implements one) is the right answer until proven otherwise.

## 1. The Kalman Filter — What It Actually Is

A KF maintains a Gaussian belief over state **x** with mean `x̂` and covariance `P`. Each cycle has two steps:

**Predict** (use the motion model, uncertainty grows):
```
x̂⁻ = F x̂ + B u
P⁻  = F P Fᵀ + Q
```

**Update** (use a measurement, uncertainty shrinks):
```
y = z − H x̂⁻              # innovation (residual)
S = H P⁻ Hᵀ + R            # innovation covariance
K = P⁻ Hᵀ S⁻¹              # Kalman gain
x̂ = x̂⁻ + K y
P  = (I − K H) P⁻
```

- `F`: state transition matrix. `B u`: control input. `H`: maps state → expected measurement.
- `Q`: process noise covariance — how much you distrust your motion model per step.
- `R`: measurement noise covariance — how much you distrust the sensor.
- The gain `K` is the optimal blend: K → 1 when R is small (trust sensor), K → 0 when P⁻ is small (trust prediction).

**Key intuition:** the KF is a recursive weighted average where the weights are inverse variances. Everything about tuning reduces to "are the relative sizes of Q, R, and P honest?"

### 1.1 Worked Example — 1D Constant-Velocity Tracking

State: position and velocity, `x = [p, v]ᵀ`. Sensor: position only (e.g., a range sensor at 10 Hz, σ = 0.5 m). dt = 0.1 s.

```
F = [1  dt]      H = [1  0]      R = [0.25]        # σ² = 0.5²
    [0   1]
```

Q from the discrete white-noise-acceleration model (the standard choice — derive Q from an assumed acceleration noise σ_a, NOT by hand-picking diagonal entries):

```
Q = σ_a² · [dt⁴/4   dt³/2]
            [dt³/2    dt² ]
```

With σ_a = 2 m/s² (a vehicle that can plausibly accelerate at ±2 m/s² between updates):
```
Q = 4 · [2.5e-5  5e-4]  = [1e-4   2e-3]
        [5e-4    1e-2]    [2e-3   4e-2]
```

One full cycle by hand. Initial: `x̂ = [0, 0]ᵀ`, `P = diag(1, 1)`. Measurement arrives: `z = 0.45`.

Predict:
```
x̂⁻ = [0 + 0·0.1, 0]ᵀ = [0, 0]ᵀ
P⁻  = [1+2·0.1+0.01   0.1] + Q = [1.2101  0.102 ]
      [0.1              1 ]      [0.102   1.04  ]
```
Update:
```
y = 0.45 − 0 = 0.45
S = 1.2101 + 0.25 = 1.4601
K = [1.2101/1.4601, 0.102/1.4601]ᵀ = [0.8288, 0.0699]ᵀ
x̂ = [0.373, 0.0314]ᵀ
P₀₀ = (1 − 0.8288)·1.2101 = 0.2072      # uncertainty collapsed from 1.21 to 0.21
```
Note the filter inferred a small **velocity** from a single **position** measurement — that's the off-diagonal P term at work. This is why you never zero out cross-covariances "to be safe": they carry the information.

Minimal correct implementation (NumPy):

```python
import numpy as np

class KalmanFilter1D:
    def __init__(self, dt, sigma_a, sigma_z):
        self.x = np.zeros(2)
        self.P = np.eye(2) * 1.0
        self.F = np.array([[1, dt], [0, 1]])
        self.H = np.array([[1.0, 0.0]])
        self.Q = sigma_a**2 * np.array([[dt**4/4, dt**3/2],
                                        [dt**3/2, dt**2 ]])
        self.R = np.array([[sigma_z**2]])

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z):
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + (K @ y).ravel()
        I_KH = np.eye(2) - K @ self.H
        # Joseph form: guaranteed symmetric PSD even with roundoff
        self.P = I_KH @ self.P @ I_KH.T + K @ self.R @ K.T
        return y, S   # return innovation for monitoring — always
```

**Always use the Joseph form** `P = (I−KH)P(I−KH)ᵀ + KRKᵀ` in production. The textbook `(I−KH)P` loses symmetry/positive-definiteness through floating-point error and the filter eventually diverges with `P` going indefinite. Also enforce `P = (P + Pᵀ)/2` after every update if running float32.

## 2. EKF — Nonlinear Systems (Bicycle Model Worked Example)

Real robot kinematics are nonlinear (heading θ enters through sin/cos). The EKF linearizes around the current estimate:

```
Predict:  x̂⁻ = f(x̂, u)            P⁻ = F P Fᵀ + Q,   F = ∂f/∂x |_(x̂,u)
Update:   y  = z − h(x̂⁻)           S = H P⁻ Hᵀ + R,   H = ∂h/∂x |_(x̂⁻)
```
Gain and covariance update identical to the linear KF. The **Jacobians are only used for covariance propagation** — the state always goes through the full nonlinear `f` and `h`. Putting the state through `F·x` instead of `f(x)` is a classic implementation bug.

### Kinematic bicycle model

State `x = [px, py, θ, v]ᵀ`, controls `u = [a, δ]` (acceleration, steering angle), wheelbase `L`:

```
px' = px + v·cos(θ)·dt
py' = py + v·sin(θ)·dt
θ'  = θ  + (v/L)·tan(δ)·dt
v'  = v  + a·dt
```

Jacobian F = ∂f/∂x:

```
F = [1  0  −v·sin(θ)·dt   cos(θ)·dt        ]
    [0  1   v·cos(θ)·dt   sin(θ)·dt        ]
    [0  0   1             tan(δ)·dt / L    ]
    [0  0   0             1                ]
```

GPS measures position: `h(x) = [px, py]ᵀ`, `H = [[1,0,0,0],[0,1,0,0]]`.
Wheel encoder measures speed: `h(x) = v`, `H = [0,0,0,1]`.
Magnetometer/dual-antenna GPS measures heading: `h(x) = θ` — **see angle wrapping below.**

```python
import numpy as np

def wrap(a):  # (-pi, pi]
    return (a + np.pi) % (2*np.pi) - np.pi

class BicycleEKF:
    def __init__(self, L=2.7):
        self.L = L
        self.x = np.zeros(4)                       # px, py, theta, v
        self.P = np.diag([10.0, 10.0, 0.5, 1.0])   # honest initial uncertainty
        # process noise: per-axis distrust of the model, scaled by dt in predict
        self.q = np.array([0.05, 0.05, 0.01, 0.5]) # m², m², rad², (m/s)² per second

    def predict(self, a, delta, dt):
        px, py, th, v = self.x
        self.x = np.array([
            px + v*np.cos(th)*dt,
            py + v*np.sin(th)*dt,
            wrap(th + v/self.L*np.tan(delta)*dt),
            v + a*dt])
        F = np.array([
            [1, 0, -v*np.sin(th)*dt, np.cos(th)*dt],
            [0, 1,  v*np.cos(th)*dt, np.sin(th)*dt],
            [0, 0,  1,               np.tan(delta)*dt/self.L],
            [0, 0,  0,               1]])
        Q = np.diag(self.q) * dt
        self.P = F @ self.P @ F.T + Q

    def update_gps(self, z_xy, sigma_gps=1.5, gate_chi2=9.21):  # 99% for 2 dof
        H = np.array([[1.,0,0,0],[0,1.,0,0]])
        R = np.eye(2) * sigma_gps**2
        y = z_xy - H @ self.x
        S = H @ self.P @ H.T + R
        nis = float(y @ np.linalg.solve(S, y))
        if nis > gate_chi2:
            return False, nis          # outlier: reject, log, DO NOT update
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.x[2] = wrap(self.x[2])
        I_KH = np.eye(4) - K @ H
        self.P = I_KH @ self.P @ I_KH.T + K @ R @ K.T
        return True, nis

    def update_heading(self, z_th, sigma_th=0.05):
        H = np.array([[0., 0, 1, 0]])
        R = np.array([[sigma_th**2]])
        y = np.array([wrap(z_th - self.x[2])])     # WRAP THE INNOVATION
        S = H @ self.P @ H.T + R
        K = self.P @ H.T / S
        self.x = self.x + (K * y).ravel()
        self.x[2] = wrap(self.x[2])
        I_KH = np.eye(4) - K @ H
        self.P = I_KH @ self.P @ I_KH.T + K @ R @ K.T
```

### Angle wrapping — the #1 EKF bug on real robots

If heading is 179° and the magnetometer reads −179°, the raw innovation is −358° instead of +2°. The filter slams the heading estimate through a full rotation, position integration goes wild, and the robot drives in a circle. **Every subtraction involving an angle — innovation, state correction, error computation — must be wrapped to (−π, π].** For 3D attitude, don't use Euler states at all: use an error-state EKF with quaternion nominal state and 3-vector attitude error (this is what every production VIO/INS does — see §7).

## 3. Designing the State, Process Noise, and Measurement Models

### State vector design rules

1. **Include every quantity a sensor measures or a model needs, nothing more.** Each extra state must be observable from some sensor combination, or its covariance grows without bound.
2. **Include sensor biases if they matter and are observable.** Gyro bias is observable when you have an absolute heading/attitude reference (magnetometer, GPS course, accelerometer gravity vector). Accelerometer bias needs position/velocity aiding. A bias state you can't observe is worse than no bias state.
3. **Observability sanity check:** build O = [H; HF; HF²; …] and check rank, or simpler: simulate with zero process noise and see which state covariances never shrink. Classic trap: with GPS position only and no motion, heading is unobservable for a ground robot — heading becomes observable only while moving (velocity direction couples to heading). Expect heading variance to balloon when stationary; this is correct behavior, don't "fix" it by shrinking Q.

### Process noise Q

- Derive Q from physical reasoning, not vibes: "the model ignores accelerations up to σ_a" → use the white-noise-acceleration Q from §1.1. For the bicycle model: how much can slip/calibration error corrupt each state per second?
- **Q scales with dt.** If you tune Q at 50 Hz then change to 100 Hz, multiply per-step Q by dt (continuous-time Q in units/second, multiply by dt at predict time — as in the code above).
- Q too small → filter overconfident → ignores measurements → diverges smoothly and confidently (the worst failure mode, because P says everything is fine).
- Q too large → noisy, laggy estimate that mirrors the raw sensors. Annoying but visible.
- When in doubt, err large. An honest-but-pessimistic filter is recoverable; an overconfident filter is not.

### Measurement noise R

- Start from the datasheet (e.g., GPS HDOP × UERE, encoder quantization, IMU noise density) then **validate against logged data**: record sensor readings against ground truth (or a stationary robot), compute the empirical variance. Datasheets are best-case.
- R is per-sensor-reading, independent of rate. But beware: many sensors output **pre-filtered** data (GPS receivers, smoothed IMU drivers). Filtered measurements have time-correlated noise, which violates the KF whiteness assumption — the filter double-counts information and becomes overconfident. Mitigations: inflate R 2–5x, or downsample updates to below the sensor's internal filter bandwidth.
- If a sensor reports per-measurement covariance (GPS accuracy estimate, visual odometry), use it — but clamp it to a floor; receivers lie about their accuracy in multipath.

## 4. Tuning Q and R in Practice — Innovation Monitoring

This is the part most teams skip and then pay for. The innovation sequence `y_k` with covariance `S_k` is the filter's self-diagnostic. **A correctly tuned filter has innovations that are zero-mean, white, with empirical covariance matching S.**

### The NIS test (Normalized Innovation Squared)

```
NIS_k = y_kᵀ S_k⁻¹ y_k     ~  χ²(m)   where m = measurement dimension
```

Over a log of N updates, the average NIS should be ≈ m. Concretely, for a 2D GPS update (m=2): mean NIS ≈ 2; about 95% of individual NIS values should fall below 5.99 (χ²₂ 95th percentile).

```python
# offline tuning loop on a logged dataset
nis_values = []
for z in gps_log:
    accepted, nis = ekf.update_gps(z)
    nis_values.append(nis)
mean_nis = np.mean(nis_values)   # target: ~2.0 for 2-dof measurement
```

**Interpretation and the tuning procedure:**

| Symptom | Meaning | Fix |
|---|---|---|
| mean NIS ≫ m (e.g., 8 for m=2) | Filter overconfident: S too small relative to real errors | Increase Q (if errors grow between updates) or increase R (if errors are present even at high rate) |
| mean NIS ≪ m (e.g., 0.3) | Filter underconfident: wasting information, laggy | Decrease Q first, then R |
| NIS OK on average but innovations are correlated in time (autocorrelation ≠ δ) | Unmodeled dynamics or filtered sensor data | Add the missing state (e.g., bias), or inflate R / downsample |
| NIS spikes only during specific maneuvers (hard turns, braking) | Model mismatch under those dynamics | Increase the relevant Q term, or upgrade model (e.g., add slip) |
| Innovation mean ≠ 0 on one axis | Sensor bias or extrinsic calibration error (lever arm, mounting angle) | Calibrate; do not absorb a bias into R |

**Procedure:**
1. Fix R from datasheet + stationary logs (this is the more measurable of the two).
2. Sweep Q (log scale: 0.1x, 1x, 10x your physical estimate) on a recorded dataset; pick the Q where mean NIS ≈ m per sensor.
3. Check innovation whiteness (autocorrelation of y over the log). If correlated, you have a modeling problem no amount of Q/R scaling fixes.
4. If you have ground truth (mocap, RTK), also run NEES: `(x−x̂)ᵀP⁻¹(x−x̂)` should average ≈ n (state dim). NEES validates P itself, not just S.
5. Re-verify on a *different* dataset than you tuned on.

### Innovation gating (outlier rejection)

Reject any measurement with NIS above the χ² 99% threshold for its dimension (m=1: 6.63, m=2: 9.21, m=3: 11.34) — as in the `update_gps` code above. This is what saves you from GPS multipath jumps and encoder glitches. **Two warnings:**
- Log every rejection. >1–2% rejection rate means your tuning is off or a sensor is failing — gating is masking it.
- Gating can deadlock: if the filter diverges, *all* measurements look like outliers and it never recovers. Add a recovery rule: after K consecutive rejections of an absolute sensor (GPS), force-accept with inflated R or reinitialize the relevant states.

## 5. Complementary Filter — the Poor Man's KF

For attitude from IMU only, a complementary filter does 90% of the job in 5 lines. It blends the gyro (good at high frequency, drifts) with the accelerometer (noisy at high frequency, unbiased gravity reference at low frequency):

```python
# pitch from gyro integration (HF) + accelerometer gravity (LF)
alpha = tau / (tau + dt)          # tau = crossover time constant, e.g. 0.5 s
pitch_acc = np.arctan2(-ax, np.sqrt(ay**2 + az**2))
pitch = alpha * (pitch + gyro_y * dt) + (1 - alpha) * pitch_acc
```

- `tau` is the single tuning knob: it is the timescale below which you trust the gyro and above which you trust the accelerometer. Start at 0.5–1.0 s. Vibration-heavy platform (drone) → larger tau. Slow platform → smaller.
- This *is* a steady-state Kalman filter with fixed gain — the KF derives `alpha` optimally and time-varyingly; the complementary filter hardcodes it.
- **Limits:** no covariance output (downstream consumers can't weight it), no bias estimation (use Mahony, which adds an integral term ≈ gyro bias state, or Madgwick), accelerometer reference corrupted by sustained linear acceleration (turning vehicle reads centripetal acceleration as tilt — gate the accel correction when `| ||a|| − g | > threshold`).
- Use it when: attitude-only, microcontroller, or as a bring-up baseline before the EKF. Don't use it as the robot's pose estimator.

## 6. UKF — When EKF Linearization Fails

The EKF approximates the nonlinear transform of a Gaussian by linearizing at a single point. This fails when the function curves significantly within the ±1σ region: large heading uncertainty, polar→Cartesian conversion of long-range bearing measurements, attitude far from reference.

The UKF instead pushes 2n+1 deterministically chosen **sigma points** through the full nonlinear function and refits a Gaussian:

```
χ₀ = x̂;   χᵢ = x̂ ± (√((n+λ)P))ᵢ      # matrix square root via Cholesky
predict:  χᵢ ← f(χᵢ);  x̂⁻ = Σ Wᵢᵐ χᵢ;  P⁻ = Σ Wᵢᶜ (χᵢ−x̂⁻)(χᵢ−x̂⁻)ᵀ + Q
update:   Zᵢ = h(χᵢ);   ẑ = Σ Wᵢᵐ Zᵢ
          S = Σ Wᵢᶜ (Zᵢ−ẑ)(Zᵢ−ẑ)ᵀ + R
          C = Σ Wᵢᶜ (χᵢ−x̂⁻)(Zᵢ−ẑ)ᵀ
          K = C S⁻¹;  x̂ = x̂⁻ + K(z−ẑ);  P = P⁻ − K S Kᵀ
```

Standard parameters: `α = 1e-3` (spread; raise to 0.1–1 for strongly nonlinear f), `β = 2` (optimal for Gaussian priors), `κ = 0`, `λ = α²(n+κ) − n`. Weights: `W₀ᵐ = λ/(n+λ)`, `W₀ᶜ = W₀ᵐ + (1−α²+β)`, `Wᵢ = 1/(2(n+λ))`.

**Practical notes:**
- No Jacobians — for complex measurement models (camera projection chains, multi-link kinematics) this alone justifies UKF: hand-derived Jacobians are the second-biggest bug source after angle wrapping.
- Cholesky of P fails if P loses positive-definiteness → the UKF crashes where an EKF would limp along. Symmetrize P every step, add jitter `P += 1e-9·I` if `cholesky` throws, or use the square-root UKF (propagates the Cholesky factor directly — do this on embedded/float32).
- Sigma-point mean of angles is wrong if computed arithmetically (mean of 179° and −179° is 0°, not 180°). Use the error-state formulation or mean-of-unit-vectors for angular states.
- Rule of thumb: prototype with EKF; if NIS shows maneuver-dependent inconsistency you can't tune away and the model is genuinely nonlinear over your P, switch to UKF before adding hacks. Use `filterpy` (Python) for prototyping; write your own or use a vetted C++ implementation for production.

## 7. IMU + GPS + Odometry Fusion Architecture

The standard mobile-robot architecture, and the one `robot_localization` implements:

```
                 ┌──────────────────────────────────────────────┐
 IMU 100-400Hz ─►│ predict (or high-rate update of θ̇, a)        │
 wheel odom 50Hz►│ update: vx, vy(=0 constraint), ω̇            │  EKF #1 (LOCAL)
                 │ output: odom → base_link    smooth, drifts   │
                 └──────────────────────────────────────────────┘
 IMU + odom    ─►┌──────────────────────────────────────────────┐
 GPS 1-10Hz    ─►│ same + absolute position updates             │  EKF #2 (GLOBAL)
 (via navsat)    │ output: map → odom (the drift correction)    │
                 └──────────────────────────────────────────────┘
```

Design rules:

1. **Two-filter pattern.** The local filter is continuous and smooth — feed it to the controller (controllers hate the discrete jumps GPS corrections cause). The global filter is accurate but jumpy — feed it to the planner. The difference between them is published as the `map→odom` transform (ROS REP-105).
2. **IMU as prediction input, not measurement** (in a full INS formulation): integrate gyro+accel in `f()`, and let GPS/odometry updates correct the integration. Alternatively (robot_localization style) treat IMU angular velocity and acceleration as measurements into a kinematic model. The INS formulation is better at high dynamics; the kinematic one is simpler and fine for ground robots.
3. **Error-state (indirect) EKF for anything with 3D attitude.** Nominal state holds the quaternion, integrated directly; the filter estimates a 15-dim error state (δp, δv, δθ, δb_gyro, δb_accel). This avoids quaternion normalization hacks and keeps attitude error small where linearization is valid. Every serious INS (and packages like `imu_filter_madgwick` aside, estimators like MSF, OpenVINS) does this.
4. **Differential-drive nonholonomic constraint is a sensor.** Pseudo-measurement `v_y = 0` (body frame) with small R (σ ≈ 0.05–0.1 m/s). Free observability, dramatically reduces lateral drift. Don't set R=0 — wheels do slip sideways.
5. **Time alignment is not optional.** GPS arrives 50–200 ms late; cameras later. Options in order of correctness: (a) buffer states, rewind to measurement timestamp, apply update, replay predictions forward (robot_localization does a version of this with `smooth_lagged_data`); (b) propagate the measurement forward with the motion model; (c) inflate R for the latency-induced error `v·Δt_latency`. Hardware-timestamp at the sensor when possible; driver-receipt timestamps carry OS jitter.
6. **GPS → local frame conversion**: convert lat/lon to a local Cartesian frame (ENU via a fixed datum, or UTM). Watch UTM zone boundaries on long missions. Account for the antenna **lever arm**: GPS measures the antenna position, not base_link — `z_expected = p + R(θ)·r_antenna`. Unmodeled 0.5 m lever arm = permanent 0.5 m oscillating bias that no Q/R tuning fixes.
7. **Sequential updates are fine.** Process each sensor's measurement with its own H and R as it arrives, in timestamp order. No need to stack into one big z. This also lets you gate each sensor independently.

## 8. robot_localization (ROS2) — Configuration That Works

`robot_localization` provides `ekf_node` and `ukf_node` (15-state: x y z, roll pitch yaw, ẋ ẏ ż, roll̇ pitcḣ yaẇ, ẍ ÿ z̈) plus `navsat_transform_node` for GPS.

Two-node setup for an outdoor differential-drive robot:

```yaml
# ekf_local.yaml — feeds the controller
ekf_local:
  ros__parameters:
    frequency: 30.0
    two_d_mode: true                  # planar robot: forces z, roll, pitch to 0
    publish_tf: true
    map_frame: map
    odom_frame: odom
    base_link_frame: base_link
    world_frame: odom                 # LOCAL filter → world_frame = odom

    odom0: /wheel/odometry
    # fuse VELOCITIES from wheel odom, not positions (see rule below)
    #             x      y      z      r      p      yaw    vx     vy     vz     vr     vp     vyaw   ax     ay     az
    odom0_config: [false, false, false, false, false, false, true,  true,  false, false, false, true,  false, false, false]
    odom0_differential: false

    imu0: /imu/data
    imu0_config:  [false, false, false, false, false, false, false, false, false, false, false, true,  true,  false, false]
    imu0_differential: false
    imu0_remove_gravitational_acceleration: true

    process_noise_covariance: [...]   # 15x15; start from package defaults,
                                      # tune diagonal via NIS methodology (§4)

# ekf_global.yaml — feeds the planner
ekf_global:
  ros__parameters:
    frequency: 30.0
    two_d_mode: true
    publish_tf: true
    world_frame: map                  # GLOBAL filter → world_frame = map
    map_frame: map
    odom_frame: odom
    base_link_frame: base_link
    odom0: /wheel/odometry
    odom0_config: [false, false, false, false, false, false, true, true, false, false, false, true, false, false, false]
    imu0: /imu/data
    imu0_config:  [false, false, false, false, false, false, false, false, false, false, false, true, true, false, false]
    odom1: /odometry/gps              # from navsat_transform_node
    odom1_config: [true,  true,  false, false, false, false, false, false, false, false, false, false, false, false, false]

navsat_transform:
  ros__parameters:
    frequency: 10.0
    delay: 3.0
    magnetic_declination_radians: 0.0   # SET THIS for your location (NOAA calculator)
    yaw_offset: 0.0                     # 0 if IMU reads 0 facing EAST (ENU/REP-103)
    zero_altitude: true
    broadcast_cartesian_transform: false
    use_odometry_yaw: false
    wait_for_datum: false
```

**Configuration rules that prevent the classic failures:**

- **Never fuse the same physical quantity as absolute from two sources** unless both are genuinely absolute in the same frame. Two absolute yaw sources that disagree (magnetometer vs. visual odom) make the estimate snap back and forth. Fuse one absolute + others as velocity/differential.
- **Fuse wheel odometry as velocity** (`vx, vy, vyaw`), not pose. Wheel odom pose drifts unboundedly; its pose covariance (usually constant in the message) becomes a lie within a minute, and the filter will fight GPS with it.
- **`two_d_mode: true` for any planar robot.** Otherwise unmeasured z/roll/pitch covariance explodes and numerically poisons the rest of P.
- The IMU message must follow REP-103/REP-145: ENU, yaw=0 facing east. NED IMUs (many flight controllers) need conversion (`imu_transformer` or driver config). Symptom of getting this wrong: robot's estimated heading rotates opposite to reality, or navsat output orbits the true position.
- Every fused message **must have a sane covariance**. A covariance of all zeros is interpreted as "perfect measurement" (some drivers ship this!) and will lock the filter. Inspect with `ros2 topic echo --field pose.covariance`.
- Check the diagnostics: `ros2 topic echo /diagnostics` — robot_localization reports timing jumps, missing covariances, and frame errors there, and almost nobody reads it.
- Tune `process_noise_covariance` with the §4 NIS method using recorded bags. The defaults are deliberately loose; they work but are laggy.

## 9. Production Failure Modes — the List That Kills Robots

1. **Angle wrapping** (§2). Symptom: estimate explodes exactly when heading crosses ±180°.
2. **Covariance loses positive-definiteness.** Symptom: NaNs after hours of runtime, or Cholesky failure in UKF. Fix: Joseph form, symmetrization, float64 for P, jitter on decomposition failure.
3. **Overconfident filter (Q too small / zero-covariance messages).** Symptom: estimate smoothly diverges from ground truth while P stays tiny; all measurements eventually gated out. This is the failure that looks like success until the robot hits a wall.
4. **Timestamp abuse**: fusing measurements at receipt time, clocks unsynced between sensor computers (run chrony/PTP), bag replay without `use_sim_time`. Symptom: estimate lags or leads reality by a fixed offset; innovations correlate with velocity.
5. **Unmodeled lever arms / mounting extrinsics** (§7.6). Symptom: position bias that rotates with heading; oscillation while turning in place.
6. **Double-counting correlated information**: feeding a fused output back in as a measurement (e.g., fusing an odometry topic that itself already contains the IMU), or fusing pre-filtered sensor data with datasheet R. Symptom: overconfidence, NIS ≫ m.
7. **GPS multipath / urban canyon**: receiver reports 1 m accuracy while being 15 m wrong. Innovation gating catches the jumps; the slow drifts it doesn't — mitigate with RTK, or by gating on satellite count/HDOP and inflating R near structures.
8. **Stationary heading drift on differential drive** (heading unobservable at standstill, §3). Symptom: robot sits still for 10 min, then drives off at an angle on first motion. Mitigations: zero-velocity updates (ZUPT: when wheels report 0, update v=0, ω=0 with tight R), gyro bias state.
9. **Initialization**: starting with P too small at a wrong x̂ → filter rejects all corrective measurements (gating deadlock §4). Initialize P generously (position σ ≥ first-GPS accuracy, heading σ ≥ 30° unless you truly know it) and consider delaying convergence claims until trace(P) drops below a threshold.
10. **dt bugs**: variable loop timing with hardcoded dt, dt=0 on duplicate timestamps (divide-by-zero in differential updates), dt spikes during CPU contention. Always compute dt from timestamps, clamp to [ε, dt_max], and skip predict on dt ≤ 0.

### Debugging methodology (in order)

1. **Reproduce on a bag/log.** Never tune live first.
2. **Plot raw sensors against each other** in a common frame before blaming the filter — half of "filter bugs" are frame conventions, units (deg vs rad!), or a bad sensor.
3. **Plot innovations per sensor** with ±3σ bounds from S. The sensor whose innovations are biased/inconsistent is your problem.
4. **Run NIS per sensor** (§4); compare to χ² expectations.
5. **Disable sensors one at a time.** The estimate getting *better* when a sensor is removed pinpoints it.
6. **Check P evolution**: any diagonal element growing without bound = unobservable state; any hitting ~0 = something claiming perfection.
7. Only after all of the above, touch Q.

## 10. Tooling

- **filterpy** (Python): KF/EKF/UKF reference implementations — prototyping and offline tuning. Companion book: Labbe, *Kalman and Bayesian Filters in Python* (free, the best practical text).
- **robot_localization** (ROS2): production EKF/UKF for mobile robots, as configured above.
- **fuse** (ROS2, Locus Robotics): factor-graph-based estimator, successor in spirit to robot_localization when you need nonlinear constraints/smoothing.
- **GTSAM / iSAM2**: factor-graph smoothing — SLAM backends, batch calibration, anything with loop closures.
- **OpenVINS / VINS-Fusion**: visual-inertial odometry with proper error-state filtering/optimization — study OpenVINS's error-state EKF even if you don't use it.
- **Eigen** (C++): the linear algebra layer for hand-rolled production filters; use `LDLT` solves instead of explicit inverses for S⁻¹.
- Ground truth for validation: motion capture indoors, RTK-GPS (u-blox F9P class) outdoors. Without ground truth you can validate consistency (NIS) but not accuracy (NEES).
