---
name: nav-planning
description: Choose, configure and tune Nav2 global planners (NavFn, Smac 2D, Smac Hybrid-A*, Smac State Lattice, Theta*),
  controllers (MPPI, Regulated Pure Pursuit, DWB, Graceful, Rotation Shim) and smoothers per drive type; write a custom
  nav2_core planner or controller plugin; opennav_coverage paths; prototype A*, Hybrid A*, RRT, RRT* with PythonRobotics.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-24
---

# Nav2 planners, controllers and path planning

Lets an agent pick the planner, controller and smoother plugins Nav2 runs for a robot's drive type, set
and tune their parameters, write its own plugin, plan coverage paths, and try planning algorithms outside
ROS. Written for ROS 2 Jazzy and Nav2 1.3.14 from the `jazzy` sources and docs.nav2.org; the recipes were
not run. Lyrical and Humble differences are at the end.

## When to use

- Choosing plugins for a differential, omnidirectional, Ackermann or legged robot, round or not.
- Editing the `planner_server`, `controller_server` and `smoother_server` blocks of `nav2_params.yaml`.
- Tuning: paths hug walls, the robot wobbles, cuts corners, stops short, will not reverse, spins at the
  goal, or the planner or control loop misses its rate.
- Writing a planner or controller plugin against `nav2_core` with pluginlib.
- Coverage paths (mowing, field rows, large-area cleaning) with opennav_coverage and Fields2Cover.
- Trying A*, Hybrid A*, RRT or RRT* on a map before committing to a plugin.

Elsewhere: Nav2 bringup, costmap layers and inflation, footprint, AMCL, the behavior tree, goals and
waypoints in [nav-nav2](../nav-nav2/SKILL.md); footprint geometry from the URDF in
[ros2-robot-description](../ros2-robot-description/SKILL.md); `cmd_vel` into the wheels in
[ros2-control](../ros2-control/SKILL.md); maps in [perception-slam](../perception-slam/SKILL.md); the
simulated robot in [sim-gazebo](../sim-gazebo/SKILL.md). Arm motion planning with MoveIt 2 and OMPL is the
later `manip-moveit2` skill.

## Pick the plugins

| Robot | Global planner | Controller |
|---|---|---|
| Differential, round | NavFn, Smac 2D or Theta* | MPPI `DiffDrive`; RPP for exact tracking; DWB |
| Differential or omni, not round | Smac State Lattice (`diff` / `omni` primitives) | MPPI with footprint checks, or RPP |
| Omnidirectional | NavFn, Smac 2D, Theta*; Lattice `omni` | MPPI `Omni`; DWB with y sampling |
| Ackermann | Smac Hybrid-A* (`DUBIN`, or `REEDS_SHEPP` to reverse) or Lattice `ackermann` | MPPI `Ackermann`; RPP without rotate-in-place; Vector Pursuit |
| Legged | Smac Hybrid-A*, or a 2D planner if it turns in place | MPPI (`DiffDrive` or `Omni` per gait), RPP, Graceful |

- Put the Rotation Shim in front of RPP, DWB or MPPI when a robot that turns in place gets paths from
  NavFn, Theta* or Smac 2D. Never on Ackermann; not needed with Hybrid-A* or Lattice paths.
- A smoother helps NavFn and Theta* paths; Smac planners smooth internally.
- Jazzy's `nav2_params.yaml` ships NavFn (Dijkstra) and MPPI. With no plugin list set, the servers fall
  back to NavFn and DWB.

The reasoning and trade-offs are in [choose a Nav2 planner and controller](../../wiki/guides/choose-a-nav2-planner-and-controller.md).

## Quick start

Swap in a planner and controller and prove both load and work:

```bash
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup
cp /opt/ros/jazzy/share/nav2_bringup/params/nav2_params.yaml ~/ros2_ws/src/my_robot_navigation/config/
# Edit planner_server.GridBased and controller_server.FollowPath from references/planners.md and
# references/controllers.md; keep the IDs GridBased and FollowPath. Then bring Nav2 up (nav-nav2).
ros2 param get /planner_server GridBased.plugin
ros2 param get /controller_server FollowPath.plugin
ros2 action send_goal /compute_path_to_pose nav2_msgs/action/ComputePathToPose \
  "{goal: {header: {frame_id: map}, pose: {position: {x: 2.0, y: 1.0}, orientation: {w: 1.0}}}, planner_id: GridBased}"
```

The result must show `error_code: 0` and a `planning_time` well below the replanning period (the default
BT replans at 1 Hz). Then send a NavigateToPose goal from RViz and watch `/plan` and `/cmd_vel_nav` (the
controller's output in the bringup launch files; the velocity smoother and collision monitor turn it into
`/cmd_vel`).

## Workflow

