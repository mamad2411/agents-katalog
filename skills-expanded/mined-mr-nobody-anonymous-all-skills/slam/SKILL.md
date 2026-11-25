---
name: slam
description: "Use when building, tuning, or debugging SLAM and localization on mobile robots — occupancy grid mapping, AMCL particle filter localization, graph SLAM with slam_toolbox or Cartographer, visual SLAM (ORB-SLAM3) vs lidar SLAM selection, map saving/serving, loop closure tuning, and fixing corridor/featureless-environment failures."
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


# SLAM: Mapping, Localization, and Why Robots Get Lost

This skill covers the SLAM knowledge needed to ship a mobile robot that builds a map once and
localizes on it reliably for years. The math is stated plainly with worked examples, the configs
are real starting points (not defaults), and the failure modes are the ones that actually kill
robots in production: corridors, glass, kidnapped robots, and odometry drift that silently
poisons your map.

---

## 1. The Core Problem in One Paragraph

SLAM is a chicken-and-egg problem: to build a map you need to know where you are, and to know
where you are you need a map. Every SLAM system breaks this circle the same way — it trusts
odometry over short distances (where drift is small), registers sensor data against the map
built so far, and corrects accumulated drift when it recognizes a previously visited place
(**loop closure**). The quality of any SLAM system is determined almost entirely by three
things: (1) how good the odometry prior is, (2) how distinctive the environment is to the
sensor, and (3) whether loop closures fire correctly. Everything else is tuning.

### The error model that matters

Wheel odometry drift is typically **1–5% of distance traveled** for translation and
**0.5–2 degrees per meter** for rotation on a well-calibrated differential-drive base
(rotation error dominates — a 1° heading error becomes 17 cm of lateral error after 10 m,
because heading error converts to position error proportional to subsequent distance).
Working rule of thumb: **after a 100 m loop, expect 1–3 m of accumulated pose error before
loop closure**. Your loop closure search radius must exceed this number or closures will never be
found. This single relationship explains most "my map is smeared" bug reports.

---

## 2. Occupancy Grid Mapping

The standard 2D map representation: a grid where each cell holds the probability it is
occupied. Updates use **log-odds** because they turn Bayesian multiplication into addition:

```
l(cell) = log( p / (1 - p) )

On each lidar beam:
  cells along the ray (free space):  l += l_free   (e.g., -0.4, p≈0.40)
  cell at the beam endpoint (hit):   l += l_occ    (e.g., +0.85, p≈0.70)
  clamp l to [l_min, l_max]          (e.g., [-2.0, +3.5]) so cells can recover
```

Worked example: a cell starts unknown (l = 0, p = 0.5). Three consecutive scans hit it:
l = 0 + 0.85·3 = 2.55 → p = 1/(1+e^-2.55) = 0.93. A person walks through and two scans see
through the cell: l = 2.55 − 0.8 = 1.75 → p = 0.85. The clamp matters: without l_max, a wall
observed 10,000 times needs 10,000 contrary observations to clear — your map can never adapt
when furniture moves.

**Resolution choice:** 0.05 m/cell is the industry standard for indoor robots. 0.025 m only
if you need tight docking precision (4× the memory and CPU). 0.10 m for large outdoor areas.
A 100×100 m building at 0.05 m is a 2000×2000 grid = 4 MB as int8 — memory is rarely the
constraint; scan-matching cost scales with resolution.

**Trinary convention (ROS):** map_server publishes cells as -1 (unknown), 0 (free),
100 (occupied). The thresholds that convert probability to trinary live in the map YAML
(`occupied_thresh: 0.65`, `free_thresh: 0.196` — keep the defaults unless you have a reason).

---

## 3. Particle Filter Localization (AMCL)

Once you have a map, you localize on it. AMCL (Adaptive Monte Carlo Localization) maintains
a cloud of particles, each a pose hypothesis (x, y, θ, weight):

1. **Predict:** move every particle by the odometry delta plus sampled noise.
2. **Update:** weight each particle by how well the lidar scan matches the map from that pose
   (likelihood field model: for each beam endpoint, look up distance to nearest obstacle).
