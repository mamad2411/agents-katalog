---
name: perception-slam
description: Localize and map a ROS 2 robot - robot_localization EKF/UKF on the odom and map frames (REP 105), navsat_transform
  GPS, IMU conventions and imu_tools filters, slam_toolbox 2D mapping, saving and localization, RTAB-Map RGB-D/lidar SLAM,
  KISS-ICP, LIO-SAM, RKO-LIO and OpenVINS odometry, Kalibr camera-IMU calibration, bags for SLAM, evo APE/RPE on TUM/KITTI.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-23
---

# Localization and SLAM

Lets an agent give a robot a smooth `odom` frame and a drift-corrected `map` frame: fuse odometry, IMU and
GPS, build and reuse maps, add lidar or visual-inertial odometry, and measure the drift. Written for ROS 2
Jazzy from the Jazzy branches of robot_localization 3.8, slam_toolbox 2.8, rtabmap_ros 0.23 and imu_tools
2.1 and the upstream repos of the others; the recipes were not run. Lyrical and Humble differences are at
the end.

## When to use

- Fusing wheel odometry, an IMU and GPS with `robot_localization` (one or two filters, `navsat_transform_node`).
- Bringing up an IMU for localization: axes, signs, gravity, covariances, an orientation filter.
- Building a 2D map with slam_toolbox, saving it, extending it, localizing in it.
- RGB-D, stereo or 3D-lidar SLAM with RTAB-Map; lidar or lidar-inertial odometry; visual-inertial odometry
  and the Kalibr calibration it needs.
- Recording bags to tune localization offline, and measuring drift with evo.
- Debugging: the robot jumps in RViz, walls double, scans are dropped, the estimate creeps at rest.

Elsewhere: camera drivers and image topics in [perception-camera](../perception-camera/SKILL.md); lidar
drivers and point clouds in [perception-lidar](../perception-lidar/SKILL.md); sensor links in the URDF in
[ros2-robot-description](../ros2-robot-description/SKILL.md); simulated IMU, lidar and GPS in
[sim-gazebo](../sim-gazebo/SKILL.md); `diff_drive_controller` odometry in
[ros2-control](../ros2-control/SKILL.md); navigation on the map in `nav-nav2`.

## Pick the stack

| Sensors | Start with | Jazzy install | Note |
|---|---|---|---|
| Wheel odometry + IMU (+ GPS outdoors) | robot_localization | `ros-jazzy-robot-localization` | Always the `odom` layer |
| 2D lidar + odometry, indoors | slam_toolbox | `ros-jazzy-slam-toolbox` | LGPL-2.1; bundled Karto LGPL-3.0+ |
| RGB-D or stereo camera, optional lidar | RTAB-Map | `ros-jazzy-rtabmap-ros` | BSD |
| 3D lidar | KISS-ICP, + RTAB-Map for loops | source build | MIT |
| 3D lidar + IMU | RKO-LIO, or LIO-SAM | `ros-jazzy-rko-lio`; LIO-SAM source, tested to Humble | MIT; BSD-3-Clause |
| Camera + IMU, no wheels | OpenVINS | source build, tested to Humble | **GPL-3.0** |

Cartographer also has Jazzy binaries; ORB-SLAM3 and VINS-Fusion are GPL-3.0 and ROS 1-era. Trade-offs and
the full comparison: [choose a SLAM system](../../wiki/guides/choose-a-slam-system.md).

## Quick start

Wheel odometry + IMU into the local EKF, then a 2D map:

```bash
sudo apt install ros-jazzy-robot-localization ros-jazzy-slam-toolbox ros-jazzy-nav2-map-server \
  ros-jazzy-imu-complementary-filter
source /opt/ros/jazzy/setup.bash
# my_robot_localization: config/ekf.yaml and launch/ekf.launch.py from references/robot-localization.md
ros2 launch my_robot_localization ekf.launch.py
ros2 run tf2_ros tf2_echo odom base_link            # follows the robot smoothly
# config/slam_toolbox_mapping.yaml and launch/slam.launch.py from references/slam-toolbox.md
ros2 launch my_robot_localization slam.launch.py
ros2 run tf2_ros tf2_echo map odom                   # published, changes in steps at loop closures
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph \
  "{filename: '/home/<user>/maps/my_map'}"
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "{name: {data: '/home/<user>/maps/my_map'}}"
```

