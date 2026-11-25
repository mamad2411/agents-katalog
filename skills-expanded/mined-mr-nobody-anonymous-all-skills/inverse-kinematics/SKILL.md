---
name: inverse-kinematics
description: "Use when solving robot arm inverse kinematics — choosing between geometric/analytical and numerical solvers, handling singularities, joint limits, redundancy, or selecting between IKFast, KDL, and trac-ik. Provides DH parameter methodology, Jacobian-based IK math with damped least squares, workspace analysis, and production-grade failure-mode handling."
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


# Inverse Kinematics for Robot Arms

Inverse kinematics (IK) answers: *given a desired end-effector pose, what joint angles achieve it?*
This is the single most failure-prone piece of math in a manipulator stack. An IK bug doesn't
throw an exception — it commands the arm to swing through a singularity at joint-velocity limits
and breaks the tooling. This skill covers IK that is **correct on real hardware the first time**.

## Mental Model: FK Is a Function, IK Is Not

Forward kinematics (FK) is a clean function: `T = f(q)` where `q ∈ R^n` (joint angles) and
`T ∈ SE(3)` (end-effector pose). It always has exactly one answer.

Inverse kinematics `q = f⁻¹(T)` is NOT a function:

- **Multiple solutions**: a 6-DOF arm typically has up to **8 discrete solutions** for one pose
  (elbow up/down × shoulder left/right × wrist flip).
- **No solution**: pose outside the workspace, or inside but unreachable due to joint limits.
- **Infinite solutions**: redundant arms (7+ DOF) have a continuum (the "self-motion manifold").
- **Ill-conditioned solutions**: near singularities, tiny Cartesian changes need huge joint motions.

Every production IK system must handle all four cases explicitly. The #1 IK bug in deployed code
is treating IK as a function and silently taking "whatever the solver returns."

---

## 1. DH Parameters: The Kinematic Description

Denavit–Hartenberg (DH) parameters describe a serial chain with 4 numbers per joint. Each link's
frame is related to the previous by:

```
T_i = Rot_z(θᵢ) · Trans_z(dᵢ) · Trans_x(aᵢ) · Rot_x(αᵢ)
```

| Parameter | Meaning | Constant or variable? |
|-----------|---------|----------------------|
| `θᵢ` (theta) | Rotation about previous z-axis | **Variable** for revolute joints (θᵢ = qᵢ + offset) |
| `dᵢ` | Translation along previous z-axis | Variable for prismatic joints, else constant |
| `aᵢ` | Link length: translation along new x-axis | Constant (from CAD) |
| `αᵢ` (alpha) | Link twist: rotation about new x-axis | Constant — almost always 0, ±90°, or 180° |

**The convention trap**: There are TWO DH conventions — **standard (distal)** and
**modified (proximal, Craig)**. They produce different tables for the same robot.
Mixing them is the most common cause of "FK is off by one link." UR robots publish standard DH;
many textbooks (Craig) and some URDF exporters use modified. Always verify by computing FK at
the zero pose and comparing against the manufacturer's published zero-pose TCP position before
trusting any table.

### Worked example: planar 3-DOF arm (3R)

Three revolute joints, all z-axes parallel (out of the plane), link lengths L1, L2, L3.

Standard DH table:

| i | θᵢ | dᵢ | aᵢ | αᵢ |
|---|------|----|------|----|
| 1 | q₁ | 0 | L1 | 0 |
| 2 | q₂ | 0 | L2 | 0 |
| 3 | q₃ | 0 | L3 | 0 |

FK reduces to:

```
x = L1·cos(q₁) + L2·cos(q₁+q₂) + L3·cos(q₁+q₂+q₃)
y = L1·sin(q₁) + L2·sin(q₁+q₂) + L3·sin(q₁+q₂+q₃)
φ = q₁ + q₂ + q₃          (end-effector orientation in the plane)
```

3 DOF, 3 task variables (x, y, φ) → generically a finite number of solutions (2: elbow up/down).

### Geometric IK for the 3R arm (the pattern for all analytical IK)

Given target (x, y, φ), peel off the last link first — this is the **wrist decoupling** trick:

```
# Step 1: wrist center = where joint 3 must be
wx = x - L3·cos(φ)
wy = y - L3·sin(φ)

# Step 2: solve the 2R subproblem for (wx, wy) — law of cosines
r² = wx² + wy²
cos(q₂) = (r² - L1² - L2²) / (2·L1·L2)

# REACHABILITY CHECK — do this BEFORE acos, not after it returns NaN
if cos(q₂) > 1 or cos(q₂) < -1:  unreachable → return failure explicitly

q₂ = ± acos(cos_q2)               # + = elbow down, − = elbow up: TWO solutions
q₁ = atan2(wy, wx) - atan2(L2·sin(q₂), L1 + L2·cos(q₂))
q₃ = φ - q₁ - q₂
```

Rules that generalize to 6-DOF geometric IK:

1. **Always use `atan2(y, x)`, never `atan(y/x)`** — `atan` loses the quadrant and divides by zero.
2. **Clamp acos/asin arguments**: floating point gives `cos(q₂) = 1.0000000002` at full extension.
   Clamp to [-1, 1] only when within ~1e-9 of the boundary; otherwise it's a genuine reach failure.
3. **Enumerate ALL branches** and return them all. Branch selection is the caller's job
   (pick closest to current q, or the one satisfying limits).
4. **Wrist decoupling**: any 6-DOF arm with a spherical wrist (axes 4,5,6 intersect at a point —
   true for most industrial arms: FANUC, KUKA KR, ABB IRB) splits into: position IK for joints 1–3
   to place the wrist center, then orientation IK for joints 4–6 (Euler-angle extraction from
   R₃₆ = R₀₃ᵀ · R₀₆). This gives the closed-form 8-solution set.

**Arms WITHOUT a spherical wrist** (UR series — consecutive offset axes; many cobots) still have
analytical solutions but via different decompositions (UR has a well-known closed form with 8
solutions). 7-DOF arms (KUKA iiwa, Franka Panda) need an extra parameter — see §6 Redundancy.

---

## 2. The Jacobian: The Core Object of Numerical IK

The geometric Jacobian `J(q) ∈ R^{6×n}` maps joint velocities to end-effector twist:

```
[v; ω] = J(q) · q̇       (v = linear velocity, ω = angular velocity, both in base frame)
```

For a revolute joint i with axis `ẑᵢ` and origin `pᵢ` (base frame, from FK):

```
J_column_i = [ ẑᵢ × (p_ee − pᵢ) ]    ← linear part (3×1)
             [ ẑᵢ              ]    ← angular part (3×1)
```

For a prismatic joint: linear part = `ẑᵢ`, angular part = 0.

```python
import numpy as np

def geometric_jacobian(joint_axes_world, joint_origins_world, p_ee):
    """joint_axes_world: list of unit z-axes in base frame (from FK chain).
    joint_origins_world: list of joint origins in base frame.
    p_ee: end-effector position in base frame.
    Returns 6xN Jacobian [linear; angular]."""
    n = len(joint_axes_world)
    J = np.zeros((6, n))
    for i in range(n):
        z = joint_axes_world[i]
        J[0:3, i] = np.cross(z, p_ee - joint_origins_world[i])
        J[3:6, i] = z
    return J
```

**Units trap**: the linear rows are in meters, angular rows in radians. They're not comparable —
1 rad of orientation error is NOT "the same size" as 1 m of position error. Numerical IK that
stacks them naively implicitly weights orientation ≈ position-error-at-1-meter-lever-arm. For a
0.8 m-reach arm this is roughly fine; for a 0.1 m micro-manipulator it badly over-weights
orientation. Use an explicit task weight matrix (see DLS code below).

---

## 3. Numerical IK: Jacobian Methods

Iterate: compute pose error, map it through an inverse of J, step the joints.

### Pose error (do this correctly or nothing converges)