3. **Resample:** draw a new particle set proportional to weights (low-variance resampling),
   only when effective sample size drops — resampling every step causes particle depletion.
4. **Adapt (KLD sampling):** shrink the particle count when converged, grow it when uncertain.

### The AMCL parameters that actually matter (ROS 2 Nav2 names)

```yaml
amcl:
  ros__parameters:
    # --- Particle count ---
    min_particles: 500          # below this, corridor localization gets flaky
    max_particles: 2000         # 5000+ for global localization in large maps; CPU scales linearly

    # --- Odometry noise model (THE most-mistuned params) ---
    # alpha1: rot noise from rot, alpha2: rot noise from trans,
    # alpha3: trans noise from trans, alpha4: trans noise from rot
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    # Defaults (0.2) assume mediocre odometry. Good wheel+IMU fusion: drop to 0.05–0.1.
    # Skid-steer or omni on slick floors: raise alpha1/alpha4 to 0.4–0.8.
    # Symptom of too-low alphas: particle cloud stays tight but drifts off the true pose,
    # then snaps violently or diverges — the filter is overconfident in odometry.
    # Symptom of too-high: cloud is huge, pose jumps around, robot "wanders" in place.

    # --- Laser model ---
    laser_model_type: "likelihood_field"   # always; "beam" is slower and brittle
    laser_likelihood_max_dist: 2.0
    z_hit: 0.7                  # weight of "beam matches map"
    z_rand: 0.3                 # weight of "random garbage" — z_hit + z_rand = 1.0
    # In dynamic environments (people, pallets), raise z_rand to 0.4–0.5 so unexpected
    # obstacles don't tank the weights of correct particles.
    sigma_hit: 0.2              # m; std-dev of the hit model; match your lidar noise + map error
    max_beams: 60               # beams actually used per scan; 60 is plenty, 180+ wastes CPU
                                # EXCEPTION: long corridors — see section 8, raise to 100–180

    # --- Update gating ---
    update_min_d: 0.1           # m moved before filter updates (default 0.25 is too lazy)
    update_min_a: 0.1           # rad turned before update
    resample_interval: 1        # resample every Nth update; 2 reduces depletion in corridors

    # --- Recovery ---
    recovery_alpha_slow: 0.001  # 0.0 disables recovery — set these nonzero!
    recovery_alpha_fast: 0.1
    # These enable injection of random particles when short-term likelihood drops below
    # long-term average — the only built-in defense against the kidnapped-robot problem.

    do_beamskip: true           # skip beams that disagree with map consensus (dynamic obstacles)
    beam_skip_threshold: 0.3
```

**Convergence check before trusting the pose:** read the covariance from
`/amcl_pose` (`PoseWithCovarianceStamped`). Rule of thumb: localized means
cov[0] (x) and cov[7] (y) < 0.25 (i.e., σ < 0.5 m) and cov[35] (yaw) < 0.1 rad².
Gate autonomous motion on this — a robot navigating on a diverged AMCL pose will drive
into walls with full confidence.

```python
# Localization health gate (rclpy)
def amcl_converged(msg: PoseWithCovarianceStamped) -> bool:
    c = msg.pose.covariance
    return c[0] < 0.25 and c[7] < 0.25 and c[35] < 0.1
```

**Global localization (unknown start pose):** call the `/reinitialize_global_localization`
service, raise max_particles to 5000–10000, drive the robot (rotation + a few meters of
translation — pure rotation cannot disambiguate), and wait for convergence. In symmetric
environments (identical aisles) global localization is fundamentally ambiguous — fix with
an initial pose from a dock, an AprilTag, or WiFi/UWB coarse prior, not with more particles.

---

## 4. Graph SLAM — The Concept

Modern SLAM (slam_toolbox, Cartographer, ORB-SLAM3) is graph-based, not filter-based:

- **Nodes** = robot poses at keyframe times (and, in visual SLAM, landmark positions).
- **Edges** = constraints with uncertainty: odometry between consecutive poses, scan-match
  results, loop closures.