## Workflow

1. **Decide who owns each TF edge** (REP 105). `map` → `odom` → `base_link`, one publisher per edge:
   `odom` → `base_link` from the local EKF (or the lidar/visual odometry, or the drive controller when
   there is no EKF), `map` → `odom` from SLAM, localization or the global EKF. Turn the others off:
   `enable_odom_tf: false` in `diff_drive_controller`, `publish_tf: false` in the EKF that does not own an
   edge or in `imu_filter_madgwick`, KISS-ICP's own TF, LIO-SAM's static `map` → `odom`. Sensor frames come
   from the URDF.
   *Check:* `ros2 run tf2_tools view_frames` shows one tree `map` → `odom` → `base_link` → sensors, and
   `ros2 topic info -v /tf` lists only the publishers you planned.

2. **Make the inputs correct before fusing them.** Odometry: twist in `child_frame_id` (`base_link`),
   non-zero covariances, REP 103 signs (forward is +vx, counter-clockwise is +vyaw). IMU:
   [imu.md](references/imu.md). GPS: `NavSatFix` with covariance and fix status.
   *Check:* driving forward raises `odom` x; turning left raises yaw and gives `angular_velocity.z` > 0;
   at rest the IMU reads about +9.81 on z.

3. **Set up the IMU.** `imu_link` in the URDF with the real mount rotation; ENU orientation; an
   orientation filter if the driver gives none (`imu_complementary_filter`, BSD; `imu_filter_madgwick` is
   GPL-3.0-or-later and publishes TF by default); `orientation_stddev` set. Indoors fuse the yaw rate, not a
   magnetometer heading. Details: [imu.md](references/imu.md).
   *Check:* the bring-up table in imu.md passes; `tf2_echo base_link imu_link` shows the mount.

4. **Local filter** (`world_frame: odom`). Fuse velocities from the wheels (vx, vy, vyaw), the IMU's vyaw
   (roll and pitch in 3D, acceleration only after the gravity test), `two_d_mode: true` on flat floors.
   Never fuse GPS here. YAML and launch: [robot-localization.md](references/robot-localization.md).
   *Check:* rotate 360° in place and drive a square: `odometry/filtered` returns close to where it started
   and the TF is smooth; `/diagnostics` (with `print_diagnostics: true`) shows no warnings.

5. **Global layer.** Indoors: SLAM or map localization owns `map` → `odom` (steps 6, 7). Outdoors: a second
   EKF in `map` fuses the same raw inputs plus `odometry/gps` from `navsat_transform_node`, which needs an
   earth-referenced IMU heading (0 facing east) or a datum.
   *Check:* `odometry/gps` traces the driven path without rotation; `map` → `odom` comes from one node.

6. **2D SLAM with slam_toolbox.** Copy the upstream parameter file, set `base_frame`, `scan_topic` and
   `max_laser_range`, launch with `use_sim_time:=false` (the Jazzy launch files default to `true`). Drive
   slowly and close loops. Save both the pose graph (`serialize_map`) and the image (`save_map`), then
   localize with `localization_launch.py` and `map_file_name`. Details:
   [slam-toolbox.md](references/slam-toolbox.md).
   *Check:* no `Message Filter dropping message` lines; walls stay single after a loop; reloading the map
   puts the robot where it is.

7. **RGB-D, stereo or lidar SLAM with RTAB-Map.** Sync the camera with `rgbd_sync`, set `frame_id`, use the
   EKF as `odom` when the robot has wheels, and pass RTAB-Map parameters as strings. `-d` starts a new
   database (`~/.ros/rtabmap.db`), which is written on shutdown. Launch file, parameters and services:
   [rtabmap.md](references/rtabmap.md).
   *Check:* `info` shows loop closures after revisiting a place; the grid stays sharp; a restart with
   `localization:=true` localizes.

