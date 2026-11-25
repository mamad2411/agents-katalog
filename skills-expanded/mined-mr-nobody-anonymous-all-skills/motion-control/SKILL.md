---
name: motion-control
description: "Use when implementing or tuning local motion control for mobile robots - DWA/TEB local planners, pure pursuit path tracking, trajectory scoring, recovery behaviors, velocity smoothing, or collision checking. Provides parameter-level tuning knowledge, the math behind each controller, and the failure modes that cause robots to oscillate, stall, or collide in production."
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


# Local Motion Control: DWA, TEB, Pure Pursuit, Recovery, and Collision Checking

Local motion control is the layer that converts a global path into velocity commands at 10-20 Hz
while respecting kinematics, dynamics, and obstacles seen in the local costmap. This is where most
navigation failures actually happen: a perfect global plan with a badly tuned local controller
produces a robot that oscillates in doorways, stalls near walls, clips obstacles at speed, or
shakes its payload apart with discontinuous accelerations.

Core decisions this skill covers:
1. Which local planner: DWA (sampling-based, robust, slow paths), TEB (optimization-based, fast,
   time-optimal, fragile), pure pursuit / Regulated Pure Pursuit (path tracking, simple, predictable),
   or MPPI (sampling MPC, the modern Nav2 default contender).
2. Every parameter that matters, with starting values and the symptom each one fixes.
3. Recovery behavior design that does not make things worse.
4. Velocity smoothing and acceleration limiting that protects hardware.
5. Footprint vs. radius collision checking and the geometry math behind it.

---

## 1. The control loop contract

Whatever planner you use, the contract is the same:

```
Inputs (per cycle, typically 20 Hz):
  - global plan (list of poses in map frame)
  - local costmap (rolling window, e.g. 6m x 6m, 0.05 m/cell, robot-centered)
  - current velocity (from odometry — feedback, NOT the last commanded velocity)
  - robot footprint or radius

Output:
  - cmd_vel: geometry_msgs/Twist (v_x, v_y, omega), published every cycle, no exceptions
```

Hard rules that prevent hardware damage:

- **Never skip a control cycle.** If computation overruns, publish the previous command decayed
  toward zero, or zero. A stale cmd_vel on most motor controllers means "keep doing the last thing"
  — into a wall. Set a cmd_vel watchdog on the base (typical: stop if no command for 0.5 s).
- **Always forward-simulate with the measured velocity, not the commanded one.** On a loaded robot
  the achieved acceleration is below the configured limit; simulating from commanded velocity
  makes the planner believe it can stop faster than it can.
- **Collision check the trajectory, not the endpoint.** A trajectory whose endpoint is free can
  pass through an obstacle mid-arc.
- **Respect the kinematic model.** Sending v_y to a differential-drive base is silently ignored by
  most base drivers; the planner then believes it executed a motion it didn't.

---

## 2. DWA (Dynamic Window Approach)

### 2.1 The algorithm in five steps

1. **Dynamic window**: from current velocity (v, ω), compute the set of velocities reachable
   within one control period dt given acceleration limits:
   `v ∈ [v - a_max·dt, v + a_max·dt] ∩ [v_min, v_max]`, same for ω.
2. **Sample**: discretize that window into `vx_samples × vth_samples` candidate (v, ω) pairs.
3. **Rollout**: forward-simulate each pair for `sim_time` seconds assuming constant velocity,
   producing an arc. For diff drive, the arc is a circle of radius `r = v/ω` (straight line if ω≈0).
4. **Score**: evaluate each trajectory with a weighted cost function (below). Discard any
   trajectory that collides.
5. **Execute**: command the best (v, ω) for one cycle, then replan.

The key property: DWA only ever commands velocities that are *dynamically reachable in one step*,
so it can never demand an acceleration the base cannot deliver. The key weakness: constant-velocity
rollout means it cannot represent "speed up then slow down" within one trajectory, so it is
conservative in tight spaces and cannot plan reversing maneuvers well.

### 2.2 Trajectory scoring (DWB critics / dwa_local_planner cost function)

Classic DWA cost (lower = better):

```
cost = path_distance_bias  · (distance from trajectory endpoint to global path)
     + goal_distance_bias  · (distance from trajectory endpoint to local goal)
     + occdist_scale       · (max obstacle cost along trajectory)
```

In Nav2's DWB these are critics: `PathAlign`, `PathDist`, `GoalAlign`, `GoalDist`,
`BaseObstacle`/`ObstacleFootprint`, `Oscillation`, `RotateToGoal`, `PreferForward`, `Twirling`.