- **Optimization** = find the set of poses that minimizes total constraint error
  (nonlinear least squares — Gauss-Newton/Levenberg-Marquardt via Ceres, g2o, or GTSAM).

The killer feature vs particle filters: **when a loop closure is found, the entire trajectory
is re-optimized and the map is rebuilt from corrected poses.** Drift accumulated over the loop
is distributed along it, weighted by each edge's covariance. A particle filter can never undo
a past mistake; a graph can.

The cost being minimized:

```
F(x) = Σ_ij  e_ij(x_i, x_j)ᵀ · Ω_ij · e_ij(x_i, x_j)
```

where e_ij is the difference between predicted and measured relative pose, and Ω_ij
(information matrix = inverse covariance) says how much to trust that edge. Practical
consequence: **a single false loop closure with high confidence (large Ω) will fold your map
in half.** False closures are worse than missed closures, always tune in that direction.

### Loop closure, concretely

1. Candidate generation: poses within search radius of the current pose estimate
   (radius must exceed accumulated drift — the section 1 rule).
2. Verification: scan-to-map matching (correlative scan matching in slam_toolbox) produces
   a match response score; below threshold → reject.
3. Edge insertion + global optimization.

Failure signatures:
- **Missed closures** (search radius too small / threshold too strict): map "feathers" —
  the same wall appears twice, slightly offset, after revisiting an area.
- **False closures** (threshold too loose, repetitive structure): map suddenly folds,
  corridors merge, everything is catastrophically wrong from one moment to the next.
  In warehouses with identical aisles this is THE failure mode — raise thresholds and
  rely on driving distinctive routes (cross-aisle passes) during mapping.

---

## 5. slam_toolbox — The Default Choice for 2D

slam_toolbox is the Nav2-blessed default. Use it unless you have a specific reason not to.

```yaml
slam_toolbox:
  ros__parameters:
    mode: mapping                      # or "localization" — see below
    odom_frame: odom
    map_frame: map
    base_frame: base_footprint
    scan_topic: /scan
    use_scan_matching: true
    resolution: 0.05
    max_laser_range: 20.0              # set to your lidar's REAL reliable range, not spec sheet
    minimum_travel_distance: 0.5       # m between keyframes; 0.2 for small/cluttered spaces
    minimum_travel_heading: 0.5        # rad
    map_update_interval: 5.0           # s; lower = fresher published map, more CPU
    transform_publish_period: 0.02     # 50 Hz map->odom TF; 0 disables (don't)

    # --- Scan matching ---
    minimum_angle_penalty: 0.9
    link_match_minimum_response_fine: 0.1
    correlation_search_space_dimension: 0.5      # m; raise to 0.8–1.0 if odom is poor

    # --- Loop closure (the knobs that matter) ---
    do_loop_closing: true
    loop_search_maximum_distance: 3.0  # RAISE to 6–10 for loops >50 m (drift rule, section 1)
    loop_match_minimum_chain_size: 10  # consecutive scans that must agree; raise to 15 in
                                       # repetitive environments to suppress false closures
    loop_match_minimum_response_coarse: 0.35
    loop_match_minimum_response_fine: 0.45  # RAISE to 0.55+ if you ever see a false closure
```

**Lifelong/localization mode:** slam_toolbox's `localization` mode loads a serialized pose
graph and continues matching against it without growing it. This is the modern alternative
to AMCL — it handles environment change better (it keeps scan-matching) but costs more CPU
and lacks AMCL's decades of corner-case hardening. Reasonable default: **AMCL for production
fleets** (cheap, predictable, well-understood failure modes), **slam_toolbox localization mode**
when the environment changes often.

**Saving — there are TWO formats and you need both:**

```bash
# 1. Occupancy grid (.pgm + .yaml) — what AMCL/Nav2 costmaps consume
ros2 run nav2_map_server map_saver_cli -f ~/maps/warehouse --ros-args -p save_map_timeout:=10.0

# 2. Serialized pose graph (.posegraph + .data) — what slam_toolbox needs to
#    continue mapping later or run localization mode. The .pgm CANNOT be converted back.
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph \
  "{filename: '/home/robot/maps/warehouse'}"
```

