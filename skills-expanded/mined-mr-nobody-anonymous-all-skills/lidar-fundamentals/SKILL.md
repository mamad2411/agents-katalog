---
name: lidar-fundamentals
description: "Use when working with 2D/3D lidar sensors — selecting hardware, parsing point clouds, correcting motion distortion, downsampling, removing ground planes, or clustering obstacles. Provides expert knowledge on lidar physics, point cloud processing pipelines (PCL/Open3D/ROS2), deskewing with IMU, RANSAC ground removal, Euclidean/DBSCAN clustering, sensor selection from hobby (RPLidar) to professional (Ouster/Hesai), and mounting/FOV planning."
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


# Lidar Fundamentals: From Photons to Obstacle Lists

This skill covers the full pipeline from raw lidar returns to actionable obstacle data:
sensor physics → point cloud structure → motion distortion correction → downsampling →
ground removal → clustering. Every section includes the parameter values that work on real
robots and the failure modes that have killed real deployments.

---

## 1. How Lidar Actually Works (the parts that matter for code)

### Time-of-Flight Basics

Lidar fires a laser pulse and measures round-trip time:

```
range = (c × Δt) / 2          where c = 299,792,458 m/s
```

A 1 ns timing error = 15 cm range error. This is why lidar range accuracy is typically
±1–3 cm — it is fundamentally a timing precision problem.

Two ranging methods you will encounter:

| Method | How | Typical use | Gotcha |
|---|---|---|---|
| Pulsed ToF | Direct timing of pulse | Most 3D lidars (Ouster, Velodyne, Hesai) | Multiple returns possible per pulse |
| Triangulation | Laser dot + camera offset | Cheap 2D units (RPLidar A1) | Accuracy degrades quadratically with range |

**Triangulation accuracy degrades with range²** — an RPLidar A1 is ±1 cm at 1 m but can be
±5 cm or worse at 8 m. Never assume datasheet "best case" accuracy holds at max range.

### Multiple Returns

A single laser pulse can hit a chain-link fence AND the wall behind it. Pro lidars report
"strongest", "last", or "dual" returns:

- **Strongest return**: best for solid obstacles; vegetation/fences absorb you into noise.
- **Last return**: penetrates foliage — standard for ground mapping/forestry.
- **Dual return**: both; doubles bandwidth. Use for safety-critical detection where a fence
  AND what's behind it both matter.

Configure this on the sensor (e.g., Ouster `udp_profile_lidar`, Velodyne return mode). If
your obstacle detector misses chain-link fences, you are probably in last-return mode.

### Intensity / Reflectivity

Each point carries an intensity value (raw photon count) or calibrated reflectivity (0–255,
range-compensated on Ouster). Uses:

- **Lane markings / retroreflective tape**: reflectivity > 200 on Ouster's calibrated scale.
  Retroreflectors saturate the detector and can cause **blooming** — phantom points around
  the reflector. Filter points with max intensity AND anomalous range.
- **Calibration targets**: checkerboard-equivalent for lidar-camera extrinsics.
- **Black objects fail**: matte black car paint (~5% reflectivity) cuts effective range by
  50–70%. A lidar rated "120 m @ 80% reflectivity" may see a black car at only 40 m. Always
  check the **10% reflectivity range** spec — that is the honest number.

### Wavelength: 905 nm vs 1550 nm

- **905 nm** (most sensors): silicon detectors, cheap, but eye-safety limits peak power →
  shorter range. Affected by sunlight (solar spectrum strong at 905 nm).
- **1550 nm** (Aeva, some Luminar): eye-safe at 40× higher power → longer range, but
  InGaAs detectors cost more, and **1550 nm is absorbed by water** — rain/fog hurt more.

### Weather Failure Modes (memorize these)

- **Rain**: each drop is a tiny retroreflector. Expect noise points in a cone in front of
  the sensor, 0.5–3 m range. Filter: drop points with low intensity AND range < 4 m, or use
  the sensor's built-in rain filtering (Ouster signal/noise field).
