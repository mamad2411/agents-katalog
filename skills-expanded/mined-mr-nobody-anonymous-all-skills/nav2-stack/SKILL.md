---
name: nav2-stack
description: "Use when configuring, customizing, or debugging the ROS2 Nav2 navigation stack — bringup, behavior trees, planner/controller servers, costmap layers, keepout/speed zones, waypoint following, or diagnosing failures like a broken TF tree, stale costmaps, or a robot spinning in place. Provides full-stack Nav2 anatomy, lifecycle ordering, BT XML patterns, and production-tested parameter values."
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


# ROS2 Nav2 Stack

Nav2 is not a monolith. It is a federation of ~10 lifecycle-managed servers coordinated by a behavior tree. Almost every "Nav2 is broken" report traces to one of three things: a bad TF tree, a misconfigured costmap, or a lifecycle node that never reached `active`. Internalize the architecture below and you can localize any failure in minutes.

Target versions: Nav2 for Humble/Iron/Jazzy. API differences are flagged inline. Default DDS assumptions: CycloneDDS or FastDDS with default QoS unless noted.

---

## 1. Full Stack Anatomy

```
                    ┌─────────────────────────────┐
  NavigateToPose ──▶│      bt_navigator           │  loads BT XML, ticks @ 10–100 Hz
  (action)          │  (BehaviorTreeEngine)       │
                    └──────┬──────────┬───────────┘
            ComputePathToPose      FollowPath        (BT action nodes = ROS action clients)
                    │                  │
        ┌───────────▼─────┐   ┌────────▼──────────┐
        │ planner_server  │   │ controller_server │
        │  - NavFn        │   │  - DWB / MPPI /   │
        │  - SmacHybrid   │   │    RPP            │
        │  - SmacLattice  │   │  - progress_checker│
        │  - ThetaStar    │   │  - goal_checker   │
        └───────┬─────────┘   └────────┬──────────┘
          global_costmap         local_costmap
          (static + obstacle      (obstacle/voxel +
           + inflation)            inflation, rolling)
                    │                  │
        ┌───────────▼──────────────────▼───────────┐
        │ behavior_server (recoveries): spin,      │
        │ backup, drive_on_heading, wait,          │
        │ assisted_teleop                          │
        ├───────────────────────────────────────────┤
        │ smoother_server   - path smoothing       │
        │ velocity_smoother - cmd_vel accel limits │
        │ collision_monitor - last-resort safety   │
        │ waypoint_follower - multi-goal sequencing│
        │ map_server / map_saver                   │
        │ amcl (or slam_toolbox) - localization    │
        └───────────────────────────────────────────┘
                    lifecycle_manager(s) orchestrate all of the above
```

Key topics/actions:

| Interface | Type | Producer → Consumer |
|---|---|---|
| `/navigate_to_pose` | action `nav2_msgs/NavigateToPose` | your code → bt_navigator |
| `/navigate_through_poses` | action | your code → bt_navigator |
| `/follow_waypoints` | action `nav2_msgs/FollowWaypoints` | your code → waypoint_follower |
| `/compute_path_to_pose` | action | bt_navigator → planner_server |
| `/follow_path` | action | bt_navigator → controller_server |
| `/cmd_vel` | `geometry_msgs/Twist` (`TwistStamped` in Jazzy+ if `enable_stamped_cmd_vel`) | controller → velocity_smoother → collision_monitor → base |
| `/local_costmap/costmap`, `/global_costmap/costmap` | `nav_msgs/OccupancyGrid` | costmap_2d → rviz/you |
| `/plan` | `nav_msgs/Path` | planner_server (visualization) |

The cmd_vel chain matters: if you run `velocity_smoother` and `collision_monitor`, the topic remapping must chain `cmd_vel_nav → cmd_vel_smoothed → cmd_vel`. A robot that "ignores" navigation commands often has a broken link in this chain — check with `ros2 topic info /cmd_vel --verbose` and confirm exactly one publisher.

### Required TF tree

```
map ──(amcl or slam_toolbox)──▶ odom ──(wheel odometry / robot_localization EKF)──▶ base_link ──(URDF, robot_state_publisher)──▶ sensors
```