Losing the posegraph file means you can never extend that map — only remap from scratch.
Archive both formats per site, versioned.

**Serving the map:**

```yaml
map_server:
  ros__parameters:
    yaml_filename: "/home/robot/maps/warehouse.yaml"
```

map_server is a lifecycle node — it publishes nothing until activated. The classic
"AMCL gets no map" bug is a map_server stuck in unconfigured state; check
`ros2 lifecycle get /map_server` and make sure it's managed by Nav2's lifecycle_manager.
The map topic is published with transient_local QoS (latched) — subscribers must request
transient_local durability or they receive nothing.

The map YAML:

```yaml
image: warehouse.pgm
resolution: 0.05
origin: [-50.0, -50.0, 0.0]   # pose of pixel (0, bottom row) in the map frame; NEVER hand-edit
negate: 0                      # the rotation term without understanding it — a wrong origin
occupied_thresh: 0.65          # shifts every goal in your fleet's database
free_thresh: 0.196
```

---

## 6. Cartographer vs slam_toolbox

| | slam_toolbox | Cartographer |
|---|---|---|
| Maintenance (2024+) | Active, Nav2 default | Effectively unmaintained upstream |
| Tuning difficulty | ~10 params matter | 50+ interacting params, notoriously hard |
| Odometry requirement | Wants decent odom | Can run lidar+IMU only (good IMU required) |
| Loop closure | Correlative matching | Branch-and-bound (very strong) |
| 3D support | No | Yes (3D lidar) |
| Map continuation | Yes (posegraph serialization) | Painful (pbstream, offline reprocessing) |
| Localization on saved map | Built-in localization mode | pure_localization trimmer mode |

**Decision rule:** slam_toolbox for any standard 2D indoor robot. Cartographer only if
(a) you need 3D lidar SLAM and can't use a modern LIO stack, or (b) you have no usable wheel
odometry but a good IMU. If you pick Cartographer, the two params that dominate everything:
`TRAJECTORY_BUILDER_2D.ceres_scan_matcher.translation_weight` /`rotation_weight` (how much to
trust the prior vs the scan match) and `POSE_GRAPH.constraint_builder.min_score` (loop closure
acceptance, default 0.55 — raise to 0.65 in repetitive spaces). For 3D lidar in 2026, prefer
a LIO front-end (FAST-LIO2, LIO-SAM) feeding a pose graph, not Cartographer 3D.

---

## 7. Visual SLAM vs Lidar SLAM — Selection

**Default to 2D lidar SLAM for indoor ground robots.** It is more robust, cheaper to compute,
and produces the occupancy grid Nav2 needs anyway. Choose visual SLAM (ORB-SLAM3, RTAB-Map,
Isaac VSLAM) when: the platform can't carry a lidar (drones, small/cheap robots), you need
appearance-based relocalization, or you're outdoors where 2D lidar geometry is degenerate.

| Failure condition | Lidar SLAM | Visual SLAM |
|---|---|---|
| Long featureless corridor | FAILS (see §8) | OK if textured walls |
| Textureless white walls | OK (geometry exists) | FAILS |
| Glass, mirrors | FAILS (beams pass through / reflect) | Mostly OK |
| Darkness / lighting change | OK | FAILS (or needs active IR) |
| Fast rotation | OK (with IMU) | FAILS (motion blur, tracking lost) |
| Dynamic crowds | Degraded | Degraded |
| Direct sunlight on sensor | Some lidars degrade | FAILS (exposure) |
| Map for navigation | Occupancy grid, directly usable | Sparse point cloud — NOT a costmap |

**ORB-SLAM3 in practice:** use **stereo-inertial or RGB-D-inertial mode** — monocular has
unobservable scale (the map is correct up to an unknown scale factor; useless for metric
navigation) and scale drifts over time. Critical integration facts:

- It needs accurate **camera-IMU extrinsics and time offset** — calibrate with Kalibr;
  >2 ms time-sync error between camera and IMU degrades it badly. Hardware-sync if possible.
