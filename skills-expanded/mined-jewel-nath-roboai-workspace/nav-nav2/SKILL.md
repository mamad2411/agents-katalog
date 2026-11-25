---
name: nav-nav2
description: Bring up Nav2 on a ROS 2 Jazzy mobile robot - TF, odom, scan and cmd_vel prerequisites, nav2_bringup launch,
  nav2_params.yaml (footprint, frames, static/obstacle/voxel/inflation layers, AMCL, map_server, velocity_smoother,
  collision_monitor), lifecycle manager, goals via RViz, CLI and nav2_simple_commander, waypoints, keepout/speed zones, docking, BT XML.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-24
---

# Nav2 bring-up

Lets an agent take a mobile robot whose TF, odometry and sensors already work and make it navigate on a map with
Nav2: configure, launch, localize, send goals, add zones, dock, and debug. Written for ROS 2 Jazzy against
navigation2 1.3.14 (`jazzy` branch and binary) and the docs.nav2.org source; the recipes were not run.
Planners and controllers stay on Nav2's defaults here. Lyrical and Humble differences are at the end.

## When to use

- Writing `my_robot_navigation`: the parameter file, the launch file, maps and behavior trees.
- Setting the robot's shape, frames, topics and costmap layers; localizing with AMCL or slam_toolbox.
- Sending goals and waypoints from RViz, the command line or a Python script.
- Adding keepout or speed zones, the collision monitor, the velocity smoother, or automatic docking.
- Changing what the robot does on failure (behavior tree XML); testing Nav2 in Gazebo.
- Debugging: Nav2 never becomes active, the robot does not move, ignores obstacles or stops for nothing.

Elsewhere: choosing and tuning planners, controllers and smoothers, writing their plugins, coverage and
standalone path planning in [nav-planning](../nav-planning/SKILL.md); building and saving maps,
robot_localization and slam_toolbox details in [perception-slam](../perception-slam/SKILL.md); URDF and frames in
[ros2-robot-description](../ros2-robot-description/SKILL.md); the drive controller in
[ros2-control](../ros2-control/SKILL.md); scan and cloud filtering in [perception-lidar](../perception-lidar/SKILL.md).

## What Nav2 needs first

| Input | Usually from | Read by |
|---|---|---|
| TF `odom` → `base_link` (or `base_footprint`), smooth | `diff_drive_controller`, a local EKF, or firmware | every server |
| `nav_msgs/Odometry` on `/odom`, twist in the base frame | the same source | `bt_navigator`, `controller_server`, `velocity_smoother` (`odom_topic`) |
| TF `base_link` → `lidar_link` and other sensors | `robot_state_publisher` | costmaps, AMCL, collision monitor |
| `LaserScan` on `/scan`, and/or `PointCloud2` | the driver, filtered | costmaps, AMCL, collision monitor |
| A map and TF `map` → `odom` | `map_server` + AMCL, or slam_toolbox | global costmap, `bt_navigator` |
| A base that moves on `/cmd_vel` | `diff_drive_controller`, Gazebo DiffDrive, firmware | end of the command chain |

## Quick start

```bash
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup   # also pulls slam_toolbox and the TB3/TB4 sims
source /opt/ros/jazzy/setup.bash
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False   # Gazebo Harmonic + AMCL + RViz
# In RViz: "2D Pose Estimate" where the robot stands, then "Nav2 Goal"
```

For your robot, build `my_robot_navigation` from [references/launch.md](references/launch.md) and
[references/params.md](references/params.md), then:

```bash
ros2 launch my_robot_navigation navigation.launch.py map:=/home/<user>/maps/my_map.yaml
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: map}, pose: {position: {x: 1.0, y: 0.5}, orientation: {w: 1.0}}}}" --feedback
```

## Workflow

1. **Prove the inputs before Nav2.** Every row of the table above must hold with Nav2 off.
   *Check:* `ros2 run tf2_tools view_frames` shows `odom` → `base_link` → sensors with one publisher per edge;
   teleop 1 m forward raises `odom` x by about 1 m; the `/scan` `frame_id` exists in TF.

2. **Make the package.** `my_robot_navigation` holds `config/nav2_params.yaml` (copied from the Jazzy
   `nav2_bringup/params/nav2_params.yaml`, then edited), `maps/`, `behavior_trees/` and a launch file that
   includes `nav2_bringup`'s `bringup_launch.py`. Keep every section of the copied file: Jazzy's
   `navigation_launch.py` also starts `route_server` and `docking_server`, and the docking server will not
   configure without `dock_plugins`. Layout and launch file: [references/launch.md](references/launch.md).
   *Check:* `colcon build` installs `config/`, `maps/`, `launch/`; `ros2 node list` shows every node of the
   bringup table in launch.md, with no parameter or plugin errors in the log.