```python
def pose_error(T_target, T_current):
    """Returns 6-vector [position_error; orientation_error] in base frame."""
    e = np.zeros(6)
    e[0:3] = T_target[0:3, 3] - T_current[0:3, 3]
    # Orientation error: rotation that takes current to target, as a rotation vector
    R_err = T_target[0:3, 0:3] @ T_current[0:3, 0:3].T
    # Log map of SO(3): axis * angle
    angle = np.arccos(np.clip((np.trace(R_err) - 1) / 2, -1.0, 1.0))
    if angle < 1e-10:
        e[3:6] = 0.0
    elif angle > np.pi - 1e-6:
        # Near pi: axis extraction from off-diagonals is degenerate; use diagonal form
        axis = np.sqrt(np.maximum(np.diag(R_err) - np.cos(angle), 0) / (1 - np.cos(angle)))
        # Fix signs using off-diagonal elements
        axis = axis * np.sign([R_err[2,1]-R_err[1,2], R_err[0,2]-R_err[2,0], R_err[1,0]-R_err[0,1]])
        e[3:6] = axis / np.linalg.norm(axis) * angle
    else:
        e[3:6] = angle / (2 * np.sin(angle)) * np.array([
            R_err[2,1] - R_err[1,2],
            R_err[0,2] - R_err[2,0],
            R_err[1,0] - R_err[0,1]])
    return e
```

**Never** compute orientation error by subtracting Euler angles or quaternion components.
Euler subtraction is wrong near gimbal lock; quaternion subtraction is wrong because q and −q
are the same rotation (causes the classic "arm takes the 350° long way around" bug —
always enforce `dot(q_target, q_current) ≥ 0` before any quaternion interpolation/difference).

### Method comparison

| Method | Update | Behavior at singularity |
|--------|--------|------------------------|
| Jacobian transpose | `Δq = α·Jᵀe` | Safe but slow; converges poorly anisotropically |
| Pseudoinverse | `Δq = J⁺e` | **Blows up** — `J⁺ = Jᵀ(JJᵀ)⁻¹`, `JJᵀ` singular → Δq → ∞ |
| **Damped least squares (DLS)** | `Δq = Jᵀ(JJᵀ + λ²I)⁻¹e` | Bounded — trades accuracy for stability near singularity |

**Use DLS. Always.** Plain pseudoinverse near a singularity commands joint steps of hundreds of
rad — on a real arm that's an emergency-stop event or worse. DLS minimizes
`‖JΔq − e‖² + λ²‖Δq‖²`: λ caps the step size in degenerate directions.

### Production DLS implementation

```python
def ik_dls(fk_func, jac_func, T_target, q0, joint_limits,
           pos_tol=1e-4, rot_tol=1e-3, max_iters=200,
           lam_min=1e-3, max_step=0.2):
    """Damped least squares IK with adaptive damping and joint limits.
    pos_tol in meters (0.1 mm), rot_tol in radians (~0.06 deg).
    max_step in radians per iteration (caps joint motion — CRITICAL for safety
    if this loop ever runs online)."""
    q = q0.copy()
    W = np.diag([1, 1, 1, 0.5, 0.5, 0.5])  # task weights: down-weight orientation slightly
    for it in range(max_iters):
        T_cur = fk_func(q)
        e = pose_error(T_target, T_cur)
        if np.linalg.norm(e[0:3]) < pos_tol and np.linalg.norm(e[3:6]) < rot_tol:
            return q, True, it
        J = jac_func(q)
        # Adaptive damping from manipulability (Nakamura): more damping near singularity
        _, s, _ = np.linalg.svd(J, full_matrices=False)
        sigma_min = s[-1]
        eps = 0.05  # singularity neighborhood threshold on sigma_min
        if sigma_min < eps:
            lam = lam_min + (1 - (sigma_min / eps) ** 2) * 0.1
        else:
            lam = lam_min
        Jw = W @ J
        ew = W @ e
        dq = Jw.T @ np.linalg.solve(Jw @ Jw.T + lam**2 * np.eye(6), ew)
        # Step limiting — never let one iteration command a large joint jump
        step = np.linalg.norm(dq)
        if step > max_step:
            dq *= max_step / step
        q = q + dq
        # Joint limit handling: clamp, and zero the gradient component into the limit
        q = np.clip(q, joint_limits[:, 0], joint_limits[:, 1])
    return q, False, max_iters
```

**Starting parameter values (these matter):**

