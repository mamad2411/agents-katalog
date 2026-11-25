---
name: perception-lidar
description: 2D and 3D lidar on ROS 2 Jazzy - rplidar_ros, urg_node, sick_scan_xd, velodyne, ouster_ros, nebula and Livox drivers,
  LaserScan/PointCloud2 QoS and frames, laser_filters, pcl_ros CropBox/VoxelGrid, ground removal and clustering nodes (NumPy, PCL),
  pointcloud_to_laserscan, lidar-camera and lidar-lidar extrinsics, octomap_server, PCD files, RViz, Foxglove, CloudCompare.
license: Apache-2.0
metadata:
  sources: [robotics-agent-skills]
  evidence: researched
  last_verified: 2026-11-23
---

# Lidar and point clouds

Lets an agent bring up a 2D or 3D lidar, mount it correctly in TF, clean and convert its data, write
a point-cloud node, calibrate it against a camera and build maps from it. Written for ROS 2 Jazzy
from the sources of perception_pcl 2.6.5, laser_filters 2.0.10, pointcloud_to_laserscan 2.0.2,
octomap_server 2.3.1 and each driver; the recipes were not run. Distro differences are at the end.

## When to use

- Choosing, installing or starting a lidar driver; a scan or cloud topic is silent or shows nothing
  in RViz.
- Adding the lidar to the URDF, or the data appears rotated, mirrored, offset or smeared.
- Removing the robot's own body, far points, noise or the floor from scans or clouds.
- Turning a 3D cloud into a LaserScan for 2D tools, or a scan into a cloud.
- Writing a node that reads or publishes `PointCloud2` (NumPy or PCL), such as obstacle clustering.
- Calibrating a lidar against a camera or a second lidar.
- Building an OctoMap or occupancy grid from clouds, saving PCD files, inspecting clouds offline.

Elsewhere: camera drivers, intrinsics and image processing in
[perception-camera](../perception-camera/SKILL.md); SLAM, lidar odometry, deskewing and state
estimation in [perception-slam](../perception-slam/SKILL.md); the sensor link and frames in
[ros2-robot-description](../ros2-robot-description/SKILL.md); simulated lidars in
[sim-gazebo](../sim-gazebo/SKILL.md); QoS and launch basics in [ros2-core](../ros2-core/SKILL.md);
costmaps fed by lidar in `nav-nav2`.

## Quick start

```bash
sudo apt install ros-jazzy-rplidar-ros ros-jazzy-laser-filters ros-jazzy-pcl-ros \
  ros-jazzy-pointcloud-to-laserscan ros-jazzy-octomap-server ros-jazzy-octomap-rviz-plugins
sudo usermod -aG dialout $USER                      # serial lidars; log out and back in
ros2 run rplidar_ros rplidar_composition --ros-args -p serial_port:=/dev/ttyUSB0 \
  -p serial_baudrate:=115200 -p frame_id:=lidar_link -p angle_compensate:=true
ros2 topic hz /scan
ros2 topic echo --once --no-arr /scan               # header, angles and limits without the arrays
```

A 3D lidar, for example an Ouster: `sudo apt install ros-jazzy-ouster-ros`, then
`ros2 launch ouster_ros sensor.launch.xml sensor_hostname:=<hostname or IP>` and
`ros2 topic hz /ouster/points`. In RViz set the Fixed Frame to the lidar's frame (or `base_link` once
the URDF has it), add a LaserScan or PointCloud2 display and set its Reliability Policy to
`Best Effort` if the driver publishes best effort. Other sensors: [references/drivers.md](references/drivers.md).

## Workflow