**The ratio that matters**: `path_distance_bias : goal_distance_bias`. If path bias dominates, the
robot hugs the global path rigidly and refuses to cut corners or dodge obstacles smoothly. If goal
bias dominates, the robot shortcuts toward the goal and ignores the path (which was planned around
obstacles for a reason). The classic disaster: goal bias too high → robot beelines toward goal,
gets trapped in a local minimum the global path avoided.

Starting values (ROS1 dwa_local_planner / Nav2 DWB equivalents):

| Parameter | Start | Effect when increased |
|---|---|---|
| `path_distance_bias` (PathAlign.scale) | 32.0 | Tracks global path tighter; less obstacle-dodging freedom |
| `goal_distance_bias` (GoalAlign.scale) | 24.0 | Cuts toward goal; risk of local minima |
| `occdist_scale` (ObstacleFootprint.scale) | 0.02 | Stronger obstacle avoidance; too high → robot refuses doorways |
| `forward_point_distance` | 0.325 m | Scoring point ahead of robot; affects heading alignment |

`occdist_scale` is deceptively scaled: it multiplies raw costmap values (0-254), so 0.02 × 254 ≈ 5,
comparable to a 0.15 m path deviation at bias 32. If your robot won't enter a doorway whose costmap
cells are inflated to ~200, this product is why. Fix the inflation layer first (see §7), then this gain.

### 2.3 Sampling and simulation parameters

| Parameter | Start (diff drive) | Notes |
|---|---|---|
| `sim_time` | 1.7 s | THE most important DWA parameter. <1.5 s: myopic, oscillates near obstacles. >3 s: trajectories curve far from reality (constant-velocity assumption breaks), corner-cutting, slow scoring. 1.5-2.0 is the sweet spot for ≤1 m/s robots. |
| `sim_granularity` | 0.025 m | Step between collision-check points along trajectory. Must be < half the costmap resolution × min obstacle size you care about. Too coarse → trajectories tunnel through thin obstacles (table legs, door frames). |
| `vx_samples` | 20 | 6-10 is too few for smooth motion; >25 wastes CPU. |
| `vth_samples` | 40 | Angular needs ~2× linear samples — rotation dominates obstacle avoidance for diff drive. |
| `vy_samples` | 0 (diff) / 10 (omni) | MUST be 0 or 1 for diff drive, or the planner scores impossible motions. |
| `controller_frequency` | 20 Hz | Below 10 Hz the dynamic window gets large and motion gets jerky. |

### 2.4 Velocity and acceleration limits

```yaml
max_vel_x: 0.8          # measured top speed × 0.9, never the datasheet number
min_vel_x: 0.0          # set negative ONLY if you want reverse sampling (rarely good with DWA)
max_vel_theta: 1.5      # rad/s
min_vel_theta: 0.4      # minimum rotation speed that actually overcomes static friction
min_in_place_vel_theta: 0.4
acc_lim_x: 1.0          # MEASURE this: command step, log odom, fit slope. Loaded robot, worst surface.
acc_lim_theta: 2.0
trans_stopped_vel: 0.1  # below this, "stopped" for oscillation/goal checks
theta_stopped_vel: 0.1
xy_goal_tolerance: 0.15 # m
yaw_goal_tolerance: 0.17 # rad (~10°)
latch_xy_goal_tolerance: true  # without this, robots orbit the goal: rotating to final yaw
                               # pushes position out of tolerance, repeat forever
```

**Measure acceleration limits, do not copy them.** Command a velocity step 0→max, record odometry,
fit the slope. Use the loaded robot on its worst floor surface. If `acc_lim_x` in config exceeds
reality, every rollout is wrong: the planner thinks it can brake in distance `v²/2a_config` but
the true stopping distance is `v²/2a_real`. At 1 m/s with config 2.0 vs real 1.0 m/s², that's
0.25 m vs 0.5 m — your robot plans to stop 25 cm inside the obstacle.

### 2.5 DWA failure modes