| Parameter | Start value | Notes |
|-----------|-------------|-------|
| `lam_min` | 1e-3 | Baseline damping far from singularities |
| `lam_max` (near singularity) | 0.1 | Scaled by manipulability as above |
| `eps` (σ_min threshold) | 0.05 | For a ~1 m arm; scale with arm reach |
| `max_step` | 0.2 rad | ~11° per iteration; lower (0.05) for online control |
| `pos_tol` | 1e-4 m | 0.1 mm — typical industrial repeatability scale |
| `rot_tol` | 1e-3 rad | ~0.06° |
| `max_iters` | 200 offline / 3–10 online | Online IK runs 1–3 iterations per control cycle |
| Restarts | 10–50 random seeds | If q0 fails — numerical IK is local; restarts find other basins |

**Convergence failure ≠ unreachable.** Numerical IK converges to the basin of q0. If it fails,
restart from random configurations within joint limits before declaring the pose unreachable.
trac-ik does exactly this internally.

### Joint limits, properly

Clamping (as above) works but can deadlock: the solver pushes into the limit every iteration and
makes no progress. Better options, in increasing sophistication:

1. **Clamp + detect stall**: if `‖dq_effective‖ < 1e-6` for 5 iterations while error is large,
   restart from a new seed.
2. **Gradient projection** (for redundant arms): add a null-space term pulling toward mid-range —
   see §6.
3. **QP-based IK**: solve `min ‖JΔq − e‖² s.t. q_min ≤ q+Δq ≤ q_max` with a QP solver (OSQP,
   qpOASES). This is what modern whole-body controllers do and is the correct answer when limits
   are active often. ~50–200 µs per solve for 7 DOF — fine for 1 kHz control.

---

## 4. Singularities: Types, Detection, Avoidance

A singularity is a configuration where J loses rank: the arm loses the ability to move
instantaneously in ≥1 Cartesian direction, and IK velocity solutions blow up approaching it.

### The three types on a 6-DOF industrial arm

1. **Wrist singularity** (most common in practice): joint-5 = 0 → axes 4 and 6 align.
   Near it, small tool reorientations command joints 4 and 6 to counter-rotate at enormous speed.
   This is the one that bites during smooth Cartesian paths through a "straight wrist" pose.
2. **Shoulder/alignment singularity**: wrist center passes directly over the joint-1 axis.
   Joint 1 becomes indeterminate; arm whips around the base.
3. **Elbow/boundary singularity**: arm fully extended (or fully folded) — `cos(q₂) = ±1` in the
   3R example. At the workspace boundary; the arm cannot move radially outward.

### Detection metrics

- **Manipulability** (Yoshikawa): `w = √det(JJᵀ)` — goes to 0 at singularity. Cheap, but scale-
  dependent and conflates all directions.
- **Minimum singular value** `σ_min(J)`: the best single metric. Tells you the worst-direction
  velocity gain. Threshold: treat `σ_min < 0.05·σ_max_nominal` as "in the singular region."
- **Condition number** `σ_max/σ_min`: scale-free; > ~100 means trouble.

### Avoidance strategies (in deployment order of preference)

1. **Plan around them**: in joint space, singular sets are thin manifolds — a joint-space planner
   (RRT-Connect on the joint space) naturally avoids them. Cartesian straight-line moves are what
   drive arms through singularities. If a task needs a Cartesian path, check `σ_min(J(q(t)))`
   along the whole path at plan time and reject/reshape paths that dip below threshold.
2. **DLS in the controller** (as above): degrades tracking gracefully instead of exploding —
   the tool deviates from the commanded path near the singularity rather than the joints
   exceeding velocity limits. Log when damping activates; it means your plans are bad.
3. **Redundancy** (7-DOF): use the null space to keep `σ_min` high (maximize manipulability as a
   secondary task).
4. **Never** rely on joint velocity limits alone to "catch" a singularity pass-through — the
   path error during the limit-saturated transit is unbounded and unpredictable.

---

## 5. Workspace Analysis

- **Reachable workspace**: set of positions the TCP can attain in *some* orientation.
- **Dexterous workspace**: positions attainable in *every* orientation — much smaller, and the
  one that matters for tasks like drilling normal to a surface anywhere on a part.