- **Fog**: attenuates beam exponentially. Dense fog can cut range to < 20 m. No software fix.
- **Snow**: worst case — large, highly reflective particles. Dedicated filters exist
  (DROR — Dynamic Radius Outlier Removal — designed exactly for this).
- **Exhaust/steam plumes**: appear as solid obstacles. A robot that hard-brakes for steam
  vents is a real, common deployment failure. Mitigate with temporal persistence checks
  (obstacle must persist N frames) and intensity thresholds (steam returns are weak).
- **Direct sun into the aperture**: blinds 905 nm sensors momentarily. Mount with slight
  downward pitch where possible.

---

## 2. Sensor Taxonomy and Selection

### 2D vs 3D

- **2D lidar**: single scan plane. Sufficient for planar indoor navigation (AMRs, vacuum
  robots, ROS2 nav2 with slam_toolbox). Fails on overhanging obstacles (table edges hit the
  robot's body above the scan plane) and ramps/holes.
- **3D lidar**: multiple beams (rings) or 2D-steered beam. Required for outdoor, uneven
  terrain, anything with overhangs.

### Mechanical Spinning vs Solid-State

| Type | Examples | Pattern | Pros | Cons |
|---|---|---|---|---|
| Mechanical spinning | Ouster OS1, Velodyne, Hesai Pandar/XT | Fixed rings, 360° | Mature, full surround | Moving parts, vibration sensitivity, taller |
| MEMS mirror | Hesai FT120, RoboSense M1 | Raster within FOV wedge | No large moving parts, cheap | Limited FOV (~120°×25°), need multiple units for surround |
| Rotating prism (Risley) | Livox Mid-360, Avia | **Non-repetitive rosette** | Cheap, dense coverage over time | Pattern is NOT rings — ring-based code breaks; instantaneous frame is sparse |
| Flash | Some Ouster/Ibeo automotive | Whole scene at once | True global shutter, no motion distortion | Short range, niche |
| OPA (optical phased array) | Research/early product | Arbitrary steering | No moving parts at all | Not yet production-mature |

**Critical for code generation**: Livox sensors do NOT produce ring-organized clouds. Any
algorithm that iterates "per ring" (classic LOAM feature extraction, ring-based ground
segmentation) must be replaced with range-image or fully unorganized variants. Check the
sensor type before generating ring-dependent code.

### Selection Ladder (2026 street prices, approximate)

| Tier | Sensor | Type | Specs | Price | Use |
|---|---|---|---|---|---|
| Hobby | RPLidar A1M8 | 2D triangulation | 12 m, 8 kHz, 5.5 Hz scan | ~$100 | Indoor SLAM learning, slow robots |
| Hobby+ | RPLidar S2/S3 | 2D ToF | 30–40 m, 32 kHz | ~$350–500 | Faster indoor AMRs, light outdoor |
| Budget 3D | Livox Mid-360 | Prism, non-repetitive | 360°×59°, 40 m @10%, ~200k pts/s | ~$750 | Indoor/outdoor SLAM on a budget — exceptional value; mind the non-ring pattern |
| Budget 3D | Unitree L1/L2 | Spinning | 30 m, dense | ~$350–500 | Legged robots, hobby 3D |
| Mid | Hesai XT16/XT32 | Spinning, 16/32 ring | 120 m, ±1 cm | ~$3–5k | Commercial AMRs, delivery robots |
| Pro | Ouster OS1-64/128 | Spinning, digital | 120 m @10%, calibrated reflectivity, near-IR ambient channel | ~$8–18k | AVs, mapping, research |
| Pro long-range | Ouster OS2, Hesai AT128 | Spinning / MEMS | 200–400 m | $10k+ | Highway-speed AVs |

Decision heuristics:

- Indoor, flat floor, < 1.5 m/s → 2D lidar + nav2 is sufficient and far cheaper.
- Any outdoor or non-flat operation → 3D, minimum 16 rings or Mid-360 equivalent.
- Required detection range: `range ≥ v² / (2·a_brake) + v·t_react + margin`.
  Example: 2 m/s robot, 1 m/s² braking, 0.3 s pipeline latency →
  2²/2 + 2×0.3 + 1 m margin = **3.6 m minimum**, at 10% reflectivity, on the worst-case
  (smallest, darkest) obstacle you must detect.
- **Vertical resolution at distance**: angular spacing between rings determines if you see a
  small obstacle. OS1-32 has ~1.05° spacing → at 10 m, rings are 18 cm apart vertically. A
  10 cm curb at 10 m may fall entirely between rings. This is the #1 reason robots hit
  curbs: do the trigonometry — `gap = range × tan(ring_spacing)` — before selecting a sensor.

---

## 3. Point Cloud Structure

### Organized vs Unorganized

- **Organized**: 2D grid (H rings × W azimuth steps), like an image. Neighbor lookup is O(1)
  array indexing. Ouster and Velodyne can produce these. `PointCloud2.height > 1`.
- **Unorganized**: flat list, `height == 1`. Neighbor lookup requires a KD-tree (O(log n)).
  Livox and most post-filtered clouds are unorganized.

Prefer keeping clouds organized as long as possible — range-image algorithms (fast ground
segmentation, depth clustering) are 10–50× faster than KD-tree equivalents.

### ROS2 PointCloud2 — parsing correctly

`sensor_msgs/msg/PointCloud2` is a binary blob with a field schema. Common fields:

```
x, y, z      : float32 (meters, sensor frame)
intensity    : float32 or uint8/uint16 — CHECK datatype, varies by driver
ring         : uint16 (beam index; absent on Livox)
t / time     : uint32 ns since frame start (Ouster) or float64 absolute (others)
range        : uint32 mm (Ouster)
```

```python
# Correct, fast parsing in ROS2 (Humble+) — do NOT iterate point-by-point in Python
import numpy as np
from sensor_msgs_py import point_cloud2

def cloud_to_numpy(msg):
    # structured array view, zero-copy where alignment allows
    pts = point_cloud2.read_points_numpy(
        msg, field_names=("x", "y", "z", "intensity"), reshape_organized_cloud=False
    )
    # Remove NaNs (no-return points) — ALWAYS do this first
    mask = np.isfinite(pts).all(axis=1)
    return pts[mask]
```

**Failure modes that produce garbage downstream:**

1. **NaN points**: no-return directions are encoded as NaN (or 0,0,0 on some drivers).
   A KD-tree built over NaNs crashes or hangs PCL. Filter first, always.
2. **Zero points at origin**: some drivers emit (0,0,0) for no-return. These cluster into a
   phantom obstacle at the sensor. Filter `range < min_range` (e.g., 0.5 m) explicitly.
3. **Endianness/datatype mismatch**: reading `intensity` as float32 when the driver packs
   uint16 gives garbage. Parse the `fields[]` schema, never hardcode offsets.
4. **`is_dense=false` ignored**: means NaNs are present. Respect it.

### Per-Point Timestamps

For deskewing (Section 4) you need each point's capture time. Conventions differ:

- **Ouster**: `t` field, nanoseconds relative to the frame's header stamp.
- **Velodyne**: `time` field, seconds (float32) relative offset.
- **Livox**: `timestamp` field, absolute nanoseconds.
- **Header stamp meaning varies**: frame START (Ouster default) vs frame END. Get this wrong
  and your deskew shifts everything by one frame period — a 0.1 s error at 1 m/s smears the
  world by 10 cm. Verify against the driver docs for YOUR driver version.

---

## 4. Motion Distortion Correction (Deskewing)

### The Problem, Quantified

A spinning lidar takes 100 ms (at 10 Hz) to complete one revolution. If the robot moves
during the sweep, points captured at the start and end of the frame are in different robot
poses, but the cloud pretends they are simultaneous.

- Translation error: `v × T_scan`. At 2 m/s and 10 Hz: **20 cm smear**. At highway 30 m/s:
  3 m — walls become diagonal smears.
- Rotation error: `ω × T_scan`. At 90°/s yaw and 10 Hz: **9° smear** — a straight wall
  becomes an arc; scan matching diverges; obstacles smear into free space.

**Rule: deskew whenever `v·T_scan > voxel_size` or `ω·T_scan > 1°`.** For any robot moving
faster than ~0.3 m/s or turning at all, that means always.

### The Algorithm

For each point with timestamp `t_i` in frame captured over `[t_start, t_end]`:

1. Estimate the sensor pose `T(t_i)` at the point's capture time (from IMU integration or
   odometry interpolation).