| Symptom | Root cause | Fix |
|---|---|---|
| Oscillates left/right approaching obstacle | sim_time too short; symmetric costs around obstacle | sim_time → 2.0; enable Oscillation critic; raise path_distance_bias |
| Refuses to pass through doorway it fits through | Inflated costmap cost × occdist_scale dominates | Check inflation_radius/cost_scaling_factor first; then lower occdist_scale to 0.01 |
| Cuts corners, clips door frames | goal_distance_bias too high relative to path bias; sim_time too long | Restore 32:24 ratio; sim_time ≤ 2.0 |
| Jerky rotation, "machine-gun" turning | vth_samples too low; min_vel_theta above what's needed | vth_samples ≥ 40 |
| Overshoots goal, orbits it | latch_xy_goal_tolerance false | Set true |
| Sluggish in open space | max_vel never reached because sim_time × max_vel > local costmap radius | Grow local costmap or cap expectations: trajectories leaving the costmap get discarded/penalized |
| Stops dead intermittently while driving | Control loop overruns (scoring too many samples), watchdog zeroes cmd | Reduce samples; check CPU; verify controller_frequency actually achieved (ros2 topic hz /cmd_vel) |

---

## 3. TEB (Timed Elastic Band)

### 3.1 What it actually optimizes

TEB takes the global path segment in the local costmap and deforms it as an "elastic band" of
poses with timestamps: `B = {s_1, Δt_1, s_2, Δt_2, ..., s_n}`. It runs sparse graph optimization
(g2o, Levenberg-Marquardt) minimizing a weighted sum: total time, obstacle clearance, kinematic
feasibility (nonholonomic constraints), velocity/acceleration limits, and path fidelity.
Because time is in the state, TEB produces genuinely time-optimal motion — it accelerates and
brakes within a single trajectory, handles reversing, and supports car-like (Ackermann) robots
natively. DWA can do none of these.

The price: it's a *local* optimizer. The band settles into the homotopy class it started in.
TEB mitigates this with parallel planning in multiple homotopy classes
(`enable_homotopy_class_planning: true`), optimizing up to `max_number_classes` alternatives and
picking the best.

### 3.2 The parameters, grouped by what they break

**Trajectory resolution**

```yaml
dt_ref: 0.3        # desired temporal spacing between band poses. Smaller = finer trajectory,
                   # more optimization variables, more CPU. 0.3 for ≤1 m/s; 0.2 for faster robots.
dt_hysteresis: 0.1 # band resizing deadband, keep ~dt_ref/3
min_samples: 3
max_samples: 500   # cap CPU on long bands
```

**Robot model and kinematics**

```yaml
max_vel_x: 0.8
max_vel_x_backwards: 0.2   # > 0 enables reversing. Set 0.0 only if you truly never reverse —
                            # but then TEB can deadlock in dead ends. Keep small if camera-blind backwards.
max_vel_theta: 1.5
acc_lim_x: 1.0              # measured, same rule as DWA
acc_lim_theta: 2.0
min_turning_radius: 0.0     # 0 = diff drive. >0 = car-like; also set wheelbase and
                            # cmd_angle_instead_rotvel: true for Ackermann steering interfaces
footprint_model:
  type: "polygon"           # point | circular | line | two_circles | polygon
  vertices: [[0.35, 0.25], [0.35, -0.25], [-0.35, -0.25], [-0.35, 0.25]]
```

`footprint_model` is TEB's *optimization* footprint — separate from the costmap footprint used for
final feasibility checking. Polygon is most accurate but each obstacle-distance evaluation costs
edge-wise distance computation. For elongated robots, `line` (a segment along the robot axis +
inflation) is 5-10× cheaper and nearly as accurate. `two_circles` suits robots wider at one end.

**Obstacle handling**

```yaml
min_obstacle_dist: 0.25        # hard clearance target measured FROM the footprint_model boundary,
                               # not the robot center. This + footprint must fit through your
                               # narrowest doorway: door 0.9m, robot 0.6m → max usable
                               # min_obstacle_dist ≈ 0.12 per side. Set 0.25 and the robot
                               # refuses the door or oscillates in it.
inflation_dist: 0.45           # soft cost region beyond min_obstacle_dist; must be > min_obstacle_dist
obstacle_poses_affected: 15    # how many band poses each obstacle attaches to (legacy association)
costmap_converter_plugin: "costmap_converter::CostmapToPolygonsDBSMCCH"
                               # convert costmap cells to polygon obstacles — large CPU win;
                               # without it every occupied cell is a separate point obstacle
include_dynamic_obstacles: true  # use obstacle velocity (if your tracker publishes it) to
                                  # predict positions along the time-parameterized band
```

**Optimization weights** (relative magnitudes are what matter)