- Output is a camera trajectory + sparse ORB landmark cloud. To navigate you still need to
  build occupancy from depth (e.g., project RGB-D depth into a 2D costmap, or use RTAB-Map
  which produces grids natively). **RTAB-Map is usually the better choice when the goal is
  "visual SLAM that feeds Nav2"** — it's a full graph-SLAM system with occupancy output,
  appearance-based loop closure (bag-of-words), and active maintenance.
- Tracking loss is normal, not exceptional. Your integration must handle the LOST state:
  stop the robot, hold last pose, attempt relocalization, escalate after a timeout.
  Never let a planner consume a VSLAM pose without checking tracking state.

---

## 8. Why SLAM Fails in Corridors (and How to Fix It)

The most common production SLAM failure. A long corridor seen by a 2D lidar is two parallel
lines. Scan matching can lock the pose **across** the corridor (lateral, fully constrained)
and in **heading** (well constrained), but motion **along** the corridor produces a nearly
identical scan — the longitudinal direction is **unobservable** from geometry. The scan
matcher's cost function is a flat valley along the corridor axis: the optimizer happily
reports any longitudinal offset, and typically pins the robot in place while it physically
moves. Symptoms: the map shows a corridor shorter than reality ("corridor compression"),
the pose freezes then jumps when the robot reaches a door or corner, AMCL particles smear
into a cigar shape along the corridor.