2. Transform the point into a common frame (convention: the pose at `t_end`, so the cloud
   represents the world "as of frame end"):

```
p_corrected = T(t_end)⁻¹ · T(t_i) · p_i
```

### IMU-Based Deskew (the standard approach)

IMU at 200–400 Hz gives angular velocity and linear acceleration. Within one 100 ms frame:

- **Rotation**: integrate gyro. Gyro bias drift over 100 ms is negligible (~0.005° for a
  consumer MEMS gyro with 50°/h bias instability) — rotation deskew from raw gyro is safe.
- **Translation**: double-integrating accelerometer over 100 ms is acceptable ONLY if you
  have a good gravity estimate and velocity initial condition (from your odometry/EKF).
  Otherwise use wheel/visual odometry velocity and assume constant velocity over the frame.

```python
import numpy as np
from scipy.spatial.transform import Rotation, Slerp
from scipy.interpolate import interp1d

def deskew(points_xyz, point_times, imu_times, imu_quats, odom_vel_body):
    """
    points_xyz : (N,3) sensor-frame points
    point_times: (N,) absolute capture time per point [s]
    imu_times  : (M,) IMU sample times spanning the frame [s]
    imu_quats  : (M,4) orientation (xyzw) from gyro integration, in a fixed frame
    odom_vel_body: (3,) body-frame linear velocity (assumed constant over frame)
    Returns points expressed in the sensor pose at frame END.
    """
    t_end = point_times.max()

    # Interpolate rotation at each point time (SLERP), position by constant velocity
    slerp = Slerp(imu_times, Rotation.from_quat(imu_quats))
    R_t = slerp(np.clip(point_times, imu_times[0], imu_times[-1]))
    R_end = slerp([np.clip(t_end, imu_times[0], imu_times[-1])])[0]

    dt = point_times - t_end                      # negative: earlier points
    trans = odom_vel_body[None, :] * dt[:, None]  # displacement rel. to end pose

    # p_end = R_end^T * (R_t * p + trans_world)   (rotations in fixed frame)
    p_world = R_t.apply(points_xyz) + R_end.apply(trans)
    return R_end.inv().apply(p_world)
```