For the 3R planar arm: reachable workspace of the wrist point is the annulus
`|L1 − L2| ≤ r ≤ L1 + L2` (modified by joint limits, which typically cut a wedge out of it).

Practical workflow for a real cell:

```python
# Monte-Carlo workspace map with a quality metric — run once at cell-design time
import numpy as np
N = 1_000_000
qs = np.random.uniform(limits[:, 0], limits[:, 1], size=(N, n_joints))
for q in qs:
    p = fk(q)[0:3, 3]
    sigma_min = np.linalg.svd(jac(q), compute_uv=False)[-1]
    voxel_map.update(p, sigma_min)   # store max sigma_min per voxel
# Result: 3D map of "how dexterous is the arm here" — place fixtures in high-sigma regions
```

**Rules of thumb that prevent redesigns:**
- Keep the task region in the middle ~60% of the reach annulus. Tasks at >90% reach live next to
  the elbow singularity; tasks very close to the base live next to the shoulder singularity.
- IK failure rates and required joint speeds both rise sharply near workspace boundaries.
- Check the workspace **with the real tool transform** — a 200 mm tool offset dramatically
  changes which poses are reachable and moves the wrist-singularity locus.

---

## 6. Redundancy Resolution (7+ DOF)

With n > 6, `Δq = J⁺e` is just the minimum-norm solution among infinitely many. The full solution
set is:

```
Δq = J⁺e + (I − J⁺J)·z        # second term: null-space motion, doesn't move the end effector
```

`(I − J⁺J)` projects any vector `z` into the null space. Standard secondary objectives for `z`:

```python
# Joint-centering (most common, keeps arm away from limits):
z = -k0 * (q - q_mid) / (q_max - q_min)**2        # k0 ≈ 0.1–1.0

# Manipulability maximization (stay away from singularities):
z = k0 * numerical_gradient(lambda q: manipulability(q), q)

# Obstacle avoidance: z = gradient of distance-to-obstacle field
```

```python
def ik_step_redundant(J, e, q, q_min, q_max, lam=1e-3, k0=0.5):
    n = J.shape[1]
    JJt_inv = np.linalg.inv(J @ J.T + lam**2 * np.eye(6))
    J_pinv = J.T @ JJt_inv
    q_mid = (q_min + q_max) / 2
    z = -k0 * (q - q_mid) / (q_max - q_min)
    N = np.eye(n) - J_pinv @ J
    return J_pinv @ e + N @ z
```

**The trap with null-space methods**: they resolve redundancy *locally and per-step*. Over a long
trajectory the elbow can drift somewhere bad, and the same Cartesian path executed twice from
different starts ends in different configurations (non-repeatability — pseudoinverse control is
famously non-cyclic). For repeatable industrial motion on a 7-DOF arm, **parameterize the
redundancy explicitly** instead: KUKA iiwa and Franka expose an "elbow angle" / arm-angle ψ
(rotation of the elbow about the shoulder–wrist line). Plan ψ(t) as an explicit DOF, solve
analytical IK given ψ. Franka's `franka_ik` and iiwa analytical solvers work this way.

---

## 7. Solver Selection: IKFast vs KDL vs trac-ik

| | IKFast | KDL (Orocos) | trac-ik |
|---|--------|--------------|---------|
| Type | Analytical (compiled closed-form C++) | Numerical (Newton/pseudoinverse) | Numerical (Newton + SQP, dual-threaded) |
| Speed | **~1–10 µs**, all solutions | ~0.1–1 ms, often fails | ~0.1–0.5 ms, high success rate |
| Solutions returned | All discrete solutions (up to 8/16) | One (local) | One (local), seeded |
| 7-DOF / redundant | Needs a free-joint discretization hack | Yes | Yes |
| Joint limits | Post-filter the solution set | **Poor — gets stuck at limits (its known fatal flaw)** | Good (SQP handles limits as constraints) |
| Setup cost | High: OpenRAVE codegen, can fail on some geometries, brittle toolchain | Trivial (URDF in) | Trivial (URDF in, drop-in KDL replacement in MoveIt) |