8. **Lidar or lidar-inertial odometry** for robots without good wheel odometry: KISS-ICP, RKO-LIO or
   LIO-SAM. Decide first whether it owns `odom` or feeds the EKF (`_differential: true`). LIO needs
   IMU-to-lidar extrinsics and per-point time. Details: [lidar-odometry.md](references/lidar-odometry.md).
   *Check:* a closed loop ends near its start; no creep at rest; walls stay thin while turning.

9. **Visual-inertial odometry.** Calibrate the camera, the IMU noise (Allan variance) and the camera-IMU
   extrinsic and time offset with Kalibr (ROS 1, in Docker, on converted bags), then run OpenVINS with
   Kalibr's files and fuse its output into the local EKF. Check the GPL-3.0 licence first.
   Details: [vio-calibration.md](references/vio-calibration.md).
   *Check:* reprojection error below about 0.2-0.5 px and IMU errors inside 3 sigma in the Kalibr report
   (OpenVINS guide); a measured straight walk gives the right distance.

10. **Record, replay, measure.** Record raw inputs with `/tf_static` while only drivers and odometry run;
    replay with `--clock` and `use_sim_time: true`; compute APE and RPE with evo against ground truth or a
    reference run. Details: [bags-evaluation.md](references/bags-evaluation.md).
    *Check:* replaying the same bag twice with the same parameters gives the same evo numbers; each number
    is stored with its command, bag and parameter files.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Robot jumps or flickers between two poses in RViz | Two publishers of `odom` → `base_link` (controller, EKF, lidar odometry, Madgwick TF) | One owner; `ros2 topic info -v /tf` |
| Yaw oscillates or drifts against the wheels | Two absolute yaw sources with understated covariance | Fuse one; `_differential: true` or the rate for the other |
| Estimate creeps at rest | IMU acceleration fused with wrong gravity handling, frame or sign | Stop fusing ax until the imu.md tests pass |
| Filter ignores an input; `Could not transform measurement into ...` | Sensor `frame_id` not in TF | Fix the URDF or the driver's frame id |
| One input dominates | Zero variance (the filter adds only 1e-6) or inflated covariances elsewhere | Real covariances; switch values off in `_config` |
| `odom` pose jumps outdoors | GPS fused in the `odom` filter | GPS only in the `map` filter |
| navsat_transform publishes nothing | `imu` or `odometry/filtered` not remapped, or no fix | Remap all three inputs; `ros2 topic echo --once /gps/fix` |
| GPS track rotated against the map | `yaw_offset` or declination wrong; the IMU does not read 0 facing east | Measure heading facing east; set `yaw_offset` |
| `imu_link` has two parents | `imu_filter_madgwick` default `publish_tf: true` | `publish_tf: false` |
| slam_toolbox: no map, `Message Filter dropping message` | Odom TF missing or late, wrong `base_frame`, or `use_sim_time` true on a real robot | Fix TF; `use_sim_time:=false` |
| Doubled or bent walls | Bad odometry (wheel radius, separation, slip) or a wrong lidar mount rotation | Calibrate odometry; check the lidar joint; `HuberLoss` |
| `save_map` fails | `nav2_map_server` not installed, or `~`/spaces in the path | Install it; absolute path |
| RTAB-Map: `Did not receive data since 5 seconds!` | Topic missing, QoS mismatch, or exact sync on unsynced topics | Check topics; `qos` argument; `approx_sync: true` |
| RTAB-Map map gone after restart | Node killed before shutdown, or `-d` still set | Clean shutdown or `backup` service; drop `-d` |
| Nodes stall or TF extrapolation errors on bag replay | No `--clock`, or a node without `use_sim_time` | `ros2 bag play --clock`; sim time everywhere |
| KISS-ICP silent on the live robot | Its launch defaults to `use_sim_time:=true` | Pass `use_sim_time:=false` |
| LIO drifts, jumps up and down, or zigzags | Wrong IMU extrinsics, 6-axis IMU for LIO-SAM, or unsynchronized stamps | Fix `extrinsicRot`/`extrinsicRPY`; 9-axis IMU; hardware sync |
| LIO-SAM deleted a folder | Its save code runs `rm -r` on the target directory | Dedicated empty directory |
| VIO scale wrong or diverges | Bad camera-IMU extrinsic, time offset or noise values | Redo Kalibr; inflate noise; check stamps |