Production notes:

- **Time sync is everything.** IMU and lidar must share a clock to < 1 ms. Use PTP
  (IEEE 1588) on Ouster/Hesai, or hardware PPS. NTP (~ms jitter) is marginal; "host receive
  time" stamping is NOT acceptable — USB/network jitter is 1–10 ms, and at 90°/s that is up
  to 0.9° of error, which defeats the purpose.
- **Extrinsics first**: rotate IMU measurements into the lidar frame using the calibrated
  `T_lidar_imu` before integrating. A 2° extrinsic rotation error leaks into every deskewed
  frame.
- In C++ production code, this lives inside your LIO pipeline — FAST-LIO2, LIO-SAM, and
  KISS-ICP all deskew internally. If you run one of those, do not deskew twice.
- Solid-state flash lidars and cameras-like global-shutter units need no deskew; Livox
  prism units DO (they sweep continuously).

### Verifying Deskew Works

Drive the robot in a tight circle around a cylindrical pillar at max angular rate. Without
deskew the pillar smears into a banana in single frames; with correct deskew it stays a
crisp circle. This 5-minute test catches sign errors, frame-start/end confusion, and time
sync failures — run it on every new platform.

---

## 5. Voxel Downsampling

Raw clouds (Ouster OS1-128 @ 10 Hz = 2.6 M pts/s) overwhelm downstream processing.
Voxel-grid filtering replaces all points in each cubic cell with their centroid.