**Decision rule:**
- **6-DOF arm + need all solutions or µs-level speed** (e.g., scanning thousands of candidate
  grasps, global trajectory optimization over IK branches): **IKFast** — generate once, ship the
  .cpp. Filter solutions by joint limits and select by continuity (min joint-space distance from
  current q) yourself.
- **General-purpose / MoveIt / any URDF / 7-DOF**: **trac-ik**. It exists specifically because
  KDL's solver has a documented high failure rate near joint limits; trac-ik runs KDL-style
  Newton and an SQP solver in parallel threads and returns the first success. In MoveIt set it in
  `kinematics.yaml`:

```yaml
manipulator:
  kinematics_solver: trac_ik_kinematics_plugin/TRAC_IKKinematicsPlugin
  kinematics_solver_timeout: 0.005          # 5 ms; raise to 0.05 for hard poses
  solve_type: Distance                       # Distance = closest-to-seed (smooth motion)
                                             # Speed = first found (fastest, may jump branches)
```

- **Default KDL**: only acceptable for quick prototypes far from joint limits. Do not ship it.
- Also worth knowing: **pink / mink** (QP-based differential IK on Pinocchio, Python) for
  research-grade whole-body tasks; **Drake**'s `InverseKinematics` (nonlinear program with
  position/orientation/collision constraints) when IK must respect collision avoidance natively;
  **cuRobo** (NVIDIA) for massively parallel GPU IK (thousands of seeds simultaneously).

### Branch selection (the part libraries don't do for you)

When an analytical solver returns 8 solutions, picking the wrong one causes a **configuration
flip**: the arm swings the elbow through 120° between two adjacent waypoints that are 2 mm apart
in Cartesian space. For any *sequence* of IK queries (a path):

```python
def select_solution(solutions, q_prev, joint_limits, weights=None):
    """Pick the IK branch closest to the previous configuration."""
    if weights is None:
        weights = np.ones(len(q_prev))   # consider weighting base joints higher (more inertia)
    best, best_cost = None, np.inf
    for q in solutions:
        if np.any(q < joint_limits[:, 0]) or np.any(q > joint_limits[:, 1]):
            continue
        # Wrap revolute differences to [-pi, pi] for continuous joints!
        dq = np.arctan2(np.sin(q - q_prev), np.cos(q - q_prev))
        cost = np.sum(weights * dq**2)
        if cost < best_cost:
            best, best_cost = q, cost
    return best   # None => no limit-respecting solution: FAIL LOUDLY
```

And enforce a **continuity gate**: if `max|dq|` between consecutive path points exceeds a
threshold (e.g., 0.3 rad for points 1 cm apart), the branch flipped or you crossed a singularity —
reject the path, don't execute it.

---

## 8. Production Failure Modes (the ones that break hardware)

1. **Tool/flange frame confusion.** IK solved for the flange but the target was specified for the
   TCP (or vice versa). Symptom: constant ~tool-length offset in every motion. Always be explicit:
   `T_base_flange = T_base_tcp_target · T_flange_tcp⁻¹` before calling IK.
2. **Degrees passed where radians expected** (or vice versa). Symptom: arm lurches to a bizarre
   pose on the first command. Assert `|q| ≤ 2π + limit_margin` at every API boundary.
3. **Quaternion sign / double-cover bug.** Interpolating between q and −q of the same orientation
   → tool spins the long way. Enforce hemisphere continuity before slerp.
4. **Silent fallback on IK failure.** Solver fails, code uses the seed/last solution, arm executes
   a path to the wrong place. IK failure must propagate as a hard error.
5. **Branch flip mid-path** (see §7). Verify joint-space continuity of every planned path.
6. **Singularity transit on a Cartesian move** — joints 4/6 counter-rotate at max velocity through
   wrist singularity. Check σ_min along the path at plan time.