Non-negotiable invariants:
- Exactly ONE publisher per transform edge. Two nodes publishing `odom→base_link` (e.g., both the base driver and an EKF) produces a jittering robot and planner failures. Decide who owns it.
- `map→odom` is published by the localizer and may jump (it represents correction). `odom→base_link` must be continuous and smooth.
- All sensor frames must connect to `base_link` via static transforms (URDF). A LiDAR whose frame is orphaned means the obstacle layer silently drops every scan.
- Use `frame_id: base_link`? No — Nav2 convention: `robot_base_frame: base_link`, `global_frame: map` (global costmap), `global_frame: odom` (local costmap). Setting local costmap global_frame to `map` makes obstacles smear when AMCL corrects pose.

Verify before anything else:
```bash
ros2 run tf2_tools view_frames          # generates frames.pdf
ros2 run tf2_ros tf2_echo map base_link  # must succeed, with recent timestamps
ros2 run tf2_ros tf2_echo odom base_link
```

---

## 2. Lifecycle Bringup — Order Matters

Every Nav2 server is a `LifecycleNode`: `unconfigured → inactive (on_configure) → active (on_activate)`. The `lifecycle_manager` walks its `node_names` list IN ORDER, configuring then activating each. Wrong order = deadlock or silent failure.

Canonical two-manager pattern (matches `nav2_bringup`):

```yaml
lifecycle_manager_localization:
  ros__parameters:
    autostart: true
    node_names: ['map_server', 'amcl']
    bond_timeout: 4.0

lifecycle_manager_navigation:
  ros__parameters:
    autostart: true
    node_names:
      - controller_server
      - smoother_server
      - planner_server
      - behavior_server
      - velocity_smoother
      - collision_monitor
      - bt_navigator
      - waypoint_follower
    bond_timeout: 4.0
```

Why this order:
1. `map_server` before `amcl` — AMCL needs the map (via `/map` topic or `map` service).
2. Costmap-owning servers (`controller_server`, `planner_server`) before `bt_navigator` — the BT's action clients wait for their action servers; if bt_navigator activates first, its `on_configure` may time out waiting for `/compute_path_to_pose`.
3. `bt_navigator` near last; `waypoint_follower` last (it is a client of bt_navigator).

Bond mechanism: each server maintains a `bond` heartbeat with the lifecycle manager. If a server crashes, the manager detects bond loss and (with `attempt_respawn_reconnection: true` on Iron+) can reconnect after respawn. `bond_timeout: 0.0` disables this — useful in simulation where clock pauses break bonds, dangerous in production.

Manual lifecycle control for debugging:
```bash
ros2 lifecycle get /controller_server                 # what state is it in?
ros2 lifecycle set /controller_server configure
ros2 lifecycle set /controller_server activate
ros2 service call /lifecycle_manager_navigation/manage_nodes \
  nav2_msgs/srv/ManageLifecycleNodes "{command: 2}"   # 0=startup 1=pause 2=resume 3=reset 4=shutdown
```

A node stuck in `unconfigured` after launch almost always means `on_configure` threw — read ITS log, not the lifecycle manager's. Common causes: malformed YAML (a string where a double is expected), plugin name typo (`nav2_navfn_planner/NavfnPlanner` vs `nav2_navfn_planner::NavfnPlanner` — Humble uses `/`, Jazzy uses `::`), missing map file path.

### Sim time
Every single node, including lifecycle managers and rviz, must agree on `use_sim_time`. A mixed setup yields TF extrapolation errors (`Lookup would require extrapolation into the future/past`). Pass it globally in launch:

```python
DeclareLaunchArgument('use_sim_time', default_value='true')
# and in every Node(parameters=[{'use_sim_time': use_sim_time}, params_file])
```

---

## 3. Costmap Layers — Where 80% of Tuning Lives

A costmap is an ordered pipeline of layer plugins; each layer writes costs into the master grid. Order matters: inflation must come LAST so it inflates everything beneath it.