```yaml
no_inner_iterations: 5
no_outer_iterations: 4         # outer loop resizes band, inner runs LM. 4×5 is standard.
weight_max_vel_x: 2.0
weight_acc_lim_x: 1.0
weight_kinematics_nh: 1000.0   # nonholonomic constraint. MUST be ~3 orders above other weights
                               # or optimized trajectories include sideways motion a diff-drive
                               # base cannot execute — the #1 cause of "TEB path looks great,
                               # robot does something else"
weight_kinematics_forward_drive: 1.0   # raise to ~1000 to strongly penalize (not forbid) reversing
weight_kinematics_turning_radius: 1.0  # car-like only
weight_optimaltime: 1.0        # the "go fast" weight. Raising it makes motion aggressive and
                               # corner-cutting. This is the main speed/safety dial.
weight_obstacle: 50.0
weight_inflation: 0.1          # keep small; it's a soft gradient, not a barrier
weight_viapoint: 1.0           # adherence to global plan via-points (with global_plan_viapoint_sep > 0)
```

**Homotopy class planning**

```yaml
enable_homotopy_class_planning: true   # ~2-4× CPU; disable on weak compute and accept local minima
max_number_classes: 4
selection_cost_hysteresis: 1.0   # raise to 1.1 to make the planner "stick" to its current
                                  # alternative — fixes the robot dithering between passing
                                  # left vs right of an obstacle (the classic TEB twitch)
```

**Feasibility and goal**

```yaml
feasibility_check_no_poses: 5  # after optimization, verify the first N poses against the REAL
                               # costmap footprint. This is the final safety gate — the optimizer's
                               # soft costs can be violated under tight constraints. Don't set >10:
                               # checking deep into the band rejects plans that would be re-optimized
                               # before the robot ever reaches them, causing spurious aborts.
xy_goal_tolerance: 0.15
yaw_goal_tolerance: 0.17
free_goal_vel: false           # true = don't require zero velocity at (intermediate) goal
```

### 3.3 TEB failure modes

| Symptom | Root cause | Fix |
|---|---|---|
| Robot twitches between left/right pass of an obstacle | Homotopy class flip-flop | selection_cost_hysteresis: 1.1; selection_prefer_initial_plan |
| Executed motion doesn't match planned band (drifts sideways) | weight_kinematics_nh too low | Set ≥1000 |
| Plans through gaps the robot doesn't fit | footprint_model smaller than real robot, or min_obstacle_dist eaten by it | Audit footprint_model against physical robot + payload overhang |
| Refuses/oscillates in doorways | min_obstacle_dist + footprint > doorway | Compute the geometry; reduce min_obstacle_dist; consider a "narrow passage" weight profile |
| CPU spikes, control loop overruns near clutter | Per-cell point obstacles | Enable costmap_converter; cap max_samples; reduce no_outer_iterations to 3 |
| Reverses unexpectedly in open space | Reversing is time-optimal and barely penalized | weight_kinematics_forward_drive: 1000 (penalty) or max_vel_x_backwards: 0.0 (hard, risks deadlock) |
| "trajectory not feasible" aborts on valid-looking plans | feasibility_check_no_poses too high, or optimization footprint ≠ costmap footprint mismatch | Reduce to 4-5; reconcile the two footprints |
| Violent accel/jerk at replan boundaries | Each optimization is independent; band warm-start lost | Verify warm starting works (teb keeps the band between cycles by default); add velocity smoother downstream (§6) |

### 3.4 DWA vs TEB vs MPPI decision

- **DWA/DWB**: choose for slow (<0.7 m/s) robots, weak compute, predictability requirements,
  diff-drive only. It is hard to make DWA do something violent.
- **TEB**: choose for car-like robots (the only mainstream option with min_turning_radius),
  robots that must reverse, speed-critical applications. Budget real tuning time and CPU.
- **MPPI (Nav2)**: sampling-based MPC, ~2000 noised trajectory rollouts scored per cycle on the
  GPU/SIMD. Best dynamic-obstacle behavior of the three, smooth, actively maintained as the Nav2
  default direction. Choose for new ROS2 builds with decent compute. Its critics mirror DWB's
  (PathAlign, Obstacles, Goal, PreferForward), so DWB tuning intuition transfers.

---

## 4. Pure Pursuit and Regulated Pure Pursuit

### 4.1 The math

Pure pursuit is geometric path *tracking*, not planning: pick a point on the path at lookahead
distance `L_d` ahead of the robot, and command the arc that passes through it.

In the robot frame, with the lookahead point at (x, y), the required arc curvature is:

```
κ = 2y / L_d²
```

Derivation: chord of length L_d on a circle of radius R subtends lateral offset y, with
`L_d² = 2Ry` from circle geometry, so `R = L_d²/(2y)`, `κ = 1/R`.

For a diff-drive robot at linear speed v: `ω = v·κ = 2·v·y / L_d²`.
For Ackermann with wheelbase W: steering angle `δ = atan(W·κ) = atan(2W·y / L_d²)`.

Worked example: robot at 0.5 m/s, lookahead 0.8 m, lookahead point 0.1 m to the left (y = +0.1):
`ω = 2 × 0.5 × 0.1 / 0.64 = 0.156 rad/s` — a gentle left arc. Same offset at L_d = 0.4:
`ω = 0.625 rad/s` — 4× sharper. Curvature gain scales with 1/L_d²; this is why lookahead is the
single tuning knob and why it's so sensitive.

### 4.2 Lookahead tuning

- **Too short** (< ~0.5× robot length or < v × 0.5 s): the controller acts like a high-gain
  servo on lateral error → weaving/oscillation along the path, worse at speed.
- **Too long**: corner cutting — the chord to a far lookahead point shortcuts the inside of every
  curve. On a 90° corner with L_d = 1.5 m the robot can cut 0.3-0.5 m inside the path. If the
  global planner put the path 0.3 m from the wall, that's a collision.
- **Rule of thumb**: `L_d = k·v` with k ≈ 0.8-1.5 s (velocity-scaled lookahead), clamped to
  `[min_lookahead, max_lookahead]` ≈ [0.3, 1.5] m for an indoor robot. Constant lookahead is
  acceptable only at constant speed.

Implementation details that bite:

- **Find the lookahead point by walking the path forward from the closest point** — never by
  global nearest-at-distance-L_d search, or on self-intersecting / switchback paths the robot
  locks onto the wrong branch.
- **Interpolate between path waypoints** for the exact L_d intersection; snapping to discrete
  waypoints causes curvature steps.
- **Goal approach**: when remaining path < L_d, the lookahead point clamps to the goal and the
  geometry degenerates. Switch to a position controller (proportional slow-down,
  `v = min(v_max, k_p·dist)`) for the last L_d meters, then rotate to final heading in place.

### 4.3 Regulated Pure Pursuit (Nav2 RPP)

Plain pure pursuit has zero obstacle awareness and constant speed. RPP adds the regulation
heuristics that make it production-usable:

```yaml
desired_linear_vel: 0.5
lookahead_dist: 0.6
use_velocity_scaled_lookahead_dist: true
min_lookahead_dist: 0.3
max_lookahead_dist: 0.9
lookahead_time: 1.5                       # L_d = v × lookahead_time when velocity-scaled
regulated_linear_scaling_min_radius: 0.9  # slow down when path curvature radius < this:
                                          # v_cmd = v · (r / r_min) — slows for corners
use_cost_regulated_linear_velocity_scaling: true  # slow down near high-cost costmap regions
use_collision_detection: true
max_allowed_time_to_collision_up_to_carrot: 1.0   # project current cmd forward; if it hits
                                                   # costmap-lethal within 1 s, stop
use_rotate_to_heading: true               # diff drive: rotate in place when path heading
rotate_to_heading_min_angle: 0.785        # differs by > 45° (e.g., path starts behind robot)
max_angular_accel: 3.2
```

RPP is the right choice when: the global planner is feasible and smooth (e.g., Smac Hybrid-A*
for car-like, or a smoothed grid path), the environment is mostly static, and you want
predictable, certifiable behavior. It *tracks*; it does not *avoid*. Dynamic obstacle avoidance
must come from elsewhere (replanning the global path, or a safety layer that scales velocity).

### 4.4 Pure pursuit failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Weaving at speed | Lookahead too short for v | use_velocity_scaled_lookahead, lookahead_time ≥ 1.0 |
| Cuts corners into obstacles | Lookahead too long; path planned too close to walls | Shrink max_lookahead; increase global inflation so paths keep clearance ≥ max corner cut |
| Spins at start when path is behind | No rotate-to-heading | Enable use_rotate_to_heading (diff drive) |
| Oscillates at goal | Degenerate geometry inside last L_d | Goal-approach mode: proportional slowdown + in-place final rotation |
| Steady-state offset on long curves | Pure pursuit has inherent tracking error ≈ L_d²·κ/2 on constant curvature | Accept it, shorten L_d in curves, or add curvature feedforward |