Mathematically: the scan-match Hessian becomes near-singular — its smallest eigenvalue
(eigenvector pointing along the corridor) approaches zero. Good systems detect this
degeneracy (Zhang & Singh's eigenvalue check) and fall back to odometry along the degenerate
direction. slam_toolbox and AMCL do **not** do this explicitly, so you engineer around it:

**Fixes, in order of effectiveness:**

1. **Better odometry is the real fix.** In a degenerate direction the system is dead-reckoning
   whether you like it or not — make the dead reckoning good. Fuse wheel odom + IMU yaw in
   `robot_localization` (EKF) and feed THAT to SLAM/AMCL. Calibrate wheel diameter and track
   width (drive a measured 10 m straight and a measured 5 full rotations; correct the params
   until reported = actual). This alone fixes most corridor sites.
2. **Lower AMCL's translational noise along-track trust correctly:** counterintuitively,
   REDUCE alpha3 (trans-from-trans noise) if odometry is good — particles then don't spread
   along the corridor faster than odometry error actually grows. Pair with
   `resample_interval: 2` and `max_beams: 100+` so the few longitudinal features
   (door frames, extinguisher boxes) that DO exist actually contribute weight.
3. **Add longitudinal features to the world.** Cheapest reliable fix on real deployments:
   reflective tape strips, posts, bins, or open a few door recesses along the corridor every
   8–10 m. One protruding feature per lidar range-window breaks the degeneracy completely.
   Sites will accept this when you explain the alternative is a lost robot.
4. **Range matters:** a 30 m lidar in a 60 m corridor sees both ends never; a corridor shorter
   than the lidar range is not degenerate (the end caps constrain it). Sometimes the fix is
   buying the 30 m lidar instead of the 10 m one.
5. **Map in the good direction:** during mapping, traverse corridors starting from a
   feature-rich area, and close loops through cross-corridors rather than down-and-back in
   the same corridor (down-and-back gives loop closure no new information in the degenerate
   axis).
6. **Add a non-geometric sensor:** UWB beacons or AprilTags every ~15 m fused via
   robot_localization give absolute longitudinal fixes. Standard for >100 m warehouse aisles.

The same degeneracy analysis applies to: large open spaces beyond lidar range (everything
unobservable — add features or use VSLAM on the ceiling), and circular rooms (rotation
unobservable).

---

## 9. Mapping Procedure That Produces Good Maps

Operator procedure matters as much as config. Bad driving makes bad maps.

1. Verify TF tree first: `map → odom → base_footprint → laser`. Static transforms for sensor
   mounts must be measured, not guessed — a 2 cm lidar offset error puts a 2 cm systematic
   error on every wall, and a 1° lidar yaw error skews the whole map.
2. Verify odometry quality BEFORE mapping: drive a square, check `/odom` returns near start.
   If odom is off by >5% over 20 m, fix that first — SLAM cannot fully save bad odometry.
3. Drive slowly: **< 0.5 m/s translation, < 0.5 rad/s rotation.** Fast rotation is the #1
   operator error — scan distortion and matcher failure both scale with angular rate.
4. Close loops early and often. Don't map the whole building then return — drive small loops,
   confirm each closes (watch the map in rviz for the "snap"), then extend.
5. End where you started, with one final loop closure.
6. Save BOTH formats (§5). Inspect the .pgm: walls should be 1–2 px thick. Thick/double
   walls = drift or bad extrinsics; fix and remap rather than shipping a smeared map.
7. Post-process the .pgm in an image editor if needed: close door gaps you don't want robots
   to plan through, white-out artifacts from people walking by. This is normal practice.

---

## 10. Debugging Methodology

Work the chain in order — each stage assumes the previous one is healthy:

```
sensor data → TF/extrinsics → odometry → scan matching → loop closure → map → localization
```

**Stage checks:**

- **Sensor:** `ros2 topic hz /scan` matches spec; rviz the scan — flat walls should be flat
  lines. Curved walls = lidar intrinsics; missing sectors = occlusion by robot body
  (mask with `laser_filters` angular bounds, don't ignore — self-hits poison maps).
- **TF:** `ros2 run tf2_tools view_frames`. Exactly one publisher per transform.
  Two publishers of `map→odom` (e.g., AMCL and slam_toolbox both running) causes the classic
  flickering-robot-in-rviz symptom.
- **Odometry:** rviz with fixed frame `odom`, drive a loop, measure return error. Also check
  timestamps: odometry/scan timestamps in the future or >100 ms stale cause TF extrapolation
  errors that present as random localization jumps. NTP/PTP-sync multi-machine setups.
- **Scan matching:** in mapping, watch for walls doubling immediately (not just after loops)
  — that's frame-to-frame matching failure: robot too fast, range too short, or
  `correlation_search_space_dimension` smaller than per-update odom error.
- **Loop closure:** map feathers after revisits → closures not firing (raise
  `loop_search_maximum_distance`). Map suddenly folds → false closure (raise
  `loop_match_minimum_response_fine`, raise `loop_match_minimum_chain_size`).
- **Localization:** log AMCL covariance over a full shift. Divergence correlated with a map
  location = environment changed there or degenerate geometry (§8). Divergence correlated
  with robot speed = update gating or odom noise model.

**Always record a bag** during mapping: `ros2 bag record /scan /odom /tf /tf_static /imu`.
SLAM tuning is then offline and repeatable (`use_sim_time:=true`, play the bag) instead of
re-driving the site for every parameter change. This is the single highest-leverage habit.

**Evaluation:** for quantitative work use `evo` (`pip install evo`) — ATE/RPE against ground
truth or between runs. For production sites without ground truth: measure 5–10 known
distances on the real floor with a tape measure and compare against the map. >2% scale error
usually means wheel diameter calibration, not SLAM.

---

## 11. Production Checklist

- [ ] Odometry validated: <2% translation error, <1°/m rotation, IMU fused via EKF
- [ ] Lidar extrinsics measured and verified (flat wall test)
- [ ] Map driven slowly, loops closed incrementally, both .pgm/.yaml and .posegraph archived
- [ ] Walls 1–2 px thick in saved map; known distances within 2%
- [ ] AMCL alphas tuned to measured odometry quality, not defaults
- [ ] recovery_alpha_slow/fast nonzero (kidnapped-robot recovery enabled)
- [ ] Navigation gated on localization covariance; LOST behavior defined and tested
- [ ] Initial pose source defined (dock pose, tag, or operator) — no "hope AMCL figures it out"
- [ ] Corridors/degenerate zones identified and mitigated (§8) before go-live
- [ ] Bag recording available on demand for field debugging
- [ ] Map update process documented (environment WILL change; plan the remap workflow)