```yaml
global_costmap:
  global_costmap:
    ros__parameters:
      global_frame: map
      robot_base_frame: base_link
      update_frequency: 1.0          # Hz; global can be slow
      publish_frequency: 1.0
      resolution: 0.05               # match your map resolution
      robot_radius: 0.22             # OR footprint: "[[x1,y1],...]" — never both
      track_unknown_space: true      # false = unknown treated as free (dangerous outdoors of map)
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: true
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: true
        observation_sources: scan
        scan:
          topic: /scan
          data_type: "LaserScan"
          max_obstacle_height: 2.0
          clearing: true             # raytrace free space
          marking: true              # mark obstacles
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5    # MUST be < raytrace_max_range or obstacles never clear
          obstacle_min_range: 0.0
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0     # lower = costs decay slower = robot stays further from walls
        inflation_radius: 0.55       # >= robot_radius + safety margin; rule of thumb: 2-3x robot radius

local_costmap:
  local_costmap:
    ros__parameters:
      global_frame: odom             # NOT map — see TF section
      robot_base_frame: base_link
      rolling_window: true
      width: 3                       # meters; must contain controller lookahead
      height: 3
      resolution: 0.05
      update_frequency: 5.0          # local must be fast: >= controller_frequency / 4
      publish_frequency: 2.0
      plugins: ["obstacle_layer", "inflation_layer"]   # no static layer locally
      # obstacle_layer / inflation_layer same shape as above
```

Layer cheat sheet:

| Layer | Plugin | Use |
|---|---|---|
| Static | `nav2_costmap_2d::StaticLayer` | map from map_server; global costmap only |
| Obstacle | `nav2_costmap_2d::ObstacleLayer` | 2D LiDAR/scan marking + raytrace clearing |
| Voxel | `nav2_costmap_2d::VoxelLayer` | 3D (depth cam, 3D LiDAR); set `publish_voxel_map: true` only for debug — it is expensive |
| Range | `nav2_costmap_2d::RangeSensorLayer` | sonar/IR cones |
| Inflation | `nav2_costmap_2d::InflationLayer` | exponential cost decay around lethal cells; ALWAYS LAST |
| Keepout | `nav2_costmap_2d::KeepoutFilter` | costmap filter — see §5 |
| Speed | `nav2_costmap_2d::SpeedFilter` | costmap filter — see §5 |
| Denoise | `nav2_costmap_2d::DenoiseLayer` (Iron+) | removes salt-and-pepper sensor noise |

Cost values: 254 = lethal, 253 = inscribed (robot center here = collision), 252→1 = inflated decay, 0 = free, 255 = unknown. The inflation function: `cost = 251 * exp(-cost_scaling_factor * (distance - inscribed_radius))`. If your robot hugs walls then clips them on corners, your `inflation_radius` is too small or you used `robot_radius` for a non-circular robot — switch to `footprint` and verify with the published `/local_costmap/published_footprint`.

**Production killer — obstacles never clear:** `clearing: true` requires the scan to raytrace THROUGH the stale obstacle cell. If `raytrace_max_range` < distance to the ghost obstacle, it persists forever. Also: data dropped due to `max_obstacle_height` (e.g., LiDAR mounted at 2.1 m with default max 2.0) marks nothing AND clears nothing. Check with:
```bash
ros2 topic echo /local_costmap/costmap_updates --no-arr   # is it updating at all?
```

**Production killer — costmap freezes:** sensor QoS mismatch. Most LiDAR drivers publish `BEST_EFFORT`; the obstacle layer's default subscription is compatible, but if you've overridden QoS or use a relayed topic with `RELIABLE`-only publisher, you get zero callbacks and no warning. `ros2 topic info /scan --verbose` and compare publisher vs subscriber QoS.

---

## 4. Planner and Controller Servers

### Planner selection

| Plugin | Robot type | Notes |
|---|---|---|
| `nav2_navfn_planner::NavfnPlanner` | differential/omni, circular | Dijkstra/A* on 2D grid; ignores orientation; fast; default |
| `nav2_smac_planner::SmacPlannerHybrid` | ackermann, legged, large non-circular diff | Hybrid-A*, kinematically feasible paths, respects `minimum_turning_radius` |
| `nav2_smac_planner::SmacPlanner2D` | circular diff/omni | A* with cost-aware smoothing |
| `nav2_smac_planner::SmacPlannerLattice` | any with motion primitives | state lattice; custom primitive files |
| `nav2_theta_star_planner::ThetaStarPlanner` | diff/omni | any-angle, fewer waypoint kinks |