1. **Write down the robot.** Drive type; minimum turning radius (Ackermann, from the steering geometry);
   whether it can turn in place; maximum speeds and accelerations (the drive controller's limits, not the
   motor datasheet's); footprint polygon or radius; the CPU it runs on.
   *Check:* every number has its source (measured, datasheet, controller YAML) and matches the
   ros2-control limits.

2. **Choose the plugins** from the table, or the guide when two fit.
   *Check:* each type string is spelled with `::` as in [planners.md](references/planners.md) and
   [controllers.md](references/controllers.md) (Humble slash names fail in Jazzy).

3. **Get the inputs the planners depend on right** (configured in nav-nav2): a `footprint` polygon for
   non-round robots in both costmaps; an inflation radius at least the circumscribed radius for Hybrid-A*,
   Lattice and MPPI; a wide, gentle inflation gradient so planners keep to the middle of corridors; global
   costmap resolution equal to the lattice file's; a local costmap at least `2 x vx_max x horizon` wide for
   MPPI.
   *Check:* no `The inflation radius (...) is smaller than the circumscribed radius` error at start-up;
   the global costmap in RViz shows cost falling off across the full width of corridors.

4. **Configure the planner.** Copy the block for your planner from
   [planners.md](references/planners.md), change only the keys your robot needs, and set
   `expected_planner_frequency` to a rate the planner meets.
   *Check:* the log says `Created global planner plugin GridBased of type ...`; ComputePathToPose returns
   code 0 for ten goals across the map; feasible planners' paths respect the turning radius in RViz; no
   `Planner loop missed its desired rate` warnings.

5. **Add a smoother if paths are jagged.** Configure `smoother_server`, then add a `SmoothPath` node to
   the BT (nav-nav2): the default Jazzy BTs never call it.
   *Check:* `/plan_smoothed` appears, keeps start and goal, and stays out of inflated cost.

6. **Configure the controller.** Copy its block from [controllers.md](references/controllers.md); set the
   motion model and limits from step 1, `controller_frequency`, and the goal checker tolerances.
   *Check:* the log says `Created controller : FollowPath of type ...`; in simulation the robot follows a
   straight 3 m path and a 90° corner; `/cmd_vel_nav` stays inside the limits; no `Control loop missed its
   desired rate` warnings.

7. **Tune on a fixed course.** Use one map and the same five goals in simulation
   ([sim-gazebo](../sim-gazebo/SKILL.md), or `nav2_bringup`'s `tb3_loopback_simulation.launch.py` for a
   quick kinematic check). Change one parameter at a time; record goals reached, time, recoveries and the
   closest approach to obstacles; record `/cmd_vel_nav`, `/plan` and odometry in a bag for PlotJuggler.
   *Check:* three runs per setting give consistent numbers; the chosen setting beats the baseline on the
   numbers, not on looks.

8. **Write a plugin only when no plugin fits.** Planner: [plugin-planner.md](references/plugin-planner.md);
   controller: [plugin-controller.md](references/plugin-controller.md).
   *Check:* `ros2 plugin list --package my_robot_nav_plugins` lists it; the server log names its type; a
   goal behind a wall fails with the right error code.

9. **Coverage.** Build opennav_coverage from source (no distro releases it) and configure its server
   and navigator: [coverage.md](references/coverage.md).
   *Check:* the swaths in RViz are `operation_width` apart and inside the field minus the headland; the
   demo field completes in simulation.

10. **Prototype outside ROS** when the algorithm is the question: PythonRobotics or the A* script in
    [prototyping.md](references/prototyping.md), on the saved map.
    *Check:* the script finds a path on the same map and goals that Nav2 uses, and the comparison is
    recorded with its command.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `Failed to create global planner` / controller, class does not exist | Type string with a slash or typo, or package not installed | Jazzy `::` names; `ros2 plugin list`; install the package |
| `planner GridBased is not a valid planner` | Plugin ID renamed but the BT still asks for `GridBased` / `FollowPath` | Keep the IDs, or change the BT's selectors |
| A parameter change does nothing | Key under the wrong plugin ID or a key that plugin does not have (ignored silently) | `ros2 param get /planner_server GridBased.<key>` |
| Hybrid-A* or Lattice takes seconds | Inflation radius below the circumscribed radius; huge open map | Raise the inflation radius; `cache_obstacle_heuristic` in static maps; downsample |
| Smac uses up all iterations near a gap | A gap too small to pass but not inflated shut (map artefact) | Fill the gap in the map or pad the footprint |
| Paths hug walls or cut corners | Inflation steep and narrow; low cost weights | Wider, gentler inflation; raise `cost_penalty`, `cost_travel_multiplier` or `w_traversal_cost` |
| DWB never moves the robot | Its kinematic limits default to 0.0 | Set `max_vel_x`, `max_speed_xy`, `max_vel_theta`, accelerations |
| Omni robot will not strafe | `min_y_velocity_threshold: 0.5` from the bringup file; `DiffDrive` model; `vy_samples` 1 | 0.001; MPPI `Omni`; DWB `max_vel_y` and `vy_samples` |
| Car-like robot tries to turn in place | RPP `use_rotate_to_heading` defaults to `true`; Rotation Shim; a 2D planner | `false`; drop the shim; Hybrid-A* or Lattice |
| Robot will not take reversing segments | RPP `allow_reversing: false`; MPPI `vx_min: 0`; `PreferForwardCritic` | `allow_reversing: true` with `use_rotate_to_heading: false`; `vx_min` < 0, `enforce_path_inversion: true` |
| MPPI misses its control rate | `batch_size`, `time_steps` or `visualize: true` too heavy for the CPU (MPPI is CPU only) | Lower `batch_size` first; `visualize: false`; or lower `controller_frequency`, keeping `model_dt` at or below its period |
| MPPI will not reach `vx_max`, hesitates | Horizon reaches past the local costmap | Widen the local costmap or shorten the horizon |
| MPPI wobbles in corridors or stalls at the edge of cost | `CostCritic` weight out of balance with the inflation | Retune it with the inflation, then `PathFollowCritic` (MPPI README) |
| RPP oscillates on straights or cuts corners | Lookahead too short or too long for the speed | Velocity-scaled lookahead with `min/max_lookahead_dist` |
| Robot spins or creeps at the goal | Yaw tolerance tighter than the controller can hold | Loosen `yaw_goal_tolerance`; keep `stateful: true` |
| Smoother configured but paths unchanged | No `SmoothPath` node in the BT | Add it (nav-nav2) |

## Checks

Before reporting planning and control done:

- The server logs name the intended plugin types; `ros2 param get` returns the values you set.
- No inflation-radius error and no missed-rate warnings over a full run.
- Ten ComputePathToPose goals across the map return code 0 within the replanning period; feasible
  planners honour the turning radius.
- The fixed course completes three times without collisions, with the numbers recorded alongside the
  parameter file and the commit.
- The controller's output (`/cmd_vel_nav` with the bringup launch files) never exceeds the limits in the
  drive controller.
- Custom plugins appear in `ros2 plugin list` and fail with the right error codes.

## Distro differences

- **Lyrical** (Nav2 1.5.3): plugins use `nav2::LifecycleNode` and `nav2::TransformBuffer` from
  `nav2_ros_common`; `createPlan` takes a viapoints vector; controllers get `newPathReceived` and the
  transformed plan in `computeVelocityCommands`. Path pruning moves to the controller server
  (`path_handler_plugins`, `nav2_controller::FeasiblePathHandler`), so `prune_distance`,
  `transform_tolerance`, `max_robot_pose_search_dist` and MPPI's `enforce_path_inversion` leave the
  controller blocks; RPP loses `stateful`. MPPI's `motion_model` names a plugin namespace
  (`motion_model: "diff_drive"` with `diff_drive.plugin: "mppi::DiffDriveMotionModel"`; a Jazzy
  `"DiffDrive"` value fails). Rotation Shim's primary controller keys move under `primary_controller:`
  with a `plugin:` key. Details in the plugin references.
- **Humble** (Nav2 1.1.20): planner types use slashes (`nav2_navfn_planner/NavfnPlanner`,
  `nav2_smac_planner/SmacPlannerHybrid`, `nav2_theta_star_planner/ThetaStarPlanner`); the controller
  server takes `progress_checker_plugin` (singular); `createPlan` has no cancel checker; the bringup
  controller is DWB.
- opennav_coverage is released for no distro; it has `humble`, `jazzy`, `jazzy-v2`, `kilted` and
  `lyrical` branches to build from source.

## Related

- References: [planners.md](references/planners.md), [controllers.md](references/controllers.md),
  [plugin-planner.md](references/plugin-planner.md), [plugin-controller.md](references/plugin-controller.md),
  [coverage.md](references/coverage.md), [prototyping.md](references/prototyping.md).
- Wiki: [choose a Nav2 planner and controller](../../wiki/guides/choose-a-nav2-planner-and-controller.md),
  [Nav2](../../wiki/software/nav2.md), [PythonRobotics](../../wiki/software/pythonrobotics.md),
  [ROS 2](../../wiki/tools/ros2.md), [Gazebo](../../wiki/tools/gazebo.md),
  [PlotJuggler](../../wiki/tools/plotjuggler.md), [Foxglove](../../wiki/tools/foxglove.md).
- Skills: [nav-nav2](../nav-nav2/SKILL.md), [ros2-control](../ros2-control/SKILL.md),
  [ros2-robot-description](../ros2-robot-description/SKILL.md), [perception-slam](../perception-slam/SKILL.md),
  [sim-gazebo](../sim-gazebo/SKILL.md), [ros2-core](../ros2-core/SKILL.md); later `manip-moveit2`.
- Upstream: docs.nav2.org (tuning guide, plugin configuration pages, plugin tutorials, migration guides),
  the package READMEs on the navigation2 `jazzy` branch (Smac, MPPI, lattice primitive generator), the
  opennav_coverage README, PythonRobotics; LaValle, *Planning Algorithms* (lavalle.pl); Dolgov et al.,
  "Practical Search Techniques in Path Planning for Autonomous Driving" (Hybrid A*).