## Checks

Before reporting localization or a map done:

- `view_frames` shows one tree; every TF edge has exactly the planned publisher.
- Each input topic arrives at its rate with the expected `frame_id`, signs and non-zero covariances.
- The local estimate is smooth and returns near the start after a loop; `/diagnostics` is clean.
- `map` → `odom` changes only in small steps; walls are single after loop closures.
- Saved maps reload: slam_toolbox `.posegraph`/`.data` and `.pgm`/`.yaml`, or the RTAB-Map database.
- APE and RPE from evo are recorded with the command, bag and parameter files; "looks fine in RViz" is not a
  result.

## Distro differences

- **Lyrical** (robot_localization 3.11): `ekf_node` and `ukf_node` are lifecycle nodes and start
  unconfigured; launch them as `LifecycleNode(..., autostart=True)` or use the package launch files.
- **Lyrical** (rosbag2 0.33): `ros2 bag record` no longer takes topics as positional arguments; use
  `--topics` (Jazzy accepts both, with a deprecation warning for positional).
- **Humble:** slam_toolbox 2.6 runs plain nodes (no lifecycle, no `autostart`); `ros2 bag record` takes
  positional topics only and writes SQLite by default; `ros2 bag play` has no `--exclude-topics`;
  `LifecycleNode` in launch has no `autostart`.
- No distro has KISS-ICP, LIO-SAM or OpenVINS in rosdistro; LIO-SAM and OpenVINS are tested upstream up to
  Humble only. Kalibr is ROS 1 on every distro.

## Related

- References: [robot-localization.md](references/robot-localization.md), [imu.md](references/imu.md),
  [slam-toolbox.md](references/slam-toolbox.md), [rtabmap.md](references/rtabmap.md),
  [lidar-odometry.md](references/lidar-odometry.md), [vio-calibration.md](references/vio-calibration.md),
  [bags-evaluation.md](references/bags-evaluation.md).
- Wiki: [robot_localization](../../wiki/software/robot-localization.md),
  [slam_toolbox](../../wiki/software/slam-toolbox.md), [RTAB-Map](../../wiki/software/rtab-map.md),
  [Cartographer](../../wiki/software/cartographer.md), [KISS-ICP](../../wiki/software/kiss-icp.md),
  [LIO-SAM](../../wiki/software/lio-sam.md), [GTSAM](../../wiki/software/gtsam.md),
  [OpenVINS](../../wiki/software/openvins.md), [ORB-SLAM3](../../wiki/software/orb-slam3.md),
  [VINS-Fusion](../../wiki/software/vins-fusion.md), [Kalibr](../../wiki/software/kalibr.md),
  [tf2](../../wiki/software/tf2.md), [choose a SLAM system](../../wiki/guides/choose-a-slam-system.md),
  [KITTI](../../wiki/learning/datasets/kitti.md), [TUM RGB-D](../../wiki/learning/datasets/tum-rgbd.md),
  [PlotJuggler](../../wiki/tools/plotjuggler.md), [Foxglove](../../wiki/tools/foxglove.md),
  [Rerun](../../wiki/tools/rerun.md).
- Skills: [perception-camera](../perception-camera/SKILL.md), [perception-lidar](../perception-lidar/SKILL.md),
  [ros2-robot-description](../ros2-robot-description/SKILL.md), [ros2-control](../ros2-control/SKILL.md),
  [ros2-core](../ros2-core/SKILL.md), [sim-gazebo](../sim-gazebo/SKILL.md),
  [ops-docker-ci](../ops-docker-ci/SKILL.md); later `nav-nav2`, `ops-bringup`, the sensor calibration
  playbook (Phase 6).
- Upstream: REP 103, REP 105, REP 145; robot_localization docs (`jazzy-devel`); slam_toolbox README
  (`jazzy`); `rtabmap_slam/doc/rtabmap.md` (`jazzy-devel`); the OpenVINS calibration guide; the Kalibr wiki;
  the rosbag2 README (`jazzy`); evo README and wiki.