```yaml
planner_server:
  ros__parameters:
    expected_planner_frequency: 1.0   # warns if planning slower; 0 disables
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner::NavfnPlanner"   # "/" separator on Humble
      tolerance: 0.5                  # accept goals within 0.5 m if exact cell blocked
      allow_unknown: true             # false strands robots at map edges
```

For SmacHybrid the parameters that actually matter: `minimum_turning_radius` (set to your real vehicle's, in meters — too small produces undrivable paths), `motion_model_for_search: "DUBIN"` (forward only) vs `"REEDS_SHEPP"` (allows reversing), `cost_penalty: 2.0` (higher = stays further from obstacles, slower search).

### Controller selection

| Plugin | Best for | Avoid when |
|---|---|---|
| MPPI (`nav2_mppi_controller::MPPIController`) | dynamic environments, smooth motion, diff/omni/ackermann | CPU-starved platforms (needs ~1 core at 30 Hz) |
| DWB (`dwb_core::DWBLocalPlanner`) | legacy, highly tunable via critics | you don't have a week to tune critics |
| RPP (`nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController`) | path-following AGVs, predictable industrial motion | obstacle-dense dynamic spaces (no avoidance — relies on path quality + collision detection to stop) |
| Rotation Shim (`nav2_rotation_shim_controller::RotationShimController`) | wrapper: rotate-to-heading first, then delegate | nonholonomic robots that can't rotate in place |

Recommended modern default (Iron+): MPPI. Starting config:

```yaml
controller_server:
  ros__parameters:
    controller_frequency: 20.0        # MUST be achievable; if loop overruns, Nav2 logs "Control loop missed its desired rate"
    failure_tolerance: 0.3            # seconds of controller exceptions tolerated before FollowPath aborts
    progress_checker_plugins: ["progress_checker"]
    goal_checker_plugins: ["general_goal_checker"]
    controller_plugins: ["FollowPath"]

    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5   # must move 0.5 m ...
      movement_time_allowance: 10.0   # ... every 10 s, else FollowPath fails → BT triggers recovery

    general_goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25        # rad; 0.05 with a real robot = endless terminal wiggle. Don't.
      stateful: true                  # once xy reached, don't re-chase xy while rotating to yaw

    FollowPath:
      plugin: "nav2_mppi_controller::MPPIController"
      time_steps: 56
      model_dt: 0.05                  # MUST equal 1/controller_frequency
      batch_size: 2000
      vx_max: 0.5                     # your robot's real max, derated 10-20%
      vx_min: -0.35
      wz_max: 1.9
      ax_max: 3.0
      motion_model: "DiffDrive"       # or "Omni", "Ackermann"
      critics: ["ConstraintCritic", "ObstaclesCritic", "GoalCritic",
                "GoalAngleCritic", "PathAlignCritic", "PathFollowCritic",
                "PathAngleCritic", "PreferForwardCritic"]
      ObstaclesCritic:
        repulsion_weight: 1.5
        critical_weight: 20.0
        consider_footprint: false     # true = accurate for non-circular but ~2x cost
```

`model_dt = 1/controller_frequency` is a hard correctness requirement for MPPI, not a suggestion.

### Velocity smoother + collision monitor (production safety chain)

```yaml
velocity_smoother:
  ros__parameters:
    smoothing_frequency: 20.0
    max_velocity: [0.5, 0.0, 2.0]     # vx, vy, wz
    max_accel: [2.5, 0.0, 3.2]
    max_decel: [-2.5, 0.0, -3.2]
    deadband_velocity: [0.0, 0.0, 0.0]
    velocity_timeout: 1.0             # zero cmd_vel if input stalls — your watchdog

collision_monitor:
  ros__parameters:
    base_frame_id: base_link
    cmd_vel_in_topic: cmd_vel_smoothed
    cmd_vel_out_topic: cmd_vel
    polygons: ["PolygonStop", "PolygonSlow"]
    PolygonStop:
      type: polygon
      points: "[[0.4,0.3],[0.4,-0.3],[0.0,-0.3],[0.0,0.3]]"
      action_type: stop
      min_points: 4                    # require N lidar points inside before triggering (noise immunity)
    PolygonSlow:
      type: polygon
      points: "[[0.8,0.5],[0.8,-0.5],[0.0,-0.5],[0.0,0.5]]"
      action_type: slowdown
      slowdown_ratio: 0.3
    observation_sources: ["scan"]
    scan:
      type: scan
      topic: /scan
```

The collision monitor is your last line — it acts on raw sensor data, independent of costmaps, planners, and localization. Every robot near humans should run it. It is NOT a substitute for a hardware-rated safety LiDAR with a certified safety controller; it shares the same compute, OS, and DDS as everything else.

---

## 5. Keepout Zones and Speed Restriction Zones

Both are "costmap filters": a separate filter mask (an OccupancyGrid published by its own map_server) interpreted via `CostmapFilterInfo`.

Architecture: **mask map_server → costmap_filter_info_server → filter layer plugin in costmap**.

### Keepout zones

1. Create the mask: copy your map PGM, paint keepout regions BLACK (occupied = keepout). Same origin/resolution as the main map is conventional (not strictly required — masks are georeferenced independently).
2. Launch the infrastructure:

```yaml
filter_mask_server:           # a nav2_map_server::MapServer instance
  ros__parameters:
    yaml_filename: "keepout_mask.yaml"
    topic_name: "/keepout_filter_mask"

costmap_filter_info_server:   # nav2_map_server::CostmapFilterInfoServer
  ros__parameters:
    type: 0                   # 0 = keepout/lanes, 1 = speed limit (%), 2 = speed limit (m/s)
    filter_info_topic: "/costmap_filter_info"
    mask_topic: "/keepout_filter_mask"
    base: 0.0
    multiplier: 1.0
```

3. Add the filter to BOTH costmaps (keepout in global only = planner avoids it but controller will happily cut through; keepout in local only = planner plans straight through it and the robot stalls at the boundary):

```yaml
filters: ["keepout_filter"]            # note: 'filters' param, kept separate from 'plugins' so filters apply above all layers
keepout_filter:
  plugin: "nav2_costmap_2d::KeepoutFilter"
  enabled: true
  filter_info_topic: "/costmap_filter_info"
```

Add both servers to a lifecycle manager or they will sit `unconfigured` and the filter logs `Filter info has not been received` forever — the single most common keepout failure.

### Speed restriction zones

Mask encoding: darker = lower speed. With `type: 1`, the filter computes `speed_% = base + multiplier * mask_value(0..100)`. The SpeedFilter goes in the **global costmap only** and publishes `nav2_msgs/SpeedLimit` on `/speed_limit`, which `controller_server` subscribes to (`speed_limit_topic` param) and uses to cap commanded velocity.

```yaml
speed_filter:
  plugin: "nav2_costmap_2d::SpeedFilter"
  enabled: true
  filter_info_topic: "/costmap_filter_info_speed"   # separate info server from keepout!
  speed_limit_topic: "/speed_limit"
```

Each filter needs its own `CostmapFilterInfoServer` + mask map_server pair. Sharing one info topic between keepout and speed silently corrupts both.

---

## 6. Behavior Tree Customization

bt_navigator loads an XML BT per navigator plugin: `default_nav_to_pose_bt_xml` and `default_nav_through_poses_bt_xml`. Stock trees live in `/opt/ros/$ROS_DISTRO/share/nav2_bt_navigator/behavior_trees/`. The goal can also carry a `behavior_tree` field to select a tree per-request.

Stock `navigate_to_pose_w_replanning_and_recovery.xml`, conceptually:

```xml
<root main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <RecoveryNode number_of_retries="6" name="NavigateRecovery">
      <PipelineSequence name="NavigateWithReplanning">
        <RateController hz="1.0">                       <!-- replan at 1 Hz -->
          <RecoveryNode number_of_retries="1" name="ComputePathToPose">
            <ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"/>
            <ClearEntireCostmap name="ClearGlobalCostmap-Context"
                                service_name="global_costmap/clear_entirely_global_costmap"/>
          </RecoveryNode>
        </RateController>
        <RecoveryNode number_of_retries="1" name="FollowPath">
          <FollowPath path="{path}" controller_id="FollowPath"/>
          <ClearEntireCostmap name="ClearLocalCostmap-Context"
                              service_name="local_costmap/clear_entirely_local_costmap"/>
        </RecoveryNode>
      </PipelineSequence>
      <ReactiveFallback name="RecoveryFallback">
        <GoalUpdated/>
        <RoundRobin name="RecoveryActions">
          <Sequence name="ClearingActions">
            <ClearEntireCostmap name="ClearLocalCostmap" service_name="local_costmap/clear_entirely_local_costmap"/>
            <ClearEntireCostmap name="ClearGlobalCostmap" service_name="global_costmap/clear_entirely_global_costmap"/>
          </Sequence>
          <Spin spin_dist="1.57"/>
          <Wait wait_duration="5"/>
          <BackUp backup_dist="0.30" backup_speed="0.05"/>
        </RoundRobin>
      </ReactiveFallback>
    </RecoveryNode>
  </BehaviorTree>
</root>
```

Reading rules:
- `PipelineSequence` re-ticks earlier children while later ones run — this is how planning keeps replanning while FollowPath executes.
- `RecoveryNode` (Nav2 custom): child 1 = task, child 2 = recovery; on task failure, run recovery then retry task, up to `number_of_retries`.
- `RoundRobin` cycles which recovery runs on each successive failure.
- Blackboard variables `{goal}`, `{path}` are how nodes share data.

Common customizations:

**Remove Spin for robots that must not rotate in place** (ackermann, robots with trailers): delete `<Spin/>` from RecoveryActions, and use SmacPlannerHybrid + RPP/MPPI with `motion_model: Ackermann`.

**Conditional replanning instead of 1 Hz** (saves CPU, avoids path oscillation on long corridors):
```xml
<RateController hz="0.333">
  <ReactiveSequence>
    <Inverter><PathExpiringTimer seconds="10" path="{path}"/></Inverter>
    ...
  </ReactiveSequence>
</RateController>
```
Or replan only when blocked: wrap with `<IsPathValid path="{path}"/>` in a Fallback.

**Custom BT node plugin** (C++):
```cpp
#include "behaviortree_cpp/action_node.h"   // behaviortree_cpp_v3 on Humble

class CheckBattery : public BT::ConditionNode {
public:
  CheckBattery(const std::string &name, const BT::NodeConfig &conf)
    : BT::ConditionNode(name, conf) {
    node_ = config().blackboard->get<rclcpp::Node::SharedPtr>("node");
    sub_ = node_->create_subscription<sensor_msgs::msg::BatteryState>(
      "/battery_state", rclcpp::SystemDefaultsQoS(),
      [this](sensor_msgs::msg::BatteryState::SharedPtr msg){ level_ = msg->percentage; });
  }
  static BT::PortsList providedPorts() {
    return { BT::InputPort<double>("min_level", 0.2, "abort threshold") };
  }
  BT::NodeStatus tick() override {
    double min_level = 0.2;
    getInput("min_level", min_level);
    return level_ > min_level ? BT::NodeStatus::SUCCESS : BT::NodeStatus::FAILURE;
  }
private:
  rclcpp::Node::SharedPtr node_;
  rclcpp::Subscription<sensor_msgs::msg::BatteryState>::SharedPtr sub_;
  double level_{1.0};
};

#include "behaviortree_cpp/bt_factory.h"
BT_REGISTER_NODES(factory) {
  factory.registerNodeType<CheckBattery>("CheckBattery");
}
```
Register in params: `bt_navigator.ros__parameters.plugin_lib_names: [..., "check_battery_bt_node"]`. On Jazzy+ the default node list is internal; you only list ADDITIONAL plugins.

Debug BTs with Groot2: set `bt_navigator: ros__parameters: ` → Humble: ZMQ publisher built in; Iron+: connect Groot2 to port 1667. Watching which node is ticking RUNNING in real time turns "robot is stuck" into "FollowPath has been RUNNING for 40 s with no progress" instantly.

---

## 7. Waypoint Following

`waypoint_follower` wraps `NavigateToPose` calls in sequence, with a `TaskExecutor` plugin executed at each arrival.

```yaml
waypoint_follower:
  ros__parameters:
    loop_rate: 20
    stop_on_failure: false          # true = entire mission aborts if one waypoint unreachable
    waypoint_task_executor_plugin: "wait_at_waypoint"
    wait_at_waypoint:
      plugin: "nav2_waypoint_follower::WaitAtWaypoint"
      waypoint_pause_duration: 200  # ms
```

Built-in executors: `WaitAtWaypoint`, `PhotoAtWaypoint`, `InputAtWaypoint` (waits for an external topic — human confirmation). Write a custom one by implementing `nav2_core::WaypointTaskExecutor::processAtWaypoint()`.

Python client (the pattern you should generate — `nav2_simple_commander` is the supported API):

```python
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped

def make_pose(nav, x, y, yaw_z=0.0, yaw_w=1.0):
    p = PoseStamped()
    p.header.frame_id = 'map'
    p.header.stamp = nav.get_clock().now().to_msg()
    p.pose.position.x, p.pose.position.y = x, y
    p.pose.orientation.z, p.pose.orientation.w = yaw_z, yaw_w   # proper quaternion, NOT euler
    return p

rclpy.init()
nav = BasicNavigator()
nav.setInitialPose(make_pose(nav, 0.0, 0.0))   # seeds AMCL — skip if using slam_toolbox
nav.waitUntilNav2Active()                       # blocks until lifecycle active + amcl localized

waypoints = [make_pose(nav, 2.0, 0.0), make_pose(nav, 2.0, 2.0, 0.707, 0.707)]
nav.followWaypoints(waypoints)
while not nav.isTaskComplete():
    fb = nav.getFeedback()
    # fb.current_waypoint is the index in progress
    rclpy.spin_once(nav, timeout_sec=0.1)

result = nav.getResult()
if result != TaskResult.SUCCEEDED:
    # FollowWaypoints result lists missed_waypoints — handle them
    pass
```

Gotchas:
- Orientation: `FollowWaypoints` historically ignored intermediate waypoint orientations with some goal checkers; if heading at each waypoint matters, verify with your goal checker or use `navigateThroughPoses` (which feeds `navigate_through_poses` BT — smoother, doesn't stop at each pose).
- An all-zeros quaternion `(0,0,0,0)` is invalid and some plugins NaN out. Always set `w=1.0` minimum.
- `waitUntilNav2Active()` hangs forever if amcl never gets an initial pose — set it programmatically or via rviz "2D Pose Estimate" first.

---

## 8. Common Bringup Failures — Diagnostic Playbook

Work top-down. Do not tune parameters until TF and lifecycle are proven good.

### Step 0: Is everything actually active?
```bash
ros2 lifecycle list                      # find lifecycle nodes (Iron+; on Humble enumerate manually)
for n in controller_server planner_server bt_navigator behavior_server; do
  echo -n "$n: "; ros2 lifecycle get /$n; done
```
Anything not `active [3]` → read that node's startup log. YAML typo, plugin name mismatch, or missing dependency.

### Failure: "Timed out waiting for transform map → base_link"
The #1 bringup failure. Decision tree:
1. `ros2 run tf2_ros tf2_echo odom base_link` fails too? → your odometry source isn't publishing TF. Check base driver / robot_localization (`publish_tf: true` in EKF config? Two EKFs fighting?).
2. odom→base_link OK, map→odom missing? → AMCL isn't localized. AMCL only publishes map→odom AFTER receiving an initial pose. Set one (rviz 2D Pose Estimate, `initial_pose` params with `set_initial_pose: true`, or programmatically).
3. Transforms exist but "extrapolation into the past/future"? → `use_sim_time` mismatch (one node on wall clock), or timestamps from a sensor with an unsynced clock (check `ros2 topic echo /scan --field header.stamp` vs `ros2 topic echo /clock`). For multi-machine: chrony/PTP is mandatory; DDS does not fix your clocks.
4. Transform timeout under load? → increase `transform_tolerance` (0.1 → 0.3) in costmaps/amcl as a mitigation, but the root cause is usually CPU saturation or a TF publisher running below 10 Hz. `ros2 topic hz /tf`.

### Failure: costmap not updating
1. `ros2 topic hz /scan` — sensor alive?
2. `ros2 topic info /scan --verbose` — QoS compatible? (BEST_EFFORT pub vs RELIABLE-only sub = silent zero messages.)
3. Scan `frame_id` resolvable to `base_link`? `ros2 run tf2_ros tf2_echo base_link laser_frame`. Orphan frame = silent drop, often only a single throttled warning.
4. `max_obstacle_height` vs actual sensor Z. Sensor data above the ceiling value is discarded entirely.
5. `obstacle_max_range` / `raytrace_max_range` sane for the sensor (and raytrace > obstacle)?
6. Costmap node actually active (step 0)? An `inactive` costmap publishes nothing and warns nothing.
7. Look for `Sensor origin ... is out of map bounds` — local costmap too small or TF wrong by meters (bad static transform sign).

### Failure: robot spins in place
Distinct causes, distinguishable by observation:
1. **Recovery Spin behavior firing repeatedly.** Log shows `Running Spin recovery`. The robot isn't "confused" — planning or control is failing and the BT is cycling recoveries. Find the upstream failure (planner can't find path → goal in lethal space, costmap saturated; controller fails → progress checker triggering). The spin is the symptom, never the disease.
2. **Inverted angular velocity sign.** Robot rotates the WRONG direction, overshoots heading, corrects, overshoots — limit cycle. Test outside Nav2: `ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{angular: {z: 0.5}}"` — robot must rotate counter-clockwise (REP-103). If clockwise, fix the base driver, not Nav2.
3. **Odometry angular scale wrong** (bad wheel separation parameter): commanded 0.5 rad/s, odometry reports 0.8 rad/s → controller fights itself. Validate: rotate the robot exactly 360° physically, check odom yaw delta.
4. **Terminal yaw wiggle at goal**: `yaw_goal_tolerance` too tight for the controller's angular deadband. Raise tolerance or set `stateful: true`.
5. **RotationShim or MPPI rotate-to-heading at path start** is NORMAL — it rotates once toward the path then drives. Only a problem if it never exits rotation: check `angular_dist_threshold` vs your odometry yaw noise.

### Failure: "Control loop missed its desired rate"
Controller can't compute within `1/controller_frequency`. Either lower the frequency (20 → 10 Hz), reduce MPPI `batch_size`/`time_steps`, shrink the local costmap, or pin the process to dedicated cores. Sustained overruns cause jerky motion and spurious FollowPath failures.

### Failure: planner succeeds, robot doesn't move
1. `ros2 topic echo /cmd_vel` — is the controller publishing? If yes and the robot is still: base driver problem or broken cmd_vel relay chain (velocity_smoother input topic remap).
2. cmd_vel nonzero but tiny? `min_vel_x` / deadband below the base's static friction threshold. Set `deadband_velocity` or raise minimum speeds.
3. collision_monitor in `stop` state from a phantom point inside the stop polygon (sensor sees a robot-mounted cable). Set `min_points` ≥ 4 and check the polygon doesn't include robot self-geometry.

### Failure: goals rejected instantly
`bt_navigator` log: `Goal was rejected`. Causes: action server inactive (step 0), goal frame_id not `map`, goal timestamp wildly off (sim time mismatch), or goal pose inside lethal cost with planner `tolerance: 0.0`.

---

## 9. Production Hardening Checklist

- [ ] Single TF publisher per edge; `view_frames` output archived in repo.
- [ ] `use_sim_time` parameterized in launch, never hardcoded per-node.
- [ ] Footprint polygon, not robot_radius, for any non-circular robot. Verify published footprint visually in rviz.
- [ ] Collision monitor active in the cmd_vel chain with a stop polygon ≥ braking distance at vx_max (d = v²/(2·|decel|): at 0.5 m/s with 2.5 m/s² decel → 0.05 m + margin).
- [ ] `velocity_timeout` in velocity_smoother as cmd_vel watchdog; base driver ALSO has its own independent timeout.
- [ ] Keepout filters in BOTH costmaps; speed filter in global; separate filter info servers; filter servers in lifecycle manager.
- [ ] `bond_timeout > 0` with respawn enabled in production launch.
- [ ] Recovery behaviors audited per platform (no Spin/BackUp where physically unsafe).
- [ ] Param files version-controlled; `ros2 param dump` of the live system compared against the repo file in CI (defaults drift between Nav2 releases).
- [ ] Log review for throttled warnings — Nav2 throttles its most important messages (sensor out of bounds, transform timeouts) to once per N seconds; a quiet log is not a clean log. `grep -iE "warn|error" ~/.ros/log/...`.
- [ ] Soak test: 8+ hours of continuous waypoint loops, watching RSS memory of costmap nodes and `/tf` rate. Costmap memory growth usually means a voxel layer with `publish_voxel_map: true` left enabled.