### Choosing voxel size

| Use case | Voxel size | Rationale |
|---|---|---|
| Obstacle detection (indoor AMR) | 0.05 m | Must keep 10 cm objects ≥ 2–3 points |
| Obstacle detection (outdoor) | 0.10 m | Range noise ~±3 cm makes finer voxels pointless |
| SLAM / scan matching | 0.25–0.5 m | KISS-ICP default 1.0 m for odometry; map voxel 0.25 |
| Visualization | 0.20 m | Eyes can't use more |

The voxel size sets your minimum detectable obstacle: an object smaller than ~2× voxel size
may reduce to a single point and be discarded by clustering's `min_points`. **Work backward
from your smallest must-detect obstacle.**

```python
# Open3D — production-quality, fast
import open3d as o3d
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)
down = pcd.voxel_down_sample(voxel_size=0.10)
```

```cpp
// PCL
pcl::VoxelGrid<pcl::PointXYZI> vg;
vg.setInputCloud(cloud);
vg.setLeafSize(0.10f, 0.10f, 0.10f);
vg.filter(*cloud_down);
// FAILURE MODE: if cloud extent / leaf_size overflows int32 indices, PCL silently
// produces garbage ("Leaf size is too small" warning). Crop to an ROI box FIRST.
```

**Order of operations matters:**

```
raw → NaN/zero filter → range crop (ROI box, e.g. ±30 m, z ∈ [-2, 3]) →
deskew → voxel downsample → ground removal → clustering
```

Crop BEFORE voxelizing (avoids the PCL overflow bug and wasted work). Deskew BEFORE
voxelizing (voxelizing a smeared cloud bakes the distortion in permanently).

Also know `RadiusOutlierRemoval` / `StatisticalOutlierRemoval` for sparse noise (rain,
dust): SOR with `mean_k=20, std_dev=2.0` is the standard starting point, but it costs a
KD-tree build — skip it indoors where there is no weather noise.

---

## 6. Ground Plane Removal

Ground points dominate the cloud (often 60–80% of points for a ground robot) and must be
removed before clustering, or every obstacle merges into one giant ground-connected blob.

### RANSAC Plane Fitting (the baseline)

Model: plane `ax + by + cz + d = 0`. RANSAC repeatedly samples 3 points, fits a plane,
counts inliers within `distance_threshold`, keeps the best.

Iterations needed: `k = log(1-p) / log(1-w³)` for success probability `p` and inlier
fraction `w`. With w=0.6 (60% ground) and p=0.999: k ≈ 30. Use 100+ for margin; it's cheap.

```python
import open3d as o3d
plane_model, inlier_idx = pcd.segment_plane(
    distance_threshold=0.10,   # outdoor; 0.03 for smooth indoor floors
    ransac_n=3,
    num_iterations=200,
)
a, b, c, d = plane_model

# CRITICAL VALIDATION — never skip:
import numpy as np
normal = np.array([a, b, c])
up = np.array([0, 0, 1])                      # base_link z-up; transform cloud first
tilt = np.degrees(np.arccos(abs(normal @ up) / np.linalg.norm(normal)))
if tilt > 15.0:
    # RANSAC latched onto a WALL, not the ground. Reject; reuse last good plane.
    ...
ground = pcd.select_by_index(inlier_idx)
obstacles = pcd.select_by_index(inlier_idx, invert=True)
```

**RANSAC failure modes (these kill robots):**

1. **Wall capture**: in a corridor, a wall can have more inliers than the floor. The "ground
   filter" then deletes the wall and keeps the floor as an "obstacle". ALWAYS validate the
   plane normal against gravity (±15°) and the plane height against the known sensor height
   (`|d|` should ≈ sensor mounting height when normal ≈ z).