3. **Frames, topics and shape.** Set `robot_base_frame`, AMCL `base_frame_id` and collision monitor
   `base_frame_id` to frames your URDF has (Jazzy's file mixes `base_link` and `base_footprint`). Point every
   scan source at your topic. Give both costmaps `footprint` (polygon in the base frame) or `robot_radius`
   (default 0.1 m). Costmap parameters must sit under `local_costmap: local_costmap: ros__parameters:` (and the
   same for global); a single level is silently ignored. Tables: [references/params.md](references/params.md).
   *Check:* `ros2 param get /local_costmap/local_costmap footprint` returns your polygon; RViz shows
   `/local_costmap/published_footprint` around the robot.

4. **Costmap layers.** Global: `static_layer`, `obstacle_layer`, `inflation_layer`. Local, rolling in `odom`:
   `voxel_layer` (or `obstacle_layer` for one planar lidar) and `inflation_layer`. For each source set
   `max_obstacle_height` (the per-source default is 0.0, which drops every point above the floor),
   `clearing: true`, and `raytrace_max_range` above `obstacle_max_range`. Inflate wide: an
   `inflation_radius` well beyond the robot's inscribed radius with a gentle `cost_scaling_factor`.
   *Check:* an object placed in front of the robot appears in both costmaps and clears when removed.

5. **Localization.** On a saved map: `map_server` + AMCL (`bringup_launch.py map:=...`); give the initial pose
   (RViz, `/initialpose`, or `set_initial_pose: true` with `initial_pose`). While mapping: `slam:=True`
   runs slam_toolbox (LGPL-2.1). slam_toolbox in localization mode: start it from
   [perception-slam](../perception-slam/references/slam-toolbox.md) and launch with `use_localization:=False`.
   Only one node may publish `map` → `odom`.
   *Check:* the particle cloud converges after a short drive; `tf2_echo map odom` changes only in small steps.

6. **The command chain.** `controller_server` and `behavior_server` publish `cmd_vel_nav` →
   `velocity_smoother` → `cmd_vel_smoothed` → `collision_monitor` → `/cmd_vel`. Set the smoother's
   `max_velocity`, `min_velocity`, `max_accel`, `max_decel` to what the base can do and keep the controller
   plugin's limits at or below them. Jazzy's Nav2 sends `Twist`; Jazzy's `diff_drive_controller` takes only
   `TwistStamped`, so set `enable_stamped_cmd_vel: true` on `controller_server`, `behavior_server`,
   `velocity_smoother`, `collision_monitor` and `docking_server`, and remap the controller's `~/cmd_vel` to
   `/cmd_vel` ([ros2-control](../ros2-control/SKILL.md)). Collision monitor polygons:
   [references/params.md](references/params.md).
   *Check:* `ros2 topic info -v /cmd_vel` shows one type on both sides; a goal moves the robot; a box placed
   in the stop polygon halts it.

7. **Bring it up.** `autostart: true` lets each lifecycle manager configure and activate its nodes in order;
   if one node fails, the manager stops bringing up its group. The global costmap waits
   `initial_transform_timeout` (60 s) for `map` → `base_link`, so set the initial pose within a minute or
   bringup fails. `bringup_launch.py` composes all nodes into one `component_container_isolated` by default;
   `use_composition:=False use_respawn:=True` gives separate, restartable processes.
   *Check:* `lifecycle_manager_localization` and `lifecycle_manager_navigation` log `Managed nodes are active`;
   `ros2 lifecycle get /bt_navigator` is `active [3]`.

8. **Send goals.** RViz "Nav2 Goal" (action) or "2D Goal Pose" (`/goal_pose` topic), the action CLI, or
   `nav2_simple_commander`'s `BasicNavigator`. Waypoints with a stop at each: `FollowWaypoints`; one smooth
   pass through several poses: `NavigateThroughPoses`. Commands and a script:
   [references/goals-waypoints.md](references/goals-waypoints.md).
   *Check:* the action result is `SUCCEEDED` and the robot stops within the goal checker tolerances
   (0.25 m, 0.25 rad in the Jazzy file).

9. **Zones.** Keepout and preferred lanes (`KeepoutFilter`) and speed limits (`SpeedFilter`) come from
   painted mask images served by a second `map_server` and a `costmap_filter_info_server`; Jazzy's
   `nav2_bringup` does not start them. Masks, YAML and launch: [references/costmap-filters.md](references/costmap-filters.md).
   *Check:* planned paths avoid the keepout area; `/speed_limit` publishes when the robot enters a zone.

10. **Docking.** `opennav_docking` (Apache-2.0, released for Jazzy, already in `navigation_launch.py`):
    a dock plugin, a dock database, a detected dock pose and battery state. Setup:
    [references/docking.md](references/docking.md).
    *Check:* `dock_robot` succeeds from the staging pose and from across the room.

11. **Behavior trees.** Pick a shipped tree or write one, set `default_nav_to_pose_bt_xml`, or pass a tree per
    goal. XML, nodes, and Groot 2 (proprietary; monitoring trees over 20 nodes is paid):
    [references/behavior-trees.md](references/behavior-trees.md).
    *Check:* the tree loads without errors at activation, and a blocked path triggers the recoveries you chose.

12. **Test in simulation first.** Gazebo: bring the robot up with [sim-gazebo](../sim-gazebo/SKILL.md),
    then the same Nav2 launch with `use_sim_time:=True`. For behavior and BT tests without physics or
    sensors, `nav2_loopback_sim` fakes odometry and `map` → `odom` (`tb3_loopback_simulation.launch.py`).
    *Check:* the same goal list succeeds in simulation before the robot runs it.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `Failed to bring up all requested nodes. Aborting bringup.` after about a minute; `Timed out waiting for transform from base_link to map` | No `map` → `odom`: no initial pose, AMCL inactive, SLAM not running | Initial pose within 60 s, `set_initial_pose: true`, or raise `initial_transform_timeout` |
| Bringup aborts at `docking_server`: `Charging dock plugins not given!` | A trimmed parameter file without the `docking_server` section | Keep the section with `dock_plugins` |
| Controller runs, robot does not move | `Twist` vs `TwistStamped` mismatch, or the base listens on another topic | `ros2 topic info -v /cmd_vel`; `enable_stamped_cmd_vel` on all five nodes; remap |
| Robot never moves, collision monitor blocks | A configured source is silent or cannot be transformed (watchdog `source_timeout`) | Fix the topic and frame, or remove the source |
| Obstacles missing from costmaps | Per-source `max_obstacle_height` unset (0.0), wrong topic, or range too short | Set heights per source; check the topic; `obstacle_max_range` |
| Ghost obstacles never clear | `clearing` false (the default), raytrace range shorter than marking, lidar no-returns as `inf` | `clearing: true`, `raytrace_max_range` > `obstacle_max_range`, `inf_is_valid: true` |
| Costmap uses defaults (radius 0.1, resolution 0.1) | Single-level `local_costmap: ros__parameters:` or old names | Nest twice; `ros2 param get` the value |
| Old names do nothing | `obstacle_range`, `raytrace_range`, `recovery_server`, `nav2_recoveries`, `default_bt_xml_filename`, `progress_checker_plugin` | `obstacle_max_range`, `raytrace_max_range`, `behavior_server`, `nav2_behaviors`, `default_nav_to_pose_bt_xml`, `progress_checker_plugins` |
| AMCL logs `Waiting for map....` | `map_server` inactive or wrong `map:=` path | Absolute map path; `ros2 lifecycle get /map_server` |
| AMCL or collision monitor cannot transform | `base_frame_id` default `base_footprint`, robot has only `base_link` | Set both to a frame in the URDF |
| Robot jumps between two poses | AMCL and slam_toolbox (or a global EKF) both publish `map` → `odom` | One owner |
| `Sensor origin at (...) is out of map bounds` | Robot pose outside the static map | Correct initial pose; check map `origin` |
| `Goal Coordinates of(...) was outside bounds` or `in lethal cost` | Goal off the map, in a wall or its inflation | Move the goal; planner tolerance in nav-planning |
| `Failed to make progress` | Under 0.5 m moved in 10 s: base not obeying, limits too low, robot stuck | Check the command chain; progress checker values |
| Robot cuts corners or brushes walls | Footprint smaller than the robot, or inflation radius at the inscribed radius | Real footprint; larger `inflation_radius`, lower `cost_scaling_factor` |
| Edited BT XML has no effect | The navigator caches the tree by file name | `always_reload_bt_xml: true`, or restart |
| `navigation_launch.py use_composition:=True` hangs | No container named `nav2_container` | Use `bringup_launch.py`, or start the container |
| Launch dies with `NameError: name 'false' is not defined` | Jazzy bringup evaluates `slam`, `use_localization`, `use_composition` as Python | Pass `True` / `False`, capitalized |
| TF extrapolation errors in Gazebo | A node on wall time, or `/clock` not bridged | `use_sim_time:=True` for Nav2 and RViz; bridge `/clock` |
| Teleop and Nav2 fight over `/cmd_vel` | Two publishers | `twist_mux` with priorities |

## Checks

Before reporting Nav2 working on a robot:

- `view_frames` shows `map` → `odom` → `base_link` → sensors, each edge with the planned publisher.
- Both lifecycle managers report `Managed nodes are active`; no repeating warnings in the log.
- `ros2 param get` confirms the footprint, frames and scan topics on the costmaps, AMCL and collision monitor.
- An obstacle placed and removed in front of the robot appears in, then clears from, both costmaps.
- Ten goals across the map succeed in simulation and on the robot; the stop polygon halts it.
- Zones, docking and custom trees, where used, pass the checks in their reference files.
- The parameter file, map and goal list used for the test are committed with the result.

## Distro differences

- **Lyrical** (Nav2 1.5): `enable_stamped_cmd_vel` defaults to `true` (from Kilted). `NavigateThroughPoses`
  takes `nav_msgs/Goals` (`poses.goals`); `BasicNavigator.goThroughPoses` accepts both forms. Docking's
  `dock_backwards` became the per-dock `dock_direction: forward|backward`. `bt_navigator` uses
  `error_code_name_prefixes` and `bt_search_directories`, and its `goal_blackboard_id`-style parameters move under
  each navigator. `IsPathValid`, `IsStopped` and `IsPoseOccupied` became `ValidatePath`, `CheckStopStatus` and
  `CheckPoseOccupancy`. `action_server_result_timeout` is gone. The costmap-level `map_topic` moved to the static
  layer. `bringup_launch.py` gains `keepout_mask`, `speed_mask` and `graph`, with the filters in its default file.
- **Humble** (Nav2 1.1): BehaviorTree.CPP v3, so XML has no `BTCPP_format="4"`, uses `SequenceStar`, and
  `plugin_lib_names` must list every BT library. Only `Twist` on `cmd_vel`. Docking is the separate
  `opennav_docking` 0.0.2 release with its own messages. Collision monitor `points` is a flat list. The TB3 sim
  runs Gazebo Classic. There is no `initial_transform_timeout`.

## Related

- References: [launch.md](references/launch.md), [params.md](references/params.md),
  [goals-waypoints.md](references/goals-waypoints.md), [costmap-filters.md](references/costmap-filters.md),
  [docking.md](references/docking.md), [behavior-trees.md](references/behavior-trees.md).
- Wiki: [Nav2](../../wiki/software/nav2.md), [BehaviorTree.CPP](../../wiki/software/behaviortree-cpp.md),
  [slam_toolbox](../../wiki/software/slam-toolbox.md), [robot_localization](../../wiki/software/robot-localization.md),
  [tf2](../../wiki/software/tf2.md), [ros2_control](../../wiki/software/ros2-control.md),
  [AprilTag](../../wiki/software/apriltag.md), [linorobot2](../../wiki/software/linorobot2.md),
  [Gazebo](../../wiki/tools/gazebo.md), [Foxglove](../../wiki/tools/foxglove.md),
  [choose a Nav2 planner and controller](../../wiki/guides/choose-a-nav2-planner-and-controller.md),
  [choose a SLAM system](../../wiki/guides/choose-a-slam-system.md).
- Skills: [nav-planning](../nav-planning/SKILL.md), [perception-slam](../perception-slam/SKILL.md),
  [perception-lidar](../perception-lidar/SKILL.md), [perception-camera](../perception-camera/SKILL.md),
  [ros2-core](../ros2-core/SKILL.md), [ros2-robot-description](../ros2-robot-description/SKILL.md),
  [ros2-control](../ros2-control/SKILL.md), [sim-gazebo](../sim-gazebo/SKILL.md),
  [ops-docker-ci](../ops-docker-ci/SKILL.md); later `ops-bringup`, `ops-fleet` (multi-robot, Open-RMF),
  `arch-safety` (safety-rated stops, which the collision monitor is not).
- Upstream: docs.nav2.org (first-time robot setup, configuration guide, tuning guide, tutorials, migration
  guides), the `navigation2` `jazzy` branch (`nav2_bringup`, `nav2_docking/README.md`), REP 103 and REP 105.