1. **Pick and start the driver.** Use the Jazzy binary where one exists and note what it publishes:
   topic, `frame_id`, QoS, and for clouds the point fields. Network lidars need the host on the
   sensor's subnet; serial ones a stable device path. Per-sensor commands, defaults and source
   builds (newer RPLIDARs, Livox, Hesai's own driver): [references/drivers.md](references/drivers.md).
   *Check:* `ros2 topic hz` shows the sensor's rate; `ros2 topic info -v <topic>` shows its QoS;
   `ros2 topic echo --once --field header.frame_id <topic>` names the frame you expect.

2. **Mount it in the URDF.** A fixed joint from `base_link` to the lidar link, with the origin at
   the sensor's measurement origin from its datasheet and x forward (REP 103); the link pattern is in
   [ros2-robot-description](../ros2-robot-description/references/sensors-control-display.md). Make
   the driver's `frame_id` equal the link name, or name the link after the driver's frame. Drivers
   that publish their own internal TF (Ouster: `os_sensor` → `os_lidar`, `os_imu`) get a URDF that
   stops at their root frame. Model an upside-down or tilted mount in the joint's `rpy`; do not
   also flip the data in the driver.
   *Check:* `ros2 run tf2_ros tf2_echo base_link <lidar_frame>` matches the drawing; in RViz with
   Fixed Frame `base_footprint`, the floor lies at z = 0, walls stand vertical, and an object placed
   in front of the robot appears on +x.

3. **Get the time right.** Stamps must be on the robot's clock: use the driver's ROS-time or PTP
   mode (Ouster `timestamp_mode: TIME_FROM_ROS_TIME` or `TIME_FROM_PTP_1588`), and `use_sim_time`
   everywhere when replaying a bag with `--clock`.
   *Check:* `ros2 topic delay <topic>` is small and steady, never seconds or negative; no
   "extrapolation into the future" from TF users.

4. **Know the messages.** `LaserScan`: `ranges` from `angle_min` in steps of `angle_increment`,
   valid only inside `range_min`..`range_max`; by REP 117, `+inf` means no return, `-inf` too close,
   NaN an invalid reading. `PointCloud2`: `height` > 1 means organized (rows and columns kept, NaN
   for missing points, `is_dense` false); `fields` lists each channel's name, offset and type, and
   these differ by driver (`ring`, `time` vs `t`, `timestamp`, `reflectivity`).
   *Check:* `ros2 topic echo --once --field fields <cloud>` lists the fields your code reads, with
   the types it expects.

5. **Clean 2D scans with `laser_filters`.** One `scan_to_scan_filter_chain` with a range filter,
   a box or footprint filter for hits on the robot, and a speckle or shadow filter for edge noise;
   YAML and launch in [references/filters.md](references/filters.md).
   *Check:* `/scan_filtered` publishes at the scan rate, and RViz shows no points on the robot's
   footprint and no veils behind object edges.

6. **Crop and thin 3D clouds with `pcl_ros`.** A `CropBox` with `input_frame` and `output_frame`
   set to `base_footprint` (surroundings only), a second one with `negative: true` for the robot's
   body, then a `VoxelGrid` with `filter_field_name: ''`, all in one component container
   ([references/filters.md](references/filters.md)). Defaults to override: VoxelGrid keeps only
   0 ≤ z ≤ 1 m, drops single-point voxels, and caps `leaf_size` at 1 m; StatisticalOutlierRemoval's
   `mean_k: 2, stddev: 0` removes much of any cloud. Filters subscribe only while their output has a
   subscriber.
   *Check:* `ros2 topic hz` on the output (which also starts the chain); in RViz the output keeps
   the scene and loses the robot's body and the far clutter.

7. **Remove the ground and find obstacles.** `pcl_ros` on Jazzy has no segmentation nodes; write
   one: voxel, fit a level plane only to points near the expected floor height (so a wall cannot
   win), drop points within a tolerance of it, then Euclidean-cluster the rest. Python with NumPy
   and SciPy in [references/python-node.md](references/python-node.md), C++ with PCL in
   [references/cpp-node.md](references/cpp-node.md). For ramps and rough outdoor ground, one plane
   is not enough (Patchwork++ fits patches).
   *Check:* on a scene with known objects, `/obstacles` coloured by Intensity shows one cluster per
   object and no floor points; `ros2 topic hz /obstacles` keeps up with the lidar.

8. **Convert between 3D and 2D.** `pointcloud_to_laserscan_node` slices a height band of a cloud in
   a level `target_frame`; set `min_height` explicitly (its default drops everything at or below
   z = 0). `laserscan_to_pointcloud_node` or `laser_geometry` go the other way
   ([references/filters.md](references/filters.md)).
   *Check:* the LaserScan overlays the cloud's obstacles in RViz at the chosen heights; its
   subscriber accepts best effort.

9. **Calibrate against a camera or a second lidar.** Calibrate camera intrinsics first, then run
   the targetless `direct_visual_lidar_calibration`, convert `T_lidar_camera` into the camera
   joint's `<origin>`, and refine lidar-to-lidar mounts with ICP:
   [references/calibration.md](references/calibration.md).
   *Check:* in an RViz Camera display over the rectified image, lidar points sit on image edges
   near and far; overlapping lidars show one wall, not two, with Decay Time on.

10. **Map from clouds.** With odometry or SLAM publishing `map` (or `odom`) → base, feed the
    filtered cloud to `octomap_server`; it produces the octree, markers and a 2D `projected_map`.
    Save with `octomap_saver_node`. Maps without a pose source are SLAM:
    [perception-slam](../perception-slam/SKILL.md). Details in
    [references/mapping-viz.md](references/mapping-viz.md).
    *Check:* the octree in RViz is sharp (no doubled walls) after driving a loop;
    `my_map.bt` reloads with `octomap_server_node -p octomap_path:=my_map.bt`.

11. **Record and inspect.** `ros2 bag record` the lidar topics with `/tf` and `/tf_static`; save
    PCDs with `pointcloud_to_pcd` or `combined_pointcloud_to_pcd`; check range, floor tilt and
    calibration in CloudCompare; view remotely in Foxglove ([references/mapping-viz.md](references/mapping-viz.md)).
    *Check:* the bag replays with TF intact, and a PCD opens with the coordinates in the frame you
    saved it in.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `ros2 topic hz` works, RViz or a node shows nothing | Best-effort publisher, reliable subscriber (RViz's default) | Display Reliability `Best Effort`; subscribe with `qos_profile_sensor_data` / `SensorDataQoS` |
| RViz "No transform from [laser] to [base_link]" | Driver `frame_id` (`laser`, `velodyne`, `os_lidar`, `livox_frame`, `hesai`) not in the URDF | Set the driver's frame to the link name, or name the link after it |
| Two parents for one frame, TF jumps | URDF and driver both publish the lidar's internal frames | URDF stops at the driver's root frame (`os_sensor`), or `pub_static_tf: false` |
| Scan mirrored or rotated 180° | Mount not modelled, or modelled and also flipped in the driver | Real mount in the joint `rpy`; driver flip flags off |
| Cloud smears when the robot turns (Decay Time on, fixed frame `odom`) | Wrong lidar yaw in the URDF, or stamps off the robot's clock | Fix the extrinsic; check `ros2 topic delay`; ROS-time or PTP stamps |
| VoxelGrid output keeps only a slab near the floor | `filter_field_name` defaults to `z` with limits 0..1 m | `filter_field_name: ''` or real limits |
| Sparse far points vanish after VoxelGrid | `min_points_per_voxel` defaults to 2 | Set it to 1 |
| pcl_ros filter output back in the sensor frame | `input_frame` set, `output_frame` empty | Set both |
| pcl_ros filter never subscribes to its input | Lazy subscription: no one listens to `output` | Expected; subscribe to the output to start it |
| `pointcloud_to_laserscan` scan empty or missing low obstacles | `min_height` default is about 2e-308, so z ≤ 0 is dropped; or `target_frame` tilted | Set `min_height`; use a level `target_frame` |
| Ground removal eats a wall, or keeps the floor on a slope | Unconstrained RANSAC plane, or one plane for uneven ground | Fit a level plane to a near-floor band; patch-wise ground (Patchwork++) |
| NumPy code crashes on NaN, or clusters near the origin | Organized cloud with NaN points | `skip_nans=True` plus an `isfinite` mask; `removeNaNFromPointCloud` |
| Python node lags behind the lidar | Per-point loops or `struct.pack` | `read_points_numpy` / `create_cloud`; voxel first; C++ for big clouds |
| `ros2 launch urg_node urg_node_launch.py` fails | Its launch file uses the removed `node_executable` argument | `ros2 run urg_node urg_node_driver --ros-args --params-file ...` |
| RPLIDAR C1, S2, S3 or T1 does not start with the apt package | Jazzy binary has SDK 1.12 | Build Slamtec's `rplidar_ros` `ros2` branch |
| Missing wedges in a 3D cloud, `hz` below the sensor rate | UDP packets dropped | Wired link, larger receive buffers, no other traffic on the NIC |
| Clouds stutter on another machine | Large messages over Wi-Fi or DDS fragmentation | Process on the robot; send a cropped or `point_cloud_transport`-compressed topic |
| `octomap_server` inserts nothing | No TF from `frame_id` to the cloud frame at the cloud's stamp | Run odometry or SLAM first; match `frame_id` to it |
| Open3D import fails or ROS messages stop importing in a venv | No Ubuntu 24.04 package; NumPy 2 pulled in | pip in a `--system-site-packages` venv, keep NumPy 1.26 ([python-node.md](references/python-node.md)) |

## Checks

Before reporting the lidar working:

- `ros2 topic hz` at the sensor's rate and `ros2 topic delay` small and steady on every lidar topic.
- `header.frame_id` exists in TF; `tf2_echo base_link <lidar_frame>` matches the mount drawing.
- RViz with Fixed Frame `base_footprint`: floor at z = 0, walls vertical, a known object at its
  measured position (within the sensor's datasheet accuracy).
- With Decay Time on and the robot rotating in place in `odom`, static walls stay one line thick.
- Each filter stage's output has the expected rate, frame and content; nothing on the robot body.
- Point fields your code reads appear in `ros2 topic echo --once --field fields`.
- For calibration: overlay on the rectified image aligned near and far; `tf2_echo` matches the
  calibration result.
- For maps: the saved `.bt` reloads; `projected_map` matches the room.

## Distro differences

- **Lyrical**: `pcl_conversions` exports `pcl_conversions::pcl_conversions` and
  `ament_target_dependencies` is deprecated ([cpp-node.md](references/cpp-node.md));
  `pcl_ros` adds `bag_to_pcd` (`bag_path`, `topic_name`, `output_directory`);
  `pointcloud_to_laserscan` 2.1 subscribes without waiting for a subscriber. No Lyrical binaries
  yet for `nebula`, `rslidar_sdk` or `grid_map`; `ouster_ros` is 0.14.2 there. PCL is 1.15 on
  Ubuntu 26.04.
- **Humble**: `pcl_ros` 2.4.5 has the filters and `pcd_to_pointcloud` only (no `pointcloud_to_pcd`,
  no lazy subscription); laser_filters 2.0.9 lacks `wrap_angle` and `LaserScanBinningFilter`.
- Livox's `build.sh` takes `humble` or `jazzy`; Lyrical is not listed.

## Related

- References: [drivers.md](references/drivers.md), [filters.md](references/filters.md),
  [python-node.md](references/python-node.md), [cpp-node.md](references/cpp-node.md),
  [calibration.md](references/calibration.md), [mapping-viz.md](references/mapping-viz.md).
- Wiki: [PCL](../../wiki/software/pcl.md), [Open3D](../../wiki/software/open3d.md),
  [OctoMap](../../wiki/software/octomap.md), [tf2](../../wiki/software/tf2.md),
  [URDF](../../wiki/software/urdf.md), [CloudCompare](../../wiki/tools/cloudcompare.md),
  [Foxglove](../../wiki/tools/foxglove.md), [ROS 2](../../wiki/tools/ros2.md),
  [Choose a SLAM system](../../wiki/guides/choose-a-slam-system.md),
  [KITTI](../../wiki/learning/datasets/kitti.md).
- Skills: [perception-camera](../perception-camera/SKILL.md),
  [perception-slam](../perception-slam/SKILL.md) (lidar odometry in its
  [lidar-odometry.md](../perception-slam/references/lidar-odometry.md)),
  [ros2-robot-description](../ros2-robot-description/SKILL.md), [ros2-core](../ros2-core/SKILL.md),
  [sim-gazebo](../sim-gazebo/SKILL.md); later `nav-nav2`, `ops-bringup`, the sensor calibration
  playbook (Phase 6).
- Upstream: the `perception_pcl`, `laser_filters`, `pointcloud_to_laserscan`, `octomap_mapping` and
  driver repos on their Jazzy branches; REP 103, 105 and 117; pointclouds.org and open3d.org docs.