2. **Single-plane assumption**: ramps, curbs, and sloped terrain are not one plane. A plane
   fit on flat ground extended to 30 m will either delete an uphill ramp (it pokes above the
   plane → "obstacle", robot refuses to climb its own ramp) or swallow low obstacles.
3. **Threshold too tight on grass/gravel**: outdoor ground has ±10 cm texture. A 3 cm
   threshold leaves a carpet of "obstacle" points; clustering then hallucinates obstacles
   everywhere.

### Better-than-RANSAC for real terrain

- **Multi-region RANSAC / Patchwork++**: split the cloud into concentric polar sectors, fit
  a plane per sector, enforce continuity between sectors. Patchwork++ (open source,
  `url-kaist/patchwork-plusplus`) is the current go-to for outdoor ground segmentation —
  use it instead of writing your own for anything beyond flat floors.
- **Ring-based / range-image methods**: walk outward along each ring; ground points have a
  small inter-ring slope (`Δz/Δr < tan(slope_max)`, slope_max ≈ 10–15°). Extremely fast
  (no KD-tree), but requires ring structure — not for Livox.
- **Simple z-threshold** (`z < z_ground + 0.15` in base_link) is acceptable ONLY for flat
  indoor floors with a well-calibrated sensor height. It fails the moment the robot pitches
  on a ramp — gate it with IMU pitch/roll if you must use it.

**Two-sided obstacle definition**: obstacles are points above the ground AND below the
robot's height + clearance. Don't waste clustering time on tree canopies 5 m up — crop
`z ∈ (ground + 0.05, robot_height + 0.3)` for the obstacle channel. Keep a separate channel
for negative obstacles: a hole has NO returns where ground should be — absence of expected
ground points within the polar grid is itself a hazard signal that pure clustering will
never produce.

---

## 7. Clustering for Obstacle Extraction

After ground removal, group remaining points into discrete objects.

### Euclidean Cluster Extraction (PCL standard)

Region growing over a KD-tree: points within `cluster_tolerance` of each other join the
same cluster.

```cpp
pcl::search::KdTree<pcl::PointXYZI>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZI>);
tree->setInputCloud(cloud_no_ground);

std::vector<pcl::PointIndices> clusters;
pcl::EuclideanClusterExtraction<pcl::PointXYZI> ec;
ec.setClusterTolerance(0.35);   // see table below
ec.setMinClusterSize(5);        // rejects rain/dust singletons
ec.setMaxClusterSize(25000);    // rejects "everything merged" failure
ec.setSearchMethod(tree);
ec.setInputCloud(cloud_no_ground);
ec.extract(clusters);
```

### DBSCAN

Adds a density requirement: a core point needs `min_samples` neighbors within `eps`. Better
than pure Euclidean at rejecting sparse noise (rain) while keeping dense clusters. Open3D:

```python
labels = np.array(pcd.cluster_dbscan(eps=0.35, min_points=8, print_progress=False))
# labels == -1 are noise; this built-in noise rejection is DBSCAN's main win
```

### Parameter selection — the part everyone gets wrong

`cluster_tolerance` / `eps` must exceed the point spacing AT YOUR DETECTION RANGE, which
grows linearly with distance:

```
horizontal spacing = range × (2π / points_per_ring)
e.g. Ouster 1024-mode: at 10 m → 6 cm;  at 30 m → 18 cm
vertical spacing    = range × tan(ring_angular_spacing)
e.g. OS1-32 (1.05°): at 10 m → 18 cm;  at 30 m → 55 cm  ← usually the binding constraint
```

| Scenario | tolerance/eps | min_points | Notes |
|---|---|---|---|
| Indoor AMR, ≤ 10 m, 16-ring | 0.25 m | 10 | |
| Outdoor, ≤ 30 m, 32-ring | 0.45 m | 5 | Vertical spacing dominates |
| Outdoor, ≤ 30 m, 128-ring | 0.30 m | 15 | |
| 2D lidar (single ring) | 0.15 m | 3 | Cluster in 2D |