7. **Calibration mismatch**: nominal DH from the datasheet vs the actual arm (manufacturing
   tolerances + the manufacturer's per-unit calibration). 0.5–2 mm TCP errors are typical with
   nominal parameters. For precision work, use the controller's calibrated kinematics or do a
   kinematic calibration (e.g., with a laser tracker / touch probe + least-squares DH
   identification).
8. **URDF axis conventions**: URDF joints rotate about an arbitrary `<axis>`, not DH z. A
   hand-written DH FK and the URDF-derived FK can disagree in zero-pose offsets and joint signs.
   Pick ONE source of kinematic truth (usually the URDF) and validate against the physical robot:
   jog each joint +10° individually and confirm the TCP moves the direction your FK predicts.

### Debugging methodology when "IK is wrong"

Work up the stack — never debug IK before FK is proven:

1. **Validate FK first**: zero pose vs datasheet TCP; then each joint individually at ±90°;
   compare against the teach pendant's reported Cartesian position (mind the controller's tool
   and base frames!).
2. **Round-trip test**: `q_rand → FK → IK → FK` must reproduce the pose to tolerance for 10k
   random samples. Log failures by region — clusters reveal singular zones or limit issues.
3. **Validate the Jacobian numerically**: finite differences of FK vs analytical J,
   `‖J_analytic − J_fd‖ < 1e-6` (use central differences, h = 1e-6 rad).
4. **Check solution-set completeness** (analytical solvers): for known 8-solution poses, count
   the solutions returned.
5. Only then look at the application layer: frames, units, branch selection, seeding.

```python
def test_ik_roundtrip(fk, ik, limits, n=10000, pos_tol=1e-4, rot_tol=1e-3):
    failures = 0
    rng = np.random.default_rng(0)
    for _ in range(n):
        q = rng.uniform(limits[:, 0], limits[:, 1])
        T = fk(q)
        q_sol, ok, _ = ik(T, seed=rng.uniform(limits[:, 0], limits[:, 1]))
        if not ok:
            failures += 1
            continue
        e = pose_error(T, fk(q_sol))
        assert np.linalg.norm(e[:3]) < pos_tol and np.linalg.norm(e[3:]) < rot_tol
    return failures / n   # trac-ik on a 6/7-DOF arm should be < 1% with one seed
```

---

## 9. Reference Architecture: IK in a Manipulation Stack

```
Task layer        target pose(s) in TASK frame
   │  transform: T_base_target = T_base_task · T_task_target · T_flange_tcp⁻¹
Plan layer        IK (all branches) → branch selection → joint-space path
   │              path checks: limits, continuity (<0.3 rad jumps), σ_min > threshold,
   │              collision (FCL / MoveIt planning scene)
Trajectory layer  time-parameterize (TOTG / Ruckig) respecting q̇/q̈/q⃛ limits
   │
Control layer     1 kHz: optional online DLS-IK (1–3 iters, max_step 0.05 rad)
   │              for servoing / visual correction only — NOT for large motions
Hardware          joint position/velocity commands + the controller's own limit checks
```

Key principle: **solve IK at plan time, in full, with all checks — and keep online IK small.**
Online differential IK (servoing) should only ever make small corrections around a verified plan;
it must run DLS with a hard `max_step`, and it must halt (not improvise) when σ_min drops below
threshold or a joint limit becomes active.

ROS 2 specifics: MoveIt 2 wraps all of this — `kinematics.yaml` selects the IK plugin (use
trac-ik or a generated IKFast plugin via `auto_create_ikfast_moveit_plugin.sh`), the
`PlanningScene` does collision checking, and `moveit_servo` provides the online differential-IK
loop with built-in singularity scaling (`lower_singularity_threshold` ≈ 17,
`hard_stop_singularity_threshold` ≈ 30 on the condition number — tune per arm).

## Quick Reference Card

- IK is multi-valued: handle 0 / finite / infinite solution cases explicitly.
- Verify FK against the physical robot before trusting any IK.
- atan2 always; clamp acos inputs; enumerate all branches; pick by joint-space distance.
- Numerical IK: DLS (λ_min = 1e-3, adaptive to 0.1 near σ_min < 0.05), step cap 0.2 rad,
  random restarts on failure.
- Orientation error = SO(3) log map. Never Euler subtraction. Mind quaternion double cover.
- σ_min(J) is your singularity gauge; check it along every Cartesian path at plan time.
- 6-DOF + need all solutions → IKFast. Everything else → trac-ik. Don't ship default KDL.
- 7-DOF repeatable motion → explicit arm-angle parameterization, not per-step null-space drift.
- IK failure is a hard error. Silent fallback breaks tooling.