---

## 5. Recovery behaviors

Recovery triggers when the controller can't find a valid command or the robot makes no progress.
Design principle: **recoveries must be ordered from least to most aggressive, each must be
collision-checked, and the sequence must terminate in a failure report — not loop forever.**

Standard escalation ladder:

1. **Costmap clearing** (cheap, safe, fixes ~70% of stalls): clear obstacles outside a radius
   (e.g., 3 m) from the local costmap. Most stalls are *phantom obstacles* — stale lethal cells
   from sensor noise, a person who walked away, or raytracing shadows. Clearing lets the planner
   see reality again. If clearing alone fixes it repeatedly, your real bug is in the observation
   layer: check `raytrace_max_range` > `obstacle_max_range`, and that your sensor actually clears
   space (a 2D lidar can't clear cells marked by a depth camera layer at a different height).
2. **Wait** (e.g., 5 s): dynamic obstacles often just move. Cheapest "recovery" of all; deploy
   before any motion-based recovery in human environments.
3. **Back up** (0.15-0.3 m, ≤0.1 m/s): collision-check the reverse path against the costmap.
   If the robot has no rear sensing, the costmap behind it may be stale — limit distance to what
   was recently observed, or don't back up at all.
4. **Rotate in place / spin** (90-360°): refreshes the costmap with a full sensor sweep AND can
   un-wedge heading-dependent stalls. MUST be footprint-checked through the full rotation —
   the classic production incident is a rectangular robot commanded to spin in a corridor where
   its diagonal doesn't fit (see §7 swept-rotation check). Skip this recovery entirely for
   long robots in narrow spaces.
5. **Abort + report** with a machine-readable reason (`NO_VALID_CONTROL`, `OSCILLATION`,
   `PROGRESS_TIMEOUT`) so the fleet layer can dispatch help.

Anti-patterns seen in production:

- **Aggressive clearing as first AND only recovery** → clear, replan into the same real obstacle,
  stall, clear, repeat at 0.2 Hz forever. Cap recovery rounds (2-3 full ladders) per goal.
- **Rotate recovery on a robot with a tail/trailer** → physical wedge or collision. Recoveries
  use the same footprint as planning; if your footprint is wrong, recoveries are where it kills you.
- **Backup into the void**: backing up beyond sensed space on stairs/dock edges. Gate reverse
  recoveries on rear sensor coverage or recent-observation maps.
- **No oscillation detection**: robot toggles left/right forever without triggering recovery
  because each cycle "has a valid command." Track net progress: if displacement over 10 s < 0.2 m
  while cmd_vel ≠ 0, that's a stall → recovery.

Nav2 implements recoveries as behavior-tree nodes (`ClearEntireCostmap`, `Spin`, `BackUp`, `Wait`)
in `bt_navigator`'s recovery subtree — encode the ladder and round-cap in the BT, not in planner code.

---

## 6. Velocity smoothing and acceleration limiting

Raw planner output is discontinuous: replans jump the commanded velocity, planner failures drop it
to zero instantly. Unfiltered, this causes wheel slip (odometry corruption → localization drift),
payload shift, brownouts from motor current spikes, and mechanical wear.

Put a velocity smoother between the controller and the base. Per axis, per cycle:

```python
def smooth(v_cmd, v_prev, dt, a_max, d_max, v_max):
    v_cmd = max(-v_max, min(v_max, v_cmd))
    dv = v_cmd - v_prev
    # accel = increasing |v|; decel = decreasing |v|  (sign-aware!)
    limit = a_max if (v_prev == 0 or dv * v_prev > 0) else d_max
    max_dv = limit * dt
    return v_prev + max(-max_dv, min(max_dv, dv))
```

Rules:

- **Smooth against feedback, not the last command** (Nav2 velocity_smoother: `feedback: OPEN_LOOP`
  vs `CLOSED_LOOP`). Open-loop integrates your own commands — fine if the base tracks well.
  Closed-loop uses odometry — correct when the base saturates, but noisy odom causes chatter;
  filter it.
- **Asymmetric limits**: deceleration limit should be 1.5-2× the acceleration limit
  (`decel_lim_x: -2.0` vs `acc_lim_x: 1.0`). Braking hard is safe; jerking forward is not.
- **Do NOT smooth emergency stops.** The smoother must have a bypass: a zero command flagged as
  e-stop passes through unsmoothed, and the safety PLC/hardware stop is below this layer anyway.
  A smoother that ramps down an e-stop over 0.8 s adds 0.4 m of stopping distance at 1 m/s.
- **Keep planner limits and smoother limits consistent.** If the smoother is more restrictive
  than the planner believes (`acc_lim` mismatch), the planner's rollouts are fiction: it plans
  stops it can't execute. Smoother limits ≥ planner-configured limits, always.
- **Jerk limiting** (limit da/dt, typical 2-5 m/s³): worth it for liquid payloads, tall robots
  (tipping), and rider comfort. Implement as a second-order filter or S-curve profile; adds lag
  (~a_max/j_max seconds), so account for it in stopping-distance math.
- Nav2: `nav2_velocity_smoother` node, `smoothing_frequency: 20.0`, with `deadband_velocity` to
  zero out commands too small for the motors to execute (which otherwise whine and heat).

Diff-drive subtlety: limiting v and ω independently changes their *ratio*, which changes the arc —
a smoothed command follows a different curve than the planned one. Scale (v, ω) by a common factor
when either saturates to preserve curvature: `s = min(1, v_lim/|v|, ω_lim/|ω|); v *= s; ω *= s`.

---

## 7. Footprint vs radius collision checking

### 7.1 The two models

**Radius (circumscribed circle)**: robot = circle of radius `r_circ = max distance from rotation
center to any footprint vertex`. Collision check = one costmap lookup per pose against a
distance-inflated costmap. O(1), rotation-invariant.

**Footprint (polygon)**: actual robot outline as a vertex list around the rotation center.
Collision check = rasterize the transformed polygon edges onto the costmap and test cells.
O(perimeter/resolution) per pose, orientation-dependent.

The decision is pure geometry. For footprint `[[0.45,0.30],[0.45,-0.30],[-0.45,-0.30],[-0.45,0.30]]`
(0.9 × 0.6 m box):

- inscribed radius `r_insc = 0.30` (half-width — nearest edge to center)
- circumscribed radius `r_circ = √(0.45² + 0.30²) = 0.54`

A radius model uses 0.54 m everywhere: the robot believes it is a 1.08 m-diameter disc and
**cannot plan through any gap under 1.08 m** even though it physically passes 0.62 m doorways
when aligned. If your narrowest passage > 2·r_circ + margin, use the radius model and enjoy the
CPU savings. Otherwise you need the polygon.

### 7.2 How the costmap encodes this (ROS inflation layer)

The inflation layer assigns cost by distance d from the nearest lethal cell:

```
d = 0                  → 254 (LETHAL)
0 < d ≤ r_insc         → 253 (INSCRIBED — robot center here = guaranteed collision regardless of heading)
r_insc < d             → cost = 252 · exp(-cost_scaling_factor · (d − r_insc)), down to 0 past inflation_radius
```

Planner semantics:

- Center cell = 254 or 253 → collision, no polygon check needed (cheap rejection).
- Cost between 253 and the *circumscribed cost* (the cost value at d = r_circ) → **possibly**
  in collision depending on heading → run the full polygon check.
- Cost below circumscribed cost → free for any heading, no polygon check (cheap acceptance).

This three-band scheme is why `inflation_radius` must exceed r_circ: if inflation stops short,
the "possibly colliding" band is truncated and orientation-dependent collisions get cheap-accepted.
Set `inflation_radius ≥ r_circ + 0.3` and tune `cost_scaling_factor` (lower = costs decay slower
= robot keeps more clearance; start 3.0, range 2-10).

### 7.3 Footprint checking done right

```python
def footprint_cost(pose, footprint, costmap) -> float:
    """Returns max cost under the footprint at pose, or LETHAL on any hit.
    pose: (x, y, theta) in costmap frame."""
    x, y, th = pose
    c, s = cos(th), sin(th)
    pts = [(x + c*fx - s*fy, y + s*fx + c*fy) for fx, fy in footprint]
    worst = 0
    for i in range(len(pts)):
        # Bresenham along each edge at costmap resolution
        for cell in raytrace(costmap.world_to_map(pts[i]),
                             costmap.world_to_map(pts[(i+1) % len(pts)])):
            cost = costmap.get(cell)
            if cost >= LETHAL_OBSTACLE:        # 254, and treat NO_INFORMATION per policy
                return LETHAL_OBSTACLE
            worst = max(worst, cost)
    return worst
```

Critical correctness points:

- **Edges only is the standard (and a known gap).** ROS costmap_2d checks the polygon *perimeter*,
  not the interior. An obstacle strictly inside the footprint (you drove over a small object, or
  a costmap update appeared under you) is missed. Combine with the inscribed-cost center check
  (253 catches anything within r_insc of a lethal cell) — the pairing covers the interior for
  convex footprints as long as inflation is configured. Concave footprints break this assumption:
  convexify them or add interior sampling.
- **Pad the physical footprint** (`footprint_padding: 0.03-0.05 m`): sensor noise, localization
  jitter, and base tracking error all eat margin. Padding belongs in the footprint, not hidden
  in inflation, so that swept checks (below) include it.
- **Swept volume between trajectory samples.** Checking poses every `sim_granularity` along a
  trajectory leaves gaps between consecutive polygons through which thin obstacles pass. Either
  keep linear steps ≤ costmap resolution, or check the convex hull of consecutive footprint pairs.
- **Rotation sweep.** For in-place rotation (and rotate recoveries), sample headings every
  `angular_sim_granularity` (≤ 0.1 rad for long robots) — between 0° and 90° a 0.9 × 0.6 m robot's
  corners sweep through the full r_circ = 0.54 m circle. The cheap conservative test: if the cell
  at the rotation center has cost < circumscribed-cost, the whole rotation is free; otherwise
  check every sampled heading.
- **NO_INFORMATION (255) policy**: in unexplored space, treating unknown as free lets the robot
  drive off sensed terrain; treating it as lethal can imprison it at startup. Standard: unknown =
  lethal for the local planner, traversable-with-penalty for the global planner.
- **The footprint must include everything attached**: payload overhang, open lid, lidar mast,
  charging contacts. Audit with a tape measure after every hardware change. A footprint 4 cm
  smaller than the physical robot is invisible in the lab and a guaranteed collision in the field.

### 7.4 Performance

Polygon checking 20 trajectories × 40 poses × 60 perimeter cells = 48k costmap reads per cycle —
fine at 20 Hz. DWA's full 800-trajectory sampling pushes ~2M reads; this is why DWB scores most
critics on the cheap center-cell cost and reserves the polygon (`ObstacleFootprint` critic) for
when the center cost is in the "possibly colliding" band. If your control loop overruns: profile
first, then reduce samples, coarsen sim_granularity toward the costmap resolution (never beyond),
or shrink the local costmap — in that order.

---

## 8. Bring-up and debugging methodology

Tune in this order; each step has a pass criterion before the next:

1. **Base layer**: command fixed cmd_vel by hand (`teleop`, or
   `ros2 topic pub /cmd_vel geometry_msgs/Twist ...`). Verify the base tracks v and ω accurately
   (plot cmd vs odom). Measure real acc limits here. *Until the base tracks open-loop commands,
   no planner tuning is meaningful.*
2. **Costmap layer**: visualize local costmap in RViz with the footprint overlay. Walk around the
   robot; confirm obstacles appear AND clear (clearing bugs cause most "random stop" reports).
   Confirm the footprint polygon matches the physical robot.
3. **Tracking, no obstacles**: long straight path, then gentle curves, in open space. Tune
   path-following gains / lookahead until tracking error < 5 cm without weaving.
4. **Static obstacles**: single box, then doorway, then corridor. This is where you tune
   obstacle weights and observe doorway behavior.
5. **Dynamics**: people walking; tune slow-down and recovery triggers.
6. **Endurance**: hours of loop driving; watch for the slow failures (costmap memory of phantom
   obstacles, recovery loops, control-loop frequency degradation).

Instruments that find the bug fast:

- `ros2 topic hz /cmd_vel` — controller actually running at configured frequency? Overruns
  show up here first.
- Plot cmd_vel vs odom twist on one graph — tracking gap = base saturation = your config
  acc/vel limits are lies.
- Publish & visualize the scored trajectory cloud (DWB publishes evaluations;
  teb markers show the band) — watch *why* the planner prefers the bad trajectory; usually one
  critic's scale dominates.
- Log the costmap cost under the robot center continuously — spikes reveal phantom obstacles
  and inflation misconfiguration.
- When the robot does something wrong, save a rosbag of /tf, costmaps, cmd_vel, odom, and the
  plan topics. Local planner bugs are 90% reproducible offline from the bag.

The meta-rule of motion control tuning: **every "planner bug" is first a costmap bug, an odometry
bug, or a lied-about acceleration limit until proven otherwise.** Check those three before
touching a single weight.