Failure modes:

1. **Tolerance < vertical ring spacing at range** → a pedestrian at 25 m splits into 3
   horizontal slices, each below `min_points`, each discarded. **The robot is blind to
   distant pedestrians while passing all close-range tests.** This is the single most
   dangerous clustering bug. Fix: range-adaptive tolerance, or cluster in a polar/range
   image where neighbor relations don't depend on metric spacing (depth_clustering by
   Bogoslavskyi & Stachniss — O(N), no KD-tree, handles this correctly).
2. **Tolerance too large** → two pedestrians walking together merge into one cluster; a
   pedestrian near a wall merges into the wall. Trackers then report one object where two
   exist — fatal for prediction.
3. **min_points too high** → small/distant obstacles vanish. min_points too low → every
   rain droplet pair becomes an obstacle and the planner freezes ("phantom braking").
4. **No max size cap** → if ground removal failed this frame, the entire cloud is one
   cluster. Cap it and treat a giant cluster as a ground-removal failure alarm, not an
   obstacle.

### From clusters to obstacles

For each cluster compute: centroid, axis-aligned or oriented bounding box (PCA on xy for
orientation), min/max z, point count. Then sanity-filter:

```python
# typical gates for a ground robot
keep = (0.1 < bbox_height < 2.5) and (bbox_xy_area < 25.0) and (n_points >= min_pts)
```

Feed surviving boxes to tracking (e.g., AB3DMOT-style: 3D IoU/Mahalanobis association +
per-object Kalman filter). **Never feed raw single-frame clusters to a planner** — require
M-of-N frame persistence (e.g., 2 of 3) to suppress rain/dust/steam phantoms, and accept
the one-frame latency cost in your braking-distance budget.

---

## 8. Mounting and FOV Planning

### Geometry you must compute before drilling holes

1. **Self-occlusion**: anything on the robot inside the FOV creates a permanent blind cone
   AND near-range reflections (a glossy chassis panel can mirror the beam and create phantom
   underground points). Mast-mount above the chassis, or accept and mask the blind sector
   explicitly in software (`angle_min/angle_max` crop — do it in the driver config, e.g.
   Ouster azimuth window, so you don't pay bandwidth for masked points).
2. **Minimum range blind ring**: sensors have 0.3–1 m minimum range. A sensor at 0.5 m
   height with a 22.5° down-FOV first sees the ground at `0.5 / tan(22.5°) ≈ 1.2 m`.
   Everything closer and lower is invisible. **A toddler-height obstacle adjacent to the
   robot can be entirely inside this blind ring.** Cover it with sonar/depth cameras or a
   low-mounted 2D lidar, or constrain motion (no blind-side maneuvers).
3. **Mounting height trade-off**:
   - Higher → sees over obstacles, smaller blind ring relative to FOV, better for mapping.
   - Lower → denser rings on nearby ground (better small-obstacle detection), but blinded
     by the first obstacle row.
   - Standard AMR compromise: 3D lidar on a mast at 0.6–1.2 m, tilted 0–10° down.
4. **Ground coverage math**: ring i at depression angle θᵢ from height h hits ground at
   `r = h / tan(θᵢ)`. Tabulate this for your sensor's beam table. If consecutive ground
   intersections are > your obstacle size apart, you have detection gaps at that range.
5. **Tilt for coverage shaping**: pitching the sensor down 10–15° trades rear/upper FOV for
   dense forward ground coverage — right call for a forward-driving delivery robot, wrong
   for omnidirectional AMRs.

### 2D lidar mounting specifics

- Scan plane height picks what you detect: 15–20 cm catches most clutter but misses
  tabletops that the robot body will strike. If robot height > scan height, you WILL hit
  overhangs — add a depth camera or tilted second lidar.
- Mount dead level: a 2° tilt puts the beam into the floor at `h/tan(2°)` ≈ 5–8 m,
  creating a phantom wall. Shim and verify with a long-corridor scan.

### Vibration, EMI, and the boring stuff that causes 3 a.m. pages

- Mechanical spinning lidars are gyroscopes: hard-mounting to a vibrating chassis induces
  precession torques and shortens bearing life. Use the manufacturer's damping mounts.
- Run PTP over a dedicated switch or direct link; lidar UDP floods (Ouster OS1-128 ≈
  250 Mbps) can starve other traffic on a shared 1 GbE link — check switch buffer drops if
  you see frame gaps.
- IP rating: "IP67 sensor" does not cover the connector. Most field water ingress is at
  improperly torqued M12 connectors.
- Multi-lidar interference: two sensors of the same model can read each other's pulses.
  Modern sensors (Ouster, Hesai) have interference mitigation / phase-locking — enable
  phase lock and offset the phases (e.g., 0° and 180°) when mounting two units.
- **Extrinsic calibration**: lidar→base_link matters more than people think — a 1° pitch
  error makes the ground plane appear tilted, breaking z-threshold ground removal at range
  (1° over 20 m = 35 cm). Calibrate by fitting the ground plane on known-flat ground and
  solving the rotation that maps its normal to +z; verify roll with a wall scan.

---

## 9. Reference Pipeline (ROS2)

Standard obstacle-detection node graph:

```
/ouster/points (PointCloud2, sensor frame, 10 Hz)
  → [driver: dual return? azimuth window? PTP locked?]
  → crop_box (ROI ±30 m, z ∈ [-2, 3], remove robot footprint box)
  → deskew (IMU + odom; or inside FAST-LIO2 if running LIO)
  → voxel_grid (0.10 m)
  → patchwork++ ground segmentation  →  /ground, /nonground
  → euclidean clustering (range-adaptive tolerance) on /nonground
  → bbox + gates → /detections (vision_msgs/Detection3DArray)
  → M-of-N persistence / tracker → planner costmap
```

Latency budget at 10 Hz: the whole chain must finish in < 100 ms to avoid frame drops.
Typical numbers on a modern embedded CPU (e.g., Orin) for a 128-beam cloud: crop+voxel
5 ms, Patchwork++ 15 ms, clustering 10–30 ms (KD-tree dominates — this is why range-image
clustering matters at scale).

Tools to reach for instead of writing from scratch:

- **PCL** (C++): filters, RANSAC, Euclidean clustering — battle-tested, verbose.
- **Open3D** (Python/C++): cleaner API, good for prototyping; `segment_plane`,
  `cluster_dbscan`, `voxel_down_sample`.
- **Patchwork++**: ground segmentation that actually works outdoors.
- **KISS-ICP / FAST-LIO2 / LIO-SAM**: odometry/SLAM with built-in deskewing.
- **ros2 pointcloud_to_laserscan**: flatten 3D → 2D scan for nav2 costmaps.
- **RViz2 + `ros2 bag record`**: always record raw sensor + IMU + TF when field testing;
  every bug in this domain is debugged from bags.

### Debugging methodology (in order)

1. **Look at the raw cloud in RViz first.** Color by intensity, then by ring, then by time.
   80% of "algorithm bugs" are actually driver config, TF, or time-sync problems visible by
   eye.
2. Check TF tree (`ros2 run tf2_tools view_frames`): wrong/missing `lidar→base_link` causes
   tilted ground and is the most common new-platform failure.
3. Verify time sync: `ros2 topic echo --field header.stamp` on lidar and IMU; plot offset.
   Ouster: confirm `timestamp_mode: TIME_FROM_PTP_1588` and PTP lock status.
4. Pillar-circle test for deskew (Section 4).
5. Log and alert on pipeline health counters in production: ground-plane tilt angle,
   inlier fraction, cluster count, max cluster size, per-stage latency. A sudden ground
   inlier-fraction drop means rain, a tarp on the sensor, or a failed plane fit — your
   robot should slow down, not plow on.
